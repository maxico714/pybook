"""Read-only view of the curriculum for the web app.

The single source of truth is still ``course/`` (the authoring package).  The
builder writes ``pybook/data`` from it, and both the notebook and this web app
read those files - so a lesson is written once and appears in both products.

Nothing here touches learner progress; that lives in :mod:`web.store`.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "pybook" / "data"
LANGUAGES = ("en", "hi", "hinglish")
LANGUAGE_NAMES = {"en": "English", "hi": "हिन्दी", "hinglish": "Hinglish"}


class Catalog:
    """Lazy, read-only access to the generated curriculum files."""

    def __init__(self, data_dir=None):
        self.data_dir = pathlib.Path(data_dir) if data_dir else DATA
        index_path = self.data_dir / "index.json"
        if not index_path.is_file():
            raise FileNotFoundError(
                "Curriculum data is missing (%s). Run `python build_notebook.py` first."
                % index_path
            )
        self.index = json.loads(index_path.read_text(encoding="utf-8"))
        self.modules: list[dict] = self.index["modules"]
        self.by_module = {module["id"]: module for module in self.modules}
        self.chapters = {
            chapter["id"]: chapter for module in self.modules for chapter in module["chapters"]
        }
        self.lessons = [
            lesson
            for module in self.modules
            for chapter in module["chapters"]
            for lesson in chapter["lessons"]
        ]
        self.by_lesson = {lesson["id"]: lesson for lesson in self.lessons}
        self.module_of_lesson = {
            lesson["id"]: module["id"]
            for module in self.modules
            for chapter in module["chapters"]
            for lesson in chapter["lessons"]
        }
        self.chapter_of_lesson = {
            lesson["id"]: chapter["id"]
            for module in self.modules
            for chapter in module["chapters"]
            for lesson in chapter["lessons"]
        }
        self.lesson_order = [lesson["id"] for lesson in self.lessons]
        self._modules: dict[str, dict] = {}
        self._visuals = None

    # ------------------------------------------------------------------ content
    def full(self, module_id: str) -> dict:
        if module_id not in self._modules:
            path = self.data_dir / ("%s.json" % module_id)
            self._modules[module_id] = json.loads(path.read_text(encoding="utf-8"))
        return self._modules[module_id]

    def lesson(self, lesson_id: str):
        module_id = self.module_of_lesson.get(lesson_id)
        if not module_id:
            return None
        for chapter in self.full(module_id)["chapters"]:
            for lesson in chapter["lessons"]:
                if lesson["id"] == lesson_id:
                    return lesson
        return None

    def module_lessons(self, module_id: str) -> list[dict]:
        return [lesson for chapter in self.full(module_id)["chapters"] for lesson in chapter["lessons"]]

    def visuals(self) -> dict:
        if self._visuals is None:
            path = self.data_dir / "visuals.json"
            self._visuals = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        return self._visuals

    def visual(self, name: str):
        return self.visuals().get(name)

    # ------------------------------------------------------------------ language
    @staticmethod
    def t(field, language: str = "hinglish") -> str:
        """Pick a translation with a documented fallback chain."""
        if field is None:
            return ""
        if isinstance(field, str):
            return field
        return (
            field.get(language)
            or field.get("hinglish")
            or field.get("en")
            or next(iter(field.values()), "")
        )

    def title(self, module_or_lesson: dict, language: str) -> str:
        return self.t(module_or_lesson.get("title"), language)
