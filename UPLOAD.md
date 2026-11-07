# Putting this on your profile

No hosting, no deployment. A GitHub profile README is just a public repository
named exactly after your username.

## 1. Create the repo

On GitHub: **+ → New repository**.

- Repository name: **`adi-0704`** — it must match your username exactly, or
  GitHub will not treat it as a profile README.
- Visibility: **Public**.
- Tick **Add a README file**.

If `adi-0704/adi-0704` already exists, open it instead of creating a new one.

## 2. Upload the files

Unzip `adi-0704-profile.zip`. In the repo, choose **Add file → Upload files**,
then drag in:

```
README.md
assets/            <- the whole folder, structure preserved
LICENSES.md
```

Drag the `assets` **folder**, not the five SVGs on their own — the README
points at `./assets/hero.svg` and friends, and the paths must survive.

Uploading `build/`, `preview.html`, `PROMPTS.md` and `UPLOAD.md` is optional.
Keep `build/` if you want to be able to regenerate the images later; it is what
produces them, and `LICENSES.md` links into it for the font licenses.

## 3. Commit

Replace the starter README with the generated one, write a commit message, and
commit to the default branch. If you commit to a new branch instead, open and
merge the pull request afterwards.

## 4. Check it live

Visit **<https://github.com/adi-0704>**. Confirm that:

- all five images load, none shows a broken-image icon;
- every link under "Find me" and in the projects table opens correctly;
- it reads well on both desktop and phone.

## If something looks wrong

**An image doesn't load.** Check filename case — `about-life.svg`, not
`About-Life.svg` — and that `assets/` really is at the repository root next to
`README.md`, not nested one level deeper.

**You see an old version after re-uploading.** GitHub caches images behind its
camo proxy. Replace the SVG, then bump its cache-buster in `README.md` from
`?v=1` to `?v=2`.

**It renders but nothing moves.** Some viewers show a static frame rather than
playing SVG animation — that is the designed fallback and everything stays
readable. Check it in a desktop browser to see the motion. Readers who have
reduced motion enabled get the static frame on purpose.

## Changing the content later

Everything personal lives in one file: [`build/profile.py`](./build/profile.py).
Edit it, then:

```bash
python build/build.py
python build/tools/make_static.py
```

Re-upload `assets/`, and bump `?v=` in the README so the cache clears.
