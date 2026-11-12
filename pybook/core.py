"""PyBook core: rendering, gating, scoring and progress storage.

This module is shipped as plain files next to the notebook, so a cell only ever
has to call a small function.  Content is read lazily from ``pybook/data``:

    data/index.json      the module/chapter/lesson tree (titles only)
    data/mNN.json        one module's full lessons, exam and skip exam
    data/visuals.json    the original SVG diagrams

Dependency-free: standard library only, with IPython used when it happens to
exist.  Every renderer returns a string as well as displaying it, which is what
the test suite drives.
"""
from __future__ import annotations

import copy
import datetime as _dt
import html
import json
import os
import pathlib
import re
import sys
import traceback

LANGUAGES = ("en", "hi", "hinglish")
LANGUAGE_NAMES = {"en": "English", "hi": "हिन्दी", "hinglish": "Hinglish"}
PROGRESS_VERSION = 1

LESSON_PASS = 0.8
EXAM_PASS = 0.8
SKIP_PASS = 0.9

INK = "#0f172a"
MUTED = "#475569"
CARD = "#ffffff"
LINE = "#e2e8f0"
ACCENT = "#1d4ed8"
GREEN = "#166534"
GREEN_BG = "#dcfce7"
RED = "#991b1b"
RED_BG = "#fee2e2"
AMBER = "#92400e"
AMBER_BG = "#fef3c7"
BLUE_BG = "#eff6ff"

_CSS = f"""
.pc-wrap{{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:{INK};
 max-width:940px;line-height:1.6}}
.pc-card{{border:1px solid {LINE};border-radius:12px;padding:14px 16px;margin:12px 0;background:{CARD}}}
.pc-title{{font-size:22px;font-weight:700;margin:0 0 4px}}
.pc-sub{{color:{MUTED};font-size:13px;margin:0 0 10px}}
.pc-chip{{display:inline-block;font-family:ui-monospace,Consolas,monospace;font-size:12px;
 background:{BLUE_BG};color:{ACCENT};border:1px solid #bfdbfe;border-radius:999px;padding:1px 9px;margin:2px 4px 2px 0}}
.pc-h{{font-size:15px;font-weight:700;margin:16px 0 6px}}
.pc-p{{margin:6px 0;font-size:14.5px}}
.pc-code{{background:#0b1220;color:#e2e8f0;border-radius:10px;padding:12px 14px;overflow-x:auto;
 font-family:ui-monospace,Consolas,monospace;font-size:13px;white-space:pre;margin:8px 0}}
.pc-out{{background:#f1f5f9;border-left:4px solid #94a3b8;border-radius:0 8px 8px 0;padding:10px 12px;
 font-family:ui-monospace,Consolas,monospace;font-size:12.5px;white-space:pre-wrap;margin:0 0 10px;color:#1e293b}}
.pc-real{{background:{AMBER_BG};border-left:5px solid {AMBER};border-radius:0 10px 10px 0;padding:10px 14px;margin:10px 0}}
.pc-take{{background:{GREEN_BG};border-left:5px solid {GREEN};border-radius:0 10px 10px 0;padding:10px 14px;margin:10px 0}}
.pc-ok{{background:{GREEN_BG};color:{GREEN};border-radius:8px;padding:8px 12px;font-weight:600}}
.pc-bad{{background:{RED_BG};color:{RED};border-radius:8px;padding:8px 12px;font-weight:600}}
.pc-lock{{background:#f8fafc;border:1px dashed #cbd5e1;color:{MUTED};border-radius:10px;padding:14px}}
.pc-row{{display:flex;justify-content:space-between;gap:10px;padding:5px 0;border-bottom:1px solid #f1f5f9;font-size:14px}}
.pc-bar{{height:8px;background:#e2e8f0;border-radius:999px;overflow:hidden;margin:4px 0 10px}}
.pc-bar>i{{display:block;height:100%;background:{ACCENT}}}
.pc-q{{border-top:1px solid {LINE};padding-top:10px;margin-top:12px}}
.pc-opt{{font-family:ui-monospace,Consolas,monospace;font-size:13.5px;margin:3px 0 3px 10px}}
.pc-small{{color:{MUTED};font-size:12px}}
a{{color:{ACCENT}}}
"""


# --------------------------------------------------------------------- helpers

def _now() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat()


