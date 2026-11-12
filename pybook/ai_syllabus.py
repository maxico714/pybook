"""The AI-engineering course: 23 chapters in 5 parts, plus one exam per part.

The chapter text and examples come from ``C:\\project\\aie-app\\notebooks`` and
``C:\\project\\ai-engineering-course``; this package holds the teachable layer and
the question banks.  :mod:`pybook.build_ai_course` merges them, runs every
example and exercise, and writes ``pybook/data/ai``.
"""
from __future__ import annotations

from .ai_lessons_a import LESSONS as _A
from .ai_lessons_b import LESSONS as _B
from .ai_lessons_c import LESSONS as _C


def _t(hinglish: str, en: str) -> dict:
    return {"hinglish": hinglish, "en": en}


LESSONS = {}
LESSONS.update(_A)
LESSONS.update(_B)
LESSONS.update(_C)

# id, part label, title, icon, chapter numbers, and the source notebook stem.
MODULES = [
    {
        "id": "m01",
        "part": "Part A",
        "title": _t("Foundations", "Foundations"),
        "goal": _t(
            "Setup, Python, math, data aur databases — woh base jis par poora AI engineering khada hai.",
            "Setup, Python, math, data and databases: the base every AI system stands on.",
        ),
        "icon": "🧱",
        "chapters": [1, 2, 3, 4, 5],
    },
    {
        "id": "m02",
        "part": "Part B",
        "title": _t("ML aur deep learning", "ML and deep learning"),
        "goal": _t(
            "Classical ML se PyTorch tak, aur attention tak — model ke andar kya hota hai.",
            "From classical ML through PyTorch to attention: what happens inside a model.",
        ),
        "icon": "🧠",
        "chapters": [6, 7, 8],
    },
    {
        "id": "m03",
        "part": "Part C",
        "title": _t("LLM engineering", "LLM engineering"),
        "goal": _t(
            "LLM behaviour, APIs, prompts, RAG, agents aur evaluation — roz ka LLM kaam.",
            "LLM behaviour, APIs, prompts, RAG, agents and evaluation: the daily LLM work.",
        ),
        "icon": "🤖",
        "chapters": [9, 10, 11, 12, 13, 14],
    },
    {
        "id": "m04",
        "part": "Part D",
        "title": _t("Specialisation aur production", "Specialisation and production"),
        "goal": _t(
            "Fine-tuning, multimodal, data quality, serving, MLOps, safety aur system design.",
            "Fine-tuning, multimodal, data quality, serving, MLOps, safety and system design.",
        ),
        "icon": "🚀",
        "chapters": [15, 16, 17, 18, 19, 20, 21],
    },
    {
        "id": "m05",
        "part": "Part E",
        "title": _t("Career aur capstones", "Career and capstones"),
        "goal": _t(
            "Interview, portfolio, freelancing aur paanch capstones jo proof dikhate hain.",
            "Interviews, portfolio, freelancing and five capstones that show proof.",
        ),
        "icon": "🎯",
        "chapters": [22, 23],
    },
]


