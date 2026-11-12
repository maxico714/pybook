"""Original SVG diagrams for the course.

Every diagram here is hand-authored markup written for this project, so there
is no third-party asset licence to honour: they ship under the same MIT licence
as the notebook.  They are inline SVG (a few KB each) with CSS keyframe
animations, which render in classic Jupyter and in Colab without any extra
package, server or network request.

Design rules followed (WCAG 2.2):
  * text is real <text>, so it scales and is selectable
  * meaning is never carried by colour alone - every colour is paired with a
    label or a shape difference
  * foreground/background pairs are >= 4.5:1 contrast
  * each diagram is wrapped in a <figure> with a visible caption, and the
    runtime passes an aria-label derived from the caption
"""
from __future__ import annotations

FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
UI = "system-ui,-apple-system,Segoe UI,Roboto,sans-serif"

# palette: dark ink on light fills, all pairs >= 4.5:1
INK = "#0f172a"
MUTED = "#334155"
BLUE = "#1d4ed8"
BLUE_FILL = "#dbeafe"
GREEN = "#166534"
GREEN_FILL = "#dcfce7"
AMBER = "#92400e"
AMBER_FILL = "#fef3c7"
RED = "#991b1b"
RED_FILL = "#fee2e2"
PURPLE = "#5b21b6"
PURPLE_FILL = "#ede9fe"


def _figure(body: str, caption: str, width: int = 640, height: int = 220) -> str:
    return (
        f'<figure style="margin:10px 0;padding:8px;border:1px solid #e2e8f0;'
        f'border-radius:10px;background:#fbfdff;max-width:{width}px">'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="100%" role="img" aria-label="{caption}" '
        f'style="font-family:{UI};max-width:100%;height:auto">'
        f"<style>"
        f".pulse{{animation:pulse 2.4s ease-in-out infinite}}"
        f"@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}"
        f".slide{{animation:slide 3s ease-in-out infinite}}"
        f"@keyframes slide{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(120px)}}}}"
        f".dash{{animation:dash 2s linear infinite}}"
        f"@keyframes dash{{to{{stroke-dashoffset:-24}}}}"
        f".spin{{animation:spin 6s linear infinite;transform-origin:center}}"
        f"@keyframes spin{{to{{transform:rotate(360deg)}}}}"
        f".fade{{animation:fade 4s ease-in-out infinite}}"
        f"@keyframes fade{{0%,45%{{opacity:1}}55%,100%{{opacity:.25}}}}"
        f"</style>"
        f"{body}</svg>"
        f'<figcaption style="font-size:12.5px;color:{MUTED};padding:6px 2px 0">'
        f"{caption}</figcaption></figure>"
    )


def _box(x, y, w, h, label, fill=BLUE_FILL, stroke=BLUE, sub="", fs=14):
    sub_el = (
        f'<text x="{x + w / 2}" y="{y + h / 2 + 16}" text-anchor="middle" '
        f'font-size="11" fill="{MUTED}">{sub}</text>'
        if sub
        else ""
    )
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="1.5"/>'
        f'<text x="{x + w / 2}" y="{y + h / 2 + (0 if not sub else -2)}" text-anchor="middle" '
        f'font-size="{fs}" font-weight="600" fill="{stroke}">{label}</text>{sub_el}'
    )


def _arrow(x1, y1, x2, y2, colour=MUTED, dashed=False, curve=None):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    if curve:
        path = f'M {x1} {y1} Q {curve[0]} {curve[1]} {x2} {y2}'
        return (
            f'<path d="{path}" fill="none" stroke="{colour}" stroke-width="2" '
            f'marker-end="url(#ah)"{dash}/>'
        )
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" '
        f'stroke-width="2" marker-end="url(#ah)"{dash}/>'
    )


DEFS = (
    '<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="8" refY="4.5" '
    f'orient="auto"><path d="M0,0 L9,4.5 L0,9 z" fill="{MUTED}"/></marker></defs>'
)


# --------------------------------------------------------------------- diagrams

