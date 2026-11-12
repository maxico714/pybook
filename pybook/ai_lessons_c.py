"""Authored lessons 17-23 of the AI-engineering course (Part D and Part E)."""


def _t(hinglish: str, en: str) -> dict:
    return {"hinglish": hinglish, "en": en}


LESSONS = {
    17: {
        "title": _t("AI ke liye data work: annotation aur quality", "Data work for AI: annotation and quality"),
        "keywords": ["annotation", "kappa", "dedup", "synthetic", "licence"],
        "intro": _t(
            "Model se zyada data decide karta hai. Annotation guideline likho, inter-annotator "
            "agreement naapo (Cohen's kappa), duplicates hatao, aur split hygiene rakho. Synthetic "
            "data madad karta hai par filter karna zaroori hai.",
            "Data decides more than the model. Write an annotation guideline, measure inter-annotator "
            "agreement (Cohen's kappa), remove duplicates, and keep splits clean. Synthetic data helps "
            "but must be filtered.",
        ),
        "real_life": _t(
            "Do teachers ek hi answer sheet check karein to marks kitne milte hain? Kappa wahi "
            "agreement naapta hai, chance agreement ko hata kar.",
            "When two teachers mark the same answer sheet, how often do they agree? Kappa measures "
            "that agreement after removing chance.",
        ),
        "takeaway": _t(
            "Kappa 0.6 se kam ho to guideline me ambiguity hai, model me nahi.",
            "If kappa is below 0.6 the ambiguity is in the guideline, not the model.",
        ),
        "example": {
            "code": (
                "a = [1, 1, 0, 0, 1, 1, 0, 0]\n"
                "b = [1, 0, 0, 0, 1, 1, 0, 1]\n"
                "agree = sum(x == y for x, y in zip(a, b)) / len(a)\n"
                "print(round(agree, 3))"
            ),
            "note": _t(
                "Percent agreement pehla check hai; chance ko hataane ke liye kappa chahiye.",
                "Percent agreement is the first check; kappa removes chance.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`kappa(a, b)` likho (observed agreement minus expected, divided by 1 minus expected) "
                "aur `score` print karo.",
                "Write `kappa(a, b)` (observed minus expected agreement, divided by 1 minus expected) "
                "and print `score`.",
            ),
            "starter": (
                "def kappa(a, b):\n"
                "    ...\n\n"
                "score = kappa([1, 1, 0, 0, 1, 1, 0, 0], [1, 0, 0, 0, 1, 1, 0, 1])\n"
                "print(round(score, 3))\n"
            ),
            "solution": (
                "def kappa(a, b):\n"
                "    n = len(a)\n"
                "    agree = sum(1 for x, y in zip(a, b) if x == y) / n\n"
                "    pa = sum(a) / n\n"
                "    pb = sum(b) / n\n"
                "    expected = pa * pb + (1 - pa) * (1 - pb)\n"
                "    return (agree - expected) / (1 - expected)\n\n"
                "score = kappa([1, 1, 0, 0, 1, 1, 0, 0], [1, 0, 0, 0, 1, 1, 0, 1])\n"
                "print(round(score, 3))\n"
            ),
            "checks": [
                "abs(score - 0.5) < 1e-9",
            ],
            "hint": _t(
                "Expected agreement = `pa*pb + (1-pa)*(1-pb)`.",
                "Expected agreement = `pa*pb + (1-pa)*(1-pb)`.",
            ),
        },
        "quiz": [
            {
                "q": _t("Cohen's kappa kya adjust karta hai?", "What does Cohen's kappa adjust for?"),
                "options": [
                    "Chance agreement",
                    "Dataset ka size",
                    "Model ka cost",
                    "Annotation ka time",
                ],
                "answer": "a",
                "why": _t(
                    "Do log random par bhi kabhi kabhi agree karte hain; kappa usse hataata hai.",
                    "Two people sometimes agree by chance; kappa removes that.",
                ),
            },
            {
                "q": _t(
                    "Duplicate rows train aur test dono me hon to?",
                    "If duplicate rows appear in both train and test?",
                ),
                "options": [
                    "Leakage — test score jhootha achha aayega",
                    "Koi farak nahi padta",
                    "Model fast ho jata hai",
                    "Accuracy kam ho jati hai",
                ],
                "answer": "a",
                "why": _t(
                    "Model ne wahi row yaad kar li; dedup split se pehle karo.",
                    "The model memorised that row; deduplicate before splitting.",
                ),
            },
            {
                "q": _t("Synthetic data ka main risk?", "The main risk of synthetic data?"),
                "options": [
                    "Model ki galtiyan aur bias scale par copy ho jate hain",
                    "Data bahut sasta hota hai",
                    "Data hamesha balanced hota hai",
                    "Model ko GPU nahi chahiye",
                ],
                "answer": "a",
                "why": _t(
                    "Generator ki weakness dataset me chali jati hai; filter aur human check rakho.",
                    "The generator's weaknesses enter the dataset; filter and spot-check with humans.",
                ),
            },
        ],
    },
    18: {
        "title": _t("Serving aur deployment", "Serving and deployment"),
        "keywords": ["FastAPI", "Docker", "queue", "rate limit", "Ollama"],
        "intro": _t(
            "Model ko users tak pahunchana alag skill hai: FastAPI endpoint, Docker image, secrets, "
            "timeouts, retries, rate limiting aur cost. Local inference ke liye Ollama/llama.cpp, "
            "team serving ke liye vLLM.",
            "Shipping a model to users is a separate skill: a FastAPI endpoint, a Docker image, "
            "secrets, timeouts, retries, rate limiting and cost. Ollama/llama.cpp for local inference, "
            "vLLM for team serving.",
        ),
        "real_life": _t(
            "Restaurant kitchen: ek hi waiter sab order le to rush me galat order jata hai. Token "
            "bucket aur queue wahi rush manage karte hain.",
            "A restaurant kitchen: one waiter taking every order causes mistakes at rush hour. A token "
            "bucket and a queue manage that rush.",
        ),
        "takeaway": _t(
            "Har network call par timeout, har endpoint par rate limit, har deploy par rollback plan.",
            "A timeout on every network call, a rate limit on every endpoint, a rollback plan for every deploy.",
        ),
        "example": {
            "code": (
                "capacity, tokens, last = 2, 2, 0.0\n"
                "def allow(now, cost=1):\n"
                "    global tokens, last\n"
                "    tokens = min(capacity, tokens + (now - last))\n"
                "    last = now\n"
                "    if tokens >= cost:\n"
                "        tokens -= cost\n"
                "        return True\n"
                "    return False\n"
                "print([allow(t) for t in (0.0, 0.2, 1.0)])"
            ),
            "note": _t(
                "Bucket time ke saath refill hota hai; isliye turant do request ke baad teesri rukti hai.",
                "The bucket refills over time, so the third immediate request is refused.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`Bucket` class banao (`capacity=1`, `refill=1`) jisme `allow(now, cost=1)` ho. "
                "`(0.0, 0.25, 1.25)` par `decisions` print karo.",
                "Build a `Bucket` class (`capacity=1`, `refill=1`) with `allow(now, cost=1)`. Print "
                "`decisions` for `(0.0, 0.25, 1.25)`.",
            ),
            "starter": (
                "class Bucket:\n"
                "    def __init__(self, capacity=1, refill=1.0):\n"
                "        ...\n\n"
                "    def allow(self, now, cost=1):\n"
                "        ...\n\n"
                "bucket = Bucket()\n"
                "decisions = [bucket.allow(t) for t in (0.0, 0.25, 1.25)]\n"
                "print(decisions)\n"
            ),
            "solution": (
                "class Bucket:\n"
                "    def __init__(self, capacity=1, refill=1.0):\n"
                "        self.capacity = capacity\n"
                "        self.tokens = capacity\n"
                "        self.refill = refill\n"
                "        self.last = 0.0\n\n"
                "    def allow(self, now, cost=1):\n"
                "        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.refill)\n"
                "        self.last = now\n"
                "        if self.tokens >= cost:\n"
                "            self.tokens -= cost\n"
                "            return True\n"
                "        return False\n\n"
                "bucket = Bucket()\n"
                "decisions = [bucket.allow(t) for t in (0.0, 0.25, 1.25)]\n"
                "print(decisions)\n"
            ),
            "checks": [
                "decisions == [True, False, True]",
                "bucket.capacity == 1",
            ],
            "hint": _t(
                "Pehle refill karo (`min(capacity, tokens + elapsed*refill)`), phir cost check karo.",
                "Refill first (`min(capacity, tokens + elapsed*refill)`), then check the cost.",
            ),
        },
        "quiz": [
            {
                "q": _t(
                    "Async endpoint me blocking call ka asar?",
                    "What does a blocking call do in an async endpoint?",
                ),
                "options": [
                    "Poora event loop ruk jata hai, doosre requests wait karte hain",
                    "Sirf wo request slow hoti hai",
                    "Server restart ho jata hai",
                    "Kuch nahi hota",
                ],
                "answer": "a",
                "why": _t(
                    "Async me shared loop hota hai; blocking I/O ko thread ya async client me bhejo.",
                    "Async shares one loop; move blocking I/O to a thread or an async client.",
                ),
            },
            {
                "q": _t("Queue kis problem ke liye hai?", "What problem does a queue solve?"),
                "options": [
                    "Traffic spike ko absorb karke workers se process karana",
                    "Model ka size kam karna",
                    "Prompt ko chhota karna",
                    "GPU ko free karna",
                ],
                "answer": "a",
                "why": _t(
                    "Queue burst ko buffer karti hai aur retry/backpressure ka rasta deti hai.",
                    "A queue buffers bursts and gives a path for retries and backpressure.",
                ),
            },
            {
                "q": _t("Health check endpoint kyun chahiye?", "Why have a health-check endpoint?"),
                "options": [
                    "Load balancer aur deploy ko pata chale ki service zinda hai",
                    "Model ko train karne ke liye",
                    "Prompt version badalne ke liye",
                    "Logs delete karne ke liye",
                ],
                "answer": "a",
                "why": _t(
                    "Bina health check ke traffic dead instance par bhi jata hai.",
                    "Without a health check, traffic still goes to dead instances.",
                ),
            },
        ],
    },
    19: {
        "title": _t("MLOps aur LLMOps", "MLOps and LLMOps"),
        "keywords": ["registry", "drift", "canary", "rollback", "experiment"],
        "intro": _t(
            "MLOps ka kaam hai repeatable banana: experiment tracking, model aur prompt registry, "
            "drift monitoring, CI me eval, canary release aur rollback. LLMOps me prompt bhi ek "
            "versioned artifact hai.",
            "MLOps is about making work repeatable: experiment tracking, a model and prompt registry, "
            "drift monitoring, evals in CI, canary releases and rollback. In LLMOps the prompt is a "
            "versioned artifact too.",
        ),
        "real_life": _t(
            "Dawai ki batch number wali strip: kaunsi batch kab gayi, pata rehta hai, aur kharab "
            "batch wapas bulai ja sakti hai. Registry wahi batch record hai.",
            "A medicine strip with a batch number: you know which batch shipped when, and a bad batch "
            "can be recalled. A registry is that batch record.",
        ),
        "takeaway": _t(
            "Jo cheez rollback nahi kar sakte, use production me mat bhejo.",
            "If you cannot roll it back, do not ship it to production.",
        ),
        "example": {
            "code": (
                "import hashlib\n\n"
                "def version(text):\n"
                "    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]\n\n"
                "print(version('Be brief.'), version('Be brief and cite sources.'))"
            ),
            "note": _t(
                "Content hash se version banta hai; same prompt ka same version, badle to naya.",
                "A content hash gives the version: same prompt, same version; changed prompt, new version.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`register(registry, name, text)` likho jo hash version ke saath entry add kare aur "
                "version return kare; `v1`, `v2` aur rollback check print karo.",
                "Write `register(registry, name, text)` that appends a hash-versioned entry and "
                "returns the version; print `v1`, `v2` and the rollback check.",
            ),
            "starter": (
                "import hashlib\n\n"
                "def register(registry, name, text):\n"
                "    ...\n\n"
                "registry = {}\n"
                "v1 = register(registry, 'tutor', 'Be brief.')\n"
                "v2 = register(registry, 'tutor', 'Be brief and cite sources.')\n"
                "rollback = registry['tutor'][-2]['version']\n"
                "print(v1 != v2, rollback == v1)\n"
            ),
            "solution": (
                "import hashlib\n\n"
                "def register(registry, name, text):\n"
                "    version = hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]\n"
                "    registry.setdefault(name, []).append({'version': version, 'text': text})\n"
                "    return version\n\n"
                "registry = {}\n"
                "v1 = register(registry, 'tutor', 'Be brief.')\n"
                "v2 = register(registry, 'tutor', 'Be brief and cite sources.')\n"
                "rollback = registry['tutor'][-2]['version']\n"
                "print(v1 != v2, rollback == v1)\n"
            ),
            "checks": [
                "v1 != v2",
                "rollback == v1",
                "len(registry['tutor']) == 2",
            ],
            "hint": _t(
                "List me append karo; pichhla version `[-2]` par milta hai.",
                "Append to a list; the previous version is at `[-2]`.",
            ),
        },
        "quiz": [
            {
                "q": _t("Drift kya hai?", "What is drift?"),
                "options": [
                    "Input data ka distribution samay ke saath badalna",
                    "Model ka file size badhna",
                    "API ka price badhna",
                    "Prompt ka translate hona",
                ],
                "answer": "a",
                "why": _t(
                    "Real users ka data training data se alag ho jata hai; monitoring se pata chalta hai.",
                    "Real user data drifts from training data; monitoring catches it.",
                ),
            },
            {
                "q": _t("Canary release kya karta hai?", "What does a canary release do?"),
                "options": [
                    "Thoda traffic naye version par bhej kar risk kam karta hai",
                    "Saara traffic ek saath badal deta hai",
                    "Model delete kar deta hai",
                    "Prompt ko freeze karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Chhota blast radius: kharab ho to rollback sasta hota hai.",
                    "Small blast radius: if it goes wrong, rollback is cheap.",
                ),
            },
            {
                "q": _t(
                    "Experiment tracking kyun zaroori hai?",
                    "Why is experiment tracking necessary?",
                ),
                "options": [
                    "Kaunsa config kis score par pahuncha, ye dobara banana sake",
                    "Model ko GPU par chalane ke liye",
                    "Prompt ko chhota karne ke liye",
                    "Users ko dikhane ke liye",
                ],
                "answer": "a",
                "why": _t(
                    "Bina tracking ke 'wahi try karo jo pehle chala tha' possible nahi hota.",
                    "Without tracking, 'try what worked before' is impossible.",
                ),
            },
        ],
    },
    20: {
        "title": _t("Safety, security aur responsible AI", "Safety, security and responsible AI"),
        "keywords": ["injection", "PII", "least privilege", "guardrail", "licence"],
        "intro": _t(
            "LLM ka output hamesha untrusted input hai. Prompt injection direct ya retrieved documents "
            "ke through aata hai. Tools ko least privilege do, PII redact karo, output validate karo, "
            "aur jailbreak/bias tests rakho.",
            "LLM output is always untrusted input. Prompt injection arrives directly or through "
            "retrieved documents. Give tools least privilege, redact PII, validate output, and keep "
            "jailbreak and bias tests.",
        ),
        "real_life": _t(
            "Kisi ne email me likha 'apna password bhej do' to aap nahi bhejte. Agent ko bhi document "
            "ke andar likhi instruction nahi maanni chahiye.",
            "If an email says 'send your password', you do not. An agent must not follow an "
            "instruction written inside a document either.",
        ),
        "takeaway": _t(
            "Instruction aur data ko alag rakho; tool ko sirf utni permission do jitna kaam ke liye chahiye.",
            "Keep instructions and data separate; give a tool only the permission the task needs.",
        ),
        "example": {
            "code": (
                "import re\n\n"
                "text = 'Mail asha@example.com or call 9876543210.'\n"
                "text = re.sub(r'[\\w.+-]+@[\\w-]+\\.[\\w.]+', '[email]', text)\n"
                "text = re.sub(r'\\b\\d{10}\\b', '[phone]', text)\n"
                "print(text)"
            ),
            "note": _t(
                "Regex se PII mask hoti hai; logs me raw email/phone mat bhejo.",
                "Regex masks PII; do not ship raw emails or phones into logs.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`redact(text)` likho jo email aur 10-digit phone ko mask kare; `clean` print karo.",
                "Write `redact(text)` that masks emails and 10-digit phones; print `clean`.",
            ),
            "starter": (
                "import re\n\n"
                "def redact(text):\n"
                "    ...\n\n"
                "clean = redact('Mail asha@example.com or call 9876543210.')\n"
                "print(clean)\n"
            ),
            "solution": (
                "import re\n\n"
                "def redact(text):\n"
                "    text = re.sub(r'[\\w.+-]+@[\\w-]+\\.[\\w.]+', '[email]', text)\n"
                "    text = re.sub(r'\\b\\d{10}\\b', '[phone]', text)\n"
                "    return text\n\n"
                "clean = redact('Mail asha@example.com or call 9876543210.')\n"
                "print(clean)\n"
            ),
            "checks": [
                "'asha@example.com' not in clean",
                "'9876543210' not in clean",
                "clean.count('[email]') == 1",
            ],
            "hint": _t(
                "Email pattern `[\\w.+-]+@[\\w-]+\\.[\\w.]+`, phone `\\b\\d{10}\\b`.",
                "Email pattern `[\\w.+-]+@[\\w-]+\\.[\\w.]+`, phone `\\b\\d{10}\\b`.",
            ),
        },
        "quiz": [
            {
                "q": _t("Indirect prompt injection kahan se aata hai?", "Where does indirect prompt injection come from?"),
                "options": [
                    "Retrieved documents, web pages ya tool output me chhupi instructions",
                    "Sirf user ke typed message se",
                    "Model ke weights se",
                    "GPU driver se",
                ],
                "answer": "a",
                "why": _t(
                    "Agent jab document padhta hai, usme likhi instruction ko data samjho, command nahi.",
                    "When an agent reads a document, treat its instructions as data, not commands.",
                ),
            },
            {
                "q": _t("Least privilege tools kyun?", "Why least-privilege tools?"),
                "options": [
                    "Agar model dhoka de jaye to nuksan chhota rahe",
                    "Tools fast chalte hain",
                    "Token cost kam hota hai",
                    "Model smart hota hai",
                ],
                "answer": "a",
                "why": _t(
                    "Read-only tool se data delete nahi hoga, chahe model kuch bhi kahe.",
                    "A read-only tool cannot delete data, whatever the model says.",
                ),
            },
            {
                "q": _t(
                    "LLM output ko kab trust karna chahiye?",
                    "When should LLM output be trusted?",
                ),
                "options": [
                    "Kabhi nahi — validate, sandbox aur human review ke baad hi use karo",
                    "Jab temperature 0 ho",
                    "Jab model bada ho",
                    "Jab output lamba ho",
                ],
                "answer": "a",
                "why": _t(
                    "Output untrusted input hai; SQL, shell ya HTML me daalne se pehle validate karo.",
                    "Output is untrusted input; validate before putting it into SQL, shell or HTML.",
                ),
            },
        ],
    },
    21: {
        "title": _t("AI system design", "AI system design"),
        "keywords": ["requirements", "architecture", "routing", "fallback", "cost"],
        "intro": _t(
            "System design interview ka pattern fix hai: requirements → data → model → architecture → "
            "eval → deploy → monitor. Har design me routing, caching, fallback, idempotency aur "
            "human review ka jawab do.",
            "The system-design interview pattern is fixed: requirements → data → model → architecture "
            "→ eval → deploy → monitor. Every design must answer routing, caching, fallback, "
            "idempotency and human review.",
        ),
        "real_life": _t(
            "Ghar ka budget: kitne log, kitne meal, kitna paisa. LLM system me bhi pehle numbers "
            "(requests, tokens, latency) likho, phir architecture chuno.",
            "A household budget: how many people, meals and rupees. In an LLM system, write the "
            "numbers (requests, tokens, latency) first, then choose the architecture.",
        ),
        "takeaway": _t(
            "Cost aur latency estimate design ka hissa hai, deployment ke baad ka surprise nahi.",
            "Cost and latency estimates are part of the design, not a post-deployment surprise.",
        ),
        "example": {
            "code": (
                "requests = 100_000\n"
                "cost = requests * (800 * 0.4 + 300 * 1.6) / 1_000_000\n"
                "print(round(cost, 2))"
            ),
            "note": _t(
                "Per-request token cost × requests = monthly bill ka estimate.",
                "Per-request token cost × requests = the monthly bill estimate.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`monthly_cost(requests, tokens_in, tokens_out, price_in, price_out)` likho aur "
                "1,00,000 requests par `cost` print karo.",
                "Write `monthly_cost(requests, tokens_in, tokens_out, price_in, price_out)` and print "
                "`cost` for 100,000 requests.",
            ),
            "starter": (
                "def monthly_cost(requests, tokens_in, tokens_out, price_in, price_out):\n"
                "    ...\n\n"
                "cost = monthly_cost(100_000, 800, 300, 0.4, 1.6)\n"
                "print(round(cost, 2))\n"
            ),
            "solution": (
                "def monthly_cost(requests, tokens_in, tokens_out, price_in, price_out):\n"
                "    return requests * (tokens_in * price_in + tokens_out * price_out) / 1_000_000\n\n"
                "cost = monthly_cost(100_000, 800, 300, 0.4, 1.6)\n"
                "print(round(cost, 2))\n"
            ),
            "checks": [
                "abs(cost - 80.0) < 1e-6",
            ],
            "hint": _t(
                "Prices per million tokens hain, isliye `1_000_000` se divide karo.",
                "Prices are per million tokens, so divide by `1_000_000`.",
            ),
        },
        "quiz": [
            {
                "q": _t("Model routing ka fayda?", "The benefit of model routing?"),
                "options": [
                    "Aasan request saste model par, mushkil request bade model par",
                    "Har request same model par",
                    "Latency hamesha badh jati hai",
                    "Cost hamesha badh jati hai",
                ],
                "answer": "a",
                "why": _t(
                    "Routing se average cost girta hai; quality-critical requests bade model par rehti hain.",
                    "Routing lowers average cost while quality-critical requests stay on the big model.",
                ),
            },
            {
                "q": _t("Fallback chain kya hai?", "What is a fallback chain?"),
                "options": [
                    "Primary provider fail hone par doosra provider try karna",
                    "Prompt ko chhota karna",
                    "Model ko quantise karna",
                    "Database ko backup lena",
                ],
                "answer": "a",
                "why": _t(
                    "Provider outage real hai; fallback aur timeout ke bina product ruk jata hai.",
                    "Provider outages are real; without fallback and timeouts the product stops.",
                ),
            },
            {
                "q": _t("Human review kab rakhein?", "When should human review be in the loop?"),
                "options": [
                    "High-impact actions par: paisa, legal, medical, public post",
                    "Har chhote answer par",
                    "Kabhi nahi",
                    "Sirf training me",
                ],
                "answer": "a",
                "why": _t(
                    "Jahan galti ka asar bada aur wapas nahi ho sakta, wahan approval gate rakho.",
                    "Where a mistake is costly and irreversible, keep an approval gate.",
                ),
            },
        ],
    },
    22: {
        "title": _t("Career: interview, portfolio aur freelancing", "Career: interviews, portfolio and freelancing"),
        "keywords": ["STAR", "ATS", "portfolio", "take-home", "pricing"],
        "intro": _t(
            "Job ke liye proof chahiye, sirf certificate nahi. Portfolio me demo + eval numbers + "
            "README rakho. Interview me STAR se bolo, aur take-home me scope likh kar time-box karo. "
            "Freelancing me proposal, scope aur price likhna sabse zaroori hai.",
            "A job needs proof, not just a certificate. Put a demo, eval numbers and a README in the "
            "portfolio. Answer interviews with STAR, and time-box a take-home with a written scope. In "
            "freelancing, the proposal, scope and price matter most.",
        ),
        "real_life": _t(
            "Shaadi ka card chhota hota hai par saari zaroori baat batata hai. Resume/README bhi wahi: "
            "short, specific, aur proof ke saath.",
            "A wedding card is small but carries every essential detail. A resume or README is the "
            "same: short, specific and backed by proof.",
        ),
        "takeaway": _t(
            "Har project ke saath ek number likho: latency, cost, accuracy ya eval score.",
            "Every project gets one number: latency, cost, accuracy or an eval score.",
        ),
        "example": {
            "code": (
                "resume = 'python sql rag evals docker'\n"
                "jd = 'python sql rag kubernetes'\n"
                "have = set(resume.split())\n"
                "want = {w for w in jd.split() if len(w) > 3}\n"
                "print(len(have & want) / len(want))"
            ),
            "note": _t(
                "ATS keyword match ka simple version; asli resume me achievements bhi likho.",
                "A simple version of ATS keyword matching; a real resume also shows achievements.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`match(resume, jd)` likho jo JD ke 4+ letter words me se kitne resume me hain, wo "
                "fraction return kare; `score` print karo.",
                "Write `match(resume, jd)` returning the fraction of 4+ letter JD words present in the "
                "resume; print `score`.",
            ),
            "starter": (
                "def match(resume, jd):\n"
                "    ...\n\n"
                "score = match('python sql rag evals docker', 'python sql rag kubernetes')\n"
                "print(round(score, 2))\n"
            ),
            "solution": (
                "def match(resume, jd):\n"
                "    resume_words = set(resume.lower().split())\n"
                "    jd_words = {word for word in jd.lower().split() if len(word) > 3}\n"
                "    return len(resume_words & jd_words) / len(jd_words)\n\n"
                "score = match('python sql rag evals docker', 'python sql rag kubernetes')\n"
                "print(round(score, 2))\n"
            ),
            "checks": [
                "abs(score - 0.5) < 1e-9",
            ],
            "hint": _t(
                "JD words ka set banao, resume words se intersection lo, size se divide karo.",
                "Build a set of JD words, intersect with resume words, divide by its size.",
            ),
        },
        "quiz": [
            {
                "q": _t("STAR ka matlab?", "What does STAR stand for?"),
                "options": [
                    "Situation, Task, Action, Result",
                    "Skill, Tool, Answer, Review",
                    "Start, Test, Apply, Repeat",
                    "Scope, Time, Amount, Risk",
                ],
                "answer": "a",
                "why": _t(
                    "Behavioural answer ko structure deta hai, aur Result par khatam karna zaroori hai.",
                    "It structures a behavioural answer, and it must end on the Result.",
                ),
            },
            {
                "q": _t(
                    "Portfolio project me kya sabse zyada matter karta hai?",
                    "What matters most in a portfolio project?",
                ),
                "options": [
                    "Chalne wala demo aur eval ke numbers",
                    "Code ki lines ki ginti",
                    "Kitne frameworks use hue",
                    "Repository ka naam",
                ],
                "answer": "a",
                "why": _t(
                    "Recruiter proof dekhta hai: demo chalta hai aur quality naapi gayi hai.",
                    "A recruiter looks for proof: the demo runs and quality was measured.",
                ),
            },
            {
                "q": _t("Take-home ka sahi approach?", "The right take-home approach?"),
                "options": [
                    "Scope likho, time-box karo, trade-offs README me batao",
                    "Jitna bada ho sake banao",
                    "Poora product banane ki koshish karo",
                    "Kuch mat likho, sirf code do",
                ],
                "answer": "a",
                "why": _t(
                    "Time-box aur clear trade-offs senior engineer ki nishani hai.",
                    "A time-box and clear trade-offs signal a senior engineer.",
                ),
            },
        ],
    },
    23: {
        "title": _t("Capstone: chhota RAG pipeline", "Capstone: a small RAG pipeline"),
        "keywords": ["retrieval", "citation", "eval", "pipeline", "cost"],
        "intro": _t(
            "Ab sab jodo: documents, retrieval, answer aur citation. Capstone ka maqsad fancy UI nahi, "
            "end-to-end proof hai — input se grounded answer tak, aur ek eval jo quality naape.",
            "Now join everything: documents, retrieval, an answer and a citation. The capstone goal is "
            "not a fancy UI but end-to-end proof, from input to a grounded answer, plus an eval that "
            "measures quality.",
        ),
        "real_life": _t(
            "Lawyer ka case file: sirf answer nahi, kaunsa page aur kaunsi line, wo bhi batana padta "
            "hai. Citation ke bina answer adhoora hai.",
            "A lawyer's case file: not just the answer but which page and line. Without a citation the "
            "answer is incomplete.",
        ),
        "takeaway": _t(
            "Capstone me ek number zaroor dikhao: recall@k, faithfulness ya cost per 1k requests.",
            "A capstone must show one number: recall@k, faithfulness or cost per 1k requests.",
        ),
        "example": {
            "code": (
                "docs = [\n"
                "    {'id': 'd1', 'text': 'RAG retrieves documents before answering.'},\n"
                "    {'id': 'd2', 'text': 'Fine-tuning changes model weights.'},\n"
                "]\n"
                "q = set('how does rag retrieve'.split())\n"
                "best = max(docs, key=lambda d: len(q & set(d['text'].lower().split())))\n"
                "print(best['id'])"
            ),
            "note": _t(
                "Retrieval ka simplest version: shared words ka count.",
                "The simplest retrieval: count shared words.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`answer(question, docs)` likho jo sabse zyada overlap wale doc ka `(id, text)` "
                "return kare; `doc_id` aur sentence print karo.",
                "Write `answer(question, docs)` returning `(id, text)` of the best-overlap document; "
                "print `doc_id` and the sentence.",
            ),
            "starter": (
                "def answer(question, docs):\n"
                "    ...\n\n"
                "docs = [\n"
                "    {'id': 'd1', 'text': 'RAG retrieves documents before answering.'},\n"
                "    {'id': 'd2', 'text': 'Fine-tuning changes model weights.'},\n"
                "]\n"
                "doc_id, sentence = answer('how does rag retrieve documents', docs)\n"
                "print(doc_id, '|', sentence)\n"
            ),
            "solution": (
                "def answer(question, docs):\n"
                "    words = set(question.lower().split())\n"
                "    best = max(docs, key=lambda doc: len(words & set(doc['text'].lower().split())))\n"
                "    return best['id'], best['text']\n\n"
                "docs = [\n"
                "    {'id': 'd1', 'text': 'RAG retrieves documents before answering.'},\n"
                "    {'id': 'd2', 'text': 'Fine-tuning changes model weights.'},\n"
                "]\n"
                "doc_id, sentence = answer('how does rag retrieve documents', docs)\n"
                "print(doc_id, '|', sentence)\n"
            ),
            "checks": [
                "doc_id == 'd1'",
                "'retrieves' in sentence",
            ],
            "hint": _t(
                "`max` ko key do: question words aur doc words ka intersection size.",
                "Give `max` a key: the intersection size of question and document words.",
            ),
        },
        "quiz": [
            {
                "q": _t(
                    "Capstone me pehle kya banana chahiye?",
                    "What should a capstone build first?",
                ),
                "options": [
                    "End-to-end thin slice: ek document se grounded answer",
                    "Poora UI",
                    "Saare providers ka integration",
                    "Fine-tuning",
                ],
                "answer": "a",
                "why": _t(
                    "Thin slice pehle: ek document, ek answer, ek citation, ek eval.",
                    "Thin slice first: one document, one answer, one citation, one eval.",
                ),
            },
            {
                "q": _t("Faithfulness eval kya check karta hai?", "What does a faithfulness eval check?"),
                "options": [
                    "Answer retrieved context se supported hai ya nahi",
                    "Answer ki length",
                    "Model ka size",
                    "API ka price",
                ],
                "answer": "a",
                "why": _t(
                    "Grounded answer ke har claim ka source context me hona chahiye.",
                    "Every claim in a grounded answer should be supported by the context.",
                ),
            },
            {
                "q": _t("Cost per 1k requests kyun likhna chahiye?", "Why report cost per 1k requests?"),
                "options": [
                    "Decision makers ko scale par cost dikhta hai",
                    "Model ko train karne ke liye",
                    "Prompt ko chhota karne ke liye",
                    "Latency badhane ke liye",
                ],
                "answer": "a",
                "why": _t(
                    "Ek request ka cost chhota lagta hai; 1k requests par asli number dikhta hai.",
                    "One request looks cheap; 1k requests shows the real number.",
                ),
            },
        ],
    },
}
