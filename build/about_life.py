"""assets/about-life.svg — capabilities list beside a three-slide interests carousel."""

from lib import (C, WIDTH, accent_rule, background, document, dot_texture,
                 panel, text, wrap, _n)

NS = "al"
H = 352
PAD = 44

CARD_X, CARD_Y, CARD_W, CARD_H = 500, 76, 336, 252


def build(P):
    caps = P["capabilities"]
    slides = P["interests"]
    n = len(slides)
    cycle = n * 4.0

    b = [dot_texture(NS), background(NS, WIDTH, H)]

    # ---- header
    b.append(accent_rule(NS, PAD, 48, 54))
    b.append(text(PAD + 68, 56, "WHAT I DO", size=11, fill=C["dim"],
                  spacing=2.4, cls=NS + "-up"))
    b.append(text(WIDTH - PAD, 56, "02 / ABOUT", size=11, fill=C["dimmer"],
                  spacing=2.4, anchor="end", cls=NS + "-up"))
    b.append(text(PAD, 104, "CAPABILITIES", font="display", size=27,
                  fill=C["text"], spacing=-0.3, cls=NS + "-up",
                  extra='style="animation-delay:.1s"'))

    # ---- capability rows
    for i, (title, sub) in enumerate(caps):
        y = 150 + i * 52
        d = 0.24 + i * 0.1
        b.append('<g class="%s-up" style="animation-delay:%ss">' % (NS, _n(d)))
        b.append('<rect x="%s" y="%s" width="2.5" height="30" rx="1.25" fill="%s"/>'
                 % (_n(PAD), _n(y - 13), C["blue"] if i % 2 == 0 else C["crimson"]))
        b.append(text(PAD + 16, y - 11, "%02d" % (i + 1), size=9.5,
                      fill=C["dimmer"], spacing=1.2))
        b.append(text(PAD + 48, y, title, size=13.5, fill=C["text"], weight=700))
        b.append(text(PAD + 48, y + 17, sub, size=10.5, fill=C["dim"]))
        b.append("</g>")

    # ---- interests carousel
    b.append('<g class="%s-up" style="animation-delay:.3s">' % NS)
    b.append(panel(CARD_X, CARD_Y, CARD_W, CARD_H, fill=C["panel2"]))
    b.append('<rect x="%s" y="%s" width="54" height="2.5" fill="%s"/>'
             % (_n(CARD_X + 24), _n(CARD_Y + 26), C["crimson"]))
    b.append(text(CARD_X + 24, CARD_Y + 54, "INTERESTS", size=10.5,
                  fill=C["dim"], spacing=2.4))
    b.append(text(CARD_X + CARD_W - 24, CARD_Y + 54, "AUTOPLAY", size=9.5,
                  fill=C["dimmer"], spacing=1.6, anchor="end"))

    for i, s in enumerate(slides):
        lines = wrap(s["body"], 44)[:3]
        g = ['<g class="%s-slide" style="animation-delay:%ss;'
             'animation-duration:%ss">' % (NS, _n(i * 4.0), _n(cycle))]
        g.append(text(CARD_X + 24, CARD_Y + 110, "%02d" % (i + 1),
                      font="display", size=36, fill=C["line"]))
        g.append(text(CARD_X + 24, CARD_Y + 146, s["title"], font="display",
                      size=17, fill=C["text"], spacing=-0.2))
        for j, ln in enumerate(lines):
            g.append(text(CARD_X + 24, CARD_Y + 174 + j * 18, ln, size=11,
                          fill=C["dim"]))
        g.append("</g>")
        b.append("".join(g))

    # ---- segment progress bars
    seg_w = (CARD_W - 48 - (n - 1) * 8) / n
    for i in range(n):
        x = CARD_X + 24 + i * (seg_w + 8)
        y = CARD_Y + CARD_H - 26
        b.append('<rect x="%s" y="%s" width="%s" height="3" rx="1.5" fill="%s"/>'
                 % (_n(x), _n(y), _n(seg_w), C["line"]))
        b.append(
            '<rect x="%s" y="%s" width="%s" height="3" rx="1.5" fill="%s" '
            'class="%s-seg%d" style="transform-origin:%spx %spx"/>'
            % (_n(x), _n(y), _n(seg_w), C["blue"], NS, i, _n(x), _n(y + 1.5))
        )
    b.append("</g>")  # closes the carousel card group

    css = (
        "@keyframes {ns}-rule-kf{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}"
        ".{ns}-rule{{transform-origin:left center;animation:{ns}-rule-kf .7s "
        "cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-up-kf{{from{{opacity:0;transform:translateY(12px)}}"
        "to{{opacity:1;transform:translateY(0)}}}}"
        ".{ns}-up{{animation:{ns}-up-kf .7s cubic-bezier(.2,.8,.2,1) both}}"
        "@keyframes {ns}-slide-kf{{"
        "0%{{opacity:0;transform:translateX(16px)}}"
        "4%{{opacity:1;transform:translateX(0)}}"
        "30%{{opacity:1;transform:translateX(0)}}"
        "34%{{opacity:0;transform:translateX(-16px)}}"
        "100%{{opacity:0;transform:translateX(-16px)}}}}"
        ".{ns}-slide{{opacity:0;animation-name:{ns}-slide-kf;"
        "animation-timing-function:cubic-bezier(.2,.8,.2,1);"
        "animation-iteration-count:infinite;animation-fill-mode:both}}"
        ".{ns}-slide:first-of-type{{opacity:1}}"
    ).format(ns=NS)

    # one keyframe set per segment so the bars fill in sequence
    for i in range(n):
        start = i / float(n) * 100.0
        end = (i + 1) / float(n) * 100.0
        css += (
            "@keyframes %s-seg%d-kf{0%%,%.4f%%{transform:scaleX(0)}"
            "%.4f%%,100%%{transform:scaleX(1)}}"
            ".%s-seg%d{transform:scaleX(0);animation:%s-seg%d-kf %ss linear infinite both}"
            % (NS, i, start, end, NS, i, NS, i, _n(cycle))
        )

    disp = "".join([c[0] for c in caps]) + "CAPABILITIES" + \
           "".join(s["title"] for s in slides) + "0123456789"
    mono = "".join(
        ["WHAT I DO", "02 / ABOUT", "INTERESTS", "AUTOPLAY", "0123456789"]
        + [c[0] + c[1] for c in caps]
        + [s["body"] for s in slides]
    )

    return document(
        NS, WIDTH, H, "".join(b), css, disp, mono,
        "What %s builds" % P["name_display"],
        "Capabilities: " + "; ".join(c[0] for c in caps)
        + ". Interests: " + ", ".join(s["title"] for s in slides) + ".",
    )
