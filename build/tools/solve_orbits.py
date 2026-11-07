"""Brute-force the three orbit phase angles so no icon/label box overlaps.

Run after changing PROFILE["orbits"], then paste the phases into stack.py.

    python build/tools/solve_orbits.py
"""
import itertools
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from profile import ICON_LABELS, PROFILE  # noqa: E402
import stack  # noqa: E402

CX, CY = stack.CX, stack.CY


def boxes(phases):
    out = []
    for k, (rx, ry, tilt, _phase, isz) in enumerate(stack.ORBITS):
        slugs = PROFILE["orbits"][k]
        for j, slug in enumerate(slugs):
            deg = phases[k] + j * (360.0 / len(slugs))
            x, y = _pt(rx, ry, tilt, deg)
            label = ICON_LABELS.get(slug, slug)
            lw = max(isz * 2.1, len(label) * 5.4)
            out.append((x - lw / 2, y - isz, x + lw / 2, y + isz * 1.6 + 6))
    return out


def _pt(rx, ry, tilt, deg):
    t = math.radians(deg)
    x, y = rx * math.cos(t), ry * math.sin(t)
    a = math.radians(tilt)
    return (CX + x * math.cos(a) - y * math.sin(a),
            CY + x * math.sin(a) + y * math.cos(a))


def overlap(a, b):
    ox = min(a[2], b[2]) - max(a[0], b[0])
    oy = min(a[3], b[3]) - max(a[1], b[1])
    return max(0.0, ox) * max(0.0, oy)


def main(step=6):
    best = None
    rng = range(0, 360, step)
    for p in itertools.product(rng, repeat=3):
        bx = boxes(p)
        bad = sum(overlap(a, b) for a, b in itertools.combinations(bx, 2))
        if best is None or bad < best[0]:
            best = (bad, p, max(a[3] for a in bx))
        if bad == 0:
            break
    print("overlap area %.2f  phases %s  lowest content y %.1f"
          % (best[0], best[1], best[2]))
    print("chips should start below y = %.0f" % (best[2] + 20))


if __name__ == "__main__":
    main()
