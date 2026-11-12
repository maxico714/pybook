"""Admin panel: review account requests, manage the roster, read the audit trail.

Every action is a POST with a CSRF token, is restricted to an ``admin`` role, and
writes an audit row.  An admin can never reject, demote or deactivate their own
account, so a single admin cannot lock the panel out.
"""
from __future__ import annotations

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from . import auth
from .auth import admin_required, current_user

bp = Blueprint("admin", __name__, url_prefix="/admin")

STATUS_LABELS = {
    "pending": "waiting",
    "approved": "approved",
    "rejected": "rejected",
}

ACTION_FILTERS = (
    ("", "Everything"),
    ("account.", "Account decisions"),
    ("login", "Logins"),
    ("progress.", "Progress"),
    ("cli.", "Command line"),
)


def _store():
    return current_app.config["STORE"]


def _catalogs():
    return current_app.config["CATALOGS"]


def _course_rows(store, user_id: int, language: str = "en") -> list[dict]:
    """Progress per course, counted against the real catalogues."""
    lessons = store.lessons(user_id)
    modules = store.modules(user_id)
    rows = []
    for course_id, catalog in _catalogs().items():
        passed = sum(
            1 for lesson in catalog.lessons if lessons.get(lesson["id"], {}).get("passed")
        )
        modules_done = sum(
            1
            for module in catalog.modules
            if modules.get(module["id"], {}).get("exam_passed")
            or modules.get(module["id"], {}).get("skip_passed")
        )
        rows.append(
            {
                "id": course_id,
                "title": catalog.t(catalog.index.get("title"), language),
                "lessons": passed,
                "lesson_total": len(catalog.lessons),
                "modules": modules_done,
                "module_total": len(catalog.modules),
                "percent": round(100 * passed / max(1, len(catalog.lessons))),
            }
        )
    return rows


@bp.get("/")
@admin_required
def dashboard():
    store = _store()
    counts = store.counts()
    return render_template(
        "admin/dashboard.html",
        counts=counts,
        pending=store.pending_users()[:6],
        audit=store.recent_audit(8),
        series=store.signups_per_day(14),
        active="dashboard",
    )


@bp.get("/requests")
@admin_required
def requests_page():
    store = _store()
    return render_template(
        "admin/requests.html",
        pending=store.pending_users(),
        counts=store.counts(),
        active="requests",
    )


@bp.get("/users")
@admin_required
def users_page():
    store = _store()
    status = request.args.get("status") or ""
    if status not in ("pending", "approved", "rejected"):
        status = ""
    role = request.args.get("role") or ""
    if role not in ("learner", "admin"):
        role = ""
    query = (request.args.get("q") or "").strip()[:80]
    return render_template(
        "admin/users.html",
        users=store.users(status or None, query=query, role=role),
        counts=store.counts(),
        status=status,
        role=role,
        query=query,
        active="users",
    )


@bp.get("/users/<int:user_id>")
@admin_required
def user_detail(user_id: int):
    store = _store()
    account = store.user_by_id(user_id)
    if not account:
        flash("That account no longer exists.", "bad")
        return redirect(url_for("admin.users_page"))
    return render_template(
        "admin/user.html",
        account=account,
        courses=_course_rows(store, user_id, (current_user(store) or {}).get("language", "en")),
        sessions=store.sessions_for_user(user_id),
        history=store.audit_for_subject(account.get("email") or ""),
        active="users",
        counts=store.counts(),
    )


@bp.get("/audit")
@admin_required
def audit_page():
    store = _store()
    action = request.args.get("action") or ""
    if action and not any(action == prefix for prefix, _ in ACTION_FILTERS):
        action = ""
    return render_template(
        "admin/audit.html",
        rows=store.audit_page(action),
        action=action,
        filters=ACTION_FILTERS,
        counts=store.counts(),
        active="audit",
    )


# ------------------------------------------------------------------- decisions
@bp.post("/requests/<int:user_id>/approve")
@admin_required
def approve(user_id: int):
    store = _store()
    actor = current_user(store)
    account = store.user_by_id(user_id)
    if not account:
        flash("That account no longer exists.", "bad")
        return redirect(url_for("admin.requests_page"))
    if account["status"] == "approved":
        flash("%s is already approved." % account["name"], "info")
        return redirect(url_for("admin.requests_page"))
    store.set_status(user_id, "approved", actor["id"], request.form.get("note") or "")
    store.audit(actor["id"], "account.approve", account.get("email") or "", account["name"])
    flash("%s can now log in." % account["name"], "ok")
    return redirect(url_for("admin.requests_page"))


