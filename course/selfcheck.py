"""Self-check: run the curriculum's own examples and exercises.

The course promises that every code example is executed and that the output
printed under it is the real output.  This module is how that promise is kept:

    python -m course.selfcheck            # every module
    python -m course.selfcheck m05 m06    # just these

It is used by the test suite and by the notebook builder, so a broken example
cannot ship.
"""
from __future__ import annotations

import contextlib
import io
import sys
import traceback
import types

from pybook.core import _raises


def run_code(code: str) -> tuple[str, dict, BaseException | None]:
    """Execute ``code`` and return (stdout, namespace, exception or None)."""
    # A real module entry in sys.modules matters: dataclasses (and anything else
    # that resolves string annotations) looks the defining module up by name.
    # In a notebook that module is __main__; here it is this throwaway one.
    module = types.ModuleType("__selfcheck__")
    namespace: dict = module.__dict__
    namespace["__name__"] = "__selfcheck__"
    namespace["_raises"] = _raises
    sys.modules["__selfcheck__"] = module
    buffer = io.StringIO()
    error: BaseException | None = None
    try:
        with contextlib.redirect_stdout(buffer):
            exec(compile(code, "<example>", "exec", dont_inherit=True), namespace)
    except BaseException as exc:  # noqa: BLE001 - we report it, we do not hide it
        error = exc
    finally:
        sys.modules.pop("__selfcheck__", None)
    return buffer.getvalue(), namespace, error


def check_lesson(lesson: dict) -> list[str]:
    problems: list[str] = []
    lid = lesson["id"]

    for n, example in enumerate(lesson.get("examples", []), 1):
        where = f"{lid}.example{n}"
        stdout, _namespace, error = run_code(example["code"])
        if error is not None:
            note = (example.get("note") or {}).get("en", "")
            if type(error).__name__ not in note:
                problems.append(
                    f"{where}: raised {type(error).__name__}: {error} "
                    f"(and the note does not mention it)"
                )
        expected = example.get("output", "").strip("\n")
        actual = stdout.strip("\n")
        if actual != expected:
            problems.append(
                f"{where}: output mismatch\n    expected: {expected!r}\n    actual:   {actual!r}"
            )

    for n, exercise in enumerate(lesson.get("exercises", []), 1):
        where = f"{lid}.exercise{n}"
        stdout, namespace, error = run_code(exercise["solution"])
        if error is not None:
            problems.append(f"{where}: the solution raised {type(error).__name__}: {error}")
            continue
        namespace["printed"] = stdout
        namespace["_raises"] = _raises
        for check in exercise["checks"]:
            try:
                ok = bool(eval(check, {}, namespace))  # noqa: S307 - authored checks
            except Exception as exc:  # noqa: BLE001
                problems.append(
                    f"{where}: check {check!r} raised {type(exc).__name__}: {exc}"
                )
                continue
            if not ok:
                problems.append(f"{where}: check failed for the solution: {check}")

    problems.extend(check_items(lesson.get("quiz", []), lid))
    return problems


def check_items(items: list[dict], where: str) -> list[str]:
    problems: list[str] = []
    for n, item in enumerate(items, 1):
        label = f"{where}.q{n}"
        options = item.get("options", [])
        if len(options) != 4:
            problems.append(f"{label}: {len(options)} options (expected 4)")
        if len({str(o).strip() for o in options}) != len(options):
            problems.append(f"{label}: duplicate options")
        if item.get("answer") not in ("a", "b", "c", "d"):
            problems.append(f"{label}: answer {item.get('answer')!r} is not a/b/c/d")
        if not item.get("question", {}).get("en"):
            problems.append(f"{label}: no English question")
        if not item.get("why", {}).get("en"):
            problems.append(f"{label}: no English explanation")
    return problems


def check_module(module: dict) -> list[str]:
    problems: list[str] = []
    for chapter in module["chapters"]:
        for lesson in chapter["lessons"]:
            problems.extend(check_lesson(lesson))
    problems.extend(check_items(module.get("exam", []), f"{module['id']}.exam"))
    return problems


def _load(names: list[str]):
    import importlib

    modules = []
    for name in names:
        mod = importlib.import_module(f".content.{name}", package="course")
        modules.append(mod.MODULE.to_dict())
    return modules


def main(argv: list[str]) -> int:
    names = argv[1:] or ["m%02d" % i for i in range(1, 13)]
    failures = 0
    for module in _load(names):
        problems = check_module(module)
        lessons = sum(len(c["lessons"]) for c in module["chapters"])
        examples = sum(
            len(ls["examples"]) for c in module["chapters"] for ls in c["lessons"]
        )
        if problems:
            failures += 1
            print(f"[FAIL] {module['id']}: {len(problems)} problem(s)")
            for problem in problems:
                print("   -", problem)
        else:
            print(
                f"[ ok ] {module['id']}: {lessons} lessons, {examples} examples, "
                f"{len(module['exam'])} exam items"
            )
    if failures:
        print(f"\n{failures} module(s) failed")
        return 1
    print("\nall checked modules are clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
