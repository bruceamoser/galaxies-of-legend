# Galaxies of Legend — Player's Book

The initial level 1–10 player-book manuscript, built in Typst with the GOL cover, crest and palette. The PDF is `output/galaxies-of-legend-players-book.pdf`.

## Edit the book

- `manuscript/`: player-facing teaching chapters in editable Markdown.
- `../ancestries/`, `../origins/`, `../classes/`, `../disciplines/`, `../cards/`, `../equipment/`: source catalog entries.
- `template.typ`: typography, page furniture, ability headers, tables and callouts.
- `book.typ`, `cover.typ`, `sheets.typ`: assembly, cover and printable sheets.
- `fonts/`: bundled open-license typefaces and their OFL notices.
- `art/`: the cover illustration and orbital crest.
- `build.py`: reads Markdown and creates the disposable `generated/body.typ` and manifest. It never rewrites the source catalog. Do not edit generated files by hand.

## Build

Requires Python 3 with `markdown-it-py` and Typst 0.15.1.

```sh
python3 -m pip install -r design/player-book/requirements.txt
python3 design/index.py
python3 design/audit.py
TYPST=/path/to/typst python3 design/player-book/build.py --compile
```

If `TYPST` is unset, the script uses Typst on PATH. Fonts are loaded from the repository. Generated files and PDFs are ignored build artifacts.

## Current baseline

The current expanded reading review contains 18 disciplines, 10 classes, 12 cultures, 12 backgrounds, 78 ability cards and 13 equipment entries. Ten playtest ancestries appear in Chapter 3. Appendix A provides associated star systems and species baselines. All additions and ship construction values are untested proposals.

See [design/README.md](../README.md) for the source map and [open-decisions.md](../open-decisions.md) for deferred content.

## Current three-book Starter Kit

The Player's Book contains the complete character and HOL personal-harm foundation, all 280 wound entries, and the four character sheets. Chapter 10 is a short reference to the separate Starship Manual. Ship construction and the two ship sheets are excluded from this volume.

The companion Starship Manual owns ship rules and records. The Sector Architect's Book contains base adjudication, preparation, threat seeds and worksheets. `python3 release/build-starter-kit.py` builds, checks and packages the coordinated review edition. Earlier single-book export scripts are historical helpers and are not the current release path.
