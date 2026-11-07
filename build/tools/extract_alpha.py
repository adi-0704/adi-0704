"""Recover a real alpha channel from an image with a checkerboard baked in.

The image tool that produced the portraits drew its transparency checkerboard
into the pixels instead of exporting alpha. The grid is two exactly-neutral
greys, so it can be keyed out reliably:

  1. mark pixels that are neutral (R==G==B within tolerance) and close to
     either checker grey;
  2. keep only the marked region connected to the image border, so neutral
     greys inside the subject survive;
  3. fill small holes, which removes the generator's corner watermark;
  4. erode one pixel and feather, so no grey fringe is left on a dark page;
  5. decontaminate the remaining edge pixels by unpremultiplying the grey.

Usage:
    python build/tools/extract_alpha.py IN.webp OUT.png
"""
import sys

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

CHECKER_GREYS = (71, 100)
GREY_TOL = 10        # how far a pixel may sit from a checker grey
NEUTRAL_TOL = 10     # max channel spread for "this pixel has no hue"
HOLE_MAX = 20000     # px; fills the watermark, never the subject
SPECK_FRAC = 0.02    # keep foreground blobs >= this fraction of the largest


def extract(src, dst, verbose=True):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape

    spread = a.max(axis=2) - a.min(axis=2)
    lum = a.mean(axis=2)
    neutral = spread <= NEUTRAL_TOL
    near = np.zeros((h, w), bool)
    for g in CHECKER_GREYS:
        near |= np.abs(lum - g) <= GREY_TOL
    cand = neutral & near

    # keep only candidate regions that touch the border
    lab, n = ndimage.label(cand)
    border = set(lab[0, :]) | set(lab[-1, :]) | set(lab[:, 0]) | set(lab[:, -1])
    border.discard(0)
    bg = np.isin(lab, list(border))

    # fill small holes in the background (the generator's watermark)
    holes = ndimage.binary_fill_holes(bg) & ~bg
    hl, hn = ndimage.label(holes)
    if hn:
        sizes = ndimage.sum(holes, hl, range(1, hn + 1))
        small = {i + 1 for i, s in enumerate(sizes) if s <= HOLE_MAX}
        if small:
            bg |= np.isin(hl, list(small))

    fg = ~bg

    # drop isolated specks: the generator's corner watermark survives the
    # grey key because it is white, and it sits against the image edge so it
    # is not a hole. Anything far smaller than the subject is not the subject.
    fl, fn = ndimage.label(fg)
    if fn > 1:
        sizes = ndimage.sum(fg, fl, range(1, fn + 1))
        biggest = sizes.max()
        keep = {i + 1 for i, s in enumerate(sizes) if s >= biggest * SPECK_FRAC}
        fg = np.isin(fl, list(keep))
        if verbose and fn - len(keep) > 0:
            print("    dropped %d speck(s)" % (fn - len(keep)))

    alpha = fg.astype(np.uint8) * 255

    # pull the matte in by a pixel, then soften, to kill the grey fringe
    alpha = np.asarray(
        Image.fromarray(alpha).filter(ImageFilter.MinFilter(3))
    )
    alpha_img = Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.6))
    alpha = np.asarray(alpha_img).astype(np.float32) / 255.0

    # decontaminate: partly-transparent pixels still carry checker grey, so
    # unpremultiply it back out instead of leaving a halo
    rgb = a.astype(np.float32)
    grey = float(np.mean(CHECKER_GREYS))
    soft = (alpha > 0.02) & (alpha < 0.98)
    k = np.clip(alpha, 0.25, 1.0)[..., None]
    rgb[soft] = np.clip(
        (rgb[soft] - grey * (1.0 - k[soft])) / k[soft], 0, 255
    )

    out = np.dstack([rgb.astype(np.uint8),
                     (alpha * 255).astype(np.uint8)])
    img = Image.fromarray(out, "RGBA")

    # crop to the subject so the asset carries no dead space
    bbox = img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        img = img.crop(bbox)

    img.save(dst, "PNG", optimize=True)

    if verbose:
        cov = float((alpha > 0.5).mean()) * 100
        print("  %s -> %s  %dx%d  subject covers %.1f%%"
              % (src.split("/")[-1], dst.split("/")[-1],
                 img.width, img.height, cov))
    return img


if __name__ == "__main__":
    extract(sys.argv[1], sys.argv[2])
