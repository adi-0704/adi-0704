"""assets/connect.svg — pointing character nudging toward the social cards.

Links inside an SVG are not clickable on GitHub, so this image is the visual
and the real anchors live in README.md directly beneath it.
"""

from lib import (C, WIDTH, accent_rule, background, document, dot_texture,
                 b64_png_fit, icon, panel, text, wrap, _n)
import portrait
from profile import ICON_LABELS

NS = "ac"
H = 380
PAD = 44

FIG_X, FIG_Y, FIG_W, FIG_H = 40, 104, 272, 258
GRID_X, GRID_Y = 348, 150
CARD_W, CARD_H, GAP = 240, 64, 14


def figure(ns):
    """right_pointing.png if present, otherwise a labelled placeholder.

    With a real alpha channel the character stands free on the page; only the
    placeholder needs a panel to sit in.
    """
    out = []

    if portrait.have(portrait.POINT_PNG):
        # soft pool of light so the cut-out does not float on flat navy
        out.append(
            '<defs><radialGradient id="%s-glow" cx="0.5" cy="0.62" r="0.5">'
            '<stop offset="0" stop-color="%s" stop-opacity="0.18"/>'
            '<stop offset="0.6" stop-color="%s" stop-opacity="0.05"/>'
            '<stop offset="1" stop-color="%s" stop-opacity="0"/>'
            "</radialGradient></defs>"
            % (ns, C["blue"], C["blue"], C["blue"])
        )
        out.append('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" '
                   'fill="url(#%s-glow)"/>'
                   % (_n(FIG_X + FIG_W / 2), _n(FIG_Y + FIG_H * 0.62),
                      _n(FIG_W * 0.72), _n(FIG_H * 0.6), ns))
        out.append(
            '<image href="data:image/png;base64,%s" x="%s" y="%s" width="%s" '
            'height="%s" preserveAspectRatio="xMidYMax meet"/>'
            % (b64_png_fit(portrait.POINT_PNG, FIG_W * 2, FIG_H * 2),
               _n(FIG_X), _n(FIG_Y), _n(FIG_W), _n(FIG_H))
        )
        return "".join(out)

    out.append(
        '<defs><linearGradient id="%s-figbg" x1="0" y1="0" x2="0.7" y2="1">'
        '<stop offset="0" stop-color="#101a30"/>'
        '<stop offset="1" stop-color="#090f1d"/></linearGradient></defs>' % ns
    )
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="16" '
               'fill="url(#%s-figbg)" stroke="%s"/>'
               % (_n(FIG_X), _n(FIG_Y), _n(FIG_W), _n(FIG_H), ns, C["line"]))
    cx, cy = FIG_X + FIG_W / 2, FIG_Y + FIG_H / 2
    out.append(text(cx, cy - 6, "AT", font="display", size=68,
                    fill=C["line"], anchor="middle"))
    out.append(text(cx, cy + 26, "RIGHT-POINTING", size=10,
                    fill=C["dimmer"], anchor="middle", spacing=2.2))
    out.append(text(cx, cy + 42, "CHARACTER", size=10, fill=C["dimmer"],
                    anchor="middle", spacing=2.2))
    return "".join(out)


