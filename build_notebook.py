"""Build PyBook: the data files, the Colab bundle and the thin notebook.

The notebook is a build artefact: never hand-edit it.  Edit ``course/`` (the
curriculum) or ``pybook/`` (the runtime), then:

    python build_notebook.py

What it writes:

    pybook/data/index.json      the module/chapter/lesson tree (titles only)
    pybook/data/mNN.json        one file per module (lessons, exam, skip exam)
    pybook/data/visuals.json    the original SVG diagrams
    pybook_bundle.zip           the ``pybook`` folder, for uploading to Colab
    PyBook.ipynb                a small notebook: every cell is one short call

The notebook deliberately contains no curriculum and no runtime source: a cell
only calls ``start()``, ``show()``, ``answer(...)``, ``check(...)``, ``exam(...)``
and friends.  That is what keeps Colab responsive.
"""
from __future__ import annotations

import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "PyBook.ipynb"
PKG = ROOT / "pybook"
DATA = PKG / "data"
BUNDLE = ROOT / "pybook_bundle.zip"

sys.path.insert(0, str(ROOT))

from course.curriculum import COURSE, curriculum_dict  # noqa: E402
from course.validate import validate  # noqa: E402
from course.visuals import VISUALS  # noqa: E402

MAX_CELL_CHARS = 3000  # a bigger cell is the thing that made Colab hang


# ------------------------------------------------------------------ markdown

COVER = """# 🐍 PyBook — Python, From Zero to Confident

One notebook: **12 modules · 26 chapters · 53 lessons · 230 quiz questions**, and
every core Python keyword. Each lesson is an introduction, a real-life example,
runnable code and a quiz. Lessons unlock in order — you cannot jump ahead.

### How to run

1. Keep `PyBook.ipynb` **and** `pybook_bundle.zip` in the same folder (or the
   already-unpacked `pybook/` folder).
2. Run the next cell once per session. It finds the content, unpacks the bundle
   if needed, and starts the course.
3. Then run one cell at a time: `show()` → `answer(...)` → `check(...)` →
   `exam(...)`.

**Colab:** upload both files to `/content` and run the setup cell. If the bundle
is missing, the cell asks you to upload it.

Nothing is sent anywhere. No account, no network call. Progress is one local
JSON file.
"""

SETUP = '''import pathlib, sys, zipfile
root = pathlib.Path.cwd()
if not (root / "pybook").is_dir() and (root / "pybook_bundle.zip").is_file():
    zipfile.ZipFile(root / "pybook_bundle.zip").extractall(root)
if not (root / "pybook").is_dir():
    try:
        from google.colab import files
    except ImportError:
        raise SystemExit("Put pybook_bundle.zip next to this notebook, then re-run this cell.")
    print("Upload pybook_bundle.zip")
    files.upload()
    zipfile.ZipFile(root / "pybook_bundle.zip").extractall(root)
sys.path.insert(0, str(root))
from pybook import (start, show, answer, check, exam, skip, dashboard,
                    progress, review, language, guide, export, restore, reset)
course = start()
'''

APPENDIX = """## 📌 Extras

| Call | What it does |
|---|---|
| `dashboard()` | every module and how far you are |
| `show()` | the lesson you have reached |
| `answer(q1="b", ...)` | answer its quiz, 80% passes |
| `check("your code")` | test exercise 1 (add `n=2` for exercise 2) |
| `exam(q1="b", ...)` | module exam, after every lesson in the module |
| `skip(q1="b", ...)` | already know the module? 90% skips it |
| `review()` | questions you answered wrong |
| `language("hi")` | `en`, `hi` or `hinglish` |
| `export()` / `restore(text)` | move progress between machines |
| `reset(confirm=True)` | start over |
| `guide()` | the command card inside the notebook |

**Where progress lives:** `course.path` prints it. In Colab with Drive mounted it
is `/content/drive/MyDrive/PyBook/progress.json`; otherwise next to the notebook.
Without Drive it disappears when the runtime resets — use `export()`.

### Licence

MIT. The diagrams are original SVG stored in `pybook/data/visuals.json`; no
third-party image assets are bundled.
"""


# --------------------------------------------------------------------- cells

def _cell(kind: str, source: str, cid: str) -> dict:
    lines = source.split("\n")
    payload = [line + "\n" for line in lines[:-1]] + [lines[-1]]
    cell = {"cell_type": kind, "id": cid, "metadata": {}, "source": payload}
    if kind == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell


