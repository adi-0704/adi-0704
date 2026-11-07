"""Shared design tokens, font embedding and SVG helpers.

Every generated SVG is fully self-contained: inline base64 fonts and images,
namespaced ids, CSS + SMIL only, zero network requests when rendered.
"""
import base64
import io
import os
import re
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
VENDOR = os.path.join(HERE, "vendor")
FONT_DIR = os.path.join(VENDOR, "fonts")
ICON_DIR = os.path.join(VENDOR, "icons")

# ---------------------------------------------------------------- design tokens

C = {
    "bg":        "#070b16",
    "panel":     "#0c1324",
    "panel2":    "#0f172c",
    "line":      "#1b2740",
    "line_soft": "#152037",
    "text":      "#e8ecf4",
    "dim":       "#8ea0c0",
    "dimmer":    "#5d6f90",
    "blue":      "#247bff",
    "blue_soft": "#5b9cff",
    "crimson":   "#ff354f",
    "white":     "#ffffff",
}

WIDTH = 880  # GitHub renders README images up to ~886px wide on desktop

DISPLAY = "AdiDisplay"
MONO = "AdiMono"

FONT_FILES = {
    "display":   ("archivo-black.ttf", DISPLAY, 400),
    "mono":      ("jbmono-400.ttf", MONO, 400),
    "mono_bold": ("jbmono-700.ttf", MONO, 700),
}


# ---------------------------------------------------------------- font embedding

def _subset_woff2(ttf_path, text):
    """Subset a TTF down to the characters actually used, return woff2 bytes."""
    from fontTools import subset

    chars = set(text) | set(" ")
    unicodes = {ord(c) for c in chars if ord(c) >= 0x20}
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.desubroutinize = True
    opts.notdef_outline = False
    opts.recalc_bounds = True
    font = subset.load_font(ttf_path, opts)
    subsetter = subset.Subsetter(options=opts)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, opts)
    font.close()
    return buf.getvalue()


def font_face_css(text_display, text_mono):
    """@font-face rules with base64 woff2 payloads, subset to the glyphs used."""
    rules = []
    jobs = [
        ("archivo-black.ttf", DISPLAY, 400, text_display),
        ("jbmono-400.ttf", MONO, 400, text_mono),
        ("jbmono-700.ttf", MONO, 700, text_mono),
    ]
    for fname, family, weight, text in jobs:
        if not text.strip():
            continue
        data = _subset_woff2(os.path.join(FONT_DIR, fname), text)
        b64 = base64.b64encode(data).decode("ascii")
        rules.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%d;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}" % (family, weight, b64)
        )
    return "".join(rules)


# ---------------------------------------------------------------- icons

_ICON_CACHE = {}


def icon_paths(slug):
    """Return the `d` attribute(s) of a Simple Icons glyph (24x24 viewBox)."""
    if slug in _ICON_CACHE:
        return _ICON_CACHE[slug]
    path = os.path.join(ICON_DIR, slug + ".svg")
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    ds = re.findall(r'<path[^>]*\bd="([^"]+)"', raw)
    if not ds:
        raise ValueError("no path data in %s" % path)
    _ICON_CACHE[slug] = ds
    return ds


def icon(slug, x, y, size, fill, opacity=1.0, extra=""):
    """Place a 24x24 brand glyph with its centre at (x, y)."""
    s = size / 24.0
    body = "".join('<path d="%s"/>' % d for d in icon_paths(slug))
    return (
        '<g transform="translate(%.2f %.2f) scale(%.4f)" fill="%s" '
        'fill-opacity="%.3f" %s>%s</g>'
        % (x - size / 2.0, y - size / 2.0, s, fill, opacity, extra, body)
    )


# ---------------------------------------------------------------- escaping

def esc(s):
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def b64_png(path):
    with open(path, "rb") as fh:
        return base64.b64encode(fh.read()).decode("ascii")


PNG_COLORS = 255  # palette size for inlined portraits; see _encode()


