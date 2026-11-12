"""Authored lessons 9-16 of the AI-engineering course (Part C and part of D)."""


def _t(hinglish: str, en: str) -> dict:
    return {"hinglish": hinglish, "en": en}


LESSONS = {
    9: {
        "title": _t("LLM fundamentals: next token aur sampling", "LLM fundamentals: next token and sampling"),
        "keywords": ["token", "softmax", "temperature", "hallucination", "context"],
        "intro": _t(
            "LLM ek hi kaam karta hai: diye gaye text ke baad next token ki probability nikalna. "
            "Chat, code aur translation sab isi loop ka side effect hain. Model sach nahi dhoondhta, "
            "plausible next token dhoondhta hai — isliye confident galat jawab aata hai.",
            "An LLM does one thing: produce a probability for the next token after the given text. "
            "Chat, code and translation are side effects of that loop. The model does not look up "
            "truth, it looks for a plausible next token, which is why confident wrong answers happen.",
        ),
        "real_life": _t(
            "Phone ka autocomplete, bas crores examples se trained: 'Chai ke saath' ke baad 'biscuit' "
            "plausible lagta hai, isliye suggest hota hai. Poora paragraph bhi isi tarah banta hai.",
            "Phone autocomplete, trained on crores of examples: after 'tea with' the word 'biscuit' "
            "looks plausible, so it is suggested. A whole paragraph is built the same way.",
        ),
        "takeaway": _t(
            "Temperature 0 = sabse likely token, high temperature = creative par zyada galat.",
            "Temperature 0 = the most likely token, high temperature = creative but more wrong.",
        ),
        "example": {
            "code": (
                "import math\n\n"
                "def softmax(logits, temperature=1.0):\n"
                "    scaled = [x / temperature for x in logits]\n"
                "    top = max(scaled)\n"
                "    exps = [math.exp(x - top) for x in scaled]\n"
                "    return [e / sum(exps) for e in exps]\n\n"
                "print([round(p, 3) for p in softmax([2, 1, 0])])"
            ),
            "note": _t(
                "Logits probability ban jate hain; sabse bada logit sabse zyada probability leta hai.",
                "Logits become probabilities; the largest logit gets the most probability.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`softmax(logits, temperature)` likho aur `cold` (0.5) vs `warm` (2.0) ke pehle "
                "token ki probability print karo.",
                "Write `softmax(logits, temperature)` and print the first token's probability for "
                "`cold` (0.5) versus `warm` (2.0).",
            ),
            "starter": (
                "import math\n\n"
                "def softmax(logits, temperature=1.0):\n"
                "    ...\n\n"
                "cold = softmax([2.0, 1.0, 0.0], temperature=0.5)\n"
                "warm = softmax([2.0, 1.0, 0.0], temperature=2.0)\n"
                "print(round(cold[0], 3), round(warm[0], 3))\n"
            ),
            "solution": (
                "import math\n\n"
                "def softmax(logits, temperature=1.0):\n"
                "    scaled = [logit / temperature for logit in logits]\n"
                "    top = max(scaled)\n"
                "    exps = [math.exp(x - top) for x in scaled]\n"
                "    total = sum(exps)\n"
                "    return [e / total for e in exps]\n\n"
                "cold = softmax([2.0, 1.0, 0.0], temperature=0.5)\n"
                "warm = softmax([2.0, 1.0, 0.0], temperature=2.0)\n"
                "print(round(cold[0], 3), round(warm[0], 3))\n"
            ),
            "checks": [
                "cold[0] > warm[0]",
                "abs(sum(cold) - 1) < 1e-9",
                "cold[0] > 0.8",
            ],
            "hint": _t(
                "Temperature chhota = distribution sharp; bada = flat.",
                "A small temperature sharpens the distribution; a large one flattens it.",
            ),
        },
        "quiz": [
            {
                "q": _t("Temperature 0 ka behaviour?", "What does temperature 0 do?"),
                "options": [
                    "Har step par sabse likely token chunta hai (greedy)",
                    "Random token chunta hai",
                    "Model ko off kar deta hai",
                    "Output ko translate karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Zero temperature deterministic greedy decoding hai; same prompt, same answer.",
                    "Zero temperature is deterministic greedy decoding: same prompt, same answer.",
                ),
            },
            {
                "q": _t("Hallucination ka main reason?", "The main cause of hallucination?"),
                "options": [
                    "Model plausibility optimise karta hai, truth verify nahi karta",
                    "Model ka internet band ho jata hai",
                    "Temperature hamesha 0 hota hai",
                    "Context window chhota hota hai",
                ],
                "answer": "a",
                "why": _t(
                    "Training objective next-token prediction hai; grounding retrieval ya tools se aati hai.",
                    "The objective is next-token prediction; grounding comes from retrieval or tools.",
                ),
            },
            {
                "q": _t("Context window badhane ka trade-off?", "The trade-off of a bigger context window?"),
                "options": [
                    "Cost aur latency badhte hain, aur lamba context degrade bhi ho sakta hai",
                    "Model free ho jata hai",
                    "Accuracy hamesha 100% ho jati hai",
                    "Tokens ki zaroorat nahi rehti",
                ],
                "answer": "a",
                "why": _t(
                    "Zyada tokens = zyada paisa aur time; beech ka content ignore bhi ho sakta hai.",
                    "More tokens cost more money and time; middle content can be ignored.",
                ),
            },
        ],
    },
    10: {
        "title": _t("LLM API engineering", "LLM API engineering"),
        "keywords": ["streaming", "retry", "schema", "timeout", "idempotency"],
        "intro": _t(
            "Production LLM code me retry, timeout, structured output aur cost tracking lazmi hai. "
            "Ek OpenAI-compatible client se `base_url` badal kar kai providers chalti hain, aur "
            "streaming se user ko pehla token jaldi milta hai.",
            "Production LLM code needs retries, timeouts, structured output and cost tracking. One "
            "OpenAI-compatible client can talk to many providers by changing `base_url`, and streaming "
            "gets the first token to the user sooner.",
        ),
        "real_life": _t(
            "Courier service: parcel na pahunche to dobara try karo, par har baar thoda wait badhao "
            "(backoff). Bina limit retry karna server par dhamaka hai.",
            "A courier: retry a failed delivery, but wait a little longer each time (backoff). "
            "Unlimited retries are a denial-of-service on yourself.",
        ),
        "takeaway": _t(
            "429 par backoff + jitter; 400 par retry mat karo, request theek karo.",
            "On 429 back off with jitter; on 400 do not retry, fix the request.",
        ),
        "example": {
            "code": (
                "def flaky(state):\n"
                "    state['calls'] += 1\n"
                "    if state['calls'] < 3:\n"
                "        raise RuntimeError('429')\n"
                "    return 'ok'\n\n"
                "state = {'calls': 0}\n"
                "for _ in range(4):\n"
                "    try:\n"
                "        print(flaky(state)); break\n"
                "    except RuntimeError:\n"
                "        print('retry')"
            ),
            "note": _t(
                "Teesri call par kaam ho jata hai; real code me sleep/backoff add hota hai.",
                "The third call succeeds; real code adds sleep/backoff.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`call_with_retry(fn, state, attempts=4)` likho jo fail hone par dobara try kare aur "
                "success par result de. `result` aur `state['calls']` print karo.",
                "Write `call_with_retry(fn, state, attempts=4)` that retries on failure and returns "
                "the result. Print `result` and `state['calls']`.",
            ),
            "starter": (
                "def flaky(state):\n"
                "    state['calls'] += 1\n"
                "    if state['calls'] < 3:\n"
                "        raise RuntimeError('429 rate limited')\n"
                "    return 'ok'\n\n"
                "def call_with_retry(fn, state, attempts=4):\n"
                "    ...\n\n"
                "state = {'calls': 0}\n"
                "result = call_with_retry(flaky, state)\n"
                "print(result, state['calls'])\n"
            ),
            "solution": (
                "def flaky(state):\n"
                "    state['calls'] += 1\n"
                "    if state['calls'] < 3:\n"
                "        raise RuntimeError('429 rate limited')\n"
                "    return 'ok'\n\n"
                "def call_with_retry(fn, state, attempts=4):\n"
                "    last = None\n"
                "    for _ in range(attempts):\n"
                "        try:\n"
                "            return fn(state)\n"
                "        except RuntimeError as exc:\n"
                "            last = exc\n"
                "    raise last\n\n"
                "state = {'calls': 0}\n"
                "result = call_with_retry(flaky, state)\n"
                "print(result, state['calls'])\n"
            ),
            "checks": [
                "result == 'ok'",
                "state['calls'] == 3",
            ],
            "hint": _t(
                "Loop ke andar try/except; last exception yaad rakho aur attempts ke baad raise karo.",
                "try/except inside a loop; remember the last exception and raise it after the attempts.",
            ),
        },
        "quiz": [
            {
                "q": _t("HTTP 429 ka matlab?", "What does HTTP 429 mean?"),
                "options": [
                    "Rate limit — thoda ruk kar backoff ke saath retry karo",
                    "API key galat hai",
                    "Server down hai hamesha ke liye",
                    "Request bahut chhoti thi",
                ],
                "answer": "a",
                "why": _t(
                    "429 throttle hai; backoff aur jitter se retry karo, warna aur block hoge.",
                    "429 is throttling; retry with backoff and jitter or you get blocked further.",
                ),
            },
            {
                "q": _t(
                    "Structured output ke liye sabse safe approach?",
                    "The safest approach to structured output?",
                ),
                "options": [
                    "JSON schema ya pydantic se validate karo, fail par retry/repair",
                    "Model par poora bharosa karo",
                    "Output ko eval karo",
                    "JSON ko string ki tarah store karo",
                ],
                "answer": "a",
                "why": _t(
                    "Model schema tod sakta hai; validation boundary par hi pakad me aata hai.",
                    "A model can break the schema; validation at the boundary catches it.",
                ),
            },
            {
                "q": _t("Streaming ka fayda?", "The benefit of streaming?"),
                "options": [
                    "Pehla token jaldi dikhta hai, perceived latency kam hoti hai",
                    "Model sasta ho jata hai",
                    "Accuracy badh jati hai",
                    "Retry ki zaroorat nahi rehti",
                ],
                "answer": "a",
                "why": _t(
                    "Total time same rehta hai, par user ko turant response dikhta hai.",
                    "Total time is the same, but the user sees a response immediately.",
                ),
            },
        ],
    },
    11: {
        "title": _t("Prompt aur context engineering", "Prompt and context engineering"),
        "keywords": ["few-shot", "context budget", "memory", "injection", "versioning"],
        "intro": _t(
            "Magic prompt tricks low value hain. Asli kaam hai poora context design karna: instructions, "
            "examples, tools, memory, retrieval aur eval. Context ek budget hai — har token ki jagah "
            "aur keemat hai.",
            "Magic prompt tricks are low value. The real job is designing the whole context: "
            "instructions, examples, tools, memory, retrieval and evaluation. Context is a budget; "
            "every token has a place and a price.",
        ),
        "real_life": _t(
            "Interview ke liye ek page ka brief: zaroori baat pehle, examples saath me, aur irrelevant "
            "purani file mat lagao. Context window bhi wahi brief hai.",
            "A one-page brief for an interview: the important point first, examples beside it, and no "
            "irrelevant old file. A context window is that brief.",
        ),
        "takeaway": _t(
            "Context me jo cheez nahi honi chahiye wo bhi utni hi important hai jitni honi chahiye.",
            "What you keep out of the context matters as much as what you put in.",
        ),
        "example": {
            "code": (
                "def size(text):\n"
                "    return len(text) // 4\n\n"
                "system = 'You are a careful tutor.'\n"
                "examples = ['Example one.', 'Example two.', 'Example three.']\n"
                "print(size(system), [size(e) for e in examples])"
            ),
            "note": _t(
                "Tokens ka quick estimate: 4 characters ≈ 1 token (English ka rule of thumb).",
                "Quick token estimate: 4 characters ≈ 1 token for English.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`build_prompt(system, examples, question, budget_tokens)` likho jo examples ko end se "
                "drop kare jab tak prompt budget me na aa jaye, aur `(prompt, used)` return kare. "
                "Kitne examples bache, print karo.",
                "Write `build_prompt(system, examples, question, budget_tokens)` that drops examples "
                "from the end until the prompt fits, returning `(prompt, used)`. Print how many "
                "examples survived.",
            ),
            "starter": (
                "def build_prompt(system, examples, question, budget_tokens):\n"
                "    def size(text):\n"
                "        return len(text) // 4\n"
                "    chosen = list(examples)\n"
                "    ...\n"
                "    return prompt, chosen\n\n"
                "system = 'You are a careful tutor.'\n"
                "examples = ['Example one is long enough.', 'Example two is also here.', 'Example three.']\n"
                "prompt, used = build_prompt(system, examples, 'Explain RAG.', 20)\n"
                "print(len(used), 'examples kept')\n"
            ),
            "solution": (
                "def build_prompt(system, examples, question, budget_tokens):\n"
                "    def size(text):\n"
                "        return len(text) // 4\n"
                "    chosen = list(examples)\n"
                "    while chosen and size(system) + sum(size(e) for e in chosen) + size(question) > budget_tokens:\n"
                "        chosen.pop()\n"
                "    prompt = '\\n'.join([system] + chosen + [question])\n"
                "    return prompt, chosen\n\n"
                "system = 'You are a careful tutor.'\n"
                "examples = ['Example one is long enough.', 'Example two is also here.', 'Example three.']\n"
                "prompt, used = build_prompt(system, examples, 'Explain RAG.', 20)\n"
                "print(len(used), 'examples kept')\n"
            ),
            "checks": [
                "len(used) < 3",
                "'Explain RAG.' in prompt",
                "used == examples[:len(used)]",
            ],
            "hint": _t(
                "Jab tak budget se bada ho, `chosen.pop()` karo; order preserve rehta hai.",
                "While it is over budget, `chosen.pop()`; the order is preserved.",
            ),
        },
        "quiz": [
            {
                "q": _t("Few-shot examples kab madad karte hain?", "When do few-shot examples help?"),
                "options": [
                    "Jab output ka format ya style dikhana ho",
                    "Jab context window unlimited ho",
                    "Jab model bahut bada ho",
                    "Jab API key na ho",
                ],
                "answer": "a",
                "why": _t(
                    "Examples format aur edge cases sikhate hain; saare rules likhne se sasta bhi ho sakta hai.",
                    "Examples teach format and edge cases, sometimes cheaper than writing every rule.",
                ),
            },
            {
                "q": _t(
                    "Prompt injection ka sabse aam rasta?",
                    "The most common prompt injection path?",
                ),
                "options": [
                    "Retrieved ya user content me instructions chhupi hoti hain",
                    "Model ka temperature 0 hota hai",
                    "API key expire ho jati hai",
                    "JSON schema galat hota hai",
                ],
                "answer": "a",
                "why": _t(
                    "Untrusted content ko instruction ki tarah padhna injection hai; use data hi rakho.",
                    "Reading untrusted content as instructions is the injection; keep it as data.",
                ),
            },
            {
                "q": _t(
                    "Prompt versioning kyun zaroori hai?",
                    "Why version prompts?",
                ),
                "options": [
                    "Badlav ka asar eval se compare kar sakein aur rollback ho sake",
                    "Prompt ko chhota rakhne ke liye",
                    "Model ko fine-tune karne ke liye",
                    "Token count badhane ke liye",
                ],
                "answer": "a",
                "why": _t(
                    "Prompt bhi code hai: version, test aur rollback ke bina regression pata nahi chalta.",
                    "A prompt is code: without versioning, tests and rollback you cannot see regressions.",
                ),
            },
        ],
    },
    12: {
        "title": _t("RAG: retrieval se grounded answer tak", "RAG: from retrieval to a grounded answer"),
        "keywords": ["chunk", "embedding", "hybrid", "rerank", "citation"],
        "intro": _t(
            "RAG model ko naya knowledge nahi sikhata; sahi waqt par sahi text context me deta hai. "
            "Chunking, hybrid search, reranking aur citation chaar cheezein hain jo demo ko product "
            "banati hain. Sirf top-3 vector search final design nahi hai.",
            "RAG does not teach the model new knowledge; it puts the right text in the context at the "
            "right time. Chunking, hybrid search, reranking and citations are the four things that turn "
            "a demo into a product. Top-3 vector search alone is not a final design.",
        ),
        "real_life": _t(
            "Exam me open-book: pehle sahi page dhoondho (retrieval), phir us page se answer likho "
            "(generation), aur page number likho (citation). Galat page = confident galat answer.",
            "An open-book exam: find the right page (retrieval), answer from that page (generation), "
            "and write the page number (citation). Wrong page = confident wrong answer.",
        ),
        "takeaway": _t(
            "Retrieval recall pehle theek karo; generation ka quality uske baad hi matter karta hai.",
            "Fix retrieval recall first; generation quality only matters after that.",
        ),
        "example": {
            "code": (
                "text = ' '.join(['rag'] * 12 + ['agent'] * 12)\n"
                "words = text.split()\n"
                "chunks = [' '.join(words[i:i + 8]) for i in range(0, len(words), 6)]\n"
                "print(len(chunks), chunks[1])"
            ),
            "note": _t(
                "Overlap se boundary par kata hua sentence doosre chunk me bhi milta hai.",
                "Overlap keeps a sentence cut at a boundary visible in the next chunk too.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`chunk(text, size=40, overlap=10)` aur `best_chunk(question, chunks)` likho; 90 words "
                "par `len(chunks)` aur best `index` print karo.",
                "Write `chunk(text, size=40, overlap=10)` and `best_chunk(question, chunks)`; print "
                "`len(chunks)` and the best `index` for 90 words.",
            ),
            "starter": (
                "def chunk(text, size=40, overlap=10):\n"
                "    ...\n\n"
                "def best_chunk(question, chunks):\n"
                "    ...\n\n"
                "text = ' '.join(['rag'] * 30 + ['agent'] * 30 + ['eval'] * 30)\n"
                "chunks = chunk(text)\n"
                "index = best_chunk('how does agent memory work', chunks)\n"
                "print(len(chunks), index)\n"
            ),
            "solution": (
                "def chunk(text, size=40, overlap=10):\n"
                "    words = text.split()\n"
                "    chunks = []\n"
                "    start = 0\n"
                "    while start < len(words):\n"
                "        chunks.append(' '.join(words[start:start + size]))\n"
                "        start += size - overlap\n"
                "    return chunks\n\n"
                "def best_chunk(question, chunks):\n"
                "    words = set(question.lower().split())\n"
                "    scored = [(len(words & set(c.lower().split())), i) for i, c in enumerate(chunks)]\n"
                "    return max(scored)[1]\n\n"
                "text = ' '.join(['rag'] * 30 + ['agent'] * 30 + ['eval'] * 30)\n"
                "chunks = chunk(text)\n"
                "index = best_chunk('how does agent memory work', chunks)\n"
                "print(len(chunks), index)\n"
            ),
            "checks": [
                "len(chunks) == 3",
                "index == 1",
                "'agent' in chunks[index]",
            ],
            "hint": _t(
                "Step `size - overlap` hai; question ke words ka set intersection score hai.",
                "The step is `size - overlap`; score chunks by set intersection with the question.",
            ),
        },
        "quiz": [
            {
                "q": _t("RAG me recall@k kya naapta hai?", "What does recall@k measure in RAG?"),
                "options": [
                    "Top-k retrieved chunks me sahi evidence aaya ya nahi",
                    "Generated answer ki length",
                    "Model ki speed",
                    "Embedding ka dimension",
                ],
                "answer": "a",
                "why": _t(
                    "Agar evidence top-k me nahi hai, generator kuch bhi kare, answer grounded nahi ho sakta.",
                    "If the evidence is not in the top-k, no generator can ground the answer.",
                ),
            },
            {
                "q": _t("Hybrid search kya milata hai?", "What does hybrid search combine?"),
                "options": [
                    "Keyword (BM25) aur dense vector search",
                    "Do LLM providers",
                    "Do databases ke passwords",
                    "Training aur inference",
                ],
                "answer": "a",
                "why": _t(
                    "Exact terms BM25 pakadta hai, meaning dense; dono mil kar recall badhate hain.",
                    "BM25 catches exact terms, dense catches meaning; together they raise recall.",
                ),
            },
            {
                "q": _t("Reranker kab lagana chahiye?", "When should a reranker be added?"),
                "options": [
                    "Retrieval ke baad, top candidates ko precise order dene ke liye",
                    "Sabse pehle, retrieval se bhi pehle",
                    "Sirf training ke waqt",
                    "Jab API key na ho",
                ],
                "answer": "a",
                "why": _t(
                    "Reranker cross-encoder hai: slow par accurate, isliye chhote candidate set par chalta hai.",
                    "A reranker is a cross-encoder: slow but accurate, so it runs on a small candidate set.",
                ),
            },
        ],
    },
    13: {
        "title": _t("Agentic AI: tool loop aur guardrails", "Agentic AI: tool loop and guardrails"),
        "keywords": ["tool", "ReAct", "state", "guardrail", "MCP"],
        "intro": _t(
            "Agent ek loop hai: model soche, tool chune, result dekhe, phir soche. Workflow pehle try "
            "karo; agent tabhi jab rasta pehle se pata na ho. Har loop me max steps, cost cap aur "
            "human approval rakho.",
            "An agent is a loop: the model thinks, picks a tool, reads the result, and thinks again. "
            "Try a workflow first; use an agent when the path is not known in advance. Every loop "
            "needs a max-step cap, a cost cap and human approval.",
        ),
        "real_life": _t(
            "Delivery boy ko address diya, par route khud chunna hai: map dekho, galat mod par wapas "
            "aao, aur petrol khatam hone se pehle ruk jao. Max steps wahi petrol ki limit hai.",
            "A delivery rider is given an address but chooses the route: check the map, turn back on a "
            "wrong turn, and stop before fuel runs out. Max steps is that fuel limit.",
        ),
        "takeaway": _t(
            "Har tool least privilege par do; model ka output hamesha untrusted input hai.",
            "Give every tool least privilege; model output is always untrusted input.",
        ),
        "example": {
            "code": (
                "tools = {'add': lambda a, b: a + b, 'search': lambda q: 'doc: ' + q}\n"
                "task = 'add 2 and 3'\n"
                "name = next((tool for tool in tools if tool in task), None)\n"
                "print(name, '->', tools[name](2, 3) if name == 'add' else '')"
            ),
            "note": _t(
                "Tool registry ek dict hai; agent ka kaam sahi tool aur sahi argument chunna hai. "
                "Har tool ek fixed function hai, kabhi `eval` nahi.",
                "A tool registry is a dict; the agent's job is picking the right tool and argument. "
                "Every tool is a fixed function, never `eval`.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`run_agent(task, tools, max_steps=3)` likho jo task me maujood tool ka naam dhoondhe, "
                "use trace me add kare aur task se hata de; `trace` print karo.",
                "Write `run_agent(task, tools, max_steps=3)` that finds a tool name in the task, adds "
                "it to the trace and removes it from the task; print `trace`.",
            ),
            "starter": (
                "def run_agent(task, tools, max_steps=3):\n"
                "    trace = []\n"
                "    ...\n"
                "    return trace\n\n"
                "trace = run_agent('calculate 2+2 then search docs', ['calculate', 'search'], max_steps=2)\n"
                "print(trace)\n"
            ),
            "solution": (
                "def run_agent(task, tools, max_steps=3):\n"
                "    trace = []\n"
                "    for _ in range(max_steps):\n"
                "        name = next((tool for tool in tools if tool in task.lower()), None)\n"
                "        if not name:\n"
                "            break\n"
                "        trace.append(name)\n"
                "        task = task.replace(name, '', 1)\n"
                "    return trace\n\n"
                "trace = run_agent('calculate 2+2 then search docs', ['calculate', 'search'], max_steps=2)\n"
                "print(trace)\n"
            ),
            "checks": [
                "trace == ['calculate', 'search']",
                "len(trace) <= 2",
            ],
            "hint": _t(
                "Har step par pehla matching tool lo, trace me daalo, phir task se hatao.",
                "Each step: take the first matching tool, append it, then remove it from the task.",
            ),
        },
        "quiz": [
            {
                "q": _t("Workflow vs agent?", "Workflow versus agent?"),
                "options": [
                    "Workflow ke steps fix hote hain; agent rasta khud chunta hai",
                    "Workflow zyada mehnga hota hai",
                    "Agent me kabhi tools nahi hote",
                    "Dono bilkul same hain",
                ],
                "answer": "a",
                "why": _t(
                    "Jab rasta pata ho to workflow sasta aur reliable hota hai; agent flexibility ke liye hai.",
                    "When the path is known, a workflow is cheaper and more reliable; an agent buys flexibility.",
                ),
            },
            {
                "q": _t("Max steps guardrail kyun zaroori hai?", "Why is a max-steps guardrail necessary?"),
                "options": [
                    "Infinite loop aur cost blow-up rokta hai",
                    "Model ko smart banata hai",
                    "Tool ki speed badhata hai",
                    "Prompt ko chhota karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Agent loop ho sakta hai; cap ke bina ek bug poora budget kha jata hai.",
                    "An agent can loop; without a cap one bug eats the whole budget.",
                ),
            },
            {
                "q": _t("MCP kya standard karta hai?", "What does MCP standardise?"),
                "options": [
                    "Model aur tools/data ke beech connection (tools, resources, prompts)",
                    "Model ke weights",
                    "GPU memory",
                    "Prompt ka language",
                ],
                "answer": "a",
                "why": _t(
                    "MCP ek protocol hai jisse ek hi tool server kai agents ke saath kaam karta hai.",
                    "MCP is a protocol so one tool server works with many agents.",
                ),
            },
        ],
    },
    14: {
        "title": _t("Evaluation aur observability", "Evaluation and observability"),
        "keywords": ["golden set", "LLM judge", "F1", "trace", "regression"],
        "intro": _t(
            "Demo aur product ka farak eval hai. Golden dataset banao, metric chuno, LLM-as-judge ko "
            "human labels se calibrate karo, aur eval ko CI me chalao. Bina eval ke har prompt change "
            "ek blind gamble hai.",
            "The difference between a demo and a product is evaluation. Build a golden dataset, choose "
            "metrics, calibrate an LLM judge against human labels, and run evals in CI. Without evals "
            "every prompt change is a blind gamble.",
        ),
        "real_life": _t(
            "Cricket me scoreboard: har ball ka result likha jata hai, warna agle match ke liye koi "
            "seekhne ki cheez nahi hoti. Eval wahi scoreboard hai.",
            "A cricket scoreboard records every ball; without it there is nothing to learn for the "
            "next match. Evaluation is that scoreboard.",
        ),
        "takeaway": _t(
            "Metric se pehle failure mode likho; metric us failure ko pakadta ho.",
            "Write the failure mode before the metric; the metric must catch that failure.",
        ),
        "example": {
            "code": (
                "def f1(tp, fp, fn):\n"
                "    precision = tp / (tp + fp) if tp + fp else 0.0\n"
                "    recall = tp / (tp + fn) if tp + fn else 0.0\n"
                "    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0\n\n"
                "print(round(f1(8, 2, 2), 3))"
            ),
            "note": _t(
                "Precision aur recall ka harmonic mean; dono me se ek girta hai to F1 bhi girta hai.",
                "The harmonic mean of precision and recall; if either drops, F1 drops.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`f1(tp, fp, fn)` likho aur do classes ke scores ka `macro` average print karo.",
                "Write `f1(tp, fp, fn)` and print the `macro` average of two class scores.",
            ),
            "starter": (
                "def f1(tp, fp, fn):\n"
                "    ...\n\n"
                "scores = [f1(8, 2, 2), f1(3, 1, 5)]\n"
                "macro = sum(scores) / len(scores)\n"
                "print(round(scores[0], 3), round(macro, 3))\n"
            ),
            "solution": (
                "def f1(tp, fp, fn):\n"
                "    precision = tp / (tp + fp) if tp + fp else 0.0\n"
                "    recall = tp / (tp + fn) if tp + fn else 0.0\n"
                "    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0\n\n"
                "scores = [f1(8, 2, 2), f1(3, 1, 5)]\n"
                "macro = sum(scores) / len(scores)\n"
                "print(round(scores[0], 3), round(macro, 3))\n"
            ),
            "checks": [
                "abs(scores[0] - 0.8) < 1e-9",
                "abs(macro - 0.65) < 1e-9",
            ],
            "hint": _t(
                "Zero division se bacho; precision+recall 0 ho to F1 0 hai.",
                "Guard zero division; if precision+recall is 0, F1 is 0.",
            ),
        },
        "quiz": [
            {
                "q": _t(
                    "95% negative data par accuracy kyun dhoka deti hai?",
                    "Why is accuracy misleading on 95% negative data?",
                ),
                "options": [
                    "Sab negative bolne se bhi 95% accuracy mil jati hai",
                    "Accuracy calculate nahi hoti",
                    "Accuracy sirf regression me hoti hai",
                    "Data ka size zyada hota hai",
                ],
                "answer": "a",
                "why": _t(
                    "Imbalance me majority class predict karna hi 'achha' score de deta hai; precision/recall dekho.",
                    "On imbalanced data, predicting the majority class scores well; look at precision/recall.",
                ),
            },
            {
                "q": _t("LLM-as-judge ka risk?", "The risk of LLM-as-judge?"),
                "options": [
                    "Judge ka bias aur calibration drift",
                    "Judge bahut sasta hota hai",
                    "Judge hamesha human se better hota hai",
                    "Judge ko GPU nahi chahiye",
                ],
                "answer": "a",
                "why": _t(
                    "Judge bhi model hai; human labels par calibrate karo aur periodic spot-check rakho.",
                    "A judge is also a model; calibrate on human labels and spot-check periodically.",
                ),
            },
            {
                "q": _t("Eval CI me kyun chalate hain?", "Why run evals in CI?"),
                "options": [
                    "Prompt/model change se regression merge se pehle pakadne ke liye",
                    "CI ko busy rakhne ke liye",
                    "Model ko train karne ke liye",
                    "GPU free karne ke liye",
                ],
                "answer": "a",
                "why": _t(
                    "Eval regression test hai: bina CI ke quality chupchap gir jati hai.",
                    "Evals are regression tests; without CI quality drops silently.",
                ),
            },
        ],
    },
    15: {
        "title": _t("Fine-tuning, LoRA aur quantisation", "Fine-tuning, LoRA and quantisation"),
        "keywords": ["LoRA", "QLoRA", "SFT", "DPO", "quantisation"],
        "intro": _t(
            "Fine-tuning pehla option nahi hai. Ladder yaad rakho: prompt → RAG → fine-tune. Jab "
            "behaviour ya style sikhana ho aur data ho, tab LoRA/QLoRA se chhota model fine-tune karo "
            "aur before/after eval se proof do.",
            "Fine-tuning is not the first option. Remember the ladder: prompt → RAG → fine-tune. When "
            "you need to teach behaviour or style and you have data, fine-tune a small model with "
            "LoRA/QLoRA and prove it with before/after evals.",
        ),
        "real_life": _t(
            "Naye employee ko poora MBA karane ke bajaye company ka 2-page handbook do — wahi LoRA hai: "
            "base model wahi, sirf chhota behaviour patch.",
            "Instead of sending a new hire for an MBA, give a two-page handbook: that is LoRA, the "
            "same base model with a small behaviour patch.",
        ),
        "takeaway": _t(
            "LoRA trainable parameters `r × (d_in + d_out)` hote hain — full model se hazaar guna chhote.",
            "LoRA has `r × (d_in + d_out)` trainable parameters, thousands of times fewer than full training.",
        ),
        "example": {
            "code": (
                "d_in = d_out = 4096\n"
                "full = d_in * d_out\n"
                "for r in (4, 8, 16):\n"
                "    lora = r * (d_in + d_out)\n"
                "    print(r, lora, round(100 * lora / full, 2), '%')"
            ),
            "note": _t(
                "r badhane se capacity badhti hai, par trainable size phir bhi chhota rehta hai.",
                "A larger r adds capacity while the trainable size stays small.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`lora_params(d_in, d_out, r)` likho; 4096×4096 model par `full`, `lora` (r=8) aur "
                "ratio print karo.",
                "Write `lora_params(d_in, d_out, r)`; print `full`, `lora` (r=8) and the ratio for a "
                "4096×4096 model.",
            ),
            "starter": (
                "def lora_params(d_in, d_out, r):\n"
                "    ...\n\n"
                "full = 4096 * 4096\n"
                "lora = lora_params(4096, 4096, 8)\n"
                "print(full, lora, round(lora / full, 4))\n"
            ),
            "solution": (
                "def lora_params(d_in, d_out, r):\n"
                "    return r * (d_in + d_out)\n\n"
                "full = 4096 * 4096\n"
                "lora = lora_params(4096, 4096, 8)\n"
                "print(full, lora, round(lora / full, 4))\n"
            ),
            "checks": [
                "lora == 65536",
                "lora < full",
                "abs(lora / full - 0.0039) < 0.0001",
            ],
            "hint": _t(
                "Do chhote matrices: `d_in × r` aur `r × d_out`.",
                "Two small matrices: `d_in × r` and `r × d_out`.",
            ),
        },
        "quiz": [
            {
                "q": _t(
                    "Naya behaviour sikhane ka sahi order?",
                    "The right order for teaching new behaviour?",
                ),
                "options": [
                    "Prompt → RAG → fine-tune",
                    "Fine-tune → prompt → RAG",
                    "RAG → fine-tune → prompt",
                    "Sirf fine-tune",
                ],
                "answer": "a",
                "why": _t(
                    "Sasta aur reversible pehle; fine-tune tab jab data aur clear behaviour ho.",
                    "Cheapest and most reversible first; fine-tune when data and behaviour are clear.",
                ),
            },
            {
                "q": _t("QLoRA kya karta hai?", "What does QLoRA do?"),
                "options": [
                    "Base model ko 4-bit me quantise karke LoRA adapters train karta hai",
                    "Model ko double karta hai",
                    "Prompt ko compress karta hai",
                    "Sirf CPU par chalta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Quantised base + small adapters se free GPU par bhi fine-tune possible hota hai.",
                    "A quantised base plus small adapters makes fine-tuning possible on free GPUs.",
                ),
            },
            {
                "q": _t("Catastrophic forgetting?", "Catastrophic forgetting?"),
                "options": [
                    "Fine-tuning se model purane skills kho deta hai",
                    "Model ka GPU memory khatam ho jata hai",
                    "Dataset delete ho jata hai",
                    "Prompt bhool jata hai",
                ],
                "answer": "a",
                "why": _t(
                    "Narrow data par zyada train karna general ability kharab kar sakta hai; eval se pakdo.",
                    "Over-training on narrow data can hurt general ability; catch it with evals.",
                ),
            },
        ],
    },
    16: {
        "title": _t("Multimodal AI: image, audio aur documents", "Multimodal AI: image, audio and documents"),
        "keywords": ["VLM", "OCR", "CLIP", "ASR", "pooling"],
        "intro": _t(
            "Multimodal ka matlab model ko text ke saath image/audio dena. OCR text nikalta hai, VLM "
            "image ko samajhta hai, CLIP image aur text ko ek hi embedding space me laata hai, aur "
            "Whisper jaisa ASR speech ko text banata hai.",
            "Multimodal means giving a model images or audio alongside text. OCR extracts text, a VLM "
            "understands the image, CLIP puts images and text in one embedding space, and ASR such as "
            "Whisper turns speech into text.",
        ),
        "real_life": _t(
            "Bank ka cheque: OCR account number padhta hai, VLM signature aur layout dekhta hai, aur "
            "rule engine amount verify karta hai. Ek model sab nahi karta.",
            "A bank cheque: OCR reads the account number, a VLM checks signature and layout, and a "
            "rule engine verifies the amount. One model does not do all of it.",
        ),
        "takeaway": _t(
            "Image ko model ke liye numbers ka grid samjho; pooling se size ghata kar compute bachao.",
            "Think of an image as a grid of numbers; pooling shrinks it to save compute.",
        ),
        "example": {
            "code": (
                "image = [[0, 2, 4, 6], [2, 4, 6, 8], [8, 6, 4, 2], [6, 4, 2, 0]]\n"
                "block = [image[y][x] for y in (0, 1) for x in (0, 1)]\n"
                "print(block, sum(block) / len(block))"
            ),
            "note": _t(
                "2×2 block ka average pooling ka pehla pixel hai.",
                "The 2×2 block average is the first pooled pixel.",
            ),
        },
        "exercise": {
            "prompt": _t(
                "`pool(image, k=2)` likho jo average pooling se image ko chhota kare; `small` ke "
                "dimensions aur pehla value print karo.",
                "Write `pool(image, k=2)` that downsizes an image with average pooling; print `small`'s "
                "dimensions and first value.",
            ),
            "starter": (
                "def pool(image, k=2):\n"
                "    ...\n\n"
                "image = [[0, 2, 4, 6], [2, 4, 6, 8], [8, 6, 4, 2], [6, 4, 2, 0]]\n"
                "small = pool(image, 2)\n"
                "print(len(small), len(small[0]), small[0][0])\n"
            ),
            "solution": (
                "def pool(image, k=2):\n"
                "    h, w = len(image), len(image[0])\n"
                "    out = []\n"
                "    for y in range(0, h, k):\n"
                "        row = []\n"
                "        for x in range(0, w, k):\n"
                "            block = [image[yy][xx] for yy in range(y, min(y + k, h)) for xx in range(x, min(x + k, w))]\n"
                "            row.append(sum(block) / len(block))\n"
                "        out.append(row)\n"
                "    return out\n\n"
                "image = [[0, 2, 4, 6], [2, 4, 6, 8], [8, 6, 4, 2], [6, 4, 2, 0]]\n"
                "small = pool(image, 2)\n"
                "print(len(small), len(small[0]), small[0][0])\n"
            ),
            "checks": [
                "len(small) == 2",
                "len(small[0]) == 2",
                "small[0][0] == 2.0",
            ],
            "hint": _t(
                "Outer loops `range(0, h, k)`, inner `range(0, w, k)`; block ka average lo.",
                "Outer loops `range(0, h, k)`, inner `range(0, w, k)`; average each block.",
            ),
        },
        "quiz": [
            {
                "q": _t("OCR aur VLM me farak?", "The difference between OCR and a VLM?"),
                "options": [
                    "OCR text nikalta hai; VLM layout aur meaning bhi samajhta hai",
                    "OCR sirf audio par chalta hai",
                    "VLM sirf numbers padhta hai",
                    "Dono bilkul same hain",
                ],
                "answer": "a",
                "why": _t(
                    "OCR characters deta hai; VLM poochh sakte hain 'ye invoice ka total kya hai?'",
                    "OCR gives characters; a VLM can answer 'what is this invoice total?'",
                ),
            },
            {
                "q": _t("CLIP kya karta hai?", "What does CLIP do?"),
                "options": [
                    "Image aur text ko ek hi embedding space me laata hai",
                    "Image ko compress karta hai",
                    "Audio ko text banata hai",
                    "Model ko quantise karta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Shared space me 'dog' ka text vector kutta wali image ke paas aata hai.",
                    "In the shared space the text vector for 'dog' sits near dog images.",
                ),
            },
            {
                "q": _t("ASR ka kaam?", "What does ASR do?"),
                "options": [
                    "Speech ko text me badalta hai",
                    "Text ko speech me badalta hai",
                    "Image ko text me badalta hai",
                    "Video ko frames me todta hai",
                ],
                "answer": "a",
                "why": _t(
                    "Automatic speech recognition = audio → text; TTS ulta kaam hai.",
                    "Automatic speech recognition is audio → text; TTS is the reverse.",
                ),
            },
        ],
    },
}