def _index(data: dict) -> dict:
    """The light tree: titles and counts only, no lesson bodies."""
    return {
        "id": data["id"],
        "title": data["title"],
        "subtitle": data["subtitle"],
        "modules": [
            {
                "id": module["id"],
                "title": module["title"],
                "goal": module["goal"],
                "icon": module.get("icon", ""),
                "lesson_count": sum(len(c["lessons"]) for c in module["chapters"]),
                "exam_count": len(module.get("exam", [])),
                "skip_count": len(module.get("skip_exam", [])),
                "chapters": [
                    {
                        "id": chapter["id"],
                        "title": chapter["title"],
                        "lessons": [
                            {
                                "id": lesson["id"],
                                "title": lesson["title"],
                                "visual": lesson.get("visual", ""),
                            }
                            for lesson in chapter["lessons"]
                        ],
                    }
                    for chapter in module["chapters"]
                ],
            }
            for module in data["modules"]
        ],
    }


def write_data() -> dict:
    DATA.mkdir(parents=True, exist_ok=True)
    data = curriculum_dict()

    index = _index(data)
    (DATA / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    for module in data["modules"]:
        (DATA / ("%s.json" % module["id"])).write_text(
            json.dumps(module, ensure_ascii=False, indent=1), encoding="utf-8"
        )
    (DATA / "visuals.json").write_text(
        json.dumps(VISUALS, ensure_ascii=False), encoding="utf-8"
    )
    return index


def write_bundle() -> int:
    if BUNDLE.exists():
        BUNDLE.unlink()
    with zipfile.ZipFile(BUNDLE, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PKG.rglob("*")):
            if "__pycache__" in path.parts or path.suffix == ".pyc" or path.is_dir():
                continue
            archive.write(path, path.relative_to(ROOT).as_posix())
    return BUNDLE.stat().st_size


def build() -> dict:
    cells: list[dict] = []

    def add(kind: str, source: str) -> None:
        cells.append(_cell(kind, source, "c%03d" % (len(cells) + 1)))

    add("markdown", COVER)
    add("code", SETUP)
    add("code", "dashboard()")

    add(
        "markdown",
        "## 1 · Read the lesson\n\n"
        "Run this cell whenever you sit down to study. It opens the lesson you have "
        "reached — nothing later is reachable, and locked lessons show a lock card "
        "instead of their content.",
    )
    add("code", "show()")

    add(
        "markdown",
        "## 2 · Answer the quiz\n\n"
        "Replace the letters with your answers and run the cell. "
        "80% passes and unlocks the next lesson.",
    )
    add("code", '# answer(q1="a", q2="b", q3="c")')

    add(
        "markdown",
        "## 3 · Practise\n\n"
        "Write your code inside the call and run it. The checker runs the exercise's "
        "own assertions and tells you which one failed.",
    )
    add("code", '# check("""\n# write your code here\n# """)')

    add(
        "markdown",
        "## 4 · Module exam\n\n"
        "The exam opens only after every lesson in the module is passed. If you "
        "already know the module, the skip exam needs 90%.",
    )
    add("code", '# exam(q1="a", q2="b", q3="c")\n# skip(q1="a", q2="b", q3="c")')

    add("markdown", APPENDIX)
    add("code", "progress()")

    for cell in cells:
        size = len("".join(cell["source"]))
        if size > MAX_CELL_CHARS:
            raise SystemExit(
                "cell %s is %d characters - keep cells small so Colab stays "
                "responsive" % (cell["id"], size)
            )

    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.12"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> int:
    errors = validate(COURSE)
    if errors:
        print("refusing to build: %d validation error(s)" % len(errors))
        for error in errors[:20]:
            print(" -", error)
        return 1

    index = write_data()
    size = write_bundle()
    notebook = build()
    OUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")

    lessons = sum(module["lesson_count"] for module in index["modules"])
    questions = sum(
        len(chapter_lesson.get("quiz", []))
        for module in curriculum_dict()["modules"]
        for chapter in module["chapters"]
        for chapter_lesson in chapter["lessons"]
    )
    print(
        "wrote %s: %d cells, %d modules, %d lessons, %d quiz questions"
        % (OUT.name, len(notebook["cells"]), len(index["modules"]), lessons, questions)
    )
    print("wrote pybook/data (index + %d module files + visuals)" % len(index["modules"]))
    print("wrote pybook_bundle.zip: %.0f KB" % (size / 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