def variables() -> str:
    body = (
        DEFS
        + _box(40, 40, 150, 70, "name", BLUE_FILL, BLUE, "the label")
        + _box(240, 40, 150, 70, '"Ada"', GREEN_FILL, GREEN, "the value")
        + _arrow(192, 75, 236, 75)
        + f'<text x="40" y="150" font-size="12.5" fill="{MUTED}">'
        f"name = &quot;Ada&quot;</text>"
        + f'<text x="40" y="172" font-size="12.5" fill="{MUTED}">'
        f"name = &quot;Grace&quot;  →  the label now points at a new value</text>"
        + _box(240, 130, 150, 40, '"Grace"', AMBER_FILL, AMBER)
        + _arrow(192, 150, 236, 150, AMBER, dashed=True)
        + f'<g class="pulse">{_box(470, 85, 130, 60, "reuse", PURPLE_FILL, PURPLE, "same name")}</g>'
    )
    return _figure(body, "A variable is a name pointing at a value, not a box that owns it.", 640, 200)


def types() -> str:
    rows = [
        ("int", "42", BLUE, BLUE_FILL),
        ("float", "3.14", GREEN, GREEN_FILL),
        ("str", '"hello"', PURPLE, PURPLE_FILL),
        ("bool", "True", AMBER, AMBER_FILL),
        ("NoneType", "None", RED, RED_FILL),
    ]
    body = DEFS + "".join(
        _box(30 + i * 120, 50, 108, 64, name, fill, stroke, value)
        for i, (name, value, stroke, fill) in enumerate(rows)
    )
    body += (
        f'<text x="30" y="150" font-size="12.5" fill="{MUTED}">'
        "type(value) tells you which one you have - never guess, just check.</text>"
    )
    return _figure(body, "The five built-in value types you meet first, with an example of each.", 640, 180)


def if_flow() -> str:
    body = (
        DEFS
        + _box(30, 85, 130, 56, "condition", AMBER_FILL, AMBER)
        + f'<polygon points="230,70 320,113 230,156 140,113" fill="{BLUE_FILL}" stroke="{BLUE}" stroke-width="1.5"/>'
        + f'<text x="230" y="118" text-anchor="middle" font-size="12.5" font-weight="600" fill="{BLUE}">True?</text>'
        + _arrow(162, 113, 137, 113)
        + _arrow(322, 100, 420, 70)
        + _arrow(322, 126, 420, 160)
        + _box(420, 42, 170, 56, "run if-block", GREEN_FILL, GREEN)
        + _box(420, 138, 170, 56, "try elif / else", RED_FILL, RED)
        + f'<text x="330" y="88" font-size="11.5" fill="{GREEN}">True</text>'
        + f'<text x="330" y="152" font-size="11.5" fill="{RED}">False</text>'
        + '<g class="pulse">'
        + _arrow(140, 160, 260, 160, BLUE, dashed=True, curve=(200, 190))
        + "</g>"
    )
    return _figure(body, "if asks one yes/no question; only the matching branch runs.", 640, 210)


def loop_flow() -> str:
    body = (
        DEFS
        + f'<circle cx="300" cy="105" r="72" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 4" class="dash"/>'
        + _box(240, 78, 120, 54, "body", GREEN_FILL, GREEN, "runs again")
        + _box(60, 78, 130, 54, "next item?", AMBER_FILL, AMBER)
        + _arrow(190, 105, 236, 105)
        + _arrow(300, 78, 300, 30, BLUE)
        + f'<text x="308" y="24" font-size="11.5" fill="{MUTED}">more items</text>'
        + _arrow(300, 176, 300, 196, RED)
        + _box(238, 196, 124, 44, "loop ends", RED_FILL, RED)
        + f'<text x="440" y="90" font-size="12.5" fill="{MUTED}">for item in items:</text>'
        + f'<text x="440" y="112" font-size="12.5" fill="{MUTED}">    do_work(item)</text>'
        + f'<text x="440" y="140" font-size="11.5" fill="{MUTED}">break → leave now</text>'
        + f'<text x="440" y="160" font-size="11.5" fill="{MUTED}">continue → skip to next</text>'
    )
    return _figure(body, "A loop repeats the body, then asks again: is there another item?", 640, 250)


