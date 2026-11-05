# Galaxies of Legend design

Current reading review: 18 disciplines, 10 classes, 12 cultures, 12 backgrounds, 78 ability cards and 13 equipment entries. All additions are playtest proposals.

- [Ancestries](ancestry.md): four placeholders, awaiting Bruce's authored material. Legacy homeworlds are excluded.
- [Cultures and backgrounds](culture-background.md)
- [Classes](class.md)
- [Disciplines](disciplines.md) and [ability coverage waves](ability-coverage.md)
- [Ability catalog](catalog.md), [equipment](equipment.md), [market](market.md), [starting coins](starting-coins.md)
- [Ship rules](starship-manual/manuscript/02-rules.md), [construction data](ships/construction.json), [budgeted examples](ships/examples.json)
- [Open decisions](open-decisions.md)

Run `python3 design/ship_builder.py` to validate sample ships, or supply a JSON ship file. The Player's Book reads authored Markdown, not generated Typst. Run index.py, audit.py and player-book/build.py --compile after source changes.

## Three-book Starter Kit

The [Player's Book](player-book/README.md) owns the complete character foundation. The [Starship Manual](starship-manual/README.md) owns construction and ship operations. The [Sector Architect's Book](sa-book/README.md) owns preparation, rulings and opposition seeds. Build and package all three with `python3 release/build-starter-kit.py` after installing the book requirements and Typst 0.15.1.
