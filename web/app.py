"""PyBook web: a local Flask learning platform over the same curriculum.

Run it with::

    python -m web.app          # http://127.0.0.1:5000
    python run.py              # production entry (waitress when installed)

What the routes guarantee:

* an anonymous visitor only ever sees the public homepage and the course
  syllabus - never a lesson, an exam or an API result;
* a new account is ``pending`` until an admin approves it, and a pending or
  rejected account cannot create a session even with the right password;
* a locked lesson is a 403 that renders a lock card, never its content;
* the module exam and the skip exam are separate pages, both refused
  server-side, so no amount of clicking in the browser opens them;
* quiz answers are never sent to the browser before the attempt is submitted;
* every POST is CSRF-checked and every response carries the security headers
  from :mod:`web.security`.
"""
from __future__ import annotations

import html
import os
import pathlib
import re

from flask import (
    Flask,
    abort,
    flash,
    g,
    get_flashed_messages,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from . import auth
from . import drills as drill_lib
from .admin import bp as admin_bp
from .auth import (
    admin_required,
    clear_session_cookie,
    csrf_ok,
    csrf_token,
    current_user,
    end_session,
    issue_session,
    login_required,
    set_session_cookie,
)
from .content import LANGUAGES, Catalog
from .flow import flow_svg
from .progress import EXAM_PASS, LESSON_PASS, SKIP_PASS, Progress
from .runner import ALLOWED_MODULES, check_exercise, run_code
from .security import apply_headers, load_secret_key
from .store import Store

ROOT = pathlib.Path(__file__).resolve().parents[1]

# A course is a folder with the same generated shape: index.json + m01..mNN.json.
COURSE_DIRS = (
    ROOT / "pybook" / "data",
    ROOT / "pybook" / "data" / "ai",
)


def _discover_catalogs(data_dir=None) -> dict[str, Catalog]:
    """Load every course that has been built; the Python course is the default."""
    found: dict[str, Catalog] = {}
    for path in ((pathlib.Path(data_dir),) if data_dir else COURSE_DIRS):
        if (path / "index.json").is_file():
            catalog = Catalog(path)
            found[catalog.index["id"]] = catalog
    if not found:
        raise FileNotFoundError(
            "Curriculum data is missing. Run `python build_notebook.py` first."
        )
    return found


def _strip_answers(items: list[dict], language: str, catalog: Catalog) -> list[dict]:
    """What the browser may see before an attempt: no answers, no explanations."""
    return [
        {
            "id": item["id"],
            "number": number,
            "question": catalog.t(item["question"], language),
            "options": list(item["options"]),
        }
        for number, item in enumerate(items, 1)
    ]


def _inline(text) -> str:
    """Render ``backticked`` fragments as <code>, with everything else escaped."""
    escaped = html.escape(str(text or ""), quote=False)
    return re.sub(r"`([^`\n]+)`", r"<code>\1</code>", escaped)


def _minutes_left(stamp: str) -> int:
    import datetime as _dt

    try:
        until = _dt.datetime.fromisoformat(stamp)
    except ValueError:
        return 15
    return max(1, int((until - _dt.datetime.now()).total_seconds() // 60) + 1)


def create_app(
    db_path=None, data_dir=None, testing: bool = False, secret_key: str | None = None
) -> Flask:
    app = Flask(__name__)
    app.config["TESTING"] = testing
    app.config["SECRET_KEY"] = secret_key or load_secret_key(app)
    app.config["MAX_CONTENT_LENGTH"] = 1_000_000
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["SESSION_COOKIE_SECURE"] = os.environ.get("PYBOOK_SECURE_COOKIES") == "1"
    app.config["SECURE_COOKIES"] = app.config["SESSION_COOKIE_SECURE"]
    app.config["PERMANENT_SESSION_LIFETIME"] = 60 * 60 * 24 * auth.REMEMBER_DAYS
    app.config.setdefault("SIGNUP_LIMIT", auth.SIGNUP_LIMIT)
    app.jinja_env.filters["inline"] = _inline

    catalogs = _discover_catalogs(data_dir)
    default_id = "pybook" if "pybook" in catalogs else next(iter(catalogs))
    catalog = catalogs[default_id]
    store = Store(db_path or os.environ.get("PYBOOK_DB") or (ROOT / "pybook.db"))
    store.purge_expired_sessions()
    store.purge_attempts()
    app.config["CATALOG"] = catalog
    app.config["CATALOGS"] = catalogs
    app.config["STORE"] = store

    def catalog_for(user) -> Catalog:
        return catalogs.get((user or {}).get("course"), catalog)

    def progress_for(user) -> Progress:
        return Progress(catalog_for(user), store, user)

    def course_cards() -> list[dict]:
        cards = []
        for course_id, course in catalogs.items():
            cards.append(
                {
                    "id": course_id,
                    "title": course.index.get("title"),
                    "subtitle": course.index.get("subtitle"),
                    "lessons": len(course.lessons),
                    "modules": len(course.modules),
                    "chapters": len(course.chapters),
                }
            )
        return cards

    def validate_signup(form: dict, raw) -> dict[str, str]:
        errors: dict[str, str] = {}
        if len(form.get("name", "")) < 2:
            errors["name"] = "Tell us the name to show on your dashboard."
        problem = auth.email_problem(form.get("email", ""))
        if problem:
            errors["email"] = problem
        password = raw.get("password") or ""
        confirm = raw.get("confirm") or ""
        problem = auth.password_problem(password, form.get("email", ""), form.get("name", ""))
        if problem:
            errors["password"] = problem
        elif password != confirm:
            errors["confirm"] = "The two passwords do not match."
        if form.get("course") not in catalogs:
            errors["course"] = "Choose one of the available courses."
        if not raw.get("agree"):
            errors["agree"] = "Please confirm that this device may store your name and email."
        return errors

    # -------------------------------------------------------------- lifecycle
    @app.before_request
    def load_account():
        g.user = current_user(store)
        if not csrf_ok():
            abort(400, description="Bad or missing form token. Reload the page and try again.")

    @app.after_request
    def security_headers(response):
        return apply_headers(response)

    @app.context_processor
    def inject():
        user = g.get("user")
        active = catalog_for(user)
        progress = Progress(active, store, user) if user else None
        language = (user or {}).get("language", "hinglish")
        pending = store.counts()["pending"] if (user and user.get("role") == "admin") else 0
        return {
            "catalog": active,
            "catalogs": catalogs,
            "course": active.index,
            "courses": course_cards(),
            "learner": user,
            "progress": progress,
            "summary": progress.summary() if progress else None,
            "trail": progress.trail() if progress else [],
            "nav_lessons": (
                [
                    {
                        "id": lesson["id"],
                        "title": active.t(lesson["title"], language),
                        "m": active.module_of_lesson[lesson["id"]],
                        "u": 1 if progress.lesson_unlocked(lesson["id"]) else 0,
                    }
                    for lesson in active.lessons
                ]
                if progress
                else []
            ),
            "lang": language,
            "t": lambda field: active.t(field, language),
            "csrf": csrf_token(),
            "flashes": get_flashed_messages(with_categories=True),
            "pending_count": pending,
            "lesson_pass": LESSON_PASS,
            "exam_pass": EXAM_PASS,
            "skip_pass": SKIP_PASS,
            "languages": LANGUAGES,
        }

    # ----------------------------------------------------------------- public
    @app.get("/healthz")
    def healthz():
        """Liveness for a supervisor or reverse proxy; exposes no account data."""
        try:
            store.db.execute("SELECT 1").fetchone()
        except Exception:  # a broken database is exactly what this must report
            return jsonify({"ok": False, "database": "error"}), 503
        response = jsonify({"ok": True, "database": "ok", "courses": len(catalogs)})
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.get("/favicon.ico")
    def favicon():
        return redirect(url_for("static", filename="favicon.svg"), code=308)

    @app.get("/")
    def index():
        if g.user:
            return redirect(url_for("learn"))
        return render_template(
            "home.html",
            modules=catalog.modules,
            lesson_count=len(catalog.lessons),
            chapter_count=len(catalog.chapters),
        )

    @app.get("/courses/<course_id>")
    def course_detail(course_id: str):
        found = catalogs.get(course_id)
        if not found:
            abort(404)
        return render_template("course.html", detail=found, detail_id=course_id)

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if g.user:
            return redirect(url_for("learn"))
        form = {
            "name": "",
            "email": "",
            "course": default_id,
            "goal": "",
            "language": "hinglish",
        }
        errors: dict[str, str] = {}
        if request.method == "POST":
            form.update(
                {
                    "name": auth.clean_name(request.form.get("name")),
                    "email": (request.form.get("email") or "").strip(),
                    "goal": (request.form.get("goal") or "").strip()[:500],
                    "course": request.form.get("course") or default_id,
                    "language": request.form.get("language") or "hinglish",
                }
            )
            if form["language"] not in LANGUAGES:
                form["language"] = "hinglish"
            locked = auth.signup_locked(store, request.remote_addr or "")
            if locked:
                errors = {
                    "form": "Too many new accounts from this device. "
                    "Try again in %d minutes." % _minutes_left(locked)
                }
                return (
                    render_template(
                        "signup.html", form=form, errors=errors, default_id=default_id
                    ),
                    429,
                )
            errors = validate_signup(form, request.form)
            if not errors:
                account = store.create_account(
                    form["name"],
                    form["email"],
                    auth.hash_password(request.form.get("password") or ""),
                    language=form["language"],
                    course=form["course"],
                    goal=form["goal"],
                )
                if account is None:
                    errors["email"] = "That email is already registered. Try logging in."
                else:
                    auth.note_signup(
                        store, request.remote_addr or "", app.config["SIGNUP_LIMIT"]
                    )
                    store.audit(None, "account.signup", form["email"], form["name"])
                    return render_template("pending.html", account=account), 201
        return render_template(
            "signup.html",
            form=form,
            errors=errors,
            default_id=default_id,
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if g.user:
            return redirect(url_for("learn"))
        error = None
        email = ""
        target = request.form.get("next") or request.args.get("next") or ""
        if request.method == "POST":
            email = (request.form.get("email") or "").strip()
            password = request.form.get("password") or ""
            key = auth.attempt_key(email, request.remote_addr or "")
            locked = auth.is_locked(store, key)
            if locked:
                error = "Too many attempts. Try again in %d minutes." % _minutes_left(locked)
            else:
                account = store.user_by_email(email)
                if account and auth.verify_password(account["password_hash"], password):
                    if account["status"] == "approved":
                        auth.note_success(store, key)
                        token = issue_session(store, account["id"])
                        store.audit(account["id"], "login", account.get("email") or "", "")
                        response = redirect(auth.safe_next(target, url_for("learn")))
                        set_session_cookie(response, token)
                        return response
                    if account["status"] == "pending":
                        error = "Your account is waiting for admin approval."
                    else:
                        error = "This account was not approved. Contact the admin."
                else:
                    auth.note_failure(store, key)
                    store.audit(None, "login.failed", email, request.remote_addr or "")
                    error = "Email or password is incorrect."
        return render_template("login.html", error=error, email=email, next=target)

    @app.post("/logout")
    @login_required
    def logout():
        store.audit(g.user["id"], "logout", g.user.get("email") or "", "")
        end_session(store)
        response = redirect(url_for("index"))
        clear_session_cookie(response)
        flash("You are signed out.", "ok")
        return response

    @app.get("/pending")
    def pending():
        if g.user:
            return redirect(url_for("learn"))
        return render_template("pending.html", account=None)

    # ------------------------------------------------------------------ learner
    @app.post("/switch/<course_id>")
    @login_required
    def switch_course(course_id: str):
        if course_id not in catalogs:
            abort(404)
        store.set_course(g.user["id"], course_id)
        return redirect(url_for("learn"))

    @app.get("/learn")
    @login_required
    def learn():
        progress = progress_for(g.user)
        return render_template("learn.html", board=progress.board(), state=progress.summary())

    @app.get("/lesson/<lesson_id>")
    @login_required
    def lesson(lesson_id: str):
        progress = progress_for(g.user)
        catalog = progress.catalog
        body = catalog.lesson(lesson_id)
        if not body:
            abort(404)
        if not progress.lesson_unlocked(lesson_id):
            return (
                render_template(
                    "locked.html",
                    what="lesson",
                    title=catalog.t(body["title"], progress.language),
                    previous=progress.next_lesson(),
                ),
                403,
            )

        module_id = catalog.module_of_lesson[lesson_id]
        visual = catalog.visual(body["visual"]) if body.get("visual") else None
        examples = [
            {
                "index": number,
                "title": catalog.t(example.get("title"), progress.language),
                "code": example["code"].strip("\n"),
                "output": (example.get("output") or "").strip("\n"),
                "note": catalog.t(example.get("note"), progress.language),
                "flow": flow_svg(example["code"]),
            }
            for number, example in enumerate(body.get("examples", []), 1)
        ]
        exercises = [
            {
                "index": number,
                "id": exercise["id"],
                "prompt": catalog.t(exercise["prompt"], progress.language),
                "starter": exercise.get("starter", ""),
                "hint": catalog.t(exercise.get("hint"), progress.language),
                "checks": len(exercise["checks"]),
                "passed": progress.exercise_passed(lesson_id, number - 1),
            }
            for number, exercise in enumerate(body.get("exercises", []), 1)
        ]
        return render_template(
            "lesson.html",
            lesson_id=lesson_id,
            body=body,
            title=catalog.t(body["title"], progress.language),
            module=catalog.by_module[module_id],
            chapter=catalog.chapters[catalog.chapter_of_lesson[lesson_id]],
            visual=visual,
            examples=examples,
            exercises=exercises,
            drills=[drill_lib.public(drill) for drill in progress.optional_drills(lesson_id)],
            ready=progress.practice_ready(lesson_id),
            practice_done=sum(1 for exercise in exercises if exercise["passed"]),
            quiz=_strip_answers(body["quiz"], progress.language, catalog),
            passed=progress.lesson_passed(lesson_id),
            best=progress.lesson_score(lesson_id),
            next_lesson=progress.next_lesson(),
        )

    def _exam_page(module_id: str, skip: bool):
        progress = progress_for(g.user)
        catalog = progress.catalog
        module = catalog.by_module.get(module_id)
        if not module:
            abort(404)
        if not progress.module_unlocked(module_id):
            return (
                render_template(
                    "locked.html",
                    what="module",
                    title=catalog.t(module["title"], progress.language),
                    previous=progress.next_lesson(),
                ),
                403,
            )
        full = catalog.full(module_id)
        items = full.get("skip_exam" if skip else "exam", [])
        remaining = (
            []
            if skip
            else [
                {
                    "id": lesson["id"],
                    "title": catalog.t(lesson["title"], progress.language),
                }
                for lesson in catalog.module_lessons(module_id)
                if not progress.lesson_passed(lesson["id"])
            ]
        )
        return render_template(
            "exam.html",
            module=module,
            module_id=module_id,
            title=catalog.t(module["title"], progress.language),
            skip=skip,
            items=_strip_answers(items, progress.language, catalog),
            blocked=bool(remaining),
            remaining=remaining,
            passed=progress.module_passed(module_id),
            best=progress.module_score(module_id),
        )

    @app.get("/exam/<module_id>")
    @login_required
    def exam(module_id: str):
        return _exam_page(module_id, skip=False)

    @app.get("/skip/<module_id>")
    @login_required
    def skip(module_id: str):
        return _exam_page(module_id, skip=True)

    @app.get("/playground")
    @login_required
    def playground():
        return render_template("playground.html", modules=ALLOWED_MODULES)

    @app.get("/progress")
    @login_required
    def progress_page():
        progress = progress_for(g.user)
        return render_template(
            "progress.html",
            board=progress.board(),
            state=progress.summary(),
            stats=progress.stats(),
            missed=progress.missed(),
        )

    # ---------------------------------------------------------------------- api
    @app.post("/api/quiz/<lesson_id>")
    @login_required
    def api_quiz(lesson_id: str):
        progress = progress_for(g.user)
        result = progress.submit_quiz(lesson_id, request.get_json(silent=True) or {})
        return jsonify(result), (200 if result.get("ok") else 400)

    @app.post("/api/exam/<module_id>")
    @login_required
    def api_exam(module_id: str):
        progress = progress_for(g.user)
        payload = request.get_json(silent=True) or {}
        result = progress.submit_exam(
            module_id, payload.get("answers") or payload, skip=bool(payload.get("skip"))
        )
        return jsonify(result), (200 if result.get("ok") else 400)

    @app.post("/api/run")
    @login_required
    def api_run():
        payload = request.get_json(silent=True) or {}
        result = run_code(payload.get("code") or "", trace=bool(payload.get("trace")))
        return jsonify(result)

    @app.post("/api/check/<exercise_id>")
    @login_required
    def api_check(exercise_id: str):
        progress = progress_for(g.user)
        catalog = progress.catalog
        match = _split_exercise(exercise_id)
        if not match:
            return jsonify({"ok": False, "error": "unknown exercise"}), 404
        lesson_id, index = match
        body = catalog.lesson(lesson_id)
        exercises = body.get("exercises", []) if body else []
        if not (0 <= index < len(exercises)):
            return jsonify({"ok": False, "error": "unknown exercise"}), 404
        if not progress.lesson_unlocked(lesson_id):
            return jsonify({"ok": False, "error": "locked"}), 403
        payload = request.get_json(silent=True) or {}
        exercise = exercises[index]
        result = check_exercise(
            payload.get("code") or "", exercise["checks"], trace=bool(payload.get("trace"))
        )
        result["hint"] = catalog.t(exercise.get("hint"), progress.language)
        if result.get("passed"):
            progress.record_practice(
                lesson_id, progress.exercise_id(lesson_id, index), "code", True
            )
        done, total = progress.practice_progress(lesson_id)
        result["practice"] = {"done": done, "total": total}
        result["ready"] = progress.practice_ready(lesson_id)
        return jsonify(result)

    @app.post("/api/drill/<lesson_id>")
    @login_required
    def api_drill(lesson_id: str):
        progress = progress_for(g.user)
        catalog = progress.catalog
        body = catalog.lesson(lesson_id)
        if not body:
            return jsonify({"ok": False, "error": "unknown lesson"}), 404
        if not progress.lesson_unlocked(lesson_id):
            return jsonify({"ok": False, "error": "locked"}), 403
        payload = request.get_json(silent=True) or {}
        drill = drill_lib.find(lesson_id, body, str(payload.get("drill_id") or ""))
        if not drill:
            return jsonify({"ok": False, "error": "unknown drill"}), 404
        result = drill_lib.grade(drill, payload.get("answer"))
        if result.get("ok"):
            progress.record_practice(
                lesson_id, drill["id"], drill["kind"], bool(result.get("passed"))
            )
        result["xp"] = drill["xp"] if result.get("passed") else 0
        result["xp_total"] = progress.xp()
        result["kind"] = drill["kind"]
        return jsonify(result)

    @app.post("/api/trace/<lesson_id>/<int:number>")
    @login_required
    def api_trace(lesson_id: str, number: int):
        progress = progress_for(g.user)
        catalog = progress.catalog
        body = catalog.lesson(lesson_id)
        examples = body.get("examples", []) if body else []
        if not (1 <= number <= len(examples)):
            return jsonify({"ok": False, "error": "unknown example"}), 404
        if not progress.lesson_unlocked(lesson_id):
            return jsonify({"ok": False, "error": "locked"}), 403
        example = examples[number - 1]
        result = run_code(example["code"], trace=True)
        result["code"] = example["code"].strip("\n").splitlines()
        result["expected"] = (example.get("output") or "").strip("\n")
        return jsonify(result)

    @app.post("/api/language")
    @login_required
    def api_language():
        payload = request.get_json(silent=True) or {}
        language = payload.get("language")
        if language not in LANGUAGES:
            return jsonify({"ok": False, "error": "unknown language"}), 400
        store.set_language(g.user["id"], language)
        return jsonify({"ok": True, "language": language, "reload": True})

    @app.post("/api/reset")
    @login_required
    def api_reset():
        store.reset(g.user["id"])
        store.audit(g.user["id"], "progress.reset", g.user.get("email") or "", "")
        return jsonify({"ok": True, "reload": True})

    @app.get("/api/export")
    @login_required
    def api_export():
        return jsonify(store.export(g.user["id"]))

    @app.get("/api/health")
    def api_health():
        return jsonify(
            {
                "ok": True,
                "modules": len(catalog.modules),
                "lessons": len(catalog.lessons),
                "courses": {
                    course_id: {
                        "modules": len(course.modules),
                        "lessons": len(course.lessons),
                    }
                    for course_id, course in catalogs.items()
                },
            }
        )

    # ------------------------------------------------------------------- admin
    app.register_blueprint(admin_bp)

    # ------------------------------------------------------------------ errors
    @app.errorhandler(400)
    def bad_request(error):
        message = getattr(error, "description", None) or "That request could not be understood."
        return render_template("error.html", code=400, message=message), 400

    @app.errorhandler(403)
    def forbidden(_error):
        return (
            render_template("error.html", code=403, message="You do not have access to that."),
            403,
        )

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("error.html", code=404, message="That page does not exist."), 404

    @app.errorhandler(413)
    def too_large(_error):
        return (
            render_template("error.html", code=413, message="That request was too large."),
            413,
        )

    return app


def _split_exercise(exercise_id: str):
    """``m01c01l01e2`` -> ``("m01c01l01", 1)``."""
    head, _, tail = exercise_id.rpartition("e")
    if not head or not tail.isdigit():
        return None
    index = int(tail) - 1
    if index < 0:
        return None
    return head, index


def __getattr__(name):
    """``app`` is built on first access, so importing this module has no side effects.

    Flask's CLI (``flask --app web.app run``) resolves the attribute lazily, and
    the tests call :func:`create_app` with their own temporary database.
    """
    if name == "app":
        return create_app()
    raise AttributeError(name)


def main() -> int:
    host = os.environ.get("PYBOOK_HOST", "127.0.0.1")
    port = int(os.environ.get("PYBOOK_PORT", "5000"))
    debug = os.environ.get("PYBOOK_DEBUG") == "1"
    print("PyBook on http://%s:%d" % (host, port))
    create_app().run(host=host, port=port, debug=debug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
