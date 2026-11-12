"""Tests for accounts, admin approval and sessions.

The owner's requirement, in order: a visitor signs up, the request lands in the
admin panel, the admin approves or rejects it, only an approved account can log
in, and the login survives a browser restart.  Each of those is a test here.
"""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers import PASSWORD, approve, csrf, login, make_user, signed_in, signup  # noqa: E402


# ------------------------------------------------------------------ the flow
def test_the_whole_approval_flow(app):
    visitor = app.test_client()
    assert signup(visitor, name="Asha", email="asha@example.com", course="ai").status_code == 201

    store = app.config["STORE"]
    account = store.user_by_email("asha@example.com")
    assert account["status"] == "pending"
    assert account["course"] == "ai"

    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")
    requests_page = admin.get("/admin/requests").get_data(as_text=True)
    assert "Asha" in requests_page
    assert "asha@example.com" in requests_page

    token = csrf(requests_page)
    response = admin.post(
        "/admin/requests/%d/approve" % account["id"],
        data={"csrf": token, "note": "met in class"},
    )
    assert response.status_code == 302

    decided = store.user_by_id(account["id"])
    assert decided["status"] == "approved"
    assert decided["decision_note"] == "met in class"
    assert decided["decided_by"] == store.user_by_email("owner@example.com")["id"]

    assert login(visitor, email="asha@example.com").status_code == 302
    assert visitor.get("/learn").status_code == 200


def test_the_request_disappears_from_the_queue_once_decided(app):
    signup(app.test_client(), email="asha@example.com", name="Asha")
    admin = signed_in(app, email="owner@example.com", role="admin")
    account = app.config["STORE"].user_by_email("asha@example.com")

    token = csrf(admin.get("/admin/requests").get_data(as_text=True))
    admin.post("/admin/requests/%d/reject" % account["id"], data={"csrf": token, "note": "duplicate"})

    page = admin.get("/admin/requests").get_data(as_text=True)
    assert "No requests waiting" in page
    assert "asha@example.com" not in page
    assert "asha@example.com" in admin.get("/admin/users").get_data(as_text=True)


def test_a_rejected_account_cannot_log_in(app):
    signup(app.test_client(), email="asha@example.com", name="Asha")
    account = app.config["STORE"].user_by_email("asha@example.com")
    app.config["STORE"].set_status(account["id"], "rejected", None, "not a fit")

    response = login(app.test_client(), email="asha@example.com")
    assert response.status_code == 200
    assert "was not approved" in response.get_data(as_text=True)


def test_rejecting_an_account_kills_its_open_sessions(app):
    member = signed_in(app)
    account = app.config["STORE"].user_by_email("tester@example.com")
    assert member.get("/learn").status_code == 200

    app.config["STORE"].set_status(account["id"], "rejected")
    assert member.get("/learn").status_code == 302, "a revoked account must lose its session"


# --------------------------------------------------------------- the admin UI
def test_admin_pages_need_the_admin_role(app):
    member = signed_in(app)
    for path in ("/admin/", "/admin/requests", "/admin/users"):
        response = member.get(path)
        assert response.status_code == 302, path
        assert response.headers["Location"].endswith("/learn"), path