def list_index() -> str:
    items = ["'a'", "'b'", "'c'", "'d'", "'e'"]
    body = DEFS
    for i, item in enumerate(items):
        body += _box(40 + i * 110, 50, 96, 56, item, BLUE_FILL, BLUE, f"index {i}")
    body += (
        f'<text x="40" y="140" font-size="12.5" fill="{MUTED}">'
        f"names[0] → 'a'&nbsp;&nbsp;&nbsp; names[-1] → 'e'</text>"
        f'<text x="40" y="164" font-size="12.5" fill="{MUTED}">'
        f"names[1:4] → ['b', 'c', 'd']&nbsp;&nbsp;&nbsp; stop index is excluded</text>"
        + '<g class="pulse">'
        + f'<rect x="40" y="50" width="96" height="56" rx="8" fill="none" stroke="{AMBER}" stroke-width="3"/>'
        + "</g>"
    )
    return _figure(body, "Counting starts at 0, and a slice stops before its end index.", 640, 190)


def dict_map() -> str:
    body = (
        DEFS
        + _box(30, 50, 140, 54, '"name"', PURPLE_FILL, PURPLE)
        + _box(30, 120, 140, 54, '"age"', PURPLE_FILL, PURPLE)
        + _box(320, 50, 180, 54, '"Ada"', GREEN_FILL, GREEN)
        + _box(320, 120, 180, 54, "36", GREEN_FILL, GREEN)
        + _arrow(172, 77, 316, 77)
        + _arrow(172, 147, 316, 147)
        + f'<text x="200" y="40" font-size="11.5" fill="{MUTED}">key</text>'
        + f'<text x="360" y="40" font-size="11.5" fill="{MUTED}">value</text>'
        + f'<text x="200" y="200" font-size="12.5" fill="{MUTED}">person[&quot;name&quot;] → &quot;Ada&quot;</text>'
    )
    return _figure(body, "A dictionary maps a key to a value; the key is how you look it up.", 640, 220)


def function_call() -> str:
    body = (
        DEFS
        + _box(20, 80, 120, 54, "3, 4", AMBER_FILL, AMBER, "arguments")
        + _box(210, 62, 190, 90, "add(a, b)", BLUE_FILL, BLUE, "function body")
        + _box(460, 80, 140, 54, "7", GREEN_FILL, GREEN, "return value")
        + _arrow(142, 107, 206, 107)
        + _arrow(402, 107, 456, 107)
        + '<g class="slide">'
        + f'<circle cx="150" cy="170" r="7" fill="{PURPLE}"/>'
        + "</g>"
        + f'<text x="20" y="200" font-size="12.5" fill="{MUTED}">'
        f"input goes in, one job happens inside, one value comes out.</text>"
    )
    return _figure(body, "A function is a machine: arguments in, one return value out.", 640, 215)


def scope_legb() -> str:
    body = (
        DEFS
        + f'<rect x="20" y="20" width="600" height="180" rx="10" fill="#f8fafc" stroke="{MUTED}" stroke-dasharray="5 4"/>'
        + f'<text x="34" y="42" font-size="12" fill="{MUTED}">module scope (global)</text>'
        + f'<rect x="120" y="60" width="400" height="120" rx="10" fill="{BLUE_FILL}" stroke="{BLUE}"/>'
        + f'<text x="134" y="82" font-size="12" fill="{BLUE}">enclosing function</text>'
        + f'<rect x="220" y="100" width="220" height="62" rx="10" fill="{GREEN_FILL}" stroke="{GREEN}"/>'
        + f'<text x="234" y="122" font-size="12" fill="{GREEN}">local scope</text>'
        + f'<text x="234" y="146" font-size="11.5" fill="{MUTED}">found here first</text>'
        + f'<text x="430" y="196" font-size="11.5" fill="{MUTED}">lookup order: local → enclosing → global → builtins</text>'
    )
    return _figure(body, "Python looks a name up from the inside out: local, enclosing, global, builtins.", 640, 220)


def alias_copy() -> str:
    body = (
        DEFS
        + _box(40, 40, 110, 50, "a", BLUE_FILL, BLUE)
        + _box(40, 120, 110, 50, "b = a", BLUE_FILL, BLUE)
        + _box(280, 80, 150, 50, "['x', 'y']", AMBER_FILL, AMBER, "one list")
        + _arrow(152, 65, 276, 95)
        + _arrow(152, 145, 276, 115)
        + f'<text x="470" y="70" font-size="12" fill="{RED}">b is a → True</text>'
        + f'<text x="470" y="92" font-size="12" fill="{RED}">b.append(1) changes both</text>'
        + _box(470, 120, 130, 44, "b = a[:]", GREEN_FILL, GREEN, "a copy")
        + f'<text x="470" y="186" font-size="12" fill="{GREEN}">b is a → False</text>'
    )
    return _figure(body, "Two names can point at one list; a copy makes a second list.", 640, 210)


