"""Accounts, sessions, CSRF and login throttling.

Design decisions, and why:

* **Passwords** use :func:`werkzeug.security.generate_password_hash`, which is
  scrypt in current Werkzeug.  Nothing hand-rolled.
* **Sessions** are server-side rows.  The browser holds a random token; the
  database holds only its SHA-256 hash.  That makes logout, "approval
  withdrawn" and password change able to kill a session immediately - a signed
  cookie cannot do that.
* **Persistence**: the cookie carries ``Max-Age`` (30 days by default), so a
  browser restart keeps the login, which is what the owner asked for.
* **CSRF**: HTML forms carry a token kept in the signed Flask session.  JSON
  ``/api`` calls are same-origin ``fetch`` with ``Content-Type: application/json``
  and a ``SameSite=Lax`` cookie; they are additionally checked against the
  ``Origin``/``Referer`` header, so a cross-site form cannot drive them.
* **Throttling**: five failures per ``email|ip`` in fifteen minutes locks that
  pair for fifteen minutes.  It is deliberately per-pair, so one attacker cannot
  lock a real user out of their own account from another address.
"""
from __future__ import annotations

import hashlib
import hmac
import re
import secrets
from functools import wraps
from urllib.parse import urlsplit

from flask import current_app, g, jsonify, redirect, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

COOKIE = "pybook_session"
REMEMBER_DAYS = 30
TOUCH_SECONDS = 60

FAILURE_LIMIT = 5
FAILURE_WINDOW = 15 * 60
LOCK_SECONDS = 15 * 60

# New accounts are cheap to request and expensive to review, so a single address
# may only create a handful per hour.  This is an anti-spam guard, not a
# security boundary: a determined person can change address.
SIGNUP_LIMIT = 10
SIGNUP_WINDOW = 60 * 60
SIGNUP_LOCK = 60 * 60

MIN_PASSWORD = 8
MAX_PASSWORD = 200
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")
_WEAK = {
    "password",
    "password1",
    "password123",
    "12345678",
    "123456789",
    "qwerty123",
    "letmein1",
    "iloveyou",
    "admin123",
    "changeme",
}


# ------------------------------------------------------------------ passwords
def hash_password(password: str) -> str:
    return generate_password_hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    if not password_hash:
        return False
    try:
        return check_password_hash(password_hash, password)
    except (ValueError, TypeError):
        return False


def password_problem(password: str, email: str = "", name: str = "") -> str | None:
    """A human message when the password is too weak, otherwise ``None``."""
    if not password:
        return "Choose a password."
    if len(password) < MIN_PASSWORD:
        return "Use at least %d characters." % MIN_PASSWORD
    if len(password) > MAX_PASSWORD:
        return "That password is too long."
    if password.lower() in _WEAK:
        return "That password is too common. Choose another one."
    if len(set(password)) == 1:
        return "Use more than one repeated character."
    local = (email or "").split("@")[0].lower()
    if local and len(local) > 3 and local in password.lower():
        return "Do not put your email address in the password."
    first = (name or "").split(" ")[0].lower()
    if first and len(first) > 3 and password.lower() == first:
        return "Do not use your own name as the password."
    return None


# ------------------------------------------------------------------- sessions
def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def issue_session(store, user_id: int, days: int = REMEMBER_DAYS) -> str:
    """Create a session row and return the raw token for the cookie."""
    import datetime as _dt

    token = secrets.token_urlsafe(32)
    expires = (_dt.datetime.now() + _dt.timedelta(days=days)).replace(microsecond=0).isoformat()
    store.create_session(user_id, token_hash(token), expires, request.user_agent.string or "")
    return token


def session_token() -> str:
    return request.cookies.get(COOKIE, "")


def current_user(store):
    """The signed-in account for this request, or ``None``."""
    token = session_token()
    if not token:
        return None
    user = store.session_user(token_hash(token))
    if not user:
        return None
    if user.get("status") != "approved":
        store.delete_session(token_hash(token))
        return None
    store.touch_session(token_hash(token))
    return user