def test_anonymous_admin_access_goes_to_login(app):
    response = app.test_client().get("/admin/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_admin_post_needs_a_csrf_token(app):
    signup(app.test_client(), email="asha@example.com", name="Asha")
    admin = signed_in(app, email="owner@example.com", role="admin")
    account = app.config["STORE"].user_by_email("asha@example.com")

    response = admin.post("/admin/requests/%d/approve" % account["id"], data={})
    assert response.status_code == 400
    assert app.config["STORE"].user_by_id(account["id"])["status"] == "pending"


def test_an_admin_cannot_reject_their_own_account(app):
    admin = signed_in(app, email="owner@example.com", role="admin")
    account = app.config["STORE"].user_by_email("owner@example.com")
    token = csrf(admin.get("/admin/users").get_data(as_text=True))

    admin.post(
        "/admin/users/%d/status" % account["id"],
        data={"csrf": token, "status": "rejected"},
    )
    assert app.config["STORE"].user_by_id(account["id"])["status"] == "approved"


def test_dashboard_counts_and_audit_are_real(app):
    signup(app.test_client(), email="asha@example.com", name="Asha")
    signup(app.test_client(), email="ravi@example.com", name="Ravi")
    admin = signed_in(app, email="owner@example.com", role="admin")
    page = admin.get("/admin/").get_data(as_text=True)

    assert "2" in page
    assert "waiting for approval" in page
    assert "account.signup" in page


# ------------------------------------------------------------------- sessions
def test_the_session_survives_a_new_client_and_logout_revokes_it(app):
    member = signed_in(app)
    token = member.get_cookie("pybook_session").value

    fresh = app.test_client()
    fresh.set_cookie("pybook_session", token)
    assert fresh.get("/learn").status_code == 200, "the cookie alone must restore the login"

    csrf_token = csrf(fresh.get("/learn").get_data(as_text=True))
    assert fresh.post("/logout", data={"csrf": csrf_token}).status_code == 302

    replay = app.test_client()
    replay.set_cookie("pybook_session", token)
    assert replay.get("/learn").status_code == 302, "logout must revoke the token server-side"


def test_the_database_never_stores_a_raw_password_or_session_token(app):
    member = signed_in(app)
    store = app.config["STORE"]
    account = store.user_by_email("tester@example.com")
    raw_token = member.get_cookie("pybook_session").value

    assert PASSWORD not in account["password_hash"]
    assert account["password_hash"].startswith(("scrypt:", "pbkdf2:"))

    row = store.db.execute("SELECT token_hash FROM sessions").fetchone()
    assert row["token_hash"] != raw_token
    assert len(row["token_hash"]) == 64, "the stored value is a sha256 hex digest"


def test_a_stale_session_row_is_refused(app):
    member = signed_in(app)
    app.config["STORE"].db.execute("UPDATE sessions SET expires = '2000-01-01T00:00:00'")
    app.config["STORE"].db.commit()
    assert member.get("/learn").status_code == 302


def test_next_parameter_cannot_leave_the_site(app):
    visitor = app.test_client()
    token = csrf(visitor.get("/login").get_data(as_text=True))
    make_user(app, email="asha@example.com")

    response = visitor.post(
        "/login",
        data={
            "csrf": token,
            "email": "asha@example.com",
            "password": PASSWORD,
            "next": "https://evil.example/steal",
        },
    )
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/learn")
    assert "evil.example" not in response.headers["Location"]


# ----------------------------------------------------------------- throttling
def test_five_wrong_passwords_lock_the_pair_for_a_while(app):
    make_user(app, email="asha@example.com")
    visitor = app.test_client()
    token = csrf(visitor.get("/login").get_data(as_text=True))

    for _ in range(5):
        visitor.post(
            "/login",
            data={"csrf": token, "email": "asha@example.com", "password": "wrong password"},
        )

    blocked = visitor.post(
        "/login",
        data={"csrf": token, "email": "asha@example.com", "password": PASSWORD},
    )
    assert blocked.status_code == 200
    assert "Too many attempts" in blocked.get_data(as_text=True)


def test_a_different_email_is_not_locked_out_by_someone_else(app):
    make_user(app, email="asha@example.com")
    make_user(app, email="ravi@example.com")
    visitor = app.test_client()
    token = csrf(visitor.get("/login").get_data(as_text=True))

    for _ in range(5):
        visitor.post(
            "/login",
            data={"csrf": token, "email": "asha@example.com", "password": "wrong password"},
        )

    assert login(visitor, email="ravi@example.com").status_code == 302


def test_a_cross_site_post_cannot_drive_the_json_api(app):
    """A foreign Origin is refused even though the session cookie is Lax."""
    member = signed_in(app)
    response = member.post(
        "/api/language",
        json={"language": "en"},
        headers={"Origin": "https://evil.example"},
    )
    assert response.status_code == 400

    allowed = member.post(
        "/api/language",
        json={"language": "en"},
        headers={"Origin": "http://localhost"},
    )
    assert allowed.status_code == 200


def test_a_cross_site_form_post_has_no_session_and_no_token(app):
    """Without the cookie there is no CSRF token, so the form post is a 400."""
    make_user(app, email="asha@example.com")
    response = app.test_client().post(
        "/login",
        data={"email": "asha@example.com", "password": PASSWORD},
        headers={"Origin": "https://evil.example"},
    )
    assert response.status_code == 400


# ---------------------------------------------------------------- admin panel
def test_the_dashboard_shows_the_queue_and_the_signup_chart(app):
    signup(app.test_client(), name="Asha", email="asha@example.com")
    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")

    page = admin.get("/admin/").get_data(as_text=True)
    assert "Asha" in page
    assert "New accounts, last 14 days" in page
    assert "signup-chart" in page
    # The chart is fed a dense 14-day series built from real rows, not a mock.
    assert "var series = [" in page
    assert page.count('"day"') == 14


def test_user_detail_shows_progress_sessions_and_history(app):
    learner = make_user(app, name="Asha", email="asha@example.com")
    app.config["STORE"].record_lesson(learner["id"], "m01c01l01", 1.0, True, [])
    signed_in(app, name="Asha", email="asha@example.com")  # leaves one open session

    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")
    page = admin.get("/admin/users/%d" % learner["id"]).get_data(as_text=True)

    assert "asha@example.com" in page
    assert "1/53 lessons" in page  # one passed lesson out of the Python course
    assert "Open sessions" in page
    assert "History" in page


def test_admin_can_search_and_filter_the_roster(app):
    make_user(app, name="Asha Verma", email="asha@example.com")
    make_user(app, name="Ravi Kumar", email="ravi@example.com")
    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")

    found = admin.get("/admin/users?q=asha").get_data(as_text=True)
    assert "asha@example.com" in found
    assert "ravi@example.com" not in found

    approved = admin.get("/admin/users?status=approved&role=learner").get_data(as_text=True)
    assert "asha@example.com" in approved
    assert "owner@example.com" in approved  # the admin is approved too

    missing = admin.get("/admin/users?q=nobody-here").get_data(as_text=True)
    assert "Nothing matches" in missing


def test_admin_can_promote_and_demote_but_not_themselves(app):
    learner = make_user(app, name="Asha", email="asha@example.com")
    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")
    store = app.config["STORE"]
    token = csrf(admin.get("/admin/users/%d" % learner["id"]).get_data(as_text=True))

    admin.post("/admin/users/%d/role" % learner["id"], data={"csrf": token, "role": "admin"})
    assert store.user_by_id(learner["id"])["role"] == "admin"

    admin.post("/admin/users/%d/role" % learner["id"], data={"csrf": token, "role": "learner"})
    assert store.user_by_id(learner["id"])["role"] == "learner"

    me = store.user_by_email("owner@example.com")
    admin.post("/admin/users/%d/role" % me["id"], data={"csrf": token, "role": "learner"})
    assert store.user_by_id(me["id"])["role"] == "admin"
    assert "cannot change your own role" in admin.get("/admin/users/%d" % me["id"]).get_data(as_text=True)


def test_revoking_sessions_signs_the_learner_out(app):
    learner = signed_in(app, name="Asha", email="asha@example.com")
    assert learner.get("/learn").status_code == 200

    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")
    account = app.config["STORE"].user_by_email("asha@example.com")
    token = csrf(admin.get("/admin/users/%d" % account["id"]).get_data(as_text=True))
    admin.post("/admin/users/%d/sessions/revoke" % account["id"], data={"csrf": token})

    assert learner.get("/learn").status_code == 302


def test_admin_can_set_a_password_and_the_old_one_stops_working(app):
    make_user(app, name="Asha", email="asha@example.com")
    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")
    account = app.config["STORE"].user_by_email("asha@example.com")
    token = csrf(admin.get("/admin/users/%d" % account["id"]).get_data(as_text=True))

    response = admin.post(
        "/admin/users/%d/password" % account["id"],
        data={"csrf": token, "password": "quiet forest 77"},
    )
    assert response.status_code == 302

    visitor = app.test_client()
    assert login(visitor, email="asha@example.com", password="quiet forest 77").status_code == 302
    assert login(app.test_client(), email="asha@example.com").status_code == 200  # old password


def test_the_audit_page_lists_the_decisions(app):
    signup(app.test_client(), name="Asha", email="asha@example.com")
    approve(app, "asha@example.com")
    admin = signed_in(app, name="Owner", email="owner@example.com", role="admin")

    page = admin.get("/admin/audit").get_data(as_text=True)
    assert "account.signup" in page
    assert "asha@example.com" in page

    filtered = admin.get("/admin/audit?action=account.").get_data(as_text=True)
    assert "account.signup" in filtered


def test_healthz_reports_the_database(app):
    response = app.test_client().get("/healthz")
    assert response.status_code == 200
    assert response.get_json()["ok"] is True
    assert response.get_json()["database"] == "ok"
    assert response.headers["Cache-Control"] == "no-store"


def test_signup_is_rate_limited_per_address(app):
    app.config["SIGNUP_LIMIT"] = 2
    visitor = app.test_client()

    assert signup(visitor, email="one@example.com", name="One").status_code == 201
    assert signup(visitor, email="two@example.com", name="Two").status_code == 201

    blocked = signup(visitor, email="three@example.com", name="Three")
    assert blocked.status_code == 429
    assert "Too many new accounts" in blocked.get_data(as_text=True)
    assert app.config["STORE"].user_by_email("three@example.com") is None


def test_the_store_is_safe_from_several_threads(app):
    """A threaded WSGI server shares one Store; each thread needs its own handle."""
    import threading

    store = app.config["STORE"]
    make_user(app, email="asha@example.com")
    errors: list[BaseException] = []

    def worker():
        try:
            for _ in range(10):
                store.counts()
                store.user_by_email("asha@example.com")
                store.audit(None, "test.thread", "thread", "")
        except BaseException as exc:  # noqa: BLE001 - the test reports whatever happened
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert errors == []
    assert len(store.recent_audit(200)) >= 80


# ---------------------------------------------------------------- migration
def test_an_old_learners_table_is_migrated_without_losing_progress(tmp_path):
    """The pre-account database must keep its rows and its progress."""
    import sqlite3

    from web.app import create_app

    path = tmp_path / "old.db"
    raw = sqlite3.connect(str(path))
    raw.executescript(
        """
        CREATE TABLE learners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            name TEXT NOT NULL,
            language TEXT NOT NULL DEFAULT 'hinglish',
            course TEXT NOT NULL DEFAULT 'pybook',
            created TEXT NOT NULL
        );
        CREATE TABLE lesson_progress (
            learner_id INTEGER NOT NULL,
            lesson_id TEXT NOT NULL,
            attempts INTEGER NOT NULL DEFAULT 0,
            best REAL NOT NULL DEFAULT 0,
            last REAL NOT NULL DEFAULT 0,
            passed INTEGER NOT NULL DEFAULT 0,
            updated TEXT NOT NULL,
            PRIMARY KEY (learner_id, lesson_id)
        );
        INSERT INTO learners (token, name, language, course, created)
            VALUES ('old-token', 'Old Learner', 'hi', 'pybook', '2026-01-01T00:00:00');
        INSERT INTO lesson_progress (learner_id, lesson_id, attempts, best, last, passed, updated)
            VALUES (1, 'm01c01l01', 2, 100, 100, 1, '2026-01-01T00:00:00');
        """
    )
    raw.commit()
    raw.close()

    app = create_app(db_path=path, testing=True)
    store = app.config["STORE"]
    migrated = store.user_by_id(1)
    assert migrated["name"] == "Old Learner"
    assert migrated["status"] == "approved"
    assert migrated["language"] == "hi"
    assert store.lessons(1)["m01c01l01"]["passed"] == 1
    assert store.db.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='learners'"
    ).fetchone() is None

