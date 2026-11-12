"""Module 12 - Real projects: async, data files, tests, and one complete program."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m12"

l01 = lesson(
    "m12c01l01",
    L("async and await", "async और await", "async aur await"),
    ["async", "await"],
    L(
        "`async def` defines a coroutine: calling it does not run the body, it returns "
        "something you must await. `await` pauses this coroutine while the event loop "
        "does other work, which is how one thread waits on many slow operations.",
        "`async def` कोरूटीन बनाता है: बुलाने पर शरीर नहीं चलता, ऐसी चीज़ मिलती है जिसे "
        "await करना होता है। `await` इस कोरूटीन को रोकता है और इवेंट लूप दूसरा काम "
        "करता है, इसी तरह एक थ्रेड कई धीमे काम संभालता है।",
        "`async def` coroutine banata hai: bulane par body nahi chalta, aisi cheez "
        "milti hai jise await karna hota hai. `await` is coroutine ko rokta hai aur "
        "event loop doosra kaam karta hai, isi tarah ek thread kai dheeme kaam "
        "sambhalta hai.",
    ),
    L(
        "One waiter in a cafe. Instead of standing at the coffee machine until it "
        "finishes, the waiter starts it, takes another order, and comes back when the "
        "machine beeps - that is await.",
        "कैफ़े में एक वेटर। कॉफ़ी मशीन के पास खड़े रहने की जगह वेटर मशीन चालू करता है, "
        "दूसरा ऑर्डर लेता है, और मशीन बीप करने पर लौटता है - यही await है।",
        "Cafe me ek waiter. Coffee machine ke paas khade rehne ki jagah waiter machine "
        "chaalu karta hai, doosra order leta hai, aur machine beep karne par laut ta "
        "hai - yahi await hai.",
    ),
    "https://docs.python.org/3/library/asyncio-task.html",
    visual="async_tasks",
    examples=[
        ex(
            'import asyncio\n\nasync def fetch(name, delay):\n    await asyncio.sleep(delay)\n    return f"{name} done"\n\nasync def main():\n    results = await asyncio.gather(fetch("a", 0.02), fetch("b", 0.01))\n    print(results)\n\nasyncio.run(main())',
            "['a done', 'b done']",
            L("two coroutines at once", "दो कोरूटीन एक साथ", "do coroutines ek saath"),
            note=L(
                "`gather` starts both and waits for both. The results keep the order of "
                "the arguments, not the order they finished.",
                "`gather` दोनों शुरू करता है और दोनों का इंतज़ार करता है। परिणाम "
                "आर्ग्युमेंट के क्रम में रहते हैं, पूरा होने के क्रम में नहीं।",
                "`gather` dono shuru karta hai aur dono ka intezaar karta hai. Results "
                "arguments ke kram me rehte hain, poora hone ke kram me nahi.",
            ),
        ),
        ex(
            'import asyncio\n\nasync def step(n):\n    await asyncio.sleep(0)\n    return n * 2\n\nasync def main():\n    one = await step(1)\n    two = await step(2)\n    print(one, two)\n\nasyncio.run(main())',
            "2 4",
            L("await one step at a time", "एक-एक कदम await करना", "ek-ek kadam await karna"),
            note=L(
                "Sequential awaits run one after another. Use gather when the work is "
                "independent and can overlap.",
                "क्रमिक await एक के बाद एक चलते हैं। जब काम स्वतंत्र हो और साथ हो सके तो "
                "gather इस्तेमाल करें।",
                "Kramik await ek ke baad ek chalte hain. Jab kaam independent ho aur "
                "saath ho sake to gather use karo.",
            ),
        ),
        ex(
            'import asyncio\n\nasync def risky(n):\n    await asyncio.sleep(0)\n    if n < 0:\n        raise ValueError("negative input")\n    return n\n\nasync def main():\n    try:\n        await risky(-1)\n    except ValueError as exc:\n        print("caught:", exc)\n\nasyncio.run(main())',
            "caught: negative input",
            L("errors work the same way", "एरर वैसे ही काम करते हैं", "errors waise hi kaam karte hain"),
            note=L(
                "A coroutine raises like any function; the exception surfaces at the "
                "await point, so normal try/except is enough.",
                "कोरूटीन आम फ़ंक्शन की तरह एरर देता है; एरर await पर सामने आता है, "
                "इसलिए सामान्य try/except काफ़ी है।",
                "Coroutine aam function ki tarah error deta hai; error await par saamne "
                "aata hai, isliye normal try/except kaafi hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `async def double(n)` that awaits `asyncio.sleep(0)` and returns "
                "`n * 2`. Run it inside `main()` with `asyncio.run` and print the result "
                "for 21.",
                "`async def double(n)` लिखें जो `asyncio.sleep(0)` await करे और `n * 2` "
                "लौटाए। `main()` में `asyncio.run` से चलाएँ और 21 का परिणाम प्रिंट करें।",
                "`async def double(n)` likho jo `asyncio.sleep(0)` await kare aur `n * 2` "
                "return kare. `main()` me `asyncio.run` se chalao aur 21 ka result print karo.",
            ),
            "import asyncio\n\n# async def double(n): ...\n\nasync def main():\n    pass\n\n# asyncio.run(main())\n",
            'import asyncio\n\nasync def double(n):\n    await asyncio.sleep(0)\n    return n * 2\n\nasync def main():\n    result = await double(21)\n    print(result)\n\nasyncio.run(main())',
            [
                "asyncio.iscoroutinefunction(double)",
                "asyncio.run(double(5)) == 10",
                "printed.strip() == '42'",
            ],
            L(
                "await the call inside main; asyncio.run starts the event loop once.",
                "main के अंदर कॉल await करें; asyncio.run इवेंट लूप एक बार शुरू करता है।",
                "main ke andar call await karo; asyncio.run event loop ek baar shuru "
                "karta hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does calling an `async def` function return?",
                "`async def` फ़ंक्शन बुलाने पर क्या लौटता है?",
                "`async def` function bulane par kya return hota hai?",
            ),
            ["the result directly", "a coroutine object", "a thread", "None"],
            "b",
            L(
                "You must await it (or schedule it) for the body to run.",
                "शरीर चलाने के लिए इसे await करना (या शेड्यूल करना) होता है।",
                "Body chalane ke liye ise await karna (ya schedule karna) hota hai.",
            ),
        ),
        quiz(
            L(
                "What does `await` do?",
                "`await` क्या करता है?",
                "`await` kya karta hai?",
            ),
            [
                "blocks the whole program",
                "pauses this coroutine so the event loop can run others",
                "starts a new process",
                "sleeps for one second",
            ],
            "b",
            L(
                "That pause-and-resume is what makes concurrency possible in one thread.",
                "यही रुकना-फिर-चलना एक थ्रेड में समवर्ती काम संभव बनाता है।",
                "Yahi rukna-phir-chalna ek thread me concurrent kaam sambhav banata hai.",
            ),
        ),
        quiz(
            L(
                "When should you prefer `asyncio.gather`?",
                "`asyncio.gather` कब बेहतर है?",
                "`asyncio.gather` kab behtar hai?",
            ),
            [
                "when tasks depend on each other's results",
                "when independent tasks can run concurrently",
                "when you need threads",
                "when the function is not async",
            ],
            "b",
            L(
                "gather overlaps independent work and returns all results together.",
                "gather स्वतंत्र काम एक साथ चलाता है और सारे परिणाम एक साथ देता है।",
                "gather independent kaam ek saath chalata hai aur saare results ek saath "
                "deta hai.",
            ),
        ),
    ],
    takeaway=L(
        "async def + await for waiting on many things in one thread; gather when the tasks are independent.",
        "एक थ्रेड में कई चीज़ों के इंतज़ार के लिए async def + await; काम स्वतंत्र हों तो gather।",
        "Ek thread me kai cheezon ke intezaar ke liye async def + await; kaam independent hon to gather.",
    ),
)

l02 = lesson(
    "m12c01l02",
    L("CSV files", "CSV फ़ाइलें", "CSV files"),
    [],
    L(
        "CSV is rows of comma-separated text - the format every spreadsheet exports. "
        "The `csv` module handles quoting, commas inside values and line endings that "
        "hand-written split(\",\") code gets wrong.",
        "CSV अल्पविराम से अलग पंक्तियों वाला टेक्स्ट है - वही जो हर स्प्रेडशीट निर्यात "
        "करती है। `csv` मॉड्यूल कोटेशन, मान के अंदर के अल्पविराम और लाइन एंडिंग संभालता "
        "है जिन्हें हाथ से लिखा split(\",\") गलत करता है।",
        "CSV comma se alag lines wala text hai - wahi jo har spreadsheet export karti "
        "hai. `csv` module quoting, value ke andar ke comma aur line endings sambhalta "
        "hai jinhe haath se likha split(\",\") galat karta hai.",
    ),
    L(
        "An attendance register. One row per student, columns for name and present or "
        "absent - readable by a human and by Excel.",
        "उपस्थिति रजिस्टर। हर छात्र के लिए एक पंक्ति, नाम और उपस्थित/अनुपस्थित के कॉलम - "
        "इंसान भी पढ़ सके और एक्सेल भी।",
        "Upasthiti register. Har student ke liye ek row, naam aur present/absent ke "
        "columns - insaan bhi padh sake aur Excel bhi.",
    ),
    "https://docs.python.org/3/library/csv.html",
    examples=[
        ex(
            'import csv\nimport io\n\nraw = "name,score\\nAsha,9\\nRavi,7\\n"\nrows = list(csv.DictReader(io.StringIO(raw)))\nprint(rows[0]["name"], rows[0]["score"])\nprint(len(rows))\nprint([row["name"] for row in rows])',
            "Asha 9\n2\n['Asha', 'Ravi']",
            L("DictReader gives named columns", "DictReader नाम वाले कॉलम देता है", "DictReader naam wale columns deta hai"),
            note=L(
                "The first row becomes the field names, so you read row[\"score\"] "
                "instead of row[1]. Much harder to break when a column moves.",
                "पहली पंक्ति फ़ील्ड नाम बन जाती है, इसलिए row[\"score\"] पढ़ते हैं row[1] "
                "की जगह। कॉलम बदलने पर टूटना बहुत कम होता है।",
                "Pehli row field naam ban jati hai, isliye row[\"score\"] padhte ho row[1] "
                "ki jagah. Column badalne par tootna bahut kam hota hai.",
            ),
        ),
        ex(
            'import csv\nimport io\n\nbuffer = io.StringIO()\nwriter = csv.writer(buffer)\nwriter.writerow(["item", "qty"])\nwriter.writerow(["tea", 2])\nprint(buffer.getvalue().strip().replace("\\r\\n", " | "))',
            "item,qty | tea,2",
            L("writing rows", "पंक्तियाँ लिखना", "rows likhna"),
            note=L(
                "csv writes \\r\\n by default; the replace() here only makes the output "
                "print on one line for the lesson.",
                "csv डिफ़ॉल्ट रूप से \\r\\n लिखता है; यहाँ replace() सिर्फ़ पाठ के लिए "
                "आउटपुट एक पंक्ति में दिखाता है।",
                "csv default roop se \\r\\n likhta hai; yahan replace() sirf paath ke "
                "liye output ek line me dikhata hai.",
            ),
        ),
        ex(
            'import csv\nimport io\n\nraw = "item,qty\\ntea,2\\n\\"gift, small\\",1\\n"\nrows = list(csv.DictReader(io.StringIO(raw)))\nprint(len(rows))\nprint(rows[1]["item"])',
            "2\ngift, small",
            L("quoted commas survive", "कोटेशन वाले अल्पविराम बचे रहते हैं", "quoted comma bache rehte hain"),
            note=L(
                "A value containing a comma is wrapped in quotes. `split(\",\")` would "
                "have produced three broken fields here.",
                "अल्पविराम वाला मान कोटेशन में लिपटा होता है। यहाँ `split(\",\")` तीन "
                "टूटे फ़ील्ड बना देता।",
                "Comma wala value quotes me lipta hota hai. Yahan `split(\",\")` teen "
                "toote field bana deta.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Parse `'city,people\\nPune,7\\nDelhi,9\\n'` with DictReader into `rows` "
                "and print the people count of Delhi.",
                "`'city,people\\nPune,7\\nDelhi,9\\n'` को DictReader से `rows` में पढ़ें और "
                "Delhi की people संख्या प्रिंट करें।",
                "`'city,people\\nPune,7\\nDelhi,9\\n'` ko DictReader se `rows` me padho "
                "aur Delhi ki people sankhya print karo.",
            ),
            "import csv\nimport io\n\nraw = 'city,people\\nPune,7\\nDelhi,9\\n'\n# rows = ...\n",
            "import csv\nimport io\n\nraw = 'city,people\\nPune,7\\nDelhi,9\\n'\nrows = list(csv.DictReader(io.StringIO(raw)))\nprint(rows[1]['people'])",
            [
                "len(rows) == 2",
                "rows[0]['city'] == 'Pune'",
                "rows[1]['people'] == '9'",
                "printed.strip() == '9'",
            ],
            L(
                "CSV values arrive as strings, so '9' compares equal to '9'.",
                "CSV मान स्ट्रिंग के रूप में आते हैं, इसलिए '9' ही '9' के बराबर है।",
                "CSV values string ke roop me aate hain, isliye '9' hi '9' ke barabar hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does DictReader use as field names?",
                "DictReader फ़ील्ड नाम किससे लेता है?",
                "DictReader field naam kis se leta hai?",
            ),
            ["the first data row", "the first row of the file", "a schema argument", "the file name"],
            "b",
            L(
                "The header row becomes the keys of every later row.",
                "हेडर पंक्ति बाद की हर पंक्ति की कुंजियाँ बनती है।",
                "Header row baad ki har row ki keys banti hai.",
            ),
        ),
        quiz(
            L(
                "Why not split CSV lines on \",\" by hand?",
                "CSV पंक्तियों को हाथ से \",\" पर क्यों नहीं तोड़ें?",
                "CSV lines ko haath se \",\" par kyun na todein?",
            ),
            [
                "it is slower",
                "quoted values may contain commas and line breaks",
                "Python forbids it",
                "it loses the header",
            ],
            "b",
            L(
                "Quoting rules are the whole reason the csv module exists.",
                "कोटेशन के नियम ही csv मॉड्यूल होने की पूरी वजह हैं।",
                "Quoting ke niyam hi csv module hone ki poori wajah hain.",
            ),
        ),
        quiz(
            L(
                "What type is every value read by csv?",
                "csv से पढ़ा हर मान किस प्रकार का होता है?",
                "csv se padha har value kis prakar ka hota hai?",
            ),
            ["int", "str", "float", "it depends on the column"],
            "b",
            L(
                "Convert explicitly with int() or float() when you need numbers.",
                "संख्याएँ चाहिए तो int() या float() से स्पष्ट रूप से बदलें।",
                "Numbers chahiye to int() ya float() se saaf roop se badlo.",
            ),
        ),
    ],
    takeaway=L(
        "Use csv.DictReader/DictWriter and convert types yourself; never split on commas by hand.",
        "csv.DictReader/DictWriter इस्तेमाल करें और टाइप खुद बदलें; अल्पविराम पर हाथ से कभी न तोड़ें।",
        "csv.DictReader/DictWriter use karo aur type khud badlo; comma par haath se kabhi na todo.",
    ),
)

l03 = lesson(
    "m12c02l03",
    L("Testing your code", "अपने कोड की जाँच", "Apne code ki jaanch"),
    [],
    L(
        "A test is code that checks other code. `unittest` ships with Python: subclass "
        "TestCase, write methods starting with `test`, and use assertEqual, "
        "assertTrue and assertRaises. Tests are how you change code without fear.",
        "टेस्ट वह कोड है जो दूसरे कोड की जाँच करता है। `unittest` पायथन के साथ आता है: "
        "TestCase से सबक्लास बनाएँ, `test` से शुरू होने वाले मेथड लिखें, और assertEqual, "
        "assertTrue, assertRaises इस्तेमाल करें। टेस्ट ही बिना डर बदलाव करने देते हैं।",
        "Test woh code hai jo doosre code ki jaanch karta hai. `unittest` Python ke "
        "saath aata hai: TestCase se subclass banao, `test` se shuru hone wale methods "
        "likho, aur assertEqual, assertTrue, assertRaises use karo. Tests hi bina dar "
        "badlav karne dete hain.",
    ),
    L(
        "A checklist before a flight. The pilot does not trust memory; the checklist "
        "runs the same checks every time and catches what a tired human misses.",
        "उड़ान से पहले चेकलिस्ट। पायलट याददाश्त पर भरोसा नहीं करता; चेकलिस्ट हर बार वही "
        "जाँच चलाती है और वह पकड़ती है जो थका इंसान चूक जाता है।",
        "Udaan se pehle checklist. Pilot yaaddasht par bharosa nahi karta; checklist "
        "har baar wahi jaanch chalati hai aur woh pakadti hai jo thaka insaan chook "
        "jata hai.",
    ),
    "https://docs.python.org/3/library/unittest.html",
    examples=[
        ex(
            'import unittest\n\ndef add(a, b):\n    return a + b\n\nclass TestAdd(unittest.TestCase):\n    def test_positive(self):\n        self.assertEqual(add(2, 3), 5)\n\n    def test_negative(self):\n        self.assertEqual(add(-1, 1), 0)\n\nsuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAdd)\nresult = unittest.TextTestRunner(verbosity=0).run(suite)\nprint(result.wasSuccessful())\nprint(result.testsRun)',
            "True\n2",
            L("two tests, both green", "दो टेस्ट, दोनों पास", "do test, dono pass"),
            note=L(
                "The loader collects every test_ method from the class; the runner "
                "executes them. wasSuccessful is True only when all passed.",
                "लोडर क्लास के हर test_ मेथड को इकट्ठा करता है; रनर उन्हें चलाता है। "
                "wasSuccessful तभी True है जब सब पास हों।",
                "Loader class ke har test_ method ko ikattha karta hai; runner unhe "
                "chalata hai. wasSuccessful tabhi True hai jab sab pass hon.",
            ),
        ),
        ex(
            'import unittest\n\ndef safe_div(a, b):\n    if b == 0:\n        raise ZeroDivisionError("b must not be zero")\n    return a / b\n\nclass TestDiv(unittest.TestCase):\n    def test_ok(self):\n        self.assertEqual(safe_div(9, 3), 3.0)\n\n    def test_zero(self):\n        with self.assertRaises(ZeroDivisionError):\n            safe_div(1, 0)\n\nsuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDiv)\nresult = unittest.TextTestRunner(verbosity=0).run(suite)\nprint(result.wasSuccessful(), result.testsRun)',
            "True 2",
            L("testing the failure path too", "विफलता का रास्ता भी जाँचना", "vifalta ka raasta bhi jaanchna"),
            note=L(
                "assertRaises passes only if the block really raises. A test that never "
                "sees the error is as valuable as no test.",
                "assertRaises तभी पास होता है जब ब्लॉक सचमुच एरर दे। जो टेस्ट एरर देखता "
                "ही नहीं वह बिना टेस्ट जैसा है।",
                "assertRaises tabhi pass hota hai jab block sachmuch error de. Jo test "
                "error dekhta hi nahi woh bina test jaisa hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `square(n)` and a TestCase with one test that checks square(4) == "
                "16. Run it with exit=False and print wasSuccessful().",
                "`square(n)` लिखें और एक TestCase जिसमें एक टेस्ट square(4) == 16 जाँचे। "
                "exit=False से चलाएँ और wasSuccessful() प्रिंट करें।",
                "`square(n)` likho aur ek TestCase jisme ek test square(4) == 16 jaanche. "
                "exit=False se chalao aur wasSuccessful() print karo.",
            ),
            "import unittest\n\n# def square(n): ...\n# class TestSquare(unittest.TestCase): ...\n",
            "import unittest\n\ndef square(n):\n    return n * n\n\nclass TestSquare(unittest.TestCase):\n    def test_four(self):\n        self.assertEqual(square(4), 16)\n\nsuite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSquare)\nresult = unittest.TextTestRunner(verbosity=0).run(suite)\nprint(result.wasSuccessful())",
            [
                "square(4) == 16",
                "square(-3) == 9",
                "printed.strip() == 'True'",
            ],
            L(
                "The method name must start with test_; load the class, then run the suite.",
                "मेथड का नाम test_ से शुरू होना चाहिए; क्लास लोड करें, फिर सूट चलाएँ।",
                "Method ka naam test_ se shuru hona chahiye; class load karo, phir suite "
                "chalao.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which method names does unittest run automatically?",
                "unittest कौन से मेथड नाम अपने आप चलाता है?",
                "unittest kaun se method naam apne aap chalata hai?",
            ),
            ["any method", "methods starting with test", "methods ending with _test", "only setUp"],
            "b",
            L(
                "The `test` prefix is the discovery rule.",
                "`test` उपसर्ग ही खोज का नियम है।",
                "`test` prefix hi khoj ka niyam hai.",
            ),
        ),
        quiz(
            L(
                "Why write a test for the error path?",
                "एरर वाले रास्ते का टेस्ट क्यों लिखें?",
                "Error wale raaste ka test kyun likhein?",
            ),
            [
                "to increase the line count",
                "to prove the code fails in the intended way, not accidentally",
                "because unittest requires it",
                "to make the code faster",
            ],
            "b",
            L(
                "assertRaises documents and locks the contract for bad input.",
                "assertRaises गलत इनपुट के समझौते को लिखता और तय करता है।",
                "assertRaises galat input ke contract ko likhta aur tay karta hai.",
            ),
        ),
        quiz(
            L(
                "Which pair loads and runs a TestCase explicitly?",
                "कौन सा जोड़ा TestCase को स्पष्ट रूप से लोड और चलाता है?",
                "Kaun sa joda TestCase ko saaf roop se load aur chalata hai?",
            ),
            [
                "loadTestsFromTestCase + TextTestRunner",
                "TestCase + assertEqual",
                "unittest.main + argv",
                "setUp + tearDown",
            ],
            "a",
            L(
                "The loader builds a suite from the class; the runner executes it. This "
                "works the same in a notebook and in a file.",
                "लोडर क्लास से सूट बनाता है; रनर उसे चलाता है। यह नोटबुक और फ़ाइल दोनों "
                "में वैसे ही चलता है।",
                "Loader class se suite banata hai; runner use chalata hai. Ye notebook "
                "aur file dono me waise hi chalta hai.",
            ),
        ),
    ],
    takeaway=L(
        "Small tests, one behaviour each, including the failure path - that is what makes refactoring safe.",
        "छोटे टेस्ट, एक-एक व्यवहार, विफलता का रास्ता भी - इसी से बदलाव सुरक्षित होते हैं।",
        "Chhote test, ek-ek behaviour, vifalta ka raasta bhi - isi se badlav safe hote hain.",
    ),
)

l04 = lesson(
    "m12c02l04",
    L("Final project: an expense tracker", "अंतिम प्रोजेक्ट: खर्च ट्रैकर", "Final project: expense tracker"),
    [],
    L(
        "This lesson puts the whole book together: a dataclass for one expense, a "
        "class that owns a list of them, JSON for saving, and a comprehension for the "
        "report. Every piece was taught earlier; only the combination is new.",
        "यह पाठ पूरी किताब जोड़ता है: एक खर्च के लिए डेटाक्लास, उनकी सूची रखने वाली "
        "क्लास, सहेजने के लिए JSON, और रिपोर्ट के लिए कॉम्प्रिहेंशन। हर हिस्सा पहले "
        "आया है; सिर्फ़ जोड़ नया है।",
        "Ye paath poori kitaab jodta hai: ek kharch ke liye dataclass, unki list rakhne "
        "wali class, save karne ke liye JSON, aur report ke liye comprehension. Har "
        "hissa pehle aaya hai; sirf jod naya hai.",
    ),
    L(
        "A notebook where you write every tea, auto and grocery spend. At month end you "
        "want the total, the biggest category and a file you can reopen next month.",
        "एक नोटबुक जिसमें आप हर चाय, ऑटो और किराने का खर्च लिखते हैं। महीने के अंत में "
        "कुल, सबसे बड़ी श्रेणी और अगले महीने खोलने लायक फ़ाइल चाहिए।",
        "Ek notebook jisme aap har chai, auto aur kirane ka kharch likhte ho. Mahine ke "
        "ant me total, sabse badi category aur agle mahine kholne layak file chahiye.",
    ),
    "https://docs.python.org/3/tutorial/stdlib.html",
    examples=[
        ex(
            'import json\nfrom dataclasses import dataclass, asdict\n\n@dataclass\nclass Expense:\n    title: str\n    amount: int\n    category: str = "other"\n\nexpense = Expense("notebook", 250, "study")\nprint(expense)\nprint(json.dumps(asdict(expense), sort_keys=True))',
            "Expense(title='notebook', amount=250, category='study')\n{\"amount\": 250, \"category\": \"study\", \"title\": \"notebook\"}",
            L("one expense as a dataclass", "एक खर्च डेटाक्लास के रूप में", "ek kharch dataclass ke roop me"),
            note=L(
                "`asdict` turns a dataclass into a plain dict, which json can write. "
                "That pair is the whole persistence layer.",
                "`asdict` डेटाक्लास को सादा dict बनाता है जिसे json लिख सकता है। यही जोड़ी "
                "पूरी सहेजने की परत है।",
                "`asdict` dataclass ko saada dict banata hai jise json likh sakta hai. "
                "Yahi jodi poori save karne ki parat hai.",
            ),
        ),
        ex(
            'import json\n\nrows = [{"title": "tea", "amount": 30, "category": "food"}, {"title": "book", "amount": 250, "category": "study"}]\ntotal = sum(row["amount"] for row in rows)\nby_category = {}\nfor row in rows:\n    by_category[row["category"]] = by_category.get(row["category"], 0) + row["amount"]\nprint(f"total: {total}")\nprint(by_category)\nprint(json.dumps({"total": total, "count": len(rows)}, sort_keys=True))',
            "total: 280\n{'food': 30, 'study': 250}\n{\"count\": 2, \"total\": 280}",
            L("the monthly report", "महीने की रिपोर्ट", "mahine ki report"),
            note=L(
                "Sum for the total, a dict for per-category totals, json for the file. "
                "Three lines you have already seen, combined.",
                "कुल के लिए sum, श्रेणी-वार के लिए dict, फ़ाइल के लिए json। तीन पंक्तियाँ "
                "जो पहले देख चुके हैं, जुड़ी हुई।",
                "Total ke liye sum, category-wise ke liye dict, file ke liye json. Teen "
                "lines jo pehle dekh chuke ho, judi hui.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Finish the tracker: `total(rows)` returns the sum of amounts, "
                "`biggest(rows)` returns the title with the largest amount. Print both "
                "for the sample rows.",
                "ट्रैकर पूरा करें: `total(rows)` रकमों का योग लौटाए, `biggest(rows)` सबसे "
                "बड़ी रकम वाला title लौटाए। नमूना पंक्तियों के लिए दोनों प्रिंट करें।",
                "Tracker poora karo: `total(rows)` amounts ka sum return kare, "
                "`biggest(rows)` sabse badi amount wala title return kare. Sample rows "
                "ke liye dono print karo.",
            ),
            'rows = [\n    {"title": "tea", "amount": 30},\n    {"title": "book", "amount": 250},\n]\n\ndef total(rows):\n    pass\n\ndef biggest(rows):\n    pass\n\n# print(total(rows))\n# print(biggest(rows))\n',
            'rows = [\n    {"title": "tea", "amount": 30},\n    {"title": "book", "amount": 250},\n]\n\ndef total(rows):\n    return sum(row["amount"] for row in rows)\n\ndef biggest(rows):\n    return max(rows, key=lambda row: row["amount"])["title"]\n\nprint(total(rows))\nprint(biggest(rows))',
            [
                "total(rows) == 280",
                "biggest(rows) == 'book'",
                "total([]) == 0",
                "printed.split() == ['280', 'book']",
            ],
            L(
                "sum() with a generator for the total; max() with key= for the biggest.",
                "कुल के लिए जनरेटर के साथ sum(); सबसे बड़े के लिए key= के साथ max()।",
                "Total ke liye generator ke saath sum(); sabse bade ke liye key= ke saath "
                "max().",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which pair saves a dataclass as JSON?",
                "डेटाक्लास को JSON में कौन सा जोड़ा सहेजता है?",
                "Dataclass ko JSON me kaun sa joda save karta hai?",
            ),
            ["str() and eval()", "asdict() and json.dumps()", "repr() and print()", "pickle and csv"],
            "b",
            L(
                "asdict gives a plain dict, json.dumps gives text.",
                "asdict सादा dict देता है, json.dumps टेक्स्ट।",
                "asdict saada dict deta hai, json.dumps text.",
            ),
        ),
        quiz(
            L(
                "Why keep expenses in a list of dicts instead of separate variables?",
                "खर्चों को अलग वेरिएबल की जगह dict की सूची में क्यों रखें?",
                "Khrchon ko alag variable ki jagah dict ki list me kyun rakhein?",
            ),
            [
                "it uses less memory",
                "loops, sum and json all work on a collection without new code",
                "dicts are faster than ints",
                "separate variables cannot be printed",
            ],
            "b",
            L(
                "A collection scales from two rows to two thousand with no code change.",
                "संग्रह दो पंक्तियों से दो हज़ार तक बिना कोड बदले चलता है।",
                "Collection do rows se do hazaar tak bina code badle chalta hai.",
            ),
        ),
        quiz(
            L(
                "What does `max(rows, key=lambda r: r[\"amount\"])` return?",
                "`max(rows, key=lambda r: r[\"amount\"])` क्या लौटाता है?",
                "`max(rows, key=lambda r: r[\"amount\"])` kya return karta hai?",
            ),
            ["the largest number", "the whole row with the largest amount", "the index", "None"],
            "b",
            L(
                "max returns the item, not the key value. Add [\"title\"] to get just the name.",
                "max आइटम लौटाता है, कुंजी का मान नहीं। सिर्फ़ नाम के लिए [\"title\"] जोड़ें।",
                "max item return karta hai, key ki value nahi. Sirf naam ke liye [\"title\"] "
                "jodo.",
            ),
        ),
    ],
    takeaway=L(
        "Small pieces you already know - dataclass, list, sum, json - combine into a real tool.",
        "जो छोटे हिस्से आप जानते हैं - डेटाक्लास, सूची, sum, json - वे मिलकर असली औज़ार बनते हैं।",
        "Jo chhote hisse aap jaante ho - dataclass, list, sum, json - wo milkar asli auzar bante hain.",
    ),
)

MODULE = module(
    M,
    L("Real Projects", "असली प्रोजेक्ट", "Asli Projects"),
    L(
        "Concurrency with async/await, reading and writing CSV, testing with unittest, "
        "and one complete expense tracker that uses everything.",
        "async/await से समवर्ती काम, CSV पढ़ना-लिखना, unittest से जाँच, और सब कुछ "
        "इस्तेमाल करने वाला एक पूरा खर्च ट्रैकर।",
        "async/await se concurrent kaam, CSV padhna-likhna, unittest se jaanch, aur sab "
        "kuch use karne wala ek poora expense tracker.",
    ),
    [
        chapter("m12c01", L("Waiting and data files", "इंतज़ार और डेटा फ़ाइलें", "Intezaar aur data files"), [l01, l02]),
        chapter("m12c02", L("Quality and a real program", "गुणवत्ता और असली प्रोग्राम", "Quality aur asli program"), [l03, l04]),
    ],
    exam=[
        quiz(
            L("What does async def create?", "async def क्या बनाता है?", "async def kya banata hai?"),
            ["a thread", "a coroutine function", "a generator only", "a class"],
            "b",
            L("Calling it returns a coroutine object to await.", "बुलाने पर await करने लायक कोरूटीन ऑब्जेक्ट मिलता है।", "Bulane par await karne layak coroutine object milta hai."),
        ),
        quiz(
            L("Which reader gives named columns?", "कौन नाम वाले कॉलम देता है?", "Kaun naam wale columns deta hai?"),
            ["csv.reader", "csv.DictReader", "csv.writer", "csv.Sniffer"],
            "b",
            L("DictReader maps the header row to keys.", "DictReader हेडर पंक्ति को कुंजियाँ बनाता है।", "DictReader header row ko keys banata hai."),
        ),
        quiz(
            L("Which assertion checks that a call raises?", "कौन सा assertion जाँचता है कि कॉल एरर देती है?", "Kaun sa assertion jaanchta hai ki call error deti hai?"),
            ["assertEqual", "assertRaises", "assertTrue", "assertIn"],
            "b",
            L("Use it as a context manager around the failing call.", "इसे विफल होने वाली कॉल के चारों ओर कॉन्टेक्स्ट मैनेजर की तरह इस्तेमाल करें।", "Ise fail hone wali call ke chaaron or context manager ki tarah use karo."),
        ),
        quiz(
            L("Which pair runs a TestCase without unittest.main?", "unittest.main के बिना TestCase कौन सा जोड़ा चलाता है?", "unittest.main ke bina TestCase kaun sa joda chalata hai?"),
            ["loadTestsFromTestCase + TextTestRunner", "assertEqual + setUp", "TestCase + main", "csv + json"],
            "a",
            L("Loader then runner: explicit and notebook-safe.", "पहले लोडर फिर रनर: स्पष्ट और नोटबुक-सुरक्षित।", "Pehle loader phir runner: saaf aur notebook-safe."),
        ),
        quiz(
            L("Which converts a dataclass to a dict?", "डेटाक्लास को dict में कौन बदलता है?", "Dataclass ko dict me kaun badalta hai?"),
            ["dataclasses.asdict", "dict(obj)", "obj.dict()", "json.loads(obj)"],
            "a",
            L("asdict recurses into nested dataclasses too.", "asdict नेस्टेड डेटाक्लास में भी जाता है।", "asdict nested dataclasses me bhi jata hai."),
        ),
        quiz(
            L("When is gather the right call?", "gather कब सही कॉल है?", "gather kab sahi call hai?"),
            ["when each step needs the previous result", "when independent coroutines can overlap", "when you want threads", "when there is one coroutine"],
            "b",
            L("Independent work overlaps; dependent work awaits in order.", "स्वतंत्र काम साथ चलता है; निर्भर काम क्रम में await होता है।", "Independent kaam saath chalta hai; dependent kaam kram me await hota hai."),
        ),
    ],
    icon="🚀",
)
