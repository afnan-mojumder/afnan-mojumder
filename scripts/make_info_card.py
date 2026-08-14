#!/usr/bin/env python3
"""
make_info_card.py
Hand-authors a small SVG that looks like the output of `neofetch`: a title
bar, then colored key/value rows. Each line fades and slides in on a short
stagger so the panel looks like it's printing next to the portrait.

Content lives here (edit CONFIG below), not in the contribution graph —
that already covers the stats numbers can't tell a story with.

STATIC=1 env var emits a frozen (no-animation) frame, useful for local
Quick Look previews.
"""
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")
STATIC = os.environ.get("STATIC") == "1"

BG = "#0d1117"
BORDER = "#30363d"
TITLE_DOT_COLORS = ["#ff5f56", "#ffbd2e", "#27c93f"]
LABEL_COLOR = "#39d353"      # neofetch-style accent for keys
VALUE_COLOR = "#c9d1d9"
MUTED = "#8b949e"
PROMPT_COLOR = "#58a6ff"

WIDTH = 490
ROW_H = 24
PAD_X = 20
TITLEBAR_H = 34

CONFIG = {
    "user": "afnan@github",
    "rows": [
        ("Name", "Afnan Mojumder"),
        ("Now", "Learning PHP, SQL & Dart"),
        ("Prev", "HTML / CSS fundamentals"),
        ("Stack", "HTML · CSS · PHP · MySQL · Dart"),
        ("Highlight", "campus_flow — PHP + MySQL project"),
        ("Status", "Just started — building in public"),
        ("Timezone", "UTC+6 (Bangladesh)"),
    ],
}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def render():
    rows = CONFIG["rows"]
    height = TITLEBAR_H + len(rows) * ROW_H + 20

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="SFMono-Regular, Consolas, Menlo, monospace">'
    )

    # Card background + border
    parts.append(
        f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{height-1}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    )

    # Title bar
    parts.append(f'<rect x="0.5" y="0.5" width="{WIDTH-1}" height="{TITLEBAR_H}" rx="10" fill="#161b22"/>')
    parts.append(f'<rect x="0.5" y="{TITLEBAR_H-10}" width="{WIDTH-1}" height="10" fill="#161b22"/>')
    for i, c in enumerate(TITLE_DOT_COLORS):
        parts.append(f'<circle cx="{18 + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{c}"/>')
    parts.append(
        f'<text x="{WIDTH/2}" y="{TITLEBAR_H/2 + 4}" text-anchor="middle" font-size="11" '
        f'fill="{MUTED}">{esc(CONFIG["user"])}</text>'
    )

    # style block for stagger fade/slide-in
    parts.append("<style>")
    if not STATIC:
        parts.append(
            ".row{opacity:0;animation:printin .4s ease-out forwards;}"
            "@keyframes printin{from{opacity:0;transform:translateX(-6px);}to{opacity:1;transform:translateX(0);}}"
        )
    parts.append("</style>")

    y = TITLEBAR_H + 24
    max_label_len = max(len(k) for k, _ in rows)
    for i, (key, val) in enumerate(rows):
        delay = i * 0.09
        style = "" if STATIC else f' style="animation-delay:{delay:.2f}s"'
        row_class = "" if STATIC else ' class="row"'
        parts.append(f'<g{row_class}{style}>')
        parts.append(
            f'<text x="{PAD_X}" y="{y}" font-size="13" font-weight="600" fill="{LABEL_COLOR}">{esc(key)}</text>'
        )
        label_px = PAD_X + (max_label_len + 1) * 8
        parts.append(
            f'<text x="{label_px}" y="{y}" font-size="13" fill="{VALUE_COLOR}">{esc(val)}</text>'
        )
        parts.append("</g>")
        y += ROW_H

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg = render()
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH}{' (static)' if STATIC else ''}")


if __name__ == "__main__":
    main()
