"""Module 9 - Comprehensions, iterators and generators: building sequences lazily."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m09"

l01 = lesson(
    "m09c01l01",
    L("Comprehensions", "कॉम्प्रिहेंशन", "Comprehensions"),
    [],
    L(
        "A comprehension builds a list, dict or set from a loop in one expression: "
        "`[expression for item in iterable if condition]`. It is the same work as a "
        "loop with append, written in one readable line.",
        "कॉम्प्रिहेंशन एक लूप से एक ही अभिव्यक्ति में सूची, dict या सेट बनाता है: "
        "`[expression for item in iterable if condition]`। यह वही काम है जो append "
        "वाले लूप से होता है, पर ेक पढ़ने योग्य पंक्ति में।",
        "Comprehension ek loop se ek hi expression me list, dict ya set banata hai: "
        "`[expression for item in iterable if condition]`. Ye wahi kaam hai jo append "
        "wale loop se hota hai, par ek padhne yogya line me.",
    ),
    L(
        "A wedding invitation list. Instead of copying names one by one, you say "
        "\"every cousin who lives in the same city\" - one rule, whole list.",
        "शादी की निमंत्रण सूची। एक-एक नाम कॉपी करने की जगह आप कहते हैं \"हर वह कज़िन जो "
        "इसी शहर में रहता है\" - एक नियम, पूरी सूची।",
        "Shaadi ki nimantran list. Ek-ek naam copy karne ki jagah aap kehte ho \"har "
        "wo cousin jo isi shehar me rehta hai\" - ek niyam, poori list.",
    ),
    "https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions",
    visual="comprehension",
    examples=[
        ex(
            "squares = [n * n for n in range(1, 6)]\nprint(squares)\n\neven_squares = [n * n for n in range(1, 11) if n % 2 == 0]\nprint(even_squares)",
            "[1, 4, 9, 16, 25]\n[4, 16, 36, 64, 100]",
            L("with and without a filter", "फ़िल्टर के साथ और बिना", "filter ke saath aur bina"),
            note=L(
                "Read it as: build n*n, for each n in the range, keeping only even n. "
                "The `if` comes after the loop, not before it.",
                "इसे ऐसे पढ़ें: n*n बनाओ, रेंज के हर n के लिए, सिर्फ़ सम n रखो। `if` "
                "लूप के बाद आता है, पहले नहीं।",
                "Ise aise padho: n*n banao, range ke har n ke liye, sirf even n rakho. "
                "`if` loop ke baad aata hai, pehle nahi.",
            ),
        ),
        ex(
            'words = ["apple", "banana", "cherry"]\nlengths = {word: len(word) for word in words}\nprint(lengths)\nprint({len(word) for word in words})',
            "{'apple': 5, 'banana': 6, 'cherry': 6}\n{5, 6}",
            L("dict and set comprehensions", "dict और set कॉम्प्रिहेंशन", "dict aur set comprehensions"),
            note=L(
                "A dict comprehension needs `key: value` before `for`. A set "
                "comprehension uses braces without a colon and removes duplicates.",
                "dict कॉम्प्रिहेंशन में `for` से पहले `key: value` चाहिए। set "
                "कॉम्प्रिहेंशन में बिना कोलन के ब्रेसिज़ होते हैं और दोहराव हट जाता है।",
                "dict comprehension me `for` se pehle `key: value` chahiye. set "
                "comprehension me bina colon ke braces hote hain aur duplicate hat "
                "jata hai.",
            ),
        ),
        ex(
            "rows = [[1, 2], [3, 4], [5, 6]]\nflat = [n for row in rows for n in row]\nprint(flat)\nprint([n * 10 for row in rows for n in row if n > 2])",
            "[1, 2, 3, 4, 5, 6]\n[30, 40, 50, 60]",
            L("two loops in one comprehension", "एक कॉम्प्रिहेंशन में दो लूप", "ek comprehension me do loops"),
            note=L(
                "The loops stay in the same order as nested for loops: outer first. If "
                "you need three levels, a normal loop is usually easier to read.",
                "लूप वही क्रम रखते हैं जो नेस्टेड for में होता है: बाहरी पहले। तीन "
                "स्तर चाहिए तो सामान्य लूप ज़्यादा पढ़ने योग्य होता है।",
                "Loops wahi kram rakhte hain jo nested for me hota hai: outer pehle. "
                "Teen level chahiye to normal loop zyada padhne yogya hota hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Build `shout` = every name in `['asha', 'ravi', 'mili']` in upper case, "
                "using one comprehension. Print it.",
                "एक कॉम्प्रिहेंशन से `shout` बनाएँ = `['asha', 'ravi', 'mili']` के हर नाम "
                "का अपर केस। उसे प्रिंट करें।",
                "Ek comprehension se `shout` banao = `['asha', 'ravi', 'mili']` ke har "
                "naam ka upper case. Use print karo.",
            ),
            "names = ['asha', 'ravi', 'mili']\n# shout = [...]\n# print(shout)\n",
            "names = ['asha', 'ravi', 'mili']\nshout = [name.upper() for name in names]\nprint(shout)",
            [
                "shout == ['ASHA', 'RAVI', 'MILI']",
                "names == ['asha', 'ravi', 'mili']",
                "printed.strip() == \"['ASHA', 'RAVI', 'MILI']\"",
            ],
            L(
                "The expression comes first: name.upper() for name in names.",
                "अभिव्यक्ति पहले आती है: name.upper() for name in names।",
                "Expression pehle aati hai: name.upper() for name in names.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which order is correct in a comprehension?",
                "कॉम्प्रिहेंशन में सही क्रम कौन है?",
                "Comprehension me sahi kram kaun hai?",
            ),
            [
                "for item in items if cond expression",
                "expression for item in items if cond",
                "if cond expression for item in items",
                "expression if cond for item in items",
            ],
            "b",
            L(
                "Expression first, then the loop, then the optional filter.",
                "पहले अभिव्यक्ति, फिर लूप, फिर वैकल्पिक फ़िल्टर।",
                "Pehle expression, phir loop, phir optional filter.",
            ),
        ),
        quiz(
            L(
                "What does `{n for n in [1, 1, 2]}` produce?",
                "`{n for n in [1, 1, 2]}` क्या देता है?",
                "`{n for n in [1, 1, 2]}` kya deta hai?",
            ),
            ["{1, 1, 2}", "{1, 2}", "[1, 2]", "{'1': 1, '2': 2}"],
            "b",
            L(
                "Braces without colons make a set, and sets drop duplicates.",
                "बिना कोलन के ब्रेसिज़ set बनाते हैं, और set दोहराव हटा देता है।",
                "Bina colon ke braces set banate hain, aur set duplicate hata deta hai.",
            ),
        ),
        quiz(
            L(
                "When is a comprehension a bad choice?",
                "कॉम्प्रिहेंशन कब गलत चुनाव है?",
                "Comprehension kab galat choice hai?",
            ),
            [
                "when the result has fewer than ten items",
                "when the logic needs several statements or side effects",
                "when you filter with if",
                "when the input is a dict",
            ],
            "b",
            L(
                "A comprehension is one expression. If you need prints, appends or "
                "branches, write a loop.",
                "कॉम्प्रिहेंशन एक अभिव्यक्ति है। प्रिंट, append या शाखाएँ चाहिए तो लूप "
                "लिखें।",
                "Comprehension ek expression hai. Print, append ya branches chahiye to "
                "loop likho.",
            ),
        ),
    ],
    takeaway=L(
        "expression for item in iterable if condition - one line, one purpose.",
        "expression for item in iterable if condition - एक पंक्ति, एक मक़सद।",
        "expression for item in iterable if condition - ek line, ek maksad.",
    ),
)

l02 = lesson(
    "m09c01l02",
    L("Iterators: iter and next", "इटरेटर: iter और next", "Iterators: iter aur next"),
    ["for", "in"],
    L(
        "An iterable can hand out an iterator. The iterator remembers where it is and "
        "gives one item per `next()` call, then raises StopIteration. A `for` loop is "
        "exactly that loop written for you.",
        "इटरेबल एक इटरेटर दे सकता है। इटरेटर याद रखता है वह कहाँ है और हर `next()` कॉल "
        "पर एक आइटम देता है, फिर StopIteration उठाता है। `for` लूप वही चीज़ आपके लिए "
        "लिखा हुआ है।",
        "Iterable ek iterator de sakta hai. Iterator yaad rakhta hai woh kahan hai aur "
        "har `next()` call par ek item deta hai, phir StopIteration uthata hai. `for` "
        "loop wahi cheez aapke liye likha hua hai.",
    ),
    L(
        "A ticket roll at a counter. The roll is the iterable; the current position is "
        "the iterator. Each tear gives one ticket, and when the roll ends there is "
        "nothing left to give.",
        "काउंटर पर टिकट का रोल। रोल इटरेबल है; मौजूदा स्थिति इटरेटर। हर बार फाड़ने पर "
        "एक टिकट मिलता है, और रोल खत्म होने पर देने को कुछ नहीं बचता।",
        "Counter par ticket ka roll. Roll iterable hai; maujooda position iterator. "
        "Har baar phaadne par ek ticket milta hai, aur roll khatam hone par dene ko "
        "kuch nahi bachta.",
    ),
    "https://docs.python.org/3/tutorial/classes.html#iterators",
    examples=[
        ex(
            "numbers = [10, 20, 30]\nit = iter(numbers)\nprint(next(it))\nprint(next(it))\nprint(next(it))",
            "10\n20\n30",
            L("three items, three calls", "तीन आइटम, तीन कॉल", "teen item, teen call"),
            note=L(
                "`iter()` returns an iterator; `next()` advances it. The list itself is "
                "unchanged - the iterator holds the position.",
                "`iter()` इटरेटर लौटाता है; `next()` उसे आगे बढ़ाता है। सूची वैसी ही "
                "रहती है - स्थिति इटरेटर में होती है।",
                "`iter()` iterator return karta hai; `next()` use aage badhata hai. List "
                "waisi hi rehti hai - position iterator me hoti hai.",
            ),
        ),
        ex(
            'text = "abc"\nit = iter(text)\nwhile True:\n    try:\n        print(next(it))\n    except StopIteration:\n        print("done")\n        break',
            "a\nb\nc\ndone",
            L("what a for loop hides", "for लूप क्या छिपाता है", "for loop kya chhipata hai"),
            note=L(
                "A `for` loop calls iter(), then next() until StopIteration, then stops "
                "quietly. This while loop shows that machinery by hand.",
                "`for` लूप iter() बुलाता है, फिर StopIteration तक next(), फिर चुपचाप "
                "रुक जाता है। यह while लूप वही मशीनरी हाथ से दिखाता है।",
                "`for` loop iter() bulata hai, phir StopIteration tak next(), phir "
                "chupchap ruk jata hai. Ye while loop wahi machinery haath se dikhata hai.",
            ),
        ),
        ex(
            "numbers = [1, 2, 3]\nit = iter(numbers)\nprint(list(it))\nprint(list(it))\nprint(sum(numbers))",
            "[1, 2, 3]\n[]\n6",
            L("an iterator is used up", "इटरेटर एक बार खर्च होता है", "iterator ek baar kharch hota hai"),
            note=L(
                "After the first list(it), the iterator is exhausted, so the second call "
                "gives an empty list. The original list is still reusable.",
                "पहले list(it) के बाद इटरेटर खत्म, इसलिए दूसरी कॉल खाली सूची देती है। मूल "
                "सूची फिर भी दोबारा चलती है।",
                "Pehle list(it) ke baad iterator khatam, isliye doosri call khaali list "
                "deti hai. Original list phir bhi dobara chalti hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Use `iter` and `next` (not a for loop) to put the first two items of "
                "`[5, 6, 7]` into `first` and `second`, then print them.",
                "`iter` और `next` से (for लूप के बिना) `[5, 6, 7]` के पहले दो आइटम "
                "`first` और `second` में रखें, फिर प्रिंट करें।",
                "`iter` aur `next` se (for loop ke bina) `[5, 6, 7]` ke pehle do item "
                "`first` aur `second` me rakho, phir print karo.",
            ),
            "values = [5, 6, 7]\n# it = ...\n# first = ...\n",
            "values = [5, 6, 7]\nit = iter(values)\nfirst = next(it)\nsecond = next(it)\n\nprint(first, second)",
            [
                "first == 5",
                "second == 6",
                "printed.strip() == '5 6'",
            ],
            L(
                "Create the iterator once, then call next twice on the same object.",
                "इटरेटर एक बार बनाएँ, फिर उसी ऑब्जेक्ट पर दो बार next बुलाएँ।",
                "Iterator ek baar banao, phir usi object par do baar next bulao.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does an exhausted iterator raise on next()?",
                "खत्म हुआ इटरेटर next() पर क्या उठाता है?",
                "Khatam hua iterator next() par kya uthata hai?",
            ),
            ["IndexError", "StopIteration", "ValueError", "nothing"],
            "b",
            L(
                "StopIteration is the signal a for loop catches to end quietly.",
                "StopIteration वह संकेत है जिसे for लूप पकड़कर चुपचाप रुकता है।",
                "StopIteration woh signal hai jise for loop pakadkar chupchap rukta hai.",
            ),
        ),
        quiz(
            L(
                "Why does `list(it)` return [] the second time?",
                "दूसरी बार `list(it)` [] क्यों लौटाता है?",
                "Doosri baar `list(it)` [] kyun return karta hai?",
            ),
            [
                "list() clears the iterator",
                "the iterator was already exhausted by the first call",
                "the original list was deleted",
                "list() only works once per program",
            ],
            "b",
            L(
                "Iterators are single-use. Call iter() again on the original iterable "
                "for a fresh pass.",
                "इटरेटर एक बार चलते हैं। नई बारी के लिए मूल इटरेबल पर फिर iter() बुलाएँ।",
                "Iterators ek baar chalte hain. Nayi baari ke liye original iterable par "
                "phir iter() bulao.",
            ),
        ),
        quiz(
            L(
                "What does a `for` loop do internally?",
                "`for` लूप अंदर से क्या करता है?",
                "`for` loop andar se kya karta hai?",
            ),
            [
                "calls len() and indexes each item",
                "calls iter() then next() until StopIteration",
                "copies the whole sequence first",
                "calls next() only",
            ],
            "b",
            L(
                "That is why any iterable works in a for loop, including files and "
                "generators.",
                "इसीलिए for लूप में हर इटरेबल चलता है, फ़ाइलें और जनरेटर भी।",
                "Isliye for loop me har iterable chalta hai, files aur generators bhi.",
            ),
        ),
    ],
    takeaway=L(
        "iter() creates a position, next() moves it, StopIteration ends it - for is the friendly wrapper.",
        "iter() स्थिति बनाता है, next() उसे बढ़ाता है, StopIteration खत्म करता है - for उसका आसान आवरण है।",
        "iter() position banata hai, next() use badhata hai, StopIteration khatam karta hai - for uska aasan aavaran hai.",
    ),
)

l03 = lesson(
    "m09c02l03",
    L("yield and generators", "yield और जनरेटर", "yield aur generators"),
    ["yield"],
    L(
        "A function with `yield` returns a generator: calling it runs no code until "
        "you ask for the first item, then it pauses at each yield and resumes where "
        "it stopped. That makes huge or endless sequences cheap.",
        "`yield` वाला फ़ंक्शन जनरेटर लौटाता है: बुलाने पर कोई कोड नहीं चलता जब तक पहला "
        "आइटम न माँगें, फिर हर yield पर रुकता है और जहाँ रुका था वहीं से आगे बढ़ता है। "
        "इससे बड़ी या अनंत श्रृंखलाएँ सस्ती हो जाती हैं।",
        "`yield` wala function generator return karta hai: bulane par koi code nahi "
        "chalta jab tak pehla item na maangein, phir har yield par rukta hai aur "
        "jahan ruka tha wahin se aage badhta hai. Isse badi ya anant sequences sasti "
        "ho jati hain.",
    ),
    L(
        "A water tap, not a bucket. A list is a bucket: fill it all at once. A "
        "generator is a tap: water comes when you open it, and you never store the "
        "whole tank.",
        "पानी का नल, बाल्टी नहीं। सूची बाल्टी है: पूरी एक बार भरो। जनरेटर नल है: खोलने पर "
        "पानी आता है, और पूरी टंकी कभी जमा नहीं करनी पड़ती।",
        "Paani ka nal, baalti nahi. List baalti hai: poori ek baar bharo. Generator "
        "nal hai: kholne par paani aata hai, aur poori tanki kabhi jama nahi karni "
        "padti.",
    ),
    "https://docs.python.org/3/tutorial/classes.html#generators",
    visual="generator_lazy",
    examples=[
        ex(
            "def countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\nprint(list(countdown(4)))\nfor number in countdown(3):\n    print(number)",
            "[4, 3, 2, 1]\n3\n2\n1",
            L("a generator can be looped", "जनरेटर पर लूप चल सकता है", "generator par loop chal sakta hai"),
            note=L(
                "The function body runs only while the loop asks for values. Each "
                "`yield` hands one value back and freezes the local variables.",
                "फ़ंक्शन का शरीर तभी चलता है जब लूप मान माँगता है। हर `yield` एक मान "
                "लौटाकर लोकल वेरिएबल जमा देता है।",
                "Function ka body tabhi chalta hai jab loop value maangta hai. Har "
                "`yield` ek value laut kar local variables jama deta hai.",
            ),
        ),
        ex(
            "def naturals():\n    n = 1\n    while True:\n        yield n\n        n += 1\n\ngen = naturals()\nprint([next(gen) for _ in range(5)])\nprint(next(gen))",
            "[1, 2, 3, 4, 5]\n6",
            L("an endless generator is safe", "अनंत जनरेटर सुरक्षित है", "anant generator safe hai"),
            note=L(
                "This generator never finishes, yet the program is fine because it only "
                "computes the six values asked for. A list of naturals would run out "
                "of memory.",
                "यह जनरेटर कभी खत्म नहीं होता, फिर भी प्रोग्राम ठीक है क्योंकि सिर्फ़ "
                "माँगे गए छह मान बनते हैं। सभी प्राकृत संख्याओं की सूची मेमोरी खत्म कर "
                "देती।",
                "Ye generator kabhi khatam nahi hota, phir bhi program theek hai kyunki "
                "sirf maange gaye chhah value bante hain. Sab natural numbers ki list "
                "memory khatam kar deti.",
            ),
        ),
        ex(
            "def read_lines(text):\n    for line in text.splitlines():\n        if line.strip():\n            yield line.strip()\n\nfor line in read_lines('tea\\n\\ncoffee\\n'):\n    print(line)",
            "tea\ncoffee",
            L("a pipeline that skips blanks", "खाली पंक्तियाँ छोड़ने वाली पाइपलाइन", "khaali lines chhodne wali pipeline"),
            note=L(
                "Generators compose: this one can feed another generator, and each "
                "stage handles one item at a time.",
                "जनरेटर जुड़ते हैं: यह दूसरे जनरेटर को खिला सकता है, और हर चरण एक बार "
                "में एक आइटम संभालता है।",
                "Generators judte hain: ye doosre generator ko khila sakta hai, aur har "
                "stage ek baar me ek item sambhalta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write a generator `evens(limit)` that yields 0, 2, 4 ... while the value "
                "is below `limit`. Print `list(evens(7))`.",
                "जनरेटर `evens(limit)` लिखें जो 0, 2, 4 ... yield करे जब तक मान `limit` "
                "से कम हो। `list(evens(7))` प्रिंट करें।",
                "Generator `evens(limit)` likho jo 0, 2, 4 ... yield kare jab tak value "
                "`limit` se kam ho. `list(evens(7))` print karo.",
            ),
            "def evens(limit):\n    # ...\n\n# print(list(evens(7)))\n",
            "def evens(limit):\n    n = 0\n    while n < limit:\n        yield n\n        n += 2\n\nprint(list(evens(7)))",
            [
                "list(evens(7)) == [0, 2, 4, 6]",
                "list(evens(1)) == [0]",
                "list(evens(0)) == []",
                "printed.strip() == '[0, 2, 4, 6]'",
            ],
            L(
                "Start at 0, yield, add 2, repeat while n < limit.",
                "0 से शुरू करें, yield करें, 2 जोड़ें, n < limit तक दोहराएँ।",
                "0 se shuru karo, yield karo, 2 jodo, n < limit tak dohrao.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does calling a generator function return?",
                "जनरेटर फ़ंक्शन बुलाने पर क्या लौटता है?",
                "Generator function bulane par kya return hota hai?",
            ),
            ["the first yielded value", "a generator object", "a list", "None"],
            "b",
            L(
                "No body code runs yet. You get an object you can iterate or pass to "
                "next().",
                "अभी शरीर का कोड नहीं चलता। आपको ऑब्जेक्ट मिलता है जिस पर लूप चला सकते "
                "हैं या next() दे सकते हैं।",
                "Abhi body ka code nahi chalta. Aapko object milta hai jis par loop "
                "chala sakte ho ya next() de sakte ho.",
            ),
        ),
        quiz(
            L(
                "What is the main advantage of a generator over a list?",
                "सूची की तुलना में जनरेटर का मुख्य लाभ?",
                "List ki tulna me generator ka mukhya labh?",
            ),
            [
                "it is always faster to index",
                "it produces items on demand instead of storing them all",
                "it can be modified in place",
                "it sorts automatically",
            ],
            "b",
            L(
                "Memory stays flat: one item at a time, however long the sequence is.",
                "मेमोरी स्थिर रहती है: एक बार में एक आइटम, श्रृंखला कितनी भी लंबी हो।",
                "Memory sthir rehti hai: ek baar me ek item, sequence kitni bhi lambi ho.",
            ),
        ),
        quiz(
            L(
                "After a generator yields once, where does it resume?",
                "जनरेटर एक बार yield करने के बाद कहाँ से आगे बढ़ता है?",
                "Generator ek baar yield karne ke baad kahan se aage badhta hai?",
            ),
            [
                "from the first line again",
                "from the statement after the yield",
                "from the last return",
                "it cannot resume",
            ],
            "b",
            L(
                "The frame is kept, so local variables survive between yields.",
                "फ़्रेम रखा जाता है, इसलिए लोकल वेरिएबल yield के बीच बचे रहते हैं।",
                "Frame rakha jata hai, isliye local variables yield ke beech bache rehte "
                "hain.",
            ),
        ),
    ],
    takeaway=L(
        "yield turns a function into a lazy producer; use it for big files, streams and endless sequences.",
        "yield फ़ंक्शन को आलसी उत्पादक बनाता है; बड़ी फ़ाइलों, स्ट्रीम और अनंत श्रृंखलाओं के लिए इस्तेमाल करें।",
        "yield function ko lazy producer banata hai; badi files, streams aur anant sequences ke liye use karo.",
    ),
)

MODULE = module(
    M,
    L("Comprehensions and Generators", "कॉम्प्रिहेंशन और जनरेटर", "Comprehensions aur Generators"),
    L(
        "Build sequences in one line, understand the iterator protocol under every "
        "for loop, and produce values lazily with yield.",
        "एक पंक्ति में श्रृंखलाएँ बनाएँ, हर for लूप के नीचे इटरेटर प्रोटोकॉल समझें, और "
        "yield से मान आलसी रूप में बनाएँ।",
        "Ek line me sequences banao, har for loop ke neeche iterator protocol samjho, "
        "aur yield se values lazy roop me banao.",
    ),
    [
        chapter("m09c01", L("One-line sequences", "एक-पंक्ति श्रृंखलाएँ", "Ek-line sequences"), [l01, l02]),
        chapter("m09c02", L("Lazy values", "आलसी मान", "Lazy values"), [l03]),
    ],
    exam=[
        quiz(
            L("`[x for x in range(3)]` gives:", "`[x for x in range(3)]` देता है:", "`[x for x in range(3)]` deta hai:"),
            ["[1, 2, 3]", "[0, 1, 2]", "0 1 2", "(0, 1, 2)"],
            "b",
            L("range(3) is 0, 1, 2 and the brackets make a list.", "range(3) यानी 0, 1, 2 और ब्रेसिज़ सूची बनाते हैं।", "range(3) yani 0, 1, 2 aur brackets list banate hain."),
        ),
        quiz(
            L("Which built-in advances an iterator?", "इटरेटर को आगे कौन बढ़ाता है?", "Iterator ko aage kaun badhata hai?"),
            ["iter()", "next()", "advance()", "yield()"],
            "b",
            L("iter() creates, next() advances.", "iter() बनाता है, next() आगे बढ़ाता है।", "iter() banata hai, next() aage badhata hai."),
        ),
        quiz(
            L("A generator function is recognised by:", "जनरेटर फ़ंक्शन किससे पहचाना जाता है?", "Generator function kis se pehchana jata hai?"),
            ["the word generator", "a yield inside it", "a return inside it", "the @gen decorator"],
            "b",
            L("Any function containing yield returns a generator when called.", "yield वाला कोई भी फ़ंक्शन बुलाने पर जनरेटर लौटाता है।", "yield wala koi bhi function bulane par generator return karta hai."),
        ),
        quiz(
            L("What ends a for loop over an iterator?", "इटरेटर पर for लूप कैसे खत्म होता है?", "Iterator par for loop kaise khatam hota hai?"),
            ["return", "StopIteration", "break only", "a None value"],
            "b",
            L("StopIteration is caught internally; break is your own early exit.", "StopIteration अंदर पकड़ा जाता है; break आपका अपना जल्दी निकलना है।", "StopIteration andar pakda jata hai; break aapka apna jaldi nikalna hai."),
        ),
        quiz(
            L("Which is a dict comprehension?", "कौन dict कॉम्प्रिहेंशन है?", "Kaun dict comprehension hai?"),
            ["{k: v for k, v in pairs}", "{k for k, v in pairs}", "[k for k, v in pairs]", "(k for k, v in pairs)"],
            "a",
            L("key: value before for, inside braces.", "for से पहले key: value, ब्रेसिज़ के अंदर।", "for se pehle key: value, braces ke andar."),
        ),
        quiz(
            L("Why can a generator handle a 10 GB log file?", "जनरेटर 10 GB लॉग फ़ाइल क्यों संभाल सकता है?", "Generator 10 GB log file kyun sambhal sakta hai?"),
            ["it compresses the file", "it reads one line at a time instead of loading everything", "it uses the GPU", "it skips errors"],
            "b",
            L("Only the current line is in memory, so size stops mattering.", "सिर्फ़ मौजूदा पंक्ति मेमोरी में होती है, इसलिए आकार मायने नहीं रखता।", "Sirf maujooda line memory me hoti hai, isliye size maayne nahi rakhta."),
        ),
    ],
    icon="🔁",
)
