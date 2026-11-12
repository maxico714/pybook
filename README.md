# 🐍 PyBook — Python and AI engineering, learned by doing

Two products, one curriculum, one local machine:

| Product | For | What it is |
|---|---|---|
| **`PyBook.ipynb`** | one learner, one file | A self-contained Jupyter notebook: 53 lessons, 12 modules, 230 authored questions, every Python keyword. No account, no internet. |
| **The web platform** (`run.py`) | a small class or a self-hosted learner | A Flask app with real accounts, admin approval, two courses, per-account progress in SQLite, a code sandbox and a playground. |

Both read the same generated data in `pybook/data/`, so a lesson is written once
and appears in both. The notebook is the "give me one file" product; the web app
is the "I want accounts and saved progress" product.

```
PyBook.ipynb      ← open this if you want the single-file course
python run.py     ← run this if you want the platform with accounts
```

---

# Part 1 — the notebook

A single, self-contained notebook that teaches the whole Python core:
**53 lessons, 12 modules, 26 chapters, 230 authored quiz questions**, every one of
the 35 Python keywords, and a lock on every lesson until the previous one is
passed.

## What a lesson looks like

1. **Intro** — what the concept is, in plain language.
2. **Real-life example** — a shop, a kitchen, a ticket counter; not `foo`/`bar`.
3. **Code** — two or three runnable examples, each with the output it really
   produces printed underneath.
4. **Practice** — at least one exercise with an automated checker, plus a quiz.

Then the gate: **80% on the quiz unlocks the next lesson.** A module exam
(**80%**) unlocks the next module. If you already know a module, its **skip exam**
is the union of every question in that module at **90%** — skipping is allowed,
but it is deliberately harder than learning.

## How to run the notebook

**Locally**

```bash
python -m pip install notebook    # or: pip install jupyterlab
jupyter notebook PyBook.ipynb
```

Run the first four code cells in order (data → runtime → diagrams → start).
Then `course.dashboard()` shows where you are.

**Google Colab**

Upload `PyBook.ipynb` and run the same four cells. To keep progress between
sessions, mount Drive *before* creating the course object:

```python
from google.colab import drive
drive.mount("/content/drive")
```

Progress then lives at `/content/drive/MyDrive/PyBook/progress.json`. Without
Drive it lives next to the notebook and disappears when the runtime resets — use
`course.export_progress()` to keep a copy.

## The commands you will actually use

| Command | What it does |
|---|---|
| `course.dashboard()` | progress for every module and lesson |
| `course.lesson("m03c01l02")` | render one lesson |
| `course.quiz("m03c01l02", {"q1": "b", "q2": "a", "q3": "c"})` | answer the quiz |
| `course.check("m03c01l02e1", "your code")` | run your exercise code against the checks |
| `course.exam("m03", {...})` | module exam, 80% to unlock the next module |
| `course.skip_exam("m03", {...})` | skip exam, 90%, marks the module done |
| `course.next()` | the next thing you are allowed to do |
| `course.review()` | questions you got wrong, for revision |
| `course.set_language("en" \| "hi" \| "hinglish")` | explanation language |
| `course.export_progress()` / `course.import_progress(text)` | move progress between machines |
| `course.reset(confirm=True)` | start over |

---

# Part 2 — the web platform

A local Flask app over the same curriculum, with **two courses** and **real
accounts**.

* **Python** — 53 lessons, 12 modules, 26 chapters.
* **AI Engineering** — 23 lessons, 5 modules, 43 runnable examples, 69 quiz items,
  30 exam items. Written in Hinglish and English; Hindi falls back to Hinglish.

## The account flow (exactly as specified)

```
visitor → homepage (site + course enquiry) → sign up
        → request saved as `pending`
        → appears in Admin → "New account requests"
        → admin approves (or rejects)
        → login works; a pending or rejected account gets a clear message instead
        → session persists across browser restarts
        → progress is stored per account, per course
```

Nothing about a lesson is reachable without a session: every page and every
`/api/*` endpoint is behind a login, and a locked lesson is a `403` that renders a
lock card, never its content.

## First run

```bash
python -m pip install -r requirements.txt   # Flask + waitress

# 1. the curriculum data (already committed; rebuild only if you edit course/)
python build_notebook.py
python -m pybook.build_ai_course

# 2. create the first admin — without one, nobody can approve a sign-up
python -m web.manage create-admin --email you@example.com --name "Your Name"

# 3. serve it
python run.py                 # http://127.0.0.1:5000
python run.py --check         # verify data, database and that an admin exists
```

`waitress` is used automatically when it is installed. Without it, `run.py` says
plainly that Flask's development server is running — fine for a classroom on your
own machine, not hardened for the public internet.

