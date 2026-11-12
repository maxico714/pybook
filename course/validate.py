"""Curriculum validation shared by the builder, the tests and CI.

Every rule here exists because breaking it would let a lesson slip through
without the four required parts, or let a lock open too early.  Failures are
returned as a list of readable strings so the builder can print them all at
once instead of dying on the first one.
"""
from __future__ import annotations

import re

LANGUAGES = ("en", "hi", "hinglish")
#: Python 3.12 keywords (keyword.kwlist)
PYTHON_KEYWORDS = [
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield",
]
SOFT_KEYWORDS = ["match", "case", "type", "_"]

LESSON_ID = re.compile(r"^m\d{2}c\d{2}l\d{2}$")
CHAPTER_ID = re.compile(r"^m\d{2}c\d{2}$")
MODULE_ID = re.compile(r"^m\d{2}$")

#: prose fields that must exist in all three languages
TRILINGUAL = ("intro", "real_life")


def _check_localised(where: str, field: dict, required: tuple[str, ...], errors: list[str]) -> None:
    if not isinstance(field, dict) or not field.get("en"):
        errors.append(f"{where}: missing English text")
        return
    for lang in required:
        if not field.get(lang):
            errors.append(f"{where}: missing '{lang}' translation")
    for key, value in field.items():
        if key not in LANGUAGES:
            errors.append(f"{where}: unknown language key {key!r}")
        elif not str(value).strip():
            errors.append(f"{where}: empty '{key}' translation")


