"""Interactive practice drills, generated from content the course already owns.

Nothing here is invented.  Every drill is built from an authored lesson:

* **predict** - the example's own verified ``output`` is the answer;
* **order** - the example's real source lines are the pool;
* **blanks** - a keyword the lesson itself names is removed from real code.

Drills are deterministic for a given lesson id, so the page and the grading
endpoint rebuild exactly the same answer without storing it in the browser.
"""
from __future__ import annotations

import hashlib
import io
import random
import re
import tokenize

XP_DRILL = 5
XP_EXERCISE = 10
XP_LESSON = 20
XP_MODULE = 40

MAX_PREDICT_LINES = 6
MAX_PREDICT_CHARS = 260
MIN_ORDER_LINES = 3
MAX_ORDER_LINES = 10
MAX_BLANK_CODE = 420

_FALLBACK_TOKENS = (
    "for",
    "if",
    "def",
    "return",
    "while",
    "in",
    "not",
    "None",
    "True",
    "False",
    "import",
    "class",
    "try",
    "except",
)

_TITLES = {
    "predict": "Predict the output",
    "order": "Put the lines in order",
    "blanks": "Fill the blank",
}

_PROMPTS = {
    "predict": "Read the code and type exactly what it prints. Trailing spaces do not matter.",
    "order": "Tap the lines in the order they must run. Indentation is part of the answer.",
    "blanks": "Tap the missing word, then check. One blank, four choices.",
}


def _seed(lesson_id: str) -> int:
    return int(hashlib.sha256(lesson_id.encode("utf-8")).hexdigest()[:8], 16)


def _lines(code: str) -> list[str]:
    return [line.rstrip() for line in str(code or "").replace("\r\n", "\n").split("\n")]