@bp.post("/requests/<int:user_id>/reject")
@admin_required
def reject(user_id: int):
    store = _store()
    actor = current_user(store)
    account = store.user_by_id(user_id)
    if not account:
        flash("That account no longer exists.", "bad")
        return redirect(url_for("admin.requests_page"))
    if account["id"] == actor["id"]:
        flash("You cannot reject your own account.", "bad")
        return redirect(url_for("admin.requests_page"))
    note = (request.form.get("note") or "").strip()
    store.set_status(user_id, "rejected", actor["id"], note)
    store.delete_sessions_for_user(user_id)
    store.audit(actor["id"], "account.reject", account.get("email") or "", note)
    flash("%s was rejected." % account["name"], "ok")
    return redirect(url_for("admin.requests_page"))


@bp.post("/users/<int:user_id>/status")
@admin_required
def set_status(user_id: int):
    """Approve, reject or revoke from the roster page."""
    store = _store()
    actor = current_user(store)
    account = store.user_by_id(user_id)
    status = (request.form.get("status") or "").strip()
    if not account:
        flash("That account no longer exists.", "bad")
        return redirect(url_for("admin.users_page"))
    if status not in ("approved", "rejected", "pending"):
        flash("Unknown status.", "bad")
        return redirect(url_for("admin.users_page"))
    if account["id"] == actor["id"]:
        flash("You cannot change your own status.", "bad")
        return redirect(url_for("admin.users_page"))
    store.set_status(user_id, status, actor["id"], request.form.get("note") or "")
    if status != "approved":
        store.delete_sessions_for_user(user_id)
    store.audit(actor["id"], "account.%s" % status, account.get("email") or "", account["name"])
    flash("%s is now %s." % (account["name"], STATUS_LABELS[status]), "ok")
    return redirect(
        url_for("admin.user_detail", user_id=user_id)
        if request.form.get("from") == "detail"
        else url_for("admin.users_page", status=request.form.get("filter") or None)
    )


@bp.post("/users/<int:user_id>/role")
@admin_required
def set_role(user_id: int):
    """Promote a learner to admin, or demote an admin back to learner."""
    store = _store()
    actor = current_user(store)
    account = store.user_by_id(user_id)
    role = (request.form.get("role") or "").strip()
    if not account:
        flash("That account no longer exists.", "bad")
        return redirect(url_for("admin.users_page"))
    if role not in ("learner", "admin"):
        flash("Unknown role.", "bad")
        return redirect(url_for("admin.users_page"))
    if account["id"] == actor["id"]:
        flash("You cannot change your own role.", "bad")
        return redirect(url_for("admin.user_detail", user_id=user_id))
    store.set_role(user_id, role)
    store.audit(actor["id"], "account.role", account.get("email") or "", role)
    flash("%s is now %s." % (account["name"], "an admin" if role == "admin" else "a learner"), "ok")
    return redirect(url_for("admin.user_detail", user_id=user_id))


@bp.post("/users/<int:user_id>/sessions/revoke")
@admin_required
def revoke_sessions(user_id: int):
    """Sign an account out everywhere; the password itself does not change."""
    store = _store()
    actor = current_user(store)
    account = store.user_by_id(user_id)
    if not account:
        flash("That account no longer exists.", "bad")
        return redirect(url_for("admin.users_page"))
    store.delete_sessions_for_user(user_id)
    store.audit(actor["id"], "session.revoke", account.get("email") or "", "all devices")
    flash("Signed %s out on every device." % account["name"], "ok")
    if account["id"] == actor["id"]:
        return redirect(url_for("login"))
    return redirect(url_for("admin.user_detail", user_id=user_id))


@bp.post("/users/<int:user_id>/password")
@admin_required
def reset_password(user_id: int):
    """Set a new password when there is no email delivery to send a reset link."""
    store = _store()
    actor = current_user(store)
    account = store.user_by_id(user_id)
    if not account:
        flash("That account no longer exists.", "bad")
        return redirect(url_for("admin.users_page"))
    password = request.form.get("password") or ""
    problem = auth.password_problem(password, account.get("email") or "", account.get("name") or "")
    if problem:
        flash(problem, "bad")
        return redirect(url_for("admin.user_detail", user_id=user_id))
    store.set_password(user_id, auth.hash_password(password))
    if account["id"] != actor["id"]:
        store.delete_sessions_for_user(user_id)
    store.audit(actor["id"], "account.password", account.get("email") or "", "set by admin")
    flash("New password saved for %s." % account["name"], "ok")
    return redirect(url_for("admin.user_detail", user_id=user_id))
