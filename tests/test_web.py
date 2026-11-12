"""Tests for the Flask platform: gating, scoring, sandbox and APIs.

Every test drives the real app through Flask's test client, so a route that
refuses to open a locked lesson is tested at the HTTP layer, not by calling a
helper directly.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:  # pytest run from elsewhere must still import web/
    sys.path.insert(0, str(ROOT))

from web.app import _split_exercise, create_app  # noqa: E402
from web.content import Catalog  # noqa: E402
from web.runner import ALLOWED_MODULES, check_exercise, run_code  # noqa: E402
from helpers import approve, csrf, login, make_user, signed_in, signup  # noqa: E402

DATA = ROOT / "pybook" / "data"


# --------------------------------------------------------------------- fixtures
@pytest.fixture(scope="module")
def catalog() -> Catalog:
    return Catalog(DATA)

def _answers(items: list[dict]) -> dict:
    return {"q%d" % (index + 1): item["answer"] for index, item in enumerate(items)}


def _lesson(catalog: Catalog, lesson_id: str) -> dict:
    return catalog.lesson(lesson_id)


def _solve(client, catalog: Catalog, lesson_id: str) -> None:
    """Complete every required exercise of a lesson, the way a learner must."""
    for exercise in _lesson(catalog, lesson_id)["exercises"]:
        data = client.post(
            "/api/check/%s" % exercise["id"], json={"code": exercise["solution"]}
        ).get_json()
        assert data["passed"], "%s: %s" % (exercise["id"], data)


# ------------------------------------------------------------------ the pages
def test_homepage_advertises_both_courses_without_a_session(app):
    body = app.test_client().get("/").get_data(as_text=True)
    assert "PyBook" in body
    assert "AI Engineering" in body
    assert "Course enquiry" in body
    assert "Create account" in body
    assert "/signup" in body
    assert "/login" in body
    # an anonymous visitor must not be able to reach a lesson
    assert "/lesson/" not in body


def test_syllabus_pages_are_public(app):
    python_page = app.test_client().get("/courses/pybook")
    ai_page = app.test_client().get("/courses/ai")
    assert python_page.status_code == 200
    assert ai_page.status_code == 200
    assert "Foundations" in ai_page.get_data(as_text=True)
    assert app.test_client().get("/courses/nope").status_code == 404


def test_anonymous_pages_and_apis_need_a_login(app):
    anonymous = app.test_client()
    for path in ("/learn", "/progress", "/playground", "/lesson/m01c01l01", "/exam/m01"):
        response = anonymous.get(path)
        assert response.status_code == 302, path
        assert "/login" in response.headers["Location"], path
    assert anonymous.post("/api/run", json={"code": "print(1)"}).status_code == 401


def test_signup_is_pending_until_an_admin_approves_it(app):
    visitor = app.test_client()

    response = signup(visitor, name="  Asha  ", email="Asha@Example.com", language="hi")
    assert response.status_code == 201
    assert "waiting for approval" in response.get_data(as_text=True)

    account = app.config["STORE"].user_by_email("asha@example.com")
    assert account["status"] == "pending"
    assert account["name"] == "Asha", "the name is whitespace-normalised"
    assert account["password_hash"] != "tester pass 123"

    refused = login(visitor, email="asha@example.com")
    assert refused.status_code == 200
    assert "waiting for admin approval" in refused.get_data(as_text=True)
    assert "pybook_session" not in refused.headers.get("Set-Cookie", "")

    approve(app, "asha@example.com")
    allowed = login(visitor, email="asha@example.com")
    assert allowed.status_code == 302
    cookie = allowed.headers.get("Set-Cookie", "")
    assert "pybook_session" in cookie
    assert "HttpOnly" in cookie
    assert "Max-Age" in cookie, "the login must survive a browser restart"
    assert "Asha" in visitor.get("/learn").get_data(as_text=True)


def test_signup_refuses_a_duplicate_email(app):
    signup(app.test_client(), email="asha@example.com")
    second = signup(app.test_client(), name="Someone Else", email="asha@example.com")
    assert second.status_code == 200
    assert "already registered" in second.get_data(as_text=True)


def test_signup_refuses_a_weak_password_and_a_missing_consent(app):
    visitor = app.test_client()
    weak = signup(visitor, password="password")
    assert weak.status_code == 200
    assert "too common" in weak.get_data(as_text=True)
    assert app.config["STORE"].user_by_email("tester@example.com") is None

    page = visitor.get("/signup").get_data(as_text=True)
    no_consent = visitor.post(
        "/signup",
        data={
            "csrf": csrf(page),
            "name": "No Consent",
            "email": "nope@example.com",
            "password": "tester pass 123",
            "confirm": "tester pass 123",
            "course": "pybook",
        },
    )
    assert no_consent.status_code == 200
    assert "confirm that this device" in no_consent.get_data(as_text=True)


def test_a_form_post_without_a_csrf_token_is_refused(app):
    response = app.test_client().post(
        "/login", data={"email": "tester@example.com", "password": "tester pass 123"}
    )
    assert response.status_code == 400


def test_logout_ends_the_session_for_good(app):
    member = signed_in(app)
    assert member.get("/learn").status_code == 200
    token = csrf(member.get("/learn").get_data(as_text=True))
    response = member.post("/logout", data={"csrf": token})
    assert response.status_code == 302
    assert "pybook_session=;" in response.headers.get("Set-Cookie", "")
    assert member.get("/learn").status_code == 302


def test_learn_shows_the_first_lesson_open_and_the_rest_locked(client, catalog):
    page = client.get("/learn").get_data(as_text=True)
    first = catalog.lessons[0]
    last = catalog.lessons[-1]
    assert catalog.t(first["title"], "en") in page
    assert "Pass the previous module's exam" in page
    # the very last lesson's title is listed but its row is a lock, not a link
    assert "/lesson/%s" % last["id"] not in page


def test_locked_lesson_is_403_and_never_leaks_its_content(client, catalog):
    last = catalog.lessons[-1]
    response = client.get("/lesson/%s" % last["id"])
    assert response.status_code == 403
    body = response.get_data(as_text=True)
    assert "locked" in body.lower()
    intro = catalog.t(catalog.lesson(last["id"])["intro"], "en")
    assert intro[:60] not in body


def test_unknown_lesson_is_404(client):
    assert client.get("/lesson/m99c99l99").status_code == 404


def test_locked_module_exam_is_403(client):
    assert client.get("/exam/m02").status_code == 403
    assert client.get("/skip/m02").status_code == 403


def test_exam_page_explains_what_is_missing(client, catalog):
    """m01 is open but its lessons are not passed, so the exam lists them."""
    page = client.get("/exam/m01").get_data(as_text=True)
    assert "Not open yet" in page
    assert "skip exam" in page.lower()
    assert len(catalog.module_lessons("m01")) > 0


def test_lesson_page_has_the_five_steps(client, catalog):
    first = catalog.lessons[0]
    page = client.get("/lesson/%s" % first["id"]).get_data(as_text=True)
    for heading in ("The idea", "In real life", "Watch it run", "Required practice", "Check yourself"):
        assert heading in page
    assert "Step through" in page
    assert "<svg" in page, "the lesson visual is rendered"
    assert "Optional drills" in page
    assert "Quiz locked" in page, "the quiz must start locked"


def test_lesson_page_never_contains_answers(client, catalog):
    first = catalog.lessons[0]
    lesson = _lesson(catalog, first["id"])
    page = client.get("/lesson/%s" % first["id"]).get_data(as_text=True)
    for item in lesson["quiz"]:
        why = catalog.t(item["why"], "en")
        if why:
            assert why[:50] not in page, "the explanation must wait for an attempt"
    assert '"answer"' not in page


def test_playground_lists_the_allowed_modules(client):
    page = client.get("/playground").get_data(as_text=True)
    assert "Playground" in page
    for name in ("math", "json", "asyncio"):
        assert name in page


def test_progress_page_renders(client):
    page = client.get("/progress").get_data(as_text=True)
    assert "Questions to revisit" in page
    assert "Export JSON" in page


# --------------------------------------------------------------- quiz gating
def test_quiz_passes_and_unlocks_exactly_the_next_lesson(client, catalog):
    first, second, third = catalog.lessons[:3]
    _solve(client, catalog, first["id"])
    response = client.post(
        "/api/quiz/%s" % first["id"], json=_answers(_lesson(catalog, first["id"])["quiz"])
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["passed"] is True
    assert data["next"] == second["id"]

    assert client.get("/lesson/%s" % second["id"]).status_code == 200
    assert client.get("/lesson/%s" % third["id"]).status_code == 403


def test_wrong_quiz_answers_keep_the_next_lesson_locked(client, catalog):
    first, second = catalog.lessons[:2]
    _solve(client, catalog, first["id"])
    items = _lesson(catalog, first["id"])["quiz"]
    wrong = {"q%d" % (index + 1): "z" for index in range(len(items))}
    data = client.post("/api/quiz/%s" % first["id"], json=wrong).get_json()
    assert data["passed"] is False
    assert data["percent"] == 0
    assert client.get("/lesson/%s" % second["id"]).status_code == 403


def test_quiz_on_a_locked_lesson_is_refused(client, catalog):
    response = client.post("/api/quiz/%s" % catalog.lessons[-1]["id"], json={"q1": "a"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "locked"


# ----------------------------------------------------------- required practice
def test_quiz_is_refused_until_the_required_practice_passes(client, catalog):
    first = catalog.lessons[0]
    items = _lesson(catalog, first["id"])["quiz"]
    data = client.post("/api/quiz/%s" % first["id"], json=_answers(items)).get_json()
    assert data["ok"] is False
    assert data["error"] == "practice"
    assert data["remaining"] == len(_lesson(catalog, first["id"])["exercises"])

    _solve(client, catalog, first["id"])
    data = client.post("/api/quiz/%s" % first["id"], json=_answers(items)).get_json()
    assert data["passed"] is True


def test_exercise_check_reports_practice_progress(client, catalog):
    first = catalog.lessons[0]
    exercise = _lesson(catalog, first["id"])["exercises"][0]
    data = client.post(
        "/api/check/%s" % exercise["id"], json={"code": exercise["solution"]}
    ).get_json()
    assert data["passed"] is True
    assert data["practice"] == {"done": 1, "total": 1}
    assert data["ready"] is True


def test_optional_drills_are_offered_and_never_leak_the_answer(client, catalog):
    from web import drills

    first = catalog.lessons[0]
    body = _lesson(catalog, first["id"])
    built = drills.build(first["id"], body)
    assert built, "a lesson with an example must support at least one drill"
    for drill in built:
        shown = drills.public(drill)
        assert "answer" not in shown
        assert shown["id"] == drill["id"]
        assert shown["xp"] == drills.XP_DRILL

    page = client.get("/lesson/%s" % first["id"]).get_data(as_text=True)
    for drill in built:
        assert drill["id"] in page


def test_api_drill_grades_and_awards_xp_once(client, catalog):
    from web import drills

    first = catalog.lessons[0]
    body = _lesson(catalog, first["id"])
    predict = next(d for d in drills.build(first["id"], body) if d["kind"] == "predict")

    wrong = client.post(
        "/api/drill/%s" % first["id"],
        json={"drill_id": predict["id"], "answer": "definitely not the output"},
    ).get_json()
    assert wrong["ok"] is True
    assert wrong["passed"] is False
    assert wrong["xp"] == 0
    assert wrong["xp_total"] == 0

    right = client.post(
        "/api/drill/%s" % first["id"],
        json={"drill_id": predict["id"], "answer": predict["answer"]},
    ).get_json()
    assert right["passed"] is True
    assert right["xp"] == drills.XP_DRILL
    assert right["xp_total"] == drills.XP_DRILL

    again = client.post(
        "/api/drill/%s" % first["id"],
        json={"drill_id": predict["id"], "answer": predict["answer"]},
    ).get_json()
    assert again["passed"] is True
    assert again["xp_total"] == drills.XP_DRILL, "XP is not paid twice for one drill"


def test_api_drill_grades_line_order(client, catalog):
    from web import drills

    first = catalog.lessons[0]
    body = _lesson(catalog, first["id"])
    order = next((d for d in drills.build(first["id"], body) if d["kind"] == "order"), None)
    if order is None:
        pytest.skip("this lesson has no order drill")

    backwards = client.post(
        "/api/drill/%s" % first["id"],
        json={"drill_id": order["id"], "answer": list(reversed(order["answer"]))},
    ).get_json()
    assert backwards["passed"] is False
    assert "Line" in backwards["message"]

    data = client.post(
        "/api/drill/%s" % first["id"],
        json={"drill_id": order["id"], "answer": order["answer"]},
    ).get_json()
    assert data["passed"] is True


def test_api_drill_refuses_a_locked_lesson_or_unknown_drill(client, catalog):
    last = catalog.lessons[-1]
    assert (
        client.post(
            "/api/drill/%s" % last["id"], json={"drill_id": "x", "answer": ""}
        ).status_code
        == 403
    )
    first = catalog.lessons[0]
    response = client.post(
        "/api/drill/%s" % first["id"], json={"drill_id": "nope", "answer": ""}
    )
    assert response.status_code == 404


def test_xp_counts_lessons_exercises_and_drills(client, catalog):
    from web import drills

    first = catalog.lessons[0]
    _solve(client, catalog, first["id"])
    body = _lesson(catalog, first["id"])
    drill = drills.build(first["id"], body)[0]
    client.post(
        "/api/drill/%s" % first["id"],
        json={"drill_id": drill["id"], "answer": drill["answer"]},
    )
    client.post("/api/quiz/%s" % first["id"], json=_answers(body["quiz"]))

    exported = client.get("/api/export").get_json()
    assert exported["lessons"][first["id"]]["passed"] == 1
    assert len(exported["practice"]) == 1 + len(body["exercises"])

    page = client.get("/progress").get_data(as_text=True)
    assert "XP" in page


def test_quiz_accepts_item_ids_as_well_as_q_numbers(client, catalog):
    first = catalog.lessons[0]
    _solve(client, catalog, first["id"])
    items = _lesson(catalog, first["id"])["quiz"]
    data = client.post(
        "/api/quiz/%s" % first["id"], json={item["id"]: item["answer"] for item in items}
    ).get_json()
    assert data["passed"] is True


def test_api_requires_a_learner(app, catalog):
    anonymous = app.test_client()
    assert anonymous.post("/api/quiz/%s" % catalog.lessons[0]["id"], json={}).status_code == 401
    assert anonymous.post("/api/run", json={"code": "print(1)"}).status_code == 401
    assert anonymous.post("/api/reset", json={}).status_code == 401


# -------------------------------------------------------------- module exams
def _pass_module(client, catalog, module_id: str) -> None:
    for lesson in catalog.module_lessons(module_id):
        _solve(client, catalog, lesson["id"])
        response = client.post(
            "/api/quiz/%s" % lesson["id"], json=_answers(_lesson(catalog, lesson["id"])["quiz"])
        )
        assert response.get_json()["passed"], lesson["id"]


def test_exam_is_refused_until_every_lesson_is_passed(client, catalog):
    lessons = catalog.module_lessons("m01")
    for lesson in lessons[:-1]:
        _solve(client, catalog, lesson["id"])
        client.post(
            "/api/quiz/%s" % lesson["id"], json=_answers(_lesson(catalog, lesson["id"])["quiz"])
        )
    data = client.post("/api/exam/m01", json={"answers": _answers(catalog.full("m01")["exam"])}).get_json()
    assert data["ok"] is False
    assert data["error"] == "lessons"
    assert data["remaining"] == [lessons[-1]["id"]]


def test_exam_passes_after_all_lessons_and_opens_the_next_module(client, catalog):
    _pass_module(client, catalog, "m01")
    response = client.post(
        "/api/exam/m01", json={"answers": _answers(catalog.full("m01")["exam"])}
    )
    data = response.get_json()
    assert data["passed"] is True
    assert data["next_module"] == "m02"
    assert client.get("/exam/m02").status_code == 200
    assert client.get("/lesson/%s" % catalog.module_lessons("m02")[0]["id"]).status_code == 200


def test_skip_exam_needs_ninety_percent(client, catalog):
    items = catalog.full("m01")["skip_exam"]
    total = len(items)
    need = -(-total * 9 // 10)  # ceil(90%)

    short = _answers(items)
    for key in list(short)[need - 1:]:
        short[key] = "z"
    data = client.post("/api/exam/m01", json={"answers": short, "skip": True}).get_json()
    assert data["ok"] is True
    assert data["passed"] is False, "%d/%d must not skip a module" % (need - 1, total)

    data = client.post("/api/exam/m01", json={"answers": _answers(items), "skip": True}).get_json()
    assert data["passed"] is True
    # skipping marks the lessons passed, so the dashboard is honest
    page = client.get("/learn").get_data(as_text=True)
    assert "1 of" in page or "passed" in page
    assert client.get("/exam/m02").status_code == 200


# -------------------------------------------------------------------- sandbox
def test_run_code_prints_output():
    result = run_code("print(2 + 3)")
    assert result["ok"] is True
    assert result["stdout"].strip() == "5"


def test_run_code_reports_an_error_and_its_line():
    result = run_code("x = 1\ny = x + 'a'\n")
    assert result["ok"] is False
    assert "TypeError" in result["error"]
    assert result["error_line"] == 2


def test_run_code_blocks_open():
    result = run_code("open('secret.txt', 'w')")
    assert result["ok"] is False
    assert "open" in result["error"]


def test_pathlib_can_use_the_temp_folder():
    code = (
        "from pathlib import Path\n"
        "import tempfile\n"
        "with tempfile.TemporaryDirectory() as tmp:\n"
        "    note = Path(tmp) / 'note.txt'\n"
        "    note.write_text('PyBook', encoding='utf-8')\n"
        "    print(note.read_text(encoding='utf-8'))\n"
    )
    result = run_code(code)
    assert result["ok"] is True, result
    assert result["stdout"].strip() == "PyBook"


def test_pathlib_cannot_read_outside_the_run_folder():
    result = run_code(
        "from pathlib import Path\n"
        "print(Path.home().joinpath('definitely-secret.txt').read_text(encoding='utf-8'))\n"
    )
    assert result["ok"] is False
    assert "PermissionError" in result["error"]


def test_run_code_blocks_unlisted_imports():
    result = run_code("import os\nprint(os.getcwd())")
    assert result["ok"] is False
    assert "not available in the practice sandbox" in result["error"]


def test_run_code_allows_listed_imports():
    result = run_code("import math\nprint(round(math.sqrt(16)))")
    assert result["ok"] is True
    assert result["stdout"].strip() == "4"


def test_run_code_stops_an_infinite_loop():
    result = run_code("while True:\n    pass\n", timeout=0.8)
    assert result["ok"] is False
    assert result["timeout"] is True
    assert "seconds" in result["error"]


def test_run_code_reports_each_check():
    result = check_exercise("print('hi')", ["printed.strip() == 'hi'", "printed.strip() == 'bye'"])
    assert result["passed"] is False
    assert [entry["ok"] for entry in result["checks"]] == [True, False]


def test_check_exercise_accepts_the_reference_solution(catalog):
    lesson = _lesson(catalog, catalog.lessons[0]["id"])
    exercise = lesson["exercises"][0]
    result = check_exercise(exercise["solution"], exercise["checks"])
    assert result["passed"] is True, result


def test_trace_returns_line_steps_with_variables():
    result = run_code("x = 1\nx = x + 1\nprint(x)", trace=True)
    assert result["ok"] is True
    assert result["steps"], "the tracer produced no steps"
    assert all("line" in step and "vars" in step for step in result["steps"])
    assert result["steps"][-1]["vars"].get("x") == "2"
    assert result["stdout"].strip() == "2"


def test_worker_and_runner_agree_on_the_allow_list():
    from web import _worker

    assert set(ALLOWED_MODULES) == set(_worker.ALLOWED_MODULES)


def test_api_run_returns_output(client):
    data = client.post("/api/run", json={"code": "print('ok')"}).get_json()
    assert data["ok"] is True
    assert data["stdout"].strip() == "ok"


def test_api_check_runs_the_exercise(client, catalog):
    lesson = _lesson(catalog, catalog.lessons[0]["id"])
    exercise = lesson["exercises"][0]
    data = client.post(
        "/api/check/%s" % exercise["id"], json={"code": exercise["solution"]}
    ).get_json()
    assert data["passed"] is True
    assert data["hint"] is not None


def test_api_check_refuses_a_locked_lesson(client, catalog):
    last = catalog.lessons[-1]
    exercise = _lesson(catalog, last["id"])["exercises"][0]
    response = client.post("/api/check/%s" % exercise["id"], json={"code": "print(1)"})
    assert response.status_code == 403


def test_api_trace_runs_a_lesson_example(client, catalog):
    lesson = catalog.lessons[0]
    data = client.post("/api/trace/%s/1" % lesson["id"], json={}).get_json()
    assert data["ok"] is True
    assert data["steps"]
    assert data["code"], "the player needs the source lines"


def test_api_trace_refuses_an_unknown_example(client, catalog):
    lesson = catalog.lessons[0]
    assert client.post("/api/trace/%s/99" % lesson["id"], json={}).status_code == 404


# ------------------------------------------------------------------- settings
def test_language_switch_is_saved(client, catalog):
    data = client.post("/api/language", json={"language": "hi"}).get_json()
    assert data["ok"] is True
    page = client.get("/lesson/%s" % catalog.lessons[0]["id"]).get_data(as_text=True)
    hindi = catalog.t(_lesson(catalog, catalog.lessons[0]["id"])["intro"], "hi")
    assert hindi[:20] in page


def test_unknown_language_is_refused(client):
    assert client.post("/api/language", json={"language": "xx"}).status_code == 400


def test_export_and_reset(client, catalog):
    first = catalog.lessons[0]
    _solve(client, catalog, first["id"])
    client.post("/api/quiz/%s" % first["id"], json=_answers(_lesson(catalog, first["id"])["quiz"]))
    exported = client.get("/api/export").get_json()
    assert exported["lessons"][first["id"]]["passed"] == 1

    assert client.post("/api/reset", json={}).get_json()["ok"] is True
    after = client.get("/api/export").get_json()
    assert after["lessons"] == {}


def test_split_exercise_parses_ids():
    assert _split_exercise("m01c01l01e2") == ("m01c01l01", 1)
    assert _split_exercise("m01c01l01e1") == ("m01c01l01", 0)
    assert _split_exercise("nonsense") is None


def test_health_endpoint(app, catalog):
    data = app.test_client().get("/api/health").get_json()
    assert data["lessons"] == len(catalog.lessons)
    assert data["modules"] == len(catalog.modules)


# --------------------------------------------------------------- whole course
def test_whole_course_can_be_completed_through_the_api(client, catalog):
    for module in catalog.modules:
        for lesson in catalog.module_lessons(module["id"]):
            _solve(client, catalog, lesson["id"])
            data = client.post(
                "/api/quiz/%s" % lesson["id"],
                json=_answers(_lesson(catalog, lesson["id"])["quiz"]),
            ).get_json()
            assert data["passed"], "%s: %s" % (lesson["id"], data)
        exam = client.post(
            "/api/exam/%s" % module["id"],
            json={"answers": _answers(catalog.full(module["id"])["exam"])},
        ).get_json()
        assert exam["passed"], "%s exam: %s" % (module["id"], exam)

    state = client.get("/api/export").get_json()
    assert len(state["lessons"]) == len(catalog.lessons)
    page = client.get("/learn").get_data(as_text=True)
    assert "Course complete" in page


def test_progress_survives_a_second_request(client, catalog):
    first = catalog.lessons[0]
    _solve(client, catalog, first["id"])
    client.post("/api/quiz/%s" % first["id"], json=_answers(_lesson(catalog, first["id"])["quiz"]))
    page = client.get("/learn").get_data(as_text=True)
    assert "1 of %d lessons passed" % len(catalog.lessons) in page


# ----------------------------------------------------------------- code flow
def test_flow_diagram_is_generated_for_a_loop():
    from web.flow import flow_svg

    svg = flow_svg("total = 0\nfor n in [1, 2, 3]:\n    total = total + n\nprint(total)")
    assert svg.startswith("<svg")
    assert svg.rstrip().endswith("</svg>")
    assert "for n in [1, 2, 3]" in svg
    assert "repeat" in svg, "a loop must show its back edge"
    assert "total = 0" in svg


def test_flow_diagram_escapes_html():
    from web.flow import flow_svg

    svg = flow_svg("name = '<script>alert(1)</script>'")
    assert "<script>" not in svg
    assert "&lt;script&gt;" in svg


def test_flow_diagram_is_empty_for_broken_code():
    from web.flow import flow_svg

    assert flow_svg("def broken(:\n") == ""
    assert flow_svg("") == ""


def test_lesson_page_includes_a_code_flow_diagram(client, catalog):
    first = catalog.lessons[0]
    page = client.get("/lesson/%s" % first["id"]).get_data(as_text=True)
    assert "Code flow" in page
    assert "<svg" in page


def test_every_example_in_the_course_gets_a_diagram(catalog):
    """A lesson that silently loses its diagram is a bug, so check all of them."""
    from web.flow import flow_svg

    missing = []
    for lesson in catalog.lessons:
        for example in catalog.lesson(lesson["id"]).get("examples", []):
            if not flow_svg(example["code"]):
                missing.append((lesson["id"], example["code"][:40]))
    assert not missing, "no diagram for: %s" % missing[:5]
