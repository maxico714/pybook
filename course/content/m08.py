"""Module 8 - Classes and objects: your own types with data and behaviour."""
from __future__ import annotations

from ..schema import L
from ._kit import chapter, ex, lesson, module, quiz, task

M = "m08"

l01 = lesson(
    "m08c01l01",
    L("class, __init__ and self", "class, __init__ और self", "class, __init__ aur self"),
    ["class"],
    L(
        "A class is a blueprint; an object is one thing built from it. `__init__` "
        "runs when the object is created and stores its starting data on `self` - "
        "the object being worked on.",
        "क्लास एक नक्शा है; ऑब्जेक्ट उससे बनी एक चीज़। ऑब्जेक्ट बनते समय `__init__` "
        "चलता है और शुरुआती डेटा `self` पर रखता है - यानी वही ऑब्जेक्ट जिस पर काम "
        "हो रहा है।",
        "Class ek blueprint hai; object usse bani ek cheez. Object bante samay "
        "`__init__` chalta hai aur shuruaati data `self` par rakhta hai - yani wahi "
        "object jis par kaam ho raha hai.",
    ),
    L(
        "A cookie cutter and cookies. The cutter is the class; every cookie is an "
        "object. Each cookie can have its own icing even though they came from one "
        "cutter.",
        "कुकी कटर और कुकीज़। कटर क्लास है; हर कुकी ऑब्जेक्ट। एक ही कटर से बनी होने पर "
        "भी हर कुकी की आइसिंग अलग हो सकती है।",
        "Cookie cutter aur cookies. Cutter class hai; har cookie object. Ek hi cutter "
        "se bani hone par bhi har cookie ki icing alag ho sakti hai.",
    ),
    "https://docs.python.org/3/tutorial/classes.html",
    visual="class_object",
    examples=[
        ex(
            'class Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def bark(self):\n        return f"{self.name} says woof"\n\ndog = Dog("Bruno")\nprint(dog.name)\nprint(dog.bark())',
            "Bruno\nBruno says woof",
            L("one class, one object", "एक क्लास, एक ऑब्जेक्ट", "ek class, ek object"),
            note=L(
                "`self` is the object the method was called on. Python passes it for "
                "you, which is why `dog.bark()` needs no argument.",
                "`self` वही ऑब्जेक्ट है जिस पर मेथड बुलाया गया। पायथन इसे अपने आप "
                "भेजता है, इसलिए `dog.bark()` में कोई आर्ग्युमेंट नहीं चाहिए।",
                "`self` wahi object hai jis par method bulaya gaya. Python ise apne "
                "aap bhejta hai, isliye `dog.bark()` me koi argument nahi chahiye.",
            ),
        ),
        ex(
            'class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def bump(self):\n        self.value += 1\n\na = Counter()\nb = Counter()\na.bump()\na.bump()\nprint(a.value, b.value)',
            "2 0",
            L("every object keeps its own data", "हर ऑब्जेक्ट अपना डेटा रखता है", "har object apna data rakhta hai"),
            note=L(
                "Two objects from one class do not share `value`. That independence is "
                "the main reason classes exist.",
                "एक क्लास से बने दो ऑब्जेक्ट `value` साझा नहीं करते। यही अलगाव क्लास का "
                "मुख्य कारण है।",
                "Ek class se bane do objects `value` share nahi karte. Yahi alagav "
                "class ka mukhya karan hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Create a class `Book` whose `__init__` stores `title` and `pages`, and "
                "a method `summary()` that returns `'<title>: <pages> pages'`. Print "
                "the summary of `Book('Python', 300)`.",
                "क्लास `Book` बनाएँ जिसका `__init__` `title` और `pages` रखे, और "
                "`summary()` मेथड `'<title>: <pages> pages'` लौटाए। "
                "`Book('Python', 300)` का summary प्रिंट करें।",
                "Class `Book` banao jiska `__init__` `title` aur `pages` rakhe, aur "
                "`summary()` method `'<title>: <pages> pages'` return kare. "
                "`Book('Python', 300)` ka summary print karo.",
            ),
            "class Book:\n    def __init__(self, title, pages):\n        pass\n\n    def summary(self):\n        pass\n\n# print(Book('Python', 300).summary())\n",
            'class Book:\n    def __init__(self, title, pages):\n        self.title = title\n        self.pages = pages\n\n    def summary(self):\n        return f"{self.title}: {self.pages} pages"\n\nprint(Book("Python", 300).summary())',
            [
                "Book('Python', 300).summary() == 'Python: 300 pages'",
                "Book('Short', 1).summary() == 'Short: 1 pages'",
                "printed.strip() == 'Python: 300 pages'",
            ],
            L(
                "Store both arguments on self, then build the string with an f-string.",
                "दोनों आर्ग्युमेंट self पर रखें, फिर f-string से स्ट्रिंग बनाएँ।",
                "Dono arguments self par rakho, phir f-string se string banao.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What is `self` inside a method?",
                "मेथड के अंदर `self` क्या है?",
                "Method ke andar `self` kya hai?",
            ),
            [
                "the class itself",
                "the object the method was called on",
                "a required keyword",
                "a copy of the arguments",
            ],
            "b",
            L(
                "self is the instance. The class is reached with `type(self)` or the "
                "class name.",
                "self इंस्टेंस है। क्लास तक `type(self)` या क्लास के नाम से पहुँचते हैं।",
                "self instance hai. Class tak `type(self)` ya class ke naam se pahunchte "
                "hain.",
            ),
        ),
        quiz(
            L(
                "When does `__init__` run?",
                "`__init__` कब चलता है?",
                "`__init__` kab chalta hai?",
            ),
            [
                "when the class is defined",
                "when an object is created",
                "when a method is called",
                "only when you call it yourself",
            ],
            "b",
            L(
                "Creating the object calls it with the arguments you passed to the "
                "class.",
                "ऑब्जेक्ट बनाने पर यह उन आर्ग्युमेंट के साथ चलता है जो आपने क्लास को दिए।",
                "Object banane par ye un arguments ke saath chalta hai jo aapne class "
                "ko diye.",
            ),
        ),
        quiz(
            L(
                "Why do two objects of the same class not share `self.value`?",
                "एक ही क्लास के दो ऑब्जेक्ट `self.value` क्यों साझा नहीं करते?",
                "Ek hi class ke do objects `self.value` kyun share nahi karte?",
            ),
            [
                "because value is read-only",
                "because each object has its own attribute dictionary",
                "because Python copies the class for each object",
                "because self is a global",
            ],
            "b",
            L(
                "Instance attributes live on the instance. Only class-level names are "
                "shared, and assigning on the instance shadows them.",
                "इंस्टेंस एट्रिब्यूट इंस्टेंस पर रहते हैं। सिर्फ़ क्लास-लेवल नाम साझा होते "
                "हैं, और इंस्टेंस पर असाइन करने से वे छिप जाते हैं।",
                "Instance attributes instance par rehte hain. Sirf class-level naam "
                "share hote hain, aur instance par assign karne se wo chhip jate hain.",
            ),
        ),
    ],
    takeaway=L(
        "class is a blueprint, __init__ sets up each object, self is the object.",
        "class नक्शा है, __init__ हर ऑब्जेक्ट तैयार करता है, self वह ऑब्जेक्ट है।",
        "class blueprint hai, __init__ har object taiyar karta hai, self woh object hai.",
    ),
)

