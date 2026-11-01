# Galaxies of Legend — current design

This `design/` tree is the authored source for the game and the Player's Book. The Markdown records are the authority; the book build reads them and writes only disposable files under `player-book/generated/` and `player-book/output/`.

The initial data set is deliberately small. It establishes the construction mechanism and the first playable slice, not the final catalog.

## Find the material

- [Design intent](design-intent.md) and [open decisions](open-decisions.md)
- [Homeworlds](ancestry.md), [cultures and backgrounds](culture-background.md), [classes](class.md), [disciplines](disciplines.md)
- [Abilities](catalog.md), [card conventions](card-conventions.md)
- [Equipment](equipment.md), [market](market.md), [starting coins](starting-coins.md)
- [Player's Book](player-book/README.md)

## Current scope

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

## Edit and validate

Edit the Markdown directly. Stable IDs identify records even when names change.

```sh
python3 design/index.py
python3 design/audit.py
python3 design/player-book/build.py --compile
```

`index.py` rebuilds navigation only. It never rewrites authored entries. `audit.py` checks record structure, links, DP budgets, coin range and derived values. The build requires Python 3 with `markdown-it-py` and Typst 0.15.1.

## Working rule

A new game built on the Legend System replaces the setting and the lists of options. It does not redesign the character-building chassis. If a rule needs to leave the chassis, record a system delta in [open-decisions.md](open-decisions.md) before writing it into the catalog.
