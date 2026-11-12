"""Module 11 - The standard library toolbox: batteries that ship with Python."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m11"

l01 = lesson(
    "m11c01l01",
    L("math, random and statistics", "math, random और statistics", "math, random aur statistics"),
    [],
    L(
        "Three small modules cover most number work: `math` for exact maths "
        "functions, `random` for shuffling and sampling (seed it for reproducible "
        "results), and `statistics` for mean, median and spread.",
        "तीन छोटे मॉड्यूल ज़्यादातर गणित का काम कर देते हैं: `math` सटीक गणितीय "
        "फ़ंक्शन के लिए, `random` फेंटने और नमूने के लिए (दोहराने योग्य परिणाम के लिए "
        "seed दें), और `statistics` औसत, माध्यिका और फैलाव के लिए।",
        "Teen chhote modules zyadatar ganit ka kaam kar dete hain: `math` sateek "
        "ganitiya functions ke liye, `random` phentne aur sample ke liye (dohrane yogya "
        "parinaam ke liye seed do), aur `statistics` average, median aur failav ke liye.",
    ),
    L(
        "A cricket scoreboard. math rounds the run rate, random decides who bats "
        "first, statistics tells you the average score of the last ten matches.",
        "क्रिकेट का स्कोरबोर्ड। math रन रेट गोल करता है, random तय करता है कौन पहले "
        "बल्लेबाज़ी करे, statistics पिछले दस मैचों का औसत बताता है।",
        "Cricket ka scoreboard. math run rate round karta hai, random tay karta hai "
        "kaun pehle batting kare, statistics pichhle das match ka average batata hai.",
    ),
    "https://docs.python.org/3/library/math.html",
    examples=[
        ex(
            "import math\nimport statistics\n\nprint(math.floor(3.9), math.ceil(3.1))\nprint(round(math.sqrt(2), 3))\nprint(statistics.mean([2, 4, 6]), statistics.median([1, 9, 5]))",
            "3 4\n1.414\n4 5",
            L("rounding and averages", "राउंडिंग और औसत", "rounding aur average"),
            note=L(
                "`round(x, 3)` keeps three decimals. `math.floor` always goes down and "
                "`math.ceil` always goes up, even for negative numbers.",
                "`round(x, 3)` तीन दशमलव रखता है। `math.floor` हमेशा नीचे और `math.ceil` "
                "हमेशा ऊपर जाता है, ऋणात्मक संख्याओं पर भी।",
                "`round(x, 3)` teen decimal rakhta hai. `math.floor` hamesha neeche aur "
                "`math.ceil` hamesha upar jata hai, negative numbers par bhi.",
            ),
        ),
        ex(
            'import random\n\nrandom.seed(42)\ncards = ["A", "K", "Q", "J"]\nrandom.shuffle(cards)\nprint(sorted(cards))\nprint(len(set(cards)))\nprint(random.choice(["rock", "paper", "scissors"]) in ["rock", "paper", "scissors"])',
            "['A', 'J', 'K', 'Q']\n4\nTrue",
            L("seeded randomness is repeatable", "seed वाली रैंडमनेस दोहराई जा सकती है", "seed wali randomness dohrai ja sakti hai"),
            note=L(
                "`seed(42)` makes the sequence reproducible, which is exactly what you "
                "want in tests. Without a seed every run differs.",
                "`seed(42)` श्रृंखला दोहराने योग्य बनाता है, टेस्ट में यही चाहिए। बिना "
                "seed हर बार अलग परिणाम आता है।",
                "`seed(42)` sequence dohrane yogya banata hai, test me yahi chahiye. Bina "
                "seed har baar alag result aata hai.",
            ),
        ),
        ex(
            "import statistics\n\nscores = [7, 8, 8, 9, 10, 3]\nprint(statistics.mean(scores))\nprint(statistics.median(scores))\nprint(statistics.mode(scores))\nprint(statistics.pstdev([2, 4, 4, 4, 5, 5, 7, 9]))",
            "7.5\n8.0\n8\n2.0",
            L("mean, median, mode and spread", "माध्य, माध्यिका, बहुलक और फैलाव", "mean, median, mode aur failav"),
            note=L(
                "The median ignores the one low score, the mean does not. That is why "
                "salaries and house prices are usually reported as medians.",
                "माध्यिका एक कम स्कोर को नज़रअंदाज़ करती है, माध्य नहीं। इसीलिए वेतन और "
                "मकानों के दाम आमतौर पर माध्यिका में बताए जाते हैं।",
                "Median ek kam score ko nazarandaz karti hai, mean nahi. Isliye salary "
                "aur ghar ke daam aam taur par median me bataye jate hain.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Using `statistics`, put the mean of `[4, 8, 6]` in `avg` and the median "
                "in `mid`, then print both.",
                "`statistics` से `[4, 8, 6]` का माध्य `avg` में और माध्यिका `mid` में "
                "रखें, फिर दोनों प्रिंट करें।",
                "`statistics` se `[4, 8, 6]` ka mean `avg` me aur median `mid` me rakho, "
                "phir dono print karo.",
            ),
            "import statistics\n\nvalues = [4, 8, 6]\n# avg = ...\n",
            "import statistics\n\nvalues = [4, 8, 6]\navg = statistics.mean(values)\nmid = statistics.median(values)\n\nprint(avg, mid)",
            [
                "avg == 6",
                "mid == 6",
                "printed.strip() == '6 6'",
            ],
            L(
                "statistics.mean(values) and statistics.median(values).",
                "statistics.mean(values) और statistics.median(values)।",
                "statistics.mean(values) aur statistics.median(values).",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which call always rounds down?",
                "कौन सी कॉल हमेशा नीचे राउंड करती है?",
                "Kaun si call hamesha neeche round karti hai?",
            ),
            ["round(x)", "math.floor(x)", "math.ceil(x)", "int(x)"],
            "b",
            L(
                "floor goes to the lower integer; int() truncates toward zero, which "
                "differs for negatives.",
                "floor निचली पूर्ण संख्या पर जाता है; int() शून्य की ओर काटता है, जो "
                "ऋणात्मक में अलग है।",
                "floor nichli pooran sankhya par jata hai; int() zero ki or kaatta hai, "
                "jo negative me alag hai.",
            ),
        ),
        quiz(
            L(
                "Why call random.seed() in a test?",
                "टेस्ट में random.seed() क्यों बुलाएँ?",
                "Test me random.seed() kyun bulayein?",
            ),
            [
                "to make random numbers truly secure",
                "to make the sequence reproducible",
                "to speed up the test",
                "it is required before randint",
            ],
            "b",
            L(
                "A fixed seed gives the same sequence every run. Never use it for "
                "passwords or tokens.",
                "तय seed हर बार वही श्रृंखला देता है। पासवर्ड या टोकन के लिए इसे कभी "
                "इस्तेमाल न करें।",
                "Tay seed har baar wahi sequence deta hai. Password ya token ke liye ise "
                "kabhi use na karo.",
            ),
        ),
        quiz(
            L(
                "Salaries [10, 10, 10, 10, 100]. Which is more representative?",
                "वेतन [10, 10, 10, 10, 100]। कौन ज़्यादा प्रतिनिधि है?",
                "Salary [10, 10, 10, 10, 100]. Kaun zyada representative hai?",
            ),
            ["the mean, 28", "the median, 10", "the mode is wrong", "they are equal"],
            "b",
            L(
                "One outlier pulls the mean far away; the median stays where most "
                "people are.",
                "एक बाहरी मान माध्य को दूर खींच लेता है; माध्यिका वहीं रहती है जहाँ "
                "ज़्यादातर लोग हैं।",
                "Ek outlier mean ko door khinch leta hai; median wahin rehti hai jahan "
                "zyadatar log hain.",
            ),
        ),
    ],
    takeaway=L(
        "math for exact operations, statistics for summaries, random with a seed when you need repeatability.",
        "सटीक संक्रियाओं के लिए math, सारांश के लिए statistics, दोहराव चाहिए तो seed वाला random।",
        "Sateek operations ke liye math, summary ke liye statistics, dohrav chahiye to seed wala random.",
    ),
)

l02 = lesson(
    "m11c01l02",
    L("Dates and times", "तारीख़ और समय", "Dates aur times"),
    [],
    L(
        "`date` is a day, `datetime` is a day plus a clock time, and `timedelta` is a "
        "duration you can add or subtract. `strftime` formats for humans, `strptime` "
        "parses text back into a datetime.",
        "`date` एक दिन है, `datetime` दिन के साथ घड़ी का समय, और `timedelta` अवधि है "
        "जिसे जोड़ या घटा सकते हैं। `strftime` इंसानों के लिए रूप बनाता है, `strptime` "
        "टेक्स्ट को वापस datetime में बदलता है।",
        "`date` ek din hai, `datetime` din ke saath ghadi ka samay, aur `timedelta` "
        "avadhi hai jise jod ya ghata sakte ho. `strftime` insaanon ke liye roop banata "
        "hai, `strptime` text ko wapas datetime me badalta hai.",
    ),
    L(
        "A train ticket. The date is printed, the departure time is printed, and the "
        "journey length lets you work out when you arrive.",
        "ट्रेन का टिकट। तारीख़ छपी है, प्रस्थान समय छपा है, और यात्रा की अवधि से आप "
        "पहुँचने का समय निकाल सकते हैं।",
        "Train ka ticket. Tareekh chhapi hai, departure time chhapa hai, aur yatra ki "
        "avadhi se aap pahunchne ka samay nikaal sakte ho.",
    ),
    "https://docs.python.org/3/library/datetime.html",
    examples=[
        ex(
            "from datetime import date, timedelta\n\nstart = date(2026, 11, 10)\nprint(start)\nprint(start + timedelta(days=30))\nprint((date(2026, 12, 25) - start).days)",
            "2026-11-10\n2026-12-10\n45",
            L("date arithmetic", "तारीख़ का गणित", "tareekh ka ganit"),
            note=L(
                "Adding a timedelta returns a new date. Subtracting two dates returns a "
                "timedelta, and `.days` gives the count.",
                "timedelta जोड़ने से नई तारीख़ मिलती है। दो तारीख़ें घटाने से timedelta "
                "मिलता है, और `.days` गिनती देता है।",
                "timedelta jodne se nayi tareekh milti hai. Do tareekh ghataane se "
                "timedelta milta hai, aur `.days` ginti deta hai.",
            ),
        ),
        ex(
            'from datetime import datetime\n\nmoment = datetime(2026, 11, 10, 9, 30)\nprint(moment.strftime("%d %b %Y, %H:%M"))\nprint(datetime.strptime("10/11/2026", "%d/%m/%Y").date())',
            "10 Nov 2026, 09:30\n2026-11-10",
            L("format out, parse in", "रूप बनाना, वापस पढ़ना", "roop banana, wapas padhna"),
            note=L(
                "%d is day, %m month, %Y four-digit year, %H hour, %M minute. The same "
                "codes are used by strftime and strptime.",
                "%d दिन, %m महीना, %Y चार अंकों का साल, %H घंटा, %M मिनट। वही कोड "
                "strftime और strptime दोनों में चलते हैं।",
                "%d din, %m mahina, %Y chaar ank ka saal, %H ghanta, %M minute. Wahi "
                "code strftime aur strptime dono me chalte hain.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "From `date(2026, 1, 1)`, compute the date 100 days later into `later` "
                "and print it.",
                "`date(2026, 1, 1)` से 100 दिन बाद की तारीख़ `later` में निकालें और "
                "प्रिंट करें।",
                "`date(2026, 1, 1)` se 100 din baad ki tareekh `later` me nikaalo aur "
                "print karo.",
            ),
            "from datetime import date, timedelta\n\nstart = date(2026, 1, 1)\n# later = ...\n",
            "from datetime import date, timedelta\n\nstart = date(2026, 1, 1)\nlater = start + timedelta(days=100)\n\nprint(later)",
            [
                "later == date(2026, 4, 11)",
                "printed.strip() == '2026-04-11'",
            ],
            L(
                "start + timedelta(days=100)",
                "start + timedelta(days=100)",
                "start + timedelta(days=100)",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which object represents a duration?",
                "अवधि कौन सा ऑब्जेक्ट दिखाता है?",
                "Avadhi kaun sa object dikhata hai?",
            ),
            ["date", "datetime", "timedelta", "timezone"],
            "c",
            L(
                "timedelta is the difference between two moments.",
                "timedelta दो क्षणों का अंतर है।",
                "timedelta do kshanon ka antar hai.",
            ),
        ),
        quiz(
            L(
                "What does `strptime` do?",
                "`strptime` क्या करता है?",
                "`strptime` kya karta hai?",
            ),
            [
                "turns a datetime into text",
                "parses text into a datetime",
                "returns the current time",
                "adds days",
            ],
            "b",
            L(
                "strftime = format to string; strptime = parse from string.",
                "strftime = स्ट्रिंग में रूप; strptime = स्ट्रिंग से पढ़ना।",
                "strftime = string me roop; strptime = string se padhna.",
            ),
        ),
        quiz(
            L(
                "Why is a naive datetime risky for global apps?",
                "वैश्विक ऐप के लिए naive datetime जोखिम भरा क्यों?",
                "Global app ke liye naive datetime risky kyun?",
            ),
            [
                "it cannot be printed",
                "it carries no timezone, so the same value means different moments",
                "it is slower",
                "it cannot be compared",
            ],
            "b",
            L(
                "Store UTC with a timezone, and convert for display only.",
                "UTC को टाइमज़ोन के साथ रखें, और सिर्फ़ दिखाने के लिए बदलें।",
                "UTC ko timezone ke saath rakho, aur sirf dikhane ke liye badlo.",
            ),
        ),
    ],
    takeaway=L(
        "Use date for days, datetime for moments, timedelta for durations; store UTC and format at the edge.",
        "दिन के लिए date, क्षण के लिए datetime, अवधि के लिए timedelta; UTC रखें और दिखाते समय रूप बदलें।",
        "Din ke liye date, kshan ke liye datetime, avadhi ke liye timedelta; UTC rakho aur dikhate samay roop badlo.",
    ),
)

l03 = lesson(
    "m11c02l03",
    L("collections: Counter, defaultdict, deque", "collections: Counter, defaultdict, deque", "collections: Counter, defaultdict, deque"),
    [],
    L(
        "`collections` has containers for jobs that come up constantly: Counter counts "
        "items, defaultdict creates a missing value instead of raising KeyError, and "
        "deque is a fast queue at both ends.",
        "`collections` में बार-बार आने वाले कामों के कंटेनर हैं: Counter चीज़ें गिनता "
        "है, defaultdict गायब मान बना देता है KeyError की जगह, और deque दोनों सिरों पर "
        "तेज़ कतार है।",
        "`collections` me baar-baar aane wale kaamon ke containers hain: Counter "
        "cheezein ginta hai, defaultdict ghayab value bana deta hai KeyError ki jagah, "
        "aur deque dono siro par tez kataar hai.",
    ),
    L(
        "A wedding hall. Counter is the person counting how many guests chose veg or "
        "non-veg. defaultdict is a new table opened automatically when a guest "
        "arrives. deque is the queue at the door.",
        "शादी का हॉल। Counter वह व्यक्ति है जो गिनता है कितने मेहमानों ने वेज या नॉन-वेज "
        "चुना। defaultdict अपने आप नई मेज़ खोलता है जब मेहमान आए। deque दरवाज़े की कतार है।",
        "Shaadi ka hall. Counter woh vyakti hai jo ginta hai kitne mehmaan ne veg ya "
        "non-veg chuna. defaultdict apne aap nayi table kholta hai jab mehmaan aaye. "
        "deque darwaze ki kataar hai.",
    ),
    "https://docs.python.org/3/library/collections.html",
    examples=[
        ex(
            'from collections import Counter\n\nvotes = ["tea", "coffee", "tea", "tea", "juice"]\ncounts = Counter(votes)\nprint(counts)\nprint(counts.most_common(1))\nprint(counts["cola"])',
            "Counter({'tea': 3, 'coffee': 1, 'juice': 1})\n[('tea', 3)]\n0",
            L("counting without a loop", "लूप के बिना गिनना", "loop ke bina ginna"),
            note=L(
                "Counter is a dict subclass, so a missing key gives 0 instead of "
                "KeyError. most_common returns (item, count) pairs.",
                "Counter dict का सबक्लास है, इसलिए गायब कुंजी KeyError की जगह 0 देती है। "
                "most_common (आइटम, गिनती) जोड़े लौटाता है।",
                "Counter dict ka subclass hai, isliye missing key KeyError ki jagah 0 "
                "deti hai. most_common (item, count) pairs return karta hai.",
            ),
        ),
        ex(
            'from collections import defaultdict\n\ngroups = defaultdict(list)\nfor name, team in [("Asha", "blue"), ("Ravi", "red"), ("Mili", "blue")]:\n    groups[team].append(name)\nprint(dict(groups))',
            "{'blue': ['Asha', 'Mili'], 'red': ['Ravi']}",
            L("grouping in one pass", "एक ही पास में समूह बनाना", "ek hi pass me group banana"),
            note=L(
                "`groups[team]` creates an empty list the first time that team "
                "appears. With a plain dict you would need an if-check first.",
                "`groups[team]` उस टीम के पहली बार आने पर खाली सूची बना देता है। सादे "
                "dict में पहले if जाँच लिखनी पड़ती।",
                "`groups[team]` us team ke pehli baar aane par khaali list bana deta hai. "
                "Saade dict me pehle if jaanch likhni padti.",
            ),
        ),
        ex(
            'from collections import deque\n\nqueue = deque(["a", "b"])\nqueue.append("c")\nqueue.appendleft("z")\nprint(list(queue))\nprint(queue.popleft())\nprint(list(queue))',
            "['z', 'a', 'b', 'c']\nz\n['a', 'b', 'c']",
            L("a queue at both ends", "दोनों सिरों पर कतार", "dono siro par kataar"),
            note=L(
                "popleft() is O(1); list.pop(0) has to shift every element.",
                "popleft() O(1) है; list.pop(0) को हर तत्व खिसकाना पड़ता है।",
                "popleft() O(1) hai; list.pop(0) ko har element khiskana padta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Count the letters of `'banana'` with Counter into `counts` and print "
                "`counts['a']`.",
                "Counter से `'banana'` के अक्षर गिनकर `counts` में रखें और "
                "`counts['a']` प्रिंट करें।",
                "Counter se `'banana'` ke letters gin kar `counts` me rakho aur "
                "`counts['a']` print karo.",
            ),
            "from collections import Counter\n\n# counts = ...\n",
            "from collections import Counter\n\ncounts = Counter('banana')\n\nprint(counts['a'])",
            [
                "counts['a'] == 3",
                "counts['n'] == 2",
                "counts['z'] == 0",
                "printed.strip() == '3'",
            ],
            L(
                "Counter accepts any iterable, including a string.",
                "Counter कोई भी इटरेबल लेता है, स्ट्रिंग भी।",
                "Counter koi bhi iterable leta hai, string bhi.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does Counter return for a missing key?",
                "Counter गायब कुंजी के लिए क्या देता है?",
                "Counter missing key ke liye kya deta hai?",
            ),
            ["KeyError", "None", "0", "an empty list"],
            "c",
            L(
                "That zero default is why counting needs no if-check.",
                "यही शून्य डिफ़ॉल्ट है जिससे गिनती में if जाँच नहीं चाहिए।",
                "Yahi zero default hai jisse ginti me if jaanch nahi chahiye.",
            ),
        ),
        quiz(
            L(
                "What does defaultdict(list) do on a missing key?",
                "defaultdict(list) गायब कुंजी पर क्या करता है?",
                "defaultdict(list) missing key par kya karta hai?",
            ),
            [
                "raises KeyError",
                "creates an empty list for that key",
                "returns None",
                "deletes the key",
            ],
            "b",
            L(
                "It calls list() to make the default, then stores it.",
                "यह डिफ़ॉल्ट बनाने के लिए list() बुलाता है, फिर उसे रख देता है।",
                "Ye default banane ke liye list() bulata hai, phir use rakh deta hai.",
            ),
        ),
        quiz(
            L(
                "Why is deque better than list for a queue?",
                "कतार के लिए deque list से बेहतर क्यों?",
                "Kataar ke liye deque list se behtar kyun?",
            ),
            [
                "it stores less memory per item",
                "removing from the front is O(1) instead of O(n)",
                "it sorts automatically",
                "it allows duplicate keys",
            ],
            "b",
            L(
                "list.pop(0) shifts everything; deque.popleft() does not.",
                "list.pop(0) सब खिसकाता है; deque.popleft() नहीं।",
                "list.pop(0) sab khiskata hai; deque.popleft() nahi.",
            ),
        ),
    ],
    takeaway=L(
        "Reach for Counter to count, defaultdict to group, deque for queues - before writing the loop by hand.",
        "गिनने के लिए Counter, समूह के लिए defaultdict, कतार के लिए deque - हाथ से लूप लिखने से पहले।",
        "Ginne ke liye Counter, group ke liye defaultdict, kataar ke liye deque - haath se loop likhne se pehle.",
    ),
)

l04 = lesson(
    "m11c02l04",
    L("itertools and functools", "itertools और functools", "itertools aur functools"),
    [],
    L(
        "`itertools` builds fast lazy pipelines (chain, groupby, product, islice) and "
        "`functools` works on functions (lru_cache for memoising, partial for fixing "
        "an argument, reduce for folding a sequence).",
        "`itertools` तेज़ आलसी पाइपलाइन बनाता है (chain, groupby, product, islice) और "
        "`functools` फ़ंक्शन पर काम करता है (memoise के लिए lru_cache, आर्ग्युमेंट तय "
        "करने के लिए partial, श्रृंखला मोड़ने के लिए reduce)।",
        "`itertools` tez lazy pipelines banata hai (chain, groupby, product, islice) aur "
        "`functools` function par kaam karta hai (memoise ke liye lru_cache, argument "
        "tay karne ke liye partial, sequence modne ke liye reduce).",
    ),
    L(
        "A kitchen assembly line. itertools joins two conveyor belts into one, and "
        "functools remembers the answer so the cook does not repeat the same dish.",
        "रसोई की असेंबली लाइन। itertools दो कन्वेयर बेल्ट को एक करता है, और functools "
        "जवाब याद रखता है ताकि रसोइया वही व्यंजन दोबारा न बनाए।",
        "Rasoi ki assembly line. itertools do conveyor belt ko ek karta hai, aur "
        "functools jawab yaad rakhta hai taaki rasoiya wahi dish dobara na banaye.",
    ),
    "https://docs.python.org/3/library/itertools.html",
    examples=[
        ex(
            'from itertools import chain, groupby\n\nprint(list(chain([1, 2], [3], [4, 5])))\n\nrows = [("fruit", "apple"), ("fruit", "mango"), ("veg", "pea")]\nfor key, group in groupby(rows, key=lambda row: row[0]):\n    print(key, [row[1] for row in group])',
            "[1, 2, 3, 4, 5]\nfruit ['apple', 'mango']\nveg ['pea']",
            L("chain and groupby", "chain और groupby", "chain aur groupby"),
            note=L(
                "groupby only groups adjacent items, so sort by the key first if equal "
                "keys are scattered.",
                "groupby सिर्फ़ पास-पास वाले आइटम समूह बनाता है, इसलिए अगर एक जैसी कुंजियाँ "
                "बिखरी हों तो पहले उस कुंजी से क्रमबद्ध करें।",
                "groupby sirf paas-paas wale items group banata hai, isliye agar same "
                "keys bikhri hon to pehle us key se sort karo.",
            ),
        ),
        ex(
            'from functools import lru_cache, partial\n\n@lru_cache(maxsize=None)\ndef slow_square(n):\n    print("computing", n)\n    return n * n\n\nprint(slow_square(4))\nprint(slow_square(4))\n\nadd_five = partial(lambda a, b: a + b, 5)\nprint(add_five(10))',
            "computing 4\n16\n16\n15",
            L("caching and partial application", "कैशिंग और आंशिक आर्ग्युमेंट", "caching aur partial argument"),
            note=L(
                "\"computing 4\" appears once because the second call is served from "
                "the cache. partial fixes 5 as the first argument.",
                "\"computing 4\" एक बार आता है क्योंकि दूसरी कॉल कैश से आती है। partial "
                "5 को पहला आर्ग्युमेंट बना देता है।",
                "\"computing 4\" ek baar aata hai kyunki doosri call cache se aati hai. "
                "partial 5 ko pehla argument bana deta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Use `chain` to join `[1, 2]` and `[3, 4]` into `joined` (a list) and "
                "print it.",
                "`chain` से `[1, 2]` और `[3, 4]` को `joined` में जोड़ें (सूची) और प्रिंट करें।",
                "`chain` se `[1, 2]` aur `[3, 4]` ko `joined` me jodo (list) aur print karo.",
            ),
            "from itertools import chain\n\n# joined = ...\n",
            "from itertools import chain\n\njoined = list(chain([1, 2], [3, 4]))\n\nprint(joined)",
            [
                "joined == [1, 2, 3, 4]",
                "isinstance(joined, list)",
                "printed.strip() == '[1, 2, 3, 4]'",
            ],
            L(
                "chain returns an iterator, so wrap it in list() to see the items.",
                "chain इटरेटर लौटाता है, इसलिए आइटम देखने के लिए list() में लपेटें।",
                "chain iterator return karta hai, isliye items dekhne ke liye list() me "
                "lapeto.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does `chain([1], [2])` return?",
                "`chain([1], [2])` क्या लौटाता है?",
                "`chain([1], [2])` kya return karta hai?",
            ),
            ["a list [1, 2]", "an iterator over 1, 2", "a tuple", "an error"],
            "b",
            L(
                "itertools functions are lazy; materialise with list() when needed.",
                "itertools फ़ंक्शन आलसी हैं; ज़रूरत हो तो list() से बना लें।",
                "itertools functions lazy hain; zaroorat ho to list() se bana lo.",
            ),
        ),
        quiz(
            L(
                "What does lru_cache do?",
                "lru_cache क्या करता है?",
                "lru_cache kya karta hai?",
            ),
            [
                "slows the function down",
                "remembers results for repeated arguments",
                "limits the arguments",
                "runs the function in a thread",
            ],
            "b",
            L(
                "Memoisation: the same input returns the stored output without rerunning "
                "the body. Only use it on pure functions.",
                "Memoisation: वही इनपुट बिना शरीर दोबारा चलाए जमा आउटपुट देता है। सिर्फ़ "
                "शुद्ध फ़ंक्शन पर इस्तेमाल करें।",
                "Memoisation: wahi input bina body dobara chalaye jama output deta hai. "
                "Sirf pure functions par use karo.",
            ),
        ),
        quiz(
            L(
                "What does partial(f, 5) create?",
                "partial(f, 5) क्या बनाता है?",
                "partial(f, 5) kya banata hai?",
            ),
            [
                "a copy of f",
                "a new callable with 5 already filled as the first argument",
                "a generator",
                "a cached f",
            ],
            "b",
            L(
                "It is handy for callbacks where the signature is fixed by someone else.",
                "यह उन कॉलबैक के लिए उपयोगी है जहाँ हस्ताक्षर किसी और ने तय किया है।",
                "Ye un callbacks ke liye useful hai jahan signature kisi aur ne tay kiya "
                "hai.",
            ),
        ),
    ],
    takeaway=L(
        "itertools for lazy pipelines, functools for caching and pre-filled arguments.",
        "आलसी पाइपलाइन के लिए itertools, कैशिंग और पहले से भरे आर्ग्युमेंट के लिए functools।",
        "Lazy pipelines ke liye itertools, caching aur pehle se bhare arguments ke liye functools.",
    ),
)

MODULE = module(
    M,
    L("The Standard Library Toolbox", "स्टैंडर्ड लाइब्रेरी का औज़ार-डिब्बा", "Standard Library ka Auzar-Dibba"),
    L(
        "math, random and statistics for numbers; datetime for time; collections for "
        "counting and grouping; itertools and functools for pipelines.",
        "संख्याओं के लिए math, random, statistics; समय के लिए datetime; गिनती और समूह के "
        "लिए collections; पाइपलाइन के लिए itertools और functools।",
        "Numbers ke liye math, random, statistics; samay ke liye datetime; ginti aur "
        "group ke liye collections; pipeline ke liye itertools aur functools.",
    ),
    [
        chapter("m11c01", L("Numbers and time", "संख्याएँ और समय", "Numbers aur time"), [l01, l02]),
        chapter("m11c02", L("Containers and pipelines", "कंटेनर और पाइपलाइन", "Containers aur pipelines"), [l03, l04]),
    ],
    exam=[
        quiz(
            L("Which module has mean and median?", "mean और median किस मॉड्यूल में?", "mean aur median kis module me?"),
            ["math", "statistics", "random", "numbers"],
            "b",
            L("statistics.mean / statistics.median.", "statistics.mean / statistics.median।", "statistics.mean / statistics.median."),
        ),
        quiz(
            L("Which object adds a duration to a date?", "तारीख़ में अवधि कौन जोड़ता है?", "Tareekh me avadhi kaun jodta hai?"),
            ["timedelta", "timespan", "duration", "period"],
            "a",
            L("date + timedelta gives a new date.", "date + timedelta नई तारीख़ देता है।", "date + timedelta nayi tareekh deta hai."),
        ),
        quiz(
            L("Which container counts items?", "कौन कंटेनर चीज़ें गिनता है?", "Kaun container cheezein ginta hai?"),
            ["deque", "Counter", "defaultdict", "OrderedDict"],
            "b",
            L("Counter is built for frequency counting.", "Counter आवृत्ति गिनने के लिए बना है।", "Counter aavritti ginne ke liye bana hai."),
        ),
        quiz(
            L("Which function groups adjacent equal keys?", "पास-पास की समान कुंजियाँ कौन समूह बनाता है?", "Paas-paas ki same keys kaun group banata hai?"),
            ["chain", "groupby", "partial", "islice"],
            "b",
            L("groupby needs sorted input to group everything together.", "सब कुछ एक साथ समूह बनाने के लिए groupby को क्रमबद्ध इनपुट चाहिए।", "Sab kuch ek saath group banane ke liye groupby ko sorted input chahiye."),
        ),
        quiz(
            L("Which decorator caches function results?", "कौन डेकोरेटर परिणाम कैश करता है?", "Kaun decorator parinaam cache karta hai?"),
            ["@property", "@lru_cache", "@staticmethod", "@total_ordering"],
            "b",
            L("@lru_cache from functools.", "functools से @lru_cache।", "functools se @lru_cache."),
        ),
        quiz(
            L("Why seed a random generator in tests?", "टेस्ट में रैंडम जनरेटर seed क्यों करें?", "Test me random generator seed kyun karein?"),
            ["for security", "for repeatable results", "for speed", "to avoid imports"],
            "b",
            L("Same seed, same sequence, so failures reproduce.", "वही seed, वही श्रृंखला, इसलिए विफलता दोहराई जा सकती है।", "Wahi seed, wahi sequence, isliye failure dohrai ja sakti hai."),
        ),
    ],
    icon="🧰",
)
