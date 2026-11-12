"""Small admin CLI: bootstrap the first admin and repair migrated accounts.

A fresh database has no admin, and an admin is the only account that can approve
anyone - so without this command a new install would be unusable.  It is also the
supported way to give a pre-account ``learners`` row an email and a password
after the automatic migration, without losing its id or its progress.

Examples::

    python -m web.manage create-admin --email owner@example.com --name "Owner"
    python -m web.manage claim --id 1 --email me@example.com --name "Asha" --admin
    python -m web.manage set-password --email owner@example.com
    python -m web.manage list

Passwords are typed at a hidden prompt, or piped with ``--password-stdin`` so a
password never appears in the process list or in shell history.
"""
from __future__ import annotations

import argparse
import getpass
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from web import auth  # noqa: E402
from web.store import Store, normalise_email  # noqa: E402

DEFAULT_DB = ROOT / "pybook.db"


def _read_password(args) -> str:
    if args.password_stdin:
        value = sys.stdin.readline().rstrip("\r\n")
        if not value:
            raise SystemExit("no password on stdin")
        return value
    first = getpass.getpass("Password: ")
    second = getpass.getpass("Repeat password: ")
    if first != second:
        raise SystemExit("the two passwords do not match")
    return first


def _set_password(store: Store, account: dict, password: str) -> None:
    problem = auth.password_problem(password, account.get("email") or "", account.get("name") or "")
    if problem:
        raise SystemExit("weak password: " + problem)
    store.set_password(account["id"], auth.hash_password(password))


def _find(store: Store, args) -> dict:
    account = store.user_by_id(args.id) if args.id else store.user_by_email(args.email or "")
    if not account:
        raise SystemExit("no account matched")
    return account


def cmd_create_admin(store: Store, args) -> int:
    if store.user_by_email(args.email):
        raise SystemExit("an account with that email already exists")
    password = _read_password(args)
    problem = auth.password_problem(password, args.email, args.name)
    if problem:
        raise SystemExit("weak password: " + problem)
    account = store.create_account(
        args.name,
        args.email,
        auth.hash_password(password),
        status="approved",
        role="admin",
        language=args.language,
    )
    if not account:
        raise SystemExit("could not create the account")
    store.audit(None, "cli.create_admin", normalise_email(args.email), args.name)
    print("created admin #%d %s" % (account["id"], account["email"]))
    return 0


def cmd_claim(store: Store, args) -> int:
    """Give a migrated account an email, a password and optionally the admin role."""
    account = store.user_by_id(args.id)
    if not account:
        raise SystemExit("no account with id %s" % args.id)
    address = normalise_email(args.email)
    other = store.user_by_email(address)
    if other and other["id"] != account["id"]:
        raise SystemExit("that email belongs to account #%d" % other["id"])
    password = _read_password(args)
    problem = auth.password_problem(password, address, args.name or account["name"])
    if problem:
        raise SystemExit("weak password: " + problem)

    store.db.execute(
        "UPDATE users SET email = ?, name = ?, password_hash = ?, status = 'approved', "
        "role = ? WHERE id = ?",
        (
            address,
            args.name or account["name"],
            auth.hash_password(password),
            "admin" if args.admin else account["role"],
            account["id"],
        ),
    )
    store.db.commit()
    store.set_status(account["id"], "approved", None, "claimed via cli")
    store.audit(account["id"], "cli.claim", address, "admin" if args.admin else "learner")
    print("account #%d is now %s (%s)" % (account["id"], address, "admin" if args.admin else account["role"]))
    return 0


def cmd_set_password(store: Store, args) -> int:
    account = _find(store, args)
    _set_password(store, account, _read_password(args))
    store.delete_sessions_for_user(account["id"])
    store.audit(account["id"], "cli.set_password", account.get("email") or "", "")
    print("password updated for #%d; existing sessions were revoked" % account["id"])
    return 0


def cmd_approve(store: Store, args) -> int:
    account = _find(store, args)
    store.set_status(account["id"], "approved", None, "approved via cli")
    store.audit(None, "cli.approve", account.get("email") or "", account["name"])
    print("#%d %s is approved" % (account["id"], account.get("email") or account["name"]))
    return 0


def cmd_promote(store: Store, args) -> int:
    account = _find(store, args)
    store.promote(account["id"])
    store.audit(None, "cli.promote", account.get("email") or "", account["name"])
    print("#%d %s is now an admin" % (account["id"], account.get("email") or account["name"]))
    return 0


def cmd_list(store: Store, args) -> int:
    rows = store.users(args.status or None)
    if not rows:
        print("no accounts")
        return 0
    print("%-4s %-28s %-9s %-7s %-6s %s" % ("id", "email", "status", "role", "course", "name"))
    for row in rows:
        print(
            "%-4d %-28s %-9s %-7s %-6s %s"
            % (
                row["id"],
                row.get("email") or "-",
                row["status"],
                row["role"],
                row.get("course") or "-",
                row["name"],
            )
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m web.manage", description=__doc__.splitlines()[0])
    parser.add_argument("--db", default=str(DEFAULT_DB), help="path to the SQLite file")
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p, *, need_id=False):
        p.add_argument("--id", type=int, help="account id")
        p.add_argument("--email", help="account email")
        p.add_argument("--password-stdin", action="store_true", help="read the password from stdin")

    p = sub.add_parser("create-admin", help="create the first approved admin")
    p.add_argument("--email", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--language", default="hinglish", choices=("en", "hi", "hinglish"))
    p.add_argument("--password-stdin", action="store_true")
    p.set_defaults(func=cmd_create_admin)

    p = sub.add_parser("claim", help="attach an email and password to a migrated account")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--email", required=True)
    p.add_argument("--name", default="")
    p.add_argument("--admin", action="store_true")
    p.add_argument("--password-stdin", action="store_true")
    p.set_defaults(func=cmd_claim)

    p = sub.add_parser("set-password", help="change a password and revoke old sessions")
    common(p)
    p.set_defaults(func=cmd_set_password)

    p = sub.add_parser("approve", help="approve an account")
    common(p)
    p.set_defaults(func=cmd_approve)

    p = sub.add_parser("promote", help="make an account an admin")
    common(p)
    p.set_defaults(func=cmd_promote)

    p = sub.add_parser("list", help="list accounts")
    p.add_argument("--status", choices=("pending", "approved", "rejected"))
    p.set_defaults(func=cmd_list)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    store = Store(args.db)
    try:
        if args.command in ("set-password", "approve", "promote") and not (args.id or args.email):
            raise SystemExit("give --id or --email")
        return args.func(store, args)
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(main())
