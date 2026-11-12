"""Authored lessons 1-8 of the AI-engineering course (Part A and part of B).

Explanations come from the chapter notebooks; the text here is the short,
teachable layer on top: one idea, one real-life analogy, one runnable example,
one checked exercise and three quiz items.  Everything is pure standard library
so the same sandbox that runs the Python course can run this course.
"""


def _t(hinglish: str, en: str) -> dict:
    """Two languages are authored; ``hi`` falls back to Hinglish by design."""
    return {"hinglish": hinglish, "en": en}


LESSONS = {
    1: {
        "title": _t(
            "Setup, tooling aur AI-assisted engineering",
            "Setup, tooling and AI-assisted engineering",
        ),
        "keywords": ["uv", "git", "Docker", "env", "AGENTS.md"],
        "intro": _t(
            "AI engineering ka pehla din code likhna nahi, environment banana hai: ek virtual "
            "environment, git, secrets ke liye `.env`, aur Docker ka basic idea. Reproducible setup "
            "har job aur take-home me check hota hai, aur leak hui API key sabse common rejection "
            "reason hai.",
            "Day one of AI engineering is not writing code, it is building an environment: a virtual "
            "environment, git, a `.env` for secrets, and the basic Docker idea. Reproducible setup is "
            "checked in almost every job and take-home, and a leaked API key is a common rejection "
            "reason.",
        ),
        "real_life": _t(
            "Jaise ghar ki chaabi bahar mat chhodo, waise API key code me mat likho. `.env` local "
            "rehti hai, `.gitignore` usse git se bahar rakhta hai, aur `.env.example` team ko sirf "
            "naam batata hai.",
            "You do not leave your house key outside, and you do not hard-code an API key. `.env` "
            "stays local, `.gitignore` keeps it out of git, and `.env.example` tells the team only "
            "the key names.",
        ),
        "takeaway": _t(
            "Agar naya laptop clone karke README follow karte hi sab chal jaye, setup sahi hai.",
            "If a fresh clone plus the README just works, the setup is right.",
        ),
        "example": {
            "code": (
                "lines = ['# local only', 'MODEL=\"mini\"', 'API_KEY=sk-live-123']\n"
                "settings = {}\n"
                "for line in lines:\n"
                "    if line.startswith('#') or '=' not in line:\n"
                "        continue\n"
                "    key, value = line.split('=', 1)\n"
                "    settings[key] = '***' if 'KEY' in key else value.strip('\"')\n"
                "print(settings)"
            ),
            "note": _t(
                "Comment lines skip hoti hain, aur secret wali key mask ho jati hai.",
                "Comment lines are skipped and the secret-looking key is masked.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`parse_env(text)` likho jo comment/blank lines skip kare, `KEY=VALUE` ko split kare, "
                "aur jis key me `KEY`, `TOKEN` ya `SECRET` ho uski value `***` kar de. Phir diye gaye "
                "text par chala kar `env` print karo.",
                "Write `parse_env(text)` that skips comments and blank lines, splits `KEY=VALUE`, and "
                "replaces the value with `***` when the key contains `KEY`, `TOKEN` or `SECRET`. Run "
                "it on the given text and print `env`.",
            ),
            "starter": (
                "def parse_env(text):\n"
                "    env = {}\n"
                "    # loop over lines, skip comments, split once on '='\n"
                "    return env\n\n"
                "env = parse_env('''\n"
                "# local only\n"
                "API_KEY=sk-live-123\n"
                "MODEL=\"gpt-4.1-mini\"\n"
                "LOG_LEVEL=info\n"
                "''')\n"
                "print(sorted(env))\n"
            ),
            "solution": (
                "def parse_env(text):\n"
                "    env = {}\n"
                "    for line in text.splitlines():\n"
                "        line = line.strip()\n"
                "        if not line or line.startswith('#'):\n"
                "            continue\n"
                "        key, _, value = line.partition('=')\n"
                "        key = key.strip()\n"
                "        value = value.strip().strip('\"')\n"
                "        if 'KEY' in key or 'TOKEN' in key or 'SECRET' in key:\n"
                "            value = '***'\n"
                "        env[key] = value\n"
                "    return env\n\n"
                "env = parse_env('''\n"
                "# local only\n"
                "API_KEY=sk-live-123\n"
                "MODEL=\"gpt-4.1-mini\"\n"
                "LOG_LEVEL=info\n"
                "''')\n"
                "print(sorted(env))\n"
            ),
            "checks": [
                "env['API_KEY'] == '***'",
                "env['MODEL'] == 'gpt-4.1-mini'",
                "len(env) == 3",
            ],
            "hint": _t(
                "`line.partition('=')` pehle `=` par todta hai, isliye value me `=` ho to bhi safe hai.",
                "`line.partition('=')` splits on the first `=`, so a value may contain more.",
            ),
        },
        "quiz": [
            {
                "q": _t(
                    "API key kahan rakhni chahiye?",
                    "Where should an API key live?",
                ),
                "options": [
                    "`.env` file me, jo `.gitignore` me ho",
                    "seedha Python file me constant ki tarah",
                    "README me taaki team use kar sake",
                    "git commit message me",
                ],
                "answer": "a",
                "why": _t(
                    "`.env` local rehti hai aur git se bahar; code me hard-code karna leak ka sabse aasan rasta hai.",
                    "`.env` stays local and out of git; hard-coding is the easiest way to leak a key.",
                ),
            },
            {
                "q": _t(
                    "Virtual environment ka kaam kya hai?",
                    "What does a virtual environment do?",
                ),
                "options": [
                    "Project ke packages ko system Python se alag rakhta hai",
                    "Python ko fast banata hai",
                    "API calls cache karta hai",
                    "Git branches manage karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Isolation se 'mere laptop par chalta tha' wali problem kam hoti hai.",
                    "Isolation removes most 'it worked on my machine' problems.",
                ),
            },
            {
                "q": _t(
                    "`AGENTS.md` ka role kya hai?",
                    "What is the role of `AGENTS.md`?",
                ),
                "options": [
                    "AI coding agent ko project ke rules aur commands batata hai",
                    "Python packages install karta hai",
                    "Database schema banata hai",
                    "API key store karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Ye agent ke liye project handbook hai: conventions, commands aur boundaries.",
                    "It is the project handbook for an agent: conventions, commands and boundaries.",
                ),
            },
        ],
    },
    2: {
        "title": _t("Python for AI engineering", "Python for AI engineering"),
        "keywords": ["dataclass", "typing", "pydantic", "asyncio", "pytest"],
        "intro": _t(
            "AI engineer pehle software engineer hota hai. Type hints, dataclasses, validation, "
            "async calls, retries aur tests hi daily LLM code ko reliable banate hain. Model badal "
            "jayega, ye habits nahi.",
            "An AI engineer is a software engineer first. Type hints, dataclasses, validation, async "
            "calls, retries and tests are what make daily LLM code reliable. Models change; these "
            "habits do not.",
        ),
        "real_life": _t(
            "Restaurant order ki parchi ki tarah: model, tokens aur price likhe hon to bill galat "
            "nahi hota. Bina structure ke har call ek alag dictionary hoti hai.",
            "Like a restaurant bill: when model, tokens and price are written down, the total is not "
            "wrong. Without structure every call is a different dictionary.",
        ),
        "takeaway": _t(
            "Boundary par validate karo, andar typed objects use karo.",
            "Validate at the boundary, use typed objects inside.",
        ),
        "example": {
            "code": (
                "from dataclasses import dataclass\n\n"
                "@dataclass\n"
                "class Call:\n"
                "    model: str\n"
                "    tokens_in: int\n"
                "    tokens_out: int\n\n"
                "    def cost(self, price_in=0.4, price_out=1.6):\n"
                "        return (self.tokens_in * price_in + self.tokens_out * price_out) / 1_000_000\n\n"
                "call = Call('mini', 1000, 500)\n"
                "print(call.model, round(call.cost(), 6))"
            ),
            "note": _t(
                "Price per million tokens se cost nikalna ek line ka kaam hai.",
                "Cost from per-million prices is a one-line method.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`Call` dataclass banao (`model`, `prompt_tokens`, `completion_tokens`) aur `cost()` "
                "method jo per-million prices 0.4 aur 1.6 use kare. Do calls ka total cost print karo.",
                "Build a `Call` dataclass (`model`, `prompt_tokens`, `completion_tokens`) with a "
                "`cost()` method using per-million prices 0.4 and 1.6. Print the total cost of two calls.",
            ),
            "starter": (
                "from dataclasses import dataclass\n\n"
                "@dataclass\n"
                "class Call:\n"
                "    model: str\n"
                "    prompt_tokens: int\n"
                "    completion_tokens: int\n\n"
                "    def cost(self):\n"
                "        ...\n\n"
                "calls = [Call('mini', 1000, 500), Call('mini', 2000, 1000)]\n"
                "total = sum(c.cost() for c in calls)\n"
                "print(round(total, 6))\n"
            ),
            "solution": (
                "from dataclasses import dataclass\n\n"
                "@dataclass\n"
                "class Call:\n"
                "    model: str\n"
                "    prompt_tokens: int\n"
                "    completion_tokens: int\n\n"
                "    def cost(self, price_in=0.4, price_out=1.6):\n"
                "        return (self.prompt_tokens * price_in + self.completion_tokens * price_out) / 1_000_000\n\n"
                "calls = [Call('mini', 1000, 500), Call('mini', 2000, 1000)]\n"
                "total = sum(c.cost() for c in calls)\n"
                "print(round(total, 6))\n"
            ),
            "checks": [
                "abs(total - 0.0036) < 1e-9",
                "abs(calls[0].cost() - 0.0012) < 1e-9",
            ],
            "hint": _t(
                "1000 input tokens × 0.4 / 1e6 = 0.0004; output 500 × 1.6 / 1e6 = 0.0008.",
                "1000 input tokens × 0.4 / 1e6 = 0.0004; output 500 × 1.6 / 1e6 = 0.0008.",
            ),
        },
        "quiz": [
            {
                "q": _t("Type hints ka sabse bada fayda?", "The biggest benefit of type hints?"),
                "options": [
                    "Editor aur tools galtiyan code chalne se pehle pakadte hain",
                    "Python code 2x fast ho jata hai",
                    "API key hide ho jati hai",
                    "Model automatically select ho jata hai",
                ],
                "answer": "a",
                "why": _t(
                    "Types runtime speed nahi badalte; wo galat call shapes jaldi pakadte hain.",
                    "Types do not speed up runtime; they catch wrong call shapes earlier.",
                ),
            },
            {
                "q": _t(
                    "Async (`asyncio`) kis kaam me sabse zyada fayda deta hai?",
                    "Where does async (`asyncio`) help most?",
                ),
                "options": [
                    "Kai network calls ek saath bhejna",
                    "CPU-heavy matrix multiply",
                    "Database schema design",
                    "Git history clean karna",
                ],
                "answer": "a",
                "why": _t(
                    "Waiting wale kaam overlap hote hain; CPU-bound kaam ke liye multiprocessing chahiye.",
                    "Waiting work overlaps; CPU-bound work needs multiprocessing.",
                ),
            },
            {
                "q": _t(
                    "Pydantic kis jagah lagana chahiye?",
                    "Where should pydantic be used?",
                ),
                "options": [
                    "Boundary par: user input aur LLM JSON output validate karne ke liye",
                    "Har loop ke andar performance ke liye",
                    "Sirf tests me",
                    "Git hooks me",
                ],
                "answer": "a",
                "why": _t(
                    "Validation boundary par karo; andar typed objects chalao.",
                    "Validate at boundaries; pass typed objects inside.",
                ),
            },
        ],
    },
    3: {
        "title": _t("Math aur statistics ka intuition", "Math and statistics intuition"),
        "keywords": ["vector", "cosine", "gradient", "softmax", "Bayes"],
        "intro": _t(
            "Formula yaad karne ki zaroorat nahi, intuition chahiye: vector kya hai, similarity kaise "
            "napte hain, gradient kis direction me neeche jata hai, aur probability se decision kaise "
            "nikalta hai. Loss, embeddings aur A/B tests sab isi par khade hain.",
            "You do not need memorised formulas, you need intuition: what a vector is, how similarity "
            "is measured, which way a gradient goes down, and how probability turns into a decision. "
            "Losses, embeddings and A/B tests all stand on this.",
        ),
        "real_life": _t(
            "Do gaano ki similarity: dono ke features (tempo, mood) ka angle jitna chhota, utne zyada "
            "similar. Cosine similarity bas wahi angle naapti hai.",
            "Two songs are similar when their feature arrows point the same way. Cosine similarity "
            "measures exactly that angle.",
        ),
        "takeaway": _t(
            "Cosine direction dekhta hai, magnitude nahi; isliye text embeddings me popular hai.",
            "Cosine looks at direction, not magnitude, which is why text embeddings use it.",
        ),
        "example": {
            "code": (
                "import math\n\n"
                "def cosine(a, b):\n"
                "    dot = sum(x * y for x, y in zip(a, b))\n"
                "    na = math.sqrt(sum(x * x for x in a))\n"
                "    nb = math.sqrt(sum(y * y for y in b))\n"
                "    return dot / (na * nb)\n\n"
                "print(round(cosine([1, 0], [1, 0]), 3), round(cosine([1, 0], [0, 1]), 3))"
            ),
            "note": _t(
                "Same direction = 1, perpendicular = 0, opposite = -1.",
                "Same direction = 1, perpendicular = 0, opposite = -1.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`cosine(a, b)` implement karo aur do pairs print karo: `[1, 2, 3]` vs `[2, 4, 6]`, "
                "aur `[1, 0]` vs `[0, 1]`.",
                "Implement `cosine(a, b)` and print two pairs: `[1, 2, 3]` vs `[2, 4, 6]`, and "
                "`[1, 0]` vs `[0, 1]`.",
            ),
            "starter": (
                "import math\n\n"
                "def cosine(a, b):\n"
                "    ...\n\n"
                "sim = cosine([1, 2, 3], [2, 4, 6])\n"
                "orthogonal = cosine([1, 0], [0, 1])\n"
                "print(round(sim, 3), round(orthogonal, 3))\n"
            ),
            "solution": (
                "import math\n\n"
                "def cosine(a, b):\n"
                "    dot = sum(x * y for x, y in zip(a, b))\n"
                "    na = math.sqrt(sum(x * x for x in a))\n"
                "    nb = math.sqrt(sum(y * y for y in b))\n"
                "    return dot / (na * nb)\n\n"
                "sim = cosine([1, 2, 3], [2, 4, 6])\n"
                "orthogonal = cosine([1, 0], [0, 1])\n"
                "print(round(sim, 3), round(orthogonal, 3))\n"
            ),
            "checks": [
                "abs(sim - 1.0) < 1e-9",
                "abs(orthogonal) < 1e-9",
            ],
            "hint": _t(
                "`[2, 4, 6]` `[1, 2, 3]` ka exact double hai, isliye angle 0 hai.",
                "`[2, 4, 6]` is exactly double `[1, 2, 3]`, so the angle is zero.",
            ),
        },
        "quiz": [
            {
                "q": _t("Cosine similarity 0 ka matlab?", "Cosine similarity of 0 means?"),
                "options": [
                    "Vectors perpendicular hain",
                    "Vectors bilkul same hain",
                    "Ek vector zero hai",
                    "Dono vectors negative hain",
                ],
                "answer": "a",
                "why": _t(
                    "0 angle 1 deta hai, 90 degree 0; isliye 0 ka matlab koi shared direction nahi.",
                    "Zero angle gives 1, ninety degrees gives 0, so 0 means no shared direction.",
                ),
            },
            {
                "q": _t(
                    "Gradient descent kis direction me step leta hai?",
                    "Which direction does gradient descent step?",
                ),
                "options": [
                    "Gradient ke opposite, loss kam karne ke liye",
                    "Gradient ke saath, loss badhane ke liye",
                    "Random direction me",
                    "Sirf pehle feature ki taraf",
                ],
                "answer": "a",
                "why": _t(
                    "Gradient sabse tezi se upar jata hai; opposite jane par loss girta hai.",
                    "The gradient points uphill fastest; going opposite lowers the loss.",
                ),
            },
            {
                "q": _t(
                    "Entropy kis cheez ko naapti hai?",
                    "What does entropy measure?",
                ),
                "options": [
                    "Distribution ki uncertainty",
                    "Model ki speed",
                    "Dataset ka size",
                    "API ka cost",
                ],
                "answer": "a",
                "why": _t(
                    "Jitni uncertain distribution, utni zyada entropy; cross-entropy loss isi se aata hai.",
                    "The more uncertain the distribution, the higher the entropy; cross-entropy loss comes from it.",
                ),
            },
        ],
    },
    4: {
        "title": _t("Data skills: cleaning, groupby, leakage", "Data skills: cleaning, groupby, leakage"),
        "keywords": ["groupby", "merge", "leakage", "outlier", "Parquet"],
        "intro": _t(
            "Zyada tar AI kaam data ka kaam hai. Groupby aur merge se sawaal ka jawab nikalta hai, "
            "cleaning se answer bharosemand hota hai, aur leakage se result jhootha 'great' lagta hai. "
            "Split pehle karo, EDA baad me.",
            "Most AI work is data work. Groupby and merge answer the question, cleaning makes the "
            "answer trustworthy, and leakage makes a result look falsely great. Split first, EDA after.",
        ),
        "real_life": _t(
            "Class ke marks ka average nikalna groupby hai; do sheets ko roll number par milana merge "
            "hai. Agar answer dekh kar features banao, to exam me cheating ho rahi hai — data me bhi "
            "wahi leakage hai.",
            "A class average is groupby; matching two sheets on roll number is merge. Building "
            "features after seeing the answer is cheating in an exam, and the same leakage in data.",
        ),
        "takeaway": _t(
            "Har feature ke liye poochho: kya ye value prediction ke waqt really available hogi?",
            "For every feature ask: would this value really be available at prediction time?",
        ),
        "example": {
            "code": (
                "from collections import defaultdict\n\n"
                "rows = [('Pune', 200), ('Pune', 400), ('Delhi', 300)]\n"
                "totals, counts = defaultdict(int), defaultdict(int)\n"
                "for city, amount in rows:\n"
                "    totals[city] += amount\n"
                "    counts[city] += 1\n"
                "print({city: totals[city] / counts[city] for city in totals})"
            ),
            "note": _t(
                "Do dictionaries se group mean nikalta hai; pandas isi ka shortcut hai.",
                "Two dictionaries give a group mean; pandas is the shortcut for this.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`mean_by_group(rows, key, value)` likho jo har group ka mean return kare, aur diye "
                "gaye rows par `means` print karo.",
                "Write `mean_by_group(rows, key, value)` returning each group's mean, and print "
                "`means` for the given rows.",
            ),
            "starter": (
                "rows = [\n"
                "    {'city': 'Pune', 'amount': 200},\n"
                "    {'city': 'Pune', 'amount': 400},\n"
                "    {'city': 'Delhi', 'amount': 300},\n"
                "]\n\n"
                "def mean_by_group(rows, key, value):\n"
                "    ...\n\n"
                "means = mean_by_group(rows, 'city', 'amount')\n"
                "print(means)\n"
            ),
            "solution": (
                "rows = [\n"
                "    {'city': 'Pune', 'amount': 200},\n"
                "    {'city': 'Pune', 'amount': 400},\n"
                "    {'city': 'Delhi', 'amount': 300},\n"
                "]\n\n"
                "def mean_by_group(rows, key, value):\n"
                "    totals, counts = {}, {}\n"
                "    for row in rows:\n"
                "        name = row[key]\n"
                "        totals[name] = totals.get(name, 0) + row[value]\n"
                "        counts[name] = counts.get(name, 0) + 1\n"
                "    return {name: totals[name] / counts[name] for name in totals}\n\n"
                "means = mean_by_group(rows, 'city', 'amount')\n"
                "print(means)\n"
            ),
            "checks": [
                "means['Pune'] == 300.0",
                "means['Delhi'] == 300.0",
                "len(means) == 2",
            ],
            "hint": _t(
                "Do dicts rakho: ek total ke liye, ek count ke liye.",
                "Keep two dicts: one for totals, one for counts.",
            ),
        },
        "quiz": [
            {
                "q": _t("Data leakage kya hai?", "What is data leakage?"),
                "options": [
                    "Training me aisi information aana jo prediction ke waqt available nahi hogi",
                    "Data ka file se memory me load hona",
                    "CSV ka corrupt hona",
                    "Model ka overfit hona",
                ],
                "answer": "a",
                "why": _t(
                    "Leakage se test score bahut achha lagta hai, production me wahi model fail hota hai.",
                    "Leakage makes the test score look great and the production model fail.",
                ),
            },
            {
                "q": _t(
                    "Missing values ko mean se bharne se pehle kya karna chahiye?",
                    "What should happen before filling missing values with the mean?",
                ),
                "options": [
                    "Sirf training data se mean nikaalna, test par apply karna",
                    "Poore dataset se mean nikaalna",
                    "Har row ka apna mean",
                    "Missing rows delete karna hamesha",
                ],
                "answer": "a",
                "why": _t(
                    "Poore dataset ka mean test ki information training me le aata hai.",
                    "The full-dataset mean brings test information into training.",
                ),
            },
            {
                "q": _t("Merge kis cheez par hota hai?", "What does a merge join on?"),
                "options": [
                    "Ek common key ya column",
                    "Row number",
                    "File name",
                    "Model name",
                ],
                "answer": "a",
                "why": _t(
                    "Join key decide karti hai kaunsi row kis row se milegi.",
                    "The join key decides which row matches which.",
                ),
            },
        ],
    },
    5: {
        "title": _t("Databases, SQL aur vector search", "Databases, SQL and vector search"),
        "keywords": ["JOIN", "GROUP BY", "index", "ANN", "pgvector"],
        "intro": _t(
            "SQL joins, GROUP BY aur indexes roz kaam aate hain; vector database usi idea ka AI "
            "version hai — nearest neighbours dhoondhna. Postgres + pgvector aaj ka practical default "
            "hai.",
            "SQL joins, GROUP BY and indexes are daily tools; a vector database is the AI version of "
            "the same idea, finding nearest neighbours. Postgres + pgvector is today's practical "
            "default.",
        ),
        "real_life": _t(
            "Library me book dhoondhna: index se seedha shelf par jao, poora hall mat chhaano. ANN "
            "index bhi billions vectors me se nearest wale jaldi nikalta hai.",
            "Finding a book in a library: use the index and go to the shelf instead of scanning the "
            "hall. An ANN index finds nearest vectors quickly among billions.",
        ),
        "takeaway": _t(
            "Pehle sahi schema aur index, phir fancy vector DB; 90% product SQL + ek vector column se ban jate hain.",
            "Right schema and index first, fancy vector DB later; 90% of products are SQL plus one vector column.",
        ),
        "example": {
            "code": (
                "users = {1: 'Asha', 2: 'Ravi'}\n"
                "orders = [(1, 250), (1, 150), (3, 99)]\n"
                "spend = {name: 0 for name in users.values()}\n"
                "for user_id, total in orders:\n"
                "    if user_id in users:\n"
                "        spend[users[user_id]] += total\n"
                "print(spend)"
            ),
            "note": _t(
                "Ye inner join + GROUP BY ka dictionary version hai.",
                "This is a dictionary version of inner join plus GROUP BY.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`spend_by_user(users, orders)` likho jo har user ka total spend return kare; jis user "
                "ka order nahi hai uska 0 rahe. `result` print karo.",
                "Write `spend_by_user(users, orders)` returning each user's total spend, with 0 for "
                "users without orders. Print `result`.",
            ),
            "starter": (
                "users = [{'id': 1, 'name': 'Asha'}, {'id': 2, 'name': 'Ravi'}]\n"
                "orders = [\n"
                "    {'user_id': 1, 'total': 250},\n"
                "    {'user_id': 1, 'total': 150},\n"
                "    {'user_id': 3, 'total': 99},\n"
                "]\n\n"
                "def spend_by_user(users, orders):\n"
                "    ...\n\n"
                "result = spend_by_user(users, orders)\n"
                "print(result)\n"
            ),
            "solution": (
                "users = [{'id': 1, 'name': 'Asha'}, {'id': 2, 'name': 'Ravi'}]\n"
                "orders = [\n"
                "    {'user_id': 1, 'total': 250},\n"
                "    {'user_id': 1, 'total': 150},\n"
                "    {'user_id': 3, 'total': 99},\n"
                "]\n\n"
                "def spend_by_user(users, orders):\n"
                "    spend = {user['id']: 0 for user in users}\n"
                "    for order in orders:\n"
                "        if order['user_id'] in spend:\n"
                "            spend[order['user_id']] += order['total']\n"
                "    return {user['name']: spend[user['id']] for user in users}\n\n"
                "result = spend_by_user(users, orders)\n"
                "print(result)\n"
            ),
            "checks": [
                "result['Asha'] == 400",
                "result['Ravi'] == 0",
                "len(result) == 2",
            ],
            "hint": _t(
                "LEFT JOIN ki tarah: pehle har user ko 0 se shuru karo, phir matching orders jodo.",
                "Like a LEFT JOIN: start every user at 0, then add matching orders.",
            ),
        },
        "quiz": [
            {
                "q": _t("Index kya fast karta hai?", "What does an index speed up?"),
                "options": [
                    "Filter aur lookup wali queries",
                    "Table ka insert hamesha",
                    "Backup lena",
                    "Password hashing",
                ],
                "answer": "a",
                "why": _t(
                    "Index lookup O(log n) jaisa banata hai, par har write par maintain karna padta hai.",
                    "An index makes lookups roughly O(log n) but must be maintained on writes.",
                ),
            },
            {
                "q": _t(
                    "Vector database me ANN ka matlab?",
                    "What does ANN mean in a vector database?",
                ),
                "options": [
                    "Approximate nearest neighbours — thoda approximate, bahut fast",
                    "Artificial neural network",
                    "Automatic normalisation",
                    "All new nodes",
                ],
                "answer": "a",
                "why": _t(
                    "Exact search slow hota hai; ANN index speed ke liye thodi accuracy trade karta hai.",
                    "Exact search is slow; an ANN index trades a little accuracy for speed.",
                ),
            },
            {
                "q": _t("GROUP BY kab chahiye?", "When do you need GROUP BY?"),
                "options": [
                    "Jab har group ka aggregate (count, sum, avg) chahiye",
                    "Jab sirf ek row chahiye",
                    "Jab table delete karni ho",
                    "Jab index banana ho",
                ],
                "answer": "a",
                "why": _t(
                    "GROUP BY rows ko buckets me daalta hai, aggregate har bucket par chalta hai.",
                    "GROUP BY puts rows into buckets and aggregates each bucket.",
                ),
            },
        ],
    },
    6: {
        "title": _t("Classical ML aur metrics", "Classical ML and metrics"),
        "keywords": ["baseline", "overfit", "precision", "recall", "Gini"],
        "intro": _t(
            "Sabse pehle simple baseline banao. Linear/logistic regression, trees aur forests tabhi "
            "try karo jab baseline ka gap samajh aa jaye. Model se pehle train vs test gap dekho — "
            "wahi overfit aur underfit batata hai.",
            "Build the simplest baseline first. Try linear/logistic regression, trees and forests only "
            "once you understand the gap to the baseline. Look at the train-vs-test gap before the "
            "model family; it tells you overfit from underfit.",
        ),
        "real_life": _t(
            "Doctor ka pehla check temperature aur BP hota hai, MRI baad me. Baseline model wahi "
            "pehla check hai; bina uske complex model ka score samajh nahi aata.",
            "A doctor checks temperature and BP before ordering an MRI. The baseline model is that "
            "first check; without it a complex score means nothing.",
        ),
        "takeaway": _t(
            "Metric business cost se chuno: cancer screening me recall, spam filter me precision.",
            "Choose the metric from business cost: recall for screening, precision for spam.",
        ),
        "example": {
            "code": (
                "def gini(labels):\n"
                "    p = sum(labels) / len(labels)\n"
                "    return 1 - p * p - (1 - p) * (1 - p)\n\n"
                "print(round(gini([1, 1, 1, 1]), 3), round(gini([1, 1, 0, 0]), 3))"
            ),
            "note": _t(
                "Pure node ki impurity 0, 50/50 mix ki 0.5 — tree isi ko kam karta hai.",
                "A pure node has impurity 0, a 50/50 mix has 0.5; a tree minimises this.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`best_split(rows)` likho jo 1-D data par woh threshold dhoonde jo weighted Gini "
                "impurity sabse kam kare. `cut` aur `score` print karo.",
                "Write `best_split(rows)` that finds the threshold minimising weighted Gini impurity "
                "on 1-D data. Print `cut` and `score`.",
            ),
            "starter": (
                "def gini(labels):\n"
                "    p = sum(labels) / len(labels)\n"
                "    return 1 - p * p - (1 - p) * (1 - p)\n\n"
                "def best_split(rows):\n"
                "    ...\n\n"
                "rows = [(1, 0), (2, 0), (3, 0), (8, 1), (9, 1), (10, 1)]\n"
                "cut, score = best_split(rows)\n"
                "print(cut, round(score, 3))\n"
            ),
            "solution": (
                "def gini(labels):\n"
                "    p = sum(labels) / len(labels)\n"
                "    return 1 - p * p - (1 - p) * (1 - p)\n\n"
                "def best_split(rows):\n"
                "    best = None\n"
                "    for cut in sorted({row[0] for row in rows})[:-1]:\n"
                "        left = [label for x, label in rows if x <= cut]\n"
                "        right = [label for x, label in rows if x > cut]\n"
                "        score = (len(left) * gini(left) + len(right) * gini(right)) / len(rows)\n"
                "        if best is None or score < best[1]:\n"
                "            best = (cut, score)\n"
                "    return best\n\n"
                "rows = [(1, 0), (2, 0), (3, 0), (8, 1), (9, 1), (10, 1)]\n"
                "cut, score = best_split(rows)\n"
                "print(cut, round(score, 3))\n"
            ),
            "checks": [
                "cut == 3",
                "abs(score) < 1e-9",
            ],
            "hint": _t(
                "Har unique value ke baad split try karo; weighted average = (n_left*gini_left + n_right*gini_right)/n.",
                "Try a split after every unique value; weighted average = (n_left*gini_left + n_right*gini_right)/n.",
            ),
        },
        "quiz": [
            {
                "q": _t(
                    "Train accuracy 1.0 aur test 0.72 hai. Kya problem hai?",
                    "Train accuracy is 1.0 and test is 0.72. What is the problem?",
                ),
                "options": [
                    "Overfitting — variance zyada hai",
                    "Underfitting — bias zyada hai",
                    "Data leakage",
                    "Learning rate bahut chhota hai",
                ],
                "answer": "a",
                "why": _t(
                    "Bada train-test gap variance ki nishani hai; regularize karo ya data badhao.",
                    "A large train-test gap signals variance; regularise or add data.",
                ),
            },
            {
                "q": _t(
                    "Cancer screening ke liye kaunsa metric pehle dekho?",
                    "Which metric matters first for cancer screening?",
                ),
                "options": [
                    "Recall — koi positive miss na ho",
                    "Precision — har positive sach ho",
                    "Accuracy",
                    "Training time",
                ],
                "answer": "a",
                "why": _t(
                    "Miss kiya case jaan ka risk hai; false alarm baad me test se clear hota hai.",
                    "A missed case is a health risk; a false alarm is cleared by a later test.",
                ),
            },
            {
                "q": _t(
                    "kNN se pehle scaling kyun zaroori hai?",
                    "Why scale features before kNN?",
                ),
                "options": [
                    "Distance par bade unit wala feature dominate kar jata hai",
                    "kNN sirf scaled data par chalta hai",
                    "Scaling se model train hota hai",
                    "Scaling se accuracy hamesha 100% hoti hai",
                ],
                "answer": "a",
                "why": _t(
                    "Income lakhs me aur age years me ho to distance sirf income se banti hai.",
                    "If income is in lakhs and age in years, distance is driven by income alone.",
                ),
            },
        ],
    },
    7: {
        "title": _t("Deep learning: ek neuron se training loop tak", "Deep learning: from one neuron to a training loop"),
        "keywords": ["tensor", "autograd", "learning rate", "dropout", "epoch"],
        "intro": _t(
            "Deep learning ka core chhota hai: input × weight + bias, activation, loss, gradient, step. "
            "PyTorch autograd yahi karta hai, bas GPU par aur lakhs parameters ke saath. Pehle ek "
            "neuron ko khud train karo, phir framework ka magic samajh aayega.",
            "The core of deep learning is small: input × weight + bias, activation, loss, gradient, "
            "step. PyTorch autograd does exactly this, on a GPU and with millions of parameters. "
            "Train one neuron by hand first; then the framework magic makes sense.",
        ),
        "real_life": _t(
            "AC ka thermostat: target aur current ka difference (loss) dekho, phir dial thoda ghumaao "
            "(gradient step). Learning rate = ek baar me kitna ghumana.",
            "An AC thermostat: look at the gap between target and current (loss), then turn the dial a "
            "little (gradient step). Learning rate = how far you turn per step.",
        ),
        "takeaway": _t(
            "Learning rate bahut bada = oscillate, bahut chhota = kabhi converge nahi.",
            "Too large a learning rate oscillates; too small never converges.",
        ),
        "example": {
            "code": (
                "w, b, lr = 0.0, 0.0, 0.05\n"
                "xs, ys = [1, 2, 3], [3, 5, 7]\n"
                "for _ in range(50):\n"
                "    preds = [w * x + b for x in xs]\n"
                "    dw = sum(2 * (p - y) * x for p, x, y in zip(preds, xs, ys)) / len(xs)\n"
                "    db = sum(2 * (p - y) for p, y in zip(preds, ys)) / len(xs)\n"
                "    w, b = w - lr * dw, b - lr * db\n"
                "print(round(w, 2), round(b, 2))"
            ),
            "note": _t(
                "Sirf 50 steps me weight 2 aur bias 1 ke kareeb pahunch jata hai.",
                "In 50 steps the weight and bias get close to 2 and 1.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "Same data par `w` aur `b` ko 400 steps train karo (`lr=0.01`), phir `w`, `b` aur "
                "final MSE `loss` print karo.",
                "Train `w` and `b` on the same data for 400 steps (`lr=0.01`), then print `w`, `b` "
                "and the final MSE `loss`.",
            ),
            "starter": (
                "w, b, lr = 0.0, 0.0, 0.01\n"
                "xs, ys = [1, 2, 3], [3, 5, 7]\n"
                "for _ in range(400):\n"
                "    # forward, gradients, update\n"
                "    ...\n"
                "loss = sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)\n"
                "print(round(w, 2), round(b, 2), round(loss, 4))\n"
            ),
            "solution": (
                "w, b, lr = 0.0, 0.0, 0.01\n"
                "xs, ys = [1, 2, 3], [3, 5, 7]\n"
                "for _ in range(400):\n"
                "    preds = [w * x + b for x in xs]\n"
                "    dw = sum(2 * (p - y) * x for p, x, y in zip(preds, xs, ys)) / len(xs)\n"
                "    db = sum(2 * (p - y) for p, y in zip(preds, ys)) / len(xs)\n"
                "    w, b = w - lr * dw, b - lr * db\n"
                "loss = sum((w * x + b - y) ** 2 for x, y in zip(xs, ys)) / len(xs)\n"
                "print(round(w, 2), round(b, 2), round(loss, 4))\n"
            ),
            "checks": [
                "abs(w - 2) < 0.05",
                "abs(b - 1) < 0.15",
                "loss < 0.01",
            ],
            "hint": _t(
                "Gradient: `2*(pred-y)*x` weight ke liye, `2*(pred-y)` bias ke liye, phir average.",
                "Gradient: `2*(pred-y)*x` for the weight, `2*(pred-y)` for the bias, then average.",
            ),
        },
        "quiz": [
            {
                "q": _t("Autograd kya karta hai?", "What does autograd do?"),
                "options": [
                    "Operations ka graph bana kar gradients automatically nikalta hai",
                    "Data clean karta hai",
                    "GPU memory free karta hai",
                    "Model ko deploy karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Forward pass record hota hai, backward pass chain rule se gradients deta hai.",
                    "It records the forward pass and uses the chain rule on the backward pass.",
                ),
            },
            {
                "q": _t(
                    "Learning rate bahut bada hone par kya hota hai?",
                    "What happens when the learning rate is too large?",
                ),
                "options": [
                    "Loss oscillate ya diverge karta hai",
                    "Model instantly converge karta hai",
                    "Gradients zero ho jate hain",
                    "Data leak hota hai",
                ],
                "answer": "a",
                "why": _t(
                    "Bada step minimum ke aar-paar koodta hai; chhota step slow hota hai.",
                    "A big step jumps across the minimum; a small step is slow.",
                ),
            },
            {
                "q": _t("Dropout kya karta hai?", "What does dropout do?"),
                "options": [
                    "Training me random neurons off karke overfitting kam karta hai",
                    "Har layer delete kar deta hai",
                    "Learning rate badhata hai",
                    "Dataset ko shuffle karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Network ko ek neuron par depend karne se rokta hai; inference me off rehta hai.",
                    "It stops the network relying on one neuron; it is off at inference.",
                ),
            },
        ],
    },
    8: {
        "title": _t("Transformers, attention aur embeddings", "Transformers, attention and embeddings"),
        "keywords": ["token", "embedding", "attention", "softmax", "BPE"],
        "intro": _t(
            "Transformer ka dil attention hai: har token dekhta hai kis doosre token se kitna matlab "
            "rakhta hai, aur unki values ka weighted mix leta hai. Embeddings text ko aise vector "
            "banati hain jahan similar matlab paas aata hai.",
            "The heart of a transformer is attention: every token looks at how much each other token "
            "matters and takes a weighted mix of their values. Embeddings turn text into vectors where "
            "similar meaning sits close together.",
        ),
        "real_life": _t(
            "Meeting me sabki baat sunkar apni baat bolna: query aapka sawaal hai, keys logon ke topic "
            "hain, values unki detail. Attention wahi weighting karta hai.",
            "Speaking in a meeting after listening to everyone: your query is the question, keys are "
            "people's topics, values their detail. Attention does that weighting.",
        ),
        "takeaway": _t(
            "Attention weights ka sum 1 hota hai; isliye `sqrt(d)` se scale karke softmax stable rakhte hain.",
            "Attention weights sum to 1; scaling by `sqrt(d)` keeps the softmax stable.",
        ),
        "example": {
            "code": (
                "import math\n\n"
                "q, keys = [1, 0], [[1, 0], [0, 1]]\n"
                "scores = [sum(a * b for a, b in zip(q, k)) / math.sqrt(len(q)) for k in keys]\n"
                "print([round(s, 3) for s in scores])"
            ),
            "note": _t(
                "Query pehli key se match karta hai, isliye uska score bada hai.",
                "The query matches the first key, so its score is larger.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`attention(query, keys, values)` likho jo scaled dot-product scores se softmax "
                "weights aur weighted output return kare. Dono print karo.",
                "Write `attention(query, keys, values)` returning softmax weights and the weighted "
                "output from scaled dot-product scores. Print both.",
            ),
            "starter": (
                "import math\n\n"
                "def attention(query, keys, values):\n"
                "    ...\n\n"
                "weights, out = attention([1, 0], [[1, 0], [0, 1]], [[10, 0], [0, 10]])\n"
                "print([round(w, 3) for w in weights])\n"
                "print([round(x, 3) for x in out])\n"
            ),
            "solution": (
                "import math\n\n"
                "def attention(query, keys, values):\n"
                "    scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(len(query)) for key in keys]\n"
                "    top = max(scores)\n"
                "    exps = [math.exp(s - top) for s in scores]\n"
                "    total = sum(exps)\n"
                "    weights = [e / total for e in exps]\n"
                "    out = [sum(w * v[i] for w, v in zip(weights, values)) for i in range(len(values[0]))]\n"
                "    return weights, out\n\n"
                "weights, out = attention([1, 0], [[1, 0], [0, 1]], [[10, 0], [0, 10]])\n"
                "print([round(w, 3) for w in weights])\n"
                "print([round(x, 3) for x in out])\n"
            ),
            "checks": [
                "abs(sum(weights) - 1) < 1e-9",
                "weights[0] > weights[1]",
                "abs(out[0] - 6.7) < 0.05",
            ],
            "hint": _t(
                "Scores ko `sqrt(d)` se divide karo, max ghatakar exp lo, sum se divide karo.",
                "Divide scores by `sqrt(d)`, subtract the max before exp, then divide by the sum.",
            ),
        },
        "quiz": [
            {
                "q": _t("Embedding kya hai?", "What is an embedding?"),
                "options": [
                    "Text ka dense vector jahan similar matlab paas hota hai",
                    "Database ka index",
                    "Model ka password",
                    "Token ka price",
                ],
                "answer": "a",
                "why": _t(
                    "Embedding semantic similarity ko distance me badal deti hai.",
                    "An embedding turns semantic similarity into distance.",
                ),
            },
            {
                "q": _t(
                    "Attention scores ko `sqrt(d)` se kyun divide karte hain?",
                    "Why divide attention scores by `sqrt(d)`?",
                ),
                "options": [
                    "Bade dimension par dot product bahut bada ho jata hai aur softmax saturate hota hai",
                    "Isse model chhota hota hai",
                    "Isse tokens kam ho jate hain",
                    "Ye GPU ke liye zaroori hai",
                ],
                "answer": "a",
                "why": _t(
                    "Scaling ke bina softmax ek token par chipak jata hai aur gradients mar jate hain.",
                    "Without scaling the softmax saturates on one token and gradients die.",
                ),
            },
            {
                "q": _t("BPE tokenisation kya karti hai?", "What does BPE tokenisation do?"),
                "options": [
                    "Common subwords ko tokens banati hai, rare words ko todti hai",
                    "Har word ko ek token banati hai",
                    "Text ko delete karti hai",
                    "Embeddings ko train karti hai",
                ],
                "answer": "a",
                "why": _t(
                    "Subword units se vocabulary chhota rehta hai aur rare words bhi handle hote hain.",
                    "Subword units keep the vocabulary small and still handle rare words.",
                ),
            },
        ],
    },
}
