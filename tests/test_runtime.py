"""Tests for the notebook runtime: gating, scoring, storage, language.

These use a small synthetic curriculum so they stay fast and independent of the
real content.  The real content has its own completeness tests.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pybook.core import Course, LANGUAGE_NAMES  # noqa: E402
from course.schema import L  # noqa: E402


def _item(qid, answer="a"):
    return {
        "id": qid,
        "question": L("Question " + qid, "à¤ªà¥à¤°à¤¶à¥à¤¨ " + qid, "Sawaal " + qid),
        "options": ["right", "wrong one", "wrong two", "wrong three"],
        "answer": answer,
        "why": L("Because it is.", "à¤•à¥à¤¯à¥‹à¤‚à¤•à¤¿ à¤à¤¸à¤¾ à¤¹à¥ˆà¥¤", "Kyunki aisa hai."),
        "misconception": "",
    }


def _lesson(lid, n_quiz=3):
    return {
        "id": lid,
        "title": L("Lesson " + lid, "à¤²à¥‡à¤¸à¤¨ " + lid, "Lesson " + lid),
        "keywords": [],
        "intro": L("Intro text", "à¤ªà¤°à¤¿à¤šà¤¯", "Intro text"),
        "real_life": L("Real life", "à¤…à¤¸à¤² à¤œà¤¼à¤¿à¤‚à¤¦à¤—à¥€", "Real life"),
        "docs": "https://docs.python.org/3/tutorial/",
        "visual": "variables",
        "examples": [
            {"title": L("Example"), "code": "print(1)", "output": "1", "note": {}},
            {"title": L("Example"), "code": "print(2)", "output": "2", "note": {}},
        ],
        "exercises": [
            {
                "id": lid + "e1",
                "prompt": L("Print 1", "1 à¤ªà¥à¤°à¤¿à¤‚à¤Ÿ à¤•à¤°à¥‡à¤‚", "1 print karo"),
                "starter": "",
                "solution": "print(1)",
                "checks": ['printed.strip() == "1"'],
                "hint": L("Use print", "print à¤‡à¤¸à¥à¤¤à¥‡à¤®à¤¾à¤² à¤•à¤°à¥‡à¤‚", "print use karo"),
            }
        ],
        "quiz": [_item(f"{lid}q{i}") for i in range(1, n_quiz + 1)],
        "takeaway": L("Remember this", "à¤¯à¤¹ à¤¯à¤¾à¤¦ à¤°à¤–à¥‡à¤‚", "Ye yaad rakho"),
    }


def _curriculum():
    return {
        "id": "test",
        "title": L("Test course", "à¤Ÿà¥‡à¤¸à¥à¤Ÿ à¤•à¥‹à¤°à¥à¤¸", "Test course"),
        "subtitle": L("Sub", "à¤‰à¤ª", "Sub"),
        "modules": [
            {
                "id": "m01",
                "title": L("One", "à¤à¤•", "One"),
                "goal": L("Goal one", "à¤²à¤•à¥à¤·à¥à¤¯", "Goal one"),
                "icon": "1",
                "chapters": [
                    {
                        "id": "m01c01",
                        "title": L("Chapter one", "à¤…à¤§à¥à¤¯à¤¾à¤¯ à¤à¤•", "Chapter one"),
                        "lessons": [_lesson("m01c01l01"), _lesson("m01c01l02")],
                    }
                ],
                "exam": [_item("m01x%02d" % i) for i in range(1, 6)],
                "skip_exam": [_item("m01s%02d" % i) for i in range(1, 9)],
            },
            {
                "id": "m02",
                "title": L("Two", "à¤¦à¥‹", "Two"),
                "goal": L("Goal two", "à¤²à¤•à¥à¤·à¥à¤¯ à¤¦à¥‹", "Goal two"),
                "icon": "2",
                "chapters": [
                    {
                        "id": "m02c01",
                        "title": L("Chapter two", "à¤…à¤§à¥à¤¯à¤¾à¤¯ à¤¦à¥‹", "Chapter two"),
                        "lessons": [_lesson("m02c01l01")],
                    }
                ],
                "exam": [_item("m02x%02d" % i) for i in range(1, 6)],
                "skip_exam": [_item("m02s%02d" % i) for i in range(1, 9)],
            },
        ],
    }


@pytest.fixture()
def course(tmp_path):
    return Course(_curriculum(), progress_path=tmp_path / "progress.json")


def _pass_all(rt, lesson_id):
    n = len(rt.by_lesson[lesson_id]["quiz"])
    answers = {f"{lesson_id}q{i}": "a" for i in range(1, n + 1)}
    return rt.quiz(lesson_id, answers)


# ------------------------------------------------------------------- gating

def test_only_the_first_lesson_starts_unlocked(course):
    assert course.lesson_unlocked("m01c01l01")
    assert not course.lesson_unlocked("m01c01l02")
    assert not course.module_unlocked("m02")


def test_locked_lesson_renders_a_lock_and_hides_content(course):
    html = course.render_lesson("m01c01l02")
    assert "locked" in html
    assert "Intro text" not in html


def test_passing_a_lesson_unlocks_the_next_one(course):
    _pass_all(course, "m01c01l01")
    assert course.lesson_passed("m01c01l01")
    assert course.lesson_unlocked("m01c01l02")


def test_failing_a_lesson_keeps_it_locked_for_the_next(course):
    course.quiz("m01c01l01", {"m01c01l01q1": "a", "m01c01l01q2": "b", "m01c01l01q3": "b"})
    assert not course.lesson_passed("m01c01l01")
    assert not course.lesson_unlocked("m01c01l02")


def test_two_of_three_is_not_enough(course):
    course.quiz("m01c01l01", {"m01c01l01q1": "a", "m01c01l01q2": "a", "m01c01l01q3": "b"})
    rec = course.state["lessons"]["m01c01l01"]
    assert rec["last_score"] == pytest.approx(2 / 3, abs=1e-3)
    assert not rec["passed"]


def test_a_later_attempt_can_pass_and_keeps_the_best_score(course):
    course.quiz("m01c01l01", {"m01c01l01q1": "a", "m01c01l01q2": "a", "m01c01l01q3": "b"})
    _pass_all(course, "m01c01l01")
    rec = course.state["lessons"]["m01c01l01"]
    assert rec["passed"]
    assert rec["attempts"] == 2
    assert rec["best_score"] == 1.0


def test_module_two_is_locked_until_the_module_one_exam_passes(course):
    _pass_all(course, "m01c01l01")
    _pass_all(course, "m01c01l02")
    assert not course.module_unlocked("m02")
    course.exam("m01", {"m01x%02d" % i: "a" for i in range(1, 6)})
    assert course.module_unlocked("m02")


def test_exam_needs_eighty_percent(course):
    _pass_all(course, "m01c01l01")
    _pass_all(course, "m01c01l02")
    course.exam("m01", {"m01x01": "a", "m01x02": "a", "m01x03": "a", "m01x04": "b", "m01x05": "b"})
    assert course.state["modules"]["m01"]["exam_best"] == pytest.approx(0.6)
    assert not course.module_unlocked("m02")


def test_locked_module_exam_is_refused(course):
    html = course.exam("m02", {"m02x01": "a"})
    assert "locked" in html
    assert "m02" not in course.state["modules"] or not course.state["modules"]["m02"].get("exam_passed")


def test_skip_exam_needs_ninety_percent_and_marks_the_module_done(course):
    eight = {"m01s%02d" % i: "a" for i in range(1, 9)}
    seven = dict(eight)
    seven["m01s08"] = "b"
    course.skip_exam("m01", seven)
    assert not course.module_passed("m01")
    course.skip_exam("m01", eight)
    assert course.module_passed("m01")
    assert course.state["modules"]["m01"]["skipped"] is True
    assert all(course.lesson_passed(ls["id"]) for ls in course.lessons if ls["id"].startswith("m01"))
    assert course.module_unlocked("m02")


# ------------------------------------------------------------------ storage

def test_progress_survives_a_new_course_object(tmp_path):
    path = tmp_path / "p.json"
    first = Course(_curriculum(), progress_path=path)
    _pass_all(first, "m01c01l01")
    first.set_language("hi")

    second = Course(_curriculum(), progress_path=path)
    assert second.lesson_passed("m01c01l01")
    assert second.state["language"] == "hi"
    assert second.lesson_unlocked("m01c01l02")


def test_progress_file_is_valid_json_with_a_version(tmp_path):
    path = tmp_path / "p.json"
    rt = Course(_curriculum(), progress_path=path)
    _pass_all(rt, "m01c01l01")
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["version"] == 1
    assert data["lessons"]["m01c01l01"]["passed"] is True


def test_a_corrupt_progress_file_is_kept_and_replaced(tmp_path, capsys):
    path = tmp_path / "p.json"
    path.write_text("{not json", encoding="utf-8")
    rt = Course(_curriculum(), progress_path=path)
    assert rt.state["lessons"] == {}
    backups = list(tmp_path.glob("p.json.corrupt-*"))
    assert backups, "the corrupt file must be preserved, not deleted"
    assert "could not be read" in capsys.readouterr().out


def test_export_and_import_round_trip(tmp_path):
    a = Course(_curriculum(), progress_path=tmp_path / "a.json")
    _pass_all(a, "m01c01l01")
    blob = a.export_progress()

    b = Course(_curriculum(), progress_path=tmp_path / "b.json")
    b.import_progress(blob)
    assert b.lesson_passed("m01c01l01")


def test_reset_needs_confirmation(tmp_path, capsys):
    rt = Course(_curriculum(), progress_path=tmp_path / "p.json")
    _pass_all(rt, "m01c01l01")
    rt.reset()
    assert rt.lesson_passed("m01c01l01")
    assert "confirm=True" in capsys.readouterr().out
    rt.reset(confirm=True)
    assert not rt.lesson_passed("m01c01l01")


# ----------------------------------------------------------------- language

def test_default_language_is_hinglish(course):
    assert course.state["language"] == "hinglish"


def test_set_language_accepts_names_and_codes(course):
    assert course.set_language("English") == "en"
    assert course.set_language("hindi") == "hi"
    assert course.set_language("hinglish") == "hinglish"
    with pytest.raises(ValueError):
        course.set_language("klingon")


def test_language_changes_rendered_text(course):
    course.set_language("en")
    assert "Intro text" in course.render_lesson("m01c01l01")
    course.set_language("hi")
    assert "à¤ªà¤°à¤¿à¤šà¤¯" in course.render_lesson("m01c01l01")


def test_missing_translation_falls_back_to_hinglish_then_english(course):
    course.set_language("hi")
    partial = {"en": "English only", "hinglish": "Hinglish version"}
    assert course.t(partial) == "Hinglish version"
    assert course.t({"en": "English only"}) == "English only"
    assert course.t({}) == ""


def test_all_three_languages_are_named(course):
    assert set(LANGUAGE_NAMES) == {"en", "hi", "hinglish"}


# ---------------------------------------------------------------- rendering

def test_a_lesson_renders_all_five_parts(course):
    html = course.render_lesson("m01c01l01")
    for marker in ("Introduction", "Real life example", "Code examples", "Exercises", "Quiz"):
        assert marker in html, marker


def test_a_lesson_shows_its_code_and_expected_output(course):
    html = course.render_lesson("m01c01l01")
    assert "print(1)" in html
    assert ">1<" in html or "1</div>" in html


def test_lesson_text_is_html_escaped(tmp_path):
    data = _curriculum()
    lesson = data["modules"][0]["chapters"][0]["lessons"][0]
    for lang in ("en", "hi", "hinglish"):
        lesson["intro"][lang] = "<script>alert(1)</script>"
    rt = Course(data, progress_path=tmp_path / "p.json")
    html = rt.render_lesson("m01c01l01")
    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_dashboard_lists_every_module_and_the_next_lesson(course):
    html = course.render_dashboard()
    assert "One" in html and "Two" in html
    assert "m01c01l01" in html


def test_module_view_marks_progress(course):
    _pass_all(course, "m01c01l01")
    html = course.render_module("m01")
    assert "✅" in html
    assert "m01c01l02" in html


def test_next_returns_the_first_unpassed_unlocked_lesson(course):
    assert course.next_lesson_id() == "m01c01l01"
    _pass_all(course, "m01c01l01")
    assert course.next_lesson_id() == "m01c01l02"


def test_review_lists_imperfect_passes(course):
    course.quiz("m01c01l01", {"m01c01l01q1": "a", "m01c01l01q2": "a", "m01c01l01q3": "a"})
    course.quiz("m01c01l01", {"m01c01l01q1": "a", "m01c01l01q2": "a", "m01c01l01q3": "b"})
    html = course.review()
    assert "Review queue" in html
    assert "Question m01c01l01q3" in html


# ---------------------------------------------------------------- exercises

def test_check_passes_correct_code(course):
    html = course.check("m01c01l01e1", "print(1)")
    assert "All checks passed" in html


def test_check_rejects_wrong_output(course):
    html = course.check("m01c01l01e1", "print(2)")
    assert "Not correct yet" in html


def test_check_reports_a_crash_without_raising(course):
    html = course.check("m01c01l01e1", "1 / 0")
    assert "raised an error" in html
    assert "ZeroDivisionError" in html


def test_check_rejects_an_unknown_exercise(course):
    assert "Unknown exercise" in course.check("nope", "print(1)")


# -------------------------------------------------------------------- misc

def test_unknown_ids_do_not_crash(course):
    assert "Unknown lesson" in course.render_lesson("m99c99l99")
    assert "Unknown module" in course.render_module("m99")


def test_answers_can_be_a_list_in_question_order(course):
    course.quiz("m01c01l01", ["a", "a", "a"])
    assert course.lesson_passed("m01c01l01")


def test_help_lists_the_commands(course):
    text = course.help()
    assert "show()" in text
    assert "answer(" in text
    assert "skip(" in text
    assert "dashboard()" in text
