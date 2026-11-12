"""Module 10 - Modern Python: type hints, closures, decorators, structural matching."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m10"

l01 = lesson(
    "m10c01l01",
    L("Type hints and type aliases", "टाइप हिंट और टाइप उपनाम", "Type hints aur type aliases"),
    ["type"],
    L(
        "A type hint says what a function expects and returns, for readers, editors "
        "and checkers. Python still does not enforce it at runtime. The `type` "
        "statement (3.12+) gives a reusable name to a type.",
        "टाइप हिंट बताता है कि फ़ंक्शन क्या लेता और लौटाता है - पढ़ने वालों, एडिटर और "
        "चेकर के लिए। पायथन रनटाइम पर इसे लागू नहीं करता। `type` स्टेटमेंट (3.12+) "
        "किसी टाइप को दोबारा इस्तेमाल लायक नाम देता है।",
        "Type hint batata hai ki function kya leta aur return karta hai - padhne "
        "walon, editor aur checker ke liye. Python runtime par ise enforce nahi karta. "
        "`type` statement (3.12+) kisi type ko dobara use layak naam deta hai.",
    ),
    L(
        "A label on a jar. \"Sugar\" on the jar does not make it sugar, but everyone "
        "in the kitchen stops guessing.",
        "जार पर लेबल। जार पर \"चीनी\" लिखा होने से अंदर चीनी नहीं बन जाती, पर रसोई में "
        "सबका अंदाज़ा खत्म हो जाता है।",
        "Jar par label. Jar par \"cheeni\" likha hone se andar cheeni nahi ban jati, par "
        "rasoi me sabka andaza khatam ho jata hai.",
    ),
    "https://docs.python.org/3/library/typing.html",
    examples=[
        ex(
            'def greet(name: str, times: int = 1) -> str:\n    return " ".join([f"Hi {name}!"] * times)\n\nprint(greet("Asha"))\nprint(greet("Ravi", 2))',
            "Hi Asha!\nHi Ravi! Hi Ravi!",
            L("annotations on parameters and return", "पैरामीटर और रिटर्न पर एनोटेशन", "parameter aur return par annotations"),
            note=L(
                "`name: str` and `-> str` are read by tools. Nothing stops you from "
                "passing an int, but an editor will warn you first.",
                "`name: str` और `-> str` टूल पढ़ते हैं। int भेजने से कोई रोकता नहीं, पर "
                "एडिटर पहले चेतावनी देगा।",
                "`name: str` aur `-> str` tools padhte hain. int bhejne se koi rokta "
                "nahi, par editor pehle chetavni dega.",
            ),
        ),
        ex(
            'type Vector = list[float]\n\ndef total(values: Vector) -> float:\n    return sum(values)\n\nprint(total([1.5, 2.5]))\nprint(total([]))',
            "4.0\n0",
            L("the type statement (Python 3.12+)", "type स्टेटमेंट (पायथन 3.12+)", "type statement (Python 3.12+)"),
            note=L(
                "`type Vector = list[float]` is a real type alias, not a variable. On "
                "Python 3.11 or older write `Vector = list[float]` instead - it works "
                "the same for hints.",
                "`type Vector = list[float]` असली टाइप उपनाम है, वेरिएबल नहीं। पायथन "
                "3.11 या पुराने में `Vector = list[float]` लिखें - हिंट के लिए वही काम "
                "करता है।",
                "`type Vector = list[float]` asli type alias hai, variable nahi. Python "
                "3.11 ya purane me `Vector = list[float]` likho - hint ke liye wahi kaam "
                "karta hai.",
            ),
        ),
        ex(
            "def find(users: list[dict], name: str) -> dict | None:\n    for user in users:\n        if user['name'] == name:\n            return user\n    return None\n\nusers = [{'name': 'Asha'}, {'name': 'Ravi'}]\nprint(find(users, 'Ravi'))\nprint(find(users, 'Mili'))",
            "{'name': 'Ravi'}\nNone",
            L("X | None means \"or nothing\"", "X | None का मतलब \"या कुछ नहीं\"", "X | None ka matlab \"ya kuch nahi\""),
            note=L(
                "The hint says the caller must handle None. That is more useful than a "
                "docstring sentence nobody reads.",
                "हिंट कहता है कि बुलाने वाले को None संभालना है। यह उस डॉकस्ट्रिंग से "
                "ज़्यादा काम का है जिसे कोई नहीं पढ़ता।",
                "Hint kehta hai ki caller ko None sambhalna hai. Ye us docstring se "
                "zyada kaam ka hai jise koi nahi padhta.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Annotate `add(a, b)` so it takes two ints and returns an int, then "
                "print `add(2, 3)`.",
                "`add(a, b)` पर एनोटेशन लगाएँ: दो int ले और int लौटाए, फिर "
                "`add(2, 3)` प्रिंट करें।",
                "`add(a, b)` par annotation lagao: do int le aur int return kare, phir "
                "`add(2, 3)` print karo.",
            ),
            "def add(a, b):\n    return a + b\n\n# print(add(2, 3))\n",
            "def add(a: int, b: int) -> int:\n    return a + b\n\nprint(add(2, 3))",
            [
                "add(2, 3) == 5",
                "add.__annotations__['a'] is int",
                "add.__annotations__['return'] is int",
                "printed.strip() == '5'",
            ],
            L(
                "Put `: int` after each parameter and `-> int` before the colon.",
                "हर पैरामीटर के बाद `: int` और कोलन से पहले `-> int` लगाएँ।",
                "Har parameter ke baad `: int` aur colon se pehle `-> int` lagao.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Does a type hint stop a wrong argument at runtime?",
                "टाइप हिंट रनटाइम पर गलत आर्ग्युमेंट रोकता है?",
                "Type hint runtime par galat argument rokta hai?",
            ),
            [
                "yes, it raises TypeError",
                "no, it is documentation for tools and readers",
                "only for int and str",
                "only inside classes",
            ],
            "b",
            L(
                "Hints are not enforced. Use a checker such as mypy or pyright for "
                "that.",
                "हिंट लागू नहीं होते। उसके लिए mypy या pyright जैसा चेकर इस्तेमाल करें।",
                "Hints laagu nahi hote. Uske liye mypy ya pyright jaisa checker use karo.",
            ),
        ),
        quiz(
            L(
                "What does `-> None` mean on a function?",
                "फ़ंक्शन पर `-> None` का क्या मतलब है?",
                "Function par `-> None` ka kya matlab hai?",
            ),
            [
                "it returns nothing useful",
                "it returns the string 'None'",
                "it cannot be called",
                "it returns False",
            ],
            "a",
            L(
                "It performs an action (print, save) and returns no value.",
                "यह कोई काम करता है (प्रिंट, सेव) और कोई मान नहीं लौटाता।",
                "Ye koi kaam karta hai (print, save) aur koi value nahi return karta.",
            ),
        ),
        quiz(
            L(
                "Which spelling is the modern union hint?",
                "आधुनिक यूनियन हिंट कौन सी है?",
                "Aadhunik union hint kaun si hai?",
            ),
            ["Union[int, None]", "Optional[int] only", "int | None", "int or None"],
            "c",
            L(
                "`int | None` works from 3.10. Union and Optional still work and are "
                "common in older code.",
                "`int | None` 3.10 से चलता है। Union और Optional भी चलते हैं और पुराने "
                "कोड में आम हैं।",
                "`int | None` 3.10 se chalta hai. Union aur Optional bhi chalte hain aur "
                "purane code me aam hain.",
            ),
        ),
    ],
    takeaway=L(
        "Annotate public functions, use `X | None` for may-be-missing values, and remember hints are not runtime checks.",
        "सार्वजनिक फ़ंक्शन पर एनोटेशन लगाएँ, अनुपस्थित हो सकने वाले मान के लिए `X | None`, और याद रखें हिंट रनटाइम जाँच नहीं हैं।",
        "Public functions par annotation lagao, missing ho sakne wale value ke liye `X | None`, aur yaad rakho hints runtime checks nahi hain.",
    ),
)

l02 = lesson(
    "m10c01l02",
    L("Functions as objects and closures", "फ़ंक्शन ऑब्जेक्ट की तरह और क्लोज़र", "Functions objects ki tarah aur closures"),
    [],
    L(
        "In Python a function is a value: you can store it in a list, pass it to "
        "another function, and return it. A closure is an inner function that "
        "remembers variables from the function that created it.",
        "पायथन में फ़ंक्शन एक मान है: उसे सूची में रख सकते हैं, दूसरे फ़ंक्शन को दे सकते "
        "हैं, और लौटा सकते हैं। क्लोज़र अंदरूनी फ़ंक्शन है जो अपने बनाने वाले फ़ंक्शन "
        "के वेरिएबल याद रखता है।",
        "Python me function ek value hai: use list me rakh sakte ho, doosre function "
        "ko de sakte ho, aur return kar sakte ho. Closure andaruni function hai jo "
        "apne banane wale function ke variables yaad rakhta hai.",
    ),
    L(
        "A key with a tag. The key shape is the function; the tag it carries is the "
        "remembered variable. Hand the key to anyone and it still opens that one lock.",
        "टैग लगी चाबी। चाबी का आकार फ़ंक्शन है; उस पर लगा टैग याद रखा वेरिएबल। चाबी किसी "
        "को भी दें, वह उसी ताले को खोलती है।",
        "Tag lagi chaabi. Chaabi ka aakaar function hai; us par laga tag yaad rakha "
        "variable. Chaabi kisi ko bhi do, woh usi taale ko kholti hai.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
    examples=[
        ex(
            'def shout(text):\n    return text.upper() + "!"\n\ndef whisper(text):\n    return text.lower() + "..."\n\ndef announce(style, text):\n    print(style(text))\n\nannounce(shout, "hello")\nannounce(whisper, "HELLO")',
            "HELLO!\nhello...",
            L("passing a function as an argument", "फ़ंक्शन को आर्ग्युमेंट की तरह भेजना", "function ko argument ki tarah bhejna"),
            note=L(
                "`style` is just a name bound to a function. The same announce() works "
                "with any function that takes one string.",
                "`style` बस एक नाम है जो फ़ंक्शन से जुड़ा है। वही announce() किसी भी ऐसे "
                "फ़ंक्शन से चलता है जो एक स्ट्रिंग ले।",
                "`style` bas ek naam hai jo function se juda hai. Wahi announce() kisi "
                "bhi aise function se chalta hai jo ek string le.",
            ),
        ),
        ex(
            "def multiplier(factor):\n    def times(number):\n        return number * factor\n    return times\n\ndouble = multiplier(2)\ntriple = multiplier(3)\nprint(double(10), triple(10))\nprint(double.__closure__[0].cell_contents)",
            "20 30\n2",
            L("a closure remembers factor", "क्लोज़र factor याद रखता है", "closure factor yaad rakhta hai"),
            note=L(
                "Each call to multiplier creates a new closure with its own `factor`. "
                "That is why double and triple do not interfere.",
                "multiplier की हर कॉल अपने `factor` वाला नया क्लोज़र बनाती है। इसलिए "
                "double और triple एक-दूसरे में नहीं पड़ते।",
                "multiplier ki har call apne `factor` wala naya closure banati hai. "
                "Isliye double aur triple ek-doosre me nahi padte.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `make_counter()` that returns a function; each call to that "
                "function returns 1, 2, 3 ... Print three calls.",
                "`make_counter()` लिखें जो फ़ंक्शन लौटाए; उस फ़ंक्शन की हर कॉल 1, 2, 3 ... "
                "लौटाए। तीन कॉल प्रिंट करें।",
                "`make_counter()` likho jo function return kare; us function ki har call "
                "1, 2, 3 ... return kare. Teen call print karo.",
            ),
            "def make_counter():\n    # count = ...\n    # def step(): ...\n    pass\n\n# counter = make_counter()\n",
            "def make_counter():\n    count = 0\n\n    def step():\n        nonlocal count\n        count += 1\n        return count\n\n    return step\n\ncounter = make_counter()\nprint(counter())\nprint(counter())\nprint(counter())",
            [
                "callable(make_counter())",
                "make_counter()() == 1",
                "printed.split() == ['1', '2', '3']",
            ],
            L(
                "The inner function needs `nonlocal count` to change the outer variable.",
                "अंदरूनी फ़ंक्शन को बाहरी वेरिएबल बदलने के लिए `nonlocal count` चाहिए।",
                "Andaruni function ko bahari variable badalne ke liye `nonlocal count` "
                "chahiye.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What is a closure?",
                "क्लोज़र क्या है?",
                "Closure kya hai?",
            ),
            [
                "a function with no arguments",
                "an inner function that keeps variables from its enclosing scope",
                "a class with one method",
                "a loop that never ends",
            ],
            "b",
            L(
                "The saved variables live in the function's __closure__ cells.",
                "याद रखे वेरिएबल फ़ंक्शन की __closure__ कोशिकाओं में रहते हैं।",
                "Yaad rakhe variables function ki __closure__ cells me rehte hain.",
            ),
        ),
        quiz(
            L(
                "Why do you need `nonlocal count` inside the inner function?",
                "अंदरूनी फ़ंक्शन में `nonlocal count` क्यों चाहिए?",
                "Andaruni function me `nonlocal count` kyun chahiye?",
            ),
            [
                "to read count",
                "to assign to the outer function's variable instead of making a local one",
                "to make count global",
                "to copy count",
            ],
            "b",
            L(
                "Assignment creates a local name unless you declare where it lives.",
                "असाइनमेंट लोकल नाम बना देता है जब तक आप न बताएँ कि वह कहाँ रहता है।",
                "Assignment local naam bana deta hai jab tak aap na batayein ki woh "
                "kahan rehta hai.",
            ),
        ),
        quiz(
            L(
                "Which value can be stored in a list?",
                "सूची में कौन सा मान रखा जा सकता है?",
                "List me kaun sa value rakha ja sakta hai?",
            ),
            [
                "only numbers",
                "only strings",
                "any object, including functions",
                "only objects with a name",
            ],
            "c",
            L(
                "Functions are objects: lists of callbacks are a normal Python pattern.",
                "फ़ंक्शन ऑब्जेक्ट हैं: कॉलबैक की सूची सामान्य पायथन पैटर्न है।",
                "Functions objects hain: callbacks ki list normal Python pattern hai.",
            ),
        ),
    ],
    takeaway=L(
        "Functions are values; a closure is a function plus the variables it remembers.",
        "फ़ंक्शन मान हैं; क्लोज़र फ़ंक्शन प्लस याद रखे वेरिएबल है।",
        "Functions values hain; closure function plus yaad rakhe variables hai.",
    ),
)

l03 = lesson(
    "m10c02l03",
    L("Decorators", "डेकोरेटर", "Decorators"),
    [],
    L(
        "A decorator is a function that takes a function and returns a replacement. "
        "`@name` above a def is short for `func = name(func)`. It is how logging, "
        "timing and caching get added without touching the original body.",
        "डेकोरेटर वह फ़ंक्शन है जो फ़ंक्शन लेकर उसका विकल्प लौटाता है। def के ऊपर `@name` "
        "का मतलब है `func = name(func)`। इसी तरह लॉगिंग, समय मापना और कैशिंग मूल शरीर "
        "को छुए बिना जुड़ते हैं।",
        "Decorator woh function hai jo function lekar uska replacement return karta "
        "hai. def ke upar `@name` ka matlab hai `func = name(func)`. Isi tarah "
        "logging, timing aur caching mool body ko chhue bina judte hain.",
    ),
    L(
        "A phone cover. The phone is unchanged, but every photo you take now has a "
        "case around it - and you can put on two covers.",
        "फ़ोन का कवर। फ़ोन वैसा ही है, पर अब हर फ़ोटो के साथ कवर भी है - और दो कवर भी "
        "लगा सकते हैं।",
        "Phone ka cover. Phone waisa hi hai, par ab har photo ke saath cover bhi hai - "
        "aur do cover bhi laga sakte ho.",
    ),
    "https://docs.python.org/3/glossary.html#term-decorator",
    examples=[
        ex(
            'def logged(func):\n    def wrapper(*args, **kwargs):\n        print("calling", func.__name__)\n        return func(*args, **kwargs)\n    return wrapper\n\n@logged\ndef add(a, b):\n    return a + b\n\nprint(add(2, 3))',
            "calling add\n5",
            L("a minimal decorator", "सबसे छोटा डेकोरेटर", "sabse chhota decorator"),
            note=L(
                "`@logged` replaced `add` with `wrapper`. The original add still exists "
                "inside the closure, so the result is unchanged.",
                "`@logged` ने `add` की जगह `wrapper` रख दिया। मूल add क्लोज़र के अंदर "
                "मौजूद है, इसलिए परिणाम वही है।",
                "`@logged` ne `add` ki jagah `wrapper` rakh diya. Mool add closure ke "
                "andar maujood hai, isliye result wahi hai.",
            ),
        ),
        ex(
            'from functools import wraps\n\ndef logged(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs)\n    return wrapper\n\n@logged\ndef area(width, height):\n    return width * height\n\nprint(area.__name__)\nprint(area(3, 4))',
            "area\n12",
            L("@wraps keeps the original name", "@wraps मूल नाम रखता है", "@wraps mool naam rakhta hai"),
            note=L(
                "Without @wraps, area.__name__ would be 'wrapper'. That breaks "
                "tracebacks, docs and test names.",
                "@wraps के बिना area.__name__ 'wrapper' होता। इससे ट्रेसबैक, डॉक्स और "
                "टेस्ट के नाम टूटते हैं।",
                "@wraps ke bina area.__name__ 'wrapper' hota. Isse traceback, docs aur "
                "test ke naam tootte hain.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write a decorator `doubled` that makes the function return twice its "
                "result. Apply it to `five()` returning 5 and print `five()`.",
                "डेकोरेटर `doubled` लिखें जो फ़ंक्शन का परिणाम दोगुना कर दे। इसे `five()` "
                "पर लगाएँ जो 5 लौटाता है और `five()` प्रिंट करें।",
                "Decorator `doubled` likho jo function ka result doguna kar de. Ise "
                "`five()` par lagao jo 5 return karta hai aur `five()` print karo.",
            ),
            "def doubled(func):\n    # def wrapper(): ...\n    pass\n\n# @doubled\n# def five(): ...\n",
            "def doubled(func):\n    def wrapper(*args, **kwargs):\n        return func(*args, **kwargs) * 2\n    return wrapper\n\n@doubled\ndef five():\n    return 5\n\nprint(five())",
            [
                "five() == 10",
                "callable(five)",
                "printed.strip() == '10'",
            ],
            L(
                "wrapper calls func() and multiplies what comes back.",
                "wrapper func() बुलाकर जो लौटे उसे गुणा करता है।",
                "wrapper func() bula kar jo laute use guna karta hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What is `@deco` above a def equivalent to?",
                "def के ऊपर `@deco` किसके बराबर है?",
                "def ke upar `@deco` kiske barabar hai?",
            ),
            ["deco()", "func = deco(func)", "deco(func) inside the body", "import deco"],
            "b",
            L(
                "The name is rebound to whatever the decorator returns.",
                "नाम उस चीज़ से जुड़ जाता है जो डेकोरेटर लौटाता है।",
                "Naam us cheez se jud jata hai jo decorator return karta hai.",
            ),
        ),
        quiz(
            L(
                "Why is `@wraps(func)` recommended?",
                "`@wraps(func)` क्यों सलाह दी जाती है?",
                "`@wraps(func)` kyun salah di jati hai?",
            ),
            [
                "it makes the wrapper faster",
                "it copies __name__ and __doc__ from the original function",
                "it catches exceptions",
                "it is required by Python",
            ],
            "b",
            L(
                "Without it every wrapped function is named 'wrapper', which hides the "
                "real function in logs and tests.",
                "इसके बिना हर लिपटा फ़ंक्शन 'wrapper' नाम का हो जाता है, जिससे लॉग और "
                "टेस्ट में असली फ़ंक्शन छिप जाता है।",
                "Iske bina har wrapped function 'wrapper' naam ka ho jata hai, jisse log "
                "aur test me asli function chhip jata hai.",
            ),
        ),
        quiz(
            L(
                "Why does a wrapper usually accept `*args, **kwargs`?",
                "wrapper आमतौर पर `*args, **kwargs` क्यों लेता है?",
                "wrapper aam taur par `*args, **kwargs` kyun leta hai?",
            ),
            [
                "to run faster",
                "so it can wrap any function without knowing its parameters",
                "because decorators forbid named parameters",
                "to avoid @wraps",
            ],
            "b",
            L(
                "A generic wrapper must forward whatever arguments the caller used.",
                "सामान्य wrapper को वही आर्ग्युमेंट आगे भेजने होते हैं जो बुलाने वाले ने दिए।",
                "Saamanya wrapper ko wahi arguments aage bhejne hote hain jo caller ne "
                "diye.",
            ),
        ),
    ],
    takeaway=L(
        "A decorator wraps a function; always forward *args/**kwargs and add @wraps.",
        "डेकोरेटर फ़ंक्शन को लपेटता है; हमेशा *args/**kwargs आगे भेजें और @wraps जोड़ें।",
        "Decorator function ko lapetta hai; hamesha *args/**kwargs aage bhejo aur @wraps jodo.",
    ),
)

l04 = lesson(
    "m10c02l04",
    L("match and case: structural patterns", "match और case: संरचनात्मक पैटर्न", "match aur case: structural patterns"),
    ["match", "case", "_"],
    L(
        "`match` compares a value against patterns, not just equality: shapes of "
        "sequences, mapping keys, class attributes and guards. `case _` is the "
        "default branch and matches anything.",
        "`match` मान की तुलना पैटर्न से करता है, सिर्फ़ बराबरी से नहीं: सीक्वेंस का आकार, "
        "mapping की कुंजियाँ, क्लास एट्रिब्यूट और guard। `case _` डिफ़ॉल्ट शाखा है जो "
        "कुछ भी मिल जाए।",
        "`match` value ki tulna patterns se karta hai, sirf barabari se nahi: sequence "
        "ka aakaar, mapping ki keys, class attributes aur guards. `case _` default "
        "branch hai jo kuch bhi match kare.",
    ),
    L(
        "A courier sorting table. Round parcels go left, flat envelopes go right, and "
        "anything unrecognised goes to the manual desk - that is `case _`.",
        "कूरियर की छँटाई मेज़। गोल पार्सल बाएँ, चपटे लिफ़ाफ़े दाएँ, और जो पहचाना न जाए वह "
        "मैनुअल डेस्क पर - यही `case _` है।",
        "Courier ki chhantai mez. Gol parcel baayein, chapte envelope daayein, aur jo "
        "pehchana na jaye woh manual desk par - yahi `case _` hai.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#match-statements",
    examples=[
        ex(
            'def describe(point):\n    match point:\n        case (0, 0):\n            return "origin"\n        case (x, 0):\n            return f"on x axis at {x}"\n        case (0, y):\n            return f"on y axis at {y}"\n        case (x, y):\n            return f"at {x},{y}"\n\nprint(describe((0, 0)))\nprint(describe((5, 0)))\nprint(describe((2, 3)))',
            "origin\non x axis at 5\nat 2,3",
            L("sequence patterns with capture", "कैप्चर के साथ सीक्वेंस पैटर्न", "capture ke saath sequence patterns"),
            note=L(
                "`(x, 0)` matches any two-item sequence whose second item is 0, and "
                "binds the first to x. Order matters: the most specific case goes "
                "first.",
                "`(x, 0)` किसी भी दो-आइटम सीक्वेंस से मिलता है जिसका दूसरा आइटम 0 हो, और "
                "पहले को x में रखता है। क्रम मायने रखता है: सबसे ख़ास केस पहले।",
                "`(x, 0)` kisi bhi do-item sequence se milta hai jiska doosra item 0 ho, "
                "aur pehle ko x me rakhta hai. Kram maayne rakhta hai: sabse khaas case "
                "pehle.",
            ),
        ),
        ex(
            'class Order:\n    def __init__(self, item, qty):\n        self.item = item\n        self.qty = qty\n\ndef check(order):\n    match order:\n        case Order(item="tea", qty=q) if q > 3:\n            return f"big tea order: {q}"\n        case Order(item=name):\n            return f"order: {name}"\n        case _:\n            return "unknown"\n\nprint(check(Order("tea", 5)))\nprint(check(Order("coffee", 1)))\nprint(check("nope"))',
            "big tea order: 5\norder: coffee\nunknown",
            L("class patterns, guard and default", "क्लास पैटर्न, guard और डिफ़ॉल्ट", "class patterns, guard aur default"),
            note=L(
                "`if q > 3` is a guard: the pattern matches but the branch is skipped "
                "when the guard is false. `case _` catches everything else.",
                "`if q > 3` गार्ड है: पैटर्न मिलता है पर गार्ड झूठा हो तो शाखा छूट जाती "
                "है। `case _` बाकी सब पकड़ता है।",
                "`if q > 3` guard hai: pattern milta hai par guard jhoota ho to branch "
                "chhoot jati hai. `case _` baaki sab pakadta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `route(command)` using match: 'start' returns 'starting', 'stop' "
                "returns 'stopping', anything else returns 'unknown'. Print all three.",
                "match से `route(command)` लिखें: 'start' → 'starting', 'stop' → "
                "'stopping', बाकी कुछ भी → 'unknown'। तीनों प्रिंट करें।",
                "match se `route(command)` likho: 'start' → 'starting', 'stop' → "
                "'stopping', baaki kuch bhi → 'unknown'. Teeno print karo.",
            ),
            "def route(command):\n    # match command: ...\n    pass\n\n# print(route('start'))\n",
            "def route(command):\n    match command:\n        case \"start\":\n            return \"starting\"\n        case \"stop\":\n            return \"stopping\"\n        case _:\n            return \"unknown\"\n\nprint(route('start'))\nprint(route('stop'))\nprint(route('pause'))",
            [
                "route('start') == 'starting'",
                "route('stop') == 'stopping'",
                "route('pause') == 'unknown'",
                "printed.split() == ['starting', 'stopping', 'unknown']",
            ],
            L(
                "Literal strings are patterns too; `case _` must come last.",
                "सादे स्ट्रिंग भी पैटर्न हैं; `case _` अंत में आना चाहिए।",
                "Saade strings bhi patterns hain; `case _` end me aana chahiye.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does `case _` match?",
                "`case _` किससे मिलता है?",
                "`case _` kis se milta hai?",
            ),
            ["only None", "anything, it is the wildcard", "only numbers", "nothing"],
            "b",
            L(
                "It is the default branch, and it must be last to be useful.",
                "यह डिफ़ॉल्ट शाखा है, और काम का होने के लिए अंत में होनी चाहिए।",
                "Ye default branch hai, aur kaam ka hone ke liye end me honi chahiye.",
            ),
        ),
        quiz(
            L(
                "What is `case (x, 0)` doing?",
                "`case (x, 0)` क्या कर रहा है?",
                "`case (x, 0)` kya kar raha hai?",
            ),
            [
                "comparing with a tuple literal",
                "matching a 2-item sequence and binding the first item to x",
                "creating a tuple",
                "calling a function",
            ],
            "b",
            L(
                "A bare name in a pattern captures; a literal must match exactly.",
                "पैटर्न में सादा नाम कैप्चर करता है; शाब्दिक मान बिल्कुल मिलना चाहिए।",
                "Pattern me saada naam capture karta hai; literal value bilkul milna "
                "chahiye.",
            ),
        ),
        quiz(
            L(
                "What does a guard (`case X if cond`) do?",
                "गार्ड (`case X if cond`) क्या करता है?",
                "Guard (`case X if cond`) kya karta hai?",
            ),
            [
                "it changes the matched value",
                "it adds an extra condition before the branch runs",
                "it disables the case",
                "it raises an error",
            ],
            "b",
            L(
                "The pattern must match and the guard must be true; otherwise the next "
                "case is tried.",
                "पैटर्न मिलना चाहिए और गार्ड सच होना चाहिए; वरना अगला case देखा जाता है।",
                "Pattern milna chahiye aur guard sach hona chahiye; warna agla case "
                "dekha jata hai.",
            ),
        ),
    ],
    takeaway=L(
        "match is for shape: literals, sequences, mappings, class attributes and guards - with case _ as the safety net.",
        "match आकार के लिए है: शाब्दिक, सीक्वेंस, mapping, क्लास एट्रिब्यूट और गार्ड - और case _ सुरक्षा जाल।",
        "match aakaar ke liye hai: literal, sequence, mapping, class attributes aur guards - aur case _ safety net.",
    ),
)

MODULE = module(
    M,
    L("Modern Python", "आधुनिक पायथन", "Modern Python"),
    L(
        "Type hints and type aliases, functions as values, closures, decorators, and "
        "structural pattern matching.",
        "टाइप हिंट और टाइप उपनाम, फ़ंक्शन मान के रूप में, क्लोज़र, डेकोरेटर, और "
        "संरचनात्मक पैटर्न मिलान।",
        "Type hints aur type aliases, functions values ke roop me, closures, "
        "decorators, aur structural pattern matching.",
    ),
    [
        chapter("m10c01", L("Hints and higher-order functions", "हिंट और उच्च-क्रम फ़ंक्शन", "Hints aur higher-order functions"), [l01, l02]),
        chapter("m10c02", L("Wrapping and matching", "लपेटना और मिलान", "Lapetna aur matching"), [l03, l04]),
    ],
    exam=[
        quiz(
            L("Do type hints raise an error when violated?", "टाइप हिंट टूटने पर एरर देते हैं?", "Type hints tootne par error dete hain?"),
            ["yes, always", "no, they are not enforced at runtime", "only in classes", "only with -> None"],
            "b",
            L("They are checked by external tools, not by the interpreter.", "वे बाहरी टूल जाँचते हैं, इंटरप्रेटर नहीं।", "Wo baahari tools jaanchte hain, interpreter nahi."),
        ),
        quiz(
            L("What does a decorator return?", "डेकोरेटर क्या लौटाता है?", "Decorator kya return karta hai?"),
            ["nothing", "a replacement function (or object)", "always the same function", "a string"],
            "b",
            L("Usually a wrapper around the original.", "आमतौर पर मूल के चारों ओर wrapper।", "Aam taur par mool ke chaaron or wrapper."),
        ),
        quiz(
            L("Which statement creates a reusable type alias in 3.12?", "3.12 में दोबारा इस्तेमाल लायक टाइप उपनाम कौन बनाता है?", "3.12 me dobara use layak type alias kaun banata hai?"),
            ["alias Vector = list[float]", "type Vector = list[float]", "typedef Vector", "Vector := list[float]"],
            "b",
            L("The type statement, new in 3.12.", "type स्टेटमेंट, 3.12 में नया।", "type statement, 3.12 me naya."),
        ),
        quiz(
            L("What does a closure keep alive?", "क्लोज़र किसे जीवित रखता है?", "Closure kise jeevit rakhta hai?"),
            ["the whole module", "variables from the enclosing function", "only globals", "the caller's stack"],
            "b",
            L("Those variables live in __closure__ cells.", "वे वेरिएबल __closure__ कोशिकाओं में रहते हैं।", "Wo variables __closure__ cells me rehte hain."),
        ),
        quiz(
            L("In a match statement, which case should come last?", "match में कौन सा case अंत में आए?", "match me kaun sa case end me aaye?"),
            ["the first literal", "case _", "a class pattern", "a guard"],
            "b",
            L("The wildcard catches everything, so anything after it is unreachable.", "वाइल्डकार्ड सब पकड़ता है, इसलिए उसके बाद कुछ नहीं पहुँचता।", "Wildcard sab pakadta hai, isliye uske baad kuch nahi pahunchta."),
        ),
        quiz(
            L("Why add @wraps inside a decorator?", "@wraps डेकोरेटर में क्यों जोड़ें?", "Decorator me @wraps kyun jodein?"),
            ["for speed", "to preserve __name__ and __doc__", "to catch errors", "to allow async"],
            "b",
            L("It keeps the wrapped function recognisable in logs and tracebacks.", "यह लिपटे फ़ंक्शन को लॉग और ट्रेसबैक में पहचानने लायक रखता है।", "Ye wrapped function ko log aur traceback me pehchanne layak rakhta hai."),
        ),
    ],
    icon="✨",
)
