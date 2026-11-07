"""assets/stack.svg — labelled tech icons on three tilted elliptical orbits."""

import math

from lib import (C, WIDTH, accent_rule, background, document, dot_texture,
                 icon, text, _n)
from profile import ICON_LABELS

NS = "as"
H = 540
PAD = 44

CX, CY = 440, 236

#               rx    ry   tilt   phase  icon size
# rx, ry and tilt are hand-set; the phases are solved numerically so that no
# icon or label box overlaps another (see tools/solve_orbits.py).
ORBITS = [
    (322.0, 92.0, -14.0, 12.0, 22.0),
    (240.0, 74.0, 24.0, 6.0, 20.0),
    (158.0, 56.0, -58.0, 78.0, 19.0),
]


def orbit_point(rx, ry, tilt, deg):
    t = math.radians(deg)
    x, y = rx * math.cos(t), ry * math.sin(t)
    a = math.radians(tilt)
    return (CX + x * math.cos(a) - y * math.sin(a),
            CY + x * math.sin(a) + y * math.cos(a))


def build(P):
    b = [dot_texture(NS), background(NS, WIDTH, H)]

    b.append(accent_rule(NS, PAD, 48, 54))
    b.append(text(PAD + 68, 56, "TOOLS I REACH FOR", size=11, fill=C["dim"],
                  spacing=2.4, cls=NS + "-up"))
    b.append(text(WIDTH - PAD, 56, "03 / STACK", size=11, fill=C["dimmer"],
                  spacing=2.4, anchor="end", cls=NS + "-up"))
    b.append(text(PAD, 104, "THE STACK", font="display", size=27,
                  fill=C["text"], spacing=-0.3, cls=NS + "-up",
                  extra='style="animation-delay:.1s"'))

    # ---- orbit rings, each with a light travelling around it
    for k, (rx, ry, tilt, phase, isz) in enumerate(ORBITS):
        per = 2 * math.pi
        circ = per * math.sqrt((rx * rx + ry * ry) / 2.0)  # good enough for dashes
        b.append(
            '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" '
            'stroke-opacity="0.75" stroke-width="1" '
            'transform="rotate(%s %s %s)" class="%s-ring" '
            'style="animation-delay:%ss"/>'
            % (_n(CX), _n(CY), _n(rx), _n(ry), C["line"], _n(tilt), _n(CX),
               _n(CY), NS, _n(0.2 + k * 0.1))
        )
        b.append(
            '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" '
            'stroke-width="1.6" stroke-linecap="round" '
            'stroke-dasharray="%s %s" transform="rotate(%s %s %s)" '
            'class="%s-trace%d"/>'
            % (_n(CX), _n(CY), _n(rx), _n(ry),
               C["blue"] if k != 1 else C["crimson"],
               _n(circ * 0.07), _n(circ), _n(tilt), _n(CX), _n(CY), NS, k)
        )

    # ---- core
    b.append('<g class="%s-pop">' % NS)
    b.append('<circle cx="%s" cy="%s" r="52" fill="%s" stroke="%s"/>'
             % (_n(CX), _n(CY), C["panel"], C["line"]))
    b.append('<circle cx="%s" cy="%s" r="52" fill="none" stroke="%s" '
             'stroke-opacity="0.6" stroke-width="1.5" class="%s-pulse" '
             'style="transform-origin:%spx %spx"/>'
             % (_n(CX), _n(CY), C["blue"], NS, _n(CX), _n(CY)))
    b.append(text(CX, CY - 2, "STACK", font="display", size=15, fill=C["text"],
                  anchor="middle", spacing=0.4))
    b.append(text(CX, CY + 16, "DAILY DRIVERS", size=8, fill=C["dimmer"],
                  anchor="middle", spacing=1.4))
    b.append("</g>")

    # ---- icons on the orbits
    idx = 0
    for k, (rx, ry, tilt, phase, isz) in enumerate(ORBITS):
        slugs = P["orbits"][k]
        for j, slug in enumerate(slugs):
            deg = phase + j * (360.0 / len(slugs))
            x, y = orbit_point(rx, ry, tilt, deg)
            label = ICON_LABELS.get(slug, slug)
            d = 0.5 + idx * 0.06
            b.append(
                '<g class="%s-node" style="animation-delay:%ss">' % (NS, _n(d))
            )
            b.append(
                '<g class="%s-float" style="animation-delay:%ss;'
                'animation-duration:%ss">' % (NS, _n(idx * 0.37), _n(5.2 + k * 0.9))
            )
            b.append('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s"/>'
                     % (_n(x), _n(y), _n(isz * 0.95), C["panel2"], C["line"]))
            b.append(icon(slug, x, y, isz * 0.92, C["text"], 0.92))
            b.append(text(x, y + isz * 1.6, label, size=8.5, fill=C["dim"],
                          anchor="middle", spacing=0.4))
            b.append("</g></g>")
            idx += 1

    # ---- grouped chips
    gy = 438
    col_w = (WIDTH - PAD * 2) / 3.0
    for gi, (gname, slugs) in enumerate(P["stack_groups"]):
        gx = PAD + gi * col_w
        b.append('<g class="%s-up" style="animation-delay:%ss">'
                 % (NS, _n(1.0 + gi * 0.1)))
        b.append('<rect x="%s" y="%s" width="20" height="2" fill="%s"/>'
                 % (_n(gx), _n(gy - 16), [C["blue"], C["crimson"], C["blue"]][gi]))
        b.append(text(gx + 28, gy - 12, gname, size=9.5, fill=C["dim"],
                      spacing=1.8))
        x, y = gx, gy + 8
        for slug in slugs:
            label = ICON_LABELS.get(slug, slug)
            w = 30 + len(label) * 6.3 + 14
            if x + w > gx + col_w - 14:
                x, y = gx, y + 32
            b.append('<rect x="%s" y="%s" width="%s" height="27" rx="13.5" '
                     'fill="%s" stroke="%s"/>'
                     % (_n(x), _n(y), _n(w), C["panel2"], C["line"]))
            b.append(icon(slug, x + 17, y + 13.5, 13, C["dim"], 0.9))
            b.append(text(x + 30, y + 17.5, label, size=10, fill=C["dim"]))
            x += w + 8
        b.append("</g>")

    css = (
        "@keyframes {ns}-rule-kf{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
        ".{ns}-rule{{transform-origin:left center;animation:{ns}-rule-kf .7s "
        "cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-up-kf{{from{{opacity:0;transform:translateY(12px)}}"
        "to{{opacity:1;transform:translateY(0)}}}}"
        ".{ns}-up{{animation:{ns}-up-kf .7s cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-ring-kf{{from{{opacity:0}}to{{opacity:1}}}}"
        ".{ns}-ring{{animation:{ns}-ring-kf .9s ease-out both}}"
        "@keyframes {ns}-pop-kf{{from{{opacity:0;transform:scale(.82)}}"
        "to{{opacity:1;transform:scale(1)}}}}"
        ".{ns}-pop{{transform-origin:{cx}px {cy}px;"
        "animation:{ns}-pop-kf .8s cubic-bezier(.16,1,.3,1) both}}"
        "@keyframes {ns}-node-kf{{from{{opacity:0;transform:scale(.7)}}"
        "to{{opacity:1;transform:scale(1)}}}}"
        ".{ns}-node{{transform-box:fill-box;transform-origin:center;"
        "animation:{ns}-node-kf .55s cubic-bezier(.16,1,.3,1) both}}"
        "@keyframes {ns}-float-kf{{0%,100%{{transform:translateY(-3px)}}"
        "50%{{transform:translateY(3px)}}}}"
        ".{ns}-float{{animation-name:{ns}-float-kf;"
        "animation-timing-function:ease-in-out;"
        "animation-iteration-count:infinite;animation-fill-mode:both}}"
        "@keyframes {ns}-pulse-kf{{0%{{transform:scale(1);opacity:.55}}"
        "70%{{transform:scale(1.5);opacity:0}}100%{{transform:scale(1.5);opacity:0}}}}"
        ".{ns}-pulse{{animation:{ns}-pulse-kf 3.6s ease-out infinite both}}"
    ).format(ns=NS, cx=_n(CX), cy=_n(CY))

    for k, (rx, ry, tilt, phase, isz) in enumerate(ORBITS):
        circ = 2 * math.pi * math.sqrt((rx * rx + ry * ry) / 2.0)
        dur = 11.0 + k * 3.5
        css += (
            "@keyframes %s-trace%d-kf{from{stroke-dashoffset:%s}"
            "to{stroke-dashoffset:%s}}"
            ".%s-trace%d{stroke-dashoffset:%s;"
            "animation:%s-trace%d-kf %ss linear infinite both}"
            % (NS, k, _n(circ), _n(-circ * 0.07), NS, k, _n(circ), NS, k, _n(dur))
        )

    labels = [ICON_LABELS.get(s, s)
              for o in P["orbits"] for s in o]
    labels += [ICON_LABELS.get(s, s) for _, g in P["stack_groups"] for s in g]
    labels += [g for g, _ in P["stack_groups"]]

    disp = "THE STACK"
    mono = "".join(labels) + "TOOLS I REACH FOR03 / STACKDAILY DRIVERS"

    return document(
        NS, WIDTH, H, "".join(b), css, disp, mono,
        "%s — technology stack" % P["name_display"],
        "Stack: " + ", ".join(dict.fromkeys(labels)) + ".",
    )