def exception_flow() -> str:
    body = (
        DEFS
        + _box(20, 90, 110, 52, "try", BLUE_FILL, BLUE)
        + _box(180, 30, 150, 48, "no error", GREEN_FILL, GREEN)
        + _box(180, 150, 150, 48, "error raised", RED_FILL, RED)
        + _box(380, 150, 140, 48, "except runs", AMBER_FILL, AMBER)
        + _box(380, 30, 140, 48, "else runs", GREEN_FILL, GREEN)
        + _box(560, 90, 60, 48, "finally", PURPLE_FILL, PURPLE)
        + _arrow(132, 105, 176, 60)
        + _arrow(132, 125, 176, 168)
        + _arrow(332, 54, 376, 54)
        + _arrow(332, 174, 376, 174)
        + _arrow(452, 150, 556, 122)
        + _arrow(452, 54, 556, 96)
        + '<g class="pulse">'
        + f'<rect x="176" y="146" width="158" height="56" rx="8" fill="none" stroke="{RED}" stroke-width="3"/>'
        + "</g>"
    )
    return _figure(body, "try runs once; exactly one of except or else runs; finally always runs.", 640, 220)


def mutable_default() -> str:
    body = (
        DEFS
        + _box(20, 40, 170, 60, "def add(x, box=[])", BLUE_FILL, BLUE)
        + _box(300, 40, 180, 60, "[] created once", AMBER_FILL, AMBER)
        + _arrow(192, 70, 296, 70)
        + _box(300, 130, 180, 60, "same list, 2nd call", RED_FILL, RED)
        + _arrow(300, 100, 300, 126, RED, dashed=True)
        + f'<text x="510" y="62" font-size="12" fill="{RED}">call 1 → [1]</text>'
        + f'<text x="510" y="84" font-size="12" fill="{RED}">call 2 → [1, 2]</text>'
        + f'<text x="510" y="112" font-size="11.5" fill="{GREEN}">fix: box=None</text>'
        + f'<text x="20" y="180" font-size="12" fill="{MUTED}">'
        f"the default value is evaluated once, when the function is defined.</text>"
    )
    return _figure(body, "A mutable default argument is shared by every call - a classic trap.", 640, 200)


def comprehension() -> str:
    body = (
        DEFS
        + _box(20, 60, 150, 52, "numbers", BLUE_FILL, BLUE)
        + _box(210, 60, 120, 52, "keep even", AMBER_FILL, AMBER)
        + _box(370, 60, 130, 52, "x * x", GREEN_FILL, GREEN)
        + _box(540, 60, 90, 52, "list", PURPLE_FILL, PURPLE)
        + _arrow(172, 86, 206, 86)
        + _arrow(332, 86, 366, 86)
        + _arrow(502, 86, 536, 86)
        + f'<text x="20" y="140" font-size="12.5" fill="{MUTED}">'
        f"[x * x for x in numbers if x % 2 == 0]</text>"
        + '<g class="fade">'
        + _box(210, 140, 120, 44, "filtered", AMBER_FILL, AMBER)
        + "</g>"
        + f'<text x="350" y="168" font-size="11.5" fill="{MUTED}">one readable line instead of a 4-line loop</text>'
    )
    return _figure(body, "A comprehension does map, filter and collect in a single expression.", 640, 190)


def generator_lazy() -> str:
    body = (
        DEFS
        + _box(20, 50, 160, 60, "generator", BLUE_FILL, BLUE, "no list yet")
        + _box(300, 20, 120, 40, "1", GREEN_FILL, GREEN)
        + _box(300, 72, 120, 40, "2", GREEN_FILL, GREEN)
        + _box(300, 124, 120, 40, "3", GREEN_FILL, GREEN)
        + _arrow(182, 80, 296, 40)
        + _arrow(182, 80, 296, 92)
        + _arrow(182, 80, 296, 144)
        + f'<text x="440" y="46" font-size="11.5" fill="{MUTED}">next() → 1</text>'
        + f'<text x="440" y="98" font-size="11.5" fill="{MUTED}">next() → 2</text>'
        + f'<text x="440" y="150" font-size="11.5" fill="{MUTED}">next() → 3</text>'
        + f'<text x="20" y="190" font-size="12" fill="{MUTED}">'
        f"values are produced on demand, so memory stays flat.</text>"
        + '<g class="pulse">'
        + f'<circle cx="240" cy="80" r="6" fill="{AMBER}"/>'
        + "</g>"
    )
    return _figure(body, "A generator hands out one value per next() call instead of building a list.", 640, 210)


