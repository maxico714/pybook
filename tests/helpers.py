"""Small helpers shared by the test modules.

Accounts are real rows in the real store: a test that needs a signed-in browser
creates an approved account and posts the real login form, so the session code
under test is the session code that runs in production.
"""
from __future__ import annotations

import re

from web.auth import hash_password

PASSWORD = "tester pass 123"
# Hashing is deliberately slow; do it once for the whole test session.
PASSWORD_HASH = hash_password(PASSWORD)

_CSRF = re.compile(r'name="csrf" value="([^"]+)"')


def csrf(html: str) -> str:
    match = _CSRF.search(html or "")
    assert match, "page has no csrf token"
    return match.group(1)


def make_user(
    app,
    *,
    name: str = "Tester",
    email: str = "tester@example.com",
    status: str = "approved",
    role: str = "learner",
    course: str = "pybook",
    language: str = "en",
    password: str = PASSWORD,
):
    """Create (or fetch) one account directly in the store."""
    store = app.config["STORE"]
    existing = store.user_by_email(email)
    if existing:
        return existing
    digest = PASSWORD_HASH if password == PASSWORD else hash_password(password)
    return store.create_account(
        name,
        email,
        digest,
        language=language,
        course=course,
        status=status,
        role=role,
    )


def signup(
    client,
    *,
    name: str = "Tester",
    email: str = "tester@example.com",
    password: str = PASSWORD,
    course: str = "pybook",
    language: str = "en",
    goal: str = "",
):
    """Submit the public signup form with a valid CSRF token."""
    page = client.get("/signup").get_data(as_text=True)
    return client.post(
        "/signup",
        data={
            "csrf": csrf(page),
            "name": name,
            "email": email,
            "password": password,
            "confirm": password,
            "course": course,
            "language": language,
            "goal": goal,
            "agree": "1",
        },
    )


def login(client, email: str = "tester@example.com", password: str = PASSWORD):
    page = client.get("/login").get_data(as_text=True)
    return client.post(
        "/login", data={"csrf": csrf(page), "email": email, "password": password}
    )


def signed_in(app, **kwargs):
    """A test client already logged in as an approved account."""
    client = app.test_client()
    account = make_user(app, **kwargs)
    response = login(client, email=account["email"], password=kwargs.get("password", PASSWORD))
    assert response.status_code == 302, "login was refused (%s)" % response.status_code
    return client


def approve(app, email: str = "tester@example.com"):
    """Approve an account the way the admin panel does."""
    account = app.config["STORE"].user_by_email(email)
    assert account, "no account for %s" % email
    app.config["STORE"].set_status(account["id"], "approved")
    return account


def post_form(client, path: str, data: dict, *, page: str = "/learn"):
    """POST a CSRF-protected HTML form."""
    token = csrf(client.get(page).get_data(as_text=True))
    payload = dict(data)
    payload["csrf"] = token
    return client.post(path, data=payload)


def switch_course(client, course_id: str):
    """Switch the active course the way the sidebar select does (JSON + header)."""
    token = csrf(client.get("/learn").get_data(as_text=True))
    return client.post("/switch/%s" % course_id, headers={"X-CSRF-Token": token})
