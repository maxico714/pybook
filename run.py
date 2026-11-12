"""Production-ish entry point for the PyBook web app.

    python run.py                 # serve on 127.0.0.1:5000
    python run.py --check         # verify data, database and secret before serving

If ``waitress`` is installed it is used, because Flask's built-in server is a
development server and says so.  This project is free-only and installs nothing
at runtime, so when waitress is missing the script explains the trade-off
instead of pretending the dev server is production grade.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def check() -> int:
    """Fail fast on the things that actually break a first run."""
    problems = []
    data = ROOT / "pybook" / "data"
    if not (data / "index.json").is_file():
        problems.append("curriculum data is missing: run `python build_notebook.py`")
    if not (data / "ai" / "index.json").is_file():
        problems.append("AI course data is missing: run `python -m pybook.build_ai_course`")

    instance = ROOT / "instance"
    try:
        instance.mkdir(exist_ok=True)
        probe = instance / ".write-probe"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as error:
        problems.append("instance/ is not writable: %s" % error)

    if not os.environ.get("PYBOOK_SECRET_KEY"):
        print("note: PYBOOK_SECRET_KEY is unset; a key will be generated in instance/secret_key")

    if os.environ.get("PYBOOK_SECURE_COOKIES") != "1":
        print("note: PYBOOK_SECURE_COOKIES is not 1, so the session cookie works over plain http")

    if problems:
        for problem in problems:
            print("FAIL " + problem)
        return 1

    from web.store import Store

    store = Store(os.environ.get("PYBOOK_DB") or (ROOT / "pybook.db"))
    try:
        counts = store.counts()
        has_admin = store.db.execute(
            "SELECT 1 FROM users WHERE role = 'admin' AND status = 'approved' LIMIT 1"
        ).fetchone()
    finally:
        store.close()

    if not has_admin:
        print("FAIL there is no approved admin, so nobody can approve a sign-up.")
        print('     create the first one: python -m web.manage create-admin --email you@example.com --name "You"')
        return 1

    print(
        "OK data, instance/, database and an admin account (%d accounts, %d waiting)"
        % (counts["total"], counts["pending"])
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the PyBook web platform.")
    parser.add_argument("--check", action="store_true", help="verify the setup and exit")
    # Render and most PaaS hosts inject PORT and expect a 0.0.0.0 bind; a local
    # run keeps the safe loopback default.
    platform_port = os.environ.get("PORT")
    default_host = os.environ.get("PYBOOK_HOST") or ("0.0.0.0" if platform_port else "127.0.0.1")
    default_port = int(platform_port or os.environ.get("PYBOOK_PORT", "5000"))
    parser.add_argument("--host", default=default_host)
    parser.add_argument("--port", type=int, default=default_port)
    args = parser.parse_args()

    if args.check:
        return check()

    from web.app import create_app

    app = create_app()
    url = "http://%s:%d" % (args.host, args.port)

    try:
        from waitress import serve
    except ImportError:
        print("WARNING: waitress is not installed, so Flask's development server is used.")
        print("         It is fine for a local classroom on your own machine, but it is")
        print("         not hardened for the public internet. For that: pip install waitress")
        print("PyBook on %s" % url)
        app.run(host=args.host, port=args.port, debug=False, threaded=True)
        return 0

    print("PyBook on %s (waitress, 8 threads)" % url)
    serve(app, host=args.host, port=args.port, threads=8, ident="PyBook")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