def _normalise_output(text) -> str:
    lines = [line.rstrip() for line in str(text or "").replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    while lines and not lines[0]:
        lines.pop(0)
    return "\n".join(lines)


def _example_pairs(lesson: dict) -> list[tuple[int, dict]]:
    return list(enumerate(lesson.get("examples") or [], 1))


def _predict(lesson_id: str, lesson: dict):
    best = None
    for number, example in _example_pairs(lesson):
        output = _normalise_output(example.get("output"))
        code = str(example.get("code") or "").strip("\n")
        if not output or not code:
            continue
        if len(output) > MAX_PREDICT_CHARS or len(output.split("\n")) > MAX_PREDICT_LINES:
            continue
        if len(code) > 700:
            continue
        best = (number, example, output, code)
        break
    if not best:
        return None
    number, example, output, code = best
    return {
        "id": "%s-predict-%d" % (lesson_id, number),
        "kind": "predict",
        "title": _TITLES["predict"],
        "prompt": _PROMPTS["predict"],
        "code": code,
        "answer": output,
        "hint": "The program prints %d line%s. Watch the values, not the source."
        % (len(output.split("\n")), "" if len(output.split("\n")) == 1 else "s"),
        "xp": XP_DRILL,
    }


def _order(lesson_id: str, lesson: dict):
    best = None
    for number, example in _example_pairs(lesson):
        source = [line for line in _lines(example.get("code")) if line.strip()]
        if not (MIN_ORDER_LINES <= len(source) <= MAX_ORDER_LINES):
            continue
        best = (number, source)
        break
    if not best:
        return None
    number, source = best
    rng = random.Random(_seed(lesson_id) + number)
    shuffled = list(source)
    for _ in range(6):
        rng.shuffle(shuffled)
        if shuffled != source:
            break
    if shuffled == source:
        shuffled = source[1:] + source[:1]
    return {
        "id": "%s-order-%d" % (lesson_id, number),
        "kind": "order",
        "title": _TITLES["order"],
        "prompt": _PROMPTS["order"],
        "pool": [{"id": index, "text": text} for index, text in enumerate(shuffled)],
        "answer": source,
        "hint": "It starts with %r." % source[0].strip(),
        "xp": XP_DRILL,
    }


def _keyword_in_code(code: str, keywords: list[str]):
    """First real NAME token that is also a lesson keyword, as (row, start, end)."""
    wanted = set(keywords)
    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        for token in tokens:
            if token.type == tokenize.NAME and token.string in wanted:
                return token.string, token.start[0], token.start[1], token.end[1]
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return None
    return None


def _blanks(lesson_id: str, lesson: dict, keywords: list[str]):
    for number, example in _example_pairs(lesson):
        code = str(example.get("code") or "").strip("\n")
        if not code or len(code) > MAX_BLANK_CODE:
            continue
        found = _keyword_in_code(code, keywords)
        if not found:
            continue
        word, row, start, end = found
        rows = _lines(code)
        line = rows[row - 1]
        rows[row - 1] = line[:start] + "___" + line[end:]
        blanked = "\n".join(rows)
        if "___" not in blanked:
            continue
        options = [word]
        pool = [item for item in keywords if item != word] + list(_FALLBACK_TOKENS)
        for candidate in pool:
            if candidate not in options:
                options.append(candidate)
            if len(options) == 4:
                break
        random.Random(_seed(lesson_id) + 90 + number).shuffle(options)
        return {
            "id": "%s-blanks-%d" % (lesson_id, number),
            "kind": "blanks",
            "title": _TITLES["blanks"],
            "prompt": _PROMPTS["blanks"],
            "code": blanked,
            "options": options,
            "answer": word,
            "hint": "The lesson lists %d keyword%s; one of them is missing here."
            % (len(keywords), "" if len(keywords) == 1 else "s"),
            "xp": XP_DRILL,
        }
    return None


def build(lesson_id: str, lesson: dict) -> list[dict]:
    """Every optional drill this lesson can support, in a stable order."""
    keywords = [item for item in (lesson.get("keywords") or []) if isinstance(item, str)]
    drills = [_predict(lesson_id, lesson), _order(lesson_id, lesson), _blanks(lesson_id, lesson, keywords)]
    return [drill for drill in drills if drill]


def public(drill: dict) -> dict:
    """The part a browser is allowed to see - never ``answer``."""
    keep = ("id", "kind", "title", "prompt", "code", "pool", "options", "hint", "xp")
    return {key: drill[key] for key in keep if key in drill}


def find(lesson_id: str, lesson: dict, drill_id: str):
    for drill in build(lesson_id, lesson):
        if drill["id"] == drill_id:
            return drill
    return None


def grade(drill: dict, answer) -> dict:
    """Compare a submitted answer with the drill's own solution."""
    kind = drill["kind"]

    if kind == "predict":
        got = _normalise_output(answer if isinstance(answer, str) else "")
        want = drill["answer"]
        if got == want:
            return {"ok": True, "passed": True, "message": "Exactly right."}
        got_lines = got.split("\n")
        want_lines = want.split("\n")
        first = 0
        for index, (mine, theirs) in enumerate(zip(got_lines, want_lines)):
            if mine != theirs:
                first = index
                break
        else:
            first = min(len(got_lines), len(want_lines))
        return {
            "ok": True,
            "passed": False,
            "message": "Line %d does not match. Check that line and try again."
            % (first + 1),
            "detail": {"line": first + 1},
        }

    if kind == "order":
        submitted = answer if isinstance(answer, list) else []
        got = [str(item).rstrip() for item in submitted if str(item).strip()]
        want = [str(item).rstrip() for item in drill["answer"]]
        if got == want:
            return {"ok": True, "passed": True, "message": "That is the real order."}
        first = 0
        for index, (mine, theirs) in enumerate(zip(got, want)):
            if mine != theirs:
                first = index
                break
        else:
            first = min(len(got), len(want))
        return {
            "ok": True,
            "passed": False,
            "message": "Line %d of your sequence is wrong. Read it again." % (first + 1),
            "detail": {"line": first + 1},
        }

    if kind == "blanks":
        got = str(answer or "").strip()
        if got == drill["answer"]:
            return {"ok": True, "passed": True, "message": "That is the missing word."}
        return {
            "ok": True,
            "passed": False,
            "message": "Not that word. The line has to run as written.",
        }

    return {"ok": False, "error": "unknown drill"}
