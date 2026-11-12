"""Gating, scoring and unlocking rules for the web platform.

The rules are deliberately the same as the notebook's, because a learner who
switches between the two must not get a different answer to "can I open this?":

* lesson 1 of the course is open; every other lesson opens only when the lesson
  before it is **passed** (80%);
* a chapter is open when its first lesson is open;
* module 1 is open; every other module opens only when the previous module is
  **passed**, by its exam (80%) or by its skip exam (90%);
* the module exam opens only after **every lesson in that module** is passed -
  the skip exam is the only shortcut, and it needs 90%.

Nothing in this module renders HTML.  It answers questions and records results,
which keeps it testable without a browser.
"""
from __future__ import annotations

import re

from . import drills as drill_lib

LESSON_PASS = 0.8
EXAM_PASS = 0.8
SKIP_PASS = 0.9

_ANSWER_KEYS = re.compile(r"^q(\d+)$")


def _ratio(correct: int, total: int) -> float:
    return (correct / total) if total else 0.0


def _reached(score: float, threshold: float) -> bool:
    """Compare scores with a tolerance so 4/5 is exactly 80%."""
    return score + 1e-9 >= threshold


class Progress:
    """One learner's view of the course: what is open, and what they scored."""

    def __init__(self, catalog, store, learner):
        self.catalog = catalog
        self.store = store
        self.learner = learner
        self.learner_id = learner["id"]
        self.language = learner.get("language", "hinglish")
        self._lessons = None
        self._modules = None
        self._practice = None

    # ------------------------------------------------------------------ records
    @property
    def lessons(self) -> dict[str, dict]:
        if self._lessons is None:
            self._lessons = self.store.lessons(self.learner_id)
        return self._lessons

    @property
    def modules(self) -> dict[str, dict]:
        if self._modules is None:
            self._modules = self.store.modules(self.learner_id)
        return self._modules

    @property
    def practice(self) -> dict[str, dict]:
        if self._practice is None:
            self._practice = self.store.practice(self.learner_id)
        return self._practice

    def _refresh(self) -> None:
        self._lessons = None
        self._modules = None
        self._practice = None

    def lesson_passed(self, lesson_id: str) -> bool:
        return bool(self.lessons.get(lesson_id, {}).get("passed"))

    def lesson_score(self, lesson_id: str) -> float:
        return float(self.lessons.get(lesson_id, {}).get("best", 0.0))

    def module_passed(self, module_id: str) -> bool:
        row = self.modules.get(module_id, {})
        return bool(row.get("exam_passed") or row.get("skip_passed"))

    def module_score(self, module_id: str) -> float:
        row = self.modules.get(module_id, {})
        return max(float(row.get("exam_best", 0.0)), float(row.get("skip_best", 0.0)))

    # ----------------------------------------------------------------- practice
    @staticmethod
    def exercise_id(lesson_id: str, index: int) -> str:
        return "%s:ex:%d" % (lesson_id, index)

    def exercise_passed(self, lesson_id: str, index: int) -> bool:
        row = self.practice.get(self.exercise_id(lesson_id, index), {})
        return bool(row.get("passed"))

    def practice_ready(self, lesson_id: str) -> bool:
        """True when every *required* exercise of the lesson is solved."""
        body = self.catalog.lesson(lesson_id) or {}
        exercises = body.get("exercises") or []
        return all(self.exercise_passed(lesson_id, index) for index in range(len(exercises)))

    def practice_progress(self, lesson_id: str) -> tuple[int, int]:
        body = self.catalog.lesson(lesson_id) or {}
        total = len(body.get("exercises") or [])
        done = sum(1 for index in range(total) if self.exercise_passed(lesson_id, index))
        return done, total

    def drill_passed(self, drill_id: str) -> bool:
        return bool(self.practice.get(drill_id, {}).get("passed"))

    def record_practice(self, lesson_id: str, drill_id: str, kind: str, passed: bool) -> None:
        self.store.record_practice(self.learner_id, drill_id, lesson_id, kind, passed)
        self._practice = None

    def optional_drills(self, lesson_id: str) -> list[dict]:
        """The optional drills for a lesson, with this learner's pass state."""
        body = self.catalog.lesson(lesson_id) or {}
        return [
            dict(drill, passed=self.drill_passed(drill["id"]))
            for drill in drill_lib.build(lesson_id, body)
        ]

    def xp(self) -> int:
        lessons = sum(1 for lesson_id in self.catalog.lesson_order if self.lesson_passed(lesson_id))
        modules = sum(1 for module in self.catalog.modules if self.module_passed(module["id"]))
        exercises = sum(
            1
            for row in self.practice.values()
            if row.get("passed") and row.get("kind") == "code"
        )
        drills = sum(
            1
            for row in self.practice.values()
            if row.get("passed") and row.get("kind") != "code"
        )
        return (
            lessons * drill_lib.XP_LESSON
            + modules * drill_lib.XP_MODULE
            + exercises * drill_lib.XP_EXERCISE
            + drills * drill_lib.XP_DRILL
        )

    # -------------------------------------------------------------------- locks
    def lesson_unlocked(self, lesson_id: str) -> bool:
        order = self.catalog.lesson_order
        if lesson_id not in self.catalog.by_lesson:
            return False
        index = order.index(lesson_id)
        if index == 0:
            return True
        return self.lesson_passed(order[index - 1])

    def chapter_unlocked(self, chapter_id: str) -> bool:
        chapter = self.catalog.chapters.get(chapter_id)
        if not chapter or not chapter["lessons"]:
            return False
        return self.lesson_unlocked(chapter["lessons"][0]["id"])

    def module_unlocked(self, module_id: str) -> bool:
        ids = [module["id"] for module in self.catalog.modules]
        if module_id not in ids:
            return False
        index = ids.index(module_id)
        if index == 0:
            return True
        return self.module_passed(ids[index - 1])

    def module_lessons_passed(self, module_id: str) -> bool:
        return all(
            self.lesson_passed(lesson["id"])
            for lesson in self.catalog.module_lessons(module_id)
        )

    def exam_unlocked(self, module_id: str) -> bool:
        """The real exam: module open *and* every lesson in it passed."""
        return self.module_unlocked(module_id) and self.module_lessons_passed(module_id)

    def skip_unlocked(self, module_id: str) -> bool:
        return self.module_unlocked(module_id)

    def next_lesson(self):
        """The first lesson that is open and not yet passed."""
        for lesson_id in self.catalog.lesson_order:
            if self.lesson_unlocked(lesson_id) and not self.lesson_passed(lesson_id):
                return lesson_id
        return None

    # ------------------------------------------------------------------ scoring
    @staticmethod
    def _answer_map(answers) -> dict[str, str]:
        """Accept ``{"q1": "b"}`` and ``{"m01c01l01q1": "b"}`` alike."""
        if not isinstance(answers, dict):
            return {}
        return {str(key): str(value).strip().lower()[:1] for key, value in answers.items()}

    def score(self, items: list[dict], answers) -> tuple[float, int, list[dict]]:
        """Return ``(ratio, correct, detail)``; detail explains every miss."""
        given = self._answer_map(answers)
        detail: list[dict] = []
        correct = 0
        for number, item in enumerate(items, 1):
            key = "q%d" % number
            picked = given.get(key) or given.get(item["id"], "")
            expected = str(item["answer"]).strip().lower()
            if picked == expected:
                correct += 1
                continue
            detail.append(
                {
                    "id": item["id"],
                    "number": number,
                    "question": self.catalog.t(item["question"], self.language),
                    "given": picked,
                    "answer": expected,
                    "why": self.catalog.t(item.get("why"), self.language),
                }
            )
        return _ratio(correct, len(items)), correct, detail

    # ------------------------------------------------------------------- submit
    def submit_quiz(self, lesson_id: str, answers) -> dict:
        """Mark a lesson quiz. Returns a JSON-safe result for the browser."""
        lesson = self.catalog.lesson(lesson_id)
        if not lesson:
            return {"ok": False, "error": "unknown lesson"}
        if not self.lesson_unlocked(lesson_id):
            return {"ok": False, "error": "locked", "message": "This lesson is still locked."}
        if not self.practice_ready(lesson_id):
            done, total = self.practice_progress(lesson_id)
            return {
                "ok": False,
                "error": "practice",
                "message": "Finish the required practice first (%d of %d solved)." % (done, total),
                "remaining": total - done,
            }

        ratio, correct, detail = self.score(lesson["quiz"], answers)
        passed = _reached(ratio, LESSON_PASS)
        self.store.record_lesson(self.learner_id, lesson_id, ratio, passed, detail)
        self._refresh()

        return {
            "ok": True,
            "score": ratio,
            "percent": round(ratio * 100),
            "correct": correct,
            "total": len(lesson["quiz"]),
            "passed": passed,
            "needed": LESSON_PASS,
            "detail": detail,
            "next": self.next_lesson(),
            "unlocked": [
                other["id"]
                for other in self.catalog.lessons
                if self.lesson_unlocked(other["id"]) and not self.lesson_passed(other["id"])
            ],
        }

    def submit_exam(self, module_id: str, answers, skip: bool = False) -> dict:
        """Mark the module exam (or the 90% skip exam)."""
        module = self.catalog.by_module.get(module_id)
        if not module:
            return {"ok": False, "error": "unknown module"}

        threshold = SKIP_PASS if skip else EXAM_PASS
        if not self.module_unlocked(module_id):
            return {
                "ok": False,
                "error": "locked",
                "message": "Pass the previous module first.",
            }
        if not skip and not self.module_lessons_passed(module_id):
            remaining = [
                lesson
                for lesson in self.catalog.module_lessons(module_id)
                if not self.lesson_passed(lesson["id"])
            ]
            return {
                "ok": False,
                "error": "lessons",
                "message": "Pass all %d lessons in this module first (%d left), or take the skip exam."
                % (len(self.catalog.module_lessons(module_id)), len(remaining)),
                "remaining": [lesson["id"] for lesson in remaining],
            }

        items = self.catalog.full(module_id).get("skip_exam" if skip else "exam", [])
        ratio, correct, detail = self.score(items, answers)
        passed = _reached(ratio, threshold)
        self.store.record_module(self.learner_id, module_id, "skip" if skip else "exam", ratio, passed)
        if passed and skip:
            # Skipping a module means knowing its lessons: mark them passed so the
            # next module's gate and the dashboard tell the truth.
            self.store.mark_lessons_passed(
                self.learner_id,
                [lesson["id"] for lesson in self.catalog.module_lessons(module_id)],
            )
        self._refresh()

        return {
            "ok": True,
            "skip": skip,
            "score": ratio,
            "percent": round(ratio * 100),
            "correct": correct,
            "total": len(items),
            "passed": passed,
            "needed": threshold,
            "detail": detail,
            "next_module": self._next_module(module_id) if passed else None,
        }

    def _next_module(self, module_id: str):
        ids = [module["id"] for module in self.catalog.modules]
        index = ids.index(module_id)
        return ids[index + 1] if index + 1 < len(ids) else None

    # ------------------------------------------------------------------ summary
    def board(self) -> list[dict]:
        """The whole course with its lock/pass state, ready to render."""
        modules = []
        for module in self.catalog.modules:
            chapters = []
            for chapter in module["chapters"]:
                chapters.append(
                    {
                        "id": chapter["id"],
                        "title": self.catalog.t(chapter["title"], self.language),
                        "unlocked": self.chapter_unlocked(chapter["id"]),
                        "lessons": [
                            {
                                "id": lesson["id"],
                                "title": self.catalog.t(lesson["title"], self.language),
                                "unlocked": self.lesson_unlocked(lesson["id"]),
                                "passed": self.lesson_passed(lesson["id"]),
                                "score": self.lesson_score(lesson["id"]),
                            }
                            for lesson in chapter["lessons"]
                        ],
                    }
                )
            lessons = [lesson for chapter in chapters for lesson in chapter["lessons"]]
            modules.append(
                {
                    "id": module["id"],
                    "title": self.catalog.t(module["title"], self.language),
                    "icon": module.get("icon", ""),
                    "unlocked": self.module_unlocked(module["id"]),
                    "passed": self.module_passed(module["id"]),
                    "exam_unlocked": self.exam_unlocked(module["id"]),
                    "lessons": lessons,
                    "done": sum(1 for lesson in lessons if lesson["passed"]),
                    "total": len(lessons),
                    "chapters": chapters,
                }
            )
        return modules

    def summary(self) -> dict:
        lessons = self.catalog.lessons
        done = sum(1 for lesson in lessons if self.lesson_passed(lesson["id"]))
        modules_done = sum(1 for module in self.catalog.modules if self.module_passed(module["id"]))
        current = self.next_lesson()
        return {
            "lessons_done": done,
            "lessons_total": len(lessons),
            "modules_done": modules_done,
            "modules_total": len(self.catalog.modules),
            "percent": round(100 * _ratio(done, len(lessons))),
            "xp": self.xp(),
            "next_lesson": current,
            "next_title": (
                self.catalog.t(self.catalog.by_lesson[current]["title"], self.language)
                if current
                else None
            ),
            "finished": current is None
            and all(self.module_passed(module["id"]) for module in self.catalog.modules),
        }

    def trail(self) -> list[dict]:
        """The sidebar path: one node per module, with the current one marked."""
        current_lesson = self.next_lesson()
        current_module = (
            self.catalog.module_of_lesson.get(current_lesson) if current_lesson else None
        )
        if current_module is None and self.catalog.modules:
            current_module = self.catalog.modules[-1]["id"]
        nodes = []
        for module in self.catalog.modules:
            lessons = self.catalog.module_lessons(module["id"])
            done = sum(1 for lesson in lessons if self.lesson_passed(lesson["id"]))
            nodes.append(
                {
                    "id": module["id"],
                    "title": self.catalog.t(module["title"], self.language),
                    "icon": module.get("icon", ""),
                    "done": done,
                    "total": len(lessons),
                    "percent": round(100 * _ratio(done, len(lessons))),
                    "passed": self.module_passed(module["id"]),
                    "unlocked": self.module_unlocked(module["id"]),
                    "current": module["id"] == current_module,
                }
            )
        return nodes

    def stats(self) -> dict:
        """Everything the dashboard charts need, computed from recorded attempts."""
        modules = []
        for module in self.catalog.modules:
            lessons = self.catalog.module_lessons(module["id"])
            passed = [lesson for lesson in lessons if self.lesson_passed(lesson["id"])]
            scores = [self.lesson_score(lesson["id"]) for lesson in passed]
            row = self.modules.get(module["id"], {})
            modules.append(
                {
                    "id": module["id"],
                    "title": self.catalog.t(module["title"], self.language),
                    "icon": module.get("icon", ""),
                    "done": len(passed),
                    "total": len(lessons),
                    "percent": round(100 * _ratio(len(passed), len(lessons))),
                    "avg": round(100 * _ratio(sum(scores), len(scores))) if scores else 0,
                    "exam": round(100 * float(row.get("exam_best", 0.0))),
                    "skip": round(100 * float(row.get("skip_best", 0.0))),
                    "passed": self.module_passed(module["id"]),
                    "unlocked": self.module_unlocked(module["id"]),
                    "attempts": int(row.get("exam_attempts", 0)) + int(row.get("skip_attempts", 0)),
                }
            )

        attempted = [row for row in self.lessons.values() if row.get("attempts")]
        best = [float(row.get("best", 0.0)) for row in attempted]
        attempts = sum(int(row.get("attempts", 0)) for row in self.lessons.values())
        attempts += sum(
            int(row.get("exam_attempts", 0)) + int(row.get("skip_attempts", 0))
            for row in self.modules.values()
        )

        ranked = [module for module in modules if module["done"]]
        weakest = sorted(ranked, key=lambda module: (module["avg"], module["percent"]))[:3]
        strongest = sorted(ranked, key=lambda module: (-module["avg"], -module["percent"]))[:3]

        drills_total = sum(
            len(drill_lib.build(lesson["id"], self.catalog.lesson(lesson["id"]) or {}))
            for lesson in self.catalog.lessons
        )
        drills_done = sum(
            1
            for row in self.practice.values()
            if row.get("passed") and row.get("kind") != "code"
        )
        exercises_done = sum(
            1
            for row in self.practice.values()
            if row.get("passed") and row.get("kind") == "code"
        )

        return {
            "lessons_done": sum(1 for lesson in self.catalog.lessons if self.lesson_passed(lesson["id"])),
            "lessons_total": len(self.catalog.lessons),
            "percent": round(100 * _ratio(len(attempted), len(self.catalog.lessons))),
            "avg_score": round(100 * _ratio(sum(best), len(best))) if best else 0,
            "attempts": attempts,
            "xp": self.xp(),
            "exercises_done": exercises_done,
            "drills_done": drills_done,
            "drills_total": drills_total,
            "questions_missed": sum(int(row.get("times", 0)) for row in self.missed()),
            "modules": modules,
            "activity": self.activity(14),
            "streak": self.streak(),
            "weakest": weakest,
            "strongest": strongest,
        }

    def activity(self, days: int = 14) -> list[dict]:
        """Attempts per day for the last ``days`` days, from the stored timestamps."""
        import datetime as _dt

        counts: dict[str, int] = {}
        rows = (
            list(self.lessons.values())
            + list(self.modules.values())
            + list(self.practice.values())
        )
        for row in rows:
            stamp = str(row.get("updated") or "")[:10]
            if stamp:
                counts[stamp] = counts.get(stamp, 0) + 1
        today = _dt.date.today()
        series = []
        for offset in range(days - 1, -1, -1):
            day = today - _dt.timedelta(days=offset)
            key = day.isoformat()
            series.append({"date": key, "label": day.strftime("%d %b"), "count": counts.get(key, 0)})
        return series

    def streak(self) -> int:
        """Consecutive days ending today (or yesterday) with recorded work."""
        import datetime as _dt

        days = {entry["date"] for entry in self.activity(400) if entry["count"]}
        if not days:
            return 0
        today = _dt.date.today()
        cursor = today if today.isoformat() in days else today - _dt.timedelta(days=1)
        streak = 0
        while cursor.isoformat() in days:
            streak += 1
            cursor -= _dt.timedelta(days=1)
        return streak

    def missed(self) -> list[dict]:
        return self.store.missed(self.learner_id)
