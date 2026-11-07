"""Portrait slot: inlines id.png when present, otherwise a designed placeholder.

The slot geometry never changes, so dropping the real PNG in and re-running
build.py swaps the artwork without touching any layout.
"""
import os

from lib import C, b64_png_fit, b64_png_square, text, _n

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "source-images")

ID_PNG = os.path.join(SRC, "id.png")
POINT_PNG = os.path.join(SRC, "right_pointing.png")


def have(path):
    return os.path.isfile(path) and os.path.getsize(path) > 1024


def circular(ns, cx, cy, r, *, monogram="AT", png=ID_PNG, cls="", ring=True):
    """A circular portrait with rim light. Real PNG if available, else monogram."""
    uid = "%s-por" % ns
    out = [
        '<defs>'
        '<clipPath id="%s-clip"><circle cx="%s" cy="%s" r="%s"/></clipPath>'
        '<radialGradient id="%s-fill" cx="0.5" cy="0.38" r="0.75">'
        '<stop offset="0" stop-color="#16203a"/>'
        '<stop offset="1" stop-color="#0a1020"/>'
        "</radialGradient>"
        '<linearGradient id="%s-rim" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="%s"/>'
        '<stop offset="0.5" stop-color="%s" stop-opacity="0.25"/>'
        '<stop offset="1" stop-color="%s"/>'
        "</linearGradient>"
        "</defs>"
        % (uid, _n(cx), _n(cy), _n(r), uid, uid, C["blue"], C["blue"], C["crimson"])
    ]

    out.append(
        '<circle cx="%s" cy="%s" r="%s" fill="url(#%s-fill)"/>'
        % (_n(cx), _n(cy), _n(r), uid)
    )

    if have(png):
        out.append(
            '<image href="data:image/png;base64,%s" x="%s" y="%s" width="%s" '
            'height="%s" clip-path="url(#%s-clip)" '
            'preserveAspectRatio="xMidYMid slice"/>'
            % (b64_png_square(png, r * 4), _n(cx - r), _n(cy - r),
               _n(r * 2), _n(r * 2), uid)
        )
    else:
        # Designed placeholder: monogram over the same disc, plus a marker so
        # it is obvious at a glance that artwork is still pending.
        out.append(
            text(cx, cy + r * 0.26, monogram, font="display",
                 size=r * 0.86, fill=C["line"], anchor="middle")
        )
        out.append(
            text(cx, cy + r * 0.62, "PORTRAIT", font="mono", size=r * 0.12,
                 fill=C["dimmer"], anchor="middle", spacing=r * 0.035)
        )

    if ring:
        out.append(
            '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="url(#%s-rim)" '
            'stroke-width="2.5"/>' % (_n(cx), _n(cy), _n(r), uid)
        )
        out.append(
            '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" '
            'stroke-opacity="0.55" stroke-width="1.2" stroke-dasharray="3 9" '
            'stroke-linecap="round" class="%s-spin" '
            'style="transform-origin:%spx %spx"/>'
            % (_n(cx), _n(cy), _n(r + 11), C["blue"], ns, _n(cx), _n(cy))
        )
    return "".join(out)


SPIN_CSS = (
    "@keyframes {ns}-spin-kf{{from{{transform:rotate(0deg)}}"
    "to{{transform:rotate(360deg)}}}}"
    ".{ns}-spin{{animation:{ns}-spin-kf 34s linear infinite}}"
)
