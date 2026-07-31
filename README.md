# Teaching Portfolio

Plain static HTML/CSS/JS. No build step, no framework. Deploys to GitHub Pages
by pushing `index.html` (and its siblings) to `main`.

## Filling in the placeholders

The sample syllabus and signature assignment sections in `index.html` are
intentionally empty records — real field labels with blank ruled areas, not
invented content. Each is wrapped in an HTML comment block:

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
