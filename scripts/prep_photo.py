#!/usr/bin/env python3
"""
prep_photo.py
A flatly-lit face converts to a dark, unreadable ASCII blob. Three steps
fix that:
  1. Remove the background with rembg, so the subject is isolated.
  2. Boost local contrast with OpenCV's CLAHE (contrast-limited adaptive
     histogram equalization) — gives a flat face real highlights/shadows.
  3. Composite onto pure white, so the background maps to the blank end
     of the ASCII ramp (white -> spaces).

Usage:
    python scripts/prep_photo.py source-photo.jpg
Output:
    source-prepped.png  (grayscale, subject on white)
"""
import sys
import os

import cv2
import numpy as np
from PIL import Image


def remove_background(input_path: str) -> Image.Image:
    from rembg import remove  # imported lazily: heavy dep, portrait-only
    with open(input_path, "rb") as f:
        input_bytes = f.read()
    output_bytes = remove(input_bytes)
    from io import BytesIO
    return Image.open(BytesIO(output_bytes)).convert("RGBA")


def clahe_boost(rgba: Image.Image) -> Image.Image:
    arr = np.array(rgba)
    rgb = arr[:, :, :3]
    alpha = arr[:, :, 3]

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    boosted = clahe.apply(gray)

    out = np.dstack([boosted, boosted, boosted, alpha])
    return Image.fromarray(out, mode="RGBA")


def composite_on_white(rgba: Image.Image) -> Image.Image:
    white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, rgba)
    return composited.convert("L")  # grayscale


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py <source-photo>")
        sys.exit(1)

    src = sys.argv[1]
    base, _ = os.path.splitext(src)
    out_path = f"{base}-prepped.png"

    print("Removing background...")
    rgba = remove_background(src)

    print("Boosting local contrast (CLAHE)...")
    boosted = clahe_boost(rgba)

    print("Compositing on white...")
    gray = composite_on_white(boosted)

    gray.save(out_path)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
