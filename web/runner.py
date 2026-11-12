"""Run learner code in a throw-away child process.

Every run gets its own temporary directory, a hard timeout and a restricted
interpreter.  The child writes a JSON result file, so nothing a learner prints
can corrupt the protocol.

    run_code("print(2 + 3)")            -> {"ok": True, "stdout": "5\n", ...}
    run_code(code, checks=[...])        -> per-check pass/fail
    run_code(code, trace=True)          -> line-by-line snapshots for the player

This is a teaching sandbox, not a security boundary: it stops the accidents that
matter in a classroom (infinite loops, `open()`, surprise imports), and the
README states that plainly instead of overclaiming.
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

WORKER = pathlib.Path(__file__).resolve().parent / "_worker.py"

TIMEOUT = 5.0
MAX_CODE_CHARS = 20000

# Kept in sync with _worker.ALLOWED_MODULES by tests/test_web.py.
ALLOWED_MODULES = (
    "math", "random", "statistics", "datetime", "json", "collections", "itertools",
    "functools", "string", "re", "decimal", "fractions", "textwrap", "csv", "io",
    "dataclasses", "typing", "unittest", "asyncio", "time", "enum", "heapq",
    "bisect", "copy", "operator", "pprint", "numbers", "secrets", "uuid",
    "pathlib", "tempfile", "hashlib",
)


def _failure(message: str) -> dict:
    return {
        "ok": False,
        "stdout": "",
        "error": message,
        "error_line": None,
        "checks": [],
        "steps": [],
        "timeout": False,
    }


def run_code(code: str, checks=None, trace: bool = False, timeout: float = TIMEOUT) -> dict:
    """Execute ``code`` and return a JSON-safe result dictionary."""
    code = code or ""
    if len(code) > MAX_CODE_CHARS:
        return _failure("Code is too long (%d characters, limit %d)." % (len(code), MAX_CODE_CHARS))

    workdir = pathlib.Path(tempfile.mkdtemp(prefix="pybook_run_"))
    payload_path = workdir / "payload.json"
    result_path = workdir / "result.json"
    try:
        payload_path.write_text(
            json.dumps(
                {"code": code, "checks": list(checks or []), "trace": bool(trace)},
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        command = [sys.executable, "-I", str(WORKER), str(payload_path), str(result_path)]
        try:
            completed = subprocess.run(  # noqa: S603 - fixed command, no shell
                command,
                cwd=str(workdir),
                capture_output=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            result = _failure(
                "Your code ran for more than %.0f seconds and was stopped. "
                "Look for a loop that never ends." % timeout
            )
            result["timeout"] = True
            return result

        if not result_path.is_file():
            detail = (completed.stderr or b"").decode("utf-8", "replace").strip()
            return _failure(
                "The sandbox did not answer.%s" % (("\n" + detail[-400:]) if detail else "")
            )

        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return _failure("The sandbox returned unreadable output.")

        result.setdefault("timeout", False)
        result.setdefault("steps", [])
        result.setdefault("checks", [])
        result.setdefault("stdout", "")
        return result
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def check_exercise(code: str, checks, trace: bool = False) -> dict:
    """Run a learner's attempt at an exercise and report each assertion."""
    result = run_code(code, checks=checks, trace=trace)
    result["passed"] = bool(result["ok"]) and bool(result["checks"]) and all(
        entry["ok"] for entry in result["checks"]
    )
    return result
