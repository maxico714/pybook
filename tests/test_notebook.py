"""End-to-end tests for the shipped artefact, PyBook.ipynb.

The notebook is deliberately thin: every cell is one short call, and the
curriculum plus the runtime live in files next to it.  These tests prove three
things:

1. the notebook stays small (no giant text cell, no embedded curriculum);
2. its setup cell really boots the course from the shipped files;
3. a learner can finish the whole course through the notebook API, and cannot
   open a lesson, chapter or module that is still locked.
"""
from __future__ import annotations

import json
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "PyBook.ipynb"

MAX_CELL_CHARS = 3000
MAX_CELLS = 20


def _read() -> dict:
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))


def _source(cell: dict) -> str:
    src = cell.get("source", "")
    return "".join(src) if isinstance(src, list) else src


@pytest.fixture(scope="module")
def notebook() -> dict:
    assert NOTEBOOK.exists(), "PyBook.ipynb has not been built"
    return _read()


@pytest.fixture()
def setup(notebook, tmp_path, monkeypatch):
    """Run the notebook's setup cell the way a kernel does, with a temp progress file."""
    monkeypatch.chdir(ROOT)
    monkeypatch.setenv("PYBOOK_PROGRESS", str(tmp_path / "progress.json"))
    namespace: dict = {"__name__": "__main__"}
    code_cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    exec(compile(_source(code_cells[0]), "<setup>", "exec"), namespace)  # noqa: S102
    return namespace


def _answers(items: list[dict]) -> dict:
    return {"q%d" % (i + 1): item["answer"] for i, item in enumerate(items)}


# ------------------------------------------------------------------ structure


def test_notebook_is_small(notebook):
    assert len(notebook["cells"]) <= MAX_CELLS, "too many cells for Colab to stay responsive"
    sizes = [len(_source(c)) for c in notebook["cells"]]
    assert max(sizes) <= MAX_CELL_CHARS, "a cell is too big: %d characters" % max(sizes)
    assert sum(sizes) < 12000, "the whole notebook should stay a few KB"


def test_notebook_has_unique_cell_ids(notebook):
    ids = [cell["id"] for cell in notebook["cells"]]
    assert len(ids) == len(set(ids))


def test_notebook_is_valid_nbformat(notebook):
    nbformat = pytest.importorskip("nbformat")
    nbformat.validate(nbformat.from_dict(notebook))


def test_curriculum_is_not_embedded(notebook):
    joined = "\n".join(_source(c) for c in notebook["cells"])
    assert "CURRICULUM" not in joined
    assert "pc-wrap" not in joined, "runtime source must live in pybook/core.py"
    assert "m01c01l01" not in joined, "lesson ids belong in the data files"


def test_setup_cell_starts_the_course(setup):
    course = setup["course"]
    assert len(course.modules) == 12
    assert len(course.lessons) == 53
    assert course.language() == "hinglish"


def test_every_code_cell_runs_top_to_bottom(notebook, tmp_path, monkeypatch):
    """Run the notebook like a learner: every code cell, in order, once."""
    monkeypatch.chdir(ROOT)
    monkeypatch.setenv("PYBOOK_PROGRESS", str(tmp_path / "progress.json"))
    namespace: dict = {"__name__": "__main__"}
    for number, cell in enumerate(
        [c for c in notebook["cells"] if c["cell_type"] == "code"], 1
    ):
        try:
            exec(compile(_source(cell), "<cell %d>" % number, "exec"), namespace)  # noqa: S102
        except Exception as exc:  # pragma: no cover - the message is the point
            raise AssertionError(
                "cell %d (%s) failed: %s: %s" % (number, cell["id"], type(exc).__name__, exc)
            ) from exc
    assert len(namespace["course"].lessons) == 53


# ------------------------------------------------------------------- the locks