Then open the site, sign up as a learner, approve yourself from
**Admin → New account requests**, and log in.

## Managing accounts

```bash
python -m web.manage list                       # every account and its status
python -m web.manage approve --email a@b.com    # approve without the browser
python -m web.manage promote --email a@b.com    # make an account an admin
python -m web.manage set-password --email a@b.com
```

Passwords are typed at a hidden prompt (or piped with `--password-stdin`, so they
never appear in the process list or shell history). `set-password` also revokes
that account's open sessions.

## The admin panel

`/admin` is a real back office, not a page of buttons:

| Page | What it does |
|---|---|
| **Dashboard** | Counts, the waiting queue with approve/reject inline, a 14-day signup chart drawn from the database, and the newest audit rows |
| **Requests** | One card per sign-up: who, which course, language, goal, and an optional note stored with the decision |
| **Accounts** | Search by name or email, filter by status and role, see passed lessons/modules and last-seen, approve or revoke in place |
| **Account detail** | Per-course progress bars, open sessions with device and timestamps, the account's own history, and the actions: approve, revoke, promote/demote, sign out everywhere, set a new password |
| **Audit trail** | Every signup, login, failure, decision, role change and password change, filterable by kind |

An admin cannot reject, demote or deactivate their own account, so one admin
cannot lock the panel out. Every action is a CSRF-protected POST and writes an
audit row with the acting account id.

Because there is no email delivery, a forgotten password is reset by an admin
from the account page (or from the command line with `set-password`).

**Upgrading an old database.** A database from the pre-account build has a
`learners` table. On first start it is migrated automatically: rows become
`approved` accounts with the same id, and every progress table is renamed from
`learner_id` to `user_id`, so no progress is lost. Those migrated rows have no
email or password yet, so they cannot log in until you claim them:

```bash
python -m web.manage claim --id 1 --email you@example.com --name "Your Name" --admin
```

## The AI Engineering course

| Module | Title | Lessons |
|---|---|---|
| ai-m01 | Foundations — setup, tooling, Python for AI, math, data, databases | 5 |
| ai-m02 | ML and deep learning — the loop, a net from scratch, evaluation | 3 |
| ai-m03 | LLM engineering — prompts, RAG, tools, agents, evals, cost | 6 |
| ai-m04 | Specialisation and production — fine-tuning, inference, safety, observability, deployment | 7 |
| ai-m05 | Career and capstones — portfolio, interviews, two capstones | 2 |

Every example's printed `output` in the data files is **real stdout**, recorded by
`pybook/build_ai_course.py` when it ran the code; the builder aborts if any
exercise solution fails its own checks. That is why the lesson pages can promise
"this is what it prints".

## Gating, in the web app

* The **practice task gates the quiz**: the quiz stays locked until the lesson's
  practice exercise passes its checks in the sandbox.
* **Optional drills** never gate anything; they only add XP.
* Lessons unlock **in order**, per course. Module exams need every lesson in the
  module passed first (the API refuses, not just the page).
* The **skip exam** is the union of every quiz item in the module plus the module
  exam, at 90% — a 2-lesson module does not require a perfect score.
* Switching course keeps each course's progress separate, in the same account.

## Security — what is actually implemented

