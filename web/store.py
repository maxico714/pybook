"""SQLite persistence for PyBook: accounts, sessions and learner progress.

``users`` is the account table the admin panel works on.  Progress tables
reference ``users.id``, so switching course never mixes two courses' rows
(lesson and module ids are disjoint between courses).

Security properties that matter here:

* a password is only ever stored as a Werkzeug hash (scrypt by default);
* a session token is random, stored as a SHA-256 hash, and revocable - a stolen
  database cannot be replayed as a login;
* failed logins are counted per ``email|ip`` with a lockout window;
* every account decision (signup, approve, reject, login) is written to
  ``audit`` so the owner can see who did what.

The module deliberately keeps raw SQL: the schema is small, and a migration
that runs on an existing database is easier to reason about than an ORM.
"""
from __future__ import annotations

import datetime as _dt
import pathlib
import secrets
import sqlite3
import threading

# --------------------------------------------------------------------- schema
SCHEMA_ACCOUNTS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    password_hash TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    role TEXT NOT NULL DEFAULT 'learner',
    goal TEXT NOT NULL DEFAULT '',
    language TEXT NOT NULL DEFAULT 'hinglish',
    course TEXT NOT NULL DEFAULT 'pybook',
    created TEXT NOT NULL,
    decided_at TEXT,
    decided_by INTEGER,
    decision_note TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS users_email ON users(email) WHERE email IS NOT NULL;

CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created TEXT NOT NULL,
    expires TEXT NOT NULL,
    seen TEXT NOT NULL,
    user_agent TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS sessions_user ON sessions(user_id);

CREATE TABLE IF NOT EXISTS login_attempts (
    key TEXT PRIMARY KEY,
    count INTEGER NOT NULL DEFAULT 0,
    first TEXT NOT NULL,
    blocked_until TEXT
);

CREATE TABLE IF NOT EXISTS audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    at TEXT NOT NULL,
    actor_id INTEGER,
    action TEXT NOT NULL,
    subject TEXT NOT NULL DEFAULT '',
    detail TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS audit_at ON audit(at DESC);