def test_locked_lesson_never_shows_its_content(setup):
    course = setup["course"]
    last = course.lessons[-1]
    html = course.lesson(last["id"])
    assert "locked" in html.lower()
    body = course._lesson(last["id"])
    assert body["intro"]["en"][:40] not in html


def test_exam_waits_for_every_lesson_in_the_module(setup):
    course = setup["course"]
    html = course.exam_current(q1="a", q2="b")
    assert "opens after every lesson" in html


def test_quiz_gate_unlocks_exactly_one_lesson(setup):
    course = setup["course"]
    first, second, third = (course.lessons[i] for i in range(3))
    assert course.lesson_unlocked(first["id"])
    assert not course.lesson_unlocked(second["id"])

    wrong = {"q%d" % (i + 1): "z" for i in range(len(course._lesson(first["id"])["quiz"]))}
    course.quiz(first["id"], wrong)
    assert not course.lesson_unlocked(second["id"])

    course.quiz(first["id"], _answers(course._lesson(first["id"])["quiz"]))
    assert course.lesson_unlocked(second["id"])
    assert not course.lesson_unlocked(third["id"])


def test_module_is_locked_until_the_previous_exam_passes(setup):
    course = setup["course"]
    assert course.module_unlocked("m01")
    assert not course.module_unlocked("m02")
    assert "locked" in course.module("m02").lower()


# --------------------------------------------------------------- the journey


def test_full_course_can_be_completed_and_saved(setup, tmp_path):
    course = setup["course"]
    for module in course.modules:
        full = course._full(module["id"])
        for chapter in full["chapters"]:
            for lesson in chapter["lessons"]:
                feedback = course.quiz(lesson["id"], _answers(lesson["quiz"]))
                assert course.lesson_passed(lesson["id"]), feedback
        feedback = course.exam(module["id"], _answers(full["exam"]))
        assert course.module_passed(module["id"]), feedback

    assert course.next_lesson_id() is None
    path = pathlib.Path(course.path)
    assert path.exists()
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert len(saved["lessons"]) == 53

    reloaded = type(course)(progress_path=path)
    assert all(reloaded.lesson_passed(ls["id"]) for ls in reloaded.lessons)


def test_skip_exam_needs_ninety_percent(setup):
    course = setup["course"]
    full = course._full("m01")
    answers = _answers(full["skip_exam"])
    total = len(answers)
    need = -(-total * 9 // 10)  # ceil(90%)
    short = {"q%d" % (i + 1): item["answer"] for i, item in enumerate(full["skip_exam"])}
    for key in list(short)[need - 1:]:
        short[key] = "z"
    course.skip_exam("m01", short)
    assert not course.module_passed("m01"), "%d/%d must not be enough" % (need - 1, total)
    course.skip_exam("m01", answers)
    assert course.module_passed("m01")
    assert course.module_unlocked("m02")


def test_language_switch_changes_rendered_text(setup):
    course = setup["course"]
    lesson_id = course.lessons[0]["id"]
    course.set_language("en")
    english = course.lesson(lesson_id)
    course.set_language("hi")
    hindi = course.lesson(lesson_id)
    assert english != hindi
    assert course._lesson(lesson_id)["intro"]["hi"][:12] in hindi
    course.set_language("hinglish")


def test_exercise_checker_accepts_the_reference_solution(setup):
    course = setup["course"]
    lesson = course._lesson(course.lessons[0]["id"])
    exercise = lesson["exercises"][0]
    assert "all checks passed" in course.check(exercise["id"], exercise["solution"]).lower()
    assert "not correct" in course.check(exercise["id"], "x = 1").lower()


def test_export_and_import_progress_round_trip(setup, tmp_path):
    course = setup["course"]
    first = course.lessons[0]["id"]
    course.quiz(first, _answers(course._lesson(first)["quiz"]))
    blob = course.export_progress()

    other = type(course)(progress_path=tmp_path / "other.json")
    other.import_progress(blob)
    assert other.lesson_passed(first)