| Concern | Implementation |
|---|---|
| Passwords | Werkzeug **scrypt** hashes; a policy rejects short, common, repeated, email- or name-based passwords |
| Sessions | Server-side rows; the cookie holds a random token and the database stores only its **SHA-256 hash**, so a stolen database cannot be replayed as a login. Logout, rejection and password change revoke sessions immediately |
| Persistence | `Max-Age` 30 days, `HttpOnly`, `SameSite=Lax`, `Secure` when `PYBOOK_SECURE_COOKIES=1` |
| CSRF | Token in the signed session for HTML forms; JSON `/api` calls are same-origin checked via `Origin`/`Referer` |
| Login throttling | 5 failures per `email\|ip` in 15 minutes locks that pair for 15 minutes — one attacker cannot lock a real user out from another address |
| Sign-up throttling | 10 new accounts per address per hour; the next request is a `429` and creates no row |
| Authorisation | `login_required` on every learner page and API; `admin_required` on the whole `/admin` blueprint; an admin cannot reject or demote their own account |
| Headers | CSP, `X-Content-Type-Options`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy` |
| Audit | Signup, login, failure, approve, reject, status change, password change and reset are written to an `audit` table shown in the admin panel |
| Secrets | `PYBOOK_SECRET_KEY` from the environment, else a random key generated once into `instance/secret_key` (mode 600) |
| Upload size | `MAX_CONTENT_LENGTH` 1 MB, with a real `413` page |

**The honest caveat about CSP.** The content policy is `'self'` for everything
except `script-src`/`style-src`, which need `'unsafe-inline'` and `'unsafe-eval'`
because Alpine.js evaluates its expressions with `new Function`. Without that the
interactive parts do not run. Everything else is locked down: no CDN, no remote
font, no third-party script, no telemetry. The trade-off is documented here rather
than hidden.

**Sandbox limits.** Learner code runs in a separate Python subprocess with a
module allow-list and blocked builtins/attributes, a timeout and a memory cap. It
is a classroom sandbox, **not** a security boundary against a determined attacker:
run the platform for people you would let run code on a shared machine, and do not
expose it publicly without OS-level isolation (container, separate user, seccomp).

## Languages

`hinglish` (default), `hi`, `en`. The fallback chain is *requested language →
hinglish → English*, so a missing translation never leaves a blank lesson. Code
stays in English on purpose: that is what real code looks like. The AI course is
authored in Hinglish and English, so `hi` shows the Hinglish text there — by
design, and stated on the lesson page rather than silently machine-translated.

## Curriculum (Python)

| Module | Title | Lessons |
|---|---|---|
| m01 | Starting Out — first program, expressions, variables, numbers, strings, `True`/`False`/`None` | 6 |
| m02 | Working with Data — indexing, slicing, string methods, comparisons, `is`/`==`/`del`, division | 5 |
| m03 | Decisions and Loops — `if`/`elif`/`else`, `match`/`case`, `while`/`break`/`continue`/`pass`, `for`/`range`/`enumerate`/`zip` | 5 |
| m04 | Collections — lists, sorting, tuples, dicts, nested data, sets | 6 |
| m05 | Functions — `def`/`return`, defaults/`*args`/`**kwargs`, scope, `lambda`, recursion | 5 |
| m06 | Errors and Exceptions — `try`/`except`/`else`/`finally`, `raise`/`assert`, custom exceptions | 3 |
| m07 | Modules, Imports and Files — `import`/`from`/`as`, `with`, text files, JSON and paths | 4 |
| m08 | Classes and Objects — `class`/`__init__`/`self`, attributes, inheritance, dunders and dataclasses | 4 |
| m09 | Comprehensions and Generators — comprehensions, iterators, `yield` | 3 |
| m10 | Modern Python — type hints and `type` aliases, closures, decorators, structural matching | 4 |
| m11 | The Standard Library Toolbox — `math`/`random`/`statistics`, dates, `collections`, `itertools`/`functools` | 4 |
| m12 | Real Projects — `async`/`await`, CSV, testing with `unittest`, a complete expense tracker | 4 |

Every lesson links its official source under **Official docs**
(`docs.python.org/3/...`), and the curriculum was checked against the Python 3.12
tutorial and language reference.

## Verification — what is actually proven

Run these yourself; the numbers below are from a real run on Python 3.12.10.

```bash
python -m course.selfcheck          # executes every example and exercise
python -m pytest tests -q           # 175 tests
python build_notebook.py            # regenerates PyBook.ipynb
python -m pybook.build_ai_course    # regenerates the AI course data
python run.py --check               # data, database, admin account
```

* `course.selfcheck` runs **all 120 code examples** and **53 exercises** and
  compares the real stdout with the output printed in the lesson, byte for byte.
  It also checks every quiz item has four distinct options and a valid answer.
* `tests/test_notebook.py` opens the shipped `.ipynb`, executes its setup cells in
  a fresh namespace **without importing the project**, then completes all 53
  lessons and all 12 module exams through the embedded runtime, saves progress,
  reloads it, switches language, and round-trips `export_progress`. One test also
  runs **every code cell of the notebook top to bottom** in a single namespace,
  which is exactly what a learner does with *Run all*.
* `tests/test_content.py` proves all 35 keywords are taught, every lesson has the
  four parts, and the notebook on disk is identical to what the generator builds
  (so the artefact cannot drift from the source).
* `tests/test_ai_course.py` proves the AI course's shape (23 lessons, 5 modules),
  that ids never collide with the Python course, that every solution passes, and
  that **every example's recorded output equals a real run**. It also plays the
  whole course through the API, including the practice gate and the module exams.
* `tests/test_accounts.py` proves the account flow end to end: signup is
  `pending`, a pending account cannot log in, an admin approves it, then login
  works; a rejected account is refused and loses its open session; the session
  survives a new client and dies on logout; the database stores a hash rather than
  a password or a raw token; CSRF and cross-site requests are refused; five wrong
  passwords lock the pair; and an old `learners` database migrates with its
  progress intact.
* The platform was also driven through a **real browser**: signup → admin approve
  → login → locked and unlocked lessons → practice gate → course switch →
  logout → second account login, with **no console errors** and only local assets
  requested.

## Deploying on Render

`render.yaml` is a blueprint for a **free** web service. Point Render at the
repository and it uses these values:

| Field | Value |
|---|---|
| Root directory | *(empty - the repo root)* |
| Build command | `pip install -r requirements.txt` |
| Start command | `python run.py` |
| Health check path | `/healthz` |
| Environment | `PYTHON_VERSION=3.12.10`, `PYBOOK_SECRET_KEY` (generated), `PYBOOK_SECURE_COOKIES=1`, `PYBOOK_ADMIN_EMAIL`, `PYBOOK_ADMIN_PASSWORD`, `PYBOOK_ADMIN_NAME` |

`python run.py` reads the `PORT` variable that Render injects and binds
`0.0.0.0`, so no flags are needed. The first admin is created from
`PYBOOK_ADMIN_EMAIL` / `PYBOOK_ADMIN_PASSWORD` on the first boot, because a free
service has no shell to run `python -m web.manage create-admin`. Remove those two
variables after the first successful deploy.

**The free plan has an ephemeral filesystem.** `pybook.db` is recreated on every
deploy, restart and idle spin-down, so accounts and progress do not survive them.
For data that lasts, either attach a paid persistent disk and set
`PYBOOK_DB=/data/pybook.db`, or move the store to Postgres (not implemented).
Free services also spin down after 15 minutes of inactivity and take about a
minute to wake.

## Limitations, stated honestly

* Pass scores (80 / 80 / 90) are a **design choice** for this course. They are not
  derived from a published mastery study, and nothing here claims they are.
* Examples are verified on **CPython 3.12**. A few lessons (`type X = ...`,
  `match`, `|` unions) need 3.10–3.12+; the lesson text says so where it matters.
* The `async` lesson uses `asyncio.sleep` so it runs offline; it does not call the
  network.
* The web app is **local-first**: one SQLite file, no email delivery, no password
  reset link, no OAuth. Approval is a human action in the admin panel by design.
* Sign-ups are limited to **10 per address per hour** inside the app. A public
  deployment should still add a reverse-proxy limit and an email verification
  step, because an address is not a person.
* The sandbox is a classroom sandbox, not a hardened jail (see above).
* The notebook keeps progress in a JSON file; the web app keeps it in SQLite.
  They do not sync with each other.

## Repository layout

```
course/                 the curriculum source of truth (Python)
  schema.py             data model (Lesson, Exercise, QuizItem, Course)
  content/              m01.py … m12.py + _kit.py authoring helpers
  runtime.py            the notebook runtime, embedded verbatim into the .ipynb
  visuals.py            16 original SVG diagrams (CSS animation, no external assets)
  validate.py           the rules a valid course must satisfy
  selfcheck.py          executes every example and exercise
