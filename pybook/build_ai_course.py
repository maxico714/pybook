"""Build ``pybook/data/ai`` - the AI-engineering course - from authored lessons.

The chapter explanations live in the 23 notebooks of
``C:\\project\\aie-app\\notebooks`` (outlined by
``C:\\project\\ai-engineering-course``); the teachable layer and the question
banks live in :mod:`pybook.ai_syllabus`.  This script merges the two:

* every authored example is **run**, and its real stdout becomes ``output``;
* up to one extra pure-stdlib cell is lifted from the matching notebook, and is
  kept only when it runs cleanly and actually prints something;
* every exercise **solution** is executed through the same sandbox a learner
  uses (``web.runner.check_exercise``); one failing check stops the build;
* the module exam and the 90% skip exam are assembled from authored banks.

Nothing is written until every example and every solution passes, so a broken
lesson can never reach a learner.

Run from the repository root::

    python -m pybook.build_ai_course

Set ``PYBOOK_AI_NOTEBOOKS`` to point at a different notebook folder.
"""
from __future__ import annotations

import ast
import json
import os
import pathlib
import re
import sys

from .ai_syllabus import EXAMS, LESSONS, MODULES

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "pybook" / "data" / "ai"
DEFAULT_NOTEBOOKS = ROOT / "notebooks"

COURSE_ID = "ai"
PREFIX = "ai-"
MAX_EXAMPLES = 2
MAX_CELL_CHARS = 1200

# One short title per authored example - presentation metadata only.
EXAMPLE_TITLES = {
    1: ("Reading a .env file safely", "`.env` file safely padhna"),
    2: ("What one API call costs", "Ek API call ka cost"),
    3: ("Cosine similarity by hand", "Cosine similarity haath se"),
    4: ("A group mean without pandas", "Pandas ke bina group mean"),
    5: ("JOIN + GROUP BY in a dict", "Dict me JOIN aur GROUP BY"),
    6: ("Gini impurity of a node", "Node ki Gini impurity"),
    7: ("Training one neuron", "Ek neuron train karna"),
    8: ("Scaled attention scores", "Scaled attention scores"),
    9: ("Temperature changes the odds", "Temperature odds badalta hai"),
    10: ("Retry until the call works", "Retry jab tak call kaam kare"),
    11: ("Estimating tokens", "Tokens ka estimate"),
    12: ("Chunking with overlap", "Overlap ke saath chunking"),
    13: ("A tool registry", "Tool registry"),
    14: ("F1 from precision and recall", "Precision aur recall se F1"),
    15: ("How small LoRA really is", "LoRA kitna chhota hai"),
    16: ("Average pooling by hand", "Average pooling haath se"),
    17: ("Percent agreement", "Percent agreement"),
    18: ("A token bucket", "Token bucket"),
    19: ("Hashing a prompt version", "Prompt version ka hash"),
    20: ("Redacting PII", "PII redact karna"),
    21: ("Monthly cost estimate", "Monthly cost ka estimate"),
    22: ("ATS keyword match", "ATS keyword match"),
    23: ("Retrieval by word overlap", "Word overlap se retrieval"),
}


class BuildError(RuntimeError):
    """A lesson is not good enough to ship."""


def _t(hinglish: str, en: str) -> dict:
    return {"hinglish": hinglish, "en": en}


# --------------------------------------------------------------- notebooks
def _notebooks(folder: pathlib.Path) -> dict[int, pathlib.Path]:
    found: dict[int, pathlib.Path] = {}
    for path in sorted(folder.glob("*.ipynb")):
        head = path.name.split("_", 1)[0]
        if head.isdigit():
            found[int(head)] = path
    return found


def _chapter_title(path: pathlib.Path, number: int) -> str:
    """The notebook's own H1, minus the ``Chapter N -`` prefix."""
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "Chapter %d" % number
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        for line in cell.get("source", []):
            text = line.strip()
            if text.startswith("#"):
                title = text.lstrip("#").strip()
                title = re.sub(r"^Chapter\s+%d\s*[-:\u2014]\s*" % number, "", title)
                return title or ("Chapter %d" % number)
    return "Chapter %d" % number


