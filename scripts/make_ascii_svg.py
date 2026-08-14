#!/usr/bin/env python3
"""
make_ascii_svg.py
Downsamples the prepped image to a character grid (~100 wide) and picks a
glyph per pixel from a density ramp (sparse chars for bright areas, dense
for dark). Monochrome + high contrast keeps it looking like a clean
portrait instead of noisy rainbow ASCII art.

Animation: each row is wrapped in a horizontal clip that wipes left-to-
right (a small block "cursor" rides the wipe edge), staggered top to
bottom. The whole portrait prints once and freezes — no looping. It's
SMIL inside the SVG, which GitHub renders fine.

Usage:
    python scripts/make_ascii_svg.py source-prepped.png
Output:
    avi-ascii.svg   (edit OUT_PATH below, or pass a second CLI arg)
"""
import sys
import os

from PIL import Image, ImageFilter

# bright (sparse) -> dark (dense). Leading space clears the background to nothing.
RAMP = " .`:-=+*cs#%@"

GRID_W = 100          # characters wide
CHAR_W = 6.2           # px per character cell (monospace-ish)
CHAR_H = 11
FONT_SIZE = 11
COLOR = "#8b949e"      # single light-gray fill; no per-char rainbow

ROW_DURATION = 0.9     # seconds for one row's wipe
ROW_STAGGER = 0.045    # seconds between successive row starts


def load_and_downsample(path: str):
    img = Image.open(path).convert("L")
    w, h = img.size

    # Fine, high-contrast texture (e.g. tweed/woven fabric) aliases into
    # noisy speckle once downsampled to a coarse character grid. A mild
    # blur proportional to the downscale factor removes that high-frequency
    # detail while leaving facial features (much lower spatial frequency)
    # intact.
    downscale_factor = w / GRID_W
    blur_radius = max(0.0, downscale_factor / 6.0)
    if blur_radius > 0.3:
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # character cells are taller than wide, so compensate the aspect ratio
    aspect_correction = CHAR_H / CHAR_W * 0.55
    grid_h = max(1, int(GRID_W * (h / w) * aspect_correction))
    small = img.resize((GRID_W, grid_h), Image.LANCZOS)
    return small


def pixel_to_char(value: int) -> str:
    # value: 0 (black) .. 255 (white). Map white -> ramp[0] (space)
    idx = int((255 - value) / 255 * (len(RAMP) - 1))
    return RAMP[idx]


def build_rows(img: Image.Image):
    w, h = img.size
    px = img.load()
    rows = []
    for y in range(h):
        chars = []
        for x in range(w):
            chars.append(pixel_to_char(px[x, y]))
        rows.append("".join(chars).rstrip())
    return rows


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_svg(rows):
    width = int(GRID_W * CHAR_W) + 20
    height = int(len(rows) * CHAR_H) + 20

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="SFMono-Regular, Consolas, Menlo, monospace">'
    )
    parts.append(f'<rect x="0" y="0" width="{width}" height="{height}" fill="none"/>')

    for i, row in enumerate(rows):
        if not row:
            continue
        row_width = len(row) * CHAR_W
        y = 15 + i * CHAR_H
        begin = i * ROW_STAGGER

        # Clip path that wipes left->right via SMIL <animate> on width
        clip_id = f"clip{i}"
        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(f'  <rect x="0" y="{y - CHAR_H}" height="{CHAR_H}" width="0">')
        parts.append(
            f'    <animate attributeName="width" from="0" to="{row_width:.1f}" '
            f'begin="{begin:.3f}s" dur="{ROW_DURATION}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.25 0.1 0.25 1" keyTimes="0;1"/>'
        )
        parts.append("  </rect>")
        parts.append("</clipPath>")

        parts.append(f'<g clip-path="url(#{clip_id})">')
        parts.append(
            f'<text x="10" y="{y}" font-size="{FONT_SIZE}" fill="{COLOR}" xml:space="preserve">{esc(row)}</text>'
        )
        parts.append("</g>")

        # small "cursor" block riding the wipe edge, then it fades out
        cursor_id = f"cursor{i}"
        parts.append(
            f'<rect x="0" y="{y - CHAR_H + 2}" width="2.4" height="{CHAR_H - 2}" fill="{COLOR}" opacity="0">'
        )
        parts.append(
            f'  <animate attributeName="x" from="10" to="{10 + row_width:.1f}" '
            f'begin="{begin:.3f}s" dur="{ROW_DURATION}s" fill="freeze" calcMode="spline" '
            f'keySplines="0.25 0.1 0.25 1" keyTimes="0;1"/>'
        )
        parts.append(
            f'  <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1" '
            f'begin="{begin:.3f}s" dur="{ROW_DURATION}s" fill="freeze"/>'
        )
        parts.append("</rect>")

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/make_ascii_svg.py <prepped-image> [out.svg]")
        sys.exit(1)

    src = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(__file__), "..", "avi-ascii.svg"
    )

    img = load_and_downsample(src)
    rows = build_rows(img)
    svg = render_svg(rows)

    with open(out_path, "w") as f:
        f.write(svg)
    print(f"Wrote {out_path} ({len(rows)} rows x {GRID_W} cols)")


if __name__ == "__main__":
    main()