build_notebook.py       generates PyBook.ipynb
pybook/
  data/                 generated JSON for both courses (pybook/, ai/)
  ai_lessons_a/b/c.py   the AI course, authored in three parts
  ai_syllabus.py        combines them into 23 lessons + 5 modules + exams
  build_ai_course.py    runs every example, records real output, writes data/ai
web/
  app.py                routes: public pages, learner pages, /api
  auth.py               passwords, sessions, CSRF, throttling, decorators
  store.py              SQLite schema, migration, accounts, sessions, progress
  admin.py              the /admin blueprint
  security.py           secret key + security headers
  manage.py             CLI: first admin, claim, approve, set-password
  runner.py/_worker.py  the subprocess sandbox
  templates/, static/   UI (vendored: Alpine, GSAP, Prism, CodeMirror, Chart.js)
tests/                  notebook, content, AI course, web and account tests
run.py                  serve (waitress when available) + --check
```

The notebook is a **build artefact**: never hand-edit it. Edit `course/`, then run
`python build_notebook.py`. The same rule applies to `pybook/data/ai`: edit
`pybook/ai_*.py`, then run `python -m pybook.build_ai_course`.

## Privacy

* The **notebook** makes no network calls, has no telemetry and writes one JSON
  progress file whose path `course.path` prints.
* The **web app** stores only what a signup submits — name, email, chosen course,
  language, optional goal — plus progress, sessions and an audit trail, all in one
  local SQLite file you control. No analytics, no third-party request, no email
  is ever sent. Deleting `pybook.db` deletes everything.

## Licence

MIT — see [LICENSES.md](LICENSES.md). The diagrams are original SVG authored for
this curriculum, and the vendored front-end libraries are listed there with their
licences.
