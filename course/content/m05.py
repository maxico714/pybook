"""Module 5 - Functions: naming a block of work so you can reuse it."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m05"

l01 = lesson(
    "m05c01l01",
    L("def and return", "def और return", "def aur return"),
    ["def", "return"],
    L(
        "A function is a named block of code that does one job. You define it once "
        "with def, then call it as many times as you like. return sends a value "
        "back to whoever called it.",
        "फ़ंक्शन एक नाम वाला कोड ब्लॉक है जो एक काम करता है। इसे def से एक बार "
        "परिभाषित करते हैं, फिर जितनी बार चाहें बुलाते हैं। return वैल्यू को वापस "
        "बुलाने वाले को भेजता है।",
        "Function ek naam wala code block hai jo ek kaam karta hai. Ise def se ek "
        "baar define karte hain, phir jitni baar chahein call karte hain. return "
        "value ko wapas caller ko bhejta hai.",
    ),
    L(
        "A mixer grinder: you put ingredients in, press the same button every time, "
        "and get a result out. You do not rebuild the machine for every chutney. A "
        "function is that button — same steps, new input, new output.",
        "मिक्सर ग्राइंडर: आप सामग्री डालते हैं, हर बार वही बटन दबाते हैं, और परिणाम "
        "मिलता है। हर चटनी के लिए मशीन दोबारा नहीं बनाते। फ़ंक्शन वही बटन है — "
        "वही स्टेप्स, नया इनपुट, नया आउटपुट।",
        "Mixer grinder: aap samagri daalte ho, har baar wahi button dabate ho, aur "
        "result milta hai. Har chutney ke liye machine dobara nahi banate. Function "
        "wahi button hai - wahi steps, naya input, naya output.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
    visual="function_call",
    examples=[
        ex(
            'def greet(name):\n    return f"Namaste, {name}!"\n\nprint(greet("Asha"))\nprint(greet("Ravi"))',
            "Namaste, Asha!\nNamaste, Ravi!",
            L("define once, call twice", "एक बार लिखो, दो बार बुलाओ", "ek baar likho, do baar bulao"),
            note=L(
                "The indented line is the function body. It runs only when you call "
                "greet(...).",
                "इंडेंटेड लाइन फ़ंक्शन की बॉडी है। वह तभी चलती है जब greet(...) बुलाएँ।",
                "Indented line function ki body hai. Woh tabhi chalti hai jab greet(...) bulao.",
            ),
        ),
        ex(
            'def add(a, b):\n    return a + b\n\nresult = add(3, 4)\nprint(result)\nprint(add("py", "thon"))',
            "7\npython",
            L("the same code, different types", "वही कोड, अलग टाइप", "wahi code, alag types"),
            note=L(
                "add does not care whether it gets numbers or text: + means whatever "
                "the values define. That flexibility is normal in Python.",
                "add को फ़र्क नहीं पड़ता कि नंबर मिले या टेक्स्ट: + का मतलब वही जो "
                "वैल्यू तय करें। यह लचीलापन पायथन में सामान्य है।",
                "add ko farq nahi padta ki number mile ya text: + ka matlab wahi jo "
                "values tay karein. Ye flexibility Python me normal hai.",
            ),
        ),
        ex(
            'def show(x):\n    print("inside", x)\n\nvalue = show(5)\nprint(value)',
            "inside 5\nNone",
            L("print versus return", "print बनाम return", "print versus return"),
            note=L(
                "show prints but returns nothing, so value is None. print shows text "
                "on screen; return hands a value back to the code that called it.",
                "show प्रिंट करता है पर कुछ लौटाता नहीं, इसलिए value None है। print "
                "स्क्रीन पर दिखाता है; return वैल्यू कोड को वापस देता है।",
                "show print karta hai par kuch return nahi karta, isliye value None "
                "hai. print screen par dikhata hai; return value code ko wapas deta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `square(n)` that returns n multiplied by itself, then print "
                "`square(6)`.",
                "`square(n)` लिखें जो n को उसी से गुणा करके लौटाए, फिर `square(6)` "
                "प्रिंट करें।",
                "`square(n)` likho jo n ko usi se multiply karke return kare, phir "
                "`square(6)` print karo.",
            ),
            "def square(n):\n    # return ...\n\n# print(square(6))\n",
            "def square(n):\n    return n * n\n\nprint(square(6))",
            [
                "callable(square)",
                "square(4) == 16",
                "square(0) == 0",
                "square(-3) == 9",
                '"36" in printed',
            ],
            L(
                "Use return, not print, inside the function.",
                "फ़ंक्शन के अंदर print नहीं, return लिखें।",
                "Function ke andar print nahi, return likho.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does a function return when it has no return statement?",
                "जिस फ़ंक्शन में return नहीं है वह क्या लौटाता है?",
                "Jis function me return nahi hai woh kya return karta hai?",
            ),
            ["0", "None", "an empty string", "an error"],
            "b",
            L(
                "Every Python function returns something. Without return, that "
                "something is None.",
                "हर पायथन फ़ंक्शन कुछ लौटाता है। return के बिना वह कुछ None है।",
                "Har Python function kuch return karta hai. return ke bina woh kuch None hai.",
            ),
            "print-vs-return",
        ),
        quiz(
            L(
                "What is the difference between print(x) and return x?",
                "print(x) और return x में क्या फ़र्क है?",
                "print(x) aur return x me kya farq hai?",
            ),
            [
                "nothing, they are the same",
                "print shows a value on screen; return hands it back to the caller",
                "return shows a value; print stores it",
                "print only works inside functions",
            ],
            "b",
            L(
                "print is a side effect on the screen. return is the value the caller "
                "receives and can store or reuse.",
                "print स्क्रीन पर असर है। return वह वैल्यू है जो बुलाने वाले को "
                "मिलती है और जिसे वह रख या दोबारा इस्तेमाल कर सकता है।",
                "print screen par side effect hai. return woh value hai jo caller ko "
                "milti hai aur jise woh store ya reuse kar sakta hai.",
            ),
            "print-vs-return",
        ),
        quiz(
            L(
                "def double(x): return x * 2 — what is double(5) + 1?",
                "def double(x): return x * 2 — double(5) + 1 क्या है?",
                "def double(x): return x * 2 — double(5) + 1 kya hai?",
            ),
            ["10", "11", "an error", "6"],
            "b",
            L(
                "double(5) is 10, and the call is replaced by its value, so 10 + 1 is "
                "11.",
                "double(5) = 10, और कॉल अपनी वैल्यू से बदल जाती है, इसलिए 10 + 1 = 11।",
                "double(5) = 10, aur call apni value se replace ho jati hai, isliye "
                "10 + 1 = 11.",
            ),
        ),
    ],
    takeaway=L(
        "def names a block; return gives a value back; print only displays.",
        "def ब्लॉक को नाम देता है; return वैल्यू लौटाता है; print सिर्फ़ दिखाता है।",
        "def block ko naam deta hai; return value lautata hai; print sirf dikhata hai.",
    ),
)

l02 = lesson(
    "m05c01l02",
    L("Defaults, *args and **kwargs", "डिफ़ॉल्ट, *args और **kwargs", "Defaults, *args aur **kwargs"),
    ["def"],
    L(
        "Parameters can have default values, so callers may skip them. *args "
        "collects extra positional arguments into a tuple and **kwargs collects "
        "extra named arguments into a dict.",
        "पैरामीटर की डिफ़ॉल्ट वैल्यू हो सकती है, इसलिए बुलाने वाला उन्हें छोड़ सकता "
        "है। *args अतिरिक्त पोज़िशनल आर्ग्युमेंट ट्यूपल में जमा करता है और "
        "**kwargs अतिरिक्त नाम वाले आर्ग्युमेंट dict में।",
        "Parameters ki default value ho sakti hai, isliye caller unhe chhod sakta "
        "hai. *args extra positional arguments tuple me jama karta hai aur "
        "**kwargs extra named arguments dict me.",
    ),
    L(
        "Ordering food: \"one chai\" is enough because size defaults to medium. "
        "\"Two chai, large\" overrides it. A thali restaurant where you just say "
        "\"add this, this, this\" is *args — any number of items, one bill.",
        "खाना ऑर्डर करना: \"एक चाय\" काफ़ी है क्योंकि साइज़ डिफ़ॉल्ट medium है। "
        "\"दो चाय, large\" उसे बदल देता है। थाली वाला रेस्टोरेंट जहाँ आप कहते हैं "
        "\"यह, यह, यह डालो\" वह *args है — कितने भी आइटम, एक बिल।",
        "Khana order karna: \"ek chai\" kaafi hai kyunki size default medium hai. "
        "\"Do chai, large\" use badal deta hai. Thali restaurant jahan aap kehte ho "
        "\"ye, ye, ye daalo\" woh *args hai - kitne bhi items, ek bill.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions",
    examples=[
        ex(
            'def order(item, qty=1, size="medium"):\n    return f"{qty} x {item} ({size})"\n\nprint(order("chai"))\nprint(order("chai", 2))\nprint(order("chai", 2, "large"))\nprint(order("chai", size="large"))',
            "1 x chai (medium)\n2 x chai (medium)\n2 x chai (large)\n1 x chai (large)",
            L("defaults and keyword arguments", "डिफ़ॉल्ट और कीवर्ड आर्ग्युमेंट", "defaults aur keyword arguments"),
            note=L(
                "order(\"chai\", size=\"large\") skips qty by naming the argument you "
                "do want. That only works for parameters after the ones you skip.",
                "order(\"chai\", size=\"large\") qty छोड़ देता है क्योंकि आप चाहा हुआ "
                "आर्ग्युमेंट नाम से देते हैं। यह सिर्फ़ छोड़े गए पैरामीटर के बाद वालों "
                "के लिए चलता है।",
                "order(\"chai\", size=\"large\") qty chhod deta hai kyunki aap chaha "
                "hua argument naam se dete ho. Ye sirf chhode gaye parameter ke baad "
                "walon ke liye chalta hai.",
            ),
        ),
        ex(
            'def total(*prices):\n    return sum(prices)\n\ndef profile(**fields):\n    return ", ".join(f"{k}={v}" for k, v in fields.items())\n\nprint(total(10, 20, 30))\nprint(total())\nprint(profile(name="Asha", city="Pune"))',
            "60\n0\nname=Asha, city=Pune",
            L("*args is a tuple, **kwargs is a dict", "*args ट्यूपल है, **kwargs dict", "*args tuple hai, **kwargs dict"),
            note=L(
                "Inside the function, prices is the tuple (10, 20, 30) and fields is "
                "a dict. The stars are only in the definition and the call.",
                "फ़ंक्शन के अंदर prices ट्यूपल (10, 20, 30) है और fields एक dict है। "
                "स्टार सिर्फ़ परिभाषा और कॉल में होते हैं।",
                "Function ke andar prices tuple (10, 20, 30) hai aur fields ek dict "
                "hai. Stars sirf definition aur call me hote hain.",
            ),
        ),
        ex(
            'def add_item(item, box=[]):\n    box.append(item)\n    return box\n\nprint(add_item("a"))\nprint(add_item("b"))\n\ndef add_safe(item, box=None):\n    if box is None:\n        box = []\n    box.append(item)\n    return box\n\nprint(add_safe("a"))\nprint(add_safe("b"))',
            "['a']\n['a', 'b']\n['a']\n['b']",
            L("the mutable default trap", "म्यूटेबल डिफ़ॉल्ट का जाल", "mutable default ka jaal"),
            note=L(
                "The default [] is created once, when the function is defined, and "
                "shared by every call. box=None is the standard fix.",
                "डिफ़ॉल्ट [] एक बार बनता है, जब फ़ंक्शन परिभाषित होता है, और हर कॉल "
                "में साझा रहता है। box=None मानक समाधान है।",
                "Default [] ek baar banta hai, jab function define hota hai, aur har "
                "call me share hota hai. box=None standard fix hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `area(width, height=1)` that returns width * height, then "
                "print `area(5)` and `area(5, 2)`.",
                "`area(width, height=1)` लिखें जो width * height लौटाए, फिर "
                "`area(5)` और `area(5, 2)` प्रिंट करें।",
                "`area(width, height=1)` likho jo width * height return kare, phir "
                "`area(5)` aur `area(5, 2)` print karo.",
            ),
            "def area(width, height=1):\n    # return ...\n\n# print(area(5))\n# print(area(5, 2))\n",
            "def area(width, height=1):\n    return width * height\n\nprint(area(5))\nprint(area(5, 2))",
            [
                "area(5) == 5",
                "area(5, 2) == 10",
                "area(3, 4) == 12",
                'printed.split() == ["5", "10"]',
            ],
            L(
                "The default makes the second argument optional.",
                "डिफ़ॉल्ट दूसरे आर्ग्युमेंट को वैकल्पिक बनाता है।",
                "Default doosre argument ko optional banata hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "def f(a, b=2) — which calls are valid?",
                "def f(a, b=2) — कौन सी कॉल वैध हैं?",
                "def f(a, b=2) — kaun si calls valid hain?",
            ),
            ["f() only", "f(1) and f(1, 3)", "f(1, 2, 3) only", "f(b=1) only"],
            "b",
            L(
                "a has no default so it must always be given; b may be skipped or "
                "overridden.",
                "a का डिफ़ॉल्ट नहीं है इसलिए वह हमेशा देना होगा; b छोड़ा या बदला जा "
                "सकता है।",
                "a ka default nahi hai isliye woh hamesha dena hoga; b chhoda ya "
                "badla ja sakta hai.",
            ),
        ),
        quiz(
            L(
                "Why is `def f(box=[])` a bug when the function appends to box?",
                "जब फ़ंक्शन box में append करता है तो `def f(box=[])` बग क्यों है?",
                "Jab function box me append karta hai to `def f(box=[])` bug kyun hai?",
            ),
            [
                "lists cannot be defaults",
                "the default list is created once and shared by every call",
                "append is not allowed on a default",
                "it raises a SyntaxError",
            ],
            "b",
            L(
                "Default values are evaluated at definition time, not at call time. "
                "Use None and create a fresh list inside.",
                "डिफ़ॉल्ट वैल्यू परिभाषा के समय तय होती हैं, कॉल के समय नहीं। None "
                "इस्तेमाल करें और अंदर नई लिस्ट बनाएँ।",
                "Default values definition ke time tay hoti hain, call ke time nahi. "
                "None use karo aur andar nayi list banao.",
            ),
            "mutable-default",
        ),
        quiz(
            L("What is the type of args inside def f(*args)?", "def f(*args) में args का टाइप क्या है?", "def f(*args) me args ka type kya hai?"),
            ["list", "tuple", "dict", "set"],
            "b",
            L(
                "*args is a tuple; **kwargs is a dict. That is why args[0] works and "
                "kwargs[\"name\"] works.",
                "*args ट्यूपल है; **kwargs dict है। इसीलिए args[0] और "
                "kwargs[\"name\"] चलते हैं।",
                "*args tuple hai; **kwargs dict hai. Isliye args[0] aur "
                "kwargs[\"name\"] chalte hain.",
            ),
        ),
    ],
    takeaway=L(
        "Defaults make arguments optional; *args is a tuple, **kwargs a dict; never default to a mutable value.",
        "डिफ़ॉल्ट आर्ग्युमेंट वैकल्पिक बनाते हैं; *args ट्यूपल, **kwargs dict; mutable डिफ़ॉल्ट कभी नहीं।",
        "Defaults arguments ko optional banate hain; *args tuple, **kwargs dict; mutable default kabhi nahi.",
    ),
)

l03 = lesson(
    "m05c02l03",
    L("Scope: global and nonlocal", "स्कोप: global और nonlocal", "Scope: global aur nonlocal"),
    ["global", "nonlocal"],
    L(
        "Python looks a name up from the inside out: local, then enclosing "
        "function, then global, then builtins. Assigning a name inside a function "
        "makes it local unless you say global or nonlocal.",
        "पायथन नाम को अंदर से बाहर खोजता है: पहले local, फिर enclosing फ़ंक्शन, फिर "
        "global, फिर builtins। फ़ंक्शन के अंदर किसी नाम को असाइन करना उसे local बना "
        "देता है, जब तक आप global या nonlocal न कहें।",
        "Python naam ko andar se bahar dhoondta hai: pehle local, phir enclosing "
        "function, phir global, phir builtins. Function ke andar kisi naam ko assign "
        "karna use local bana deta hai, jab tak aap global ya nonlocal na kaho.",
    ),
    L(
        "A family budget: the money box in the kitchen is global — anyone can read "
        "it. If you want to change what is in it, you need explicit permission "
        "(global). A locked drawer inside your own room is local.",
        "परिवार का बजट: रसोई का पैसा वाला डिब्बा global है — कोई भी पढ़ सकता है। "
        "उसमें बदलाव करना हो तो साफ़ अनुमति चाहिए (global)। अपने कमरे की बंद दराज़ "
        "local है।",
        "Family budget: kitchen ka paisa wala dibba global hai - koi bhi padh sakta "
        "hai. Usme badlav karna ho to saaf permission chahiye (global). Apne kamre "
        "ki band daraz local hai.",
    ),
    "https://docs.python.org/3/reference/simple_stmts.html#the-global-statement",
    visual="scope_legb",
    examples=[
        ex(
            "count = 0\n\ndef bump():\n    global count\n    count += 1\n\nbump()\nbump()\nprint(count)",
            "2",
            L("global lets a function rebind a module name", "global फ़ंक्शन को मॉड्यूल नाम बदलने देता है", "global function ko module naam badalne deta hai"),
            note=L(
                "Without the global line, count += 1 would create a local count and "
                "then fail with UnboundLocalError when it reads it.",
                "global लाइन के बिना count += 1 एक local count बनाता और फिर उसे पढ़ते "
                "समय UnboundLocalError देता।",
                "global line ke bina count += 1 ek local count banata aur phir use "
                "padhte samay UnboundLocalError deta.",
            ),
        ),
        ex(
            "count = 5\n\ndef outer():\n    total = 0\n    def inner():\n        nonlocal total\n        total += 10\n        return total\n    inner()\n    inner()\n    return total\n\ndef shadow():\n    count = 99\n    return count\n\nprint(outer())\nprint(shadow(), count)",
            "20\n99 5",
            L("nonlocal changes the enclosing function", "nonlocal बाहरी फ़ंक्शन बदलता है", "nonlocal bahari function badalta hai"),
            note=L(
                "inner changes outer's total, so two calls make 20. shadow assigns "
                "its own count and leaves the global one at 5.",
                "inner, outer का total बदलता है, इसलिए दो कॉल 20 बनाते हैं। shadow अपना "
                "count बनाता है और global को 5 ही रहने देता है।",
                "inner, outer ka total badalta hai, isliye do calls 20 banate hain. "
                "shadow apna count banata hai aur global ko 5 hi rehne deta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Make `add_points` add to the module-level `score`, so the program "
                "prints 8.",
                "`add_points` को मॉड्यूल-स्तर के `score` में जोड़ने दें, ताकि प्रोग्राम "
                "8 प्रिंट करे।",
                "`add_points` ko module-level `score` me jodne do, taaki program 8 "
                "print kare.",
            ),
            "score = 0\n\ndef add_points(n):\n    # add n to score\n    pass\n\nadd_points(5)\nadd_points(3)\nprint(score)\n",
            "score = 0\n\ndef add_points(n):\n    global score\n    score += n\n\nadd_points(5)\nadd_points(3)\nprint(score)",
            ["score == 8", 'printed.strip() == "8"'],
            L(
                "One line at the top of the function: global score.",
                "फ़ंक्शन के ऊपर एक लाइन: global score।",
                "Function ke upar ek line: global score.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which keyword lets a function change a module-level variable?",
                "कौन सा कीवर्ड फ़ंक्शन को मॉड्यूल-स्तर वेरिएबल बदलने देता है?",
                "Kaun sa keyword function ko module-level variable badalne deta hai?",
            ),
            ["global", "nonlocal", "public", "outer"],
            "a",
            L(
                "global points at module scope; nonlocal points at the nearest "
                "enclosing function.",
                "global मॉड्यूल स्कोप की ओर इशारा करता है; nonlocal नज़दीकी बाहरी "
                "फ़ंक्शन की ओर।",
                "global module scope ki taraf ishara karta hai; nonlocal nazdeeki "
                "bahari function ki taraf.",
            ),
        ),
        quiz(
            L(
                "What does nonlocal refer to?",
                "nonlocal किसे दर्शाता है?",
                "nonlocal kise darshata hai?",
            ),
            [
                "the builtins namespace",
                "the nearest enclosing function's variable",
                "the module namespace",
                "a variable in another file",
            ],
            "b",
            L(
                "nonlocal is only valid inside a nested function and reaches the "
                "enclosing function's name, not the module's.",
                "nonlocal सिर्फ़ अंदरूनी फ़ंक्शन में वैध है और बाहरी फ़ंक्शन का नाम "
                "पकड़ता है, मॉड्यूल का नहीं।",
                "nonlocal sirf andaruni function me valid hai aur bahari function ka "
                "naam pakadta hai, module ka nahi.",
            ),
        ),
        quiz(
            L(
                "x = 10; def f(): x = 5; f(); print(x) — what prints?",
                "x = 10; def f(): x = 5; f(); print(x) — क्या प्रिंट होगा?",
                "x = 10; def f(): x = 5; f(); print(x) — kya print hoga?",
            ),
            ["5", "10", "None", "an error"],
            "b",
            L(
                "The assignment inside f creates a local x and leaves the global one "
                "alone. This is the single most common scope surprise.",
                "f के अंदर असाइनमेंट एक local x बनाता है और global को छोड़ देता है। "
                "स्कोप का यह सबसे आम आश्चर्य है।",
                "f ke andar assignment ek local x banata hai aur global ko chhod deta "
                "hai. Scope ka ye sabse aam surprise hai.",
            ),
            "scope-shadowing",
        ),
    ],
    takeaway=L(
        "Lookup goes local, enclosing, global, builtins; assignment makes a name local unless declared global or nonlocal.",
        "खोज local, enclosing, global, builtins क्रम में; असाइनमेंट नाम को local बनाता है जब तक global/nonlocal न कहें।",
        "Lookup local, enclosing, global, builtins; assignment naam ko local banata hai jab tak global/nonlocal na kaho.",
    ),
)

l04 = lesson(
    "m05c02l04",
    L("lambda: small anonymous functions", "lambda: छोटे बिना-नाम फ़ंक्शन", "lambda: chhote bina-naam functions"),
    ["lambda"],
    L(
        "A lambda is a function written in one expression, without a name. It can "
        "only contain a single expression and returns its result automatically. It "
        "exists for the places where a tiny function is needed once.",
        "lambda एक एक्सप्रेशन में लिखा फ़ंक्शन है, बिना नाम। इसमें सिर्फ़ एक "
        "एक्सप्रेशन हो सकता है और उसका परिणाम अपने आप लौटता है। यह उन जगहों के लिए "
        "है जहाँ एक बार के लिए छोटा फ़ंक्शन चाहिए।",
        "lambda ek expression me likha function hai, bina naam. Isme sirf ek "
        "expression ho sakta hai aur uska result apne aap return hota hai. Ye un "
        "jagahon ke liye hai jahan ek baar ke liye chhota function chahiye.",
    ),
    L(
        "Sorting a contact list by age, or a price list by amount: you do not want "
        "to write a full named function just to say \"compare this field\". That is "
        "exactly what key=lambda does in one line.",
        "कॉन्टैक्ट लिस्ट को उम्र से, या कीमत की लिस्ट को रकम से सॉर्ट करना: सिर्फ़ "
        "\"इस फ़ील्ड से तुलना करो\" कहने के लिए पूरा नाम वाला फ़ंक्शन नहीं लिखना "
        "चाहते। key=lambda यही एक लाइन में करता है।",
        "Contact list ko age se, ya price list ko amount se sort karna: sirf \"is "
        "field se compare karo\" kehne ke liye poora named function nahi likhna "
        "chahte. key=lambda yahi ek line me karta hai.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#lambda-expressions",
    examples=[
        ex(
            "double = lambda x: x * 2\nprint(double(7))\nprint((lambda a, b: a + b)(3, 4))",
            "14\n7",
            L("a lambda with a name, and one without", "नाम वाला lambda, और बिना नाम वाला", "naam wala lambda, aur bina naam wala"),
            note=L(
                "The second line calls the lambda immediately by putting arguments "
                "in brackets right after it.",
                "दूसरी लाइन lambda को तुरंत बुलाती है — उसके ठीक बाद ब्रैकेट में "
                "आर्ग्युमेंट देकर।",
                "Doosri line lambda ko turant call karti hai - uske theek baad bracket "
                "me arguments dekar.",
            ),
        ),
        ex(
            'people = [("Asha", 30), ("Ravi", 25), ("Meera", 35)]\npeople.sort(key=lambda p: p[1])\nprint(people)\nprint(sorted(people, key=lambda p: p[0], reverse=True))',
            "[('Ravi', 25), ('Asha', 30), ('Meera', 35)]\n[('Ravi', 25), ('Meera', 35), ('Asha', 30)]",
            L("sorting by one field", "एक फ़ील्ड से सॉर्ट करना", "ek field se sort karna"),
            note=L(
                "key receives each item and returns the value to compare. p[1] means "
                "the second item of the tuple, which is the age.",
                "key हर आइटम लेता है और तुलना की वैल्यू लौटाता है। p[1] ट्यूपल का "
                "दूसरा आइटम है, यानी उम्र।",
                "key har item leta hai aur compare ki value return karta hai. p[1] "
                "tuple ka doosra item hai, yani age.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Using a lambda as the key, sort `words = ['banana', 'fig', 'kiwi']` "
                "by length into `by_len` and print it.",
                "lambda को key बनाकर `words = ['banana', 'fig', 'kiwi']` को लंबाई से "
                "सॉर्ट करके `by_len` में रखें और प्रिंट करें।",
                "lambda ko key bana kar `words = ['banana', 'fig', 'kiwi']` ko length "
                "se sort karke `by_len` me rakho aur print karo.",
            ),
            "words = ['banana', 'fig', 'kiwi']\n# by_len = sorted(...)\n# print(by_len)\n",
            "words = ['banana', 'fig', 'kiwi']\nby_len = sorted(words, key=lambda w: len(w))\nprint(by_len)",
            [
                "by_len == ['fig', 'kiwi', 'banana']",
                "words == ['banana', 'fig', 'kiwi']",
                "str(by_len) in printed",
            ],
            L(
                "key=lambda w: len(w) gives sorted() the number to compare.",
                "key=lambda w: len(w) sorted() को तुलना का नंबर देता है।",
                "key=lambda w: len(w) sorted() ko compare ka number deta hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What can the body of a lambda contain?",
                "lambda की बॉडी में क्या हो सकता है?",
                "lambda ki body me kya ho sakta hai?",
            ),
            [
                "any number of statements",
                "exactly one expression",
                "only a return statement",
                "only a print call",
            ],
            "b",
            L(
                "One expression, whose value is returned. If you need several "
                "statements or a docstring, write a normal def.",
                "एक एक्सप्रेशन, जिसकी वैल्यू लौटती है। कई स्टेटमेंट या docstring "
                "चाहिए तो सामान्य def लिखें।",
                "Ek expression, jiski value return hoti hai. Kai statements ya "
                "docstring chahiye to normal def likho.",
            ),
        ),
        quiz(
            L("What is (lambda x: x + 1)(4)?", "(lambda x: x + 1)(4) क्या है?", "(lambda x: x + 1)(4) kya hai?"),
            ["4", "5", "an error", "x + 1"],
            "b",
            L(
                "The lambda is called with 4, so x is 4 and the result is 5.",
                "lambda को 4 के साथ बुलाया गया, इसलिए x = 4 और परिणाम 5 है।",
                "lambda ko 4 ke saath bulaya gaya, isliye x = 4 aur result 5 hai.",
            ),
        ),
        quiz(
            L(
                "When should you prefer def over lambda?",
                "def को lambda पर कब प्राथमिकता दें?",
                "def ko lambda par kab priority dein?",
            ),
            [
                "never, lambda is always better",
                "when the function needs a name, a docstring or several statements",
                "when the function has parameters",
                "when you use it with sorted()",
            ],
            "b",
            L(
                "lambda is for throwaway one-liners. Anything you need to explain, "
                "name or reuse belongs in a def.",
                "lambda एक बार के one-liner के लिए है। जिसे समझाना, नाम देना या "
                "दोबारा इस्तेमाल करना हो वह def में जाना चाहिए।",
                "lambda ek baar ke one-liner ke liye hai. Jise samjhana, naam dena ya "
                "reuse karna ho woh def me jaana chahiye.",
            ),
        ),
    ],
    takeaway=L(
        "lambda is a one-expression function; use it for key= and other throwaway callbacks.",
        "lambda एक-एक्सप्रेशन फ़ंक्शन है; key= और एक बार के कॉलबैक के लिए इस्तेमाल करें।",
        "lambda ek-expression function hai; key= aur ek baar ke callbacks ke liye use karo.",
    ),
)

l05 = lesson(
    "m05c02l05",
    L("Recursion", "रिकर्शन", "Recursion"),
    ["def", "return"],
    L(
        "A recursive function calls itself on a smaller version of the same "
        "problem. Every recursive function needs a base case that stops the "
        "calling, or it runs until Python raises RecursionError.",
        "रिकर्सिव फ़ंक्शन खुद को उसी समस्या के छोटे रूप पर बुलाता है। हर रिकर्सिव "
        "फ़ंक्शन को एक बेस केस चाहिए जो कॉल रोके, वरना वह तब तक चलता है जब तक "
        "पायथन RecursionError न दे।",
        "Recursive function khud ko usi problem ke chhote roop par bulata hai. Har "
        "recursive function ko ek base case chahiye jo call roke, warna woh tab tak "
        "chalta hai jab tak Python RecursionError na de.",
    ),
    L(
        "Standing between two mirrors: you see a copy inside a copy inside a copy. "
        "The copies get smaller and stop at the mirror's edge — that edge is the "
        "base case.",
        "दो आईनों के बीच खड़े होना: आप एक कॉपी के अंदर कॉपी के अंदर कॉपी देखते हैं। "
        "कॉपियाँ छोटी होती जाती हैं और आईने के किनारे पर रुक जाती हैं — वही किनारा "
        "बेस केस है।",
        "Do aainon ke beech khade hona: aap ek copy ke andar copy ke andar copy "
        "dekhte ho. Copies chhoti hoti jaati hain aur aaine ke kinare par ruk jaati "
        "hain - wahi kinara base case hai.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#defining-functions",
    examples=[
        ex(
            "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))\nprint(factorial(1))",
            "120\n1",
            L("factorial", "फ़ैक्टोरियल", "factorial"),
            note=L(
                "factorial(5) becomes 5 * 4 * 3 * 2 * 1. The base case n <= 1 stops "
                "the chain.",
                "factorial(5) = 5 * 4 * 3 * 2 * 1 बन जाता है। बेस केस n <= 1 चेन रोकता है।",
                "factorial(5) = 5 * 4 * 3 * 2 * 1 ban jata hai. Base case n <= 1 chain rokta hai.",
            ),
        ),
        ex(
            'def countdown(n):\n    if n == 0:\n        print("liftoff")\n        return\n    print(n)\n    countdown(n - 1)\n\ncountdown(3)',
            "3\n2\n1\nliftoff",
            L("a countdown", "उल्टी गिनती", "ulti ginti"),
            note=L(
                "The prints happen on the way down, before each recursive call. That "
                "order is what makes the output count downwards.",
                "प्रिंट नीचे जाते समय होते हैं, हर रिकर्सिव कॉल से पहले। इसी क्रम से "
                "आउटपुट उल्टा गिनता है।",
                "Prints neeche jaate samay hote hain, har recursive call se pehle. "
                "Isi order se output ulta ginta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `total(nums)` recursively: an empty list is 0, otherwise the "
                "first item plus the total of the rest.",
                "`total(nums)` रिकर्सिव लिखें: खाली लिस्ट 0 है, वरना पहला आइटम प्लस "
                "बाकी का टोटल।",
                "`total(nums)` recursive likho: khaali list 0 hai, warna pehla item "
                "plus baaki ka total.",
            ),
            "def total(nums):\n    # base case, then recursive case\n\n# print(total([1, 2, 3]))\n",
            "def total(nums):\n    if not nums:\n        return 0\n    return nums[0] + total(nums[1:])\n\nprint(total([1, 2, 3]))",
            ["total([1, 2, 3]) == 6", "total([]) == 0", "total([5]) == 5", 'printed.strip() == "6"'],
            L(
                "`if not nums: return 0` is the base case.",
                "`if not nums: return 0` बेस केस है।",
                "`if not nums: return 0` base case hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What must every recursive function have?",
                "हर रिकर्सिव फ़ंक्शन में क्या होना चाहिए?",
                "Har recursive function me kya hona chahiye?",
            ),
            [
                "a loop",
                "a base case that stops the recursion",
                "a global variable",
                "a lambda",
            ],
            "b",
            L(
                "Without a base case the calls never stop and Python raises "
                "RecursionError after about a thousand levels.",
                "बेस केस के बिना कॉल कभी नहीं रुकते और पायथन लगभग हज़ार स्तरों के बाद "
                "RecursionError देता है।",
                "Base case ke bina calls kabhi nahi rukte aur Python lagbhag hazaar "
                "levels ke baad RecursionError deta hai.",
            ),
        ),
        quiz(
            L(
                "Is recursion faster than a loop in Python?",
                "क्या पायथन में रिकर्शन लूप से तेज़ है?",
                "Kya Python me recursion loop se tez hai?",
            ),
            [
                "yes, always",
                "no, a loop is usually faster and has no depth limit",
                "only for numbers",
                "only inside a class",
            ],
            "b",
            L(
                "Every call costs a stack frame, and Python has a recursion limit. "
                "Recursion is a clarity tool, not a speed tool.",
                "हर कॉल एक स्टैक फ़्रेम लेती है, और पायथन की रिकर्शन सीमा है। रिकर्शन "
                "स्पष्टता का औज़ार है, तेज़ी का नहीं।",
                "Har call ek stack frame leti hai, aur Python ki recursion limit hai. "
                "Recursion clarity ka tool hai, speed ka nahi.",
            ),
        ),
        quiz(
            L(
                "def f(n): return f(n - 1) — what happens when you call f(3)?",
                "def f(n): return f(n - 1) — f(3) बुलाने पर क्या होगा?",
                "def f(n): return f(n - 1) — f(3) bulane par kya hoga?",
            ),
            ["it returns 2", "it returns None", "RecursionError", "SyntaxError"],
            "c",
            L(
                "There is no base case, so the calls keep going until the stack "
                "limit is hit.",
                "कोई बेस केस नहीं है, इसलिए कॉल तब तक चलते हैं जब तक स्टैक सीमा न "
                "पहुँचे।",
                "Koi base case nahi hai, isliye calls tab tak chalte hain jab tak "
                "stack limit na pahunche.",
            ),
        ),
    ],
    takeaway=L(
        "Recursion needs a base case; it trades stack depth for a shorter, clearer definition.",
        "रिकर्शन को बेस केस चाहिए; यह स्टैक गहराई के बदले छोटी और साफ़ परिभाषा देता है।",
        "Recursion ko base case chahiye; ye stack depth ke badle chhoti aur saaf definition deta hai.",
    ),
)

MODULE = module(
    M,
    L("Functions", "फ़ंक्शन", "Functions"),
    L(
        "Name a block of work once and reuse it: return values, defaults, *args, "
        "scope, lambda and recursion.",
        "काम के ब्लॉक को एक बार नाम दें और दोबारा इस्तेमाल करें: return वैल्यू, "
        "डिफ़ॉल्ट, *args, स्कोप, lambda और रिकर्शन।",
        "Kaam ke block ko ek baar naam do aur dobara use karo: return values, "
        "defaults, *args, scope, lambda aur recursion.",
    ),
    [
        chapter("m05c01", L("Writing functions", "फ़ंक्शन लिखना", "Functions likhna"), [l01, l02]),
        chapter("m05c02", L("Scope and small functions", "स्कोप और छोटे फ़ंक्शन", "Scope aur chhote functions"), [l03, l04, l05]),
    ],
    exam=[
        quiz(
            L("What is f(3) if def f(x): return x * x?", "def f(x): return x * x हो तो f(3) क्या है?", "def f(x): return x * x ho to f(3) kya hai?"),
            ["6", "9", "3", "None"],
            "b",
            L("3 * 3 = 9.", "3 * 3 = 9।", "3 * 3 = 9."),
        ),
        quiz(
            L("What is printed by: def f(): pass — print(f())", "क्या प्रिंट होगा: def f(): pass — print(f())", "Kya print hoga: def f(): pass — print(f())"),
            ["0", "None", "nothing", "an error"],
            "b",
            L("pass does nothing, so the function returns None.", "pass कुछ नहीं करता, इसलिए फ़ंक्शन None लौटाता है।", "pass kuch nahi karta, isliye function None lautata hai."),
        ),
        quiz(
            L("Which call is invalid for def f(a, b=1)?", "def f(a, b=1) के लिए कौन सी कॉल अवैध है?", "def f(a, b=1) ke liye kaun si call invalid hai?"),
            ["f(1)", "f(1, 2)", "f(b=2, a=1)", "f()"],
            "d",
            L("a has no default, so f() is missing a required argument.", "a का डिफ़ॉल्ट नहीं है, इसलिए f() में ज़रूरी आर्ग्युमेंट गायब है।", "a ka default nahi hai, isliye f() me zaroori argument gayab hai."),
        ),
        quiz(
            L("What is the type of kwargs in def f(**kwargs)?", "def f(**kwargs) में kwargs का टाइप क्या है?", "def f(**kwargs) me kwargs ka type kya hai?"),
            ["tuple", "list", "dict", "set"],
            "c",
            L("**kwargs collects named arguments into a dict.", "**kwargs नाम वाले आर्ग्युमेंट dict में जमा करता है।", "**kwargs named arguments dict me jama karta hai."),
        ),
        quiz(
            L("x = 1; def f(): x = 2; f(); print(x) — what prints?", "x = 1; def f(): x = 2; f(); print(x) — क्या प्रिंट होगा?", "x = 1; def f(): x = 2; f(); print(x) — kya print hoga?"),
            ["1", "2", "None", "an error"],
            "a",
            L("The assignment inside f is local, so the global x stays 1.", "f के अंदर असाइनमेंट local है, इसलिए global x 1 ही रहता है।", "f ke andar assignment local hai, isliye global x 1 hi rehta hai."),
        ),
        quiz(
            L("Which is the correct lambda for squaring?", "वर्ग करने के लिए सही lambda कौन सा है?", "Square karne ke liye sahi lambda kaun sa hai?"),
            ["lambda x: x * x", "lambda x: return x * x", "lambda (x): x * x", "lambda x -> x * x"],
            "a",
            L("A lambda has no return keyword and takes plain parameter names.", "lambda में return कीवर्ड नहीं होता और सादे पैरामीटर नाम होते हैं।", "lambda me return keyword nahi hota aur saade parameter naam hote hain."),
        ),
    ],
    icon="🧰",
)
