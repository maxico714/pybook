"""Module 7 - Modules, imports and files: using other people's code, saving data."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m07"

l01 = lesson(
    "m07c01l01",
    L("import, from and as", "import, from और as", "import, from aur as"),
    ["import", "from", "as"],
    L(
        "A module is one .py file full of reusable code. `import math` loads the "
        "module and gives you its name; `from math import sqrt` takes one name out "
        "of it; `as` renames whatever you imported so it is shorter or clearer.",
        "मॉड्यूल एक .py फ़ाइल है जिसमें दोबारा काम आने वाला कोड होता है। `import math` "
        "मॉड्यूल लोड करके उसका नाम देता है; `from math import sqrt` उसमें से एक नाम "
        "लेता है; `as` आयातित चीज़ का नाम छोटा या साफ़ कर देता है।",
        "Module ek .py file hai jisme dobara kaam aane wala code hota hai. "
        "`import math` module load karke uska naam deta hai; `from math import sqrt` "
        "usme se ek naam leta hai; `as` imported cheez ka naam chhota ya saaf kar "
        "deta hai.",
    ),
    L(
        "A toolbox. `import math` is carrying the whole toolbox into the room. "
        "`from math import sqrt` is taking only the screwdriver. `as` is putting a "
        "label on it so you remember what it is.",
        "औज़ारों का डिब्बा। `import math` पूरा डिब्बा कमरे में लाना है। "
        "`from math import sqrt` सिर्फ़ पेचकस लेना है। `as` उस पर लेबल चिपकाना है ताकि "
        "याद रहे कि क्या है।",
        "Auzaron ka dibba. `import math` poora dibba kamre me laana hai. "
        "`from math import sqrt` sirf pechkas lena hai. `as` us par label chipkana "
        "hai taaki yaad rahe kya hai.",
    ),
    "https://docs.python.org/3/tutorial/modules.html",
    examples=[
        ex(
            "import math\n\nprint(math.sqrt(16))\nprint(math.pi > 3.14)",
            "4.0\nTrue",
            L("import keeps the module name", "import मॉड्यूल का नाम रखता है", "import module ka naam rakhta hai"),
            note=L(
                "After `import math`, everything lives under `math.`: that prefix is "
                "how Python knows which sqrt you mean when five modules all have one.",
                "`import math` के बाद सब कुछ `math.` के नीचे रहता है: यही उपसर्ग बताता "
                "है कि किस मॉड्यूल का sqrt चाहिए।",
                "`import math` ke baad sab kuch `math.` ke neeche rehta hai: yahi "
                "prefix batata hai ki kis module ka sqrt chahiye.",
            ),
        ),
        ex(
            "from math import sqrt as square_root\n\nprint(square_root(81))\nprint(square_root(2) > 1.41)",
            "9.0\nTrue",
            L("from ... import ... as ...", "from ... import ... as ...", "from ... import ... as ..."),
            note=L(
                "`from math import sqrt` drops the prefix. Adding `as square_root` "
                "makes the call read like a sentence.",
                "`from math import sqrt` उपसर्ग हटा देता है। `as square_root` जोड़ने से "
                "कॉल वाक्य जैसी पढ़ने में आती है।",
                "`from math import sqrt` prefix hata deta hai. `as square_root` "
                "jodne se call vakya jaisi padhne me aati hai.",
            ),
        ),
        ex(
            "import statistics as stats\n\nscores = [7, 9, 10]\nprint(stats.mean(scores))\nprint(stats.median(scores))",
            "8.666666666666666\n9",
            L("a short alias for a long name", "लंबे नाम के लिए छोटा उपनाम", "lambe naam ke liye chhota upnaam"),
            note=L(
                "The alias is only for this file. Another file can import the same "
                "module under a different name.",
                "उपनाम सिर्फ़ इस फ़ाइल के लिए है। दूसरी फ़ाइल उसी मॉड्यूल को अलग नाम से "
                "आयात कर सकती है।",
                "Upnaam sirf is file ke liye hai. Doosri file usi module ko alag naam "
                "se import kar sakti hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Import factorial from math under the name `fact`, then print "
                "`fact(5)`.",
                "math से factorial को `fact` नाम से आयात करें, फिर `fact(5)` प्रिंट करें।",
                "math se factorial ko `fact` naam se import karo, phir `fact(5)` print karo.",
            ),
            "# from math import ...\n# print(...)\n",
            "from math import factorial as fact\n\nprint(fact(5))",
            [
                "fact(5) == 120",
                "fact(0) == 1",
                "printed.strip() == '120'",
            ],
            L(
                "from math import factorial as fact",
                "from math import factorial as fact",
                "from math import factorial as fact",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "After `import math`, how do you call sqrt?",
                "`import math` के बाद sqrt कैसे बुलाएँ?",
                "`import math` ke baad sqrt kaise bulayein?",
            ),
            ["sqrt(9)", "math.sqrt(9)", "math(sqrt, 9)", "import sqrt(9)"],
            "b",
            L(
                "A plain `import` keeps the module as a namespace, so you need the "
                "prefix.",
                "सादा `import` मॉड्यूल को नेमस्पेस बनाए रखता है, इसलिए उपसर्ग चाहिए।",
                "Saada `import` module ko namespace banaye rakhta hai, isliye prefix "
                "chahiye.",
            ),
        ),
        quiz(
            L(
                "What does `from math import pi as PI` do?",
                "`from math import pi as PI` क्या करता है?",
                "`from math import pi as PI` kya karta hai?",
            ),
            [
                "imports the whole math module",
                "binds the value of math.pi to the name PI",
                "renames the math module on disk",
                "creates a new variable equal to 3",
            ],
            "b",
            L(
                "`as` only changes the local name you use for the imported object.",
                "`as` सिर्फ़ स्थानीय नाम बदलता है जिससे आप आयातित चीज़ को बुलाते हैं।",
                "`as` sirf local naam badalta hai jisse aap imported cheez ko bulate ho.",
            ),
        ),
        quiz(
            L(
                "Which is a good reason to import inside a function instead of at the "
                "top?",
                "फ़ंक्शन के अंदर import करने की अच्छी वजह कौन है?",
                "Function ke andar import karne ki achhi wajah kaun hai?",
            ),
            [
                "it makes the code faster in every case",
                "the module is heavy and only sometimes needed",
                "Python forbids top-level imports",
                "it hides the dependency from readers",
            ],
            "b",
            L(
                "A local import can avoid loading an expensive module on the paths "
                "that never use it. It also makes the dependency easy to miss, so use "
                "it deliberately.",
                "लोकल import महँगा मॉड्यूल उन रास्तों पर लोड नहीं करता जहाँ वह चाहिए ही "
                "नहीं। यह निर्भरता छिपा भी देता है, इसलिए सोच-समझकर करें।",
                "Local import mehnga module un raaston par load nahi karta jahan woh "
                "chahiye hi nahi. Ye dependency chhipa bhi deta hai, isliye soch-"
                "samajh kar karo.",
            ),
        ),
    ],
    takeaway=L(
        "import module for the whole toolbox, from module import name for one tool, as to rename it.",
        "पूरे डिब्बे के लिए import module, एक औज़ार के लिए from module import name, नाम बदलने के लिए as।",
        "Poore dibbe ke liye import module, ek auzar ke liye from module import name, naam badalne ke liye as.",
    ),
)

l02 = lesson(
    "m07c01l02",
    L("with: closing things safely", "with: चीज़ें सुरक्षित बंद करना", "with: cheezein safe band karna"),
    ["with", "as"],
    L(
        "`with` runs a block and guarantees cleanup afterwards, even if the block "
        "raises an error. For files it means the file is always closed, so nothing "
        "stays half-written on disk.",
        "`with` एक ब्लॉक चलाता है और बाद में सफ़ाई की गारंटी देता है, चाहे ब्लॉक में "
        "एरर आ जाए। फ़ाइलों के लिए इसका मतलब है फ़ाइल हमेशा बंद होती है, इसलिए डिस्क "
        "पर अधूरा लिखा नहीं रहता।",
        "`with` ek block chalata hai aur baad me safai ki guarantee deta hai, chahe "
        "block me error aa jaye. Files ke liye iska matlab hai file hamesha band hoti "
        "hai, isliye disk par adhoora likha nahi rehta.",
    ),
    L(
        "A shop shutter. You open it (enter the block), do your business, and the "
        "shutter comes down on its own when you leave - even if you run out in a "
        "hurry.",
        "दुकान का शटर। आप खोलते हैं (ब्लॉक में प्रवेश), काम करते हैं, और निकलते ही शटर "
        "अपने आप नीचे आ जाता है - चाहे आप जल्दी में भागें।",
        "Dukaan ka shutter. Aap kholte ho (block me pravesh), kaam karte ho, aur "
        "nikalte hi shutter apne aap neeche aa jata hai - chahe aap jaldi me bhaago.",
    ),
    "https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files",
    visual="files_with",
    examples=[
        ex(
            'from pathlib import Path\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    note = Path(tmp) / "note.txt"\n    with note.open("w", encoding="utf-8") as handle:\n        handle.write("hello")\n    with note.open(encoding="utf-8") as handle:\n        print(handle.read())',
            "hello",
            L("write, then read, both with with", "with से लिखें, फिर with से पढ़ें", "with se likho, phir with se padho"),
            note=L(
                "Two separate `with` blocks: one opens for writing, one for reading. "
                "The file is closed between them, so the text is really on disk.",
                "दो अलग `with` ब्लॉक: एक लिखने के लिए, एक पढ़ने के लिए। बीच में फ़ाइल "
                "बंद होती है, इसलिए टेक्स्ट सचमुच डिस्क पर है।",
                "Do alag `with` blocks: ek likhne ke liye, ek padhne ke liye. Beech me "
                "file band hoti hai, isliye text sachmuch disk par hai.",
            ),
        ),
        ex(
            'from pathlib import Path\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    log = Path(tmp) / "log.txt"\n    with log.open("w", encoding="utf-8") as handle:\n        handle.write("line")\n    print(handle.closed)',
            "True",
            L("closed without calling close()", "close() बुलाए बिना बंद", "close() bulaye bina band"),
            note=L(
                "`with` called close() for you. Without it you would need try/finally "
                "to close the file on every exit path.",
                "`with` ने आपके लिए close() बुला दिया। इसके बिना हर निकास रास्ते पर "
                "फ़ाइल बंद करने के लिए try/finally लिखना पड़ता।",
                "`with` ne aapke liye close() bula diya. Iske bina har nikaas raaste "
                "par file band karne ke liye try/finally likhna padta.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write the text `PyBook` into a temporary file using `with`, read it "
                "back into `text`, and print `text`.",
                "`with` से एक अस्थायी फ़ाइल में `PyBook` लिखें, उसे वापस `text` में "
                "पढ़ें, और `text` प्रिंट करें।",
                "`with` se ek temporary file me `PyBook` likho, use wapas `text` me "
                "padho, aur `text` print karo.",
            ),
            "from pathlib import Path\nimport tempfile\n\n# with tempfile.TemporaryDirectory() as tmp:\n#     ...\n",
            'from pathlib import Path\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    path = Path(tmp) / "pybook.txt"\n    with path.open("w", encoding="utf-8") as handle:\n        handle.write("PyBook")\n    with path.open(encoding="utf-8") as handle:\n        text = handle.read()\n\nprint(text)',
            [
                "text == 'PyBook'",
                "printed.strip() == 'PyBook'",
            ],
            L(
                "Open once with \"w\" to write, once with no mode to read.",
                "लिखने के लिए \"w\" के साथ खोलें, पढ़ने के लिए बिना मोड के।",
                "Likhne ke liye \"w\" ke saath kholo, padhne ke liye bina mode ke.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does `with` guarantee?",
                "`with` किसकी गारंटी देता है?",
                "`with` kiski guarantee deta hai?",
            ),
            [
                "the block runs faster",
                "cleanup runs even if the block raises",
                "no exceptions can happen",
                "the file is kept in memory",
            ],
            "b",
            L(
                "That is the whole point: the exit step (usually close()) runs on "
                "success and on failure.",
                "यही पूरा मक़सद है: निकास कदम (आमतौर पर close()) सफलता और विफलता दोनों "
                "पर चलता है।",
                "Yahi poora maksad hai: exit step (aam taur par close()) safalta aur "
                "vifalta dono par chalta hai.",
            ),
        ),
        quiz(
            L(
                "Which line opens a file for writing and clears old contents?",
                "कौन सी लाइन लिखने के लिए खोलती है और पुरानी सामग्री मिटा देती है?",
                "Kaun si line likhne ke liye kholti hai aur purani content mita deti hai?",
            ),
            ['open(p, "r")', 'open(p, "w")', 'open(p, "a")', 'open(p)'],
            "b",
            L(
                '"w" truncates. "a" appends, "r" reads.',
                '"w" काट देता है। "a" जोड़ता है, "r" पढ़ता है।',
                '"w" kaat deta hai. "a" jodta hai, "r" padhta hai.',
            ),
        ),
        quiz(
            L(
                "Why pass `encoding=\"utf-8\"` when opening a text file?",
                "टेक्स्ट फ़ाइल खोलते समय `encoding=\"utf-8\"` क्यों दें?",
                "Text file kholte samay `encoding=\"utf-8\"` kyun dein?",
            ),
            [
                "it makes reading faster",
                "the default encoding depends on the operating system",
                "Python cannot read files without it",
                "it compresses the file",
            ],
            "b",
            L(
                "Windows and Linux do not agree on the default. Naming the encoding "
                "keeps Hindi, emoji and accented text intact everywhere.",
                "Windows और Linux का डिफ़ॉल्ट एक जैसा नहीं है। एनकोडिंग लिखने से हिंदी, "
                "इमोजी और एक्सेंट वाला टेक्स्ट हर जगह सही रहता है।",
                "Windows aur Linux ka default ek jaisa nahi hai. Encoding likhne se "
                "Hindi, emoji aur accented text har jagah sahi rehta hai.",
            ),
        ),
    ],
    takeaway=L(
        "Any resource that must be released belongs in a `with` block.",
        "जो भी संसाधन छोड़ना ज़रूरी है, वह `with` ब्लॉक में रखें।",
        "Jo bhi resource chhodna zaroori hai, woh `with` block me rakho.",
    ),
)

l03 = lesson(
    "m07c02l03",
    L("Reading and writing text files", "टेक्स्ट फ़ाइलें पढ़ना और लिखना", "Text files padhna aur likhna"),
    [],
    L(
        "Text files store characters as bytes using an encoding. `read_text` grabs "
        "the whole file, `splitlines()` turns it into a list of lines, and mode \"a\" "
        "adds to the end instead of replacing.",
        "टेक्स्ट फ़ाइलें एनकोडिंग की मदद से अक्षरों को बाइट्स में रखती हैं। `read_text` "
        "पूरी फ़ाइल लेता है, `splitlines()` उसे पंक्तियों की सूची बनाता है, और मोड "
        "\"a\" बदलने की जगह अंत में जोड़ता है।",
        "Text files encoding ki madad se characters ko bytes me rakhti hain. "
        "`read_text` poori file leta hai, `splitlines()` use lines ki list banata "
        "hai, aur mode \"a\" badalne ki jagah end me jodta hai.",
    ),
    L(
        "A shopping list on the fridge. You write three items, later you add a "
        "fourth at the bottom without rewriting the page.",
        "फ्रिज पर लगी खरीदारी की सूची। आप तीन चीज़ें लिखते हैं, बाद में चौथी नीचे जोड़ते "
        "हैं, पूरा पन्ना दोबारा नहीं लिखते।",
        "Fridge par lagi kharidari ki list. Aap teen cheezein likhte ho, baad me "
        "chouthi neeche jodte ho, poora panna dobara nahi likhte.",
    ),
    "https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects",
    examples=[
        ex(
            'from pathlib import Path\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    path = Path(tmp) / "shopping.txt"\n    path.write_text("milk\\neggs\\nbread\\n", encoding="utf-8")\n    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):\n        print(number, line)',
            "1 milk\n2 eggs\n3 bread",
            L("write_text and splitlines", "write_text और splitlines", "write_text aur splitlines"),
            note=L(
                "`\\n` is one newline character. `splitlines()` removes it and gives "
                "you clean lines to loop over.",
                "`\\n` एक न्यूलाइन अक्षर है। `splitlines()` उसे हटाकर साफ़ पंक्तियाँ "
                "देता है जिन पर लूप चला सकें।",
                "`\\n` ek newline character hai. `splitlines()` use hata kar saaf "
                "lines deta hai jin par loop chala sako.",
            ),
        ),
        ex(
            'from pathlib import Path\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    path = Path(tmp) / "notes.txt"\n    path.write_text("first\\n", encoding="utf-8")\n    with path.open("a", encoding="utf-8") as handle:\n        handle.write("second\\n")\n    print(path.read_text(encoding="utf-8").strip().replace("\\n", " | "))',
            "first | second",
            L("append instead of overwrite", "बदलने की जगह जोड़ना", "badalne ki jagah jodna"),
            note=L(
                'Mode "a" keeps what is already there. Mode "w" would have left only '
                "`second`.",
                'मोड "a" पुरानी सामग्री रखता है। मोड "w" सिर्फ़ `second` छोड़ता।',
                'Mode "a" purani content rakhta hai. Mode "w" sirf `second` chhodta.',
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Create a file with the lines `one`, `two`, `three`, read it back and "
                "print how many lines it has.",
                "`one`, `two`, `three` पंक्तियों वाली फ़ाइल बनाएँ, वापस पढ़ें और बताएँ "
                "कि कितनी पंक्तियाँ हैं।",
                "`one`, `two`, `three` lines wali file banao, wapas padho aur batao "
                "kitni lines hain.",
            ),
            "from pathlib import Path\nimport tempfile\n\n# with tempfile.TemporaryDirectory() as tmp:\n#     ...\n",
            'from pathlib import Path\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    path = Path(tmp) / "lines.txt"\n    path.write_text("one\\ntwo\\nthree\\n", encoding="utf-8")\n    lines = path.read_text(encoding="utf-8").splitlines()\n\nprint(len(lines))',
            [
                "lines == ['one', 'two', 'three']",
                "len(lines) == 3",
                "printed.strip() == '3'",
            ],
            L(
                "write_text with \\n between the words, then splitlines().",
                "शब्दों के बीच \\n डालकर write_text, फिर splitlines()।",
                "Shabdon ke beech \\n daal kar write_text, phir splitlines().",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does splitlines() return?",
                "splitlines() क्या लौटाता है?",
                "splitlines() kya return karta hai?",
            ),
            [
                "one string with \\n removed",
                "a list of lines without the newline characters",
                "a list of characters",
                "the number of lines",
            ],
            "b",
            L(
                "You get a list, one item per line, and the trailing \\n is gone.",
                "आपको सूची मिलती है, हर पंक्ति एक आइटम, और अंत का \\n हट जाता है।",
                "Aapko list milti hai, har line ek item, aur end ka \\n hat jata hai.",
            ),
        ),
        quiz(
            L(
                "You open a file with mode \"w\" that already has text. What happens?",
                "जिस फ़ाइल में पहले से टेक्स्ट है उसे मोड \"w\" से खोलते हैं। क्या होता है?",
                "Jis file me pehle se text hai use mode \"w\" se kholte hain. Kya hota hai?",
            ),
            [
                "the old text stays and new text is added",
                "the old text is erased",
                "Python raises FileExistsError",
                "the file is opened read-only",
            ],
            "b",
            L(
                '"w" means write from scratch. Use "a" when you want to keep the old '
                "content.",
                '"w" का मतलब शुरू से लिखना। पुरानी सामग्री रखनी हो तो "a" इस्तेमाल करें।',
                '"w" ka matlab shuru se likhna. Purani content rakhni ho to "a" use karo.',
            ),
        ),
        quiz(
            L(
                "Why does this course always name the encoding?",
                "यह कोर्स हमेशा एनकोडिंग क्यों लिखता है?",
                "Ye course hamesha encoding kyun likhta hai?",
            ),
            [
                "it is required by the open() signature",
                "the platform default can differ, which corrupts non-English text",
                "it makes files smaller",
                "it locks the file",
            ],
            "b",
            L(
                "UTF-8 is the safe common choice; leaving it out invites mojibake on "
                "Windows.",
                "UTF-8 सुरक्षित साझा विकल्प है; छोड़ने पर Windows पर अक्षर बिगड़ सकते हैं।",
                "UTF-8 safe common choice hai; chhodne par Windows par characters bigad "
                "sakte hain.",
            ),
        ),
    ],
    takeaway=L(
        "Name the encoding, prefer write_text/read_text for small files, and use \"a\" to add without erasing.",
        "एनकोडिंग लिखें, छोटी फ़ाइलों के लिए write_text/read_text रखें, और मिटाए बिना जोड़ने के लिए \"a\"।",
        "Encoding likho, chhoti files ke liye write_text/read_text rakho, aur mitaye bina jodne ke liye \"a\".",
    ),
)

l04 = lesson(
    "m07c02l04",
    L("JSON and paths", "JSON और पाथ", "JSON aur paths"),
    [],
    L(
        "JSON is plain text that both Python and every web API understand: objects "
        "become dicts, arrays become lists, and numbers, strings, true/false/null map "
        "to the obvious Python values. `pathlib` builds file paths without string "
        "concatenation.",
        "JSON सादा टेक्स्ट है जिसे पायथन और हर वेब API समझते हैं: ऑब्जेक्ट dict बनते "
        "हैं, ऐरे list, और नंबर, स्ट्रिंग, true/false/null सीधे संबंधित पायथन मान। "
        "`pathlib` स्ट्रिंग जोड़े बिना फ़ाइल पाथ बनाता है।",
        "JSON saada text hai jise Python aur har web API samajhte hain: objects dict "
        "bante hain, arrays list, aur numbers, strings, true/false/null seedhe "
        "sambandhit Python value. `pathlib` string jode bina file path banata hai.",
    ),
    L(
        "A courier label. The parcel inside can be anything, but the label follows "
        "one standard so every sorting office can read it - that is JSON for data.",
        "कूरियर का लेबल। अंदर का पार्सल कुछ भी हो सकता है, पर लेबल एक मानक मानता है "
        "ताकि हर कार्यालय पढ़ सके - डेटा के लिए यही JSON है।",
        "Courier ka label. Andar ka parcel kuch bhi ho sakta hai, par label ek "
        "standard manta hai taaki har office padh sake - data ke liye yahi JSON hai.",
    ),
    "https://docs.python.org/3/library/json.html",
    examples=[
        ex(
            'import json\n\nprofile = {"name": "Asha", "level": 3, "topics": ["loops", "files"]}\nprint(json.dumps(profile, sort_keys=True))',
            '{"level": 3, "name": "Asha", "topics": ["loops", "files"]}',
            L("dict to JSON text", "dict से JSON टेक्स्ट", "dict se JSON text"),
            note=L(
                "`dumps` returns a string. `sort_keys=True` makes the output stable, "
                "which is what you want in tests and diffs.",
                "`dumps` स्ट्रिंग लौटाता है। `sort_keys=True` आउटपुट स्थिर रखता है, जो "
                "टेस्ट और diff में चाहिए।",
                "`dumps` string return karta hai. `sort_keys=True` output stable "
                "rakhta hai, jo test aur diff me chahiye.",
            ),
        ),
        ex(
            'import json\n\nraw = \'{"user": "ravi", "points": 12}\'\ndata = json.loads(raw)\nprint(data["user"], data["points"] + 8)\nprint(len(json.loads("[]")))',
            "ravi 20\n0",
            L("JSON text to dict", "JSON टेक्स्ट से dict", "JSON text se dict"),
            note=L(
                "`loads` parses text into Python objects. Numbers come back as int or "
                "float, so normal arithmetic works immediately.",
                "`loads` टेक्स्ट को पायथन ऑब्जेक्ट में बदलता है। नंबर int या float "
                "बनकर आते हैं, इसलिए सामान्य गणित सीधे चलता है।",
                "`loads` text ko Python object me badalta hai. Numbers int ya float "
                "bankar aate hain, isliye normal arithmetic seedhe chalta hai.",
            ),
        ),
        ex(
            'from pathlib import Path\nimport tempfile\n\nwith tempfile.TemporaryDirectory() as tmp:\n    folder = Path(tmp) / "data"\n    folder.mkdir()\n    target = folder / "progress.json"\n    target.write_text("{}", encoding="utf-8")\n    print(target.name)\n    print(target.parent.name)\n    print(target.exists())',
            "progress.json\ndata\nTrue",
            L("pathlib builds paths", "pathlib पाथ बनाता है", "pathlib path banata hai"),
            note=L(
                "The `/` operator joins path parts. `.name`, `.parent` and `.exists()` "
                "read the path instead of guessing with string slicing.",
                "`/` ऑपरेटर पाथ के हिस्से जोड़ता है। `.name`, `.parent` और `.exists()` "
                "स्ट्रिंग काटने की जगह पाथ पढ़ते हैं।",
                "`/` operator path ke hisse jodta hai. `.name`, `.parent` aur "
                "`.exists()` string kaatne ki jagah path padhte hain.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Build `record = {\"name\": \"PyBook\", \"lessons\": 53}`, write it to a "
                "temporary file with `json.dump`, load it back and print the name.",
                "`record = {\"name\": \"PyBook\", \"lessons\": 53}` बनाएँ, उसे `json.dump` "
                "से अस्थायी फ़ाइल में लिखें, वापस लोड करें और name प्रिंट करें।",
                "`record = {\"name\": \"PyBook\", \"lessons\": 53}` banao, use "
                "`json.dump` se temporary file me likho, wapas load karo aur name print karo.",
            ),
            "import json\nfrom pathlib import Path\nimport tempfile\n\nrecord = {\"name\": \"PyBook\", \"lessons\": 53}\n# ...\n",
            'import json\nfrom pathlib import Path\nimport tempfile\n\nrecord = {"name": "PyBook", "lessons": 53}\n\nwith tempfile.TemporaryDirectory() as tmp:\n    path = Path(tmp) / "record.json"\n    with path.open("w", encoding="utf-8") as handle:\n        json.dump(record, handle)\n    with path.open(encoding="utf-8") as handle:\n        loaded = json.load(handle)\n\nprint(loaded["name"])',
            [
                "loaded == record",
                "loaded['lessons'] == 53",
                "printed.strip() == 'PyBook'",
            ],
            L(
                "json.dump writes to a file handle; json.dumps returns a string.",
                "json.dump फ़ाइल हैंडल में लिखता है; json.dumps स्ट्रिंग लौटाता है।",
                "json.dump file handle me likhta hai; json.dumps string return karta hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which pair converts between Python objects and JSON text?",
                "पायथन ऑब्जेक्ट और JSON टेक्स्ट के बीच कौन बदलता है?",
                "Python object aur JSON text ke beech kaun badalta hai?",
            ),
            ["dumps / loads", "encode / decode", "write / read", "dump / parse"],
            "a",
            L(
                "`dumps` = dump string, `loads` = load string. The file versions drop "
                "the s.",
                "`dumps` = dump string, `loads` = load string. फ़ाइल वाले रूप में s "
                "हट जाता है।",
                "`dumps` = dump string, `loads` = load string. File wale roop me s hat "
                "jata hai.",
            ),
        ),
        quiz(
            L(
                "What does JSON `null` become in Python?",
                "JSON का `null` पायथन में क्या बनता है?",
                "JSON ka `null` Python me kya banta hai?",
            ),
            ["0", "None", "False", '""'],
            "b",
            L(
                "null maps to None; true/false map to True/False.",
                "null None बनता है; true/false True/False बनते हैं।",
                "null None banta hai; true/false True/False bante hain.",
            ),
        ),
        quiz(
            L(
                "Why prefer `Path(\"a\") / \"b.txt\"` over `\"a\" + \"/\" + \"b.txt\"`?",
                "`Path(\"a\") / \"b.txt\"` को `\"a\" + \"/\" + \"b.txt\"` से बेहतर क्यों?",
                "`Path(\"a\") / \"b.txt\"` ko `\"a\" + \"/\" + \"b.txt\"` se behtar kyun?",
            ),
            [
                "it is faster",
                "it uses the right separator for the operating system",
                "it creates the file",
                "it works only on Windows",
            ],
            "b",
            L(
                "pathlib handles Windows backslashes and POSIX slashes for you, and "
                "gives you .name, .parent, .suffix for free.",
                "pathlib Windows के बैकस्लैश और POSIX के स्लैश संभालता है, और .name, "
                ".parent, .suffix मुफ़्त देता है।",
                "pathlib Windows ke backslash aur POSIX ke slash sambhalta hai, aur "
                ".name, .parent, .suffix muft deta hai.",
            ),
        ),
    ],
    takeaway=L(
        "JSON for structured text, pathlib for paths: two stdlib modules that replace a lot of fragile string code.",
        "संरचित टेक्स्ट के लिए JSON, पाथ के लिए pathlib: दो stdlib मॉड्यूल जो बहुत सारा नाज़ुक स्ट्रिंग कोड बदल देते हैं।",
        "Structured text ke liye JSON, path ke liye pathlib: do stdlib modules jo bahut saara fragile string code badal dete hain.",
    ),
)

MODULE = module(
    M,
    L("Modules, Imports and Files", "मॉड्यूल, इम्पोर्ट और फ़ाइलें", "Modules, Imports aur Files"),
    L(
        "Reuse code with import/from/as, release resources with with, and keep data "
        "on disk as text, JSON and paths.",
        "import/from/as से कोड दोबारा इस्तेमाल करें, with से संसाधन छोड़ें, और डेटा "
        "डिस्क पर टेक्स्ट, JSON और पाथ के रूप में रखें।",
        "import/from/as se code dobara use karo, with se resources chhodo, aur data "
        "disk par text, JSON aur path ke roop me rakho.",
    ),
    [
        chapter("m07c01", L("Modules and cleanup", "मॉड्यूल और सफ़ाई", "Modules aur cleanup"), [l01, l02]),
        chapter("m07c02", L("Data on disk", "डिस्क पर डेटा", "Disk par data"), [l03, l04]),
    ],
    exam=[
        quiz(
            L("Which import keeps the module prefix?", "कौन सा import मॉड्यूल उपसर्ग रखता है?", "Kaun sa import module prefix rakhta hai?"),
            ["from math import pi", "import math", "import pi from math", "from math as pi"],
            "b",
            L("Only plain `import math` keeps `math.` in front of every name.", "सिर्फ़ सादा `import math` हर नाम के आगे `math.` रखता है।", "Sirf saada `import math` har naam ke aage `math.` rakhta hai."),
        ),
        quiz(
            L("What is the mode to add text at the end of a file?", "फ़ाइल के अंत में टेक्स्ट जोड़ने का मोड?", "File ke end me text jodne ka mode?"),
            ['"r"', '"w"', '"a"', '"x"'],
            "c",
            L('"a" appends and creates the file if needed.', '"a" जोड़ता है और ज़रूरत हो तो फ़ाइल बनाता है।', '"a" jodta hai aur zaroorat ho to file banata hai.'),
        ),
        quiz(
            L("Which function turns a dict into a JSON string?", "dict को JSON स्ट्रिंग में कौन बदलता है?", "dict ko JSON string me kaun badalta hai?"),
            ["json.load", "json.loads", "json.dump", "json.dumps"],
            "d",
            L("dumps = dump to string. load/loads go the other way.", "dumps = string में dump। load/loads उलटी दिशा हैं।", "dumps = string me dump. load/loads ulti disha hain."),
        ),
        quiz(
            L("What happens to a file opened in a `with` block when the block ends?", "with ब्लॉक खत्म होने पर फ़ाइल का क्या होता है?", "with block khatam hone par file ka kya hota hai?"),
            ["it stays open until the program ends", "it is closed automatically", "it is deleted", "it is copied to disk"],
            "b",
            L("The context manager closes it on the way out, including on errors.", "कॉन्टेक्स्ट मैनेजर निकास पर उसे बंद करता है, एरर पर भी।", "Context manager nikaas par use band karta hai, error par bhi."),
        ),
        quiz(
            L("Which path builds `data/progress.json` portably?", "कौन सा पाथ `data/progress.json` पोर्टेबल बनाता है?", "Kaun sa path `data/progress.json` portable banata hai?"),
            ['Path("data") + "progress.json"', 'Path("data") / "progress.json"', 'Path("data").join("progress.json")', 'Path("data" + "/" + "progress.json")'],
            "b",
            L("The `/` operator on Path joins parts with the platform separator.", "Path पर `/` ऑपरेटर प्लेटफ़ॉर्म विभाजक से हिस्से जोड़ता है।", "Path par `/` operator platform separator se hisse jodta hai."),
        ),
        quiz(
            L("Which is the safest way to read a small UTF-8 file?", "छोटी UTF-8 फ़ाइल पढ़ने का सुरक्षित तरीका?", "Chhoti UTF-8 file padhne ka safe tarika?"),
            ['open(p).read()', 'Path(p).read_text(encoding="utf-8")', 'p.read()', 'open(p, "rb").read()'],
            "b",
            L("read_text names the encoding and closes the file for you.", "read_text एनकोडिंग लिखता है और फ़ाइल बंद कर देता है।", "read_text encoding likhta hai aur file band kar deta hai."),
        ),
    ],
    icon="📦",
)