l02 = lesson(
    "m08c01l02",
    L("Attributes and methods", "एट्रिब्यूट और मेथड", "Attributes aur methods"),
    [],
    L(
        "Attributes are the data an object carries; methods are the functions that "
        "read or change it. A class attribute is shared by every object, an instance "
        "attribute belongs to one object and wins when both exist.",
        "एट्रिब्यूट वह डेटा हैं जो ऑब्जेक्ट रखता है; मेथड वे फ़ंक्शन हैं जो उसे पढ़ते या "
        "बदलते हैं। क्लास एट्रिब्यूट हर ऑब्जेक्ट में साझा होता है, इंस्टेंस एट्रिब्यूट "
        "एक ऑब्जेक्ट का होता है और दोनों हों तो इंस्टेंस वाला जीतता है।",
        "Attributes woh data hain jo object rakhta hai; methods woh functions hain jo "
        "use padhte ya badalte hain. Class attribute har object me share hota hai, "
        "instance attribute ek object ka hota hai aur dono hon to instance wala "
        "jeetta hai.",
    ),
    L(
        "A school uniform. The school decides the uniform colour (class attribute). "
        "A student can wear a badge that only they have (instance attribute).",
        "स्कूल की वर्दी। स्कूल रंग तय करता है (क्लास एट्रिब्यूट)। एक छात्र अपना अलग "
        "बैज लगा सकता है (इंस्टेंस एट्रिब्यूट)।",
        "School ki vardi. School rang tay karta hai (class attribute). Ek student "
        "apna alag badge laga sakta hai (instance attribute).",
    ),
    "https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables",
    examples=[
        ex(
            'class Player:\n    team = "Blue"\n\n    def __init__(self, name):\n        self.name = name\n\np1 = Player("Asha")\np2 = Player("Ravi")\nprint(p1.team, p2.team)\nPlayer.team = "Red"\nprint(p1.team, p2.team)\np1.team = "Green"\nprint(p1.team, p2.team)',
            "Blue Blue\nRed Red\nGreen Red",
            L("class attribute vs instance attribute", "क्लास एट्रिब्यूट बनाम इंस्टेंस एट्रिब्यूट", "class attribute vs instance attribute"),
            note=L(
                "Changing Player.team reached both objects. Assigning p1.team created a "
                "new instance attribute that shadows the class one only for p1.",
                "Player.team बदलने से दोनों ऑब्जेक्ट पर असर हुआ। p1.team असाइन करने से "
                "नया इंस्टेंस एट्रिब्यूट बना जो सिर्फ़ p1 के लिए क्लास वाले को छिपाता है।",
                "Player.team badalne se dono objects par asar hua. p1.team assign karne "
                "se naya instance attribute bana jo sirf p1 ke liye class wale ko "
                "chhipata hai.",
            ),
        ),
        ex(
            'class Wallet:\n    def __init__(self, rupees=0):\n        self.rupees = rupees\n\n    def add(self, amount):\n        self.rupees += amount\n        return self.rupees\n\nwallet = Wallet()\nprint(wallet.add(50))\nprint(wallet.add(25))\nprint(wallet.rupees)',
            "50\n75\n75",
            L("a method that changes state", "स्थिति बदलने वाला मेथड", "state badalne wala method"),
            note=L(
                "`self.rupees += amount` reads the attribute, adds, and stores it back "
                "on the same object.",
                "`self.rupees += amount` एट्रिब्यूट पढ़ता है, जोड़ता है, और उसी ऑब्जेक्ट "
                "पर वापस रखता है।",
                "`self.rupees += amount` attribute padhta hai, jodta hai, aur usi object "
                "par wapas rakhta hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Create `Temperature` with `celsius`, and a method `fahrenheit()` that "
                "returns `celsius * 9 / 5 + 32`. Print `Temperature(100).fahrenheit()`.",
                "`Temperature` बनाएँ जिसमें `celsius` हो और `fahrenheit()` मेथड "
                "`celsius * 9 / 5 + 32` लौटाए। `Temperature(100).fahrenheit()` प्रिंट करें।",
                "`Temperature` banao jisme `celsius` ho aur `fahrenheit()` method "
                "`celsius * 9 / 5 + 32` return kare. `Temperature(100).fahrenheit()` print karo.",
            ),
            "class Temperature:\n    def __init__(self, celsius):\n        pass\n\n    def fahrenheit(self):\n        pass\n\n# print(Temperature(100).fahrenheit())\n",
            "class Temperature:\n    def __init__(self, celsius):\n        self.celsius = celsius\n\n    def fahrenheit(self):\n        return self.celsius * 9 / 5 + 32\n\nprint(Temperature(100).fahrenheit())",
            [
                "Temperature(100).fahrenheit() == 212.0",
                "Temperature(0).fahrenheit() == 32.0",
                "Temperature(-40).fahrenheit() == -40.0",
                "printed.strip() == '212.0'",
            ],
            L(
                "Store celsius on self, then use self.celsius in the formula.",
                "celsius को self पर रखें, फिर सूत्र में self.celsius इस्तेमाल करें।",
                "celsius ko self par rakho, phir formula me self.celsius use karo.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "`p1.team = \"Green\"` after `Player.team = \"Red\"`. What is `p2.team`?",
                "`Player.team = \"Red\"` के बाद `p1.team = \"Green\"`। `p2.team` क्या है?",
                "`Player.team = \"Red\"` ke baad `p1.team = \"Green\"`. `p2.team` kya hai?",
            ),
            ["Green", "Red", "an error", "None"],
            "b",
            L(
                "Only p1 got its own attribute; p2 still reads the class value.",
                "सिर्फ़ p1 को अपना एट्रिब्यूट मिला; p2 अभी भी क्लास वाला पढ़ता है।",
                "Sirf p1 ko apna attribute mila; p2 abhi bhi class wala padhta hai.",
            ),
        ),
        quiz(
            L(
                "Which lookup wins when an instance and its class both define `size`?",
                "जब इंस्टेंस और क्लास दोनों `size` रखें, कौन जीतता है?",
                "Jab instance aur class dono `size` rakhein, kaun jeetta hai?",
            ),
            ["the class attribute", "the instance attribute", "whichever is newer", "Python raises an error"],
            "b",
            L(
                "Attribute lookup checks the instance first, then the class.",
                "एट्रिब्यूट खोज पहले इंस्टेंस देखती है, फिर क्लास।",
                "Attribute lookup pehle instance dekhti hai, phir class.",
            ),
        ),
        quiz(
            L(
                "Why is a mutable class attribute like `items = []` dangerous?",
                "`items = []` जैसा बदलने योग्य क्लास एट्रिब्यूट खतरनाक क्यों?",
                "`items = []` jaisa mutable class attribute khatarnak kyun?",
            ),
            [
                "it cannot be printed",
                "every object that mutates it changes the shared list",
                "it is slower than a tuple",
                "it is deleted after each call",
            ],
            "b",
            L(
                "One shared list for all objects is a classic bug. Create it in "
                "__init__ instead.",
                "सभी ऑब्जेक्ट के लिए एक साझा सूची classic बग है। इसे __init__ में बनाएँ।",
                "Sab objects ke liye ek shared list classic bug hai. Ise __init__ me "
                "banao.",
            ),
        ),
    ],
    takeaway=L(
        "Put per-object data in __init__; use class attributes only for values that really are shared.",
        "हर ऑब्जेक्ट का डेटा __init__ में रखें; क्लास एट्रिब्यूट सिर्फ़ सचमुच साझा मानों के लिए।",
        "Har object ka data __init__ me rakho; class attribute sirf sachmuch shared values ke liye.",
    ),
)

