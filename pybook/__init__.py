"""PyBook - the notebook-side API.

Every cell in ``PyBook.ipynb`` calls one of these short functions.  The content
and the logic live in files next to the notebook (``pybook/core.py`` and
``pybook/data/*.json``), so the notebook itself stays small enough for Colab.

    from pybook import start
    course = start()

    show()                  # the lesson you have reached
    answer(q1="b", q2="a")  # answer its quiz
    check("your code")      # test exercise 1
    exam(q1="b", q2="a")    # module exam
    skip(q1="b", q2="a")    # skip exam (90%)
    dashboard() / progress() / review() / language("hi") / guide()

Lessons unlock strictly in order.  A locked lesson, chapter or module renders a
lock card instead of its content, and the module exam opens only after every
lesson in that module is passed - the skip exam is the only shortcut, and it
needs 90%.
"""
from __future__ import annotations

from .core import (  # noqa: F401
    EXAM_PASS,
    LANGUAGES,
    LANGUAGE_NAMES,
    LESSON_PASS,
    SKIP_PASS,
    Course,
)

__all__ = [
    "Course",
    "LANGUAGES",
    "LANGUAGE_NAMES",
    "LESSON_PASS",
    "EXAM_PASS",
    "SKIP_PASS",
    "course",
    "start",
    "show",
    "lesson",
    "answer",
    "quiz",
    "check",
    "exam",
    "skip",
    "dashboard",
    "progress",
    "review",
    "language",
    "guide",
    "export",
    "restore",
    "reset",
]

course: Course | None = None


def start(root=None, progress_path=None, language: str = "hinglish") -> Course:
    """Load PyBook and return the course object (also bound to ``course``)."""
    global course
    course = Course(root, progress_path=progress_path, language=language)
    print(
        "PyBook ready · %d modules · %d lessons · language %s"
        % (len(course.modules), len(course.lessons), course.state["language"])
    )
    print("Next: show()")
    return course


def _c() -> Course:
    if course is None:
        raise RuntimeError("Run the setup cell first: course = start()")
    return course


def show() -> str:
    """Render the next lesson you are allowed to read."""
    return _c().next()


def lesson(lesson_id: str | None = None) -> str:
    """Render one lesson. A locked lesson shows a lock card, never its content."""
    return _c().lesson(lesson_id)


def answer(**answers) -> str:
    """Answer the quiz of the current lesson: ``answer(q1="b", q2="a")``."""
    return _c().answer(**answers)


def quiz(**answers) -> str:
    """Alias of :func:`answer`."""
    return _c().answer(**answers)


def check(code: str, n: int = 1) -> str:
    """Run ``code`` against exercise ``n`` of the current lesson."""
    return _c().check_current(code, n)


def exam(**answers) -> str:
    """Take the module exam of the module you are in."""
    return _c().exam_current(**answers)


def skip(**answers) -> str:
    """Take the skip exam (90%) for the module you are in."""
    return _c().skip_current(**answers)


def dashboard() -> str:
    return _c().dashboard()


def progress() -> dict:
    return _c().progress()


def review() -> str:
    return _c().review()


def language(code: str) -> str:
    """Switch explanation language: ``en``, ``hi`` or ``hinglish``."""
    return _c().set_language(code)


def guide() -> str:
    return _c().help()


def export() -> str:
    """Return the whole progress state as JSON text."""
    return _c().export_progress()


def restore(text: str) -> None:
    return _c().import_progress(text)


def reset(confirm: bool = False) -> None:
    return _c().reset(confirm)