def _cell_is_runnable(code: str, allowed: set[str]) -> bool:
    """True for a short, pure-stdlib cell with no magics or file access."""
    if not code.strip() or len(code) > MAX_CELL_CHARS:
        return False
    for line in code.splitlines():
        if line.strip().startswith(("%", "!")):
            return False
    for needle in ("get_ipython", "display(", "open(", "input(", "read_csv("):
        if needle in code:
            return False
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".")[0] not in allowed:
                    return False
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                return False
            if (node.module or "").split(".")[0] not in allowed:
                return False
    return True


def _from_notebook(path, allowed, run_code):
    """The first notebook cell that runs cleanly and prints something."""
    if path is None or not path.is_file():
        return None
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        code = "".join(cell.get("source", [])).strip("\n")
        if not _cell_is_runnable(code, allowed):
            continue
        result = run_code(code)
        if not result.get("ok") or not (result.get("stdout") or "").strip():
            continue
        return {
            "title": _t("Chapter notebook se", "Straight from the chapter notebook"),
            "code": code,
            "output": result["stdout"].strip("\n"),
            "note": {},
        }
    return None


# ------------------------------------------------------------------ payload
def _quiz(lesson_id: str, raw: dict) -> list[dict]:
    items = []
    for number, item in enumerate(raw["quiz"], 1):
        items.append(
            {
                "id": "%sq%d" % (lesson_id, number),
                "question": item["q"],
                "options": list(item["options"]),
                "answer": item["answer"],
                "why": item["why"],
                "misconception": "",
            }
        )
    return items


def _exercise(lesson_id: str, raw: dict) -> dict:
    exercise = raw["exercise"]
    return {
        "id": "%se1" % lesson_id,
        "prompt": exercise["prompt"],
        "starter": exercise["starter"],
        "solution": exercise["solution"],
        "checks": list(exercise["checks"]),
        "hint": exercise["hint"],
    }


def _lesson(number: int, module_id: str, notebooks, allowed, run_code, check_exercise) -> dict:
    raw = LESSONS[number]
    lesson_id = "%s%sc%02dl01" % (PREFIX, module_id, number)

    code = raw["example"]["code"]
    result = run_code(code)
    if not result.get("ok"):
        raise BuildError(
            "lesson %d: example does not run (%s)" % (number, result.get("error"))
        )
    if not (result.get("stdout") or "").strip():
        raise BuildError("lesson %d: example prints nothing" % number)

    hinglish, english = EXAMPLE_TITLES[number]
    examples = [
        {
            "title": _t(hinglish, english),
            "code": code,
            "output": result["stdout"].strip("\n"),
            "note": raw["example"].get("note") or {},
        }
    ]

    extra = _from_notebook(notebooks.get(number), allowed, run_code)
    if extra and extra["code"].strip() != code.strip():
        examples.append(extra)
    examples = examples[:MAX_EXAMPLES]

    exercise = _exercise(lesson_id, raw)
    checked = check_exercise(exercise["solution"], exercise["checks"])
    if not checked.get("passed"):
        failed = [entry for entry in checked.get("checks", []) if not entry["ok"]]
        detail = "; ".join("%s -> %s" % (entry["check"], entry.get("detail")) for entry in failed)
        raise BuildError(
            "lesson %d: solution fails %d check(s): %s"
            % (number, len(failed), detail or checked.get("error"))
        )

    starter = check_exercise(exercise["starter"], exercise["checks"])
    if starter.get("passed"):
        print("  ! lesson %d: the starter already passes - the task is too easy" % number)

    return {
        "id": lesson_id,
        "title": raw["title"],
        "keywords": list(raw["keywords"]),
        "intro": raw["intro"],
        "real_life": raw["real_life"],
        "takeaway": raw["takeaway"],
        "examples": examples,
        "exercises": [exercise],
        "quiz": _quiz(lesson_id, raw),
    }


def _module(module: dict, lessons: dict[int, dict]) -> dict:
    module_id = "%s%s" % (PREFIX, module["id"])
    chapters = []
    for number in module["chapters"]:
        body = lessons[number]
        chapters.append(
            {
                "id": body["id"].rsplit("l", 1)[0],
                "title": body["title"],
                "lessons": [body],
            }
        )

    exam = []
    for number, item in enumerate(EXAMS[module["id"]], 1):
        exam.append(
            {
                "id": "%sx%02d" % (module_id, number),
                "question": item["q"],
                "options": list(item["options"]),
                "answer": item["answer"],
                "why": item["why"],
                "misconception": "",
            }
        )

    # The 90% skip exam is the whole module in one sitting: every authored quiz
    # item plus the exam bank.  A module of two chapters would otherwise need a
    # perfect score, which is not a fair placement test.
    skip = []
    for number in module["chapters"]:
        for item in lessons[number]["quiz"]:
            skip.append(dict(item))
    for item in exam:
        skip.append(dict(item))
    for number, item in enumerate(skip, 1):
        item["id"] = "%ss%02d" % (module_id, number)

    return {
        "id": module_id,
        "title": module["title"],
        "goal": module["goal"],
        "icon": module["icon"],
        "chapters": chapters,
        "exam": exam,
        "skip_exam": skip,
    }


