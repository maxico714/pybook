"""Module 6 - Errors and exceptions: what to do when things go wrong."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m06"

l01 = lesson(
    "m06c01l01",
    L("try, except, else, finally", "try, except, else, finally", "try, except, else, finally"),
    ["try", "except", "else", "finally"],
    L(
        "try runs code that might fail. except catches the failure and decides what "
        "to do. else runs only when nothing failed, and finally always runs, "
        "whether or not there was an error.",
        "try वह कोड चलाता है जो फेल हो सकता है। except गिरफ़्तार करके तय करता है क्या "
        "करना है। else तभी चलता है जब कुछ फेल न हुआ हो, और finally हमेशा चलता है, "
        "चाहे एरर आया हो या नहीं।",
        "try woh code chalata hai jo fail ho sakta hai. except pakadkar tay karta "
        "hai kya karna hai. else tabhi chalta hai jab kuch fail na hua ho, aur "
        "finally hamesha chalta hai, chahe error aaya ho ya nahi.",
    ),
    L(
        "Paying at a shop: try to scan the card (try). If the machine says declined, "
        "ask for cash (except). If it worked, print the receipt (else). Either way "
        "you take your bag and leave (finally).",
        "दुकान पर भुगतान: कार्ड स्कैन करने की कोशिश करें (try)। मशीन \"declined\" "
        "कहे तो नकद माँगें (except)। चल गया तो रसीद प्रिंट करें (else)। दोनों हालत "
        "में आप थैला लेकर निकलते हैं (finally)।",
        "Dukaan par payment: card scan karne ki koshish karo (try). Machine "
        "\"declined\" kahe to cash maango (except). Chal gaya to receipt print karo "
        "(else). Dono haalat me aap thaila lekar nikalte ho (finally).",
    ),
    "https://docs.python.org/3/tutorial/errors.html#handling-exceptions",
    visual="exception_flow",
    examples=[
        ex(
            'try:\n    n = int("4")\n    print(10 / n)\nexcept ZeroDivisionError:\n    print("cannot divide by zero")\nexcept ValueError:\n    print("not a number")\nelse:\n    print("no error happened")\nfinally:\n    print("this always runs")',
            "2.5\nno error happened\nthis always runs",
            L("all four blocks in one flow", "चारों ब्लॉक एक फ़्लो में", "chaaron blocks ek flow me"),
            note=L(
                "Nothing failed, so except is skipped and else runs. finally runs "
                "either way.",
                "कुछ फेल नहीं हुआ, इसलिए except छूटा और else चला। finally दोनों "
                "हालतों में चलता है।",
                "Kuch fail nahi hua, isliye except chhoota aur else chala. finally "
                "dono haalaton me chalta hai.",
            ),
        ),
        ex(
            "def safe_div(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\n\nprint(safe_div(10, 2))\nprint(safe_div(10, 0))",
            "5.0\nNone",
            L("a function that refuses to crash", "क्रैश न करने वाला फ़ंक्शन", "crash na karne wala function"),
            note=L(
                "Catching ZeroDivisionError turns a crash into a normal return "
                "value the caller can check.",
                "ZeroDivisionError पकड़ने से क्रैश एक सामान्य रिटर्न वैल्यू बन जाता "
                "है जिसे बुलाने वाला जाँच सकता है।",
                "ZeroDivisionError pakadne se crash ek normal return value ban jata "
                "hai jise caller check kar sakta hai.",
            ),
        ),
        ex(
            'try:\n    print(1 / 0)\nexcept ZeroDivisionError as exc:\n    print("caught:", exc)\nfinally:\n    print("cleanup done")',
            "caught: division by zero\ncleanup done",
            L("reading the exception message", "एक्सेप्शन मैसेज पढ़ना", "exception message padhna"),
            note=L(
                "`as exc` gives you the exception object. str(exc) is the message "
                "Python would have printed at the bottom of the traceback.",
                "`as exc` आपको एक्सेप्शन ऑब्जेक्ट देता है। str(exc) वही मैसेज है जो "
                "पायथन ट्रेसबैक के अंत में प्रिंट करता।",
                "`as exc` aapko exception object deta hai. str(exc) wahi message hai "
                "jo Python traceback ke end me print karta.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `safe_int(text)` that returns int(text), or 0 when the text is "
                "not a number. Print `safe_int('12')` and `safe_int('abc')`.",
                "`safe_int(text)` लिखें जो int(text) लौटाए, या टेक्स्ट नंबर न हो तो 0। "
                "`safe_int('12')` और `safe_int('abc')` प्रिंट करें।",
                "`safe_int(text)` likho jo int(text) return kare, ya text number na "
                "ho to 0. `safe_int('12')` aur `safe_int('abc')` print karo.",
            ),
            "def safe_int(text):\n    # try / except\n\n# print(safe_int('12'))\n# print(safe_int('abc'))\n",
            "def safe_int(text):\n    try:\n        return int(text)\n    except ValueError:\n        return 0\n\nprint(safe_int('12'))\nprint(safe_int('abc'))",
            [
                "safe_int('12') == 12",
                "safe_int('abc') == 0",
                "safe_int('-5') == -5",
                'printed.split() == ["12", "0"]',
            ],
            L(
                "int('abc') raises ValueError, so that is the exception to catch.",
                "int('abc') ValueError देता है, इसलिए वही पकड़ना है।",
                "int('abc') ValueError deta hai, isliye wahi pakadna hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which block runs only when no exception occurred?",
                "कौन सा ब्लॉक तभी चलता है जब कोई एक्सेप्शन न आया हो?",
                "Kaun sa block tabhi chalta hai jab koi exception na aaya ho?",
            ),
            ["try", "except", "else", "finally"],
            "c",
            L(
                "else is the success path. finally runs in both cases.",
                "else सफलता का रास्ता है। finally दोनों हालतों में चलता है।",
                "else success ka rasta hai. finally dono haalaton me chalta hai.",
            ),
        ),
        quiz(
            L(
                "Which block always runs?",
                "कौन सा ब्लॉक हमेशा चलता है?",
                "Kaun sa block hamesha chalta hai?",
            ),
            ["try", "except", "else", "finally"],
            "d",
            L(
                "finally runs after success, after a caught error, and even when the "
                "error was not caught.",
                "finally सफलता के बाद, पकड़े गए एरर के बाद, और बिना पकड़े एरर पर भी "
                "चलता है।",
                "finally success ke baad, pakde gaye error ke baad, aur bina pakde "
                "error par bhi chalta hai.",
            ),
        ),
        quiz(
            L(
                "Why is `except:` (bare) usually a bad idea?",
                "`except:` (बिना टाइप) आम तौर पर बुरा क्यों है?",
                "`except:` (bina type) aam taur par bura kyun hai?",
            ),
            [
                "it is slower",
                "it hides real bugs, including KeyboardInterrupt and typos",
                "it only catches ValueError",
                "it is a syntax error",
            ],
            "b",
            L(
                "Catch the exception you actually expect. A bare except also swallows "
                "programming mistakes you need to see.",
                "वही एक्सेप्शन पकड़ें जिसकी आपको उम्मीद है। बिना टाइप वाला except आपकी "
                "असली गलतियाँ भी निगल जाता है जो दिखनी चाहिए।",
                "Wahi exception pakdo jiski aapko ummeed hai. Bina type wala except "
                "aapki asli galtiyan bhi nigal jata hai jo dikhni chahiye.",
            ),
            "bare-except",
        ),
    ],
    takeaway=L(
        "try once; exactly one of except or else runs; finally always runs.",
        "try एक बार; except या else में से ठीक एक चलता है; finally हमेशा।",
        "try ek baar; except ya else me se exactly ek chalta hai; finally hamesha.",
    ),
)

l02 = lesson(
    "m06c01l02",
    L("raise, assert and common exceptions", "raise, assert और आम एक्सेप्शन", "raise, assert aur common exceptions"),
    ["raise", "assert"],
    L(
        "raise creates an exception on purpose. assert checks something that must "
        "be true and raises AssertionError if it is not. Knowing the common "
        "exception names lets you read a traceback in seconds.",
        "raise जान-बूझकर एक्सेप्शन बनाता है। assert ऐसी चीज़ जाँचता है जो सच होनी "
        "चाहिए और न होने पर AssertionError देता है। आम एक्सेप्शन नाम जानने से "
        "ट्रेसबैक कुछ सेकंड में पढ़ा जा सकता है।",
        "raise jaan-boojh kar exception banata hai. assert aisi cheez check karta hai "
        "jo sach honi chahiye aur na hone par AssertionError deta hai. Common "
        "exception naam jaanne se traceback kuch second me padha ja sakta hai.",
    ),
    L(
        "A form at a government office: if the photo is missing, the clerk does not "
        "silently continue — they say \"photo required\" and hand the form back. "
        "raise is that clerk. assert is the checklist the clerk uses internally.",
        "सरकारी दफ़्तर का फ़ॉर्म: फ़ोटो न हो तो क्लर्क चुपचाप आगे नहीं बढ़ता — वह "
        "\"फ़ोटो ज़रूरी है\" कहकर फ़ॉर्म लौटा देता है। raise वही क्लर्क है। assert "
        "क्लर्क की अंदरूनी चेकलिस्ट है।",
        "Sarkari daftar ka form: photo na ho to clerk chupchaap aage nahi badhta - "
        "woh \"photo zaroori hai\" kehkar form lautata hai. raise wahi clerk hai. "
        "assert clerk ki andaruni checklist hai.",
    ),
    "https://docs.python.org/3/tutorial/errors.html#raising-exceptions",
    examples=[
        ex(
            'def set_age(age):\n    if age < 0:\n        raise ValueError("age cannot be negative")\n    return age\n\nprint(set_age(30))\ntry:\n    set_age(-5)\nexcept ValueError as exc:\n    print("rejected:", exc)',
            "30\nrejected: age cannot be negative",
            L("raise with a useful message", "काम की मैसेज के साथ raise", "kaam ki message ke saath raise"),
            note=L(
                "The message should say what is wrong, not just \"error\". Whoever "
                "reads the traceback gets the explanation for free.",
                "मैसेज बताना चाहिए क्या गलत है, सिर्फ़ \"error\" नहीं। ट्रेसबैक पढ़ने "
                "वाले को वजह अपने आप मिल जाती है।",
                "Message batana chahiye kya galat hai, sirf \"error\" nahi. Traceback "
                "padhne wale ko wajah apne aap mil jati hai.",
            ),
        ),
        ex(
            'def average(nums):\n    assert nums, "the list must not be empty"\n    return sum(nums) / len(nums)\n\nprint(average([2, 4, 6]))\ntry:\n    average([])\nexcept AssertionError as exc:\n    print("assert failed:", exc)',
            "4.0\nassert failed: the list must not be empty",
            L("assert as an internal guard", "assert अंदरूनी गार्ड की तरह", "assert andaruni guard ki tarah"),
            note=L(
                "assert is for checks that should never fail in correct code. It is "
                "not for validating user input: running python -O removes it.",
                "assert उन जाँचों के लिए है जो सही कोड में कभी फेल न हों। यह यूज़र "
                "इनपुट जाँचने के लिए नहीं है: python -O उसे हटा देता है।",
                "assert un jaanchon ke liye hai jo sahi code me kabhi fail na hon. Ye "
                "user input validate karne ke liye nahi hai: python -O use hata deta hai.",
            ),
        ),
        ex(
            'for bad in [lambda: [1, 2][5], lambda: {"a": 1}["b"], lambda: "1" + 1]:\n    try:\n        bad()\n    except Exception as exc:\n        print(type(exc).__name__)',
            "IndexError\nKeyError\nTypeError",
            L("the three names you will meet most", "सबसे ज़्यादा मिलने वाले तीन नाम", "sabse zyada milne wale teen naam"),
            note=L(
                "IndexError is a bad position, KeyError a missing key, TypeError a "
                "wrong kind of value. ValueError is a right type, wrong content.",
                "IndexError गलत पोज़िशन, KeyError गुम की, TypeError गलत तरह की "
                "वैल्यू। ValueError सही टाइप, गलत सामग्री।",
                "IndexError galat position, KeyError missing key, TypeError galat "
                "tarah ki value. ValueError sahi type, galat content.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Write `shout(text)` that raises ValueError('empty text') when the "
                "text is blank, otherwise returns it in capitals with a '!' added.",
                "`shout(text)` लिखें जो टेक्स्ट खाली हो तो ValueError('empty text') "
                "दे, वरना उसे बड़े अक्षरों में '!' के साथ लौटाए।",
                "`shout(text)` likho jo text khaali ho to ValueError('empty text') "
                "de, warna use capital me '!' ke saath return kare.",
            ),
            "def shout(text):\n    # if blank: raise ...\n    # return ...\n",
            'def shout(text):\n    if not text.strip():\n        raise ValueError("empty text")\n    return text.upper() + "!"',
            [
                'shout("hi") == "HI!"',
                '_raises(shout, "", exc=ValueError)',
                '_raises(shout, "   ", exc=ValueError)',
            ],
            L(
                "text.strip() is empty for spaces only, so `not text.strip()` catches "
                "both cases.",
                "सिर्फ़ स्पेस पर text.strip() खाली है, इसलिए `not text.strip()` दोनों "
                "पकड़ लेता है।",
                "Sirf space par text.strip() khaali hai, isliye `not text.strip()` "
                "dono pakad leta hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does raise ValueError('bad') do?",
                "raise ValueError('bad') क्या करता है?",
                "raise ValueError('bad') kya karta hai?",
            ),
            [
                "prints the message and continues",
                "stops the current flow and creates an exception with that message",
                "returns 'bad'",
                "does nothing unless caught",
            ],
            "b",
            L(
                "raise immediately interrupts normal execution and starts looking "
                "for a matching except.",
                "raise तुरंत सामान्य निष्पादन रोकता है और मिलता-जुलता except ढूँढने "
                "लगता है।",
                "raise turant normal execution rokta hai aur matching except "
                "dhoondhne lagta hai.",
            ),
        ),
        quiz(
            L(
                "Which exception means a key was not found in a dict?",
                "कौन सा एक्सेप्शन बताता है कि dict में की नहीं मिली?",
                "Kaun sa exception batata hai ki dict me key nahi mili?",
            ),
            ["IndexError", "KeyError", "ValueError", "TypeError"],
            "b",
            L(
                "KeyError for dicts, IndexError for sequences, TypeError for the "
                "wrong kind of object.",
                "dict के लिए KeyError, सीक्वेंस के लिए IndexError, गलत तरह के "
                "ऑब्जेक्ट के लिए TypeError।",
                "dict ke liye KeyError, sequence ke liye IndexError, galat tarah ke "
                "object ke liye TypeError.",
            ),
        ),
        quiz(
            L(
                "Why should assert not be used to validate user input?",
                "यूज़र इनपुट जाँचने के लिए assert क्यों नहीं इस्तेमाल करना चाहिए?",
                "User input check karne ke liye assert kyun nahi use karna chahiye?",
            ),
            [
                "it is too slow",
                "running Python with -O removes assert statements",
                "it cannot take a message",
                "it only works on numbers",
            ],
            "b",
            L(
                "Assertions are a development aid. Use if + raise for anything the "
                "program must enforce at runtime.",
                "assert डेवलपमेंट का सहायक है। जो चीज़ रनटाइम पर लागू होनी चाहिए उसके "
                "लिए if + raise इस्तेमाल करें।",
                "assert development ka helper hai. Jo cheez runtime par enforce honi "
                "chahiye uske liye if + raise use karo.",
            ),
            "assert-vs-raise",
        ),
    ],
    takeaway=L(
        "raise with a clear message; assert only for internal checks; learn the five common exception names.",
        "साफ़ मैसेज के साथ raise; assert सिर्फ़ अंदरूनी जाँच के लिए; पाँच आम एक्सेप्शन नाम याद रखें।",
        "Saaf message ke saath raise; assert sirf andaruni check ke liye; paanch common exception naam yaad rakho.",
    ),
)

l03 = lesson(
    "m06c01l03",
    L("Custom exceptions and chaining", "कस्टम एक्सेप्शन और चेनिंग", "Custom exceptions aur chaining"),
    ["class", "raise", "except", "from"],
    L(
        "You can define your own exception class by inheriting from Exception. That "
        "lets callers catch your specific problem instead of guessing. `raise ... "
        "from exc` keeps the original error attached as the cause.",
        "आप Exception से इनहेरिट करके अपना एक्सेप्शन क्लास बना सकते हैं। इससे "
        "बुलाने वाला आपकी ख़ास समस्या पकड़ सकता है, अंदाज़ा नहीं लगाना पड़ता। "
        "`raise ... from exc` मूल एरर को कारण के रूप में जोड़े रखता है।",
        "Aap Exception se inherit karke apna exception class bana sakte ho. Isse "
        "caller aapki khaas problem pakad sakta hai, andaza nahi lagana padta. "
        "`raise ... from exc` original error ko cause ke roop me joda rakhta hai.",
    ),
    L(
        "A bank app: \"not enough balance\" is not a ValueError, it is its own kind "
        "of problem. Giving it a name means the app can show a friendly message "
        "instead of a generic error page.",
        "बैंक ऐप: \"बैलेंस कम है\" कोई ValueError नहीं, वह अपनी अलग तरह की समस्या "
        "है। उसे नाम देने से ऐप सामान्य एरर पेज की जगह मिली-जुली मैसेज दिखा सकता है।",
        "Bank app: \"balance kam hai\" koi ValueError nahi, woh apni alag tarah ki "
        "problem hai. Use naam dene se app generic error page ki jagah friendly "
        "message dikha sakta hai.",
    ),
    "https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions",
    examples=[
        ex(
            'class InsufficientFunds(Exception):\n    pass\n\ndef withdraw(balance, amount):\n    if amount > balance:\n        raise InsufficientFunds(f"need {amount - balance} more")\n    return balance - amount\n\nprint(withdraw(100, 30))\ntry:\n    withdraw(100, 150)\nexcept InsufficientFunds as exc:\n    print("blocked:", exc)',
            "70\nblocked: need 50 more",
            L("a named business error", "नाम वाला बिज़नेस एरर", "naam wala business error"),
            note=L(
                "The class body is just pass: the name and the parent class are the "
                "whole point.",
                "क्लास की बॉडी में सिर्फ़ pass है: नाम और पैरेंट क्लास ही पूरा मक़सद हैं।",
                "Class body me sirf pass hai: naam aur parent class hi poora maksad hain.",
            ),
        ),
        ex(
            'def parse(text):\n    try:\n        return int(text)\n    except ValueError as exc:\n        raise ValueError(f"bad number: {text!r}") from exc\n\ntry:\n    parse("abc")\nexcept ValueError as exc:\n    print(exc)\n    print("caused by:", type(exc.__cause__).__name__)',
            "bad number: 'abc'\ncaused by: ValueError",
            L("chaining keeps the original error", "चेनिंग मूल एरर रखती है", "chaining original error rakhti hai"),
            note=L(
                "`from exc` stores the original exception in __cause__, so a "
                "traceback shows both: your clear message and the real reason.",
                "`from exc` मूल एक्सेप्शन को __cause__ में रखता है, इसलिए ट्रेसबैक "
                "दोनों दिखाता है: आपकी साफ़ मैसेज और असली वजह।",
                "`from exc` original exception ko __cause__ me rakhta hai, isliye "
                "traceback dono dikhata hai: aapki saaf message aur asli wajah.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Define `TooSmall(Exception)` and `check(n)` that raises TooSmall when "
                "n is below 10, otherwise returns n.",
                "`TooSmall(Exception)` परिभाषित करें और `check(n)` जो n 10 से कम हो तो "
                "TooSmall दे, वरना n लौटाए।",
                "`TooSmall(Exception)` define karo aur `check(n)` jo n 10 se kam ho to "
                "TooSmall de, warna n return kare.",
            ),
            "class TooSmall(Exception):\n    pass\n\ndef check(n):\n    # ...\n",
            "class TooSmall(Exception):\n    pass\n\ndef check(n):\n    if n < 10:\n        raise TooSmall(f\"{n} is too small\")\n    return n",
            [
                "issubclass(TooSmall, Exception)",
                "check(20) == 20",
                "check(10) == 10",
                "_raises(check, 5, exc=TooSmall)",
            ],
            L(
                "raise TooSmall(...) inside the if, return n after it.",
                "if के अंदर raise TooSmall(...), उसके बाद return n।",
                "if ke andar raise TooSmall(...), uske baad return n.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which class should a custom exception inherit from?",
                "कस्टम एक्सेप्शन किस क्लास से इनहेरिट करे?",
                "Custom exception kis class se inherit kare?",
            ),
            ["object", "Exception", "ValueError only", "BaseException"],
            "b",
            L(
                "Exception is the normal base. BaseException is for things like "
                "KeyboardInterrupt, which you do not want to swallow.",
                "Exception सामान्य आधार है। BaseException उन चीज़ों के लिए है जैसे "
                "KeyboardInterrupt, जिन्हें आप निगलना नहीं चाहते।",
                "Exception normal base hai. BaseException un cheezon ke liye hai jaise "
                "KeyboardInterrupt, jinhe aap nigalna nahi chahte.",
            ),
        ),
        quiz(
            L(
                "What does `raise NewError(...) from exc` add?",
                "`raise NewError(...) from exc` क्या जोड़ता है?",
                "`raise NewError(...) from exc` kya jodta hai?",
            ),
            [
                "nothing, it is decoration",
                "it sets __cause__ so the original error is kept",
                "it catches exc automatically",
                "it prints exc",
            ],
            "b",
            L(
                "The cause chain is what makes a traceback say \"the above exception "
                "was the direct cause of the following exception\".",
                "कारण की चेन ही ट्रेसबैक में कहती है \"the above exception was the "
                "direct cause of the following exception\"।",
                "Cause chain hi traceback me kehti hai \"the above exception was the "
                "direct cause of the following exception\".",
            ),
        ),
        quiz(
            L(
                "Why bother with a custom exception instead of raising ValueError?",
                "ValueError की जगह कस्टम एक्सेप्शन क्यों बनाएँ?",
                "ValueError ki jagah custom exception kyun banayein?",
            ),
            [
                "custom exceptions are faster",
                "callers can catch exactly that problem and handle it differently",
                "ValueError cannot carry a message",
                "custom exceptions skip the traceback",
            ],
            "b",
            L(
                "A distinct type is a precise contract: the caller decides what to do "
                "with your problem without catching unrelated errors.",
                "अलग टाइप एक साफ़ समझौता है: बुलाने वाला आपकी समस्या पर तय कर सकता है "
                "बिना दूसरी गलतियाँ पकड़े।",
                "Alag type ek saaf contract hai: caller aapki problem par tay kar "
                "sakta hai bina doosri galtiyan pakde.",
            ),
        ),
    ],
    takeaway=L(
        "Name your own failures by subclassing Exception; chain with `from` to keep the cause.",
        "अपनी गलतियों को Exception से सबक्लास बनाकर नाम दें; कारण रखने के लिए `from` से चेन करें।",
        "Apni galtiyon ko Exception se subclass bana kar naam do; cause rakhne ke liye `from` se chain karo.",
    ),
)

MODULE = module(
    M,
    L("Errors and Exceptions", "एरर और एक्सेप्शन", "Errors aur Exceptions"),
    L(
        "Handle failure deliberately: try/except/else/finally, raise, assert, the "
        "common exception names, and your own exception classes.",
        "गड़बड़ी को समझदारी से संभालें: try/except/else/finally, raise, assert, आम "
        "एक्सेप्शन नाम, और अपने एक्सेप्शन क्लास।",
        "Gadbad ko samajhdari se sambhalo: try/except/else/finally, raise, assert, "
        "common exception naam, aur apne exception classes.",
    ),
    [
        chapter("m06c01", L("Handling and raising", "संभालना और उठाना", "Handle aur raise"), [l01, l02, l03]),
    ],
    exam=[
        quiz(
            L("Which runs after a successful try block?", "सफल try ब्लॉक के बाद कौन चलता है?", "Successful try block ke baad kaun chalta hai?"),
            ["except", "else", "finally only", "nothing"],
            "b",
            L("else is the no-error path; finally runs after it as well.", "else बिना-एरर रास्ता है; उसके बाद finally भी चलता है।", "else bina-error rasta hai; uske baad finally bhi chalta hai."),
        ),
        quiz(
            L("What does int('abc') raise?", "int('abc') क्या उठाता है?", "int('abc') kya uthata hai?"),
            ["TypeError", "ValueError", "KeyError", "SyntaxError"],
            "b",
            L("The type is right (str) but the content is not a number: ValueError.", "टाइप सही है (str) पर सामग्री नंबर नहीं: ValueError।", "Type sahi hai (str) par content number nahi: ValueError."),
        ),
        quiz(
            L("What does [1, 2][9] raise?", "[1, 2][9] क्या उठाता है?", "[1, 2][9] kya uthata hai?"),
            ["IndexError", "KeyError", "ValueError", "TypeError"],
            "a",
            L("A position past the end of a sequence is IndexError.", "सीक्वेंस के अंत से आगे की पोज़िशन IndexError है।", "Sequence ke end se aage ki position IndexError hai."),
        ),
        quiz(
            L("Which is the correct way to add context to a re-raised error?", "दोबारा उठाए एरर में संदर्भ जोड़ने का सही तरीका?", "Dobara uthaye error me context jodne ka sahi tarika?"),
            ["raise NewError() from exc", "raise NewError() + exc", "raise NewError() as exc", "raise NewError(), exc"],
            "a",
            L("`from` is the chaining syntax; `as` is only for except clauses.", "`from` चेनिंग सिंटैक्स है; `as` सिर्फ़ except के लिए है।", "`from` chaining syntax hai; `as` sirf except ke liye hai."),
        ),
        quiz(
            L("finally runs when the try block raises and nothing catches it?", "try ब्लॉक एरर दे और कोई न पकड़े, तब भी finally चलता है?", "try block error de aur koi na pakde, tab bhi finally chalta hai?"),
            ["yes, before the error propagates", "no", "only with else", "only if you call sys.exit"],
            "a",
            L("finally is guaranteed cleanup: it runs before the exception continues outward.", "finally गारंटीड सफ़ाई है: एरर बाहर जाने से पहले चलता है।", "finally guaranteed cleanup hai: error bahar jaane se pehle chalta hai."),
        ),
    ],
    icon="🛟",
)
