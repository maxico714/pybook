"""Module 1 - Starting Out: the first hour with Python."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m01"

# --------------------------------------------------------------- chapter 1

l01 = lesson(
    "m01c01l01",
    L("Your first program", "आपका पहला प्रोग्राम", "Aapka pehla program"),
    [],
    L(
        "Python is a programming language: you write instructions in a text file "
        "and Python carries them out, one line at a time, from top to bottom.",
        "पायथन एक प्रोग्रामिंग भाषा है: आप निर्देश लिखते हैं और पायथन उन्हें "
        "एक-एक करके, ऊपर से नीचे तक चलाता है।",
        "Python ek programming language hai: aap instructions likhte ho aur Python "
        "unhe ek-ek karke, upar se neeche tak chalata hai.",
    ),
    L(
        "Think of a recipe. \"Boil water\" is one instruction, \"add tea leaves\" is "
        "the next. A program is the same list of steps, but written so precisely "
        "that a machine can follow it without guessing.",
        "रेसिपी की तरह सोचिए। \"पानी उबालो\" एक निर्देश है, \"चायपत्ती डालो\" अगला। "
        "प्रोग्राम भी स्टेप्स की ऐसी ही लिस्ट है, बस इतनी साफ़ लिखी हुई कि मशीन "
        "बिना अंदाज़ा लगाए उसे चला सके।",
        "Recipe ki tarah socho. \"Paani ubalo\" ek instruction hai, \"chai patti daalo\" "
        "agla. Program bhi steps ki wahi list hai, bas itni saaf likhi hui ki machine "
        "bina andaza lagaye use chala sake.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator",
    visual="variables",
    examples=[
        ex(
            'print("Namaste, Python!")\nprint(2 + 3)',
            "Namaste, Python!\n5",
            L("print shows a value", "print वैल्यू दिखाता है", "print value dikhata hai"),
        ),
        ex(
            '# this line is a comment: Python ignores it\nprint("Price:", 250, "rupees")\nprint("Total:", 250 * 3)',
            "Price: 250 rupees\nTotal: 750",
            L(
                "comments and several values",
                "कमेंट और कई वैल्यू",
                "comment aur kai values",
            ),
            note=L(
                "print() puts one space between the values you give it.",
                "print() दी गई वैल्यू के बीच एक स्पेस डालता है।",
                "print() di gayi values ke beech ek space daalta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Print two lines: first `Namaste, Python!` and then "
                "`I am learning Python.`",
                "दो लाइनें प्रिंट करें: पहले `Namaste, Python!` और फिर "
                "`I am learning Python.`",
                "Do lines print karo: pehle `Namaste, Python!` aur phir "
                "`I am learning Python.`",
            ),
            "# write two print() calls\n",
            'print("Namaste, Python!")\nprint("I am learning Python.")',
            [
                '"Namaste, Python!" in printed.splitlines()',
                '"I am learning Python." in printed.splitlines()',
                "len(printed.splitlines()) == 2",
            ],
            L(
                "One print() call per line.",
                "हर लाइन के लिए एक print() कॉल।",
                "Har line ke liye ek print() call.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does this program print?",
                "यह प्रोग्राम क्या प्रिंट करेगा?",
                "Ye program kya print karega?",
            ),
            ["7", "3 + 4", "34", "an error"],
            "a",
            L(
                "Python works out 3 + 4 first and prints the result, 7. Quotes would "
                "be needed to print the text itself.",
                "पायथन पहले 3 + 4 जोड़ता है और परिणाम 7 प्रिंट करता है। टेक्स्ट "
                "प्रिंट करने के लिए कोटेशन चाहिए होते।",
                "Python pehle 3 + 4 jodta hai aur result 7 print karta hai. Text "
                "print karne ke liye quotes chahiye hote.",
            ),
            "quotes",
        ),
        quiz(
            L("Which line is a comment?", "कौन सी लाइन कमेंट है?", "Kaun si line comment hai?"),
            ["print('hi')", "# print('hi')", "print('#hi')", "'# print hi'"],
            "b",
            L(
                "A comment starts with #. Inside quotes the # is just text, which is "
                "why option c prints it.",
                "# से कमेंट शुरू होता है। कोटेशन के अंदर # सिर्फ़ टेक्स्ट है, इसलिए "
                "विकल्प c उसे प्रिंट करता है।",
                "# se comment shuru hota hai. Quotes ke andar # sirf text hai, isliye "
                "option c use print karta hai.",
            ),
        ),
        quiz(
            L(
                "In what order does Python run the lines of a program?",
                "पायथन लाइनों को किस क्रम में चलाता है?",
                "Python lines ko kis order me chalata hai?",
            ),
            [
                "random order",
                "bottom to top",
                "top to bottom",
                "only the first line",
            ],
            "c",
            L(
                "Execution is top to bottom unless a loop or a function call sends it "
                "somewhere else.",
                "निष्पादन ऊपर से नीचे होता है, जब तक कोई लूप या फ़ंक्शन कॉल उसे "
                "कहीं और न भेज दे।",
                "Execution upar se neeche hota hai, jab tak koi loop ya function call "
                "use kahin aur na bhej de.",
            ),
        ),
    ],
    takeaway=L(
        "print() shows values; # starts a comment; code runs top to bottom.",
        "print() वैल्यू दिखाता है; # कमेंट शुरू करता है; कोड ऊपर से नीचे चलता है।",
        "print() value dikhata hai; # comment shuru karta hai; code upar se neeche chalta hai.",
    ),
)

l02 = lesson(
    "m01c01l02",
    L("Expressions and your first error", "एक्सप्रेशन और पहली एरर", "Expression aur pehli error"),
    [],
    L(
        "An expression is anything Python can turn into a value: 2 + 3, 'a' * 3, or "
        "len('hello'). When you give Python something it cannot do, it stops and "
        "shows an error message instead of guessing.",
        "एक्सप्रेशन वह है जिसे पायथन एक वैल्यू में बदल सकता है: 2 + 3, 'a' * 3, या "
        "len('hello')। जब आप पायथन को कुछ ऐसा देते हैं जो वह नहीं कर सकता, तो वह "
        "रुक जाता है और अंदाज़ा लगाने की जगह एरर दिखाता है।",
        "Expression woh hai jise Python ek value me badal sakta hai: 2 + 3, 'a' * 3, "
        "ya len('hello'). Jab aap Python ko kuch aisa dete ho jo woh nahi kar sakta, "
        "to woh ruk jata hai aur andaza lagane ki jagah error dikhata hai.",
    ),
    L(
        "A calculator shows \"Error\" when you divide by zero. Python is more helpful: "
        "it says which line, which kind of problem, and what it was doing. Reading "
        "that message is a skill worth learning on day one.",
        "कैलकुलेटर ज़ीरो से भाग देने पर बस \"Error\" दिखाता है। पायथन ज़्यादा मदद करता "
        "है: कौन सी लाइन, किस तरह की दिक्कत, और वह क्या कर रहा था। उस मैसेज को "
        "पढ़ना पहले दिन सीखने लायक कौशल है।",
        "Calculator zero se divide karne par bas \"Error\" dikhata hai. Python zyada "
        "madad karta hai: kaun si line, kis tarah ki dikkat, aur woh kya kar raha tha. "
        "Us message ko padhna pehle din seekhne layak skill hai.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator",
    examples=[
        ex(
            'print(10 / 2)\nprint("ha" * 3)\nprint(len("hello"))',
            "5.0\nhahaha\n5",
            L("three expressions", "तीन एक्सप्रेशन", "teen expressions"),
        ),
        ex(
            'print(10 / 0)',
            "",
            L("this one fails on purpose", "यह जान-बूझकर फेल होता है", "ye jaan-boojh kar fail hota hai"),
            note=L(
                "ZeroDivisionError: division by zero. The last line of the message "
                "names the problem; the line above it shows where.",
                "ZeroDivisionError: division by zero. मैसेज की आख़िरी लाइन समस्या "
                "बताती है; उसके ऊपर की लाइन बताती है कहाँ।",
                "ZeroDivisionError: division by zero. Message ki aakhri line problem "
                "batati hai; uske upar ki line batati hai kahan.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Print the remainder when 17 is divided by 5. Use the % operator.",
                "17 को 5 से भाग देने पर बचा शेष प्रिंट करें। % ऑपरेटर इस्तेमाल करें।",
                "17 ko 5 se divide karne par bacha remainder print karo. % operator use karo.",
            ),
            "# one line, using %\n",
            "print(17 % 5)",
            ['printed.strip() == "2"'],
            L("a % b gives what is left over.", "a % b बचा हुआ देता है।", "a % b bacha hua deta hai."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is 10 / 2 in Python?", "पायथन में 10 / 2 क्या है?", "Python me 10 / 2 kya hai?"),
            ["5", "5.0", "2", "0.5"],
            "b",
            L(
                "A single / always produces a float, even when the division is exact. "
                "10 // 2 would give the int 5.",
                "अकेला / हमेशा float देता है, चाहे भाग पूरा बंट जाए। 10 // 2 int 5 देता।",
                "Akela / hamesha float deta hai, chahe division poora bat jaaye. "
                "10 // 2 int 5 deta.",
            ),
            "division-type",
        ),
        quiz(
            L(
                "A program stops with ZeroDivisionError. What happened?",
                "प्रोग्राम ZeroDivisionError पर रुक गया। क्या हुआ?",
                "Program ZeroDivisionError par ruk gaya. Kya hua?",
            ),
            [
                "a variable was never created",
                "something was divided by zero",
                "a quote mark was missing",
                "the number was too big",
            ],
            "b",
            L(
                "The exception name is a literal description. Learning to read the "
                "name first, then the line number, solves most beginner errors.",
                "एक्सेप्शन का नाम ही विवरण है। पहले नाम पढ़ना, फिर लाइन नंबर — इससे "
                "ज़्यादातर शुरुआती एरर हल हो जाती हैं।",
                "Exception ka naam hi description hai. Pehle naam padhna, phir line "
                "number - isse zyadatar beginner errors hal ho jati hain.",
            ),
        ),
        quiz(
            L('What is "ha" * 3?', '"ha" * 3 क्या है?', '"ha" * 3 kya hai?'),
            ["hahaha", "ha3", "an error", "haha"],
            "a",
            L(
                "Multiplying a string by an int repeats it. Adding a number instead "
                "(a + 3) would raise a TypeError.",
                "स्ट्रिंग को int से गुणा करने पर वह दोहराई जाती है। उसकी जगह नंबर "
                "जोड़ने (a + 3) पर TypeError आता।",
                "String ko int se multiply karne par woh repeat hoti hai. Uski jagah "
                "number add karne (a + 3) par TypeError aata.",
            ),
        ),
    ],
    takeaway=L(
        "Read errors from the last line upwards: type of error, then where.",
        "एरर को आख़िरी लाइन से ऊपर की ओर पढ़ें: पहले एरर का प्रकार, फिर जगह।",
        "Error ko aakhri line se upar ki taraf padho: pehle error ka type, phir jagah.",
    ),
)

# --------------------------------------------------------------- chapter 2

l03 = lesson(
    "m01c02l03",
    L("Variables and assignment", "वेरिएबल और असाइनमेंट", "Variable aur assignment"),
    [],
    L(
        "A variable is a name you attach to a value so you can use it again. The = "
        "sign means \"store this value under this name\"; it is not the maths equals "
        "sign, so a = a + 1 is perfectly legal.",
        "वेरिएबल एक नाम है जो आप किसी वैल्यू से जोड़ते हैं ताकि उसे दोबारा इस्तेमाल "
        "कर सकें। = का मतलब है \"इस वैल्यू को इस नाम में रखो\"; यह गणित का बराबर "
        "नहीं है, इसलिए a = a + 1 बिल्कुल वैध है।",
        "Variable ek naam hai jo aap kisi value se jodte ho taaki use dobara use kar "
        "sako. = ka matlab hai \"is value ko is naam me rakho\"; ye maths ka equals "
        "nahi hai, isliye a = a + 1 bilkul valid hai.",
    ),
    L(
        "Your phone's contact list: \"Mummy\" is a name pointing at one number. If "
        "Mummy changes her number you update the entry once and every place that "
        "says \"Mummy\" now means the new number. The name did not change, the value did.",
        "फ़ोन की कॉन्टैक्ट लिस्ट: \"Mummy\" एक नाम है जो एक नंबर की ओर इशारा करता है। "
        "अगर Mummy नंबर बदल दें तो आप एक जगह अपडेट करते हैं और हर जगह \"Mummy\" का "
        "मतलब नया नंबर हो जाता है। नाम नहीं बदला, वैल्यू बदली।",
        "Phone ki contact list: \"Mummy\" ek naam hai jo ek number ki taraf point "
        "karta hai. Agar Mummy number badal dein to aap ek jagah update karte ho aur "
        "har jagah \"Mummy\" ka matlab naya number ho jata hai. Naam nahi badla, value badli.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#first-steps-towards-programming",
    visual="variables",
    examples=[
        ex(
            'city = "Pune"\nprint(city)\nprint(city + " is in India")',
            "Pune\nPune is in India",
            L("store, then reuse", "रखो, फिर दोबारा इस्तेमाल करो", "store karo, phir reuse karo"),
        ),
        ex(
            "score = 10\nscore = score + 5\nprint(score)\nscore += 2\nprint(score)",
            "15\n17",
            L("updating a variable", "वेरिएबल अपडेट करना", "variable update karna"),
            note=L(
                "score += 2 is shorthand for score = score + 2.",
                "score += 2, score = score + 2 का छोटा रूप है।",
                "score += 2, score = score + 2 ka chhota roop hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Create `name` (a string) and `age` (a whole number), then print both "
                "in one print() call.",
                "`name` (स्ट्रिंग) और `age` (पूरा नंबर) बनाएँ, फिर दोनों को एक ही "
                "print() में प्रिंट करें।",
                "`name` (string) aur `age` (poore number) banao, phir dono ko ek hi "
                "print() me print karo.",
            ),
            '# name = ...\n# age = ...\n',
            'name = "Aarav"\nage = 14\nprint(name, "is", age)',
            [
                "isinstance(name, str)",
                "isinstance(age, int) and not isinstance(age, bool)",
                "name in printed",
                "str(age) in printed",
            ],
            L(
                "A whole number has no decimal point.",
                "पूरे नंबर में दशमलव नहीं होता।",
                "Poore number me decimal nahi hota.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "After these lines, what is x?",
                "इन लाइनों के बाद x क्या है?",
                "In lines ke baad x kya hai?",
            ),
            ["3", "5", "8", "an error"],
            "c",
            L(
                "x = 3 then x = x + 5 reads the old value (3), adds 5, and stores 8. "
                "The right side is always worked out first.",
                "x = 3 फिर x = x + 5 पुरानी वैल्यू (3) पढ़ता है, 5 जोड़ता है और 8 रखता "
                "है। दाईं ओर हमेशा पहले हल होती है।",
                "x = 3 phir x = x + 5 purani value (3) padhta hai, 5 jodta hai aur 8 "
                "rakhta hai. Right side hamesha pehle solve hoti hai.",
            ),
            "assignment-vs-equals",
        ),
        quiz(
            L(
                "Which name is NOT allowed as a Python variable?",
                "कौन सा नाम पायथन वेरिएबल के लिए मान्य नहीं है?",
                "Kaun sa naam Python variable ke liye valid nahi hai?",
            ),
            ["total_2", "_temp", "2total", "Total"],
            "c",
            L(
                "A name cannot start with a digit. total_2 is fine because the digit "
                "is not first.",
                "नाम अंक से शुरू नहीं हो सकता। total_2 ठीक है क्योंकि अंक पहले नहीं है।",
                "Naam digit se shuru nahi ho sakta. total_2 theek hai kyunki digit "
                "pehle nahi hai.",
            ),
        ),
        quiz(
            L(
                "What does print(type(5)) show?",
                "print(type(5)) क्या दिखाता है?",
                "print(type(5)) kya dikhata hai?",
            ),
            ["5", "<class 'int'>", "int", "<class 'number'>"],
            "b",
            L(
                "type() returns a type object, and printing it shows its repr. "
                "That is why the answer has the angle brackets.",
                "type() एक टाइप ऑब्जेक्ट देता है, और उसे प्रिंट करने पर उसका repr "
                "दिखता है। इसीलिए जवाब में कोणीय ब्रैकेट हैं।",
                "type() ek type object deta hai, aur use print karne par uska repr "
                "dikhta hai. Isliye answer me angle brackets hain.",
            ),
        ),
    ],
    takeaway=L(
        "= stores a value under a name; the right-hand side is computed first.",
        "= किसी वैल्यू को नाम में रखता है; दाईं ओर पहले हल होती है।",
        "= value ko naam me store karta hai; right side pehle solve hoti hai.",
    ),
)

l04 = lesson(
    "m01c02l04",
    L("Numbers: int and float", "नंबर: int और float", "Numbers: int aur float"),
    [],
    L(
        "Python has two everyday number types: int for whole numbers (7, -3, "
        "1000000) and float for numbers with a decimal point (3.5, -0.25). The type "
        "follows the value, you never declare it.",
        "पायथन में दो आम नंबर टाइप हैं: int पूरे नंबरों के लिए (7, -3, 1000000) और "
        "float दशमलव वाले नंबरों के लिए (3.5, -0.25)। टाइप वैल्यू से तय होता है, "
        "आप उसे घोषित नहीं करते।",
        "Python me do aam number types hain: int poore numbers ke liye (7, -3, "
        "1000000) aur float decimal wale numbers ke liye (3.5, -0.25). Type value se "
        "tay hota hai, aap use declare nahi karte.",
    ),
    L(
        "Money is a good example of why types matter. A shop bill of ₹250 is a whole "
        "number; 12.5% GST on it is 31.25, which is not. Python keeps them as "
        "different types, and mixing them gives a float.",
        "पैसा अच्छा उदाहरण है कि टाइप क्यों मायने रखता है। ₹250 का बिल पूरा नंबर है; "
        "उस पर 12.5% GST = 31.25, जो पूरा नंबर नहीं है। पायथन इन्हें अलग टाइप "
        "रखता है, और मिलाने पर float मिलता है।",
        "Paisa achha example hai ki type kyun matter karta hai. ₹250 ka bill poora "
        "number hai; us par 12.5% GST = 31.25, jo poora number nahi hai. Python inhe "
        "alag type rakhta hai, aur milane par float milta hai.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#numbers",
    visual="types",
    examples=[
        ex(
            "print(type(7))\nprint(type(7.0))\nprint(7 + 2, 7 - 2, 7 * 2)",
            "<class 'int'>\n<class 'float'>\n9 5 14",
            L("two number types", "दो नंबर टाइप", "do number types"),
        ),
        ex(
            'print(int("42") + 8)\nprint(float("2.5") * 4)\nprint(round(0.1 + 0.2, 2))',
            "50\n10.0\n0.3",
            L("converting and rounding", "बदलना और राउंड करना", "convert aur round karna"),
            note=L(
                "int() and float() turn text into numbers. round(x, 2) keeps two "
                "decimals.",
                "int() और float() टेक्स्ट को नंबर बनाते हैं। round(x, 2) दो दशमलव रखता है।",
                "int() aur float() text ko number banate hain. round(x, 2) do decimal rakhta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Convert 37 degrees Celsius to Fahrenheit with the formula "
                "`f = c * 9 / 5 + 32`, then print `f`.",
                "37 डिग्री सेल्सियस को फ़ॉर्मूले `f = c * 9 / 5 + 32` से फ़ारेनहाइट "
                "में बदलें, फिर `f` प्रिंट करें।",
                "37 degree Celsius ko formula `f = c * 9 / 5 + 32` se Fahrenheit me "
                "badlo, phir `f` print karo.",
            ),
            "c = 37\n# f = ...\n# print(f)\n",
            "c = 37\nf = c * 9 / 5 + 32\nprint(f)",
            ["abs(f - 98.6) < 1e-9", '"98.6" in printed'],
            L("Keep the order of operations: * and / before +.", "क्रम रखें: + से पहले * और /.", "Order rakho: + se pehle * aur /."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is type(7 / 2)?", "type(7 / 2) क्या है?", "type(7 / 2) kya hai?"),
            ["int", "float", "str", "bool"],
            "b",
            L(
                "True division always returns a float, so 7 / 2 is 3.5. Use // when "
                "you want the whole-number part.",
                "सच्चा भाग हमेशा float देता है, इसलिए 7 / 2 = 3.5। पूरा भाग चाहिए तो // "
                "इस्तेमाल करें।",
                "True division hamesha float deta hai, isliye 7 / 2 = 3.5. Poora "
                "bhaag chahiye to // use karo.",
            ),
            "division-type",
        ),
        quiz(
            L('What does int("3.9") do?', 'int("3.9") क्या करता है?', 'int("3.9") kya karta hai?'),
            ["returns 3", "returns 4", "raises ValueError", "returns 3.9"],
            "c",
            L(
                "int() on text only accepts a whole-number string. Convert with "
                "float(\"3.9\") first, then int() it if you want 3.",
                "टेक्स्ट पर int() सिर्फ़ पूरा नंबर स्वीकार करता है। पहले "
                "float(\"3.9\") करें, फिर चाहें तो int() करें।",
                "Text par int() sirf poora number accept karta hai. Pehle "
                "float(\"3.9\") karo, phir chaho to int() karo.",
            ),
            "int-of-float-string",
        ),
        quiz(
            L(
                "0.1 + 0.2 == 0.3 is False. Why?",
                "0.1 + 0.2 == 0.3 False है। क्यों?",
                "0.1 + 0.2 == 0.3 False hai. Kyun?",
            ),
            [
                "Python has a bug",
                "floats store an approximation, so the last digit differs",
                "the == operator is broken",
                "0.2 is not a float",
            ],
            "b",
            L(
                "Binary floating point cannot represent 0.1 exactly, so tiny errors "
                "accumulate. Compare with round() or math.isclose() instead.",
                "बाइनरी फ़्लोटिंग पॉइंट 0.1 को ठीक-ठीक नहीं रख सकता, इसलिए छोटी "
                "गलतियाँ जुड़ जाती हैं। round() या math.isclose() से तुलना करें।",
                "Binary floating point 0.1 ko exactly nahi rakh sakta, isliye chhoti "
                "galtiyan jud jati hain. round() ya math.isclose() se compare karo.",
            ),
            "float-precision",
        ),
    ],
    takeaway=L(
        "int is whole, float has a decimal point; / gives float, // gives int.",
        "int पूरा है, float में दशमलव है; / float देता है, // int।",
        "int poora hai, float me decimal hai; / float deta hai, // int deta hai.",
    ),
)

l05 = lesson(
    "m01c02l05",
    L("Strings: text values", "स्ट्रिंग: टेक्स्ट वैल्यू", "Strings: text values"),
    [],
    L(
        "A string is text inside quotes: 'hello', \"hello\" and \"\"\"hello\"\"\" are all "
        "the same value. Strings are immutable, which means every string method "
        "returns a new string instead of changing the old one.",
        "स्ट्रिंग कोटेशन के अंदर लिखा टेक्स्ट है: 'hello', \"hello\" और "
        "\"\"\"hello\"\"\" एक ही वैल्यू हैं। स्ट्रिंग अपरिवर्तनीय (immutable) हैं, "
        "यानी हर मेथड पुरानी को बदलने की जगह नई स्ट्रिंग देता है।",
        "String quotes ke andar likha text hai: 'hello', \"hello\" aur "
        "\"\"\"hello\"\"\" ek hi value hain. Strings immutable hain, yani har method "
        "purani ko badalne ki jagah nayi string deta hai.",
    ),
    L(
        "A printed boarding pass: the name, the seat, the gate. You do not rewrite "
        "the pass to change the gate — you print a new one. String methods work the "
        "same way: `seat.replace('12A', '14C')` gives you a new string.",
        "प्रिंटेड बोर्डिंग पास: नाम, सीट, गेट। गेट बदलने के लिए आप पास पर लिखते "
        "नहीं — नया प्रिंट करते हैं। स्ट्रिंग मेथड वैसे ही काम करते हैं: "
        "`seat.replace('12A', '14C')` नई स्ट्रिंग देता है।",
        "Printed boarding pass: naam, seat, gate. Gate badalne ke liye aap pass par "
        "likhte nahi - naya print karte ho. String methods waise hi kaam karte hain: "
        "`seat.replace('12A', '14C')` nayi string deta hai.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#strings",
    examples=[
        ex(
            'name = "aarav"\nprint(name.upper())\nprint(name)\nprint(len(name))',
            "AARAV\naarav\n5",
            L("methods return a new string", "मेथड नई स्ट्रिंग देते हैं", "methods nayi string dete hain"),
            note=L(
                "name itself is still 'aarav' — upper() returned a new value that we "
                "printed but did not store.",
                "name अब भी 'aarav' है — upper() ने नई वैल्यू दी जिसे हमने प्रिंट "
                "किया पर सेव नहीं किया।",
                "name ab bhi 'aarav' hai - upper() ne nayi value di jise humne print "
                "kiya par save nahi kiya.",
            ),
        ),
        ex(
            'first = "Python"\nlast = "course"\nprint(first + " " + last)\nprint(f"{first} {last}")\nprint("-" * 20)',
            "Python course\nPython course\n--------------------",
            L("joining text", "टेक्स्ट जोड़ना", "text jodna"),
            note=L(
                "The f-string (f\"...\") is the modern way to build text from "
                "variables; {first} is replaced by its value.",
                "f-string (f\"...\") वेरिएबल से टेक्स्ट बनाने का आधुनिक तरीका है; "
                "{first} की जगह उसकी वैल्यू आती है।",
                "f-string (f\"...\") variable se text banane ka modern tarika hai; "
                "{first} ki jagah uski value aati hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Build a greeting in `greeting` that says `Hello, <name>!` using an "
                "f-string, then print it.",
                "`greeting` में f-string से `Hello, <name>!` बनाएँ, फिर प्रिंट करें।",
                "`greeting` me f-string se `Hello, <name>!` banao, phir print karo.",
            ),
            'name = "Meera"\n# greeting = ...\n# print(greeting)\n',
            'name = "Meera"\ngreeting = f"Hello, {name}!"\nprint(greeting)',
            [
                'greeting == "Hello, Meera!"',
                "greeting in printed",
            ],
            L(
                "Put the variable inside braces inside the quoted f-string.",
                "वेरिएबल को f-string के अंदर ब्रेसेस में रखें।",
                "Variable ko f-string ke andar braces me rakho.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is len('Python')?", "len('Python') क्या है?", "len('Python') kya hai?"),
            ["5", "6", "7", "an error"],
            "b",
            L(
                "len counts characters: P-y-t-h-o-n is 6. Spaces and quotes are not "
                "counted because they are not part of the value.",
                "len अक्षर गिनता है: P-y-t-h-o-n = 6. स्पेस और कोटेशन नहीं गिने जाते "
                "क्योंकि वे वैल्यू का हिस्सा नहीं हैं।",
                "len characters ginta hai: P-y-t-h-o-n = 6. Space aur quotes nahi "
                "gine jaate kyunki woh value ka hissa nahi hain.",
            ),
            "off-by-one",
        ),
        quiz(
            L(
                "After s = 'abc' and s.upper(), what is s?",
                "s = 'abc' और s.upper() के बाद s क्या है?",
                "s = 'abc' aur s.upper() ke baad s kya hai?",
            ),
            ["'ABC'", "'abc'", "an error", "None"],
            "b",
            L(
                "Strings are immutable: upper() returns 'ABC' but does not change s. "
                "You must write s = s.upper() to keep the change.",
                "स्ट्रिंग immutable हैं: upper() 'ABC' देता है पर s नहीं बदलता। बदलाव "
                "रखने के लिए s = s.upper() लिखना होगा।",
                "Strings immutable hain: upper() 'ABC' deta hai par s nahi badalta. "
                "Change rakhne ke liye s = s.upper() likhna hoga.",
            ),
            "immutability",
        ),
        quiz(
            L(
                'What does f"{2 + 3}" produce?',
                'f"{2 + 3}" क्या देता है?',
                'f"{2 + 3}" kya deta hai?',
            ),
            ['"2 + 3"', '"5"', "an error", '"23"'],
            "b",
            L(
                "Braces in an f-string hold an expression, not just a name. Any valid "
                "Python expression works inside them.",
                "f-string के ब्रेसेस में एक्सप्रेशन रख सकते हैं, सिर्फ़ नाम नहीं। अंदर "
                "कोई भी वैध पायथन एक्सप्रेशन चलता है।",
                "f-string ke braces me expression rakh sakte ho, sirf naam nahi. Andar "
                "koi bhi valid Python expression chalta hai.",
            ),
        ),
    ],
    takeaway=L(
        "Strings are immutable; methods return new strings; f-strings build text.",
        "स्ट्रिंग immutable हैं; मेथड नई स्ट्रिंग देते हैं; f-string टेक्स्ट बनाता है।",
        "Strings immutable hain; methods nayi string dete hain; f-string text banata hai.",
    ),
)

l06 = lesson(
    "m01c02l06",
    L("True, False and None", "True, False और None", "True, False aur None"),
    ["True", "False", "None"],
    L(
        "True and False are the two bool values; they are the answers to yes/no "
        "questions. None is a separate type with exactly one value, and it means "
        "\"no value here yet\" — not 0, not \"\", not False.",
        "True और False दो bool वैल्यू हैं; ये हाँ/नहीं के जवाब हैं। None अलग टाइप है "
        "जिसकी एक ही वैल्यू है, और उसका मतलब है \"अभी कोई वैल्यू नहीं\" — 0 नहीं, "
        "\"\" नहीं, False नहीं।",
        "True aur False do bool values hain; ye haan/nahi ke jawab hain. None alag "
        "type hai jiski ek hi value hai, aur uska matlab hai \"abhi koi value nahi\" "
        "- 0 nahi, \"\" nahi, False nahi.",
    ),
    L(
        "A form field you left blank is None: the question was asked and you gave "
        "nothing. That is different from answering \"no\" (False) or answering "
        "\"zero\" (0). Code that treats None as False silently loses that difference.",
        "फ़ॉर्म में खाली छोड़ा गया फ़ील्ड None है: सवाल पूछा गया और आपने कुछ नहीं दिया। "
        "यह \"नहीं\" (False) या \"शून्य\" (0) कहने से अलग है। जो कोड None को False "
        "मान लेता है, वह यह अंतर खो देता है।",
        "Form me khaali chhoda gaya field None hai: sawaal poocha gaya aur aapne kuch "
        "nahi diya. Ye \"nahi\" (False) ya \"zero\" (0) kehne se alag hai. Jo code "
        "None ko False maan leta hai, woh ye difference kho deta hai.",
    ),
    "https://docs.python.org/3/library/stdtypes.html#truth-value-testing",
    visual="types",
    examples=[
        ex(
            "print(3 > 2)\nprint(3 == 3.0)\nprint(0 == False)",
            "True\nTrue\nTrue",
            L("comparisons give bools", "तुलना bool देती है", "comparison bool deta hai"),
        ),
        ex(
            'result = None\nprint(result)\nprint(result is None)\nprint(bool(0), bool(""), bool([]), bool("0"))',
            "None\nTrue\nFalse False False True",
            L("None and truthiness", "None और सत्यता", "None aur truthiness"),
            note=L(
                "Empty things are falsy, but the text \"0\" is not empty, so it is "
                "truthy. That surprises almost everyone once.",
                "खाली चीज़ें falsy हैं, पर टेक्स्ट \"0\" खाली नहीं है, इसलिए truthy है। "
                "यह लगभग सबको एक बार चौंकाता है।",
                "Khaali cheezein falsy hain, par text \"0\" khaali nahi hai, isliye "
                "truthy hai. Ye lagbhag sabko ek baar chaukaata hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Print the result of `bool()` on four values: 0, \"\", [] and \"0\". "
                "Expected output: `False False False True`.",
                "चार वैल्यू पर `bool()` का परिणाम प्रिंट करें: 0, \"\", [] और \"0\"। "
                "अपेक्षित आउटपुट: `False False False True`।",
                "Chaar values par `bool()` ka result print karo: 0, \"\", [] aur \"0\". "
                "Expected output: `False False False True`.",
            ),
            "# one print() with four bool() calls\n",
            'print(bool(0), bool(""), bool([]), bool("0"))',
            ['printed.strip() == "False False False True"'],
            L(
                "print separates values with a space, so one call is enough.",
                "print वैल्यू को स्पेस से अलग करता है, इसलिए एक कॉल काफ़ी है।",
                "print values ko space se alag karta hai, isliye ek call kaafi hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is bool(0)?", "bool(0) क्या है?", "bool(0) kya hai?"),
            ["True", "False", "None", "0"],
            "b",
            L(
                "Zero is falsy. So are 0.0, \"\", [], {} and None. Everything else is "
                "truthy, including the string \"0\".",
                "शून्य falsy है। 0.0, \"\", [], {} और None भी। बाकी सब truthy है, "
                "स्ट्रिंग \"0\" भी।",
                "Zero falsy hai. 0.0, \"\", [], {} aur None bhi. Baaki sab truthy hai, "
                "string \"0\" bhi.",
            ),
            "truthiness",
        ),
        quiz(
            L(
                "Which check is the correct way to test for None?",
                "None जाँचने का सही तरीका कौन सा है?",
                "None check karne ka sahi tarika kaun sa hai?",
            ),
            ["x == None", "x is None", "x == False", "not x"],
            "b",
            L(
                "`is` compares identity and there is only one None object. `x == None` "
                "usually works but fails for objects with a custom __eq__, and "
                "`not x` is also true for 0 and \"\".",
                "`is` पहचान तुलना करता है और None एक ही ऑब्जेक्ट है। `x == None` आम "
                "तौर पर चलता है पर custom __eq__ वाले ऑब्जेक्ट पर फेल होता है, और "
                "`not x` 0 और \"\" के लिए भी सही है।",
                "`is` identity compare karta hai aur None ek hi object hai. "
                "`x == None` aam taur par chalta hai par custom __eq__ wale object par "
                "fail hota hai, aur `not x` 0 aur \"\" ke liye bhi true hai.",
            ),
            "is-vs-eq",
        ),
        quiz(
            L("What is type(True)?", "type(True) क्या है?", "type(True) kya hai?"),
            ["bool", "int", "str", "TrueType"],
            "a",
            L(
                "bool is its own type, but it is a subclass of int: True + True is 2. "
                "That is why isinstance(True, int) is also True.",
                "bool अपना टाइप है, पर int का सबक्लास है: True + True = 2। इसीलिए "
                "isinstance(True, int) भी True है।",
                "bool apna type hai, par int ka subclass hai: True + True = 2. Isliye "
                "isinstance(True, int) bhi True hai.",
            ),
            "bool-is-int",
        ),
    ],
    takeaway=L(
        "Empty values are falsy; None means \"no value\"; test None with `is None`.",
        "खाली वैल्यू falsy हैं; None का मतलब \"कोई वैल्यू नहीं\"; None को `is None` से जाँचें।",
        "Khaali values falsy hain; None ka matlab \"koi value nahi\"; None ko `is None` se check karo.",
    ),
)

# ------------------------------------------------------------------- module

MODULE = module(
    M,
    L("Starting Out", "शुरुआत", "Shuruaat"),
    L(
        "Run your first lines, store values in names, meet the number, text and "
        "true/false types, and learn to read an error message.",
        "अपनी पहली लाइनें चलाएँ, नामों में वैल्यू रखें, नंबर, टेक्स्ट और सही/गलत "
        "टाइप से मिलें, और एरर मैसेज पढ़ना सीखें।",
        "Apni pehli lines chalao, naamon me value rakho, number, text aur "
        "sahi/galat types se milo, aur error message padhna seekho.",
    ),
    [
        chapter(
            "m01c01",
            L("First Steps", "पहले कदम", "Pehle Kadam"),
            [l01, l02],
        ),
        chapter(
            "m01c02",
            L("Variables and Types", "वेरिएबल और टाइप", "Variable aur Types"),
            [l03, l04, l05, l06],
        ),
    ],
    exam=[
        quiz(
            L(
                "What does print('2' + '3') show?",
                "print('2' + '3') क्या दिखाता है?",
                "print('2' + '3') kya dikhata hai?",
            ),
            ["5", "23", "'23'", "an error"],
            "b",
            L(
                "Both sides are strings, so + joins them. print(2 + 3) would show 5.",
                "दोनों तरफ़ स्ट्रिंग हैं, इसलिए + जोड़ देता है। print(2 + 3) 5 दिखाता।",
                "Dono taraf string hain, isliye + jod deta hai. print(2 + 3) 5 dikhata.",
            ),
        ),
        quiz(
            L(
                "Which value is falsy?",
                "कौन सी वैल्यू falsy है?",
                "Kaun si value falsy hai?",
            ),
            ['"False"', "[0]", "0.0", '" "'],
            "c",
            L(
                "0.0 is zero. \"False\" and \" \" are non-empty strings (truthy), and "
                "[0] is a non-empty list (truthy).",
                "0.0 शून्य है। \"False\" और \" \" खाली नहीं हैं (truthy), और [0] खाली "
                "नहीं लिस्ट है (truthy)।",
                "0.0 zero hai. \"False\" aur \" \" khaali nahi hain (truthy), aur [0] "
                "khaali nahi list hai (truthy).",
            ),
        ),
        quiz(
            L(
                "What is the value of x after: x = 4; x = x * 2; x = x - 3?",
                "x = 4; x = x * 2; x = x - 3 के बाद x क्या है?",
                "x = 4; x = x * 2; x = x - 3 ke baad x kya hai?",
            ),
            ["2", "5", "8", "11"],
            "b",
            L("4 → 8 → 5. Each line uses the value the previous line left behind.", "4 → 8 → 5. हर लाइन पिछली लाइन की वैल्यू इस्तेमाल करती है।", "4 → 8 → 5. Har line pichli line ki value use karti hai."),
        ),
        quiz(
            L(
                "What does 7 // 2 give?",
                "7 // 2 क्या देता है?",
                "7 // 2 kya deta hai?",
            ),
            ["3.5", "3", "4", "1"],
            "b",
            L(
                "// is floor division: it drops the decimal part for positive "
                "numbers. 7 % 2 gives the remainder, 1.",
                "// फ़्लोर डिवीज़न है: धनात्मक नंबरों में दशमलव हटा देता है। 7 % 2 शेष "
                "देता है, 1।",
                "// floor division hai: positive numbers me decimal hata deta hai. "
                "7 % 2 remainder deta hai, 1.",
            ),
        ),
        quiz(
            L(
                "Which line prints exactly: Hello, world!",
                "कौन सी लाइन ठीक यह प्रिंट करती है: Hello, world!",
                "Kaun si line exactly ye print karti hai: Hello, world!",
            ),
            [
                'print("Hello", "world!")',
                'print("Hello, world!")',
                "print(Hello, world!)",
                'print("Hello, world!")#',
            ],
            "b",
            L(
                "Option a inserts a space and no comma. Option c treats the words as "
                "variables. Option d is a syntax error because # starts a comment "
                "inside the call.",
                "विकल्प a स्पेस डालता है और कॉमा नहीं। विकल्प c शब्दों को वेरिएबल "
                "मानता है। विकल्प d सिंटैक्स एरर है क्योंकि # कॉल के अंदर कमेंट "
                "शुरू कर देता है।",
                "Option a space daalta hai aur comma nahi. Option c words ko variable "
                "maanta hai. Option d syntax error hai kyunki # call ke andar comment "
                "shuru kar deta hai.",
            ),
        ),
        quiz(
            L(
                "s = 'Data'; s.lower(); print(s). What is printed?",
                "s = 'Data'; s.lower(); print(s)। क्या प्रिंट होगा?",
                "s = 'Data'; s.lower(); print(s). Kya print hoga?",
            ),
            ["data", "Data", "DATA", "an error"],
            "b",
            L(
                "The result of lower() was thrown away because it was not assigned. "
                "Strings cannot change in place.",
                "lower() का परिणाम फेंक दिया गया क्योंकि उसे सेव नहीं किया। स्ट्रिंग "
                "जगह पर नहीं बदलती।",
                "lower() ka result phenk diya gaya kyunki use save nahi kiya. String "
                "jagah par nahi badalti.",
            ),
        ),
    ],
    icon="🚀",
)