def _display(html_text: str) -> None:
    """Show HTML in a notebook, or readable text when IPython is absent."""
    try:
        from IPython.display import HTML, display  # type: ignore

        display(HTML(_CSS + html_text))
        return
    except Exception:
        pass
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html_text, flags=re.S | re.I)
    text = re.sub(r"<br\s*/?>|</p>|</div>|</h[1-6]>|</li>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    print("\n".join(line.rstrip() for line in text.splitlines()).strip())


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _pct(x: float) -> str:
    return "%d%%" % round(x * 100)


def _raises(func, *args, exc: type = Exception, **kwargs) -> bool:
    """True only when calling ``func`` raises the expected exception type.

    Exercises use this so "must raise an error" can be tested with a plain
    assertion instead of a try/except block the learner has to write.
    """
    try:
        func(*args, **kwargs)
    except exc:
        return True
    except Exception:
        return False
    return False


def default_progress_path() -> pathlib.Path:
    """Progress file: explicit env var, then Google Drive, then this directory.

    ``PYBOOK_PROGRESS`` exists so the test suite (and anyone scripting the
    course) can point progress at a throwaway file without touching the
    learner's real one.
    """
    override = os.environ.get("PYBOOK_PROGRESS")
    if override:
        return pathlib.Path(override)
    drive = pathlib.Path("/content/drive/MyDrive")
    if drive.is_dir():
        return drive / "PyBook" / "progress.json"
    return pathlib.Path.cwd() / "pybook_progress.json"


# ---------------------------------------------------------------------- course

class Course:
    """Drives the whole course: one object, one progress file, lazy content.

    ``source`` may be:

    * ``None`` - read the shipped ``pybook/data`` folder next to this module;
    * a path - read ``<path>/data``;
    * a dict - use that in-memory curriculum (what the authoring tests do).
    """

    def __init__(self, source=None, progress_path=None, language: str = "hinglish",
                 verbose: bool = True):
        if isinstance(source, dict):
            data = source
            self._file_backed = False
            self.root = pathlib.Path(__file__).resolve().parent
        else:
            self.root = pathlib.Path(source) if source else pathlib.Path(__file__).resolve().parent
            self._file_backed = True
            index = self.root / "data" / "index.json"
            if not index.is_file():
                raise FileNotFoundError(
                    "PyBook content is missing: expected %s. Unzip pybook_bundle.zip "
                    "next to the notebook and run the setup cell again." % index
                )
            data = json.loads(index.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "modules" not in data:
            raise ValueError("curriculum data must be a dict with a 'modules' key")
        self.data = data
        self.modules: list[dict] = data["modules"]
        self.lessons: list[dict] = [
            ls for m in self.modules for c in m["chapters"] for ls in c["lessons"]
        ]
        self.by_lesson = {ls["id"]: ls for ls in self.lessons}
        self.by_module = {m["id"]: m for m in self.modules}
        self.by_chapter = {c["id"]: c for m in self.modules for c in m["chapters"]}
        self._chapter_of_lesson = {
            ls["id"]: c["id"] for m in self.modules for c in m["chapters"] for ls in c["lessons"]
        }
        self._module_of_lesson = {
            ls["id"]: m["id"] for m in self.modules for c in m["chapters"] for ls in c["lessons"]
        }
        self._module_of_chapter = {
            c["id"]: m["id"] for m in self.modules for c in m["chapters"]
        }
        self._order = [ls["id"] for ls in self.lessons]
        self._full_cache: dict[str, dict] = {}
        self._visual_cache = None
        self.current = None
        self.path = pathlib.Path(progress_path) if progress_path else default_progress_path()
        self.verbose = verbose
        self.state = self._blank_state(language)
        self._load()
        if self.state.get("language") not in LANGUAGES:
            self.state["language"] = language

    # ------------------------------------------------------------ content io
    def _full(self, module_id: str) -> dict:
        """The complete module (lessons, exam, skip exam), loaded once."""
        if not self._file_backed:
            return self.by_module[module_id]
        if module_id not in self._full_cache:
            path = self.root / "data" / ("%s.json" % module_id)
            self._full_cache[module_id] = json.loads(path.read_text(encoding="utf-8"))
        return self._full_cache[module_id]

    def _lesson(self, lesson_id: str):
        if not self._file_backed:
            return self.by_lesson.get(lesson_id)
        module_id = self._module_of_lesson.get(lesson_id)
        if not module_id:
            return None
        for chapter in self._full(module_id)["chapters"]:
            for lesson in chapter["lessons"]:
                if lesson["id"] == lesson_id:
                    return lesson
        return None

    def _exercise(self, exercise_id: str):
        match = re.match(r"^(.*)e(\d+)$", exercise_id)
        if not match:
            return None
        lesson = self._lesson(match.group(1))
        if not lesson:
            return None
        index = int(match.group(2)) - 1
        exercises = lesson.get("exercises", [])
        if 0 <= index < len(exercises):
            return exercises[index]
        return None

    def _visuals(self) -> dict:
        if self._visual_cache is None:
            if self._file_backed:
                path = self.root / "data" / "visuals.json"
                self._visual_cache = json.loads(path.read_text(encoding="utf-8"))
            else:
                self._visual_cache = VISUAL_REGISTRY
        return self._visual_cache

    # ------------------------------------------------------------- state io
    def _blank_state(self, language: str) -> dict:
        return {
            "version": PROGRESS_VERSION,
            "language": language,
            "created": _now(),
            "updated": _now(),
            "lessons": {},
            "modules": {},
            "missed": {},
            "log": [],
        }

    def _load(self) -> None:
        path = self.path
        if not path.is_file():
            return
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise ValueError("progress file is not a JSON object")
        except Exception as exc:
            backup = path.with_suffix(path.suffix + ".corrupt-%s" % _dt.datetime.now().strftime("%Y%m%d%H%M%S"))
            try:
                path.replace(backup)
            except Exception:
                backup = None
            if self.verbose:
                print("⚠️  Progress file could not be read (%s: %s)." % (type(exc).__name__, exc))
                print("   A fresh file was started%s." % (" and the old one kept as %s" % backup.name if backup else ""))
            return
        state = self._blank_state(raw.get("language", self.state["language"]))
        for key in ("language", "created", "updated", "lessons", "modules", "missed", "log"):
            if key in raw and isinstance(raw[key], type(state[key])):
                state[key] = raw[key]
        state["version"] = PROGRESS_VERSION
        self.state = state

    def _save(self) -> None:
        self.state["updated"] = _now()
        self.state["version"] = PROGRESS_VERSION
        path = self.path
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(path.suffix + ".tmp")
            tmp.write_text(json.dumps(self.state, indent=2, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp, path)
        except Exception as exc:
            print("⚠️  Could not save progress to %s (%s: %s)." % (path, type(exc).__name__, exc))
            print("   Your answers in this session still count, but they will be lost on restart.")

    # -------------------------------------------------------------- language
    def set_language(self, code: str) -> str:
        code = (code or "").strip().lower()
        aliases = {"english": "en", "en-us": "en", "hindi": "hi", "हिन्दी": "hi",
                   "hinglish": "hinglish", "hi-en": "hinglish", "hing": "hinglish"}
        code = aliases.get(code, code)
        if code not in LANGUAGES:
            raise ValueError("language must be one of %s (got %r)" % (", ".join(LANGUAGES), code))
        self.state["language"] = code
        self._save()
        return code

    def language(self, code: str | None = None):
        if code:
            return self.set_language(code)
        return self.state["language"]

    def t(self, field) -> str:
        """Resolve a localised field with a documented fallback chain."""
        if isinstance(field, str):
            return field
        if not field:
            return ""
        lang = self.state.get("language", "hinglish")
        for key in (lang, "hinglish", "en"):
            value = field.get(key)
            if value:
                return value
        for value in field.values():
            if value:
                return value
        return ""

    # ---------------------------------------------------------------- gating
    def lesson_passed(self, lesson_id: str) -> bool:
        return bool(self.state["lessons"].get(lesson_id, {}).get("passed"))

    def module_passed(self, module_id: str) -> bool:
        rec = self.state["modules"].get(module_id, {})
        return bool(rec.get("exam_passed") or rec.get("skipped"))

    def chapter_passed(self, chapter_id: str) -> bool:
        chapter = self.by_chapter.get(chapter_id)
        if not chapter:
            return False
        return all(self.lesson_passed(ls["id"]) for ls in chapter["lessons"])

    def _prev_lesson(self, lesson_id: str):
        i = self._order.index(lesson_id)
        return self._order[i - 1] if i > 0 else None

    def lesson_unlocked(self, lesson_id: str) -> bool:
        if lesson_id not in self.by_lesson:
            return False
        chapter_id = self._chapter_of_lesson[lesson_id]
        if not self.chapter_unlocked(chapter_id):
            return False
        chapter = self.by_chapter[chapter_id]
        first = chapter["lessons"][0]["id"]
        if lesson_id == first:
            return True
        prev = self._prev_lesson(lesson_id)
        return bool(prev and (self.lesson_passed(prev) or self.chapter_passed(chapter_id)))

    def chapter_unlocked(self, chapter_id: str) -> bool:
        module_id = self._module_of_chapter.get(chapter_id)
        if not module_id:
            return False
        if not self.module_unlocked(module_id):
            return False
        chapters = self.by_module[module_id]["chapters"]
        first = chapters[0]["id"]
        if chapter_id == first:
            return True
        ids = [c["id"] for c in chapters]
        prev = ids[ids.index(chapter_id) - 1]
        return self.chapter_passed(prev)

    def module_unlocked(self, module_id: str) -> bool:
        ids = [m["id"] for m in self.modules]
        if module_id not in ids:
            return False
        i = ids.index(module_id)
        if i == 0:
            return True
        return self.module_passed(ids[i - 1])

    def next_lesson_id(self):
        for lesson_id in self._order:
            if self.lesson_unlocked(lesson_id) and not self.lesson_passed(lesson_id):
                return lesson_id
        return None

    # -------------------------------------------------------------- scoring
    @staticmethod
    def _normalise(answers, items: list[dict]) -> dict:
        if answers is None:
            return {}
        if isinstance(answers, dict):
            return {str(k): str(v).strip().lower() for k, v in answers.items()}
        if isinstance(answers, (list, tuple)):
            out = {}
            for item, value in zip(items, answers):
                if value is not None and str(value).strip():
                    out[item["id"]] = str(value).strip().lower()
            return out
        raise TypeError("answers must be a dict {question_id: 'a'} or a list in question order")

    def _score(self, items: list[dict], answers) -> tuple[float, list[dict], dict]:
        given = self._normalise(answers, items)
        detail = []
        correct = 0
        for position, item in enumerate(items, 1):
            # The notebook teaches {"q1": "b"}; internal ids also work, which is
            # what a list of answers and the tests use.
            got = given.get(item["id"])
            if got is None:
                got = given.get("q%d" % position, "")
            ok = got == item["answer"].lower()
            correct += int(ok)
            detail.append({"item": item, "given": got, "ok": ok})
        total = len(items) or 1
        return correct / total, detail, given

    def _record_missed(self, detail: list[dict]) -> None:
        for row in detail:
            item = row["item"]
            if row["ok"]:
                self.state["missed"].pop(item["id"], None)
            else:
                self.state["missed"][item["id"]] = {
                    "question": item["question"].get("en", ""),
                    "times": int(self.state["missed"].get(item["id"], {}).get("times", 0)) + 1,
                    "at": _now(),
                }

    def _log(self, kind: str, target: str, score: float, passed: bool) -> None:
        self.state["log"].append(
            {"kind": kind, "target": target, "score": round(score, 3), "passed": passed, "at": _now()}
        )
        self.state["log"] = self.state["log"][-400:]

    # ------------------------------------------------------------ rendering
    def render_cover(self) -> str:
        total = len(self.lessons)
        return (
            f'<div class="pc-wrap"><div class="pc-card">'
            f'<p class="pc-title">{_e(self.t(self.data["title"]))}</p>'
            f'<p class="pc-sub">{_e(self.t(self.data["subtitle"]))}</p>'
            f'<p class="pc-p">{total} lessons · {len(self.modules)} modules · '
            f"{len(self.by_chapter)} chapters · language: "
            f"<b>{_e(LANGUAGE_NAMES[self.state['language']])}</b></p>"
            f"</div></div>"
        )

    def render_dashboard(self) -> str:
        done = sum(1 for ls in self.lessons if self.lesson_passed(ls["id"]))
        total = len(self.lessons)
        overall = done / total if total else 0.0
        rows = []
        for module in self.modules:
            lessons = [ls for c in module["chapters"] for ls in c["lessons"]]
            mdone = sum(1 for ls in lessons if self.lesson_passed(ls["id"]))
            share = mdone / len(lessons) if lessons else 0.0
            if self.module_passed(module["id"]):
                badge = '<span class="pc-ok">passed</span>'
            elif self.module_unlocked(module["id"]):
                badge = '<span class="pc-small">unlocked</span>'
            else:
                badge = '<span class="pc-small">🔒 locked</span>'
            rows.append(
                f'<div class="pc-row"><span>{_e(module.get("icon", ""))} '
                f'{_e(self.t(module["title"]))}</span>'
                f"<span>{mdone}/{len(lessons)} {badge}</span></div>"
                f'<div class="pc-bar"><i style="width:{share * 100:.0f}%"></i></div>'
            )
        nxt = self.next_lesson_id()
        if nxt:
            lesson = self.by_lesson[nxt]
            hint = (
                f'<p class="pc-p">Next: <b>{_e(self.t(lesson["title"]))}</b> '
                f'<code>{_e(nxt)}</code></p>'
                f'<p class="pc-small">Run: course.lesson("{_e(nxt)}")</p>'
            )
        else:
            hint = '<p class="pc-ok">Every lesson is passed. Well done.</p>'
        return (
            f'<div class="pc-wrap"><div class="pc-card">'
            f'<p class="pc-title">Your progress</p>'
            f'<p class="pc-sub">{done} of {total} lessons passed · {_pct(overall)}</p>'
            f'<div class="pc-bar"><i style="width:{overall * 100:.0f}%"></i></div>'
            + "".join(rows)
            + hint
            + f'<p class="pc-small">Progress file: {_e(self.path)}</p>'
            f"</div></div>"
        )

    def render_module(self, module_id: str) -> str:
        module = self.by_module.get(module_id)
        if not module:
            return f'<div class="pc-bad">Unknown module: {_e(module_id)}</div>'
        if not self.module_unlocked(module_id):
            ids = [m["id"] for m in self.modules]
            prev = ids[ids.index(module_id) - 1]
            return (
                f'<div class="pc-wrap"><div class="pc-lock">🔒 <b>{_e(self.t(module["title"]))}</b> '
                f"is locked.<br>Pass the exam of module <code>{_e(prev)}</code> first: "
                f'<code>course.exam("{_e(prev)}", {{...}})</code></div></div>'
            )
        body = []
        for chapter in module["chapters"]:
            open_ = self.chapter_unlocked(chapter["id"])
            body.append(
                f'<div class="pc-h">{_e(self.t(chapter["title"]))} '
                f'<span class="pc-small">{"open" if open_ else "🔒"}</span></div>'
            )
            for lesson in chapter["lessons"]:
                passed = self.lesson_passed(lesson["id"])
                unlocked = self.lesson_unlocked(lesson["id"])
                mark = "✅" if passed else ("▶️" if unlocked else "🔒")
                body.append(
                    f'<div class="pc-row"><span>{mark} {_e(self.t(lesson["title"]))}</span>'
                    f'<span class="pc-small">{_e(lesson["id"])}</span></div>'
                )
        exam_done = self.module_passed(module_id)
        body.append(
            f'<p class="pc-p">Module exam: {"passed" if exam_done else "not passed yet"} '
            f'({len(module.get("exam", []))} questions, {_pct(EXAM_PASS)} to pass)</p>'
        )
        return (
            f'<div class="pc-wrap"><div class="pc-card">'
            f'<p class="pc-title">{_e(module.get("icon", ""))} {_e(self.t(module["title"]))}</p>'
            f'<p class="pc-sub">{_e(self.t(module["goal"]))}</p>'
            + "".join(body)
            + "</div></div>"
        )

    def render_lesson(self, lesson_id: str) -> str:
        lesson = self._lesson(lesson_id)
        if not lesson:
            return f'<div class="pc-bad">Unknown lesson: {_e(lesson_id)}</div>'
        if not self.lesson_unlocked(lesson_id):
            prev = self._prev_lesson(lesson_id)
            need = (
                f'Pass <code>{_e(prev)}</code> first.'
                if prev
                else "Finish the earlier chapters first."
            )
            return (
                f'<div class="pc-wrap"><div class="pc-lock">🔒 <b>{_e(self.t(lesson["title"]))}</b>'
                f" is locked.<br>{need}</div></div>"
            )
        parts = [
            f'<div class="pc-wrap"><div class="pc-card">',
            f'<p class="pc-title">{_e(self.t(lesson["title"]))}</p>',
            f'<p class="pc-sub">{_e(lesson_id)} · {len(lesson.get("quiz", []))} quiz questions '
            f"· {_pct(LESSON_PASS)} to unlock the next lesson</p>",
        ]
        if lesson.get("keywords"):
            parts.append(
                "".join(f'<span class="pc-chip">{_e(k)}</span>' for k in lesson["keywords"])
            )
        parts.append(f'<div class="pc-h">1 · Introduction</div>')
        parts.append(f'<p class="pc-p">{_e(self.t(lesson["intro"]))}</p>')
        if lesson.get("visual") and lesson["visual"] in self._visuals():
            svg, caption = self._visuals()[lesson["visual"]]
            parts.append(svg)
        parts.append('<div class="pc-h">2 · Real life example</div>')
        parts.append(f'<div class="pc-real">{_e(self.t(lesson["real_life"]))}</div>')
        parts.append('<div class="pc-h">3 · Code examples</div>')
        for example in lesson.get("examples", []):
            parts.append(f'<p class="pc-p"><b>{_e(self.t(example["title"]))}</b></p>')
            parts.append(f'<div class="pc-code">{_e(example["code"].strip())}</div>')
            if example.get("output"):
                parts.append(f'<div class="pc-out">{_e(example["output"].strip())}</div>')
            if example.get("note"):
                parts.append(f'<p class="pc-small">{_e(self.t(example["note"]))}</p>')
        if lesson.get("exercises"):
            parts.append('<div class="pc-h">4 · Exercises</div>')
            for i, ex in enumerate(lesson["exercises"], 1):
                parts.append(
                    f'<p class="pc-p"><b>Exercise {i}.</b> {_e(self.t(ex["prompt"]))}</p>'
                )
                parts.append(f'<div class="pc-code">{_e(ex["starter"].strip())}</div>')
                if ex.get("hint"):
                    parts.append(
                        f'<p class="pc-small">Hint: {_e(self.t(ex["hint"]))}</p>'
                    )
                parts.append(
                    f'<p class="pc-small">Check it with: '
                    f'<code>course.check("{_e(ex["id"])}", your_code)</code></p>'
                )
                parts.append(
                    f'<details><summary class="pc-small">Show solution</summary>'
                    f'<div class="pc-code">{_e(ex["solution"].strip())}</div></details>'
                )
        parts.append('<div class="pc-h">5 · Quiz</div>')
        for n, item in enumerate(lesson.get("quiz", []), 1):
            parts.append(f'<div class="pc-q"><p class="pc-p"><b>Q{n}.</b> {_e(self.t(item["question"]))}</p>')
            for letter, option in zip("abcd", item["options"]):
                parts.append(f'<div class="pc-opt">{letter}) {_e(option)}</div>')
            parts.append("</div>")
        parts.append(
            f'<div class="pc-code">course.quiz("{_e(lesson_id)}", '
            f'{{"q1": "a", "q2": "b", "q3": "c"}})</div>'
        )
        if lesson.get("takeaway"):
            parts.append(f'<div class="pc-take"><b>Remember:</b> {_e(self.t(lesson["takeaway"]))}</div>')
        if lesson.get("docs"):
            parts.append(
                f'<p class="pc-small">Official docs: '
                f'<a href="{_e(lesson["docs"])}" target="_blank" rel="noopener">{_e(lesson["docs"])}</a></p>'
            )
        rec = self.state["lessons"].get(lesson_id, {})
        if rec.get("passed"):
            parts.append(
                f'<p class="pc-ok">Passed with {_pct(rec.get("best_score", 0))} '
                f'(best of {rec.get("attempts", 1)} attempt(s))</p>'
            )
        parts.append("</div></div>")
        return "".join(parts)

    def _feedback(self, title: str, score: float, need: float, detail: list[dict],
                  passed: bool, next_hint: str = "") -> str:
        rows = []
        for n, row in enumerate(detail, 1):
            item = row["item"]
            if row["ok"]:
                rows.append(f'<p class="pc-p">✅ <b>Q{n}</b> correct.</p>')
            else:
                correct = item["answer"].lower()
                right = item["options"]["abcd".index(correct)] if correct in "abcd" else "?"
                rows.append(
                    f'<p class="pc-p">❌ <b>Q{n}</b> you answered '
                    f'<code>{_e(row["given"] or "-")}</code>; the answer is '
                    f'<code>{_e(correct)}</code> ({_e(right)}).</p>'
                    f'<p class="pc-small">{_e(self.t(item["why"]))}</p>'
                )
        verdict = (
            f'<p class="pc-ok">Passed · {_pct(score)} (needed {_pct(need)})</p>'
            if passed
            else f'<p class="pc-bad">Not yet · {_pct(score)} (needed {_pct(need)})</p>'
        )
        return (
            f'<div class="pc-wrap"><div class="pc-card"><p class="pc-title">{_e(title)}</p>'
            f"{verdict}{''.join(rows)}"
            + (f'<p class="pc-p">{next_hint}</p>' if next_hint else "")
            + "</div></div>"
        )

    # ------------------------------------------------------------- commands
    def dashboard(self) -> str:
        out = self.render_dashboard()
        _display(out)
        return out

    def module(self, module_id: str) -> str:
        out = self.render_module(module_id)
        _display(out)
        return out

    def lesson(self, lesson_id: str | None = None) -> str:
        """Open a lesson. No argument means the one you have reached."""
        if lesson_id is None:
            lesson_id = self.current or self.next_lesson_id()
        if lesson_id is None:
            out = self.render_dashboard()
            _display(out)
            return out
        out = self.render_lesson(lesson_id)
        if self.lesson_unlocked(lesson_id):
            self.current = lesson_id
        _display(out)
        return out

    def answer(self, **answers) -> str:
        """Quiz the lesson you are on, using keyword answers: answer(q1="b")."""
        lesson_id = self.current or self.next_lesson_id()
        if not lesson_id:
            out = '<div class="pc-bad">Every lesson is passed - take the module exams.</div>'
            _display(out)
            return out
        return self.quiz(lesson_id, answers)

    def _current_module(self) -> str | None:
        lesson_id = self.current or self.next_lesson_id()
        if lesson_id:
            return self._module_of_lesson.get(lesson_id)
        return self.modules[-1]["id"] if self.modules else None

    def exam_current(self, **answers) -> str:
        module_id = self._current_module()
        if not module_id:
            out = '<div class="pc-bad">No module to examine.</div>'
            _display(out)
            return out
        return self.exam(module_id, answers)

    def skip_current(self, **answers) -> str:
        module_id = self._current_module()
        if not module_id:
            out = '<div class="pc-bad">No module to skip.</div>'
            _display(out)
            return out
        return self.skip_exam(module_id, answers)

    def check_current(self, code: str, n: int = 1) -> str:
        lesson_id = self.current or self.next_lesson_id()
        if not lesson_id:
            out = '<div class="pc-bad">Open a lesson first: show()</div>'
            _display(out)
            return out
        return self.check("%se%d" % (lesson_id, n), code)

    def quiz(self, lesson_id: str, answers) -> str:
        lesson = self._lesson(lesson_id)
        if not lesson:
            out = f'<div class="pc-bad">Unknown lesson: {_e(lesson_id)}</div>'
            _display(out)
            return out
        if not self.lesson_unlocked(lesson_id):
            out = (
                f'<div class="pc-wrap"><div class="pc-lock">🔒 {_e(self.t(lesson["title"]))} '
                f"is still locked - pass the previous lesson first.</div></div>"
            )
            _display(out)
            return out
        items = lesson.get("quiz", [])
        score, detail, _ = self._score(items, answers)
        passed = score >= LESSON_PASS
        rec = self.state["lessons"].setdefault(
            lesson_id, {"best_score": 0.0, "attempts": 0, "passed": False}
        )
        rec["attempts"] = int(rec.get("attempts", 0)) + 1
        rec["last_score"] = round(score, 3)
        rec["best_score"] = max(float(rec.get("best_score", 0.0)), score)
        rec["last_answers"] = self._normalise(answers, items)
        if passed:
            rec["passed"] = True
            rec.setdefault("passed_at", _now())
        self._record_missed(detail)
        self._log("lesson", lesson_id, score, passed)
        self._save()
        hint = ""
        if passed:
            nxt = self.next_lesson_id()
            hint = (
                f'Next up: <b>{_e(self.t(self.by_lesson[nxt]["title"]))}</b> - '
                f'<code>course.lesson("{_e(nxt)}")</code>'
                if nxt
                else "That was the last lesson. Take the module exams to finish."
            )
        out = self._feedback(f"Quiz · {self.t(lesson['title'])}", score, LESSON_PASS,
                             detail, passed, hint)
        _display(out)
        return out

    def exam(self, module_id: str, answers) -> str:
        return self._module_gate(module_id, answers, skip=False)

    def skip_exam(self, module_id: str, answers) -> str:
        return self._module_gate(module_id, answers, skip=True)

    def _module_gate(self, module_id: str, answers, skip: bool) -> str:
        module = self.by_module.get(module_id)
        if not module:
            out = f'<div class="pc-bad">Unknown module: {_e(module_id)}</div>'
            _display(out)
            return out
        if not self.module_unlocked(module_id):
            out = (
                f'<div class="pc-wrap"><div class="pc-lock">🔒 Module {_e(module_id)} is locked. '
                f"Pass the previous module exam first.</div></div>"
            )
            _display(out)
            return out
        full = self._full(module_id)
        if not skip:
            pending = [
                ls for chapter in full["chapters"] for ls in chapter["lessons"]
                if not self.lesson_passed(ls["id"])
            ]
            if pending:
                # No jumping: the exam opens only after every lesson is passed.
                # A learner who already knows the module takes the skip exam.
                out = (
                    f'<div class="pc-wrap"><div class="pc-lock">🔒 The exam for '
                    f'<b>{_e(self.t(module["title"]))}</b> opens after every lesson in the '
                    f"module is passed ({len(pending)} left).<br>Already know this module? "
                    f"Take the skip exam instead: <code>skip(...)</code> at "
                    f"{_pct(SKIP_PASS)}.</div></div>"
                )
                _display(out)
                return out
        items = full.get("skip_exam" if skip else "exam", [])
        need = SKIP_PASS if skip else EXAM_PASS
        score, detail, _ = self._score(items, answers)
        passed = score >= need
        rec = self.state["modules"].setdefault(module_id, {})
        key = "skip" if skip else "exam"
        rec[key + "_attempts"] = int(rec.get(key + "_attempts", 0)) + 1
        rec[key + "_best"] = max(float(rec.get(key + "_best", 0.0)), score)
        if passed:
            rec[key + "_passed"] = True
            if skip:
                rec["skipped"] = True
                # a passed skip exam means the content is known: mark lessons passed
                for chapter in module["chapters"]:
                    for lesson in chapter["lessons"]:
                        lrec = self.state["lessons"].setdefault(
                            lesson["id"], {"best_score": 0.0, "attempts": 0, "passed": False}
                        )
                        lrec["passed"] = True
                        lrec["via_skip"] = True
            else:
                rec["exam_passed"] = True
            rec.setdefault(key + "_passed_at", _now())
        self._record_missed(detail)
        self._log(key, module_id, score, passed)
        self._save()
        title = ("Skip exam · " if skip else "Module exam · ") + self.t(module["title"])
        hint = ""
        if passed:
            ids = [m["id"] for m in self.modules]
            i = ids.index(module_id)
            hint = (
                f'Module <code>{_e(ids[i + 1])}</code> is now unlocked.'
                if i + 1 < len(ids)
                else "That was the final module. You finished the course."
            )
        out = self._feedback(title, score, need, detail, passed, hint)
        _display(out)
        return out

    def check(self, exercise_id: str, code: str) -> str:
        """Run a learner's code and then the exercise's assertions."""
        ex = self._exercise(exercise_id)
        if not ex:
            out = f'<div class="pc-bad">Unknown exercise: {_e(exercise_id)}</div>'
            _display(out)
            return out
        namespace: dict = {"__name__": "__learner__"}
        import contextlib
        import io
        import types

        # Register the namespace as a module so dataclasses (and similar tools that
        # resolve string annotations) can look it up by name, exactly as __main__
        # works in a normal notebook session.
        learner_module = types.ModuleType("__learner__")
        learner_module.__dict__.update(namespace)
        sys.modules["__learner__"] = learner_module
        namespace = learner_module.__dict__

        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                exec(compile(code, "<your code>", "exec", dont_inherit=True), namespace)  # noqa: S102 - learner's own code
        except Exception:
            tb = traceback.format_exc(limit=4)
            out = (
                f'<div class="pc-wrap"><div class="pc-card"><p class="pc-bad">'
                f"Your code raised an error</p>"
                f'<div class="pc-code">{_e(tb)}</div></div></div>'
            )
            _display(out)
            return out
        namespace["printed"] = buffer.getvalue()
        namespace["_raises"] = _raises
        failures = []
        for check in ex["checks"]:
            try:
                ok = bool(eval(check, {}, namespace))  # noqa: S307 - authored checks
            except Exception as exc:
                failures.append(f"{check}  →  raised {type(exc).__name__}: {exc}")
                continue
            if not ok:
                failures.append(check)
        if failures:
            out = (
                f'<div class="pc-wrap"><div class="pc-card"><p class="pc-bad">Not correct yet</p>'
                + "".join(f'<p class="pc-small"><code>{_e(f)}</code> failed</p>' for f in failures)
                + f'<p class="pc-small">Hint: {_e(self.t(ex.get("hint", {})))}</p>'
                f"</div></div>"
            )
        else:
            out = (
                f'<div class="pc-wrap"><div class="pc-card"><p class="pc-ok">All checks passed.</p>'
                f'<p class="pc-small">{len(ex["checks"])} assertion(s) green.</p></div></div>'
            )
        _display(out)
        return out

    def next(self) -> str:
        lesson_id = self.next_lesson_id()
        if not lesson_id:
            out = self.render_dashboard()
            _display(out)
            return out
        return self.lesson(lesson_id)

    def review(self) -> str:
        """Lessons that were passed but not perfectly, plus missed questions."""
        rows = []
        for lesson_id in self._order:
            rec = self.state["lessons"].get(lesson_id, {})
            if rec.get("passed") and float(rec.get("best_score", 1.0)) < 1.0:
                rows.append(
                    f'<div class="pc-row"><span>{_e(self.t(self.by_lesson[lesson_id]["title"]))}</span>'
                    f'<span class="pc-small">{_pct(rec["best_score"])}</span></div>'
                )
        missed = self.state.get("missed", {})
        if not rows and not missed:
            body = '<p class="pc-ok">Nothing to review yet.</p>'
        else:
            body = "".join(rows)
            if missed:
                body += f'<p class="pc-p">{len(missed)} question(s) answered wrong at some point.</p>'
                for qid, rec in list(missed.items())[:15]:
                    body += (
                        f'<p class="pc-small">· {_e(rec.get("question", qid))} '
                        f'(missed {rec.get("times", 1)}×)</p>'
                    )
        out = (
            f'<div class="pc-wrap"><div class="pc-card"><p class="pc-title">Review queue</p>'
            f'<p class="pc-sub">Re-run a quiz to push its score to 100%.</p>{body}</div></div>'
        )
        _display(out)
        return out

    def progress(self) -> dict:
        done = [ls["id"] for ls in self.lessons if self.lesson_passed(ls["id"])]
        print("Language:", self.state["language"])
        print("Lessons passed: %d/%d" % (len(done), len(self.lessons)))
        print("Modules passed: %d/%d" % (
            sum(1 for m in self.modules if self.module_passed(m["id"])), len(self.modules)))
        print("Progress file:", self.path)
        return {"lessons": done, "language": self.state["language"], "path": str(self.path)}

    def export_progress(self) -> str:
        return json.dumps(self.state, indent=2, ensure_ascii=False)

    def import_progress(self, text: str) -> None:
        state = json.loads(text)
        if not isinstance(state, dict) or "lessons" not in state:
            raise ValueError("that does not look like a progress export")
        self.state = state
        self._save()
        print("Progress imported.")

    def reset(self, confirm: bool = False) -> None:
        if not confirm:
            print('This deletes all saved progress. Run course.reset(confirm=True) to do it.')
            return
        self.state = self._blank_state(self.state.get("language", "hinglish"))
        self._save()
        print("Progress reset.")

    def help(self) -> str:
        out = (
            f'<div class="pc-wrap"><div class="pc-card"><p class="pc-title">How to use this notebook</p>'
            f'<div class="pc-code">show()                 # the lesson you have reached\n'
            f'answer(q1="a", q2="b")  # answer its quiz ({_pct(LESSON_PASS)} to pass)\n'
            f'check("""your code""")  # test exercise 1 of that lesson\n'
            f'exam(q1="a", q2="b")    # module exam, after every lesson in it\n'
            f'skip(q1="a", q2="b")    # already know it? {_pct(SKIP_PASS)} to skip\n'
            f'dashboard()            # where am I?\n'
            f'progress()             # plain summary\n'
            f'review()               # what to revisit\n'
            f'language("hi")         # en / hi / hinglish\n'
            f'guide()                # this card\n'
            f'reset(confirm=True)    # start over</div>'
            f'<p class="pc-small">Lessons unlock in order: no lesson, chapter or module '
            f"opens before the one before it is passed. A lesson needs {_pct(LESSON_PASS)}, "
            f"a module exam {_pct(EXAM_PASS)} after all its lessons, a skip exam {_pct(SKIP_PASS)}.</p>"
            f"</div></div>"
        )
        _display(out)
        return out


# ------------------------------------------------------------------- visuals

def _figure(body: str, caption: str, width: int = 640, height: int = 220) -> str:
    return (
        f'<figure style="margin:10px 0;padding:8px;border:1px solid #e2e8f0;'
        f'border-radius:10px;background:#fbfdff;max-width:{width}px">'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" role="img" aria-label="{html.escape(caption, quote=True)}" '
        f'style="max-width:100%;height:auto">'
        f"<style>"
        f".pulse{{animation:pulse 2.4s ease-in-out infinite}}"
        f"@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}"
        f".dash{{animation:dash 2s linear infinite}}"
        f"@keyframes dash{{to{{stroke-dashoffset:-24}}}}"
        f".fade{{animation:fade 4s ease-in-out infinite}}"
        f"@keyframes fade{{0%,45%{{opacity:1}}55%,100%{{opacity:.25}}}}"
        f".slide{{animation:slide 3s ease-in-out infinite}}"
        f"@keyframes slide{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(120px)}}}}"
        f"</style>{body}</svg>"
        f'<figcaption style="font-size:12.5px;color:#334155;padding:6px 2px 0">'
        f"{html.escape(caption)}</figcaption></figure>"
    )


VISUAL_REGISTRY: dict[str, tuple[str, dict[str, str]]] = {}