def build(P):
    socials = P["socials"]
    b = [dot_texture(NS), background(NS, WIDTH, H)]

    b.append(accent_rule(NS, PAD, 48, 54))
    b.append(text(PAD + 68, 56, "FIND ME HERE", size=11, fill=C["dim"],
                  spacing=2.4, cls=NS + "-up"))
    b.append(text(WIDTH - PAD, 56, "05 / CONNECT", size=11, fill=C["dimmer"],
                  spacing=2.4, anchor="end", cls=NS + "-up"))
    b.append(text(GRID_X, 104, "LET'S BUILD SOMETHING", font="display",
                  size=27, fill=C["text"], spacing=-0.3, cls=NS + "-up",
                  extra='style="animation-delay:.1s"'))
    b.append(text(GRID_X, 128, "Open to freelance automation work and "
                  "full-time AI engineering roles.", size=10.5,
                  fill=C["dimmer"], cls=NS + "-up",
                  extra='style="animation-delay:.18s"'))

    b.append('<g class="%s-up">%s</g>' % (NS, figure(NS)))

    # nudging chevrons between the figure and the cards
    for i in range(3):
        x = FIG_X + FIG_W + 14 + i * 13
        y = FIG_Y + FIG_H / 2
        b.append(
            '<path d="M%s %s l7 8 l-7 8" fill="none" stroke="%s" '
            'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" '
            'class="%s-nudge" style="animation-delay:%ss"/>'
            % (_n(x), _n(y - 8), C["crimson"] if i == 2 else C["blue"], NS,
               _n(i * 0.16))
        )

    # ---- social cards
    for i, s in enumerate(socials):
        col, row = i % 2, i // 2
        x = GRID_X + col * (CARD_W + GAP)
        y = GRID_Y + row * (CARD_H + GAP)
        b.append('<g class="%s-up" style="animation-delay:%ss">'
                 % (NS, _n(0.34 + i * 0.1)))
        b.append(panel(x, y, CARD_W, CARD_H, r=13, fill=C["panel2"]))
        b.append('<rect x="%s" y="%s" width="40" height="40" rx="11" fill="%s"/>'
                 % (_n(x + 12), _n(y + 12), C["panel"]))
        b.append(icon(s["platform"], x + 32, y + 32, 19, C["text"], 0.95))
        b.append(text(x + 64, y + 28, s["label"], size=12, fill=C["text"],
                      weight=700))
        b.append(text(x + 64, y + 45, s["handle"], size=10, fill=C["dim"]))
        b.append('<path d="M%s %s l5 6 l-5 6" fill="none" stroke="%s" '
                 'stroke-width="1.8" stroke-linecap="round" '
                 'stroke-linejoin="round"/>'
                 % (_n(x + CARD_W - 24), _n(y + 26), C["dimmer"]))
        b.append("</g>")

    rows = (len(socials) + 1) // 2
    fy = GRID_Y + rows * (CARD_H + GAP) + 10
    b.append('<g class="%s-up" style="animation-delay:.8s">' % NS)
    b.append('<rect x="%s" y="%s" width="%s" height="1" fill="%s"/>'
             % (_n(GRID_X), _n(fy), _n(CARD_W * 2 + GAP), C["line"]))
    b.append(text(GRID_X, fy + 22, "The links below this image are the "
                  "clickable ones.", size=10, fill=C["dimmer"]))
    b.append("</g>")

    css = (
        "@keyframes {ns}-rule-kf{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
        ".{ns}-rule{{transform-origin:left center;animation:{ns}-rule-kf .7s "
        "cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-up-kf{{from{{opacity:0;transform:translateY(12px)}}"
        "to{{opacity:1;transform:translateY(0)}}}}"
        ".{ns}-up{{animation:{ns}-up-kf .7s cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-nudge-kf{{"
        "0%,100%{{opacity:.25;transform:translateX(0)}}"
        "45%{{opacity:1;transform:translateX(5px)}}}}"
        ".{ns}-nudge{{animation:{ns}-nudge-kf 1.9s ease-in-out infinite both}}"
    ).format(ns=NS)

    disp = "LET'S BUILD SOMETHINGAT"
    mono = "".join(
        ["FIND ME HERE", "05 / CONNECT", "RIGHT-POINTING", "CHARACTER",
         "Open to freelance automation work and full-time AI engineering roles.",
         "The links below this image are the clickable ones."]
        + [s["label"] + s["handle"] for s in socials]
    )

    return document(
        NS, WIDTH, H, "".join(b), css, disp, mono,
        "Connect with %s" % P["name_display"],
        "Find %s on %s." % (P["name_display"],
                            ", ".join(s["label"] for s in socials)),
    )