def class_object() -> str:
    body = (
        DEFS
        + _box(20, 70, 150, 70, "class Dog", PURPLE_FILL, PURPLE, "blueprint")
        + _box(260, 20, 170, 56, "dog1: Rex", GREEN_FILL, GREEN)
        + _box(260, 90, 170, 56, "dog2: Moti", GREEN_FILL, GREEN)
        + _box(260, 160, 170, 56, "dog3: ...", GREEN_FILL, GREEN)
        + _arrow(172, 90, 256, 50)
        + _arrow(172, 105, 256, 118)
        + _arrow(172, 120, 256, 186, dashed=True)
        + f'<text x="460" y="52" font-size="12" fill="{MUTED}">each object has its own data</text>'
        + f'<text x="460" y="76" font-size="12" fill="{MUTED}">all share the methods</text>'
        + '<g class="pulse">'
        + _box(20, 160, 150, 50, "methods", BLUE_FILL, BLUE)
        + "</g>"
    )
    return _figure(body, "A class is the blueprint; each object is one thing built from it.", 640, 230)


def async_tasks() -> str:
    body = (
        DEFS
        + f'<text x="20" y="40" font-size="12" fill="{MUTED}">task A</text>'
        + f'<text x="20" y="100" font-size="12" fill="{MUTED}">task B</text>'
        + f'<rect x="90" y="24" width="150" height="26" rx="5" fill="{BLUE_FILL}" stroke="{BLUE}"/>'
        + f'<text x="165" y="42" text-anchor="middle" font-size="11" fill="{BLUE}">network wait</text>'
        + f'<rect x="250" y="24" width="140" height="26" rx="5" fill="{BLUE_FILL}" stroke="{BLUE}"/>'
        + f'<text x="320" y="42" text-anchor="middle" font-size="11" fill="{BLUE}">more work</text>'
        + f'<rect x="90" y="84" width="300" height="26" rx="5" fill="{GREEN_FILL}" stroke="{GREEN}"/>'
        + f'<text x="240" y="102" text-anchor="middle" font-size="11" fill="{GREEN}">runs while A is waiting</text>'
        + f'<text x="410" y="42" font-size="11.5" fill="{MUTED}">await = pause here, let others run</text>'
        + f'<text x="410" y="102" font-size="11.5" fill="{MUTED}">one thread, no blocking</text>'
        + f'<line x1="90" y1="140" x2="390" y2="140" stroke="{MUTED}" stroke-dasharray="4 4"/>'
        + f'<text x="90" y="160" font-size="11" fill="{MUTED}">time →</text>'
    )
    return _figure(body, "async/await lets one task wait while another one uses the time.", 640, 180)


def files_with() -> str:
    body = (
        DEFS
        + _box(20, 60, 120, 54, "open()", BLUE_FILL, BLUE)
        + _box(200, 60, 180, 54, "with block", GREEN_FILL, GREEN, "file is open")
        + _box(440, 60, 170, 54, "auto close", PURPLE_FILL, PURPLE, "even on error")
        + _arrow(142, 87, 196, 87)
        + _arrow(382, 87, 436, 87)
        + f'<text x="20" y="160" font-size="12.5" fill="{MUTED}">'
        f"with open(&quot;notes.txt&quot;, &quot;r&quot;, encoding=&quot;utf-8&quot;) as f:</text>"
        + f'<text x="20" y="182" font-size="12.5" fill="{MUTED}">    text = f.read()</text>'
    )
    return _figure(body, "The with statement closes the file for you, even if the block raises.", 640, 200)


