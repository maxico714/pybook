"""Module 3 - Decisions and Loops."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m03"

l01 = lesson(
    "m03c01l01",
    L("if, elif, else", "if, elif, else", "if, elif, else"),
    ["if", "elif", "else"],
    L(
        "An if statement runs a block only when its condition is true. elif adds "
        "another question, and else catches everything left over. Exactly one "
        "branch of a chain runs.",
        "if ब्लॉक तभी चलता है जब उसकी शर्त सच हो। elif दूसरा सवाल जोड़ता है, और "
        "else बाकी सब पकड़ लेता है। चेन में ठीक एक शाखा चलती है।",
        "if block tabhi chalta hai jab uski condition sach ho. elif doosra sawaal "
        "jodta hai, aur else baaki sab pakad leta hai. Chain me exactly ek branch chalti hai.",
    ),
    L(
        "Grading a paper: 90+ is A, 70+ is B, 50+ is C, anything lower is \"try "
        "again\". Python checks from the top and stops at the first true condition, "
        "so the order of the questions matters.",
        "पेपर जाँचना: 90+ पर A, 70+ पर B, 50+ पर C, उससे कम पर \"फिर कोशिश करो\"। "
        "पायथन ऊपर से जाँचता है और पहली सच शर्त पर रुक जाता है, इसलिए सवालों का "
        "क्रम मायने रखता है।",
        "Paper check karna: 90+ par A, 70+ par B, 50+ par C, usse kam par \"phir "
        "koshish karo\". Python upar se check karta hai aur pehli true condition par "
        "ruk jata hai, isliye sawaalon ka order matter karta hai.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#if-statements",
    visual="if_flow",
    examples=[
        ex(
            'marks = 72\nif marks >= 90:\n    print("A")\nelif marks >= 70:\n    print("B")\nelif marks >= 50:\n    print("C")\nelse:\n    print("Try again")',
            "B",
            L("a grading chain", "ग्रेडिंग चेन", "grading chain"),
            note=L(
                "Only 'B' prints. Once a branch runs, the rest of the chain is skipped.",
                "सिर्फ़ 'B' प्रिंट होता है। एक शाखा चलने पर बाकी चेन छोड़ दी जाती है।",
                "Sirf 'B' print hota hai. Ek branch chalne par baaki chain chhod di jati hai.",
            ),
        ),
        ex(
            'items = []\nif items:\n    print("we have items")\nelse:\n    print("empty cart")\n\nname = ""\nprint("guest" if not name else name)',
            "empty cart\nguest",
            L("truthiness and a one-line if", "सत्यता और एक-लाइन if", "truthiness aur one-line if"),
            note=L(
                "`a if condition else b` picks one of two values without a full block.",
                "`a if condition else b` पूरे ब्लॉक के बिना दो में से एक वैल्यू चुनता है।",
                "`a if condition else b` poore block ke bina do me se ek value chunta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Print 'positive', 'negative' or 'zero' for n = -4. Use if/elif/else.",
                "n = -4 के लिए 'positive', 'negative' या 'zero' प्रिंट करें। "
                "if/elif/else इस्तेमाल करें।",
                "n = -4 ke liye 'positive', 'negative' ya 'zero' print karo. "
                "if/elif/else use karo.",
            ),
            "n = -4\n# if ...\n",
            'n = -4\nif n > 0:\n    print("positive")\nelif n < 0:\n    print("negative")\nelse:\n    print("zero")',
            ['printed.strip() == "negative"'],
            L("Three cases: greater than 0, less than 0, and neither.", "तीन केस: 0 से बड़ा, 0 से छोटा, और न तो।", "Teen cases: 0 se bada, 0 se chhota, aur na to."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "x = 5; if x > 10: print('big') elif x > 3: print('medium') else: "
                "print('small'). What prints?",
                "x = 5; if x > 10: print('big') elif x > 3: print('medium') else: "
                "print('small')। क्या प्रिंट होगा?",
                "x = 5; if x > 10: print('big') elif x > 3: print('medium') else: "
                "print('small'). Kya print hoga?",
            ),
            ["big", "medium", "small", "nothing"],
            "b",
            L(
                "5 > 10 is false, so Python tries the elif. 5 > 3 is true, so it prints "
                "'medium' and skips the else.",
                "5 > 10 गलत है, इसलिए पायथन elif आज़माता है। 5 > 3 सही है, इसलिए "
                "'medium' प्रिंट होता है और else छूट जाता है।",
                "5 > 10 false hai, isliye Python elif try karta hai. 5 > 3 true hai, "
                "isliye 'medium' print hota hai aur else chhoot jata hai.",
            ),
        ),
        quiz(
            L(
                "Why does this print nothing? if 0: print('yes')",
                "यह कुछ क्यों नहीं प्रिंट करता? if 0: print('yes')",
                "Ye kuch kyun nahi print karta? if 0: print('yes')",
            ),
            [
                "because 0 is falsy",
                "because 0 is not a number",
                "because print is misspelled",
                "it does print yes",
            ],
            "a",
            L(
                "if does not require True: any value is tested for truthiness. 0, "
                "0.0, '', [], {} and None are all falsy.",
                "if को True नहीं चाहिए: हर वैल्यू की सत्यता जाँची जाती है। 0, 0.0, '', "
                "[], {} और None सब falsy हैं।",
                "if ko True nahi chahiye: har value ki truthiness check hoti hai. 0, "
                "0.0, '', [], {} aur None sab falsy hain.",
            ),
            "truthiness",
        ),
        quiz(
            L(
                "What is wrong with: if x = 5: print('five')",
                "इसमें क्या गलत है: if x = 5: print('five')",
                "Isme kya galat hai: if x = 5: print('five')",
            ),
            [
                "nothing, it prints five",
                "assignment needs == for comparison",
                "print cannot be inside if",
                "5 must be quoted",
            ],
            "b",
            L(
                "A single = assigns, so the condition has no value to test. Python "
                "raises a SyntaxError and points at the =.",
                "अकेला = असाइन करता है, इसलिए शर्त के पास जाँचने को वैल्यू नहीं होती। "
                "पायथन SyntaxError देता है और = की ओर इशारा करता है।",
                "Akela = assign karta hai, isliye condition ke paas check karne ko "
                "value nahi hoti. Python SyntaxError deta hai aur = ki taraf ishara karta hai.",
            ),
            "assign-vs-compare",
        ),
    ],
    takeaway=L(
        "First true branch wins; else is optional; any value can be a condition.",
        "पहली सच शाखा जीतती है; else वैकल्पिक है; कोई भी वैल्यू शर्त बन सकती है।",
        "Pehli true branch jeetti hai; else optional hai; koi bhi value condition ban sakti hai.",
    ),
)

l02 = lesson(
    "m03c01l02",
    L("match and case", "match और case", "match aur case"),
    ["match", "case", "_"],
    L(
        "match compares one value against several patterns and runs the first one "
        "that fits. It is not a switch statement: patterns can unpack tuples, "
        "check types and bind names.",
        "match एक वैल्यू की कई पैटर्न से तुलना करता है और पहला मेल खाने वाला चलाता है। "
        "यह switch नहीं है: पैटर्न ट्यूपल खोल सकते हैं, टाइप जाँच सकते हैं और नाम "
        "बाँध सकते हैं।",
        "match ek value ki kai patterns se tulna karta hai aur pehla match chalata "
        "hai. Ye switch nahi hai: patterns tuple khol sakte hain, type check kar "
        "sakte hain aur naam bind kar sakte hain.",
    ),
    L(
        "A TV remote has a few buttons. Press \"start\" it plays, \"stop\" it stops, "
        "anything else shows \"unknown button\". match is exactly that: one value, "
        "a list of shapes it might have, one action each.",
        "टीवी रिमोट में कुछ बटन हैं। \"start\" दबाओ तो चलता है, \"stop\" दबाओ तो रुकता "
        "है, बाकी कुछ भी दबाओ तो \"unknown button\"। match ठीक यही है: एक वैल्यू, "
        "उसके संभावित रूपों की लिस्ट, हर एक के लिए एक काम।",
        "TV remote me kuch buttons hain. \"start\" dabao to chalta hai, \"stop\" dabao "
        "to rukta hai, baaki kuch bhi dabao to \"unknown button\". match exactly yahi "
        "hai: ek value, uske possible shapes ki list, har ek ke liye ek kaam.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#match-statements",
    examples=[
        ex(
            'command = "start"\nmatch command:\n    case "start":\n        print("Starting...")\n    case "stop":\n        print("Stopping.")\n    case _:\n        print("Unknown command")',
            "Starting...",
            L("matching text", "टेक्स्ट मैच करना", "text match karna"),
            note=L(
                "case _ is the catch-all. Without it, an unmatched value simply does "
                "nothing.",
                "case _ सब कुछ पकड़ता है। इसके बिना बिना-मेल वैल्यू पर कुछ नहीं होता।",
                "case _ sab kuch pakadta hai. Iske bina unmatched value par kuch nahi hota.",
            ),
        ),
        ex(
            "point = (0, 5)\nmatch point:\n    case (0, 0):\n        print(\"origin\")\n    case (0, y):\n        print(f\"on y axis at {y}\")\n    case (x, 0):\n        print(f\"on x axis at {x}\")\n    case _:\n        print(\"somewhere else\")",
            "on y axis at 5",
            L("unpacking a tuple pattern", "ट्यूपल पैटर्न खोलना", "tuple pattern kholna"),
            note=L(
                "The pattern (0, y) both tests the first item and binds the second to "
                "the name y.",
                "पैटर्न (0, y) पहला आइटम जाँचता है और दूसरे को नाम y से बाँधता है।",
                "Pattern (0, y) pehla item check karta hai aur doosre ko naam y se bind karta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Use match on `status = 404` to print 'not found' for 404, 'ok' for "
                "200, and 'other' otherwise.",
                "`status = 404` पर match इस्तेमाल करें: 404 पर 'not found', 200 पर "
                "'ok', बाकी पर 'other' प्रिंट करें।",
                "`status = 404` par match use karo: 404 par 'not found', 200 par 'ok', "
                "baaki par 'other' print karo.",
            ),
            "status = 404\n# match status:\n",
            'status = 404\nmatch status:\n    case 200:\n        print("ok")\n    case 404:\n        print("not found")\n    case _:\n        print("other")',
            ['printed.strip() == "not found"'],
            L("Numbers match by value, exactly like strings.", "नंबर वैल्यू से मैच करते हैं, स्ट्रिंग की तरह।", "Numbers value se match karte hain, string ki tarah."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which version of Python added match?",
                "match किस पायथन संस्करण में आया?",
                "match kis Python version me aaya?",
            ),
            ["3.8", "3.10", "3.12", "2.7"],
            "b",
            L(
                "match/case arrived in 3.10. On older versions it is a SyntaxError, "
                "which is worth knowing when you share code.",
                "match/case 3.10 में आया। पुराने संस्करणों पर यह SyntaxError है, जो "
                "कोड साझा करते समय जानना ज़रूरी है।",
                "match/case 3.10 me aaya. Purane versions par ye SyntaxError hai, jo "
                "code share karte samay jaanna zaroori hai.",
            ),
        ),
        quiz(
            L(
                "What happens if no case matches and there is no case _?",
                "अगर कोई case मेल न खाए और case _ भी न हो तो?",
                "Agar koi case match na kare aur case _ bhi na ho to?",
            ),
            [
                "an error is raised",
                "nothing happens",
                "the first case runs",
                "None is returned",
            ],
            "b",
            L(
                "match with no matching case does nothing at all — it is not like an "
                "if chain without else, and it raises nothing.",
                "बिना मेल वाले case पर match कुछ नहीं करता — यह बिना else वाली if चेन "
                "जैसा नहीं है, और कोई एरर नहीं देता।",
                "Bina match wale case par match kuch nahi karta - ye bina else wali if "
                "chain jaisa nahi hai, aur koi error nahi deta.",
            ),
        ),
        quiz(
            L(
                "In `case (0, y):`, what is y?",
                "`case (0, y):` में y क्या है?",
                "`case (0, y):` me y kya hai?",
            ),
            [
                "a constant that must equal 'y'",
                "a name bound to the second item of the tuple",
                "a syntax error",
                "the number of items",
            ],
            "b",
            L(
                "A bare name in a pattern captures. A name with a dot (like "
                "Colour.RED) is compared as a value instead.",
                "पैटर्न में सादा नाम कैप्चर करता है। डॉट वाला नाम (जैसे Colour.RED) "
                "वैल्यू की तरह तुलना होता है।",
                "Pattern me saada naam capture karta hai. Dot wala naam (jaise "
                "Colour.RED) value ki tarah compare hota hai.",
            ),
        ),
    ],
    takeaway=L(
        "match picks the first fitting pattern; case _ is the safe catch-all.",
        "match पहला फ़िटिंग पैटर्न चुनता है; case _ सुरक्षित कैच-ऑल है।",
        "match pehla fitting pattern chunta hai; case _ safe catch-all hai.",
    ),
)

l03 = lesson(
    "m03c02l03",
    L("while, break, continue, pass", "while, break, continue, pass", "while, break, continue, pass"),
    ["while", "break", "continue", "pass"],
    L(
        "while repeats a block as long as its condition stays true. break leaves "
        "the loop immediately, continue jumps to the next round, and pass is a "
        "do-nothing placeholder that keeps the syntax valid.",
        "while तब तक ब्लॉक दोहराता है जब तक शर्त सच रहे। break लूप से तुरंत बाहर "
        "निकलता है, continue अगले चक्कर पर कूदता है, और pass कुछ न करने वाला "
        "प्लेसहोल्डर है जो सिंटैक्स सही रखता है।",
        "while tab tak block dohrata hai jab tak condition sach rahe. break loop se "
        "turant bahar nikalta hai, continue agle chakkar par koodta hai, aur pass "
        "kuch na karne wala placeholder hai jo syntax sahi rakhta hai.",
    ),
    L(
        "A lift door: while someone is still walking in, keep the door open. If the "
        "door sensor breaks (break), stop waiting. If the person says \"not this "
        "lift\", skip them (continue) and keep waiting for others.",
        "लिफ़्ट का दरवाज़ा: जब तक कोई अंदर आ रहा है, दरवाज़ा खुला रखो। अगर सेंसर "
        "ख़राब हो (break) तो इंतज़ार बंद। अगर कोई कहे \"यह लिफ़्ट नहीं\" (continue) "
        "तो उसे छोड़कर बाकी का इंतज़ार करो।",
        "Lift ka darwaza: jab tak koi andar aa raha hai, darwaza khula rakho. Agar "
        "sensor kharab ho (break) to intezaar band. Agar koi kahe \"ye lift nahi\" "
        "(continue) to use chhodkar baaki ka intezaar karo.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#break-and-continue-statements",
    visual="loop_flow",
    examples=[
        ex(
            'n = 3\nwhile n > 0:\n    print(n)\n    n -= 1\nprint("liftoff")',
            "3\n2\n1\nliftoff",
            L("counting down", "उल्टी गिनती", "ulti ginti"),
            note=L(
                "Forgetting n -= 1 makes the condition true forever: an infinite loop.",
                "n -= 1 भूलने पर शर्त हमेशा सच रहती है: अनंत लूप।",
                "n -= 1 bhoolne par condition hamesha true rehti hai: infinite loop.",
            ),
        ),
        ex(
            "for n in range(1, 10):\n    if n == 3:\n        continue\n    if n == 6:\n        break\n    print(n)",
            "1\n2\n4\n5",
            L("continue then break", "पहले continue फिर break", "pehle continue phir break"),
            note=L(
                "3 is skipped by continue; 6 stops the loop before printing.",
                "3 को continue छोड़ देता है; 6 प्रिंट होने से पहले लूप रोक देता है।",
                "3 ko continue chhod deta hai; 6 print hone se pehle loop rok deta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Print the numbers 1 to 5 using a while loop.",
                "while लूप से 1 से 5 तक नंबर प्रिंट करें।",
                "while loop se 1 se 5 tak numbers print karo.",
            ),
            "n = 1\n# while ...\n",
            'n = 1\nwhile n <= 5:\n    print(n)\n    n += 1',
            ['printed.split() == ["1", "2", "3", "4", "5"]'],
            L("Change the condition inside the loop, or it never ends.", "लूप के अंदर शर्त बदलें, वरना वह कभी ख़त्म नहीं होगा।", "Loop ke andar condition badlo, warna woh kabhi khatam nahi hoga."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What is the main risk of a while loop?",
                "while लूप का मुख्य ख़तरा क्या है?",
                "while loop ka main khatra kya hai?",
            ),
            [
                "it runs at most once",
                "the condition may never become false",
                "it cannot use break",
                "it needs a list",
            ],
            "b",
            L(
                "If nothing inside the loop changes the condition, it runs forever. "
                "A for loop over a fixed sequence cannot do that.",
                "अगर लूप के अंदर कुछ शर्त नहीं बदलता, तो वह हमेशा चलता है। तय "
                "सीक्वेंस वाला for लूप ऐसा नहीं कर सकता।",
                "Agar loop ke andar kuch condition nahi badalta, to woh hamesha chalta "
                "hai. Fixed sequence wala for loop aisa nahi kar sakta.",
            ),
        ),
        quiz(
            L(
                "What does continue do?",
                "continue क्या करता है?",
                "continue kya karta hai?",
            ),
            [
                "stops the loop entirely",
                "skips the rest of this round and goes to the next",
                "restarts the program",
                "does nothing",
            ],
            "b",
            L(
                "continue jumps to the next iteration. break would leave the loop.",
                "continue अगले चक्कर पर कूदता है। break लूप छोड़ देता है।",
                "continue agle iteration par koodta hai. break loop chhod deta hai.",
            ),
        ),
        quiz(
            L(
                "When is pass useful?",
                "pass कब काम आता है?",
                "pass kab kaam aata hai?",
            ),
            [
                "to skip the rest of a loop",
                "as a placeholder where a block is required but nothing should happen",
                "to end the program",
                "to return None",
            ],
            "b",
            L(
                "Python needs at least one statement in every block. pass satisfies "
                "that while you are still writing the code.",
                "पायथन को हर ब्लॉक में कम से कम एक स्टेटमेंट चाहिए। जब आप कोड लिख "
                "रहे हों, pass वह शर्त पूरी करता है।",
                "Python ko har block me kam se kam ek statement chahiye. Jab aap code "
                "likh rahe ho, pass woh shart poori karta hai.",
            ),
        ),
    ],
    takeaway=L(
        "while needs its condition to change; break exits, continue skips, pass waits.",
        "while की शर्त बदलनी चाहिए; break बाहर, continue छोड़ता, pass रुकता है।",
        "while ki condition badalni chahiye; break bahar, continue chhodta, pass rukta hai.",
    ),
)

l04 = lesson(
    "m03c02l04",
    L("for, range, enumerate, zip", "for, range, enumerate, zip", "for, range, enumerate, zip"),
    ["for", "in"],
    L(
        "for walks over a sequence one item at a time. range() produces numbers "
        "without building a list, enumerate() adds a counter, and zip() walks two "
        "sequences side by side.",
        "for सीक्वेंस पर एक-एक आइटम चलता है। range() बिना लिस्ट बनाए नंबर देता है, "
        "enumerate() काउंटर जोड़ता है, और zip() दो सीक्वेंस साथ-साथ चलाता है।",
        "for sequence par ek-ek item chalta hai. range() bina list banaye numbers "
        "deta hai, enumerate() counter jodta hai, aur zip() do sequences saath-saath chalata hai.",
    ),
    L(
        "Checking attendance: go through the register name by name. enumerate is the "
        "roll number plus the name. zip is matching the name list with the marks list, "
        "line by line.",
        "हाज़िरी जाँचना: रजिस्टर में नाम-दर-नाम जाओ। enumerate = रोल नंबर + नाम। "
        "zip = नाम की लिस्ट और नंबर की लिस्ट को लाइन-दर-लाइन मिलाना।",
        "Attendance check karna: register me naam-dar-naam jao. enumerate = roll "
        "number + naam. zip = naam ki list aur marks ki list ko line-dar-line milana.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#for-statements",
    visual="loop_flow",
    examples=[
        ex(
            'for i in range(3):\n    print("round", i)\nprint(list(range(2, 10, 3)))',
            "round 0\nround 1\nround 2\n[2, 5, 8]",
            L("range with start, stop, step", "range: शुरू, अंत, कदम", "range: start, stop, step"),
            note=L(
                "range(2, 10, 3) starts at 2 and adds 3 until it would reach 10, so it "
                "stops at 8.",
                "range(2, 10, 3) 2 से शुरू होकर 3 जोड़ता है जब तक 10 तक पहुँचे, इसलिए "
                "8 पर रुकता है।",
                "range(2, 10, 3) 2 se shuru hokar 3 jodta hai jab tak 10 tak pahunche, "
                "isliye 8 par rukta hai.",
            ),
        ),
        ex(
            'names = ["Asha", "Ravi"]\nscores = [91, 78]\nfor i, (name, score) in enumerate(zip(names, scores), start=1):\n    print(f"{i}. {name}: {score}")',
            "1. Asha: 91\n2. Ravi: 78",
            L("two lists at once", "एक साथ दो लिस्ट", "ek saath do lists"),
        ),
    ],
    exercises=[
        task(
            L(
                "Print the squares of 1 to 5 using a for loop and range().",
                "for लूप और range() से 1 से 5 तक के वर्ग प्रिंट करें।",
                "for loop aur range() se 1 se 5 tak ke squares print karo.",
            ),
            "# for n in range(...):\n#     print(...)\n",
            "for n in range(1, 6):\n    print(n * n)",
            ['printed.split() == ["1", "4", "9", "16", "25"]'],
            L("range(1, 6) gives 1,2,3,4,5 — 6 is excluded.", "range(1, 6) 1,2,3,4,5 देता है — 6 शामिल नहीं।", "range(1, 6) 1,2,3,4,5 deta hai - 6 include nahi."),
        ),
    ],
    quiz_items=[
        quiz(
            L("What does list(range(3)) give?", "list(range(3)) क्या देता है?", "list(range(3)) kya deta hai?"),
            ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[3]"],
            "b",
            L(
                "range starts at 0 by default and stops before the number you give. "
                "This off-by-one is the most common loop bug.",
                "range डिफ़ॉल्ट 0 से शुरू होता है और दिए नंबर से पहले रुकता है। यह "
                "off-by-one सबसे आम लूप बग है।",
                "range default 0 se shuru hota hai aur diye number se pehle rukta hai. "
                "Ye off-by-one sabse aam loop bug hai.",
            ),
            "range-exclusive",
        ),
        quiz(
            L(
                "What does zip(['a','b'], [1,2]) produce when looped?",
                "zip(['a','b'], [1,2]) लूप में क्या देता है?",
                "zip(['a','b'], [1,2]) loop me kya deta hai?",
            ),
            ["['a', 1, 'b', 2]", "('a', 1) then ('b', 2)", "['ab', '12']", "an error"],
            "b",
            L(
                "zip pairs items position by position and stops at the shorter "
                "sequence.",
                "zip आइटम को जगह-दर-जगह जोड़ता है और छोटी सीक्वेंस पर रुक जाता है।",
                "zip items ko position-dar-position jodta hai aur chhoti sequence par ruk jata hai.",
            ),
        ),
        quiz(
            L(
                "What is wrong here? for i in range(5): print(i) print('done')",
                "यहाँ क्या गलत है? for i in range(5): print(i) print('done')",
                "Yahan kya galat hai? for i in range(5): print(i) print('done')",
            ),
            [
                "nothing, it works",
                "the second print must be indented inside the loop or written on a new line",
                "range cannot be used with print",
                "i is undefined",
            ],
            "b",
            L(
                "On one line after the colon only one simple statement fits. The "
                "second statement needs a new line, and its indentation decides "
                "whether it is inside the loop.",
                "कोलन के बाद एक ही लाइन में सिर्फ़ एक साधारण स्टेटमेंट आता है। दूसरे "
                "के लिए नई लाइन चाहिए, और इंडेंटेशन तय करता है कि वह लूप के अंदर है या नहीं।",
                "Colon ke baad ek hi line me sirf ek simple statement aata hai. Doosre "
                "ke liye nayi line chahiye, aur indentation tay karta hai ki woh loop "
                "ke andar hai ya nahi.",
            ),
            "indentation",
        ),
    ],
    takeaway=L(
        "range stops before its stop value; enumerate counts; zip pairs two sequences.",
        "range अपनी अंत वैल्यू से पहले रुकता है; enumerate गिनता है; zip दो सीक्वेंस जोड़ता है।",
        "range apni stop value se pehle rukta hai; enumerate ginta hai; zip do sequences jodta hai.",
    ),
)

l05 = lesson(
    "m03c02l05",
    L("Nested loops and loop else", "नेस्टेड लूप और loop else", "Nested loops aur loop else"),
    [],
    L(
        "A loop inside a loop runs the inner loop completely for every single turn "
        "of the outer loop. A loop can also carry an else block, which runs only "
        "when the loop finished without hitting break.",
        "लूप के अंदर लूप: बाहरी लूप के हर एक चक्कर के लिए अंदरूनी लूप पूरा चलता है। "
        "लूप के साथ else ब्लॉक भी हो सकता है, जो तभी चलता है जब लूप बिना break के "
        "पूरा हुआ हो।",
        "Loop ke andar loop: bahari loop ke har ek chakkar ke liye andaruni loop "
        "poora chalta hai. Loop ke saath else block bhi ho sakta hai, jo tabhi chalta "
        "hai jab loop bina break ke poora hua ho.",
    ),
    L(
        "A cinema hall: for each row (outer), check each seat (inner). A timetable is "
        "the same shape — rows are days, columns are hours, and every cell is one "
        "meeting.",
        "सिनेमा हॉल: हर पंक्ति (बाहरी) के लिए हर सीट (अंदरूनी) जाँचो। टाइमटेबल भी "
        "वही आकार है — पंक्तियाँ दिन, कॉलम घंटे, और हर सेल एक मीटिंग।",
        "Cinema hall: har row (bahari) ke liye har seat (andaruni) check karo. "
        "Timetable bhi wahi shape hai - rows din, columns ghante, aur har cell ek meeting.",
    ),
    "https://docs.python.org/3/tutorial/controlflow.html#else-clauses-on-loops",
    examples=[
        ex(
            'for row in range(1, 4):\n    for col in range(1, 4):\n        print(f"{row * col:2}", end="")\n    print()',
            " 1 2 3\n 2 4 6\n 3 6 9",
            L("a multiplication table", "पहाड़ा", "pahada"),
            note=L(
                "The inner print uses end=\"\" so nothing breaks the line; the outer "
                "print() ends the row.",
                "अंदरूनी print में end=\"\" है इसलिए लाइन नहीं टूटती; बाहरी print() "
                "पंक्ति ख़त्म करता है।",
                "Andaruni print me end=\"\" hai isliye line nahi tootti; bahari print() "
                "row khatam karta hai.",
            ),
        ),
        ex(
            "for n in [2, 4, 6]:\n    if n % 2:\n        print(\"odd found:\", n)\n        break\nelse:\n    print(\"all even\")",
            "all even",
            L("else runs when there was no break", "break न हो तो else चलता है", "break na ho to else chalta hai"),
            note=L(
                "The else belongs to the for, not to the if. It runs after a complete "
                "loop with no break.",
                "else, for का है, if का नहीं। यह बिना break वाले पूरे लूप के बाद चलता है।",
                "else, for ka hai, if ka nahi. Ye bina break wale poore loop ke baad chalta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Print a 3x3 grid of stars, one row per line, using nested loops.",
                "नेस्टेड लूप से 3x3 स्टार ग्रिड प्रिंट करें, हर पंक्ति अलग लाइन में।",
                "Nested loops se 3x3 star grid print karo, har row alag line me.",
            ),
            "# for row in range(3):\n#     for col in range(3):\n",
            'for row in range(3):\n    for col in range(3):\n        print("*", end="")\n    print()',
            ['printed.split() == ["***", "***", "***"]'],
            L("end=\"\" keeps the stars on one line.", "end=\"\" स्टार एक लाइन में रखता है।", "end=\"\" stars ko ek line me rakhta hai."),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "How many times does the inner body run? for i in range(3): for j in range(4): ...",
                "अंदरूनी बॉडी कितनी बार चलेगी? for i in range(3): for j in range(4): ...",
                "Andaruni body kitni baar chalegi? for i in range(3): for j in range(4): ...",
            ),
            ["4", "7", "12", "3"],
            "c",
            L(
                "3 outer turns × 4 inner turns = 12. Nested loops multiply, they do "
                "not add.",
                "3 बाहरी × 4 अंदरूनी = 12। नेस्टेड लूप गुणा करते हैं, जोड़ते नहीं।",
                "3 bahari × 4 andaruni = 12. Nested loops multiply karte hain, add nahi.",
            ),
        ),
        quiz(
            L(
                "When does a loop's else block run?",
                "लूप का else ब्लॉक कब चलता है?",
                "Loop ka else block kab chalta hai?",
            ),
            [
                "always, after the loop",
                "only if the loop finished without break",
                "only if the loop was empty",
                "never",
            ],
            "b",
            L(
                "This is the one place where else does not mean 'otherwise'. It means "
                "'the loop completed normally'.",
                "यह एक जगह है जहाँ else का मतलब 'वरना' नहीं है। इसका मतलब है 'लूप सामान्य "
                "रूप से पूरा हुआ'।",
                "Ye ek jagah hai jahan else ka matlab 'warna' nahi hai. Iska matlab hai "
                "'loop normally poora hua'.",
            ),
        ),
        quiz(
            L(
                "Why is this an infinite loop? while True: pass",
                "यह अनंत लूप क्यों है? while True: pass",
                "Ye infinite loop kyun hai? while True: pass",
            ),
            [
                "pass restarts the loop",
                "the condition never becomes false",
                "True is not a bool",
                "it is not infinite",
            ],
            "b",
            L(
                "True stays True forever and nothing inside changes it. A break is the "
                "only way out.",
                "True हमेशा True रहता है और अंदर कुछ उसे नहीं बदलता। बाहर निकलने का "
                "एक ही रास्ता break है।",
                "True hamesha True rehta hai aur andar kuch use nahi badalta. Bahar "
                "nikalne ka ek hi rasta break hai.",
            ),
        ),
    ],
    takeaway=L(
        "Nested loops multiply; loop else means 'finished without break'.",
        "नेस्टेड लूप गुणा करते हैं; loop else का मतलब 'बिना break पूरा हुआ'।",
        "Nested loops multiply karte hain; loop else ka matlab 'bina break poora hua'.",
    ),
)

MODULE = module(
    M,
    L("Decisions and Loops", "फ़ैसले और लूप", "Decisions aur Loops"),
    L(
        "Make the program choose with if/elif/else and match, then repeat work with "
        "while and for — including the three statements that change how a loop ends.",
        "if/elif/else और match से प्रोग्राम को चुनने दें, फिर while और for से काम "
        "दोहराएँ — उन तीन स्टेटमेंट के साथ जो लूप का अंत बदलते हैं।",
        "if/elif/else aur match se program ko choose karne do, phir while aur for se "
        "kaam dohrao - un teen statements ke saath jo loop ka end badalte hain.",
    ),
    [
        chapter("m03c01", L("Branching", "शाखाएँ", "Branching"), [l01, l02]),
        chapter("m03c02", L("Loops", "लूप", "Loops"), [l03, l04, l05]),
    ],
    exam=[
        quiz(
            L("What does range(5) produce?", "range(5) क्या देता है?", "range(5) kya deta hai?"),
            ["1,2,3,4,5", "0,1,2,3,4", "0,1,2,3,4,5", "5"],
            "b",
            L("Start 0, stop before 5: five values, 0 to 4.", "शुरू 0, 5 से पहले रुको: पाँच वैल्यू, 0 से 4।", "Start 0, 5 se pehle ruko: paanch values, 0 se 4."),
        ),
        quiz(
            L("What is bool(0.0)?", "bool(0.0) क्या है?", "bool(0.0) kya hai?"),
            ["True", "False", "None", "an error"],
            "b",
            L("Zero of any numeric type is falsy, including 0.0.", "किसी भी न्यूमेरिक टाइप का शून्य falsy है, 0.0 भी।", "Kisi bhi numeric type ka zero falsy hai, 0.0 bhi."),
        ),
        quiz(
            L("How many times does 'hi' print? for i in range(2): for j in range(3): print('hi')", "'hi' कितनी बार प्रिंट होगा? for i in range(2): for j in range(3): print('hi')", "'hi' kitni baar print hoga? for i in range(2): for j in range(3): print('hi')"),
            ["2", "3", "5", "6"],
            "d",
            L("2 × 3 = 6.", "2 × 3 = 6।", "2 × 3 = 6."),
        ),
        quiz(
            L("Which statement leaves a loop immediately?", "कौन सा स्टेटमेंट लूप से तुरंत बाहर निकलता है?", "Kaun sa statement loop se turant bahar nikalta hai?"),
            ["continue", "pass", "break", "return only"],
            "c",
            L("break exits the loop. continue skips one round; pass does nothing.", "break लूप छोड़ता है। continue एक चक्कर छोड़ता है; pass कुछ नहीं करता।", "break loop chhodta hai. continue ek chakkar chhodta hai; pass kuch nahi karta."),
        ),
        quiz(
            L("if a > b: print('A') else: print('B') — when does B print?", "if a > b: print('A') else: print('B') — B कब प्रिंट होता है?", "if a > b: print('A') else: print('B') — B kab print hota hai?"),
            ["when a > b", "when a <= b", "always", "never"],
            "b",
            L("else is everything the if did not catch, which here is a <= b.", "else वह सब है जो if ने नहीं पकड़ा, यानी a <= b।", "else woh sab hai jo if ne nahi pakda, yani a <= b."),
        ),
        quiz(
            L("Which is NOT valid Python?", "कौन सा वैध पायथन नहीं है?", "Kaun sa valid Python nahi hai?"),
            ["while x < 5:", "for i in range(3):", "if x > 2 and y < 1:", "elif x > 2:"],
            "d",
            L("elif only exists as part of an if chain; it cannot start a statement on its own.", "elif सिर्फ़ if चेन के हिस्से के रूप में होता है; वह अकेला स्टेटमेंट नहीं बन सकता।", "elif sirf if chain ke hisse ke roop me hota hai; woh akela statement nahi ban sakta."),
        ),
    ],
    icon="🔀",
)