"""

SCHEMA_PROGRESS = """
CREATE TABLE IF NOT EXISTS lesson_progress (
    user_id INTEGER NOT NULL,
    lesson_id TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    best REAL NOT NULL DEFAULT 0,
    last REAL NOT NULL DEFAULT 0,
    passed INTEGER NOT NULL DEFAULT 0,
    updated TEXT NOT NULL,
    PRIMARY KEY (user_id, lesson_id)
);
CREATE TABLE IF NOT EXISTS module_progress (
    user_id INTEGER NOT NULL,
    module_id TEXT NOT NULL,
    exam_attempts INTEGER NOT NULL DEFAULT 0,
    exam_best REAL NOT NULL DEFAULT 0,
    exam_passed INTEGER NOT NULL DEFAULT 0,
    skip_attempts INTEGER NOT NULL DEFAULT 0,
    skip_best REAL NOT NULL DEFAULT 0,
    skip_passed INTEGER NOT NULL DEFAULT 0,
    updated TEXT NOT NULL,
    PRIMARY KEY (user_id, module_id)
);
CREATE TABLE IF NOT EXISTS missed (
    user_id INTEGER NOT NULL,
    item_id TEXT NOT NULL,
    question TEXT NOT NULL,
    times INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (user_id, item_id)
);
CREATE TABLE IF NOT EXISTS practice (
    user_id INTEGER NOT NULL,
    drill_id TEXT NOT NULL,
    lesson_id TEXT NOT NULL,
    kind TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    passed INTEGER NOT NULL DEFAULT 0,
    updated TEXT NOT NULL,
    PRIMARY KEY (user_id, drill_id)
);
"""

STATUSES = ("pending", "approved", "rejected")
ROLES = ("learner", "admin")
PROGRESS_TABLES = ("lesson_progress", "module_progress", "missed", "practice")


def _now() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat()


def normalise_email(value: str) -> str:
    return " ".join((value or "").split()).lower()


class Store:
    """SQLite storage with one connection per thread.

    A WSGI server answers requests on several threads, and sharing one
    ``sqlite3.Connection`` across them is not safe in practice.  Each thread gets
    its own handle to the same file; WAL mode lets them read concurrently and the
    busy timeout covers the single-writer case.  Every handle is kept so
    :meth:`close` can shut them all down.
    """

    def __init__(self, path):
        self.path = pathlib.Path(path)
        if str(self.path) != ":memory:":
            self.path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._handles: list[sqlite3.Connection] = []
        self._handles_lock = threading.Lock()
        self._connection()  # opens this thread's handle and migrates the schema

    def _connection(self) -> sqlite3.Connection:
        conn = getattr(self._local, "conn", None)
        if conn is None:
            conn = sqlite3.connect(str(self.path), check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode = WAL")
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("PRAGMA busy_timeout = 5000")
            self._local.conn = conn
            with self._handles_lock:
                self._handles.append(conn)
            self._migrate()
        return conn

    db = property(_connection)

    # ------------------------------------------------------------- migration
    def _table(self, name: str) -> bool:
        row = self.db.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (name,)
        ).fetchone()
        return bool(row)

    def _columns(self, table: str) -> set[str]:
        return {row["name"] for row in self.db.execute("PRAGMA table_info(%s)" % table)}

    def _migrate(self) -> None:
        """Bring any older database up to the account schema, without data loss."""
        self.db.executescript(SCHEMA_ACCOUNTS)

        if self._table("learners"):
            columns = self._columns("learners")
            course = "course" if "course" in columns else "'pybook'"
            language = "language" if "language" in columns else "'hinglish'"
            self.db.execute(
                "INSERT INTO users (id, name, email, password_hash, status, role, goal, "
                "language, course, created) "
                "SELECT id, name, NULL, NULL, 'approved', 'learner', '', %s, %s, created "
                "FROM learners" % (language, course)
            )
            self.db.execute("DROP TABLE learners")

        for table in PROGRESS_TABLES:
            if self._table(table) and "learner_id" in self._columns(table):
                self.db.execute(
                    "ALTER TABLE %s RENAME COLUMN learner_id TO user_id" % table
                )

        self.db.executescript(SCHEMA_PROGRESS)

        # A database from the very first build has no `course` on users.
        if "course" not in self._columns("users"):
            self.db.execute(
                "ALTER TABLE users ADD COLUMN course TEXT NOT NULL DEFAULT 'pybook'"
            )
        self.db.commit()

    def close(self) -> None:
        with self._handles_lock:
            handles, self._handles = self._handles, []
        for conn in handles:
            try:
                conn.close()
            except sqlite3.Error:
                pass
        self._local = threading.local()

    # ---------------------------------------------------------------- accounts
    def create_account(
        self,
        name: str,
        email: str,
        password_hash: str,
        language: str = "hinglish",
        course: str = "pybook",
        goal: str = "",
        status: str = "pending",
        role: str = "learner",
    ) -> dict | None:
        """Create one account. Returns ``None`` when the email is already used."""
        clean = " ".join((name or "").split())[:60] or "Learner"
        address = normalise_email(email)
        try:
            cursor = self.db.execute(
                "INSERT INTO users (name, email, password_hash, status, role, goal, "
                "language, course, created) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    clean,
                    address,
                    password_hash,
                    status if status in STATUSES else "pending",
                    role if role in ROLES else "learner",
                    (goal or "").strip()[:500],
                    language,
                    course,
                    _now(),
                ),
            )
        except sqlite3.IntegrityError:
            return None
        self.db.commit()
        return self.user_by_id(cursor.lastrowid)

    def user_by_email(self, email: str):
        address = normalise_email(email)
        if not address:
            return None
        row = self.db.execute("SELECT * FROM users WHERE email = ?", (address,)).fetchone()
        return dict(row) if row else None

    def user_by_id(self, user_id: int):
        row = self.db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None

    def set_password(self, user_id: int, password_hash: str) -> None:
        self.db.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id)
        )
        self.db.commit()

    def set_language(self, user_id: int, language: str) -> None:
        self.db.execute("UPDATE users SET language = ? WHERE id = ?", (language, user_id))
        self.db.commit()

    def set_course(self, user_id: int, course: str) -> None:
        self.db.execute("UPDATE users SET course = ? WHERE id = ?", (course, user_id))
        self.db.commit()

    def set_status(
        self,
        user_id: int,
        status: str,
        actor_id: int | None = None,
        note: str = "",
    ) -> None:
        if status not in STATUSES:
            raise ValueError("unknown status: %s" % status)
        self.db.execute(
            "UPDATE users SET status = ?, decided_at = ?, decided_by = ?, decision_note = ? "
            "WHERE id = ?",
            (status, _now(), actor_id, (note or "").strip()[:500], user_id),
        )
        self.db.commit()

    def pending_users(self) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM users WHERE status = 'pending' ORDER BY created, id"
        ).fetchall()
        return [dict(row) for row in rows]

    def users(self, status: str | None = None, query: str = "", role: str = "") -> list[dict]:
        """The roster, with last-seen and passed counts for the admin table."""
        clauses: list[str] = []
        params: list = []
        if status in STATUSES:
            clauses.append("u.status = ?")
            params.append(status)
        if role in ROLES:
            clauses.append("u.role = ?")
            params.append(role)
        text = " ".join((query or "").split())
        if text:
            like = "%" + text.replace("%", "").replace("_", "") + "%"
            clauses.append("(u.name LIKE ? OR u.email LIKE ?)")
            params.extend([like, like])
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        rows = self.db.execute(
            "SELECT u.*, "
            "(SELECT MAX(s.seen) FROM sessions s WHERE s.user_id = u.id) AS last_seen, "
            "(SELECT COUNT(*) FROM lesson_progress p "
            " WHERE p.user_id = u.id AND p.passed = 1) AS lessons_passed, "
            "(SELECT COUNT(*) FROM module_progress m "
            " WHERE m.user_id = u.id AND (m.exam_passed = 1 OR m.skip_passed = 1)) AS modules_passed "
            "FROM users u" + where + " ORDER BY u.created DESC, u.id DESC",
            params,
        ).fetchall()
        return [dict(row) for row in rows]

    def sessions_for_user(self, user_id: int) -> list[dict]:
        """Open sessions, newest activity first. Never exposes the token or its hash."""
        rows = self.db.execute(
            "SELECT created, expires, seen, user_agent FROM sessions "
            "WHERE user_id = ? ORDER BY seen DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def audit_for_subject(self, subject: str, limit: int = 40) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM audit WHERE subject = ? ORDER BY id DESC LIMIT ?",
            ((subject or "").strip()[:120], limit),
        ).fetchall()
        return [dict(row) for row in rows]

    def audit_page(self, action: str = "", limit: int = 120) -> list[dict]:
        if action:
            rows = self.db.execute(
                "SELECT * FROM audit WHERE action LIKE ? ORDER BY id DESC LIMIT ?",
                (action.replace("%", "") + "%", limit),
            ).fetchall()
        else:
            rows = self.db.execute(
                "SELECT * FROM audit ORDER BY id DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def signups_per_day(self, days: int = 14) -> list[dict]:
        """A dense day-by-day series, so the chart has no gaps to hide."""
        days = max(1, min(int(days), 90))
        today = _dt.date.today()
        start = (today - _dt.timedelta(days=days - 1)).isoformat()
        rows = self.db.execute(
            "SELECT substr(created, 1, 10) AS day, COUNT(*) AS n FROM users "
            "WHERE created >= ? GROUP BY day",
            (start,),
        ).fetchall()
        seen = {row["day"]: int(row["n"]) for row in rows}
        series = []
        for offset in range(days):
            day = (today - _dt.timedelta(days=days - 1 - offset)).isoformat()
            series.append({"day": day, "n": seen.get(day, 0)})
        return series

    def counts(self) -> dict:
        row = self.db.execute(
            "SELECT "
            "COUNT(*) AS total, "
            "SUM(status = 'pending') AS pending, "
            "SUM(status = 'approved') AS approved, "
            "SUM(status = 'rejected') AS rejected "
            "FROM users"
        ).fetchone()
        data = {key: int(row[key] or 0) for key in ("total", "pending", "approved", "rejected")}
        active = self.db.execute(
            "SELECT COUNT(DISTINCT user_id) FROM sessions WHERE seen >= ?",
            ((_dt.datetime.now() - _dt.timedelta(days=7)).replace(microsecond=0).isoformat(),),
        ).fetchone()[0]
        data["active_7d"] = int(active or 0)
        return data

    def promote(self, user_id: int) -> None:
        self.db.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
        self.db.commit()

    def set_role(self, user_id: int, role: str) -> None:
        if role not in ROLES:
            raise ValueError("unknown role: %s" % role)
        self.db.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
        self.db.commit()

    # ---------------------------------------------------------------- sessions
    def create_session(
        self, user_id: int, token_hash: str, expires: str, user_agent: str = ""
    ) -> None:
        self.db.execute(
            "INSERT INTO sessions (token_hash, user_id, created, expires, seen, user_agent) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (token_hash, user_id, _now(), expires, _now(), (user_agent or "")[:250]),
        )
        self.db.commit()

    def session_user(self, token_hash: str):
        """The account behind a live session token hash, or ``None``."""
        if not token_hash:
            return None
        row = self.db.execute(
            "SELECT s.expires, u.* FROM sessions s JOIN users u ON u.id = s.user_id "
            "WHERE s.token_hash = ?",
            (token_hash,),
        ).fetchone()
        if not row:
            return None
        if _dt.datetime.fromisoformat(row["expires"]) <= _dt.datetime.now():
            self.delete_session(token_hash)
            return None
        return dict(row)

    def touch_session(self, token_hash: str) -> None:
        self.db.execute(
            "UPDATE sessions SET seen = ? WHERE token_hash = ?", (_now(), token_hash)
        )
        self.db.commit()

    def delete_session(self, token_hash: str) -> None:
        self.db.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
        self.db.commit()

    def delete_sessions_for_user(self, user_id: int) -> None:
        self.db.execute("DELETE FROM sessions WHERE user_id = ?", (user_id,))
        self.db.commit()

    def purge_expired_sessions(self) -> int:
        cursor = self.db.execute(
            "DELETE FROM sessions WHERE expires <= ?", (_now(),)
        )
        self.db.commit()
        return cursor.rowcount

    # -------------------------------------------------------------- throttling
    def attempt(self, key: str):
        row = self.db.execute("SELECT * FROM login_attempts WHERE key = ?", (key,)).fetchone()
        return dict(row) if row else None

    def record_failure(
        self, key: str, limit: int, window_seconds: int, lock_seconds: int
    ) -> dict:
        """Count one failure; start a lockout once ``limit`` is reached."""
        now = _dt.datetime.now().replace(microsecond=0)
        row = self.attempt(key)
        if row is None or (
            _dt.datetime.fromisoformat(row["first"])
            < now - _dt.timedelta(seconds=window_seconds)
        ):
            count, first = 1, now
        else:
            count, first = row["count"] + 1, _dt.datetime.fromisoformat(row["first"])
        blocked = (
            (now + _dt.timedelta(seconds=lock_seconds)).isoformat() if count >= limit else None
        )
        self.db.execute(
            "INSERT INTO login_attempts (key, count, first, blocked_until) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(key) DO UPDATE SET count = excluded.count, "
            "first = excluded.first, blocked_until = excluded.blocked_until",
            (key, count, first.isoformat(), blocked),
        )
        self.db.commit()
        return {"count": count, "blocked_until": blocked}

    def clear_failures(self, key: str) -> None:
        self.db.execute("DELETE FROM login_attempts WHERE key = ?", (key,))
        self.db.commit()

    def purge_attempts(self, older_than_days: int = 7) -> int:
        """Drop counters that are old and no longer blocking, so the table stays small."""
        cutoff = (_dt.datetime.now() - _dt.timedelta(days=older_than_days)).replace(
            microsecond=0
        ).isoformat()
        cursor = self.db.execute(
            "DELETE FROM login_attempts WHERE first < ? "
            "AND (blocked_until IS NULL OR blocked_until < ?)",
            (cutoff, _now()),
        )
        self.db.commit()
        return cursor.rowcount

    @staticmethod
    def blocked_until(row) -> str | None:
        """The lockout expiry of an attempt row, if it is still in the future."""
        if not row or not row.get("blocked_until"):
            return None
        until = _dt.datetime.fromisoformat(row["blocked_until"])
        return row["blocked_until"] if until > _dt.datetime.now() else None

    # ------------------------------------------------------------------- audit
    def audit(self, actor_id, action: str, subject: str = "", detail: str = "") -> None:
        self.db.execute(
            "INSERT INTO audit (at, actor_id, action, subject, detail) VALUES (?, ?, ?, ?, ?)",
            (_now(), actor_id, action, subject[:120], detail[:500]),
        )
        self.db.commit()

    def recent_audit(self, limit: int = 20) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM audit ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(row) for row in rows]

    # ----------------------------------------------------------------- lessons
    def lessons(self, user_id: int) -> dict[str, dict]:
        rows = self.db.execute(
            "SELECT * FROM lesson_progress WHERE user_id = ?", (user_id,)
        ).fetchall()
        return {row["lesson_id"]: dict(row) for row in rows}

    def record_lesson(
        self, user_id: int, lesson_id: str, score: float, passed: bool, missed: list[dict]
    ) -> None:
        row = self.db.execute(
            "SELECT * FROM lesson_progress WHERE user_id = ? AND lesson_id = ?",
            (user_id, lesson_id),
        ).fetchone()
        if row:
            self.db.execute(
                "UPDATE lesson_progress SET attempts = ?, best = ?, last = ?, passed = ?, "
                "updated = ? WHERE user_id = ? AND lesson_id = ?",
                (
                    row["attempts"] + 1,
                    max(row["best"], score),
                    score,
                    1 if (passed or row["passed"]) else 0,
                    _now(),
                    user_id,
                    lesson_id,
                ),
            )
        else:
            self.db.execute(
                "INSERT INTO lesson_progress (user_id, lesson_id, attempts, best, last, "
                "passed, updated) VALUES (?, ?, 1, ?, ?, ?, ?)",
                (user_id, lesson_id, score, score, 1 if passed else 0, _now()),
            )
        for item in missed:
            existing = self.db.execute(
                "SELECT times FROM missed WHERE user_id = ? AND item_id = ?",
                (user_id, item["id"]),
            ).fetchone()
            if existing:
                self.db.execute(
                    "UPDATE missed SET times = times + 1 WHERE user_id = ? AND item_id = ?",
                    (user_id, item["id"]),
                )
            else:
                self.db.execute(
                    "INSERT INTO missed (user_id, item_id, question, times) VALUES (?, ?, ?, 1)",
                    (user_id, item["id"], item["question"][:200]),
                )
        self.db.commit()

    def mark_lessons_passed(self, user_id: int, lesson_ids: list[str]) -> None:
        for lesson_id in lesson_ids:
            row = self.db.execute(
                "SELECT * FROM lesson_progress WHERE user_id = ? AND lesson_id = ?",
                (user_id, lesson_id),
            ).fetchone()
            if row:
                self.db.execute(
                    "UPDATE lesson_progress SET passed = 1, updated = ? "
                    "WHERE user_id = ? AND lesson_id = ?",
                    (_now(), user_id, lesson_id),
                )
            else:
                self.db.execute(
                    "INSERT INTO lesson_progress (user_id, lesson_id, attempts, best, last, "
                    "passed, updated) VALUES (?, ?, 0, 0, 0, 1, ?)",
                    (user_id, lesson_id, _now()),
                )
        self.db.commit()

    # ----------------------------------------------------------------- modules
    def modules(self, user_id: int) -> dict[str, dict]:
        rows = self.db.execute(
            "SELECT * FROM module_progress WHERE user_id = ?", (user_id,)
        ).fetchall()
        return {row["module_id"]: dict(row) for row in rows}

    def record_module(
        self, user_id: int, module_id: str, kind: str, score: float, passed: bool
    ) -> None:
        assert kind in ("exam", "skip")
        row = self.db.execute(
            "SELECT * FROM module_progress WHERE user_id = ? AND module_id = ?",
            (user_id, module_id),
        ).fetchone()
        if not row:
            self.db.execute(
                "INSERT INTO module_progress (user_id, module_id, updated) VALUES (?, ?, ?)",
                (user_id, module_id, _now()),
            )
            row = self.db.execute(
                "SELECT * FROM module_progress WHERE user_id = ? AND module_id = ?",
                (user_id, module_id),
            ).fetchone()
        attempts = row[kind + "_attempts"] + 1
        best = max(row[kind + "_best"], score)
        done = 1 if (passed or row[kind + "_passed"]) else 0
        self.db.execute(
            "UPDATE module_progress SET %s_attempts = ?, %s_best = ?, %s_passed = ?, updated = ? "
            "WHERE user_id = ? AND module_id = ?" % (kind, kind, kind),
            (attempts, best, done, _now(), user_id, module_id),
        )
        self.db.commit()

    # ---------------------------------------------------------------- practice
    def practice(self, user_id: int) -> dict[str, dict]:
        rows = self.db.execute(
            "SELECT * FROM practice WHERE user_id = ?", (user_id,)
        ).fetchall()
        return {row["drill_id"]: dict(row) for row in rows}

    def record_practice(
        self, user_id: int, drill_id: str, lesson_id: str, kind: str, passed: bool
    ) -> None:
        row = self.db.execute(
            "SELECT * FROM practice WHERE user_id = ? AND drill_id = ?",
            (user_id, drill_id),
        ).fetchone()
        if row:
            self.db.execute(
                "UPDATE practice SET attempts = ?, passed = ?, updated = ? "
                "WHERE user_id = ? AND drill_id = ?",
                (
                    row["attempts"] + 1,
                    1 if (passed or row["passed"]) else 0,
                    _now(),
                    user_id,
                    drill_id,
                ),
            )
        else:
            self.db.execute(
                "INSERT INTO practice (user_id, drill_id, lesson_id, kind, attempts, passed, updated) "
                "VALUES (?, ?, ?, ?, 1, ?, ?)",
                (user_id, drill_id, lesson_id, kind, 1 if passed else 0, _now()),
            )
        self.db.commit()

    # ------------------------------------------------------------------- extra
    def missed(self, user_id: int) -> list[dict]:
        rows = self.db.execute(
            "SELECT * FROM missed WHERE user_id = ? ORDER BY times DESC, item_id",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]

    def reset(self, user_id: int) -> None:
        for table in PROGRESS_TABLES:
            self.db.execute("DELETE FROM %s WHERE user_id = ?" % table, (user_id,))
        self.db.commit()

    def export(self, user_id: int) -> dict:
        account = self.user_by_id(user_id) or {}
        return {
            "learner": {"name": account.get("name", ""), "email": account.get("email", "")},
            "lessons": self.lessons(user_id),
            "modules": self.modules(user_id),
            "practice": self.practice(user_id),
            "missed": self.missed(user_id),
        }
