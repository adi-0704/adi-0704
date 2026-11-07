"""assets/hero.svg — typed greeting, rising-mask name, cycling roles, portrait."""

from lib import (C, WIDTH, accent_rule, background, document, dot_texture,
                 panel, text, _n)
import portrait

NS = "ah"
H = 330
PAD = 44

MONO_CH = 0.6  # JetBrains Mono advance width in em


def chip(x, y, label, *, accent=None, delay=0.0, h=28, size=11):
    w = len(label) * size * MONO_CH + 30
    g = [
        '<g class="%s-up" style="animation-delay:%ss">' % (NS, _n(delay)),
        '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
        'stroke="%s"/>' % (_n(x), _n(y), _n(w), _n(h), _n(h / 2), C["panel2"],
                           C["line"]),
    ]
    tx = x + 15
    if accent:
        g.append('<circle cx="%s" cy="%s" r="3.2" fill="%s"/>'
                 % (_n(x + 15), _n(y + h / 2), accent))
        tx = x + 27
        w += 12
    g.append(text(tx, y + h / 2 + size * 0.36, label, size=size, fill=C["dim"]))
    g.append("</g>")
    return "".join(g), w


def build(P):
    name_a, name_b = P["name"].split(" ", 1)
    name_b += "."
    roles = P["roles"]
    greet = "$ " + P["greeting"]

    b = [dot_texture(NS), background(NS, WIDTH, H)]

    # ---- eyebrow row
    b.append(accent_rule(NS, PAD, 46, 54))
    b.append(text(PAD + 68, 54, P["github"].upper(), size=11, fill=C["dim"],
                  spacing=2.4, cls=NS + "-up"))
    b.append(text(WIDTH - PAD, 54, "01 / INTRO", size=11, fill=C["dimmer"],
                  spacing=2.4, anchor="end", cls=NS + "-up"))

    # ---- typed greeting, clipped by a widening rect (full width is the
    #      static fallback, so the text reads even if SMIL is ignored)
    gw = len(greet) * 13 * MONO_CH + 4
    b.append(
        '<defs><clipPath id="%s-type">'
        '<rect x="%s" y="68" width="%s" height="24">'
        '<animate attributeName="width" values="0;0;%s" keyTimes="0;0.06;0.62" '
        'dur="2.6s" calcMode="discrete" repeatCount="1" fill="freeze"/>'
        "</rect></clipPath></defs>"
        % (NS, _n(PAD), _n(gw), _n(gw))
    )
    b.append('<g clip-path="url(#%s-type)">%s</g>'
             % (NS, text(PAD, 85, greet, size=13, fill=C["blue_soft"])))
    b.append(
        '<rect x="%s" y="73" width="7" height="15" fill="%s" class="%s-caret"/>'
        % (_n(PAD + gw + 3), C["crimson"], NS)
    )

    # ---- name, revealed by a rising mask
    for i, (line, fill, by) in enumerate(
        [(name_a, C["text"], 144), (name_b, C["blue"], 196)]
    ):
        b.append(
            '<defs><clipPath id="%s-m%d">'
            '<rect x="%s" y="%s" width="520" height="54"/>'
            "</clipPath></defs>" % (NS, i, _n(PAD - 6), _n(by - 44))
        )
        b.append(
            '<g clip-path="url(#%s-m%d)"><g class="%s-rise" '
            'style="animation-delay:%ss">%s</g></g>'
            % (NS, i, NS, _n(0.45 + i * 0.14),
               text(PAD, by, line, font="display", size=50, fill=fill,
                    spacing=-0.6))
        )

    # ---- cycling roles
    cyc = len(roles) * 3.0
    b.append('<g>')
    for i, r in enumerate(roles):
        b.append(
            '<g class="%s-role" style="animation-delay:%ss;animation-duration:%ss">%s</g>'
            % (NS, _n(i * 3.0), _n(cyc),
               text(PAD + 14, 234, r, size=15, fill=C["blue_soft"], weight=700))
        )
    b.append('<rect x="%s" y="221" width="3" height="17" rx="1.5" fill="%s"/>'
             % (_n(PAD), C["crimson"]))
    b.append("</g>")

    # ---- pitch
    b.append(text(PAD, 262, P["pitch"], size=12.5, fill=C["dim"],
                  cls=NS + "-up", extra='style="animation-delay:1.05s"'))

    # ---- chips
    x = PAD
    for i, (label, accent) in enumerate(
        [(P["location"], C["blue"]), (P["role_primary"], C["crimson"])]
    ):
        g, w = chip(x, 282, label, accent=accent, delay=1.2 + i * 0.12)
        b.append(g)
        x += w + 10

    # ---- portrait
    b.append('<g class="%s-pop">' % NS)
    b.append(portrait.circular(NS, 724, 158, 92))
    b.append("</g>")
    b.append(
        '<g class="%s-up" style="animation-delay:1.0s">'
        '<rect x="632" y="236" width="168" height="28" rx="6" fill="%s"/>%s</g>'
        % (NS, C["crimson"],
           text(648, 255, "YOUR IDENTITY", size=11, fill=C["white"],
                weight=700, spacing=1.8))
    )

    css = (
        "@keyframes {ns}-rule-kf{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
        ".{ns}-rule{{transform-origin:left center;animation:{ns}-rule-kf .7s "
        "cubic-bezier(.2,.8,.2,1) both}}"

        "@keyframes {ns}-rise-kf{{from{{transform:translateY(54px)}}"
        "to{{transform:translateY(0)}}}}"
        ".{ns}-rise{{animation:{ns}-rise-kf .9s cubic-bezier(.16,1,.3,1) both}}"

        "@keyframes {ns}-up-kf{{from{{opacity:0;transform:translateY(10px)}}"
        "to{{opacity:1;transform:translateY(0)}}}}"
        ".{ns}-up{{animation:{ns}-up-kf .7s cubic-bezier(.2,.8,.2,1) both}}"

        "@keyframes {ns}-pop-kf{{from{{opacity:0;transform:scale(.9)}}"
        "to{{opacity:1;transform:scale(1)}}}}"
        ".{ns}-pop{{transform-origin:724px 158px;"
        "animation:{ns}-pop-kf .9s cubic-bezier(.16,1,.3,1) both}}"

        "@keyframes {ns}-caret-kf{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}"
        ".{ns}-caret{{animation:{ns}-caret-kf 1.05s steps(1) infinite}}"

        "@keyframes {ns}-role-kf{{"
        "0%{{opacity:0;transform:translateY(9px)}}"
        "3%{{opacity:1;transform:translateY(0)}}"
        "22%{{opacity:1;transform:translateY(0)}}"
        "25%{{opacity:0;transform:translateY(-9px)}}"
        "100%{{opacity:0;transform:translateY(-9px)}}}}"
        ".{ns}-role{{opacity:0;animation-name:{ns}-role-kf;"
        "animation-timing-function:cubic-bezier(.2,.8,.2,1);"
        "animation-iteration-count:infinite;animation-fill-mode:both}}"
        ".{ns}-role:first-of-type{{opacity:1}}"
    ).format(ns=NS) + portrait.SPIN_CSS.format(ns=NS)

    disp = name_a + name_b
    mono = "".join([greet, P["github"].upper(), "01 / INTRO", P["pitch"],
                    P["location"], P["role_primary"], "YOUR IDENTITY",
                    "PORTRAIT", "AT"] + roles)

    return document(
        NS, WIDTH, H, "".join(b), css, disp, mono,
        "%s — %s" % (P["name_display"], P["role_primary"]),
        "%s. %s Based %s." % (P["name_display"], P["pitch"], P["location"]),
    )
