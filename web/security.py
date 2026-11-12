"""Secret key and HTTP security headers.

The secret key signs the small Flask session that carries the CSRF token.  It
is read from ``PYBOOK_SECRET_KEY`` when set, otherwise generated once and kept
in ``instance/secret_key`` so a restart does not invalidate every open form.

The CSP below is deliberately honest: Alpine.js evaluates expressions with
``new Function``, so ``'unsafe-eval'`` is required for the interactive parts to
work.  Everything else is locked to ``'self'`` - no CDN, no remote font, no
third-party script, which matches the local-only promise of the project.
"""
from __future__ import annotations

import os
import pathlib
import secrets

HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "same-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=(), payment=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'"
    ),
}


def load_secret_key(app) -> str:
    env = os.environ.get("PYBOOK_SECRET_KEY")
    if env:
        return env
    if app.config.get("TESTING"):
        return "pybook-testing-secret-key-not-for-production"
    path = pathlib.Path(app.instance_path) / "secret_key"
    if path.is_file():
        value = path.read_text(encoding="utf-8").strip()
        if len(value) >= 32:
            return value
    value = secrets.token_hex(32)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:  # Windows: best effort, the file is inside the project
        pass
    return value


def apply_headers(response):
    for name, value in HEADERS.items():
        response.headers.setdefault(name, value)
    return response
