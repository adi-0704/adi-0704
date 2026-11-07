# The two image prompts

> **Done — 07 Nov 2026.** Both portraits are generated and wired in. The files
> you sent had the transparency checkerboard baked into the pixels instead of a
> real alpha channel, so `build/tools/extract_alpha.py` keys the grid out,
> removes the generator watermark and re-exports proper PNGs with alpha. The
> originals are kept in `source-images/original/`.
> Keep the rest of this file for when you want to regenerate the artwork.


Run these in an **image-capable** AI tool — [claude.ai](https://claude.ai) or ChatGPT.
Not here: this Claude Code session has no image generation.

Run them **separately**. Prompt 02 needs the output of prompt 01 attached.

---

## Prompt 01 — The stylized portrait

**Attach:** the photo of yourself (the café one you sent me is fine).
**Save the result as:** `id.png`

```
Transform my attached photo into a premium semi-realistic illustrated profile
portrait. Preserve my recognizable face, skin tone, hairstyle and glasses. Give
me a confident, approachable expression and stylish dark streetwear, with subtle
electric-blue and crimson rim light. Frame me from the chest up with the full
head visible. Use a genuinely transparent background with alpha, not a
checkerboard drawn into the image. No text, badges, logos or extra objects.
Export a sharp, high-resolution PNG.
```

> I don't see glasses in the photo you sent. Drop "and glasses" from the prompt
> unless you want them added.

---

## Prompt 02 — The right-pointing character

**Attach:** `id.png` from prompt 01 (not the original photo).
**Save the result as:** `right_pointing.png`

```
Use the attached stylized portrait as the identity and style reference. Create
the same person in the same outfit, shown from the waist up, positioned to the
left and pointing toward the viewer's RIGHT with a natural hand pose. Leave room
around the head and pointing hand; do not crop either. Match the face, hair,
colors and illustration style. Use a genuinely transparent alpha background. No
text, handles, logos, arrows or badges. Export a high-resolution PNG.
```

---

## Then put both files here

```
adi-0704/
  source-images/
    id.png              <- from prompt 01
    right_pointing.png  <- from prompt 02
```

Tell me when they're in and I'll inline them into the SVGs as base64.

---

## Checking transparency before you send them

Open each PNG on a **dark** background and a **light** one. If you can see gray
checkerboard squares, the transparency was drawn into the image rather than
being real alpha — run it through a background remover and re-export as PNG
with alpha. Keep the face intact.
