# Galaxies of Legend — Player's Book

The initial level 1–10 player-book manuscript, built in Typst with the GOL cover, crest and palette. The PDF is `output/galaxies-of-legend-players-book.pdf`.

## Edit the book

- `manuscript/`: player-facing teaching chapters in editable Markdown.
- `../homeworlds/`, `../origins/`, `../classes/`, `../disciplines/`, `../cards/`, `../equipment/`: source catalog entries.
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

This is the **initial playtest data set**: four homeworlds, four cultures, four backgrounds, six classes, nine disciplines, forty-eight ability cards and ten equipment entries. Ship Hull, DR, FTL clocks and the wound table are seed values marked playtest in the design notes.

See [design/README.md](../README.md) for the source map and [open-decisions.md](../open-decisions.md) for deferred content.

## Current reading review

The 2026-11-02 proof expands Chapter 10 with proposed ship procedures and worked examples, and adds ship records to the back. It uses a cleaner cinematic visual direction. All ship additions await Bruce's review; the character chassis is unchanged.

After compiling, run `python3 release/export-review.py` (requires `pypdf`) to copy the full reading PDF and extract the ship chapter and ship sheets into `output/pdf/`.
