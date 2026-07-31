#!/usr/bin/env python3
"""
Development-time asset generator for the teaching portfolio site.

Reads assets/img/canopy.png (the source watercolor) and produces every derived
image the site uses: the header plate (desktop + mobile), the trailing vine
cutout, and three small section-divider crops. Run this once (or again only if
canopy.png changes); nothing about the shipped static site depends on it.

Usage:
    pip3 install Pillow numpy
    python3 scripts/build_images.py
"""

import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = "assets/img/canopy.png"
OUT = "assets/img"

PAPER = (244, 243, 234)  # --paper, #F4F3EA

random.seed(11)


def load_source():
    return Image.open(SRC).convert("RGBA")


def paper_distance_alpha(rgba, low=16, high=58):
    """Soft alpha ramp from color-distance to --paper. Below `low` -> fully
    transparent (paper), above `high` -> fully opaque (specimen). Linear ramp
    between, which avoids the crunchy halo a hard threshold produces on
    watercolor edges."""
    arr = np.asarray(rgba.convert("RGB"), dtype=np.float32)
    paper = np.array(PAPER, dtype=np.float32)
    dist = np.sqrt(((arr - paper) ** 2).sum(axis=-1))
    alpha = np.clip((dist - low) / (high - low), 0.0, 1.0)
    alpha = (alpha * 255).astype(np.uint8)
    return Image.fromarray(alpha, mode="L")


def radial_vignette(size, inner=0.45, outer=0.98):
    """Elliptical fade to transparent, strongest in the corners. Used for the
    small divider crops so a leaf/frond reads as an isolated mark regardless
    of what's sitting in the corners of its bounding box (dark background
    foliage as well as paper)."""
    w, h = size
    cx, cy = w / 2, h / 2
    ys, xs = np.mgrid[0:h, 0:w]
    nx = (xs - cx) / (w / 2)
    ny = (ys - cy) / (h / 2)
    dist = np.sqrt(nx ** 2 + ny ** 2)
    alpha = np.clip(1 - (dist - inner) / (outer - inner), 0, 1)
    alpha = (alpha * 255).astype(np.uint8)
    return Image.fromarray(alpha, mode="L")


def edge_vignette(size, feather):
    """Grayscale mask, white in the interior, fading to black within
    `feather` px of every edge -- used to guarantee a crop blends into the
    page regardless of what's sitting at its literal boundary pixels."""
    w, h = size
    mask = Image.new("L", size, 255)
    draw = ImageDraw.Draw(mask)
    for i in range(feather):
        v = int(255 * (i / feather))
        draw.rectangle([i, i, w - 1 - i, h - 1 - i], outline=v)
    return mask.filter(ImageFilter.GaussianBlur(feather / 3))


def jagged_band_mask(size, band_height, jitter, at="bottom", blur=5, seed=0):
    """Grayscale mask for a synthetic deckled-paper edge: white (paper) below
    an irregular, noise-jittered boundary line, black (source) above it, with
    the boundary itself softened by a blur so it reads as a torn/painted edge
    rather than a ruled cut."""
    w, h = size
    rng = random.Random(seed)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)

    # coarse random offsets smoothed into a wavy boundary line
    step = 8
    n = w // step + 2
    raw = [rng.uniform(-jitter, jitter) for _ in range(n)]
    smooth = []
    for i in range(n):
        lo, hi = max(0, i - 2), min(n, i + 3)
        smooth.append(sum(raw[lo:hi]) / (hi - lo))

    base_y = h - band_height if at == "bottom" else band_height
    points = []
    for i, off in enumerate(smooth):
        x = i * step
        y = base_y + off if at == "bottom" else base_y + off
        points.append((x, y))

    if at == "bottom":
        poly = [(0, h)] + points + [(w, h)]
    else:
        poly = [(0, 0)] + points + [(w, 0)]
    draw.polygon(poly, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(blur))