l03 = lesson(
    "m08c02l03",
    L("Inheritance and super()", "इनहेरिटेंस और super()", "Inheritance aur super()"),
    ["class"],
    L(
        "A subclass inherits every attribute and method of its parent, then adds or "
        "replaces what it needs. `super()` calls the parent version so you do not "
        "copy its code.",
        "सबक्लास अपने पैरेंट के सभी एट्रिब्यूट और मेथड विरासत में लेता है, फिर जो चाहिए "
        "वह जोड़ता या बदलता है। `super()` पैरेंट वाला रूप बुलाता है ताकि उसका कोड "
        "दोबारा न लिखना पड़े।",
        "Subclass apne parent ke saare attributes aur methods inherit karta hai, phir "
        "jo chahiye woh jodta ya badalta hai. `super()` parent wala roop bulata hai "
        "taaki uska code dobara na likhna pade.",
    ),
    L(
        "A pizza menu. Every pizza has a base and cheese (parent). Margherita adds "
        "tomato; Farmhouse adds onion and capsicum. You do not rebuild the base each "
        "time.",
        "पिज़्ज़ा मेन्यू। हर पिज़्ज़ा में बेस और चीज़ होती है (पैरेंट)। मार्गरीटा में "
        "टमाटर जुड़ता है; फार्महाउस में प्याज़ और शिमला मिर्च। बेस हर बार दोबारा नहीं "
        "बनाते।",
        "Pizza menu. Har pizza me base aur cheese hoti hai (parent). Margherita me "
        "tomato judta hai; Farmhouse me onion aur capsicum. Base har baar dobara "
        "nahi banate.",
    ),
    "https://docs.python.org/3/tutorial/classes.html#inheritance",
    examples=[
        ex(
            'class Animal:\n    def __init__(self, name):\n        self.name = name\n\n    def speak(self):\n        return "..."\n\nclass Cat(Animal):\n    def speak(self):\n        return "meow"\n\nclass Dog(Animal):\n    def speak(self):\n        return "woof"\n\nfor pet in (Cat("Mili"), Dog("Bruno")):\n    print(pet.name, pet.speak())',
            "Mili meow\nBruno woof",
            L("same call, different behaviour", "एक कॉल, अलग व्यवहार", "ek call, alag behaviour"),
            note=L(
                "`name` and `__init__` were written once in Animal. Each subclass "
                "replaced only `speak`.",
                "`name` और `__init__` Animal में एक बार लिखे गए। हर सबक्लास ने सिर्फ़ "
                "`speak` बदला।",
                "`name` aur `__init__` Animal me ek baar likhe gaye. Har subclass ne "
                "sirf `speak` badla.",
            ),
        ),
        ex(
            'class Account:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self.balance = balance\n\n    def describe(self):\n        return f"{self.owner}: {self.balance}"\n\nclass Savings(Account):\n    def __init__(self, owner, balance=0, rate=0.05):\n        super().__init__(owner, balance)\n        self.rate = rate\n\n    def describe(self):\n        return super().describe() + f" (rate {self.rate})"\n\naccount = Savings("Asha", 1000)\nprint(account.describe())\nprint(isinstance(account, Account), isinstance(account, Savings))',
            "Asha: 1000 (rate 0.05)\nTrue True",
            L("super() reuses the parent", "super() पैरेंट दोबारा इस्तेमाल करता है", "super() parent dobara use karta hai"),
            note=L(
                "super().__init__ sets owner and balance; super().describe() builds the "
                "first half of the sentence. isinstance is True for both classes.",
                "super().__init__ owner और balance रखता है; super().describe() वाक्य का "
                "पहला हिस्सा बनाता है। isinstance दोनों क्लास के लिए True है।",
                "super().__init__ owner aur balance rakhta hai; super().describe() "
                "vakya ka pehla hissa banata hai. isinstance dono classes ke liye True hai.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Create `Shape` with a method `area()` returning 0, and `Square(Shape)` "
                "with `side` and its own `area()`. Print `Square(4).area()`.",
                "`Shape` बनाएँ जिसका `area()` 0 लौटाए, और `Square(Shape)` जिसमें `side` "
                "और अपना `area()` हो। `Square(4).area()` प्रिंट करें।",
                "`Shape` banao jiska `area()` 0 return kare, aur `Square(Shape)` jisme "
                "`side` aur apna `area()` ho. `Square(4).area()` print karo.",
            ),
            "class Shape:\n    def area(self):\n        return 0\n\nclass Square(Shape):\n    # ...\n",
            "class Shape:\n    def area(self):\n        return 0\n\nclass Square(Shape):\n    def __init__(self, side):\n        self.side = side\n\n    def area(self):\n        return self.side * self.side\n\nprint(Square(4).area())",
            [
                "issubclass(Square, Shape)",
                "Square(4).area() == 16",
                "Square(1).area() == 1",
                "Shape().area() == 0",
                "printed.strip() == '16'",
            ],
            L(
                "Square needs its own __init__ and area; the parent already gives the "
                "fallback.",
                "Square को अपना __init__ और area चाहिए; गिरने का विकल्प पैरेंट देता है।",
                "Square ko apna __init__ aur area chahiye; fallback parent deta hai.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "What does a subclass get from its parent?",
                "सबक्लास को पैरेंट से क्या मिलता है?",
                "Subclass ko parent se kya milta hai?",
            ),
            [
                "nothing until you copy it",
                "all attributes and methods it does not override",
                "only __init__",
                "only private names",
            ],
            "b",
            L(
                "Inheritance is automatic reuse; overriding replaces one piece.",
                "इनहेरिटेंस अपने आप दोबारा इस्तेमाल है; override एक हिस्सा बदलता है।",
                "Inheritance apne aap dobara use hai; override ek hissa badalta hai.",
            ),
        ),
        quiz(
            L(
                "Why call `super().__init__(...)` in a subclass?",
                "सबक्लास में `super().__init__(...)` क्यों बुलाएँ?",
                "Subclass me `super().__init__(...)` kyun bulayein?",
            ),
            [
                "to make the class abstract",
                "to let the parent set up the attributes it owns",
                "to avoid calling the subclass constructor",
                "because Python requires it",
            ],
            "b",
            L(
                "Without it the parent's setup never runs and those attributes are "
                "missing.",
                "इसके बिना पैरेंट की तैयारी कभी नहीं चलती और वे एट्रिब्यूट गायब रहते हैं।",
                "Iske bina parent ki taiyari kabhi nahi chalti aur wo attributes "
                "ghayab rehte hain.",
            ),
        ),
        quiz(
            L(
                "`isinstance(Savings('a'), Account)` is:",
                "`isinstance(Savings('a'), Account)` है:",
                "`isinstance(Savings('a'), Account)` hai:",
            ),
            ["True", "False", "an error", "None"],
            "a",
            L(
                "A subclass instance is also an instance of every parent class.",
                "सबक्लास का ऑब्जेक्ट हर पैरेंट क्लास का भी ऑब्जेक्ट है।",
                "Subclass ka object har parent class ka bhi object hai.",
            ),
        ),
    ],
    takeaway=L(
        "Inherit for real \"is a\" relationships, override one method at a time, and let super() do the parent's work.",
        "सच्चे \"is a\" संबंध के लिए इनहेरिट करें, एक-एक मेथड override करें, और पैरेंट का काम super() को दें।",
        "Sachche \"is a\" relation ke liye inherit karo, ek-ek method override karo, aur parent ka kaam super() ko do.",
    ),
)

