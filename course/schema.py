"""Data model for the Python course.

Everything here is plain stdlib and JSON-serialisable, because the whole
curriculum is embedded into the notebook as one JSON blob.  The builder walks
these objects, the tests validate them, and the notebook runtime reads the
JSON.  One source of truth, three consumers.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

LANGUAGES = ("en", "hi", "hinglish")
LANGUAGE_NAMES = {"en": "English", "hi": "हिन्दी", "hinglish": "Hinglish"}
DEFAULT_LANGUAGE = "hinglish"

#: a learner must reach this share of correct answers to pass a lesson quiz
LESSON_PASS = 0.8
#: a module exam is cumulative, so the bar is the same but over more items
EXAM_PASS = 0.8
#: skipping a whole module is a privilege, so the bar is deliberately higher
SKIP_PASS = 0.9


def L(en: str, hi: str = "", hinglish: str = "") -> dict[str, str]:
    """Build a localised string. ``en`` is always required."""
    out = {"en": en}
    if hi:
        out["hi"] = hi
    if hinglish:
        out["hinglish"] = hinglish
    return out


class _Record:
    """Shared JSON export.  The notebook and the tests both consume dicts."""

    def to_dict(self) -> dict[str, Any]:
        from dataclasses import asdict

        return asdict(self)


@dataclass
class CodeExample(_Record):
    """One runnable snippet plus the output it is documented to produce."""

    title: dict[str, str]
    code: str
    output: str = ""
    note: dict[str, str] = field(default_factory=dict)


@dataclass
class Exercise(_Record):
    """A practice task.  ``checks`` are assert lines run against the learner's
    code namespace, so a hardcoded return value cannot pass by accident when
    the check also probes a second input."""

    id: str
    prompt: dict[str, str]
    starter: str
    solution: str
    checks: list[str]
    hint: dict[str, str] = field(default_factory=dict)


@dataclass
class QuizItem(_Record):
    """One multiple-choice question.  ``answer`` is a letter a/b/c/d."""

    id: str
    question: dict[str, str]
    options: list[str]
    answer: str
    why: dict[str, str]
    misconception: str = ""


@dataclass
class Lesson(_Record):
    id: str
    title: dict[str, str]
    keywords: list[str]
    intro: dict[str, str]
    real_life: dict[str, str]
    docs: str
    visual: str = ""
    examples: list[CodeExample] = field(default_factory=list)
    exercises: list[Exercise] = field(default_factory=list)
    quiz: list[QuizItem] = field(default_factory=list)
    takeaway: dict[str, str] = field(default_factory=dict)


@dataclass
class Chapter(_Record):
    id: str
    title: dict[str, str]
    lessons: list[Lesson] = field(default_factory=list)


@dataclass
class Module(_Record):
    id: str
    title: dict[str, str]
    goal: dict[str, str]
    chapters: list[Chapter] = field(default_factory=list)
    exam: list[QuizItem] = field(default_factory=list)
    skip_exam: list[QuizItem] = field(default_factory=list)
    icon: str = ""


@dataclass
class Course(_Record):
    id: str
    title: dict[str, str]
    subtitle: dict[str, str]
    modules: list[Module] = field(default_factory=list)

    # ---------------------------------------------------------------- helpers
    def lessons(self) -> list[Lesson]:
        return [ls for m in self.modules for c in m.chapters for ls in c.lessons]

    def lesson_ids(self) -> list[str]:
        return [ls.id for ls in self.lessons()]

    def find_lesson(self, lesson_id: str) -> Lesson | None:
        for lesson in self.lessons():
            if lesson.id == lesson_id:
                return lesson
        return None

    def find_module(self, module_id: str) -> Module | None:
        for module in self.modules:
            if module.id == module_id:
                return module
        return None

    def find_chapter(self, chapter_id: str) -> Chapter | None:
        for module in self.modules:
            for chapter in module.chapters:
                if chapter.id == chapter_id:
                    return chapter
        return None

    def module_of(self, lesson_id: str) -> Module | None:
        for module in self.modules:
            for chapter in module.chapters:
                if any(ls.id == lesson_id for ls in chapter.lessons):
                    return module
        return None

    def chapter_of(self, lesson_id: str) -> Chapter | None:
        for module in self.modules:
            for chapter in module.chapters:
                if any(ls.id == lesson_id for ls in chapter.lessons):
                    return chapter
        return None

    def keywords(self) -> set[str]:
        return {kw for ls in self.lessons() for kw in ls.keywords}

    def to_dict(self) -> dict[str, Any]:
        from dataclasses import asdict

        return asdict(self)
