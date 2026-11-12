"""Small authoring helpers so content files stay readable.

A lesson is written as one call with keyword arguments; quiz ids and exercise
ids are derived from the lesson id, which removes a whole class of copy-paste
mistakes from the curriculum.
"""
from __future__ import annotations

from ..schema import (
    Chapter,
    CodeExample,
    Exercise,
    Lesson,
    L,
    Module,
    QuizItem,
)

DEFAULT_EXAMPLE_TITLE = L("Example", "उदाहरण", "Example")


def _text(value):
    """Accept a plain string or an already-localised dict."""
    if isinstance(value, dict):
        return value
    return L(str(value))


def ex(code: str, output: str = "", title=DEFAULT_EXAMPLE_TITLE, note="") -> CodeExample:
    return CodeExample(
        title=_text(title),
        code=code.strip("\n"),
        output=output.strip("\n"),
        note=_text(note) if note else {},
    )


def quiz(question, options, answer: str, why, misconception: str = "") -> dict:
    """One question, before ids are assigned."""
    return {
        "question": _text(question),
        "options": list(options),
        "answer": answer,
        "why": _text(why),
        "misconception": misconception,
    }


def task(prompt, starter: str, solution: str, checks: list[str], hint="") -> dict:
    return {
        "prompt": _text(prompt),
        "starter": starter.strip("\n"),
        "solution": solution.strip("\n"),
        "checks": list(checks),
        "hint": _text(hint) if hint else {},
    }


def lesson(
    lid: str,
    title,
    keywords: list[str],
    intro,
    real_life,
    docs: str,
    examples: list[CodeExample],
    exercises: list[dict],
    quiz_items: list[dict],
    visual: str = "",
    takeaway="",
) -> Lesson:
    items = [
        QuizItem(
            id=f"{lid}q{n}",
            question=item["question"],
            options=item["options"],
            answer=item["answer"],
            why=item["why"],
            misconception=item["misconception"],
        )
        for n, item in enumerate(quiz_items, 1)
    ]
    return Lesson(
        id=lid,
        title=_text(title),
        keywords=list(keywords),
        intro=_text(intro),
        real_life=_text(real_life),
        docs=docs,
        visual=visual,
        examples=list(examples),
        exercises=[
            Exercise(
                id=f"{lid}e{n}",
                prompt=item["prompt"],
                starter=item["starter"],
                solution=item["solution"],
                checks=item["checks"],
                hint=item["hint"],
            )
            for n, item in enumerate(exercises, 1)
        ],
        quiz=items,
        takeaway=_text(takeaway) if takeaway else {},
    )


def chapter(cid: str, title, lessons: list[Lesson]) -> Chapter:
    return Chapter(id=cid, title=_text(title), lessons=list(lessons))


def module(
    mid: str,
    title,
    goal,
    chapters: list[Chapter],
    exam: list[dict],
    icon: str = "",
    skip_exam: list[dict] | None = None,
) -> Module:
    exam_items = [
        QuizItem(
            id=f"{mid}x{n:02d}",
            question=item["question"],
            options=item["options"],
            answer=item["answer"],
            why=item["why"],
            misconception=item["misconception"],
        )
        for n, item in enumerate(exam, 1)
    ]
    if skip_exam is None:
        # The skip exam is the union of every lesson quiz in the module plus the
        # module exam: you cannot skip a module by guessing six questions.  The
        # copies get their own ids so that every item in the course is unique.
        pool: list[QuizItem] = []
        for ch in chapters:
            for ls in ch.lessons:
                pool.extend(ls.quiz)
        pool.extend(exam_items)
        skip_items = [
            QuizItem(
                id=f"{mid}s{n:02d}",
                question=item.question,
                options=list(item.options),
                answer=item.answer,
                why=item.why,
                misconception=item.misconception,
            )
            for n, item in enumerate(pool, 1)
        ]
    else:
        skip_items = [
            QuizItem(
                id=f"{mid}s{n:02d}",
                question=item["question"],
                options=item["options"],
                answer=item["answer"],
                why=item["why"],
                misconception=item["misconception"],
            )
            for n, item in enumerate(skip_exam, 1)
        ]
    return Module(
        id=mid,
        title=_text(title),
        goal=_text(goal),
        chapters=list(chapters),
        exam=exam_items,
        skip_exam=skip_items,
        icon=icon,
    )