VISUALS: dict[str, tuple[str, dict[str, str]]] = {
    "variables": (variables(), {
        "en": "A variable is a name pointing at a value.",
        "hi": "वेरिएबल एक नाम है जो किसी वैल्यू की ओर इशारा करता है।",
        "hinglish": "Variable ek naam hai jo value ki taraf point karta hai.",
    }),
    "types": (types(), {
        "en": "The five core value types.",
        "hi": "पाँच मुख्य वैल्यू टाइप।",
        "hinglish": "Paanch core value types.",
    }),
    "if_flow": (if_flow(), {
        "en": "Only one branch of an if/elif/else runs.",
        "hi": "if/elif/else में सिर्फ़ एक शाखा चलती है।",
        "hinglish": "if/elif/else me sirf ek branch chalti hai.",
    }),
    "loop_flow": (loop_flow(), {
        "en": "A loop repeats until there are no items left.",
        "hi": "लूप तब तक दोहराता है जब तक आइटम बचे हैं।",
        "hinglish": "Loop tab tak repeat karta hai jab tak items bache hain.",
    }),
    "list_index": (list_index(), {
        "en": "Indexing starts at 0; slices exclude the stop index.",
        "hi": "इंडेक्स 0 से शुरू होता है; स्लाइस का अंत शामिल नहीं होता।",
        "hinglish": "Index 0 se shuru hota hai; slice ka end include nahi hota.",
    }),
    "dict_map": (dict_map(), {
        "en": "A dict maps keys to values.",
        "hi": "डिक्शनरी की को वैल्यू से जोड़ती है।",
        "hinglish": "Dict key ko value se jodta hai.",
    }),
    "function_call": (function_call(), {
        "en": "Arguments in, one return value out.",
        "hi": "आर्ग्युमेंट अंदर, एक रिटर्न वैल्यू बाहर।",
        "hinglish": "Arguments andar, ek return value bahar.",
    }),
    "scope_legb": (scope_legb(), {
        "en": "Name lookup goes local, enclosing, global, builtins.",
        "hi": "नाम की खोज local, enclosing, global, builtins क्रम में होती है।",
        "hinglish": "Naam ki lookup local, enclosing, global, builtins ke order me hoti hai.",
    }),
    "alias_copy": (alias_copy(), {
        "en": "Two names, one list versus a real copy.",
        "hi": "दो नाम एक ही लिस्ट पर, बनाम असली कॉपी।",
        "hinglish": "Do naam ek hi list par, versus asli copy.",
    }),
    "exception_flow": (exception_flow(), {
        "en": "try, except, else and finally paths.",
        "hi": "try, except, else और finally के रास्ते।",
        "hinglish": "try, except, else aur finally ke raste.",
    }),
    "mutable_default": (mutable_default(), {
        "en": "A mutable default argument is created once and shared.",
        "hi": "म्यूटेबल डिफ़ॉल्ट आर्ग्युमेंट एक बार बनता है और साझा रहता है।",
        "hinglish": "Mutable default argument ek baar banta hai aur share hota hai.",
    }),
    "comprehension": (comprehension(), {
        "en": "A comprehension maps, filters and collects in one line.",
        "hi": "कॉम्प्रिहेंशन एक पंक्ति में map, filter और collect करता है।",
        "hinglish": "Comprehension ek line me map, filter aur collect karta hai.",
    }),
    "generator_lazy": (generator_lazy(), {
        "en": "A generator produces values on demand.",
        "hi": "जनरेटर माँगने पर वैल्यू बनाता है।",
        "hinglish": "Generator maangne par value banata hai.",
    }),
    "class_object": (class_object(), {
        "en": "A class is a blueprint; objects are built from it.",
        "hi": "क्लास एक ब्लूप्रिंट है; ऑब्जेक्ट उससे बनते हैं।",
        "hinglish": "Class ek blueprint hai; object usse bante hain.",
    }),
    "async_tasks": (async_tasks(), {
        "en": "await pauses one task so another can run.",
        "hi": "await एक टास्क को रोकता है ताकि दूसरा चल सके।",
        "hinglish": "await ek task ko roakta hai taaki doosra chal sake.",
    }),
    "files_with": (files_with(), {
        "en": "with closes the file automatically.",
        "hi": "with फ़ाइल को अपने आप बंद कर देता है।",
        "hinglish": "with file ko apne aap band kar deta hai.",
    }),
}
