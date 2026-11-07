"""Write animation-free copies of every asset to assets/static/.

Useful for checking the readable fallback: whatever a viewer sees when
animation is unsupported or the reader has reduced motion turned on.

    python build/tools/make_static.py
"""
import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "assets")
DST = os.path.join(SRC, "static")

KEYFRAMES = re.compile(r"@keyframes[^{]*\{(?:[^{}]*\{[^{}]*\})*[^{}]*\}")
ANIM_DECL = re.compile(r"animation[a-z-]*\s*:[^;}]*;?")
SMIL = re.compile(r"<animate[^>]*/>|<animate[^>]*>.*?</animate>", re.S)
INLINE_ANIM = re.compile(r'style="([^"]*)"')


FACE_END = "format('woff2');}"


def strip(svg):
    svg = SMIL.sub("", svg)

    # Only touch the rule block, never the base64 @font-face payloads: the
    # letters "animation" can and do occur inside base64 text.
    head, sep, tail = svg.rpartition(FACE_END)
    if not sep:
        head, sep, tail = "", "", svg
    cut = tail.index("</style>")
    rules, rest = tail[:cut], tail[cut:]

    rules = KEYFRAMES.sub("", rules)
    rules = ANIM_DECL.sub("", rules)

    def fix(m):
        kept = [d for d in m.group(1).split(";")
                if d.strip() and not d.strip().startswith("animation")]
        return 'style="%s"' % ";".join(kept) if kept else ""

    return head + sep + rules + INLINE_ANIM.sub(fix, rest)


def main():
    os.makedirs(DST, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(SRC, "*.svg"))):
        with open(path, encoding="utf-8") as fh:
            out = strip(fh.read())
        dst = os.path.join(DST, os.path.basename(path))
        with open(dst, "w", encoding="utf-8") as fh:
            fh.write(out)
        print("  static/%-18s %6.1f KB" % (os.path.basename(path),
                                           len(out.encode()) / 1024))


if __name__ == "__main__":
    main()
