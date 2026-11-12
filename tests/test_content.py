"""Content tests: completeness, truthfulness of every example, and artefact sync.

Three promises are checked here:

1. Completeness - all 35 Python keywords are taught, every lesson has the four
   required parts, and the course is big enough to be a real reference.
2. Truthfulness - every code example is executed and its printed output must
   match the output shown in the notebook byte for byte.
3. Sync - PyBook.ipynb on disk is exactly what ``build_notebook.py`` produces
   from ``course/``, so the shipped file cannot drift from the source.
"""
from __future__ import annotations

import json
import pathlib

import pytest

from course import selfcheck
from course.curriculum import COURSE, curriculum_dict
from course.validate import PYTHON_KEYWORDS, SOFT_KEYWORDS, validate
from course.visuals import VISUALS

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "PyBook.ipynb"


def _modules() -> list:
    return [source.MODULE for source in __import__("course.curriculum", fromlist=["MODULE_SOURCES"]).MODULE_SOURCES]


# ------------------------------------------------------------------ structure


def test_curriculum_is_valid():
    assert validate(COURSE) == []


def test_course_size():
    assert len(COURSE.modules) == 12
    assert len(COURSE.lessons()) >= 45
    assert sum(len(ls.exercises) for ls in COURSE.lessons()) >= len(COURSE.lessons())
    assert sum(len(ls.quiz) for ls in COURSE.lessons()) >= 3 * len(COURSE.lessons())


def test_every_keyword_is_taught():
    covered = COURSE.keywords()
    missing = [kw for kw in PYTHON_KEYWORDS if kw not in covered]
    assert not missing, "keywords never taught: %s" % ", ".join(missing)


def test_only_real_keywords_are_claimed():
    unknown = sorted(kw for kw in COURSE.keywords() if kw not in PYTHON_KEYWORDS + SOFT_KEYWORDS)
    assert not unknown, "not Python keywords: %s" % ", ".join(unknown)


def test_every_lesson_has_the_four_parts():
    for lesson in COURSE.lessons():
        where = lesson.id
        for lang in ("en", "hi", "hinglish"):
            assert lesson.intro.get(lang), f"{where}: intro missing {lang}"
            assert lesson.real_life.get(lang), f"{where}: real_life missing {lang}"
        assert len(lesson.examples) >= 2, f"{where}: needs 2+ examples"
        assert len(lesson.exercises) >= 1, f"{where}: needs an exercise"
        assert len(lesson.quiz) >= 3, f"{where}: needs 3+ quiz items"
        assert lesson.docs.startswith("https://docs.python.org/3/"), where
        if lesson.visual:
            assert lesson.visual in VISUALS, f"{where}: unknown visual {lesson.visual}"


def test_every_example_has_a_title_and_exercises_have_checks():
    for lesson in COURSE.lessons():
        for example in lesson.examples:
            assert example.title.get("en"), lesson.id
            assert example.code.strip(), lesson.id
        for exercise in lesson.exercises:
            assert exercise.checks, f"{exercise.id}: no checks"
            assert exercise.solution.strip(), f"{exercise.id}: no solution"
            assert exercise.prompt.get("en") and exercise.prompt.get("hinglish"), exercise.id


# --------------------------------------------------------------- truthfulness


@pytest.mark.parametrize("source", _modules(), ids=lambda m: m.id)
def test_module_examples_are_real(source):
    problems = selfcheck.check_module(source.to_dict())
    assert problems == [], "\n".join(problems)


# --------------------------------------------------------------------- sync


def test_notebook_matches_the_generator():
    import build_notebook

    built = build_notebook.build()
    on_disk = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert on_disk["cells"] == built["cells"], "PyBook.ipynb is stale - run build_notebook.py"
    assert on_disk["metadata"] == built["metadata"]


def test_data_files_match_the_generator():
    """pybook/data is generated: it must equal what the builder writes today."""
    import build_notebook

    expected_index = build_notebook._index(curriculum_dict())
    on_disk = json.loads((ROOT / "pybook" / "data" / "index.json").read_text(encoding="utf-8"))
    assert on_disk == expected_index, "pybook/data/index.json is stale - run build_notebook.py"

    for module in curriculum_dict()["modules"]:
        path = ROOT / "pybook" / "data" / ("%s.json" % module["id"])
        assert json.loads(path.read_text(encoding="utf-8")) == module, path.name


def test_data_files_cover_every_lesson():
    index = json.loads((ROOT / "pybook" / "data" / "index.json").read_text(encoding="utf-8"))
    ids = [
        lesson["id"]
        for module in index["modules"]
        for chapter in module["chapters"]
        for lesson in chapter["lessons"]
    ]
    assert len(ids) == len(set(ids)) == 53
    for module in index["modules"]:
        assert (ROOT / "pybook" / "data" / ("%s.json" % module["id"])).is_file()


def test_colab_bundle_contains_the_package():
    import zipfile

    bundle = ROOT / "pybook_bundle.zip"
    assert bundle.is_file(), "run build_notebook.py to create the Colab bundle"
    with zipfile.ZipFile(bundle) as archive:
        names = set(archive.namelist())
    assert "pybook/__init__.py" in names
    assert "pybook/core.py" in names
    assert "pybook/data/index.json" in names
    assert all("__pycache__" not in name for name in names)


def test_no_stale_python_course_names():
    """The project was renamed to PyBook; no artefact may still use the old name."""
    stale = ["Python_Course.ipynb", "python_course_progress", "PythonCourse/", 'id="python-core"']
    for path in [
        ROOT / "build_notebook.py",
        ROOT / "pybook" / "core.py",
        ROOT / "pybook" / "__init__.py",
        ROOT / "course" / "curriculum.py",
    ]:
        text = path.read_text(encoding="utf-8")
        for needle in stale:
            assert needle not in text, f"{path.name} still mentions {needle!r}"
