"""Child process that runs one piece of learner code, then exits.

It is started by :mod:`web.runner` as

    python -I _worker.py <payload.json> <result.json>

and it must never write to stdout, because the parent reads only the result
file.  Learner code runs with restricted builtins, an import allow-list and
``Path.open`` confined to the run folder plus the OS temp folder.  This is a
teaching sandbox, not a security boundary, and the README says so.
"""
from __future__ import annotations

import builtins as _builtins
import io
import json
import pathlib
import sys
import traceback
import types

ALLOWED_MODULES = {
    "math", "random", "statistics", "datetime", "json", "collections", "itertools",
    "functools", "string", "re", "decimal", "fractions", "textwrap", "csv", "io",
    "dataclasses", "typing", "unittest", "asyncio", "time", "enum", "heapq",
    "bisect", "copy", "operator", "pprint", "numbers", "secrets", "uuid",
    "pathlib", "tempfile", "hashlib",
}

BLOCKED_NAMES = {
    "open", "eval", "exec", "compile", "input", "breakpoint", "globals", "locals",
    "vars", "memoryview", "help", "exit", "quit", "setattr", "delattr",
}

MAX_STEPS = 200
MAX_VARS = 12
MAX_REPR = 120
MAX_OUTPUT = 8000


def _raises(func, *args, exc: type = Exception, **kwargs) -> bool:
    """Same helper the notebook exposes, so exercises behave identically."""
    try:
        func(*args, **kwargs)
    except exc:
        return True
    except Exception:
        return False
    return False


def _import(name, globals=None, locals=None, fromlist=(), level=0):
    root = name.split(".")[0]
    if root not in ALLOWED_MODULES:
        raise ImportError(
            "%r is not available in the practice sandbox. Allowed: %s"
            % (name, ", ".join(sorted(ALLOWED_MODULES)))
        )
    return _builtins.__import__(name, globals, locals, fromlist, level)


def _builtin_table(print_func) -> dict:
    table = {}
    for name in dir(_builtins):
        if name.startswith("_") or name in BLOCKED_NAMES:
            continue
        table[name] = getattr(_builtins, name)
    table["print"] = print_func
    table["__import__"] = _import
    # `class` statements are a core lesson (custom exceptions), and CPython needs
    # this hook to build a class at all.  It is a language primitive, not an escape.
    table["__build_class__"] = _builtins.__build_class__
    return table


def _confine_file_access() -> None:
    """Let ``Path.open`` touch only this run's folder or the OS temp folder.

    Module 7 teaches files, so ``pathlib``/``tempfile`` are importable.  That would
    otherwise let learner code read any file on the machine; this keeps the lesson
    runnable while the blast radius stays a scratch directory.
    """
    import pathlib as _pathlib
    import tempfile as _tempfile

    original = _pathlib.Path.open

    def open_(self, *args, **kwargs):
        target = self.resolve()
        roots = (
            _pathlib.Path.cwd().resolve(),
            _pathlib.Path(_tempfile.gettempdir()).resolve(),
        )
        for root in roots:
            if target == root or root in target.parents:
                return original(self, *args, **kwargs)
        raise PermissionError(
            "File access is limited to this run's folder and the temp folder."
        )

    _pathlib.Path.open = open_


def _snapshot(frame) -> dict:
    values = {}
    for name, value in list(frame.f_locals.items()):
        if name.startswith("_") or isinstance(value, types.ModuleType):
            continue
        try:
            text = repr(value)
        except Exception:  # a broken __repr__ must not break the trace
            text = "<%s>" % type(value).__name__
        values[name] = text[:MAX_REPR]
        if len(values) >= MAX_VARS:
            break
    return values


def _trace_hook(steps: list, counter: dict) -> object:
    def local(frame, event, arg):
        if frame.f_code.co_filename != "<learner>":
            return None
        if event == "line":
            if len(steps) >= MAX_STEPS:
                return None
            steps.append(
                {"line": frame.f_lineno, "vars": _snapshot(frame), "out": counter["n"]}
            )
        return local

    def global_hook(frame, event, arg):
        if frame.f_code.co_filename != "<learner>":
            return None
        return local

    return global_hook


def run(payload: dict) -> dict:
    code = payload.get("code") or ""
    checks = payload.get("checks") or []
    trace = bool(payload.get("trace"))
    result = {
        "ok": True,
        "stdout": "",
        "error": None,
        "error_line": None,
        "checks": [],
        "steps": [],
    }

    chunks: list[str] = []
    size = 0
    counter = {"n": 0}

    def collect(*args, sep=" ", end="\n", **kwargs):
        nonlocal size
        if size >= MAX_OUTPUT:
            return
        text = sep.join(str(arg) for arg in args) + end
        size += len(text)
        counter["n"] += len(text)
        chunks.append(text)

    namespace: dict = {"__name__": "__learner__"}
    namespace["__builtins__"] = _builtin_table(collect)
    namespace["_raises"] = _raises

    # Register the namespace as a module so dataclasses and string annotations
    # resolve exactly as they do in a notebook cell.
    module = types.ModuleType("__learner__")
    module.__dict__.update(namespace)
    sys.modules["__learner__"] = module
    namespace = module.__dict__

    steps: list = []
    if trace:
        sys.settrace(_trace_hook(steps, counter))
    _confine_file_access()
    try:
        exec(compile(code, "<learner>", "exec", dont_inherit=True), namespace)  # noqa: S102
    except SyntaxError as exc:
        result["ok"] = False
        result["error"] = "%s: %s" % (type(exc).__name__, exc.msg)
        result["error_line"] = exc.lineno
    except BaseException as exc:  # noqa: BLE001 - the learner's error is the payload
        result["ok"] = False
        result["error"] = "%s: %s" % (type(exc).__name__, exc)
        tb = traceback.extract_tb(exc.__traceback__)
        for frame in reversed(tb):
            if frame.filename == "<learner>":
                result["error_line"] = frame.lineno
                break
    finally:
        sys.settrace(None)

    printed = "".join(chunks)
    result["stdout"] = printed[:MAX_OUTPUT]
    if size >= MAX_OUTPUT:
        result["stdout"] += "\n… output truncated"
    result["steps"] = steps

    namespace["printed"] = printed
    namespace["_raises"] = _raises
    for number, check in enumerate(checks, 1):
        entry = {"n": number, "ok": False, "error": None}
        try:
            entry["ok"] = bool(eval(check, {}, namespace))  # noqa: S307 - authored checks
        except Exception as exc:
            entry["error"] = "%s: %s" % (type(exc).__name__, exc)
        result["checks"].append(entry)

    return result


def main(argv: list[str]) -> int:
    payload_path = pathlib.Path(argv[1])
    result_path = pathlib.Path(argv[2])
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
        result = run(payload)
    except Exception:  # pragma: no cover - a broken worker must still answer
        result = {
            "ok": False,
            "stdout": "",
            "error": "sandbox failed: " + traceback.format_exc(limit=2),
            "error_line": None,
            "checks": [],
            "steps": [],
        }
    result_path.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
