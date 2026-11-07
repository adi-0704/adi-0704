"""assets/id-dashboard.svg — a lanyard ID card that drops in and settles,
beside verified, dated GitHub facts."""

import hashlib

from lib import (C, WIDTH, accent_rule, background, document, dot_texture,
                 icon, panel, text, _n)

NS = "ai"
H = 580
PAD = 44

PIVOT_X, PIVOT_Y = 250, 58          # where the lanyard hangs from
CARD_X, CARD_Y, CARD_W, CARD_H = 115, 206, 270, 346
CLASP_Y = 176

RX, RY, RW = 440, 150, 396          # right-hand facts column


def barcode(seed, x, y, w, h):
    """Deterministic barcode derived from the username."""
    digest = hashlib.sha256(seed.encode()).digest()
    out, cx, i = [], x, 0
    while cx < x + w - 1 and i < len(digest) * 4:
        bit = (digest[i % len(digest)] >> (i // len(digest) % 8)) & 1
        bw = 1.2 + ((digest[i % len(digest)] >> 3) & 3) * 0.8
        if bit:
            out.append('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>'
                       % (_n(cx), _n(y), _n(bw), _n(h), C["text"]))
        cx += bw + 1.1
        i += 1
    return "".join(out)


def _stat_tile(i, label, value, y):
    g = ['<g class="%s-up" style="animation-delay:%ss">' % (NS, _n(0.5 + i * 0.12))]
    g.append(panel(RX, y, RW, 66, r=12, fill=C["panel"]))
    g.append('<rect x="%s" y="%s" width="3" height="34" rx="1.5" fill="%s"/>'
             % (_n(RX + 18), _n(y + 16), C["blue"] if i != 1 else C["crimson"]))
    g.append(text(RX + 34, y + 28, label, size=9.5, fill=C["dimmer"], spacing=1.8))
    g.append(text(RX + 34, y + 52, value, font="display", size=20,
                  fill=C["text"], spacing=-0.2))
    g.append('<text x="%s" y="%s" font-family="AdiMono" font-size="9.5" '
             'fill="%s" text-anchor="end" letter-spacing="1.4">VERIFIED</text>'
             % (_n(RX + RW - 18), _n(y + 28), C["dimmer"]))
    g.append('<circle cx="%s" cy="%s" r="3" fill="%s"/>'
             % (_n(RX + RW - 18 - 62), _n(y + 24.6), C["blue"]))
    g.append("</g>")
    return "".join(g)


def build(P):
    b = [dot_texture(NS), background(NS, WIDTH, H)]

    b.append(accent_rule(NS, PAD, 48, 54))
    b.append(text(PAD + 68, 56, "IDENTITY", size=11, fill=C["dim"],
                  spacing=2.4, cls=NS + "-up"))
    b.append(text(WIDTH - PAD, 56, "04 / ID", size=11, fill=C["dimmer"],
                  spacing=2.4, anchor="end", cls=NS + "-up"))

    # ---------------------------------------------------------------- the card
    b.append(
        '<defs>'
        '<clipPath id="%s-card"><rect x="%s" y="%s" width="%s" height="%s" rx="16"/></clipPath>'
        '<linearGradient id="%s-cardbg" x1="0" y1="0" x2="0.6" y2="1">'
        '<stop offset="0" stop-color="#121c33"/><stop offset="1" stop-color="#0a1120"/>'
        "</linearGradient>"
        '<linearGradient id="%s-foil" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#ffffff" stop-opacity="0"/>'
        '<stop offset="0.45" stop-color="#9dc4ff" stop-opacity="0.16"/>'
        '<stop offset="0.5" stop-color="#ffffff" stop-opacity="0.26"/>'
        '<stop offset="0.55" stop-color="#ff8fa0" stop-opacity="0.14"/>'
        '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/>'
        "</linearGradient>"
        '<linearGradient id="%s-strap" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#1d2b47"/><stop offset="1" stop-color="#2a3d62"/>'
        "</linearGradient>"
        '<linearGradient id="%s-metal" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#5c6a83"/><stop offset="0.4" stop-color="#aebbd2"/>'
        '<stop offset="0.6" stop-color="#7f8da3"/><stop offset="1" stop-color="#4d5a72"/>'
        "</linearGradient>"
        "</defs>"
        % (NS, _n(CARD_X), _n(CARD_Y), _n(CARD_W), _n(CARD_H), NS, NS, NS, NS)
    )

    hang = ['<g class="%s-drop"><g class="%s-settle"><g class="%s-swing">' % (NS, NS, NS)]

    # lanyard straps
    hang.append(
        '<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="url(#%s-strap)" '
        'stroke="%s" stroke-width="0.8"/>'
        % (_n(PIVOT_X - 13), _n(PIVOT_Y), _n(CARD_X + CARD_W / 2 - 9), _n(CLASP_Y),
           _n(CARD_X + CARD_W / 2 - 1), _n(CLASP_Y), _n(PIVOT_X - 3), _n(PIVOT_Y),
           NS, C["line"])
    )
    hang.append(
        '<path d="M%s %s L%s %s L%s %s L%s %s Z" fill="url(#%s-strap)" '
        'stroke="%s" stroke-width="0.8"/>'
        % (_n(PIVOT_X + 3), _n(PIVOT_Y), _n(CARD_X + CARD_W / 2 + 1), _n(CLASP_Y),
           _n(CARD_X + CARD_W / 2 + 9), _n(CLASP_Y), _n(PIVOT_X + 13), _n(PIVOT_Y),
           NS, C["line"])
    )
    # metal clasp
    hang.append('<rect x="%s" y="%s" width="26" height="22" rx="4" '
                'fill="url(#%s-metal)" stroke="#39465d"/>'
                % (_n(CARD_X + CARD_W / 2 - 13), _n(CLASP_Y), NS))
    hang.append('<rect x="%s" y="%s" width="14" height="5" rx="2.5" fill="#2a3346"/>'
                % (_n(CARD_X + CARD_W / 2 - 7), _n(CLASP_Y + 8)))
    hang.append('<rect x="%s" y="%s" width="34" height="12" rx="6" fill="none" '
                'stroke="url(#%s-metal)" stroke-width="2.4"/>'
                % (_n(CARD_X + CARD_W / 2 - 17), _n(CLASP_Y + 18), NS))

    # card body
    hang.append('<rect x="%s" y="%s" width="%s" height="%s" rx="16" '
                'fill="url(#%s-cardbg)" stroke="%s"/>'
                % (_n(CARD_X), _n(CARD_Y), _n(CARD_W), _n(CARD_H), NS, C["line"]))
    hang.append('<g clip-path="url(#%s-card)">' % NS)
    hang.append('<rect x="%s" y="%s" width="%s" height="34" fill="%s"/>'
                % (_n(CARD_X), _n(CARD_Y), _n(CARD_W), C["blue"]))
    hang.append(text(CARD_X + 18, CARD_Y + 22, "DEVELOPER ID", size=10.5,
                     fill=C["white"], weight=700, spacing=2.2))
    hang.append(text(CARD_X + CARD_W - 18, CARD_Y + 22, "2026", size=10.5,
                     fill=C["white"], spacing=1.6, anchor="end"))

    import portrait
    hang.append(portrait.circular(NS, CARD_X + CARD_W / 2, CARD_Y + 102, 50,
                                  ring=False))
    hang.append('<circle cx="%s" cy="%s" r="50" fill="none" stroke="%s" '
                'stroke-opacity="0.8" stroke-width="2"/>'
                % (_n(CARD_X + CARD_W / 2), _n(CARD_Y + 102), C["blue"]))

    hang.append(text(CARD_X + CARD_W / 2, CARD_Y + 186, P["name_display"],
                     font="display", size=21, fill=C["text"], anchor="middle",
                     spacing=-0.2))
    hang.append(text(CARD_X + CARD_W / 2, CARD_Y + 206, P["role_primary"].upper(),
                     size=9.5, fill=C["blue_soft"], anchor="middle", spacing=1.6))
    hang.append('<rect x="%s" y="%s" width="%s" height="1" fill="%s"/>'
                % (_n(CARD_X + 24), _n(CARD_Y + 222), _n(CARD_W - 48), C["line"]))

    for i, (k, v) in enumerate([("GITHUB", "@" + P["github"]),
                                ("LOCATION", P["location"])]):
        y = CARD_Y + 246 + i * 24
        hang.append(text(CARD_X + 24, y, k, size=9, fill=C["dimmer"], spacing=1.4))
        hang.append(text(CARD_X + CARD_W - 24, y, v, size=10, fill=C["text"],
                         anchor="end"))

    hang.append(barcode(P["github"], CARD_X + 24, CARD_Y + 286, CARD_W - 48, 28))
    hang.append(text(CARD_X + CARD_W / 2, CARD_Y + 332, P["github"].upper(),
                     size=9, fill=C["dim"], anchor="middle", spacing=3.4))

    # foil sweep
    hang.append(
        '<rect x="-140" y="%s" width="120" height="%s" fill="url(#%s-foil)" '
        'transform="skewX(-18)" class="%s-foil"/>'
        % (_n(CARD_Y - 20), _n(CARD_H + 60), NS, NS)
    )
    hang.append("</g>")          # card clip
    hang.append("</g></g></g>")  # swing / settle / drop
    b.append("".join(hang))

    # ------------------------------------------------------- verified facts
    b.append(text(RX, 104, "VERIFIED FACTS", font="display", size=27,
                  fill=C["text"], spacing=-0.3, cls=NS + "-up",
                  extra='style="animation-delay:.1s"'))
    b.append(text(RX, 128, "Read from the GitHub REST API on %s. "
                  "Nothing here is estimated." % P["stats_asof"],
                  size=10, fill=C["dimmer"], cls=NS + "-up",
                  extra='style="animation-delay:.2s"'))

    for i, (label, value) in enumerate(P["stats"]):
        b.append(_stat_tile(i, label, value, RY + 24 + i * 76))

    # ---- language mix
    ly = RY + 24 + len(P["stats"]) * 76 + 16
    total = sum(v for _, v in P["lang_mix"])
    b.append('<g class="%s-up" style="animation-delay:.95s">' % NS)
    b.append(text(RX, ly, "LANGUAGE MIX BY REPOSITORY", size=9.5,
                  fill=C["dimmer"], spacing=1.8))
    b.append(text(RX + RW, ly, "%d REPOS" % total, size=9.5, fill=C["dimmer"],
                  spacing=1.4, anchor="end"))
    x = RX
    cols = [C["blue"], C["blue_soft"], C["crimson"], C["dimmer"]]
    for i, (name, v) in enumerate(P["lang_mix"]):
        w = RW * v / float(total)
        b.append('<rect x="%s" y="%s" width="%s" height="11" fill="%s" '
                 'class="%s-bar" style="transform-origin:%spx %spx;'
                 'animation-delay:%ss"/>'
                 % (_n(x), _n(ly + 14), _n(w - 2), cols[i % len(cols)], NS,
                    _n(x), _n(ly + 19.5), _n(1.0 + i * 0.09)))
        x += w
    lx = RX
    for i, (name, v) in enumerate(P["lang_mix"]):
        b.append('<circle cx="%s" cy="%s" r="3.4" fill="%s"/>'
                 % (_n(lx + 4), _n(ly + 48), cols[i % len(cols)]))
        b.append(text(lx + 14, ly + 52, "%s %d" % (name, v), size=10,
                      fill=C["dim"]))
        lx += 24 + len(name) * 6.3 + 14
    b.append("</g>")

    css = (
        "@keyframes {ns}-rule-kf{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
        ".{ns}-rule{{transform-origin:left center;animation:{ns}-rule-kf .7s "
        "cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-up-kf{{from{{opacity:0;transform:translateY(12px)}}"
        "to{{opacity:1;transform:translateY(0)}}}}"
        ".{ns}-up{{animation:{ns}-up-kf .7s cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-bar-kf{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
        ".{ns}-bar{{animation:{ns}-bar-kf .8s cubic-bezier(.2,.8,.2,1) both}}"

        # card drops in, overshoots, settles
        "@keyframes {ns}-drop-kf{{"
        "0%{{opacity:0;transform:translateY(-300px)}}"
        "18%{{opacity:1}}"
        "52%{{transform:translateY(10px)}}"
        "70%{{transform:translateY(-5px)}}"
        "86%{{transform:translateY(2px)}}"
        "100%{{opacity:1;transform:translateY(0)}}}}"
        ".{ns}-drop{{animation:{ns}-drop-kf 1.5s cubic-bezier(.3,.7,.3,1) both}}"

        # damped pendulum, once
        "@keyframes {ns}-settle-kf{{"
        "0%{{transform:rotate(-6.4deg)}}"
        "26%{{transform:rotate(4.1deg)}}"
        "50%{{transform:rotate(-2.5deg)}}"
        "74%{{transform:rotate(1.4deg)}}"
        "100%{{transform:rotate(0deg)}}}}"
        ".{ns}-settle{{transform-origin:{px}px {py}px;"
        "animation:{ns}-settle-kf 3.4s cubic-bezier(.4,0,.2,1) .9s both}}"

        # then a gentle, permanent +/-1.7 degree swing
        "@keyframes {ns}-swing-kf{{"
        "0%,100%{{transform:rotate(-1.7deg)}}50%{{transform:rotate(1.7deg)}}}}"
        ".{ns}-swing{{transform-origin:{px}px {py}px;"
        "animation:{ns}-swing-kf 5.6s ease-in-out 4.4s infinite forwards}}"

        # foil sweep: quick pass, long pause
        "@keyframes {ns}-foil-kf{{"
        "0%{{transform:skewX(-18deg) translateX(0)}}"
        "26%{{transform:skewX(-18deg) translateX(620px)}}"
        "100%{{transform:skewX(-18deg) translateX(620px)}}}}"
        ".{ns}-foil{{animation:{ns}-foil-kf 7s cubic-bezier(.4,0,.3,1) 2.4s "
        "infinite both}}"
    ).format(ns=NS, px=_n(PIVOT_X), py=_n(PIVOT_Y))

    disp = (P["name_display"] + "VERIFIED FACTS"
            + "".join(v for _, v in P["stats"]) + "0123456789")
    mono = "".join(
        ["IDENTITY", "04 / ID", "DEVELOPER ID", "2026", "VERIFIED", "GITHUB",
         "LOCATION", "@" + P["github"], P["github"].upper(), P["location"],
         P["role_primary"].upper(), P["stats_asof"],
         "Read from the GitHub REST API on . Nothing here is estimated.",
         "LANGUAGE MIX BY REPOSITORY", "REPOS", "PORTRAIT", "AT", "0123456789"]
        + [l for l, _ in P["stats"]]
        + [n for n, _ in P["lang_mix"]]
    )

    return document(
        NS, WIDTH, H, "".join(b), css, disp, mono,
        "%s — developer ID card and verified GitHub facts" % P["name_display"],
        "ID card for %s (@%s), %s. %s."
        % (P["name_display"], P["github"], P["role_primary"],
           "; ".join("%s %s" % (k.lower(), v) for k, v in P["stats"])),
    )
