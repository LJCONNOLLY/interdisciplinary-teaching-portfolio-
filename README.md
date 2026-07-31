# Teaching Portfolio

Plain static HTML/CSS/JS. No build step, no framework. Deploys to GitHub Pages
by pushing these files to `main`.

## Pages

Five separate HTML files, each a complete page (no server-side includes, so
the nav/footer markup is duplicated in each file by necessity — edit all five
if that shared chrome changes):

- `index.html` — home: header plate, name/tagline, links to the other four pages
- `philosophy.html` — full teaching statement, with its own in-page sub-nav
- `syllabus.html` — sample syllabus placeholder
- `assignment.html` — signature assignment placeholder
- `courses.html` — courses prepared to teach

## Filling in the placeholders

`syllabus.html` and `assignment.html` are intentionally empty records — real
field labels with blank ruled areas, not invented content. Each is wrapped in
an HTML comment block:

```html
<!-- BEGIN PLACEHOLDER: SYLLABUS — paste real content into each .field-empty below -->
...
<!-- END PLACEHOLDER: SYLLABUS -->
```

To fill one in: replace the empty `<div class="field-empty ...">` with your
real content (text, lists, whatever fits), and remove the `field-empty` class
and `aria-hidden="true"` attribute since the div will no longer be a blank
ruled area. Update that card's metadata row (`FIELDS` / `LEVEL` / `STATUS`)
to reflect the real course once it exists — `STATUS` in particular should
move off `Not yet written`.

Two files are linked but not yet in the repo: `assets/teaching-statement.pdf`
and `assets/cv.pdf`. Drop the real files in at those paths and the existing
links will resolve.

## Accessibility

- Every text size on the page is at least 1.35rem (21.6px), which clears
  16pt (21.3px). Sizes are all in `rem` against the page root, not fixed `px`.
- `js/text-size.js` adds an on-page A−/Reset/A+ control that scales the
  entire page (it changes the root font-size; everything else follows because
  it's all `rem`-based) and remembers the choice in `localStorage` across
  pages and visits.
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