def validate(course) -> list[str]:
    """Return a list of problems; an empty list means the course is valid."""
    errors: list[str] = []
    data = course.to_dict() if hasattr(course, "to_dict") else course
    modules = data["modules"]

    _check_localised("course.title", data["title"], LANGUAGES, errors)
    _check_localised("course.subtitle", data["subtitle"], LANGUAGES, errors)

    if not modules:
        errors.append("course has no modules")
        return errors

    seen: dict[str, str] = {}

    def claim(identifier: str, kind: str) -> None:
        if identifier in seen:
            errors.append(f"duplicate id {identifier!r} ({kind} and {seen[identifier]})")
        seen[identifier] = kind

    for m_index, module in enumerate(modules):
        mid = module["id"]
        claim(mid, "module")
        if not MODULE_ID.match(mid):
            errors.append(f"module id {mid!r} must look like mNN")
        if mid != "m%02d" % (m_index + 1):
            errors.append(f"module {mid} is out of order (expected m{m_index + 1:02d})")
        _check_localised(f"{mid}.title", module["title"], LANGUAGES, errors)
        _check_localised(f"{mid}.goal", module["goal"], LANGUAGES, errors)

        chapters = module["chapters"]
        if len(chapters) < 1:
            errors.append(f"{mid}: needs at least one chapter")

        module_lessons = 0
        for c_index, chapter in enumerate(chapters):
            cid = chapter["id"]
            claim(cid, "chapter")
            if not CHAPTER_ID.match(cid):
                errors.append(f"chapter id {cid!r} must look like mNNcNN")
            if not cid.startswith(mid):
                errors.append(f"chapter {cid} does not belong to module {mid}")
            if c_index == 0 and not cid.endswith("c01"):
                errors.append(f"{mid}: first chapter must be c01, got {cid}")
            _check_localised(f"{cid}.title", chapter["title"], LANGUAGES, errors)
            lessons = chapter["lessons"]
            if not lessons:
                errors.append(f"{cid}: has no lessons")

            for l_index, lesson in enumerate(lessons):
                lid = lesson["id"]
                module_lessons += 1
                claim(lid, "lesson")
                if not LESSON_ID.match(lid):
                    errors.append(f"lesson id {lid!r} must look like mNNcNNlNN")
                if not lid.startswith(cid):
                    errors.append(f"lesson {lid} does not belong to chapter {cid}")
                if not lid.endswith("l%02d" % module_lessons):
                    errors.append(
                        f"{mid}: lesson {lid} should be number l{module_lessons:02d} "
                        f"(lessons are numbered across the whole module)"
                    )
                where = lid
                _check_localised(f"{where}.title", lesson["title"], LANGUAGES, errors)
                for field in TRILINGUAL:
                    _check_localised(f"{where}.{field}", lesson[field], LANGUAGES, errors)
                if lesson.get("takeaway"):
                    _check_localised(f"{where}.takeaway", lesson["takeaway"], LANGUAGES, errors)
                docs = lesson["docs"]
                if not docs.startswith("https://docs.python.org/3/"):
                    errors.append(f"{where}: docs link must be a docs.python.org/3/ URL, got {docs!r}")
                if lesson["visual"] and lesson["visual"] not in _VISUAL_NAMES:
                    errors.append(f"{where}: unknown visual {lesson['visual']!r}")

                examples = lesson["examples"]
                if len(examples) < 2:
                    errors.append(f"{where}: needs at least 2 code examples, has {len(examples)}")
                for n, example in enumerate(examples, 1):
                    if not example["code"].strip():
                        errors.append(f"{where}: example {n} has no code")
                    _check_localised(f"{where}.example{n}.title", example["title"], ("en",), errors)
                    if example.get("note"):
                        _check_localised(f"{where}.example{n}.note", example["note"], ("en",), errors)

                exercises = lesson["exercises"]
                if len(exercises) < 1:
                    errors.append(f"{where}: needs at least 1 exercise")
                for n, exercise in enumerate(exercises, 1):
                    claim(exercise["id"], "exercise")
                    if not exercise["id"].startswith(lid):
                        errors.append(f"exercise {exercise['id']} should start with its lesson id {lid}")
                    _check_localised(f"{where}.exercise{n}.prompt", exercise["prompt"], ("en", "hinglish"), errors)
                    if exercise.get("hint"):
                        _check_localised(f"{where}.exercise{n}.hint", exercise["hint"], ("en", "hinglish"), errors)
                    if not exercise["solution"].strip():
                        errors.append(f"{where}: exercise {n} has no solution")
                    if not exercise["checks"]:
                        errors.append(f"{where}: exercise {n} has no checks")
                    for check in exercise["checks"]:
                        try:
                            compile(check, "<check>", "eval")
                        except SyntaxError as exc:
                            errors.append(f"{where}: exercise {n} check is not valid Python: {check!r} ({exc})")

                quiz = lesson["quiz"]
                if len(quiz) < 3:
                    errors.append(f"{where}: needs at least 3 quiz questions, has {len(quiz)}")
                _validate_items(quiz, where, claim, errors)

        if module_lessons < 2:
            errors.append(f"{mid}: only {module_lessons} lesson(s); a module needs at least 2")
        _validate_items(module["exam"], f"{mid}.exam", claim, errors, minimum=5)
        _validate_items(module["skip_exam"], f"{mid}.skip_exam", claim, errors, minimum=8)

    # keyword coverage
    covered = {kw for m in modules for c in m["chapters"] for ls in c["lessons"] for kw in ls["keywords"]}
    missing = [kw for kw in PYTHON_KEYWORDS if kw not in covered]
    if missing:
        errors.append("Python keywords never taught: " + ", ".join(missing))
    unknown = sorted(kw for kw in covered if kw not in PYTHON_KEYWORDS + SOFT_KEYWORDS)
    if unknown:
        errors.append("keywords claimed but not Python keywords: " + ", ".join(unknown))

    lessons_total = sum(len(c["lessons"]) for m in modules for c in m["chapters"])
    if lessons_total < 45:
        errors.append(f"only {lessons_total} lessons; the completeness bar is 45")

    return errors


def _validate_items(items, where: str, claim, errors: list[str], minimum: int = 1) -> None:
    if len(items) < minimum:
        errors.append(f"{where}: needs at least {minimum} questions, has {len(items)}")
    for n, item in enumerate(items, 1):
        claim(item["id"], "quiz item")
        _check_localised(f"{where}.q{n}.question", item["question"], ("en",), errors)
        _check_localised(f"{where}.q{n}.why", item["why"], ("en", "hinglish"), errors)
        options = item["options"]
        if len(options) != 4:
            errors.append(f"{where}.q{n}: needs exactly 4 options, has {len(options)}")
        if len({o.strip() for o in options}) != len(options):
            errors.append(f"{where}.q{n}: duplicate options")
        if item["answer"] not in ("a", "b", "c", "d"):
            errors.append(f"{where}.q{n}: answer must be a/b/c/d, got {item['answer']!r}")
        if any(not str(o).strip() for o in options):
            errors.append(f"{where}.q{n}: has an empty option")


from .visuals import VISUALS  # noqa: E402  (avoids a circular import at module load)

_VISUAL_NAMES = set(VISUALS)
