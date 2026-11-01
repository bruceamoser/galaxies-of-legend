# Galaxies of Legend

**A science-fiction TTRPG built on the Legend System.**

Build a crew from a homeworld, culture, background and class. Roll 3d6 plus one attribute, apply Boons and Banes, and read the card's Weak, Standard or Strong outcome. The ship is a shared character: Hull, DR, systems and Consumable Dice. FTL is a preparation problem, not a travel cutscene.

This repository is the **initial playtest data set** and the Player's Book build pipeline. It is intentionally smaller than the eventual game.

## Current contents

| Content | Count |
|---|---:|
| Homeworlds | 4 |
| Homeworld traits | 20 |
| Cultures | 4 |
| Backgrounds | 4 |
| Classes | 6 |
| Disciplines | 9 |
| Ability cards | 48 |
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
- [Homeworlds](design/ancestry.md), [cultures and backgrounds](design/culture-background.md), [classes](design/class.md), [disciplines](design/disciplines.md).
- [Abilities](design/catalog.md), [card conventions](design/card-conventions.md).
- [Equipment](design/equipment.md), [market](design/market.md), [starting coins](design/starting-coins.md).
- [Player's Book](design/player-book/README.md): Typst build and manuscript.
- [Open decisions](design/open-decisions.md): deferred classes, ship numbers and playtest boundaries.

## Status

The catalog is approved for initial playtesting. Structural checks do not certify balance. The cover and crest are real assets; interior art is a placeholder in this edition.

Git history is the archive. Do not treat generated Typst or PDFs as editable sources.
