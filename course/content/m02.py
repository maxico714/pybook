"""Module 2 - Working with Data: slicing, text methods, operators, numbers."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m02"

l01 = lesson(
    "m02c01l01",
    L("Indexing and slicing", "इंडेक्सिंग और स्लाइसिंग", "Indexing aur slicing"),
    [],
    L(
        "Every sequence (string, list, tuple) is numbered from 0. square brackets "
        "pick one item by number, and a slice with a colon picks a range.",
        "हर सीक्वेंस (स्ट्रिंग, लिस्ट, ट्यूपल) 0 से गिना जाता है। स्क्वायर ब्रैकेट "
        "नंबर से एक आइटम चुनते हैं, और कोलन वाला स्लाइस एक रेंज चुनता है।",
        "Har sequence (string, list, tuple) 0 se gina jata hai. Square bracket "
        "number se ek item chunte hain, aur colon wala slice ek range chunta hai.",
    ),
    L(
        "A train has numbered coaches and you have a seat 3C. `train[3]` is coach 3. "
        "A reservation for coaches 3 to 5 is a slice: `train[3:6]` — note that the "
        "stop number is the one *after* the last coach you want.",
        "ट्रेन में डिब्बे नंबर पर होते हैं और आपकी सीट 3C है। `train[3]` डिब्बा 3 है। "
        "डिब्बा 3 से 5 तक की बुकिंग स्लाइस है: `train[3:6]` — ध्यान दें कि रुकने "
        "वाला नंबर आख़िरी डिब्बे के *बाद* वाला है।",
        "Train me coaches number par hote hain aur aapki seat 3C hai. `train[3]` "
        "coach 3 hai. Coach 3 se 5 tak ki booking slice hai: `train[3:6]` - dhyan do "
        "ki rukne wala number aakhri coach ke *baad* wala hai.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#strings",
    visual="list_index",
    examples=[
        ex(
            'word = "Python"\nprint(word[0], word[-1])\nprint(word[1:4])\nprint(word[:3], word[3:])\nprint(word[::2])',
            "P n\nyth\nPyt hon\nPto",
            L("one item versus a slice", "एक आइटम बनाम स्लाइस", "ek item versus slice"),
            note=L(
                "-1 is the last item; a negative step walks backwards.",
                "-1 आख़िरी आइटम है; नेगेटिव स्टेप पीछे की ओर चलता है।",
                "-1 aakhri item hai; negative step peeche ki taraf chalta hai.",
            ),
        ),
        ex(
            "nums = [10, 20, 30, 40, 50]\nprint(nums[1:3])\nprint(nums[::-1])\nprint(len(nums))",
            "[20, 30]\n[50, 40, 30, 20, 10]\n5",
            L("slicing a list", "लिस्ट स्लाइस करना", "list slice karna"),
        ),
    ],
    exercises=[
        task(
            L(
                "From `text = 'programming'`, print the first 7 characters, then the "
                "last 3.",
                "`text = 'programming'` से पहले 7 अक्षर प्रिंट करें, फिर आख़िरी 3।",
                "`text = 'programming'` se pehle 7 characters print karo, phir aakhri 3.",
            ),
            "text = 'programming'\n# print(...)\n# print(...)\n",
            "text = 'programming'\nprint(text[:7])\nprint(text[-3:])",
            ['"program" in printed', '"ing" in printed'],
            L("[:7] means from the start up to 7.", "[:7] का मतलब शुरू से 7 तक।", "[:7] matlab shuru se 7 tak."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What is 'Python'[1:3]?",
                "'Python'[1:3] क्या है?",
                "'Python'[1:3] kya hai?",
            ),
            ["'yt'", "'yth'", "'y'", "'Pyt'"],
            "a",
            L(
                "Start at index 1 ('y') and stop before index 3, so only 1 and 2 are "
                "included.",
                "इंडेक्स 1 ('y') से शुरू और 3 से पहले रुको, इसलिए सिर्फ़ 1 और 2 शामिल हैं।",
                "Index 1 ('y') se shuru aur 3 se pehle ruk, isliye sirf 1 aur 2 include hain.",
            ),
            "slice-exclusive-end",
        ),
        quiz(
            L(
                "What is [1, 2, 3][-1]?",
                "[1, 2, 3][-1] क्या है?",
                "[1, 2, 3][-1] kya hai?",
            ),
            ["1", "3", "an error", "[3]"],
            "b",
            L(
                "Negative indexes count from the end, so -1 is the last item. An "
                "IndexError only happens when the number is too large in either "
                "direction.",
                "नेगेटिव इंडेक्स अंत से गिनते हैं, इसलिए -1 आख़िरी आइटम है। IndexError "
                "तभी आता है जब नंबर दोनों दिशाओं में बहुत बड़ा हो।",
                "Negative index end se ginte hain, isliye -1 aakhri item hai. "
                "IndexError tabhi aata hai jab number dono directions me bahut bada ho.",
            ),
        ),
        quiz(
            L(
                "Why does 'abc'[0:10] not raise an error?",
                "'abc'[0:10] एरर क्यों नहीं देता?",
                "'abc'[0:10] error kyun nahi deta?",
            ),
            [
                "because slicing clamps to the length",
                "because 10 is a float",
                "because strings are immutable",
                "it does raise an error",
            ],
            "a",
            L(
                "A slice never fails for an out-of-range number: it just stops at the "
                "end. Indexing with [10] would raise IndexError.",
                "स्लाइस रेंज से बाहर के नंबर पर कभी फेल नहीं होता: वह अंत पर रुक जाता "
                "है। [10] से इंडेक्स करने पर IndexError आता।",
                "Slice range se bahar ke number par kabhi fail nahi hota: woh end par "
                "ruk jata hai. [10] se index karne par IndexError aata.",
            ),
        ),
    ],
    takeaway=L(
        "Indexes start at 0; slices stop before the end number; -1 is the last item.",
        "इंडेक्स 0 से शुरू; स्लाइस अंत वाले नंबर से पहले रुकता है; -1 आख़िरी आइटम।",
        "Index 0 se shuru; slice end number se pehle rukta hai; -1 aakhri item.",
    ),
)

l02 = lesson(
    "m02c01l02",
    L("String methods and f-strings", "स्ट्रिंग मेथड और f-string", "String methods aur f-strings"),
    [],
    L(
        "Strings come with ready-made methods: strip, lower, replace, split, join, "
        "startswith and many more. f-strings are the modern way to put values "
        "inside text.",
        "स्ट्रिंग के साथ तैयार मेथड आते हैं: strip, lower, replace, split, join, "
        "startswith और भी। f-string वैल्यू को टेक्स्ट के अंदर डालने का आधुनिक तरीका है।",
        "Strings ke saath ready-made methods aate hain: strip, lower, replace, split, "
        "join, startswith aur bhi. f-string value ko text ke andar daalne ka modern "
        "tarika hai.",
    ),
    L(
        "Cleaning up a form: people type \"  ASHA  \" or \"asha\". One strip() and one "
        "lower() turn both into a single consistent \"asha\" you can compare.",
        "फ़ॉर्म साफ़ करना: लोग \"  ASHA  \" या \"asha\" टाइप करते हैं। एक strip() और "
        "एक lower() दोनों को एक जैसा \"asha\" बना देते हैं जिसकी तुलना हो सके।",
        "Form saaf karna: log \"  ASHA  \" ya \"asha\" type karte hain. Ek strip() "
        "aur ek lower() dono ko ek jaisa \"asha\" bana dete hain jiski compare ho sake.",
    ),
    "https://docs.python.org/3/library/stdtypes.html#string-methods",
    examples=[
        ex(
            'text = "  Hello World  "\nprint(text.strip())\nprint(text.strip().lower())\nprint(text.strip().replace("World", "Python"))\nprint("a,b,c".split(","))\nprint("-".join(["a", "b", "c"]))',
            "Hello World\nhello world\nHello Python\n['a', 'b', 'c']\na-b-c",
            L("the five you will use daily", "रोज़ काम आने वाले पाँच", "roz kaam aane wale paanch"),
            note=L(
                "Methods chain left to right: strip() first, then lower() on its result.",
                "मेथड बाएँ से दाएँ जुड़ते हैं: पहले strip(), फिर उसके परिणाम पर lower()।",
                "Methods left se right judte hain: pehle strip(), phir uske result par lower().",
            ),
        ),
        ex(
            'name = "Asha"\nscore = 91.5\nprint(f"{name} scored {score}")\nprint(f"{score:.1f}")\nprint(f"{name!r}")',
            "Asha scored 91.5\n91.5\n'Asha'",
            L("f-string formatting", "f-string फ़ॉर्मेटिंग", "f-string formatting"),
            note=L(
                ":.1f means one decimal place; !r means show the repr, which adds quotes.",
                ":.1f का मतलब एक दशमलव; !r का मतलब repr दिखाओ, जिससे कोटेशन जुड़ते हैं।",
                ":.1f matlab ek decimal; !r matlab repr dikhao, jisse quotes judte hain.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Given `raw = '  Ravi KUMAR  '`, produce `clean` = 'Ravi Kumar' "
                "(no spaces at the ends, first letters capitalised) and print it.",
                "`raw = '  Ravi KUMAR  '` से `clean` = 'Ravi Kumar' बनाएँ (किनारों पर "
                "स्पेस नहीं, पहले अक्षर बड़े) और प्रिंट करें।",
                "`raw = '  Ravi KUMAR  '` se `clean` = 'Ravi Kumar' banao (kinaaron "
                "par space nahi, pehle letters bade) aur print karo.",
            ),
            "raw = '  Ravi KUMAR  '\n# clean = ...\n# print(clean)\n",
            "raw = '  Ravi KUMAR  '\nclean = raw.strip().title()\nprint(clean)",
            ['clean == "Ravi Kumar"', "clean in printed"],
            L("strip() then title().", "पहले strip() फिर title()।", "Pehle strip() phir title()."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is 'a-b-c'.split('-')?", "'a-b-c'.split('-') क्या है?", "'a-b-c'.split('-') kya hai?"),
            ["['a', 'b', 'c']", "'abc'", "['a-b-c']", "('a', 'b', 'c')"],
            "a",
            L(
                "split returns a list of the pieces between the separator. join is "
                "the opposite operation.",
                "split सेपरेटर के बीच के टुकड़ों की लिस्ट देता है। join उल्टा काम करता है।",
                "split separator ke beech ke tukdon ki list deta hai. join ulta kaam karta hai.",
            ),
        ),
        quiz(
            L(
                "s = '  hi  '; s.strip(); print(s). What prints?",
                "s = '  hi  '; s.strip(); print(s)। क्या प्रिंट होगा?",
                "s = '  hi  '; s.strip(); print(s). Kya print hoga?",
            ),
            ["hi", "'  hi  '", "an error", "None"],
            "b",
            L(
                "strip() returned a new string that was never stored. Write "
                "s = s.strip() to keep it.",
                "strip() ने नई स्ट्रिंग दी जो कहीं रखी नहीं गई। रखने के लिए "
                "s = s.strip() लिखें।",
                "strip() ne nayi string di jo kahin rakhi nahi gayi. Rakhne ke liye "
                "s = s.strip() likho.",
            ),
            "immutability",
        ),
        quiz(
            L(
                'What does f"{3 * 4}" produce?',
                'f"{3 * 4}" क्या देता है?',
                'f"{3 * 4}" kya deta hai?',
            ),
            ["'3 * 4'", "'12'", "12", "an error"],
            "b",
            L(
                "The result of an f-string is always a string, so the answer has "
                "quotes in it. Without the f it would be the literal text 3 * 4.",
                "f-string का परिणाम हमेशा स्ट्रिंग होता है, इसलिए जवाब में कोटेशन हैं। "
                "f के बिना वह 3 * 4 टेक्स्ट ही रहता।",
                "f-string ka result hamesha string hota hai, isliye answer me quotes "
                "hain. f ke bina woh 3 * 4 text hi rehta.",
            ),
        ),
    ],
    takeaway=L(
        "Methods return new strings; chain them; f-strings build text with values.",
        "मेथड नई स्ट्रिंग देते हैं; उन्हें जोड़ें; f-string वैल्यू से टेक्स्ट बनाता है।",
        "Methods nayi string dete hain; unhe chain karo; f-string value se text banata hai.",
    ),
)

l03 = lesson(
    "m02c02l03",
    L("Comparison and logical operators", "तुलना और लॉजिकल ऑपरेटर", "Comparison aur logical operators"),
    ["and", "or", "not", "in"],
    L(
        "Comparison operators (==, !=, <, <=, >, >=) answer with True or False. "
        "and, or and not combine those answers into one. Python also allows "
        "chained comparisons like 1 < x < 10.",
        "तुलना ऑपरेटर (==, !=, <, <=, >, >=) True या False देते हैं। and, or और "
        "not उन जवाबों को एक में जोड़ते हैं। पायथन 1 < x < 10 जैसी चेन तुलना भी "
        "देता है।",
        "Comparison operators (==, !=, <, <=, >, >=) True ya False dete hain. and, "
        "or aur not un jawabon ko ek me jodte hain. Python 1 < x < 10 jaisi chained "
        "comparison bhi deta hai.",
    ),
    L(
        "A ticket counter rule: \"age at least 18 AND a valid ID\". Both must be "
        "true. A discount rule: \"student OR senior citizen\". Either one is enough.",
        "टिकट काउंटर का नियम: \"उम्र कम से कम 18 और वैध आईडी\"। दोनों सही होने "
        "चाहिए। छूट का नियम: \"छात्र या वरिष्ठ नागरिक\"। एक भी काफ़ी है।",
        "Ticket counter ka rule: \"age kam se kam 18 AND valid ID\". Dono sahi hone "
        "chahiye. Discount ka rule: \"student OR senior citizen\". Ek bhi kaafi hai.",
    ),
    "https://docs.python.org/3/reference/expressions.html#comparisons",
    examples=[
        ex(
            "age = 20\nprint(age >= 18 and age < 60)\nprint(not age == 20)\nprint(1 < age < 100)\nprint(\"a\" in \"cat\", 3 in [1, 2, 3])",
            "True\nFalse\nTrue\nTrue True",
            L("combining conditions", "शर्तें जोड़ना", "conditions jodna"),
        ),
        ex(
            'print(True and "yes")\nprint(False and "yes")\nprint(False or "backup")\nprint(0 or 5)',
            "yes\nFalse\nbackup\n5",
            L("and/or return a value, not just True/False", "and/or वैल्यू देते हैं, सिर्फ़ True/False नहीं", "and/or value dete hain, sirf True/False nahi"),
            note=L(
                "and stops at the first falsy value; or stops at the first truthy "
                "one. That is why `name or \"guest\"` is a common default.",
                "and पहली falsy वैल्यू पर रुकता है; or पहली truthy पर। इसीलिए "
                "`name or \"guest\"` आम डिफ़ॉल्ट है।",
                "and pehli falsy value par rukta hai; or pehli truthy par. Isliye "
                "`name or \"guest\"` aam default hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Set `can_vote` to the result of: age is at least 18 AND country is "
                "'India'. Print it. Use age = 21, country = 'India'.",
                "`can_vote` में यह परिणाम रखें: उम्र कम से कम 18 AND देश 'India'। "
                "प्रिंट करें। age = 21, country = 'India' लें।",
                "`can_vote` me ye result rakho: age kam se kam 18 AND country "
                "'India'. Print karo. age = 21, country = 'India' lo.",
            ),
            "age = 21\ncountry = 'India'\n# can_vote = ...\n# print(can_vote)\n",
            "age = 21\ncountry = 'India'\ncan_vote = age >= 18 and country == 'India'\nprint(can_vote)",
            ["can_vote is True", '"True" in printed'],
            L("Use == to compare text, not =.", "टेक्स्ट तुलना के लिए ==, = नहीं।", "Text compare ke liye ==, = nahi."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is 1 < 5 < 3?", "1 < 5 < 3 क्या है?", "1 < 5 < 3 kya hai?"),
            ["True", "False", "an error", "5"],
            "b",
            L(
                "It means (1 < 5) and (5 < 3). The first is true, the second is "
                "false, so the whole chain is False.",
                "इसका मतलब (1 < 5) and (5 < 3)। पहला सही, दूसरा गलत, इसलिए पूरी चेन "
                "False है।",
                "Iska matlab (1 < 5) and (5 < 3). Pehla true, doosra false, isliye "
                "poori chain False hai.",
            ),
            "chained-comparison",
        ),
        quiz(
            L("What is bool('0' == 0)?", "bool('0' == 0) क्या है?", "bool('0' == 0) kya hai?"),
            ["True", "False", "an error", "0"],
            "b",
            L(
                "The text '0' and the number 0 are different values, so == is False. "
                "Python does not convert between str and int for you.",
                "टेक्स्ट '0' और नंबर 0 अलग वैल्यू हैं, इसलिए == False है। पायथन "
                "str और int को अपने आप नहीं बदलता।",
                "Text '0' aur number 0 alag values hain, isliye == False hai. Python "
                "str aur int ko apne aap nahi badalta.",
            ),
            "str-vs-int",
        ),
        quiz(
            L("What is 0 or 'fallback'?", "0 or 'fallback' क्या है?", "0 or 'fallback' kya hai?"),
            ["0", "'fallback'", "True", "an error"],
            "b",
            L(
                "0 is falsy, so `or` moves on and returns the second operand. "
                "`or` returns a value, not a bool.",
                "0 falsy है, इसलिए `or` आगे बढ़कर दूसरा ऑपरेंड देता है। `or` वैल्यू "
                "देता है, bool नहीं।",
                "0 falsy hai, isliye `or` aage badhkar doosra operand deta hai. `or` "
                "value deta hai, bool nahi.",
            ),
        ),
    ],
    takeaway=L(
        "and/or return an operand, not only True/False; chained comparisons work.",
        "and/or ऑपरेंड देते हैं, सिर्फ़ True/False नहीं; चेन तुलना चलती है।",
        "and/or operand dete hain, sirf True/False nahi; chained comparison chalti hai.",
    ),
)

l04 = lesson(
    "m02c02l04",
    L("is, == and del", "is, == और del", "is, == aur del"),
    ["is", "del"],
    L(
        "== asks \"are these two values equal?\". is asks \"are these the same object "
        "in memory?\". del removes a name or an item; it does not destroy the value "
        "while another name still points at it.",
        "== पूछता है \"क्या ये दो वैल्यू बराबर हैं?\"। is पूछता है \"क्या ये मेमोरी में "
        "एक ही ऑब्जेक्ट हैं?\"। del नाम या आइटम हटाता है; जब तक दूसरा नाम उस वैल्यू "
        "को दिखा रहा है, वह वैल्यू ख़त्म नहीं होती।",
        "== poochhta hai \"kya ye do values barabar hain?\". is poochhta hai \"kya ye "
        "memory me ek hi object hain?\". del naam ya item hataata hai; jab tak doosra "
        "naam us value ko point kar raha hai, woh value khatam nahi hoti.",
    ),
    L(
        "Two people can have identical ID copies (==) but they are still two "
        "different people (is). And deleting a contact from your phone does not "
        "delete the person — that is del on a name.",
        "दो लोगों के पास एक जैसी आईडी कॉपी हो सकती है (==) पर वे दो अलग लोग हैं (is)। "
        "और फ़ोन से कॉन्टैक्ट हटाने से व्यक्ति नहीं मिटता — वही नाम पर del है।",
        "Do logon ke paas ek jaisi ID copy ho sakti hai (==) par woh do alag log hain "
        "(is). Aur phone se contact hatane se insaan nahi mitta - wahi naam par del hai.",
    ),
    "https://docs.python.org/3/reference/expressions.html#is",
    visual="alias_copy",
    examples=[
        ex(
            "a = [1, 2]\nb = [1, 2]\nc = a\nprint(a == b, a is b)\nprint(a is c)\nprint(id(a) == id(c))",
            "True False\nTrue\nTrue",
            L("equal values, different objects", "बराबर वैल्यू, अलग ऑब्जेक्ट", "barabar values, alag objects"),
            note=L(
                "id() prints the memory address. Two separate lists get two addresses.",
                "id() मेमोरी पता दिखाता है। दो अलग लिस्ट को दो पते मिलते हैं।",
                "id() memory address dikhata hai. Do alag lists ko do addresses milte hain.",
            ),
        ),
        ex(
            'nums = [1, 2, 3, 4]\ndel nums[0]\nprint(nums)\nperson = {"a": 1, "b": 2}\ndel person["a"]\nprint(person)\ntemp = 99\ndel temp',
            "[2, 3, 4]\n{'b': 2}",
            L("del removes an item or a name", "del आइटम या नाम हटाता है", "del item ya naam hataata hai"),
            note=L(
                "del nums[0] removes by index; del person[\"a\"] removes by key. "
                "del temp removes the name itself.",
                "del nums[0] इंडेक्स से हटाता है; del person[\"a\"] की से हटाता है। "
                "del temp नाम ही हटा देता है।",
                "del nums[0] index se hataata hai; del person[\"a\"] key se hataata "
                "hai. del temp naam hi hata deta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Make `same` True only when x and y are the same object. Use x = [1]; "
                "y = x.",
                "`same` तभी True हो जब x और y एक ही ऑब्जेक्ट हों। x = [1]; y = x लें।",
                "`same` tabhi True ho jab x aur y ek hi object hon. x = [1]; y = x lo.",
            ),
            "x = [1]\ny = x\n# same = ...\n# print(same)\n",
            "x = [1]\ny = x\nsame = x is y\nprint(same)",
            ["same is True", '"True" in printed'],
            L("Identity uses the `is` keyword.", "पहचान के लिए `is` कीवर्ड।", "Identity ke liye `is` keyword."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "a = [1]; b = [1]. What is a is b?",
                "a = [1]; b = [1]. a is b क्या है?",
                "a = [1]; b = [1]. a is b kya hai?",
            ),
            ["True", "False", "an error", "1"],
            "b",
            L(
                "Two list literals create two objects. They are == (equal) but not "
                "`is` (identical).",
                "दो लिस्ट लिटरल दो ऑब्जेक्ट बनाते हैं। वे == हैं (बराबर) पर `is` "
                "नहीं (एक जैसे नहीं)।",
                "Do list literals do objects banate hain. Woh == hain (barabar) par "
                "`is` nahi (identical nahi).",
            ),
            "is-vs-eq",
        ),
        quiz(
            L(
                "Which is the recommended None check?",
                "None की सही जाँच कौन सी है?",
                "None ki sahi check kaun si hai?",
            ),
            ["x is None", "x == None", "x is not 0", "x == 'None'"],
            "a",
            L(
                "None is a single object, so identity is both correct and faster. "
                "The linter warning 'comparison to None should be is' points at this.",
                "None एक ही ऑब्जेक्ट है, इसलिए identity सही भी है और तेज़ भी। लिंटर "
                "की चेतावनी 'comparison to None should be is' यही कहती है।",
                "None ek hi object hai, isliye identity sahi bhi hai aur fast bhi. "
                "Linter ki warning 'comparison to None should be is' yahi kehti hai.",
            ),
            "is-vs-eq",
        ),
        quiz(
            L(
                "After a = [1, 2]; b = a; del a, what is b?",
                "a = [1, 2]; b = a; del a के बाद b क्या है?",
                "a = [1, 2]; b = a; del a ke baad b kya hai?",
            ),
            ["[1, 2]", "an error, because the list was deleted", "None", "[]"],
            "a",
            L(
                "del removes the name a. The list still has b pointing at it, so it "
                "stays alive.",
                "del नाम a हटाता है। लिस्ट को b दिखा रहा है, इसलिए वह ज़िंदा रहती है।",
                "del naam a hataata hai. List ko b point kar raha hai, isliye woh zinda rehti hai.",
            ),
            "del-vs-destroy",
        ),
    ],
    takeaway=L(
        "== compares values, is compares identity; del drops a name or an item.",
        "== वैल्यू तुलना करता है, is पहचान; del नाम या आइटम हटाता है।",
        "== value compare karta hai, is identity; del naam ya item hataata hai.",
    ),
)

l05 = lesson(
    "m02c03l05",
    L("Division, modulo and precision", "भाग, मॉड्यूलो और परिशुद्धता", "Division, modulo aur precision"),
    [],
    L(
        "Python has three division tools: / gives a float, // gives the floor "
        "(rounded down), and % gives the remainder. Floats are binary "
        "approximations, so 0.1 + 0.2 is not exactly 0.3.",
        "पायथन में भाग के तीन औज़ार हैं: / float देता है, // फ़्लोर (नीचे की ओर) देता "
        "है, और % शेष देता है। float बाइनरी अनुमान हैं, इसलिए 0.1 + 0.2 ठीक 0.3 "
        "नहीं है।",
        "Python me division ke teen tools hain: / float deta hai, // floor (neeche ki "
        "taraf) deta hai, aur % remainder deta hai. Floats binary approximation "
        "hain, isliye 0.1 + 0.2 exactly 0.3 nahi hai.",
    ),
    L(
        "Splitting a bill of ₹100 among 3 people: // tells you each pays ₹33 and % "
        "tells you ₹1 is left over. That leftover rupee is exactly what the modulo "
        "operator is for.",
        "₹100 का बिल 3 लोगों में बाँटना: // बताता है हर कोई ₹33 देगा और % बताता है "
        "₹1 बचता है। वही बचा रुपया मॉड्यूलो ऑपरेटर का काम है।",
        "₹100 ka bill 3 logon me baantna: // batata hai har koi ₹33 dega aur % "
        "batata hai ₹1 bachta hai. Wahi bacha rupaya modulo operator ka kaam hai.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#numbers",
    examples=[
        ex(
            "print(7 / 2, 7 // 2, 7 % 2)\nprint(-7 // 2, -7 % 2)\nprint(2 ** 10, 2 ** 0.5)\nprint(divmod(17, 5))",
            "3.5 3 1\n-4 1\n1024 1.4142135623730951\n(3, 2)",
            L("the four arithmetic tools", "चार अंकगणितीय औज़ार", "chaar arithmetic tools"),
            note=L(
                "// rounds towards minus infinity, so -7 // 2 is -4, not -3. divmod "
                "returns (quotient, remainder) in one call.",
                "// ऋणात्मक अनंत की ओर राउंड करता है, इसलिए -7 // 2 = -4, -3 नहीं। "
                "divmod एक कॉल में (भागफल, शेष) देता है।",
                "// minus infinity ki taraf round karta hai, isliye -7 // 2 = -4, -3 "
                "nahi. divmod ek call me (quotient, remainder) deta hai.",
            ),
        ),
        ex(
            'print(0.1 + 0.2)\nprint(round(0.1 + 0.2, 2))\nprint(f"{1 / 3:.3f}")\nimport math\nprint(math.isclose(0.1 + 0.2, 0.3))',
            "0.30000000000000004\n0.3\n0.333\nTrue",
            L("living with float precision", "float परिशुद्धता के साथ", "float precision ke saath"),
            note=L(
                "Never compare money with ==. Use round() for display and "
                "math.isclose() for checks, or store paise as int.",
                "पैसे की == से तुलना कभी न करें। दिखाने के लिए round() और जाँच के लिए "
                "math.isclose(), या पैसे int में रखें।",
                "Paise ki == se compare kabhi na karo. Dikhane ke liye round() aur "
                "check ke liye math.isclose(), ya paise int me rakho.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "100 rupees split among 3: print the share per person (//) and the "
                "leftover (%).",
                "100 रुपये 3 लोगों में: प्रति व्यक्ति हिस्सा (//) और बचा हुआ (%) प्रिंट करें।",
                "100 rupees 3 logon me: per person share (//) aur bacha hua (%) print karo.",
            ),
            "# print(100 // 3, 100 % 3)\n",
            "print(100 // 3, 100 % 3)",
            ['printed.strip() == "33 1"'],
            L("Both operators on the same numbers.", "एक ही नंबरों पर दोनों ऑपरेटर।", "Ek hi numbers par dono operators."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is -7 // 2?", "-7 // 2 क्या है?", "-7 // 2 kya hai?"),
            ["-3", "-4", "-3.5", "3"],
            "b",
            L(
                "Floor division always rounds down, and -3.5 rounds down to -4. This "
                "is the single most surprising result in beginner arithmetic.",
                "फ़्लोर डिवीज़न हमेशा नीचे राउंड करता है, और -3.5 नीचे -4 बनता है। "
                "शुरुआती अंकगणित में यह सबसे चौंकाने वाला परिणाम है।",
                "Floor division hamesha neeche round karta hai, aur -3.5 neeche -4 "
                "banta hai. Beginner arithmetic me ye sabse chaukaane wala result hai.",
            ),
            "floor-division-negative",
        ),
        quiz(
            L("What is 17 % 5?", "17 % 5 क्या है?", "17 % 5 kya hai?"),
            ["3", "2", "3.4", "12"],
            "b",
            L(
                "17 = 5*3 + 2, so the remainder is 2. % is often used to test even/odd "
                "(n % 2 == 0) or to wrap around a range.",
                "17 = 5*3 + 2, इसलिए शेष 2 है। % अक्सर सम/विषम जाँचने (n % 2 == 0) या "
                "रेंज में घुमाने के लिए इस्तेमाल होता है।",
                "17 = 5*3 + 2, isliye remainder 2 hai. % aksar even/odd check karne "
                "(n % 2 == 0) ya range me ghumane ke liye use hota hai.",
            ),
        ),
        quiz(
            L(
                "Why is 0.1 + 0.2 != 0.3?",
                "0.1 + 0.2 != 0.3 क्यों है?",
                "0.1 + 0.2 != 0.3 kyun hai?",
            ),
            [
                "float stores a binary approximation of 0.1",
                "Python adds a hidden 0.00000000000000004",
                "== is unreliable for all numbers",
                "0.2 is stored as a string",
            ],
            "a",
            L(
                "There is no bug and no hidden number: 0.1 has no exact binary "
                "representation, so the sum lands one bit away from 0.3.",
                "कोई बग नहीं और कोई छिपा नंबर नहीं: 0.1 का ठीक बाइनरी रूप नहीं है, "
                "इसलिए जोड़ 0.3 से एक बिट दूर पड़ता है।",
                "Koi bug nahi aur koi chhupa number nahi: 0.1 ka exact binary roop "
                "nahi hai, isliye sum 0.3 se ek bit door padta hai.",
            ),
            "float-precision",
        ),
    ],
    takeaway=L(
        "/ float, // floor, % remainder; never compare money with ==.",
        "/ float, // floor, % शेष; पैसे की == से तुलना कभी नहीं।",
        "/ float, // floor, % remainder; paise ki == se compare kabhi nahi.",
    ),
)

MODULE = module(
    M,
    L("Working with Data", "डेटा के साथ काम", "Data ke saath kaam"),
    L(
        "Cut text and lists into pieces, clean text up, combine conditions, tell "
        "identity apart from equality, and handle division correctly.",
        "टेक्स्ट और लिस्ट के टुकड़े करें, टेक्स्ट साफ़ करें, शर्तें जोड़ें, पहचान "
        "और बराबरी में फ़र्क करें, और भाग सही संभालें।",
        "Text aur lists ke tukde karo, text saaf karo, conditions jodo, identity aur "
        "equality me farq karo, aur division sahi sambhalo.",
    ),
    [
        chapter("m02c01", L("Text in depth", "टेक्स्ट विस्तार से", "Text vistar se"), [l01, l02]),
        chapter("m02c02", L("Operators and identity", "ऑपरेटर और पहचान", "Operators aur identity"), [l03, l04]),
        chapter("m02c03", L("Numbers in practice", "नंबर व्यवहार में", "Numbers practice me"), [l05]),
    ],
    exam=[
        quiz(
            L("What is 'hello'[1:3]?", "'hello'[1:3] क्या है?", "'hello'[1:3] kya hai?"),
            ["'el'", "'ell'", "'e'", "'he'"],
            "a",
            L("Index 1 is 'e', index 2 is 'l', and index 3 is excluded.", "इंडेक्स 1 'e', इंडेक्स 2 'l', और इंडेक्स 3 शामिल नहीं।", "Index 1 'e', index 2 'l', aur index 3 include nahi."),
        ),
        quiz(
            L("What is len([1, 2, 3][1:])?", "len([1, 2, 3][1:]) क्या है?", "len([1, 2, 3][1:]) kya hai?"),
            ["1", "2", "3", "an error"],
            "b",
            L("The slice drops index 0, leaving [2, 3], which has two items.", "स्लाइस इंडेक्स 0 हटाता है, [2, 3] बचता है, जिसमें दो आइटम हैं।", "Slice index 0 hataata hai, [2, 3] bachta hai, jisme do items hain."),
        ),
        quiz(
            L("What does ' x '.strip() return?", "' x '.strip() क्या लौटाता है?", "' x '.strip() kya return karta hai?"),
            ["' x '", "'x'", "'x '", "an error"],
            "b",
            L("strip() removes whitespace from both ends, including spaces and newlines.", "strip() दोनों किनारों से व्हाइटस्पेस हटाता है, स्पेस और न्यूलाइन दोनों।", "strip() dono kinaaron se whitespace hataata hai, space aur newline dono."),
        ),
        quiz(
            L("What is bool([])?", "bool([]) क्या है?", "bool([]) kya hai?"),
            ["True", "False", "None", "an error"],
            "b",
            L("An empty list is falsy. So are {}, '', 0 and None.", "खाली लिस्ट falsy है। {}, '', 0 और None भी।", "Khaali list falsy hai. {}, '', 0 aur None bhi."),
        ),
        quiz(
            L("a = (1, 2); b = (1, 2). What is a is b?", "a = (1, 2); b = (1, 2). a is b क्या है?", "a = (1, 2); b = (1, 2). a is b kya hai?"),
            ["True", "False", "an error", "depends on the Python version"],
            "b",
            L(
                "Two tuple literals are two objects; equality is True but identity is "
                "False. Small ints are the special case where `is` can be True by caching.",
                "दो ट्यूपल लिटरल दो ऑब्जेक्ट हैं; बराबरी True पर पहचान False। छोटे "
                "int ख़ास केस हैं जहाँ कैशिंग से `is` True हो सकता है।",
                "Do tuple literals do objects hain; equality True par identity False. "
                "Chhote int special case hain jahan caching se `is` True ho sakta hai.",
            ),
        ),
        quiz(
            L("What is divmod(9, 4)?", "divmod(9, 4) क्या है?", "divmod(9, 4) kya hai?"),
            ["(2, 1)", "(1, 2)", "2.25", "(2.25, 0)"],
            "a",
            L("divmod returns (quotient, remainder) as a tuple: 9 // 4 = 2 and 9 % 4 = 1.", "divmod (भागफल, शेष) ट्यूपल देता है: 9 // 4 = 2 और 9 % 4 = 1।", "divmod (quotient, remainder) tuple deta hai: 9 // 4 = 2 aur 9 % 4 = 1."),
        ),
    ],
    icon="🧩",
)