# ------------------------------------------------------- bootstrap (no shell)
def test_bootstrap_creates_the_first_admin_once(app, monkeypatch):
    """Render has no shell, so the first admin must come from env vars."""
    from web.bootstrap import ensure_admin

    store = app.config["STORE"]
    monkeypatch.setenv("PYBOOK_ADMIN_EMAIL", "boss@example.com")
    monkeypatch.setenv("PYBOOK_ADMIN_PASSWORD", "quiet forest 77")
    monkeypatch.setenv("PYBOOK_ADMIN_NAME", "Boss")

    first = ensure_admin(store)
    assert first is not None
    assert first["role"] == "admin"
    assert first["status"] == "approved"

    # A restart with the same variables must not create a second admin.
    assert ensure_admin(store) is None
    admins = store.db.execute(
        "SELECT COUNT(*) AS n FROM users WHERE role = 'admin'"
    ).fetchone()["n"]
    assert admins == 1

    # The password really works for logging in.
    client = app.test_client()
    response = login(client, email="boss@example.com", password="quiet forest 77")
    assert response.status_code == 302


def test_bootstrap_refuses_a_short_password(app, monkeypatch):
    from web.bootstrap import ensure_admin

    store = app.config["STORE"]
    monkeypatch.setenv("PYBOOK_ADMIN_EMAIL", "boss@example.com")
    monkeypatch.setenv("PYBOOK_ADMIN_PASSWORD", "short")

    assert ensure_admin(store) is None
    assert store.user_by_email("boss@example.com") is None


def test_bootstrap_does_nothing_without_variables(app, monkeypatch):
    from web.bootstrap import ensure_admin

    store = app.config["STORE"]
    monkeypatch.delenv("PYBOOK_ADMIN_EMAIL", raising=False)
    monkeypatch.delenv("PYBOOK_ADMIN_PASSWORD", raising=False)
    assert ensure_admin(store) is None
