"""Module 4 - Collections: lists, tuples, dicts, sets."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m04"

l01 = lesson(
    "m04c01l01",
    L("Lists and mutability", "लिस्ट और परिवर्तनशीलता", "Lists aur mutability"),
    [],
    L(
        "A list holds many values in order and you can change it: add, remove, "
        "replace. That is what mutable means. Two names can point at the same list, "
        "so changing it through one name is visible through the other.",
        "लिस्ट क्रम में कई वैल्यू रखती है और आप उसे बदल सकते हैं: जोड़ना, हटाना, "
        "बदलना। इसे mutable कहते हैं। दो नाम एक ही लिस्ट को दिखा सकते हैं, इसलिए "
        "एक नाम से बदलाव दूसरे से भी दिखता है।",
        "List order me kai values rakhti hai aur aap use badal sakte ho: jodna, "
        "hatana, badalna. Ise mutable kehte hain. Do naam ek hi list ko point kar "
        "sakte hain, isliye ek naam se change doosre se bhi dikhta hai.",
    ),
    L(
        "A shared shopping list on the fridge. If you add \"milk\" with a pen, your "
        "brother sees milk too — there is only one list. That is aliasing. If you "
        "photocopy it first, his copy stays unchanged — that is a real copy.",
        "फ़्रिज पर लगी साझा शॉपिंग लिस्ट। आप पेन से \"दूध\" जोड़ते हैं तो भाई को भी "
        "दूध दिखता है — लिस्ट एक ही है। यह aliasing है। पहले फ़ोटोकॉपी कर लें तो उसकी "
        "कॉपी नहीं बदलती — यह असली कॉपी है।",
        "Fridge par lagi shared shopping list. Aap pen se \"doodh\" jodte ho to bhai "
        "ko bhi doodh dikhta hai - list ek hi hai. Ye aliasing hai. Pehle photocopy "
        "kar lo to uski copy nahi badalti - ye asli copy hai.",
    ),
    "https://docs.python.org/3/tutorial/introduction.html#lists",
    visual="alias_copy",
    examples=[
        ex(
            "nums = [10, 20, 30]\nnums.append(40)\nprint(nums)\nnums[0] = 99\nprint(nums, len(nums))",
            "[10, 20, 30, 40]\n[99, 20, 30, 40] 4",
            L("changing a list in place", "लिस्ट को जगह पर बदलना", "list ko jagah par badalna"),
            note=L(
                "append and index assignment change the same list; no new list is made.",
                "append और इंडेक्स असाइनमेंट उसी लिस्ट को बदलते हैं; नई लिस्ट नहीं बनती।",
                "append aur index assignment usi list ko badalte hain; nayi list nahi banti.",
            ),
        ),
        ex(
            "a = [1, 2]\nb = a\nb.append(3)\nprint(a)\nc = a[:]\nc.append(4)\nprint(a)\nprint(c)",
            "[1, 2, 3]\n[1, 2, 3]\n[1, 2, 3, 4]",
            L("alias versus copy", "एलियस बनाम कॉपी", "alias versus copy"),
            note=L(
                "b = a makes a second name for one list. a[:] or list(a) or a.copy() "
                "makes a second list.",
                "b = a एक लिस्ट के लिए दूसरा नाम बनाता है। a[:] या list(a) या a.copy() "
                "दूसरी लिस्ट बनाते हैं।",
                "b = a ek list ke liye doosra naam banata hai. a[:] ya list(a) ya "
                "a.copy() doosri list banate hain.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Start with `cart = ['bread']`, add 'milk' with append, then print the "
                "length.",
                "`cart = ['bread']` से शुरू करें, append से 'milk' जोड़ें, फिर लंबाई प्रिंट करें।",
                "`cart = ['bread']` se shuru karo, append se 'milk' jodo, phir length print karo.",
            ),
            "cart = ['bread']\n# ...\n",
            "cart = ['bread']\ncart.append('milk')\nprint(len(cart))",
            ["cart == ['bread', 'milk']", 'printed.strip() == "2"'],
            L("append changes the list and returns None.", "append लिस्ट बदलता है और None देता है।", "append list badalta hai aur None deta hai."),
        ),
    ],
    quiz_items=[
        quiz(
            L("a = [1, 2]; b = a; b.append(3). What is a?", "a = [1, 2]; b = a; b.append(3). a क्या है?", "a = [1, 2]; b = a; b.append(3). a kya hai?"),
            ["[1, 2]", "[1, 2, 3]", "an error", "[3]"],
            "b",
            L(
                "b is another name for the same list, so appending through b changes "
                "a as well.",
                "b उसी लिस्ट का दूसरा नाम है, इसलिए b से append करने पर a भी बदल जाता है।",
                "b usi list ka doosra naam hai, isliye b se append karne par a bhi badal jata hai.",
            ),
            "aliasing",
        ),
        quiz(
            L(
                "Which one makes an independent copy?",
                "कौन सा स्वतंत्र कॉपी बनाता है?",
                "Kaun sa independent copy banata hai?",
            ),
            ["b = a", "b = a[:]", "b = a.append(0)", "b = a[0]"],
            "b",
            L(
                "A full slice copies the list. b = a only adds a name, and append "
                "returns None.",
                "पूरा स्लाइस लिस्ट कॉपी करता है। b = a सिर्फ़ नाम जोड़ता है, और append "
                "None देता है।",
                "Poora slice list copy karta hai. b = a sirf naam jodta hai, aur "
                "append None deta hai.",
            ),
            "aliasing",
        ),
        quiz(
            L("What is len([1, [2, 3], 4])?", "len([1, [2, 3], 4]) क्या है?", "len([1, [2, 3], 4]) kya hai?"),
            ["4", "3", "2", "an error"],
            "b",
            L(
                "len counts top-level items. The inner list counts as one item, no "
                "matter how many things are inside it.",
                "len सिर्फ़ ऊपरी स्तर के आइटम गिनता है। अंदरूनी लिस्ट एक आइटम है, चाहे "
                "उसमें कुछ भी हो।",
                "len sirf top-level items ginta hai. Andaruni list ek item hai, chahe "
                "usme kuch bhi ho.",
            ),
        ),
    ],
    takeaway=L(
        "Lists are mutable; b = a shares, a[:] copies.",
        "लिस्ट mutable हैं; b = a साझा करता है, a[:] कॉपी करता है।",
        "Lists mutable hain; b = a share karta hai, a[:] copy karta hai.",
    ),
)

l02 = lesson(
    "m04c01l02",
    L("List methods and sorting", "लिस्ट मेथड और सॉर्टिंग", "List methods aur sorting"),
    [],
    L(
        "Lists have methods for everyday work: append, insert, remove, pop, extend, "
        "count, index, sort, reverse. sorted() returns a new sorted list while "
        "list.sort() sorts in place and returns None.",
        "लिस्ट में रोज़ के काम के मेथड हैं: append, insert, remove, pop, extend, "
        "count, index, sort, reverse। sorted() नई सॉर्टेड लिस्ट देता है जबकि "
        "list.sort() जगह पर सॉर्ट करता है और None देता है।",
        "List me roz ke kaam ke methods hain: append, insert, remove, pop, extend, "
        "count, index, sort, reverse. sorted() nayi sorted list deta hai jabki "
        "list.sort() jagah par sort karta hai aur None deta hai.",
    ),
    L(
        "A queue at a ticket counter: append joins the back, pop() leaves from the "
        "back, and pop(0) would be the front. For a real queue you would use "
        "collections.deque, but a list is fine to learn the idea.",
        "टिकट काउंटर की कतार: append पीछे जोड़ता है, pop() पीछे से निकालता है, और "
        "pop(0) आगे से। असली कतार के लिए collections.deque बेहतर है, पर आइडिया "
        "समझने के लिए लिस्ट ठीक है।",
        "Ticket counter ki kataar: append peeche jodta hai, pop() peeche se nikalta "
        "hai, aur pop(0) aage se. Asli kataar ke liye collections.deque behtar hai, "
        "par idea samajhne ke liye list theek hai.",
    ),
    "https://docs.python.org/3/tutorial/datastructures.html#more-on-lists",
    examples=[
        ex(
            "nums = [3, 1, 4, 1, 5]\nnums.append(9)\nnums.insert(0, 7)\nnums.remove(1)\nprint(nums)\nprint(nums.pop())\nprint(nums)",
            "[7, 3, 4, 1, 5, 9]\n9\n[7, 3, 4, 1, 5]",
            L("adding and removing", "जोड़ना और हटाना", "jodna aur hataana"),
            note=L(
                "remove(1) removes the first value equal to 1, not index 1. That "
                "difference bites beginners constantly.",
                "remove(1) पहली वैल्यू 1 हटाता है, इंडेक्स 1 नहीं। यह फ़र्क शुरुआती "
                "लोगों को लगातार चौंकाता है।",
                "remove(1) pehli value 1 hataata hai, index 1 nahi. Ye farq beginners "
                "ko lagatar chaukaata hai.",
            ),
        ),
        ex(
            'words = ["banana", "fig", "kiwi"]\nprint(sorted(words))\nprint(sorted(words, key=len))\nprint(sorted(words, reverse=True))\nprint(words)',
            "['banana', 'fig', 'kiwi']\n['fig', 'kiwi', 'banana']\n['kiwi', 'fig', 'banana']\n['banana', 'fig', 'kiwi']",
            L("sorted returns a new list", "sorted नई लिस्ट देता है", "sorted nayi list deta hai"),
            note=L(
                "words is unchanged at the end. sort() would have changed it in place.",
                "अंत में words वैसा ही है। sort() उसे जगह पर बदल देता।",
                "End me words waisa hi hai. sort() use jagah par badal deta.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Sort `scores = [55, 91, 72]` from highest to lowest and print the "
                "result. Do not change the original list.",
                "`scores = [55, 91, 72]` को सबसे बड़े से छोटे क्रम में सॉर्ट करें और "
                "प्रिंट करें। मूल लिस्ट न बदलें।",
                "`scores = [55, 91, 72]` ko sabse bade se chhote order me sort karo aur "
                "print karo. Original list na badlo.",
            ),
            "scores = [55, 91, 72]\n# ...\n",
            "scores = [55, 91, 72]\nprint(sorted(scores, reverse=True))",
            ['printed.strip() == "[91, 72, 55]"', "scores == [55, 91, 72]"],
            L("sorted(..., reverse=True) returns a new list.", "sorted(..., reverse=True) नई लिस्ट देता है।", "sorted(..., reverse=True) nayi list deta hai."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What does [1, 2, 3].pop() return?", "[1, 2, 3].pop() क्या लौटाता है?", "[1, 2, 3].pop() kya return karta hai?"),
            ["1", "3", "[1, 2]", "None"],
            "b",
            L(
                "pop() removes and returns the last item. pop(0) would return 1.",
                "pop() आख़िरी आइटम हटाकर लौटाता है। pop(0) 1 लौटाता।",
                "pop() aakhri item hataakar return karta hai. pop(0) 1 return karta.",
            ),
        ),
        quiz(
            L(
                "nums = [3, 1, 2]; result = nums.sort(); print(result). What prints?",
                "nums = [3, 1, 2]; result = nums.sort(); print(result)। क्या प्रिंट होगा?",
                "nums = [3, 1, 2]; result = nums.sort(); print(result). Kya print hoga?",
            ),
            ["[1, 2, 3]", "None", "an error", "[3, 1, 2]"],
            "b",
            L(
                "sort() sorts in place and returns None. Assigning its result is the "
                "classic mistake; use sorted() if you want the value.",
                "sort() जगह पर सॉर्ट करता है और None देता है। उसका परिणाम असाइन करना "
                "क्लासिक गलती है; वैल्यू चाहिए तो sorted() इस्तेमाल करें।",
                "sort() jagah par sort karta hai aur None deta hai. Uska result "
                "assign karna classic galti hai; value chahiye to sorted() use karo.",
            ),
            "sort-returns-none",
        ),
        quiz(
            L(
                "nums = [1, 2, 3]; nums.remove(2). What is nums now?",
                "nums = [1, 2, 3]; nums.remove(2). अब nums क्या है?",
                "nums = [1, 2, 3]; nums.remove(2). Ab nums kya hai?",
            ),
            ["[1, 3]", "[1, 2]", "[2, 3]", "an error"],
            "a",
            L(
                "remove takes a value, not an index, and deletes the first match.",
                "remove वैल्यू लेता है, इंडेक्स नहीं, और पहला मेल हटाता है।",
                "remove value leta hai, index nahi, aur pehla match hataata hai.",
            ),
        ),
    ],
    takeaway=L(
        "sorted() returns a list; sort() returns None; remove takes a value.",
        "sorted() लिस्ट देता है; sort() None देता है; remove वैल्यू लेता है।",
        "sorted() list deta hai; sort() None deta hai; remove value leta hai.",
    ),
)

l03 = lesson(
    "m04c02l03",
    L("Tuples and unpacking", "ट्यूपल और अनपैकिंग", "Tuples aur unpacking"),
    [],
    L(
        "A tuple is an ordered collection you cannot change. It is perfect for a "
        "fixed group of values such as coordinates or a date. Unpacking assigns "
        "several names in one line.",
        "ट्यूपल क्रम में रखा ऐसा संग्रह है जिसे बदला नहीं जा सकता। तय समूह के लिए "
        "यह परफ़ेक्ट है जैसे निर्देशांक या तारीख़। अनपैकिंग एक लाइन में कई नाम "
        "असाइन करती है।",
        "Tuple order me rakha aisa collection hai jise badla nahi ja sakta. Fixed "
        "group ke liye ye perfect hai jaise coordinates ya date. Unpacking ek line "
        "me kai naam assign karti hai.",
    ),
    L(
        "A passport is a tuple: name, date of birth, place. You do not edit those "
        "fields, you get a new passport. A shopping list is a list: it changes every "
        "week.",
        "पासपोर्ट एक ट्यूपल है: नाम, जन्मतिथि, जगह। आप वे फ़ील्ड बदलते नहीं, नया "
        "पासपोर्ट मिलता है। शॉपिंग लिस्ट एक लिस्ट है: वह हर हफ़्ते बदलती है।",
        "Passport ek tuple hai: naam, date of birth, jagah. Aap woh fields badalte "
        "nahi, naya passport milta hai. Shopping list ek list hai: woh har hafte badalti hai.",
    ),
    "https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences",
    examples=[
        ex(
            "point = (3, 5)\nx, y = point\nprint(x, y)\nprint(point[0])\nprint(len(point))",
            "3 5\n3\n2",
            L("unpacking a tuple", "ट्यूपल खोलना", "tuple kholna"),
        ),
        ex(
            "first, *rest = [1, 2, 3, 4]\nprint(first, rest)\na, b = 1, 2\na, b = b, a\nprint(a, b)\nprint((1, 2) + (3,))",
            "1 [2, 3, 4]\n2 1\n(1, 2, 3)",
            L("star unpacking and swapping", "स्टार अनपैकिंग और बदलना", "star unpacking aur swap"),
            note=L(
                "a, b = b, a swaps without a temporary variable. The trailing comma in "
                "(3,) makes it a tuple, not a number in brackets.",
                "a, b = b, a बिना टेम्परेरी वेरिएबल के बदल देता है। (3,) में अंतिम "
                "कॉमा उसे ट्यूपल बनाता है, ब्रैकेट में नंबर नहीं।",
                "a, b = b, a bina temporary variable ke swap karta hai. (3,) me "
                "trailing comma use tuple banata hai, bracket me number nahi.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Given `pair = ('Asha', 91)`, unpack it into `name` and `score`, then "
                "print `name`.",
                "`pair = ('Asha', 91)` को `name` और `score` में खोलें, फिर `name` प्रिंट करें।",
                "`pair = ('Asha', 91)` ko `name` aur `score` me kholo, phir `name` print karo.",
            ),
            "pair = ('Asha', 91)\n# name, score = ...\n",
            "pair = ('Asha', 91)\nname, score = pair\nprint(name)",
            ['name == "Asha"', "score == 91", '"Asha" in printed'],
            L("Left side has the names, right side has the tuple.", "बाएँ नाम, दाएँ ट्यूपल।", "Left me naam, right me tuple."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is type((5))?", "type((5)) क्या है?", "type((5)) kya hai?"),
            ["tuple", "int", "list", "an error"],
            "b",
            L(
                "(5) is just 5 in brackets. A one-item tuple needs a comma: (5,).",
                "(5) सिर्फ़ ब्रैकेट में 5 है। एक आइटम का ट्यूपल (5,) होता है।",
                "(5) sirf bracket me 5 hai. Ek item ka tuple (5,) hota hai.",
            ),
            "single-tuple-comma",
        ),
        quiz(
            L("Can you do t = (1, 2); t[0] = 9?", "क्या t = (1, 2); t[0] = 9 चलेगा?", "Kya t = (1, 2); t[0] = 9 chalega?"),
            ["yes", "no, TypeError", "no, but only for strings", "yes, if you use append"],
            "b",
            L(
                "Tuples are immutable, so item assignment raises TypeError. You would "
                "build a new tuple instead.",
                "ट्यूपल immutable हैं, इसलिए आइटम असाइनमेंट TypeError देता है। उसकी "
                "जगह नया ट्यूपल बनाएँ।",
                "Tuples immutable hain, isliye item assignment TypeError deta hai. "
                "Uski jagah naya tuple banao.",
            ),
        ),
        quiz(
            L("What is a, b = 1, 2, 3?", "a, b = 1, 2, 3 क्या है?", "a, b = 1, 2, 3 kya hai?"),
            ["a=1, b=2", "a=1, b=(2, 3)", "a=(1,2), b=3", "ValueError"],
            "d",
            L(
                "The counts must match: two names, three values. Use a, b, *rest = "
                "1, 2, 3 to collect the extra one.",
                "गिनती मेल खानी चाहिए: दो नाम, तीन वैल्यू। बचा इकट्ठा करने के लिए "
                "a, b, *rest = 1, 2, 3 लिखें।",
                "Count match karni chahiye: do naam, teen values. Bacha collect karne "
                "ke liye a, b, *rest = 1, 2, 3 likho.",
            ),
        ),
    ],
    takeaway=L(
        "Tuples are immutable; unpacking names several values in one line.",
        "ट्यूपल immutable हैं; अनपैकिंग एक लाइन में कई नाम देती है।",
        "Tuples immutable hain; unpacking ek line me kai naam deti hai.",
    ),
)

l04 = lesson(
    "m04c03l04",
    L("Dictionaries", "डिक्शनरी", "Dictionaries"),
    [],
    L(
        "A dict stores key-value pairs. You look a value up by its key instead of by "
        "position, which is what you want when the data has names. Keys must be "
        "immutable; values can be anything.",
        "डिक्शनरी की-वैल्यू जोड़े रखती है। आप वैल्यू को पोज़िशन की जगह उसकी की से "
        "ढूँढते हैं, जो तब चाहिए जब डेटा के नाम हों। की immutable होनी चाहिए; वैल्यू "
        "कुछ भी हो सकती है।",
        "Dictionary key-value pairs rakhti hai. Aap value ko position ki jagah uski "
        "key se dhoondte ho, jo tab chahiye jab data ke naam hon. Key immutable honi "
        "chahiye; value kuch bhi ho sakti hai.",
    ),
    L(
        "A phone book is the perfect dict: the name is the key, the number is the "
        "value. You do not ask for \"entry 47\", you ask for \"Mummy\".",
        "फ़ोन बुक परफ़ेक्ट dict है: नाम की है, नंबर वैल्यू। आप \"entry 47\" नहीं "
        "पूछते, आप \"Mummy\" पूछते हैं।",
        "Phone book perfect dict hai: naam key hai, number value. Aap \"entry 47\" "
        "nahi poochhte, aap \"Mummy\" poochhte ho.",
    ),
    "https://docs.python.org/3/tutorial/datastructures.html#dictionaries",
    visual="dict_map",
    examples=[
        ex(
            'person = {"name": "Asha", "age": 30}\nprint(person["name"])\nprint(person.get("city", "unknown"))\nperson["city"] = "Pune"\nprint(person)\nprint(list(person.keys()))',
            "Asha\nunknown\n{'name': 'Asha', 'age': 30, 'city': 'Pune'}\n['name', 'age', 'city']",
            L("lookup, default, add", "खोज, डिफ़ॉल्ट, जोड़ना", "lookup, default, add"),
            note=L(
                "person[\"city\"] would raise KeyError before the key exists. get() "
                "returns a default instead.",
                "की बनने से पहले person[\"city\"] KeyError देता। get() उसकी जगह "
                "डिफ़ॉल्ट देता है।",
                "Key banne se pehle person[\"city\"] KeyError deta. get() uski jagah "
                "default deta hai.",
            ),
        ),
        ex(
            'counts = {}\nfor word in ["a", "b", "a"]:\n    counts[word] = counts.get(word, 0) + 1\nprint(counts)\nfor key, value in counts.items():\n    print(key, value)',
            "{'a': 2, 'b': 1}\na 2\nb 1",
            L("counting with get", "get से गिनना", "get se ginna"),
            note=L(
                "This is the standard counting pattern before you learn "
                "collections.Counter in module 11.",
                "यह मॉड्यूल 11 में collections.Counter सीखने से पहले का मानक गिनती "
                "पैटर्न है।",
                "Ye module 11 me collections.Counter seekhne se pehle ka standard "
                "ginti pattern hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Build `ages = {'Asha': 30}` and add 'Ravi': 25, then print Ravi's age "
                "using its key.",
                "`ages = {'Asha': 30}` बनाएँ और 'Ravi': 25 जोड़ें, फिर की से Ravi की "
                "उम्र प्रिंट करें।",
                "`ages = {'Asha': 30}` banao aur 'Ravi': 25 jodo, phir key se Ravi ki "
                "age print karo.",
            ),
            "ages = {'Asha': 30}\n# ...\n",
            "ages = {'Asha': 30}\nages['Ravi'] = 25\nprint(ages['Ravi'])",
            ["ages == {'Asha': 30, 'Ravi': 25}", 'printed.strip() == "25"'],
            L("Square brackets with a new key create it.", "नई की के साथ स्क्वायर ब्रैकेट उसे बना देता है।", "Nayi key ke saath square bracket use bana deta hai."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                'd = {"a": 1}. What does d["b"] do?',
                'd = {"a": 1}. d["b"] क्या करता है?',
                'd = {"a": 1}. d["b"] kya karta hai?',
            ),
            ["returns None", "returns 0", "raises KeyError", "creates the key"],
            "c",
            L(
                "Square-bracket lookup of a missing key raises KeyError. Use .get(\"b\") "
                "when the key may be absent.",
                "गुम की पर स्क्वायर-ब्रैकेट लुकअप KeyError देता है। की न हो सकती हो तो "
                ".get(\"b\") इस्तेमाल करें।",
                "Missing key par square-bracket lookup KeyError deta hai. Key na ho "
                "sakti ho to .get(\"b\") use karo.",
            ),
            "dict-keyerror",
        ),
        quiz(
            L(
                "Which is a valid dict key?",
                "कौन सी वैध dict की है?",
                "Kaun si valid dict key hai?",
            ),
            ["[1, 2]", "{'a': 1}", "(1, 2)", "['a']"],
            "c",
            L(
                "Keys must be immutable (hashable). A tuple of numbers is fine; a list "
                "or a dict is not.",
                "की immutable (hashable) होनी चाहिए। नंबरों का ट्यूपल ठीक है; लिस्ट या "
                "dict नहीं।",
                "Key immutable (hashable) honi chahiye. Numbers ka tuple theek hai; "
                "list ya dict nahi.",
            ),
        ),
        quiz(
            L(
                "What does {'a': 1}.get('b', 0) return?",
                "{'a': 1}.get('b', 0) क्या लौटाता है?",
                "{'a': 1}.get('b', 0) kya return karta hai?",
            ),
            ["KeyError", "None", "0", "1"],
            "c",
            L(
                "get returns the second argument when the key is missing. That is why "
                "get(key, 0) + 1 is the classic counter.",
                "की न होने पर get दूसरा आर्ग्युमेंट लौटाता है। इसीलिए get(key, 0) + 1 "
                "क्लासिक काउंटर है।",
                "Key na hone par get doosra argument return karta hai. Isliye "
                "get(key, 0) + 1 classic counter hai.",
            ),
        ),
    ],
    takeaway=L(
        "Dicts map keys to values; use get() for keys that may be missing.",
        "dict की को वैल्यू से जोड़ती है; गुम की के लिए get() इस्तेमाल करें।",
        "Dict key ko value se jodta hai; missing key ke liye get() use karo.",
    ),
)

l05 = lesson(
    "m04c03l05",
    L("Nested data", "नेस्टेड डेटा", "Nested data"),
    [],
    L(
        "Real data is nested: a list of dicts, a dict of lists, a list of lists. You "
        "reach inside one step at a time, and .get() chains keep missing pieces from "
        "crashing the program.",
        "असली डेटा नेस्टेड होता है: dict की लिस्ट, लिस्ट की dict, लिस्ट की लिस्ट। "
        "आप एक-एक कदम अंदर जाते हैं, और .get() की चेन गुम टुकड़ों पर प्रोग्राम "
        "क्रैश नहीं होने देती।",
        "Asli data nested hota hai: dict ki list, list ki dict, list ki list. Aap "
        "ek-ek kadam andar jaate ho, aur .get() ki chain missing tukdon par program "
        "crash nahi hone deti.",
    ),
    L(
        "A class register: a list of students, each student a dict with a name and a "
        "list of marks. That is exactly how JSON from a web API looks, which is why "
        "this lesson matters later.",
        "क्लास रजिस्टर: छात्रों की लिस्ट, हर छात्र एक dict जिसमें नाम और नंबरों की "
        "लिस्ट। वेब API का JSON बिल्कुल ऐसा ही दिखता है, इसीलिए यह लेसन आगे काम आता है।",
        "Class register: students ki list, har student ek dict jisme naam aur marks "
        "ki list. Web API ka JSON bilkul aisa hi dikhta hai, isliye ye lesson aage kaam aata hai.",
    ),
    "https://docs.python.org/3/tutorial/datastructures.html#dictionaries",
    examples=[
        ex(
            'students = [\n    {"name": "Asha", "marks": [88, 92]},\n    {"name": "Ravi", "marks": [70, 81]},\n]\nfor s in students:\n    print(s["name"], sum(s["marks"]) / len(s["marks"]))',
            "Asha 90.0\nRavi 75.5",
            L("a list of dicts", "dict की लिस्ट", "dict ki list"),
        ),
        ex(
            'data = {"user": {"name": "Asha", "roles": ["admin", "editor"]}}\nprint(data["user"]["name"])\nprint(data["user"]["roles"][0])\nprint(data.get("missing", {}).get("name", "n/a"))',
            "Asha\nadmin\nn/a",
            L("walking down safely", "सुरक्षित नीचे जाना", "safely neeche jaana"),
            note=L(
                "data.get(\"missing\", {}) returns an empty dict, so the second .get() "
                "still works. Chaining plain [] here would raise KeyError.",
                "data.get(\"missing\", {}) खाली dict देता है, इसलिए दूसरा .get() भी "
                "चलता है। यहाँ सादा [] KeyError देता।",
                "data.get(\"missing\", {}) khaali dict deta hai, isliye doosra .get() "
                "bhi chalta hai. Yahan saada [] KeyError deta.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "From `order = {'items': [{'price': 50}, {'price': 70}]}` print the "
                "total price.",
                "`order = {'items': [{'price': 50}, {'price': 70}]}` से कुल कीमत प्रिंट करें।",
                "`order = {'items': [{'price': 50}, {'price': 70}]}` se total price print karo.",
            ),
            "order = {'items': [{'price': 50}, {'price': 70}]}\n# ...\n",
            "order = {'items': [{'price': 50}, {'price': 70}]}\nprint(sum(i['price'] for i in order['items']))",
            ['printed.strip() == "120"'],
            L("A generator inside sum() keeps it to one line.", "sum() के अंदर जनरेटर एक लाइन में रखता है।", "sum() ke andar generator ek line me rakhta hai."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                'data = {"a": {"b": 5}}. What is data["a"]["b"]?',
                'data = {"a": {"b": 5}}. data["a"]["b"] क्या है?',
                'data = {"a": {"b": 5}}. data["a"]["b"] kya hai?',
            ),
            ["5", "'b'", "{'b': 5}", "an error"],
            "a",
            L(
                "The first [] gets the inner dict, the second gets the value inside it.",
                "पहला [] अंदरूनी dict देता है, दूसरा उसके अंदर की वैल्यू।",
                "Pehla [] andaruni dict deta hai, doosra uske andar ki value.",
            ),
        ),
        quiz(
            L(
                "Why is data.get('x', {}).get('y') safer than data['x']['y']?",
                "data.get('x', {}).get('y') data['x']['y'] से सुरक्षित क्यों है?",
                "data.get('x', {}).get('y') data['x']['y'] se safe kyun hai?",
            ),
            [
                "get is faster",
                "a missing 'x' gives an empty dict instead of KeyError",
                "get creates the key",
                "it is not safer",
            ],
            "b",
            L(
                "With [], a missing key raises KeyError and the program stops. With "
                "get, you get a default and can keep going.",
                "[], में गुम की KeyError देती है और प्रोग्राम रुक जाता है। get से "
                "डिफ़ॉल्ट मिलता है और काम चलता रहता है।",
                "[], me missing key KeyError deti hai aur program ruk jata hai. get se "
                "default milta hai aur kaam chalta rehta hai.",
            ),
        ),
        quiz(
            L(
                "Which is the correct way to read the first mark? marks = [[88, 92], [70]]",
                "पहला नंबर पढ़ने का सही तरीका? marks = [[88, 92], [70]]",
                "Pehla mark padhne ka sahi tarika? marks = [[88, 92], [70]]",
            ),
            ["marks[0]", "marks[0][0]", "marks[1][0]", "marks[0, 0]"],
            "b",
            L(
                "marks[0] is the inner list [88, 92]; one more [0] gets 88. marks[0, 0] "
                "is a tuple index and raises TypeError on a list.",
                "marks[0] अंदरूनी लिस्ट [88, 92] है; एक और [0] से 88 मिलता है। "
                "marks[0, 0] ट्यूपल इंडेक्स है और लिस्ट पर TypeError देता है।",
                "marks[0] andaruni list [88, 92] hai; ek aur [0] se 88 milta hai. "
                "marks[0, 0] tuple index hai aur list par TypeError deta hai.",
            ),
        ),
    ],
    takeaway=L(
        "Nested data is read one step at a time; .get() keeps missing keys safe.",
        "नेस्टेड डेटा एक-एक कदम पढ़ा जाता है; .get() गुम की को सुरक्षित रखता है।",
        "Nested data ek-ek kadam padha jata hai; .get() missing key ko safe rakhta hai.",
    ),
)

l06 = lesson(
    "m04c04l06",
    L("Sets", "सेट", "Sets"),
    [],
    L(
        "A set is an unordered collection with no duplicates. It answers \"is this "
        "in here?\" extremely fast and supports the maths you learned at school: "
        "union, intersection and difference.",
        "सेट बिना क्रम और बिना दोहराव का संग्रह है। यह \"क्या यह इसमें है?\" बहुत तेज़ "
        "बताता है और स्कूल की गणित देता है: यूनियन, इंटरसेक्शन और डिफ़रेंस।",
        "Set bina order aur bina duplicate ka collection hai. Ye \"kya ye isme hai?\" "
        "bahut fast batata hai aur school ki maths deta hai: union, intersection aur difference.",
    ),
    L(
        "Two friends compare their movie lists. Which movies both watched? "
        "Intersection. Which did only you watch? Difference. Which did at least one "
        "of you watch? Union.",
        "दो दोस्त अपनी मूवी लिस्ट मिलाते हैं। दोनों ने कौन सी देखी? इंटरसेक्शन। सिर्फ़ "
        "आपने कौन सी देखी? डिफ़रेंस। कम से कम एक ने कौन सी देखी? यूनियन।",
        "Do dost apni movie list milate hain. Dono ne kaun si dekhi? Intersection. "
        "Sirf aapne kaun si dekhi? Difference. Kam se kam ek ne kaun si dekhi? Union.",
    ),
    "https://docs.python.org/3/tutorial/datastructures.html#sets",
    examples=[
        ex(
            "a = {1, 2, 3}\nb = {3, 4}\nprint(a | b)\nprint(a & b)\nprint(a - b)\nprint(2 in a)",
            "{1, 2, 3, 4}\n{3}\n{1, 2}\nTrue",
            L("set algebra", "सेट गणित", "set algebra"),
            note=L(
                "| is union, & is intersection, - is difference. The method names are "
                "union(), intersection(), difference().",
                "| यूनियन, & इंटरसेक्शन, - डिफ़रेंस। मेथड नाम union(), "
                "intersection(), difference() हैं।",
                "| union, & intersection, - difference. Method naam union(), "
                "intersection(), difference() hain.",
            ),
        ),
        ex(
            'names = ["asha", "ravi", "asha"]\nunique = set(names)\nprint(len(unique))\nprint(sorted(unique))\nempty = set()\nprint(type(empty))',
            "2\n['asha', 'ravi']\n<class 'set'>",
            L("removing duplicates", "दोहराव हटाना", "duplicates hataana"),
            note=L(
                "{} makes an empty dict, not an empty set. Use set() for an empty set.",
                "{} खाली dict बनाता है, खाली सेट नहीं। खाली सेट के लिए set() लिखें।",
                "{} khaali dict banata hai, khaali set nahi. Khaali set ke liye set() likho.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Find the common subjects in a = {'math', 'art'} and b = {'art', "
                "'music'} and print them.",
                "a = {'math', 'art'} और b = {'art', 'music'} में साझा विषय खोजें और प्रिंट करें।",
                "a = {'math', 'art'} aur b = {'art', 'music'} me common subject dhoondo aur print karo.",
            ),
            "a = {'math', 'art'}\nb = {'art', 'music'}\n# print(...)\n",
            "a = {'math', 'art'}\nb = {'art', 'music'}\nprint(a & b)",
            ['printed.strip() in ("{\'art\'}", "set()") or "art" in printed'],
            L("& gives the intersection.", "& इंटरसेक्शन देता है।", "& intersection deta hai."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What is len({1, 1, 2, 2, 3})?", "len({1, 1, 2, 2, 3}) क्या है?", "len({1, 1, 2, 2, 3}) kya hai?"),
            ["5", "3", "2", "an error"],
            "b",
            L("A set drops duplicates, so only 1, 2 and 3 remain.", "सेट दोहराव हटाता है, इसलिए सिर्फ़ 1, 2, 3 बचते हैं।", "Set duplicate hataata hai, isliye sirf 1, 2, 3 bachte hain."),
        ),
        quiz(
            L("What is type({})?", "type({}) क्या है?", "type({}) kya hai?"),
            ["set", "dict", "tuple", "an error"],
            "b",
            L(
                "Empty braces make a dict. set() is the only way to write an empty set.",
                "खाली ब्रेसेस dict बनाते हैं। खाली सेट लिखने का एक ही तरीका set() है।",
                "Khaali braces dict banate hain. Khaali set likhne ka ek hi tarika set() hai.",
            ),
            "empty-braces",
        ),
        quiz(
            L(
                "Why can a set not be indexed like s[0]?",
                "सेट को s[0] की तरह इंडेक्स क्यों नहीं कर सकते?",
                "Set ko s[0] ki tarah index kyun nahi kar sakte?",
            ),
            [
                "it has no order, so position 0 means nothing",
                "it is too slow",
                "sets are immutable",
                "you can, it works",
            ],
            "a",
            L(
                "Sets are unordered by design (that is what makes membership fast). "
                "Convert with list(s) or sorted(s) when you need positions.",
                "सेट डिज़ाइन से बिना क्रम हैं (इसी से सदस्यता तेज़ होती है)। पोज़िशन "
                "चाहिए तो list(s) या sorted(s) करें।",
                "Sets design se unordered hain (isise membership fast hoti hai). "
                "Position chahiye to list(s) ya sorted(s) karo.",
            ),
        ),
    ],
    takeaway=L(
        "Sets remove duplicates and answer membership fast; {} is a dict, set() is a set.",
        "सेट दोहराव हटाते हैं और सदस्यता तेज़ बताते हैं; {} dict है, set() सेट है।",
        "Sets duplicate hataate hain aur membership fast batate hain; {} dict hai, set() set hai.",
    ),
)

MODULE = module(
    M,
    L("Collections", "संग्रह", "Collections"),
    L(
        "Hold many values well: lists when order and change matter, tuples when the "
        "group is fixed, dicts for named fields, sets for uniqueness and membership.",
        "कई वैल्यू अच्छे से रखें: क्रम और बदलाव के लिए लिस्ट, तय समूह के लिए ट्यूपल, "
        "नाम वाले फ़ील्ड के लिए dict, विशिष्टता के लिए सेट।",
        "Kai values achhe se rakho: order aur change ke liye list, fixed group ke "
        "liye tuple, named fields ke liye dict, uniqueness ke liye set.",
    ),
    [
        chapter("m04c01", L("Lists", "लिस्ट", "Lists"), [l01, l02]),
        chapter("m04c02", L("Tuples", "ट्यूपल", "Tuples"), [l03]),
        chapter("m04c03", L("Dictionaries", "डिक्शनरी", "Dictionaries"), [l04, l05]),
        chapter("m04c04", L("Sets", "सेट", "Sets"), [l06]),
    ],
    exam=[
        quiz(
            L("Which collection cannot contain duplicates?", "कौन सा संग्रह दोहराव नहीं रख सकता?", "Kaun sa collection duplicate nahi rakh sakta?"),
            ["list", "tuple", "set", "dict values"],
            "c",
            L("A set stores unique values only. A list and a tuple happily repeat.", "सेट सिर्फ़ अलग-अलग वैल्यू रखता है। लिस्ट और ट्यूपल दोहराव रख लेते हैं।", "Set sirf alag-alag values rakhta hai. List aur tuple duplicate rakh lete hain."),
        ),
        quiz(
            L("What is [1, 2] + [3]?", "[1, 2] + [3] क्या है?", "[1, 2] + [3] kya hai?"),
            ["[1, 2, 3]", "an error", "[1, 5]", "[4]"],
            "a",
            L("+ on lists concatenates and returns a new list. Use append or extend to change one in place.", "लिस्ट पर + जोड़ता है और नई लिस्ट देता है। जगह पर बदलने के लिए append या extend।", "List par + jodta hai aur nayi list deta hai. Jagah par badalne ke liye append ya extend."),
        ),
        quiz(
            L("What is (1, 2) * 2?", "(1, 2) * 2 क्या है?", "(1, 2) * 2 kya hai?"),
            ["(2, 4)", "(1, 2, 1, 2)", "an error", "(1, 2, 2)"],
            "b",
            L("* on a tuple or list repeats it, exactly like * on a string.", "ट्यूपल या लिस्ट पर * उसे दोहराता है, स्ट्रिंग की तरह।", "Tuple ya list par * use repeat karta hai, string ki tarah."),
        ),
        quiz(
            L("Which dict method returns all key-value pairs?", "कौन सा dict मेथड सभी की-वैल्यू जोड़े देता है?", "Kaun sa dict method sab key-value pairs deta hai?"),
            ["keys()", "values()", "items()", "get()"],
            "c",
            L("items() yields (key, value) tuples, which is why `for k, v in d.items()` works.", "items() (key, value) ट्यूपल देता है, इसीलिए `for k, v in d.items()` चलता है।", "items() (key, value) tuple deta hai, isliye `for k, v in d.items()` chalta hai."),
        ),
        quiz(
            L("What is {1, 2} & {2, 3}?", "{1, 2} & {2, 3} क्या है?", "{1, 2} & {2, 3} kya hai?"),
            ["{1, 2, 3}", "{2}", "{1, 3}", "an error"],
            "b",
            L("& keeps only the shared items.", "& सिर्फ़ साझा आइटम रखता है।", "& sirf shared items rakhta hai."),
        ),
        quiz(
            L("Which statement about tuple unpacking is true?", "ट्यूपल अनपैकिंग के बारे में कौन सा सही है?", "Tuple unpacking ke baare me kaun sa sahi hai?"),
            ["the number of names must match the number of values", "you need a loop", "it only works for strings", "it changes the tuple"],
            "a",
            L("a, b = 1, 2 works; a, b = 1, 2, 3 raises ValueError unless you use *rest.", "a, b = 1, 2 चलता है; a, b = 1, 2, 3 ValueError देता है जब तक *rest न लें।", "a, b = 1, 2 chalta hai; a, b = 1, 2, 3 ValueError deta hai jab tak *rest na lo."),
        ),
    ],
    icon="📦",
)