l04 = lesson(
    "m08c02l04",
    L("Dunder methods and dataclasses", "डंडर मेथड और डेटाक्लास", "Dunder methods aur dataclasses"),
    ["class"],
    L(
        "Names with two underscores on each side (`__init__`, `__repr__`, `__eq__`) "
        "are hooks Python calls for you. `@dataclass` writes the boring ones - "
        "`__init__`, `__repr__`, `__eq__` - from the field list.",
        "दोनों तरफ़ दो अंडरस्कोर वाले नाम (`__init__`, `__repr__`, `__eq__`) ऐसे हुक हैं "
        "जिन्हें पायथन आपके लिए बुलाता है। `@dataclass` फ़ील्ड सूची से ऊबाऊ वाले - "
        "`__init__`, `__repr__`, `__eq__` - अपने आप लिख देता है।",
        "Dono taraf do underscore wale naam (`__init__`, `__repr__`, `__eq__`) aise "
        "hooks hain jinhe Python aapke liye bulata hai. `@dataclass` field list se "
        "boring wale - `__init__`, `__repr__`, `__eq__` - apne aap likh deta hai.",
    ),
    L(
        "A visiting card. `__repr__` is what is printed on the card; `__eq__` decides "
        "whether two cards belong to the same person.",
        "विज़िटिंग कार्ड। `__repr__` वह है जो कार्ड पर छपा है; `__eq__` तय करता है कि दो "
        "कार्ड एक ही व्यक्ति के हैं या नहीं।",
        "Visiting card. `__repr__` woh hai jo card par chhapa hai; `__eq__` tay karta "
        "hai ki do card ek hi vyakti ke hain ya nahi.",
    ),
    "https://docs.python.org/3/library/dataclasses.html",
    examples=[
        ex(
            'class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\n    def __eq__(self, other):\n        return isinstance(other, Point) and (self.x, self.y) == (other.x, other.y)\n\n    def __repr__(self):\n        return f"Point({self.x}, {self.y})"\n\nprint(Point(1, 2) == Point(1, 2))\nprint(Point(1, 2) == Point(3, 4))\nprint([Point(0, 1)])',
            "True\nFalse\n[Point(0, 1)]",
            L("__eq__ and __repr__ by hand", "__eq__ और __repr__ हाथ से", "__eq__ aur __repr__ haath se"),
            note=L(
                "Without __eq__, two objects with the same values compare unequal, "
                "because the default is identity. Without __repr__, a list shows "
                "`<__main__.Point object at 0x...>`.",
                "__eq__ के बिना समान मान वाले दो ऑब्जेक्ट बराबर नहीं माने जाते, क्योंकि "
                "डिफ़ॉल्ट पहचान है। __repr__ के बिना सूची `<__main__.Point object at "
                "0x...>` दिखाती है।",
                "__eq__ ke bina same value wale do objects barabar nahi maane jate, "
                "kyunki default identity hai. __repr__ ke bina list "
                "`<__main__.Point object at 0x...>` dikhati hai.",
            ),
        ),
        ex(
            'from dataclasses import dataclass\n\n@dataclass\nclass Task:\n    title: str\n    done: bool = False\n\ntask = Task("write notes")\nprint(task)\ntask.done = True\nprint(task)\nprint(task == Task("write notes", True))',
            "Task(title='write notes', done=False)\nTask(title='write notes', done=True)\nTrue",
            L("the same class as a dataclass", "वही क्लास डेटाक्लास के रूप में", "wahi class dataclass ke roop me"),
            note=L(
                "One decorator replaced the hand-written __init__, __repr__ and "
                "__eq__. The type hints also document the fields.",
                "एक डेकोरेटर ने हाथ से लिखे __init__, __repr__ और __eq__ की जगह ली। "
                "टाइप हिंट फ़ील्ड भी बताते हैं।",
                "Ek decorator ne haath se likhe __init__, __repr__ aur __eq__ ki jagah "
                "li. Type hints field bhi batate hain.",
            ),
        ),
    ],
    exercises=[
        task(
            L(
                "Turn `Book` into a dataclass with fields `title: str` and `pages: int` "
                "(default 100). Print `Book('Python')`.",
                "`Book` को डेटाक्लास बनाएँ जिसमें `title: str` और `pages: int` "
                "(डिफ़ॉल्ट 100) हों। `Book('Python')` प्रिंट करें।",
                "`Book` ko dataclass banao jisme `title: str` aur `pages: int` "
                "(default 100) hon. `Book('Python')` print karo.",
            ),
            "from dataclasses import dataclass\n\n# @dataclass\n# class Book:\n#     ...\n",
            "from dataclasses import dataclass\n\n@dataclass\nclass Book:\n    title: str\n    pages: int = 100\n\nprint(Book(\"Python\"))",
            [
                "Book('Python').pages == 100",
                "Book('X', 5).pages == 5",
                "Book('A') == Book('A')",
                "printed.strip() == \"Book(title='Python', pages=100)\"",
            ],
            L(
                "@dataclass above the class, then plain annotated fields with defaults.",
                "क्लास के ऊपर @dataclass, फिर डिफ़ॉल्ट के साथ सादे annotated फ़ील्ड।",
                "Class ke upar @dataclass, phir default ke saath saade annotated fields.",
            ),
        ),
    ],
    quiz_items=[
        quiz(
            L(
                "Which method controls what `print(obj)` shows?",
                "`print(obj)` क्या दिखाए, यह कौन सा मेथड तय करता है?",
                "`print(obj)` kya dikhaye, ye kaun sa method tay karta hai?",
            ),
            ["__init__", "__str__", "__eq__", __name__],
            "b",
            L(
                "__str__ is for humans; __repr__ is the developer-facing fallback and "
                "what containers show.",
                "__str__ इंसानों के लिए; __repr__ डेवलपर के लिए और कंटेनर वही दिखाते हैं।",
                "__str__ insaanon ke liye; __repr__ developer ke liye aur containers "
                "wahi dikhate hain.",
            ),
        ),
        quiz(
            L(
                "What does @dataclass generate?",
                "@dataclass क्या बनाता है?",
                "@dataclass kya banata hai?",
            ),
            [
                "only __init__",
                "__init__, __repr__ and __eq__ by default",
                "a database table",
                "getters and setters for every field",
            ],
            "b",
            L(
                "Those three are the default. You can ask for more with parameters "
                "such as frozen=True or order=True.",
                "ये तीन डिफ़ॉल्ट हैं। frozen=True या order=True जैसे पैरामीटर से और मँगा "
                "सकते हैं।",
                "Ye teen default hain. frozen=True ya order=True jaise parameters se "
                "aur maang sakte ho.",
            ),
        ),
        quiz(
            L(
                "Two objects with equal field values compare unequal. Which method is "
                "missing?",
                "समान फ़ील्ड मान वाले दो ऑब्जेक्ट बराबर नहीं माने जाते। कौन सा मेथड गायब है?",
                "Same field value wale do objects barabar nahi maane jate. Kaun sa "
                "method ghayab hai?",
            ),
            ["__repr__", "__eq__", "__init__", "__len__"],
            "b",
            L(
                "Default equality is identity, so value equality needs __eq__.",
                "डिफ़ॉल्ट समानता पहचान है, इसलिए मान की समानता के लिए __eq__ चाहिए।",
                "Default equality identity hai, isliye value equality ke liye __eq__ "
                "chahiye.",
            ),
        ),
    ],
    takeaway=L(
        "Learn the four dunders you will actually write (init, repr, eq, len) and let @dataclass write them when the class is mostly data.",
        "चार डंडर याद रखें जो सचमुच लिखेंगे (init, repr, eq, len); जब क्लास ज़्यादातर डेटा हो तो @dataclass से लिखवाएँ।",
        "Chaar dunder yaad rakho jo sachmuch likhoge (init, repr, eq, len); jab class zyadatar data ho to @dataclass se likhwao.",
    ),
)