def apply_deckle_edges(img, band=34, jitter=11, blur=5):
    """Composite a synthetic deckled paper edge onto the top and bottom of a
    crop so a cut mid-illustration reads as a mounted plate edge, matching
    the source image's own painted-margin style."""
    w, h = img.size
    paper_layer = Image.new("RGBA", (w, h), PAPER + (255,))
    out = img.convert("RGBA")

    top_mask = jagged_band_mask((w, h), band, jitter, at="top", blur=blur, seed=1)
    bottom_mask = jagged_band_mask((w, h), band, jitter, at="bottom", blur=blur, seed=2)
    combined = Image.fromarray(
        np.maximum(np.asarray(top_mask), np.asarray(bottom_mask))
    )
    out = Image.composite(paper_layer, out, combined)
    return out


def save_webp_png(img, name, quality=82, max_kb=None, lossless=False):
    webp_path = f"{OUT}/{name}.webp"
    png_path = f"{OUT}/{name}.png"
    if lossless:
        img.save(webp_path, "WEBP", lossless=True, method=6)
    else:
        img.save(webp_path, "WEBP", quality=quality, method=6)
    img.save(png_path, "PNG", optimize=True)
    import os
    wkb = os.path.getsize(webp_path) / 1024
    pkb = os.path.getsize(png_path) / 1024
    flag = ""
    if max_kb and wkb > max_kb:
        flag = f"  *** OVER BUDGET ({max_kb}KB) ***"
    print(f"  {name}: webp {wkb:.0f}KB, png {pkb:.0f}KB{flag}")


def build_header():
    src = load_source()
    w, h = src.size  # 1312x716

    # Desktop plate: ~3:1, top of image (real deckle already at y=0)
    crop_h = round(w / 3)  # 437
    desktop = src.crop((0, 0, w, crop_h))
    desktop = apply_deckle_edges(desktop, band=30, jitter=9)
    save_webp_png(desktop, "header-plate", quality=80, max_kb=250)

    # Mobile plate: taller aspect so foliage doesn't get squeezed to a sliver
    mobile_h = round(w / 2.2)
    mobile = src.crop((0, 0, w, mobile_h))
    mobile = apply_deckle_edges(mobile, band=30, jitter=9)
    save_webp_png(mobile, "header-plate-mobile", quality=80, max_kb=250)


def build_vine():
    src = load_source()
    box = (1060, 0, 1312, 716)
    crop = src.crop(box)
    w, h = crop.size

    alpha = paper_distance_alpha(crop, low=16, high=58)
    vignette = edge_vignette((w, h), feather=44)
    # only feather the left edge hard (where the cutout meets page content);
    # top/bottom/right are true image edges already keyed by the paper alpha
    left_fade = Image.new("L", (w, h), 255)
    draw = ImageDraw.Draw(left_fade)
    for x in range(70):
        v = int(255 * (x / 70))
        draw.line([(x, 0), (x, h)], fill=v)
    left_fade = left_fade.filter(ImageFilter.GaussianBlur(14))

    combined = Image.fromarray(
        np.minimum(
            np.asarray(alpha),
            np.minimum(np.asarray(vignette), np.asarray(left_fade)),
        )
    )
    out = crop.copy()
    out.putalpha(combined)
    save_webp_png(out, "vine-cutout", quality=95, max_kb=150)


DIVIDERS = {
    "divider-fern": (0, 540, 300, 716),
    "divider-palmetto": (0, 250, 320, 500),
    "divider-monstera": (395, 15, 585, 165),
}


def build_dividers():
    src = load_source()
    for name, box in DIVIDERS.items():
        crop = src.crop(box)
        w, h = crop.size
        alpha = paper_distance_alpha(crop, low=16, high=58)
        vignette = radial_vignette((w, h), inner=0.4, outer=0.98)
        combined = Image.fromarray(
            np.minimum(np.asarray(alpha), np.asarray(vignette))
        )
        out = crop.copy()
        out.putalpha(combined)
        # normalize to a consistent tall-thumbnail scale for crisp downscaling in CSS
        target_h = 160
        target_w = round(w * target_h / h)
        out = out.resize((target_w, target_h), Image.LANCZOS)
        save_webp_png(out, name, quality=95, max_kb=60)


if __name__ == "__main__":
    print("Building header plate...")
    build_header()
    print("Building vine cutout...")
    build_vine()
    print("Building section dividers...")
    build_dividers()
    print("Done.")
