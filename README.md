# Teaching Portfolio

Plain static HTML/CSS/JS. No build step, no framework. Deploys to GitHub Pages
by pushing these files to `main`.

## Pages

Five separate HTML files, each a complete page (no server-side includes, so
the nav/footer markup is duplicated in each file by necessity — edit all five
if that shared chrome changes):

- `index.html` — home: header plate, name/tagline, links to the other four pages
- `philosophy.html` — full teaching statement, with its own in-page sub-nav
- `syllabus.html` — links out to the real, separately-published syllabus (Technofeminisms in Practice)
- `assignment.html` — the real signature assignment (Technofeminisms in Practice final project), in full
- `courses.html` — courses prepared to teach

## Placeholders

Neither `syllabus.html` nor `assignment.html` is a placeholder anymore —
both link to or contain LJ's real content. If a future artifact needs the
empty-record placeholder treatment again, the pattern that was here is:
each field is a `.specimen-field` with a `.field-label` and either real
content or a blank `.field-empty field-empty--{sm,md,lg,xl}` div
(`aria-hidden="true"`), with the card's `STATUS` meta value reading
`Not yet written` until it's filled in. Wrap the block in
`<!-- BEGIN/END PLACEHOLDER: ... -->` comments so it's easy to find later.

`assets/teaching-statement.pdf` and `assets/cv.pdf` are generated from the
source docx files at the repo root (`Teaching Statement.docx`,
`Connolly CV.docx`) by `scripts/build_pdfs.py` — see below. Edit those docx
files and re-run the script rather than hand-editing the PDFs.

## Accessibility

- Every text size on the page is at least 1.35rem (21.6px), which clears
  16pt (21.3px). Sizes are all in `rem` against the page root, not fixed `px`,
  so browser-level zoom/text-size settings still work as expected.
- Skip-to-content link, visible focus states, semantic heading order, and
  `prefers-reduced-motion` support are all in place already.

## Regenerating the illustration assets

`assets/img/canopy.png` is the source watercolor. Everything else in
`assets/img/` (header plate, trailing vine cutout, section dividers) is
derived from it by `scripts/build_images.py`. Re-run this only if
`canopy.png` changes:

```
pip3 install Pillow numpy
python3 scripts/build_images.py
```

This is a one-time development tool — the site itself has no build step and
doesn't run this script.

## Regenerating the PDFs

`Teaching Statement.docx` and `Connolly CV.docx` at the repo root are the
source documents for the two downloadable PDFs. `scripts/build_pdfs.py`
reads their paragraph/bold structure directly (LibreOffice's headless
conversion wasn't reliable enough to depend on) and renders a plain PDF
styled with the site's own palette — not a pixel copy of the Word
formatting, but the same real text. Re-run after editing either docx:

```
pip3 install reportlab
python3 scripts/build_pdfs.py
```
