# Third-party assets embedded in these SVGs

## Fonts

Both typefaces are embedded as base64 WOFF2, subset to only the glyphs each
image actually draws. Both are licensed under the SIL Open Font License 1.1,
which permits embedding.

| Font | Used for | License | Full text |
| --- | --- | --- | --- |
| **Archivo Black** — Omnibus-Type | Display headings and names | SIL OFL 1.1 | [`build/vendor/fonts/OFL-ArchivoBlack.txt`](./build/vendor/fonts/OFL-ArchivoBlack.txt) |
| **JetBrains Mono** — JetBrains s.r.o. | All monospace text | SIL OFL 1.1 | [`build/vendor/fonts/OFL-JetBrainsMono.txt`](./build/vendor/fonts/OFL-JetBrainsMono.txt) |

The OFL requires that the embedded fonts are not sold on their own and that the
license travels with them — both satisfied by this file and the two texts above.

## Icons

Brand marks come from [Simple Icons](https://github.com/simple-icons/simple-icons),
released under **CC0 1.0 Universal**. The icon files are public domain; the
brands they depict remain trademarks of their respective owners and are used
here only to identify the technologies, which is nominative use.

Icons embedded: Python, TypeScript, JavaScript, Node.js, React, OpenAI, Gemini,
LangChain, n8n, FastAPI, PostgreSQL, Docker, Supabase, Git, GitHub, Vercel,
LinkedIn.

## Portrait images

`source-images/id.png` and `source-images/right_pointing.png` are generated
from a photograph of the repository owner and are his own. The generator wrote
its transparency checkerboard into the pixels rather than exporting alpha;
`build/tools/extract_alpha.py` recovers a real alpha channel from the untouched
originals in `source-images/original/`. They are palette-quantised, downscaled
to twice their drawn size and inlined as base64 at build time.

## Everything else

The layout, animation and build scripts in this repository are the owner's own
work and carry no third-party claims.
