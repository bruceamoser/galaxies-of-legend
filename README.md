# Galaxies of Legend

**A science-fiction TTRPG built on the Legend System.**

Build a crew from an ancestry, culture, background and class. Roll 3d6 plus one attribute, apply Boons and Banes, and read the card's Weak, Standard or Strong outcome. The ship is a shared character: Hull, DR, systems and Consumable Dice. FTL is a preparation problem, not a travel cutscene.

This repository is the **expanded design review** and the Player's Book build pipeline. It is intentionally smaller than the eventual game.

## Current contents

| Content | Count |
|---|---:|
| Ancestry placeholders (not finished options) | 4 |
| Cultures | 12 |
| Backgrounds | 12 |
| Classes | 10 |
| Disciplines | 18 |
| Ability cards | 69 |
| Equipment entries | 10 |

The Player's Book covers levels 1–10, character creation, abilities, equipment, harm and recovery, starships, FTL and printable sheets.

## Build the book

With Python 3, `markdown-it-py` and Typst 0.15.1:

```sh
python3 -m pip install -r design/player-book/requirements.txt
python3 design/index.py
python3 design/audit.py
python3 design/player-book/build.py --compile
```

The PDF is written to `design/player-book/output/galaxies-of-legend-players-book.pdf`. Generated files and PDFs are ignored.

## Source map

- [Current design](design/README.md): catalog and scope.
- [Ancestries](design/ancestry.md), [cultures and backgrounds](design/culture-background.md), [classes](design/class.md), [disciplines](design/disciplines.md).
- [Abilities](design/catalog.md), [card conventions](design/card-conventions.md).
- [Equipment](design/equipment.md), [market](design/market.md), [starting coins](design/starting-coins.md).
- [Player's Book](design/player-book/README.md): Typst build and manuscript.
- [Open decisions](design/open-decisions.md): deferred classes, ship numbers and playtest boundaries.

## Status

The character catalog has passed structural checks. The ship system and book presentation are in design review as of 2026-11-02; this does not establish readiness for table playtesting. See [ship review delta](design/system-deltas/2026-11-02-ship-review.md). The cover and crest are real assets; interior art is a placeholder in this edition.

Git history is the archive. Do not treat generated Typst or PDFs as editable sources.

## Release preparation

- [Initial release review](release/review.md)
- [Artwork production plan](release/artwork-plan.md)

The reading-review layout uses white pages, Oswald headings, Roboto text, black and blue-teal structure with red accents. Gold is limited to rules callouts and the existing crest. Cinematic artwork establishes the tone; heavy decorative rails and missing-art boxes have been removed.

## Expanded roster and ship builder

The current reading revision fixes ability readability and the class-cost table. The eighteen-field roster matches HOL's field count; [coverage waves](design/ability-coverage.md) define later ability work. Ancestries are placeholders awaiting Bruce.

Ships use five frame sizes, die allocation costs and required/optional modules. Run `python3 design/ship_builder.py` to check the three budgeted builds, or pass a JSON ship file. The [ship chapter](design/player-book/manuscript/11-starships.md) teaches construction and operation; the [delta](design/system-deltas/2026-11-02-expanded-roster-and-ships.md) records replacements to the earlier proposal.
