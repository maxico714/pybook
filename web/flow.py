"""Draw a code-flow diagram for a snippet, straight from its syntax tree.

This is the "code flow" half of the visual pair: the step-through player shows
what happens *when* code runs, and this shows how the code is *shaped* - which
statements run in order, what is nested inside a loop, where the loop jumps back
to.  It is generated, never hand-drawn, so a new example gets a diagram for free.

Standard library only: :mod:`ast` for the structure and hand-written SVG.
"""
from __future__ import annotations

import ast
import html

WIDTH = 660
ROW = 34
BOX_H = 22
PAD = 14
INDENT = 30
MAX_NODES = 44

KIND_FILL = {
    "loop": "#fdf3d8",
    "loop-line": "#b45309",
    "branch": "#e8efff",
    "branch-line": "#2563eb",
    "def": "#e7f6ec",
    "def-line": "#15803d",
    "stop": "#fdeceb",
    "stop-line": "#b42318",
    "plain": "#ffffff",
    "plain-line": "#cbd5e1",
}
TEXT = "#0f172a"
MUTED = "#5b6b82"
LINE = "#94a3b8"


def _kind(node) -> str:
    if isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
        return "loop"
    if isinstance(node, (ast.If, ast.Try, ast.With, ast.AsyncWith)):
        return "branch"
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return "def"
    if isinstance(node, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
        return "stop"
    return "plain"


def _label(node) -> str:
    try:
        text = ast.unparse(node)
    except Exception:  # pragma: no cover - unparse is total in practice
        return type(node).__name__
    first = text.split("\n")[0].strip()
    if isinstance(node, (ast.If, ast.While)) and len(first) > 48:
        first = first[:45] + "…"
    if isinstance(node, (ast.For, ast.AsyncFor)) and len(first) > 48:
        first = first[:45] + "…"
    return first


def _walk(body, depth: int, nodes: list, loops: list) -> None:
    for statement in body:
        index = len(nodes)
        nodes.append(
            {"depth": depth, "label": _label(statement), "kind": _kind(statement), "loop": False}
        )
        if len(nodes) > MAX_NODES:
            return

        if isinstance(statement, (ast.For, ast.AsyncFor, ast.While)):
            nodes[index]["loop"] = True
            start = len(nodes)
            _walk(statement.body, depth + 1, nodes, loops)
            if len(nodes) > start:
                loops.append((index, start, len(nodes) - 1))
            _walk(statement.orelse, depth + 1, nodes, loops)
        elif isinstance(statement, ast.If):
            _walk(statement.body, depth + 1, nodes, loops)
            _walk(statement.orelse, depth + 1, nodes, loops)
        elif isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            _walk(statement.body, depth + 1, nodes, loops)
        elif isinstance(statement, (ast.Try,)):
            _walk(statement.body, depth + 1, nodes, loops)
            for handler in statement.handlers:
                _walk(handler.body, depth + 1, nodes, loops)
            _walk(statement.finalbody, depth + 1, nodes, loops)
        elif isinstance(statement, (ast.With, ast.AsyncWith)):
            _walk(statement.body, depth + 1, nodes, loops)


def _truncate(text: str, room: int) -> str:
    limit = max(8, int(room / 6.1))
    return text if len(text) <= limit else text[: limit - 1] + "…"


def flow_svg(code: str, width: int = WIDTH) -> str:
    """Return an SVG diagram of ``code``, or an empty string when it cannot parse."""
    source = (code or "").strip("\n")
    if not source:
        return ""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ""

    nodes: list[dict] = []
    loops: list[tuple[int, int, int]] = []
    _walk(tree.body, 0, nodes, loops)
    if not nodes:
        return ""

    height = PAD * 2 + len(nodes) * ROW
    parts: list[str] = [
        '<svg viewBox="0 0 %d %d" width="100%%" role="img" '
        'aria-label="Code flow diagram" xmlns="http://www.w3.org/2000/svg" '
        'font-family="ui-monospace, Consolas, monospace">' % (width, height),
        "<defs><marker id='ah' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' "
        "markerHeight='6' orient='auto-start-reverse'>"
        "<path d='M 0 0 L 10 5 L 0 10 z' fill='%s'/></marker>"
        "<marker id='ah2' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' "
        "markerHeight='6' orient='auto-start-reverse'>"
        "<path d='M 0 0 L 10 5 L 0 10 z' fill='#b45309'/></marker></defs>" % LINE,
    ]

    for index, node in enumerate(nodes):
        x = PAD + node["depth"] * INDENT
        y = PAD + index * ROW
        box_width = max(150, width - x - PAD - 8)
        fill = KIND_FILL[node["kind"]]
        stroke = KIND_FILL[node["kind"] + "-line"]
        parts.append(
            "<rect x='%d' y='%d' width='%d' height='%d' rx='6' fill='%s' stroke='%s' "
            "stroke-width='1.2'/>" % (x, y, box_width, BOX_H, fill, stroke)
        )
        parts.append(
            "<text x='%d' y='%d' font-size='11.5' fill='%s'>%s</text>"
            % (x + 9, y + 15, TEXT, html.escape(_truncate(node["label"], box_width - 20)))
        )
        if node["loop"]:
            parts.append(
                "<text x='%d' y='%d' font-size='10' fill='%s' text-anchor='end'>↺ repeat</text>"
                % (x + box_width - 8, y + 15, KIND_FILL["loop-line"])
            )

        if index + 1 < len(nodes):
            next_node = nodes[index + 1]
            nx = PAD + next_node["depth"] * INDENT
            ny = PAD + (index + 1) * ROW
            sx, sy = x + 12, y + BOX_H
            if nx == x:
                parts.append(
                    "<line x1='%d' y1='%d' x2='%d' y2='%d' stroke='%s' stroke-width='1.2' "
                    "marker-end='url(#ah)'/>" % (sx, sy, nx + 12, ny, LINE)
                )
            else:
                mid = sy + (ny - sy) / 2
                parts.append(
                    "<path d='M %d %d L %d %.1f L %d %.1f L %d %d' fill='none' stroke='%s' "
                    "stroke-width='1.2' marker-end='url(#ah)'/>"
                    % (sx, sy, sx, mid, nx + 12, mid, nx + 12, ny, LINE)
                )

    for loop_index, first_child, last_child in loops:
        loop_node = nodes[loop_index]
        lx = PAD + loop_node["depth"] * INDENT
        ly = PAD + loop_index * ROW + BOX_H / 2
        child = nodes[last_child]
        cx = PAD + child["depth"] * INDENT
        cy = PAD + last_child * ROW + BOX_H
        rail = lx - 11
        parts.append(
            "<path d='M %d %d L %d %d L %d %.1f' fill='none' stroke='%s' stroke-width='1.2' "
            "stroke-dasharray='4 3' marker-end='url(#ah2)'/>"
            % (cx, cy, rail, cy, rail, ly, KIND_FILL["loop-line"])
        )

    parts.append("</svg>")
    return "".join(parts)