def _index(modules: list[dict]) -> dict:
    entries = []
    for module in modules:
        entries.append(
            {
                "id": module["id"],
                "title": module["title"],
                "goal": module["goal"],
                "icon": module["icon"],
                "lesson_count": sum(len(chapter["lessons"]) for chapter in module["chapters"]),
                "exam_count": len(module["exam"]),
                "skip_count": len(module["skip_exam"]),
                "chapters": [
                    {
                        "id": chapter["id"],
                        "title": chapter["title"],
                        "lessons": [
                            {
                                "id": lesson["id"],
                                "title": lesson["title"],
                                "keywords": lesson["keywords"],
                            }
                            for lesson in chapter["lessons"]
                        ],
                    }
                    for chapter in module["chapters"]
                ],
            }
        )
    return {
        "id": COURSE_ID,
        "title": _t(
            "AI Engineering — Zero se Production tak",
            "AI Engineering — From Zero to Production",
        ),
        "subtitle": _t(
            "23 chapters, 5 parts: setup se RAG, agents, evaluation aur capstone tak — har lesson "
            "me intro, real-life example, chalne wala code, mandatory practice aur quiz.",
            "23 chapters in 5 parts, from setup to RAG, agents, evaluation and capstones. Every "
            "lesson has an introduction, a real-life example, runnable code, mandatory practice "
            "and a quiz.",
        ),
        "modules": entries,
    }


# --------------------------------------------------------------------- main
def build(out_dir=None, notebook_dir=None) -> dict:
    """Build the course and return a summary.  Raises :class:`BuildError`."""
    from web.runner import ALLOWED_MODULES, check_exercise, run_code

    out_dir = pathlib.Path(out_dir) if out_dir else OUT_DIR
    folder = pathlib.Path(
        notebook_dir or os.environ.get("PYBOOK_AI_NOTEBOOKS") or DEFAULT_NOTEBOOKS
    )
    notebooks = _notebooks(folder)
    if not notebooks:
        print("  ! no notebooks found in %s - examples come from the authored lesson only" % folder)
    allowed = set(ALLOWED_MODULES)

    built: dict[int, dict] = {}
    modules: list[dict] = []
    for module in MODULES:
        print("%s %s" % (module["id"], module["title"]["en"]))
        for number in module["chapters"]:
            body = _lesson(number, module["id"], notebooks, allowed, run_code, check_exercise)
            built[number] = body
            print("  %2d %-58s %d example(s)" % (number, body["title"]["en"][:58], len(body["examples"])))
        modules.append(_module(module, built))

    # Chapter titles come from the notebooks, so the part view reads like the
    # source course instead of repeating the lesson title twice.
    for module, spec in zip(modules, MODULES):
        for chapter, number in zip(module["chapters"], spec["chapters"]):
            path = notebooks.get(number)
            if path is not None:
                chapter["title"] = _t(
                    _chapter_title(path, number), _chapter_title(path, number)
                )

    index = _index(modules)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    for module in modules:
        (out_dir / ("%s.json" % module["id"])).write_text(
            json.dumps(module, ensure_ascii=False, indent=1), encoding="utf-8"
        )

    return {
        "lessons": len(built),
        "modules": len(modules),
        "examples": sum(len(body["examples"]) for body in built.values()),
        "exercises": len(built),
        "questions": sum(len(body["quiz"]) for body in built.values()),
        "exam": sum(len(module["exam"]) for module in modules),
        "skip": sum(len(module["skip_exam"]) for module in modules),
        "out": str(out_dir),
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        summary = build(*argv)
    except BuildError as exc:
        print("\nBUILD FAILED: %s" % exc, file=sys.stderr)
        return 1
    print(
        "\nwrote {lessons} lessons in {modules} modules, {examples} runnable examples, "
        "{questions} quiz items, {exam} exam and {skip} skip items -> {out}".format(**summary)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
