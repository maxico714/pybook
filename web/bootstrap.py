"""Create the first admin from environment variables, for hosts without a shell.

Render's free web services have no shell and no one-off jobs, so
``python -m web.manage create-admin`` cannot be run there.  A fresh deploy would
otherwise have no admin, and an admin is the only account that can approve a
sign-up - the site would be unusable.

Set ``PYBOOK_ADMIN_EMAIL`` and ``PYBOOK_ADMIN_PASSWORD`` (optionally
``PYBOOK_ADMIN_NAME``) and this runs once, on the first boot.  It never touches
an existing admin, so leaving the variables set is harmless; removing them after
the first successful boot is still the safer habit.
"""
from __future__ import annotations

import os

from . import auth


def ensure_admin(store) -> dict | None:
    """Create the bootstrap admin if needed. Returns the new account or ``None``."""
    email = (os.environ.get("PYBOOK_ADMIN_EMAIL") or "").strip()
    password = os.environ.get("PYBOOK_ADMIN_PASSWORD") or ""
    if not email or not password:
        return None

    existing = store.db.execute(
        "SELECT 1 FROM users WHERE role = 'admin' AND status = 'approved' LIMIT 1"
    ).fetchone()
    if existing:
        return None

    if len(password) < 8:
        print(
            "bootstrap: PYBOOK_ADMIN_PASSWORD is shorter than 8 characters; "
            "no admin was created. Fix the variable and restart.",
            flush=True,
        )
        return None

    name = (os.environ.get("PYBOOK_ADMIN_NAME") or "Admin").strip() or "Admin"
    account = store.create_account(
        name=name,
        email=email,
        password_hash=auth.hash_password(password),
        status="approved",
        role="admin",
    )
    if account is None:
        print("bootstrap: %s already exists; no admin was created." % email, flush=True)
        return None

    store.audit(account["id"], "bootstrap.admin", account.get("email") or email, "")
    print("bootstrap: created admin %s (id %d)" % (email, account["id"]), flush=True)
    return account