EXAMS = {
    "m01": [
        {
            "q": _t("API key kahan rakhi jati hai?", "Where does an API key belong?"),
            "options": ["`.env` me, git se bahar", "Python constant me", "README me", "Test file me"],
            "answer": "a",
            "why": _t("`.env` + `.gitignore` standard hai; code me key leak ka rasta hai.", "`.env` plus `.gitignore` is the standard; a key in code is a leak."),
        },
        {
            "q": _t("Type hints ka fayda?", "The benefit of type hints?"),
            "options": ["Galtiyan jaldi pakadte hain", "Runtime 2x fast", "Model select karte hain", "Key hide karte hain"],
            "answer": "a",
            "why": _t("Static tools aur editor galat shapes pehle pakadte hain.", "Static tools and editors catch wrong shapes earlier."),
        },
        {
            "q": _t("Cosine similarity kya naapti hai?", "What does cosine similarity measure?"),
            "options": ["Vectors ke beech ka angle", "Vectors ki length", "Data ka size", "Model ka cost"],
            "answer": "a",
            "why": _t("Direction compare hoti hai, magnitude nahi.", "It compares direction, not magnitude."),
        },
        {
            "q": _t("Data leakage ka example?", "An example of data leakage?"),
            "options": ["Test ka mean training me use karna", "CSV load karna", "Model save karna", "Index banana"],
            "answer": "a",
            "why": _t("Test ki information training me aana leakage hai.", "Test information entering training is leakage."),
        },
        {
            "q": _t("ANN index kya karta hai?", "What does an ANN index do?"),
            "options": ["Approximate nearest neighbours jaldi dhoondhta hai", "Saare vectors exact scan karta hai", "SQL join karta hai", "Model train karta hai"],
            "answer": "a",
            "why": _t("Speed ke liye thodi accuracy trade hoti hai.", "It trades a little accuracy for speed."),
        },
        {
            "q": _t("Virtual environment kya deta hai?", "What does a virtual environment give you?"),
            "options": ["Project ke packages ki isolation", "Faster Python", "Free API credits", "Automatic tests"],
            "answer": "a",
            "why": _t("Isolation reproducible setup ka base hai.", "Isolation is the base of a reproducible setup."),
        },
    ],
    "m02": [
        {
            "q": _t("Overfit ka signal?", "The signal of overfitting?"),
            "options": ["Train score bahut high, test low", "Train aur test dono low", "Loss zero se start", "Learning rate chhota"],
            "answer": "a",
            "why": _t("Bada gap variance ki nishani hai.", "A large gap signals variance."),
        },
        {
            "q": _t("Screening ke liye pehla metric?", "The first metric for screening?"),
            "options": ["Recall", "Precision", "Accuracy", "AUC sirf"],
            "answer": "a",
            "why": _t("Positive miss karna sabse mehnga hai.", "Missing a positive is the costliest error."),
        },
        {
            "q": _t("Gradient descent kis direction me jata hai?", "Which direction does gradient descent go?"),
            "options": ["Gradient ke opposite", "Gradient ke saath", "Random", "Sirf bias update"],
            "answer": "a",
            "why": _t("Opposite direction loss kam karta hai.", "The opposite direction lowers the loss."),
        },
        {
            "q": _t("Autograd kya deta hai?", "What does autograd provide?"),
            "options": ["Automatic gradients", "Automatic data cleaning", "Automatic deployment", "Automatic tokenisation"],
            "answer": "a",
            "why": _t("Chain rule se backward pass gradients deta hai.", "It computes gradients on the backward pass via the chain rule."),
        },
        {
            "q": _t("Attention me `sqrt(d)` scaling kyun?", "Why scale attention by `sqrt(d)`?"),
            "options": ["Softmax saturation rokne ke liye", "Model chhota karne ke liye", "Tokens kam karne ke liye", "GPU ke liye"],
            "answer": "a",
            "why": _t("Bade dot products softmax ko ek token par chipka dete hain.", "Large dot products saturate the softmax on one token."),
        },
        {
            "q": _t("BPE kya karta hai?", "What does BPE do?"),
            "options": ["Subword tokens banata hai", "Har word ek token", "Text delete karta hai", "Embeddings train karta hai"],
            "answer": "a",
            "why": _t("Subwords se vocabulary chhota aur rare words handle hote hain.", "Subwords keep the vocabulary small and handle rare words."),
        },
    ],
    "m03": [
        {
            "q": _t("Temperature 0 kya karta hai?", "What does temperature 0 do?"),
            "options": ["Greedy decoding", "Random sampling", "Model off", "Translation"],
            "answer": "a",
            "why": _t("Sabse likely token deterministic hota hai.", "The most likely token becomes deterministic."),
        },
        {
            "q": _t("429 par kya karein?", "What should you do on a 429?"),
            "options": ["Backoff + jitter ke saath retry", "Turant 100 retry", "Request delete", "Model badal do"],
            "answer": "a",
            "why": _t("Rate limit ko respect karna zaroori hai.", "You must respect the rate limit."),
        },
        {
            "q": _t("Context budget ka matlab?", "What is a context budget?"),
            "options": ["Tokens ki fixed jagah jise manage karna hai", "Paisa", "Model ka size", "Database ki limit"],
            "answer": "a",
            "why": _t("Har token jagah aur keemat leta hai.", "Every token takes space and cost."),
        },
        {
            "q": _t("RAG me recall@k kya batata hai?", "What does recall@k show in RAG?"),
            "options": ["Sahi evidence top-k me aaya", "Answer ki length", "Model ki speed", "Embedding size"],
            "answer": "a",
            "why": _t("Evidence na mile to answer grounded nahi ho sakta.", "Without evidence the answer cannot be grounded."),
        },
        {
            "q": _t("Agent me max steps kyun?", "Why max steps in an agent?"),
            "options": ["Loop aur cost blow-up rokne ke liye", "Model smart karne ke liye", "Tool speed ke liye", "Prompt chhota karne ke liye"],
            "answer": "a",
            "why": _t("Cap ke bina bug poora budget kha sakta hai.", "Without a cap a bug can eat the budget."),
        },
        {
            "q": _t("Eval CI me kyun?", "Why evals in CI?"),
            "options": ["Regression merge se pehle pakadne ke liye", "CI busy rakhne ke liye", "Model train karne ke liye", "GPU free karne ke liye"],
            "answer": "a",
            "why": _t("Eval regression test hai.", "Evals are regression tests."),
        },
    ],
    "m04": [
        {
            "q": _t("Fine-tune ka sahi order?", "The right order for fine-tuning?"),
            "options": ["Prompt → RAG → fine-tune", "Fine-tune → prompt → RAG", "RAG → fine-tune → prompt", "Sirf fine-tune"],
            "answer": "a",
            "why": _t("Sasta aur reversible pehle.", "Cheapest and most reversible first."),
        },
        {
            "q": _t("LoRA kya train karta hai?", "What does LoRA train?"),
            "options": ["Chhote adapter matrices", "Poore model ke weights", "Sirf embeddings", "Tokenizer"],
            "answer": "a",
            "why": _t("Base frozen rehta hai; adapters chhote hote hain.", "The base stays frozen; adapters are small."),
        },
        {
            "q": _t("Kappa 0.4 ka matlab?", "What does kappa 0.4 mean?"),
            "options": ["Annotation agreement kam hai, guideline clear karo", "Model perfect hai", "Data balanced hai", "Eval pass hai"],
            "answer": "a",
            "why": _t("Low kappa ambiguity dikhata hai.", "Low kappa shows ambiguity."),
        },
        {
            "q": _t("Token bucket kya karta hai?", "What does a token bucket do?"),
            "options": ["Rate limit lagata hai", "Model train karta hai", "Prompt cache karta hai", "Data dedup karta hai"],
            "answer": "a",
            "why": _t("Time ke saath refill aur cost par allow.", "It refills over time and allows by cost."),
        },
        {
            "q": _t("Drift kya hai?", "What is drift?"),
            "options": ["Input distribution ka badalna", "Model file ka bada hona", "API price", "Prompt translation"],
            "answer": "a",
            "why": _t("Real data training data se alag hota jata hai.", "Real data moves away from training data."),
        },
        {
            "q": _t("Prompt injection ka best defence?", "The best defence against prompt injection?"),
            "options": ["Untrusted content ko data maano, instruction nahi", "Temperature 0", "Bada model", "Lamba prompt"],
            "answer": "a",
            "why": _t("Instruction aur data ka separation base hai.", "Separating instructions from data is the base."),
        },
    ],
    "m05": [
        {
            "q": _t("STAR ka R kya hai?", "What is the R in STAR?"),
            "options": ["Result", "Review", "Repeat", "Risk"],
            "answer": "a",
            "why": _t("Answer result par khatam hona chahiye.", "The answer should end on the result."),
        },
        {
            "q": _t("Portfolio me kya dikhana chahiye?", "What should a portfolio show?"),
            "options": ["Demo + eval numbers", "Sirf code lines", "Frameworks ki list", "Certificate"],
            "answer": "a",
            "why": _t("Proof demo aur measurement se aata hai.", "Proof comes from a demo and measurement."),
        },
        {
            "q": _t("Capstone ka pehla step?", "The first capstone step?"),
            "options": ["Thin end-to-end slice", "Poora UI", "Saare providers", "Fine-tuning"],
            "answer": "a",
            "why": _t("Ek document se grounded answer tak pehle.", "One document to a grounded answer first."),
        },
        {
            "q": _t("Faithfulness kya check karta hai?", "What does faithfulness check?"),
            "options": ["Answer context se supported hai", "Answer lamba hai", "Model bada hai", "API sasta hai"],
            "answer": "a",
            "why": _t("Grounded answer ke claims context me hone chahiye.", "Claims in a grounded answer must be in the context."),
        },
        {
            "q": _t("Cost per 1k requests kyun?", "Why cost per 1k requests?"),
            "options": ["Scale par asli cost dikhta hai", "Model train hota hai", "Prompt chhota hota hai", "Latency badhti hai"],
            "answer": "a",
            "why": _t("Ek request sasta lagta hai; 1k par number saaf dikhta hai.", "One request looks cheap; 1k shows the real number."),
        },
        {
            "q": _t("Take-home me kya likhna chahiye?", "What should a take-home include?"),
            "options": ["Scope aur trade-offs", "Sirf code", "Sirf screenshot", "Kuch nahi"],
            "answer": "a",
            "why": _t("Time-box aur trade-offs senior signal hain.", "A time-box and trade-offs signal seniority."),
        },
    ],
}