def end_session(store) -> None:
    token = session_token()
    if token:
        store.delete_session(token_hash(token))


def set_session_cookie(response, token: str) -> None:
    response.set_cookie(
        COOKIE,
        token,
        max_age=REMEMBER_DAYS * 24 * 60 * 60,
        httponly=True,
        samesite="Lax",
        secure=bool(current_app.config.get("SECURE_COOKIES")),
        path="/",
    )


def clear_session_cookie(response) -> None:
    response.delete_cookie(COOKIE, path="/")


# ----------------------------------------------------------------------- CSRF
def csrf_token() -> str:
    token = session.get("csrf")
    if not token:
        token = secrets.token_urlsafe(32)
        session["csrf"] = token
    return token


def _same_origin() -> bool:
    """True when the request's Origin/Referer names this host."""
    source = request.headers.get("Origin") or request.headers.get("Referer") or ""
    if not source:
        return True  # a same-origin form post may omit both; the token still guards it
    host = urlsplit(source).netloc.lower()
    return host == request.host.lower()


def csrf_ok() -> bool:
    if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
        return True
    if request.path.startswith("/api/"):
        return _same_origin()
    sent = request.form.get("csrf") or request.headers.get("X-CSRF-Token") or ""
    expected = session.get("csrf") or ""
    return bool(sent and expected and hmac.compare_digest(sent, expected))


# ------------------------------------------------------------------ throttling
def attempt_key(email: str, ip: str) -> str:
    return "%s|%s" % ((email or "").strip().lower(), (ip or "")[:60])


def is_locked(store, key: str) -> str | None:
    return store.blocked_until(store.attempt(key))


def note_failure(store, key: str) -> None:
    store.record_failure(key, FAILURE_LIMIT, FAILURE_WINDOW, LOCK_SECONDS)


def note_success(store, key: str) -> None:
    store.clear_failures(key)


# Signup uses the same counter table with its own key namespace, so one
# mechanism (and one tested code path) covers both throttles.
def signup_key(ip: str) -> str:
    return "signup|%s" % ((ip or "")[:60])


def signup_locked(store, ip: str) -> str | None:
    return is_locked(store, signup_key(ip))


def note_signup(store, ip: str, limit: int = SIGNUP_LIMIT) -> None:
    store.record_failure(signup_key(ip), max(1, limit), SIGNUP_WINDOW, SIGNUP_LOCK)


# ------------------------------------------------------------------ decorators
def _wants_json() -> bool:
    return request.path.startswith("/api/") or request.accept_mimetypes.best == "application/json"


def _current():
    """The account for this request, loading it once into ``g``."""
    user = getattr(g, "user", None)
    if user is None:
        store = current_app.config.get("STORE")
        if store is not None:
            user = current_user(store)
            g.user = user
    return user


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = _current()
        if not user:
            if _wants_json():
                return jsonify({"ok": False, "error": "login"}), 401
            target = request.full_path if request.query_string else request.path
            return redirect(url_for("login", next=target))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = _current()
        if not user:
            if _wants_json():
                return jsonify({"ok": False, "error": "login"}), 401
            return redirect(url_for("login", next=request.path))
        if user.get("role") != "admin":
            if _wants_json():
                return jsonify({"ok": False, "error": "forbidden"}), 403
            return redirect(url_for("learn"))
        return view(*args, **kwargs)

    return wrapped


# ----------------------------------------------------------------- validation
def clean_name(value: str) -> str:
    return " ".join((value or "").split())[:60]


def email_problem(value: str) -> str | None:
    address = (value or "").strip()
    if not address:
        return "Enter your email address."
    if len(address) > 190 or not _EMAIL.match(address):
        return "That does not look like an email address."
    return None


def safe_next(target: str | None, fallback: str) -> str:
    """Only allow a local path, so ``?next=`` cannot become an open redirect."""
    if not target:
        return fallback
    parts = urlsplit(target)
    if parts.scheme or parts.netloc:
        return fallback
    if not target.startswith("/") or target.startswith("//"):
        return fallback
    return target