def _encode(im):
    """Palette-quantise and encode. Illustrated art survives 255 colours with
    no visible loss, at roughly a fifth of the bytes of full RGBA -- which
    matters a lot when every image is inlined into the README."""
    from PIL import Image

    q = im.quantize(colors=PNG_COLORS, method=Image.FASTOCTREE)
    buf = io.BytesIO()
    q.save(buf, "PNG", optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


_FIT_CACHE = {}


def b64_png_fit(path, max_w, max_h):
    """Base64 PNG downscaled to fit (max_w, max_h).

    Portraits arrive far larger than they are ever drawn. Every asset is
    inlined, so shipping the full-resolution file would bloat the README for
    no visible gain; this renders at 2x the drawn size and no more.
    """
    key = (path, int(max_w), int(max_h), os.path.getmtime(path))
    if key in _FIT_CACHE:
        return _FIT_CACHE[key]

    from PIL import Image

    im = Image.open(path).convert("RGBA")
    scale = min(max_w / im.width, max_h / im.height, 1.0)
    if scale < 1.0:
        im = im.resize((max(1, round(im.width * scale)),
                        max(1, round(im.height * scale))), Image.LANCZOS)
    out = _encode(im)
    _FIT_CACHE[key] = out
    return out


def b64_png_square(path, size):
    """Head-and-shoulders square crop, for drawing inside a circle.

    The source is already cropped tight to the subject, so a square taken
    from the top edge and centred on the subject horizontally frames the
    head with the shoulders running off the bottom of the circle.
    """
    key = ("sq", path, int(size), os.path.getmtime(path))
    if key in _FIT_CACHE:
        return _FIT_CACHE[key]

    from PIL import Image

    im = Image.open(path).convert("RGBA")
    side = min(im.width, im.height)
    left = max(0, (im.width - side) // 2)
    im = im.crop((left, 0, left + side, side))
    if side > size:
        im = im.resize((int(size), int(size)), Image.LANCZOS)
    out = _encode(im)
    _FIT_CACHE[key] = out
    return out


# ---------------------------------------------------------------- text helpers

def text(x, y, s, *, font="mono", size=13, fill=None, weight=400, anchor="start",
         cls="", opacity=None, spacing=None, extra=""):
    fam = DISPLAY if font == "display" else MONO
    fill = fill or C["text"]
    bits = [
        'x="%s"' % _n(x),
        'y="%s"' % _n(y),
        'font-family="%s"' % fam,
        'font-size="%s"' % _n(size),
        'fill="%s"' % fill,
    ]
    if weight != 400:
        bits.append('font-weight="%d"' % weight)
    if anchor != "start":
        bits.append('text-anchor="%s"' % anchor)
    if cls:
        bits.append('class="%s"' % cls)
    if opacity is not None:
        bits.append('opacity="%s"' % _n(opacity))
    if spacing is not None:
        bits.append('letter-spacing="%s"' % _n(spacing))
    if extra:
        bits.append(extra)
    return "<text %s>%s</text>" % (" ".join(bits), esc(s))


def _n(v):
    if isinstance(v, float):
        return ("%.2f" % v).rstrip("0").rstrip(".")
    return str(v)


def wrap(s, width):
    """Greedy word wrap to `width` characters."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- document shell

REDUCED_MOTION = (
    "@media (prefers-reduced-motion: reduce){"
    "*{animation:none!important;transition:none!important;}"
    "}"
)


def document(ns, width, height, body, css, all_text_display, all_text_mono,
             title, desc):
    """Wrap a body in a complete, self-contained SVG document.

    `ns` namespaces every id so several of these can coexist on one page.
    """
    faces = font_face_css(all_text_display, all_text_mono)
    style = "<style>%s%s%s</style>" % (faces, css, REDUCED_MOTION)
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'xmlns:xlink="http://www.w3.org/1999/xlink" '
        'viewBox="0 0 %d %d" width="%d" height="%d" '
        'role="img" aria-labelledby="%s-t %s-d" preserveAspectRatio="xMidYMid meet">'
        '<title id="%s-t">%s</title><desc id="%s-d">%s</desc>'
        "%s%s</svg>"
    ) % (width, height, width, height, ns, ns, ns, esc(title), ns, esc(desc),
         style, body)


# ---------------------------------------------------------------- shared chrome

def dot_texture(ns, opacity=0.5):
    return (
        '<pattern id="%s-dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        '<circle cx="1.5" cy="1.5" r="1.1" fill="%s" fill-opacity="%.2f"/>'
        "</pattern>" % (ns, C["blue"], 0.1 * opacity)
    )


def accent_rule(ns, x, y, w, h=3, delay=0.0):
    """The blue-to-crimson hairline that tops each panel."""
    return (
        '<defs><linearGradient id="%s-rule" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="%s"/>'
        '<stop offset="0.58" stop-color="%s"/>'
        '<stop offset="0.58" stop-color="%s"/>'
        '<stop offset="1" stop-color="%s"/>'
        "</linearGradient></defs>"
        '<rect x="%s" y="%s" width="%s" height="%s" fill="url(#%s-rule)" '
        'class="%s-rule" style="animation-delay:%ss"/>'
        % (ns, C["blue"], C["blue"], C["crimson"], C["crimson"],
           _n(x), _n(y), _n(w), _n(h), ns, ns, _n(delay))
    )


def panel(x, y, w, h, *, r=14, fill=None, stroke=None, cls="", style=""):
    return (
        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
        'stroke="%s" stroke-width="1" class="%s" style="%s"/>'
        % (_n(x), _n(y), _n(w), _n(h), _n(r), fill or C["panel"],
           stroke or C["line"], cls, style)
    )


def background(ns, width, height):
    return (
        '<rect width="%d" height="%d" rx="18" fill="%s"/>'
        '<rect width="%d" height="%d" rx="18" fill="url(#%s-dots)"/>'
        '<rect x="0.5" y="0.5" width="%s" height="%s" rx="17.5" fill="none" '
        'stroke="%s"/>' % (width, height, C["bg"], width, height, ns,
                           _n(width - 1), _n(height - 1), C["line"])
    )