MODULE = module(
    M,
    L("Classes and Objects", "क्लास और ऑब्जेक्ट", "Classes aur Objects"),
    L(
        "Build your own types: __init__ and self, attributes vs class attributes, "
        "inheritance with super(), and dataclasses for data-heavy classes.",
        "अपने टाइप बनाएँ: __init__ और self, एट्रिब्यूट बनाम क्लास एट्रिब्यूट, super() "
        "के साथ इनहेरिटेंस, और डेटा-भारी क्लास के लिए डेटाक्लास।",
        "Apne types banao: __init__ aur self, attributes vs class attributes, super() "
        "ke saath inheritance, aur data-heavy class ke liye dataclasses.",
    ),
    [
        chapter("m08c01", L("Objects and state", "ऑब्जेक्ट और स्थिति", "Objects aur state"), [l01, l02]),
        chapter("m08c02", L("Reuse and behaviour", "दोबारा इस्तेमाल और व्यवहार", "Reuse aur behaviour"), [l03, l04]),
    ],
    exam=[
        quiz(
            L("Which name refers to the current object inside a method?", "मेथड के अंदर मौजूदा ऑब्जेक्ट किस नाम से?", "Method ke andar maujooda object kis naam se?"),
            ["this", "self", "obj", "me"],
            "b",
            L("Python uses self by convention; the first parameter always receives the instance.", "पायथन में self परंपरा है; पहला पैरामीटर हमेशा इंस्टेंस पाता है।", "Python me self parampara hai; pehla parameter hamesha instance paata hai."),
        ),
        quiz(
            L("Which method is the constructor hook?", "कौन सा मेथड कंस्ट्रक्टर हुक है?", "Kaun sa method constructor hook hai?"),
            ["__new__ only", "__init__", "__start__", "__create__"],
            "b",
            L("__init__ initialises the object after it is created.", "__init__ बनने के बाद ऑब्जेक्ट को तैयार करता है।", "__init__ banne ke baad object ko taiyar karta hai."),
        ),
        quiz(
            L("`class Cat(Animal)` means:", "`class Cat(Animal)` का मतलब:", "`class Cat(Animal)` ka matlab:"),
            ["Cat contains Animal", "Cat inherits from Animal", "Animal inherits from Cat", "Cat is an alias of Animal"],
            "b",
            L("The name in brackets is the parent.", "कोष्ठक में नाम पैरेंट है।", "Koshtak me naam parent hai."),
        ),
        quiz(
            L("What does super().method() do?", "super().method() क्या करता है?", "super().method() kya karta hai?"),
            ["calls the subclass method again", "calls the parent version of the method", "creates a new object", "deletes the override"],
            "b",
            L("It reaches the parent implementation, which is how you extend instead of replace.", "यह पैरेंट के रूप तक पहुँचता है, इसी तरह बदलने की जगह बढ़ाते हैं।", "Ye parent ke roop tak pahunchta hai, isi tarah badalne ki jagah badhate hain."),
        ),
        quiz(
            L("Which decorator writes __init__, __repr__ and __eq__ for you?", "कौन सा डेकोरेटर __init__, __repr__ और __eq__ लिख देता है?", "Kaun sa decorator __init__, __repr__ aur __eq__ likh deta hai?"),
            ["@property", "@dataclass", "@staticmethod", "@classmethod"],
            "b",
            L("@dataclass from the dataclasses module.", "dataclasses मॉड्यूल से @dataclass।", "dataclasses module se @dataclass."),
        ),
        quiz(
            L("A method that changes self.value must:", "self.value बदलने वाला मेथड:", "self.value badalne wala method:"),
            ["return a new object", "assign to self.value", "declare global value", "use nonlocal"],
            "b",
            L("Assignment on self stores the change on that object.", "self पर असाइन करने से बदलाव उसी ऑब्जेक्ट पर रहता है।", "self par assign karne se badlav usi object par rehta hai."),
        ),
    ],
    icon="🏗️",
)
