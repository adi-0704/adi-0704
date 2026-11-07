"""Generate every asset in ../assets. Run: python build/build.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")

from profile import PROFILE  # noqa: E402

MODULES = ["hero", "about_life", "stack", "id_dashboard", "connect"]
FILENAMES = {
    "hero": "hero.svg",
    "about_life": "about-life.svg",
    "stack": "stack.svg",
    "id_dashboard": "id-dashboard.svg",
    "connect": "connect.svg",
}


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    for name in MODULES:
        if only and name not in only:
            continue
        try:
            mod = __import__(name)
        except ImportError:
            print("  skip %-14s (not written yet)" % name)
            continue
        svg = mod.build(PROFILE)
        path = os.path.join(OUT, FILENAMES[name])
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print("  %-18s %7.1f KB" % (FILENAMES[name], len(svg.encode()) / 1024))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
