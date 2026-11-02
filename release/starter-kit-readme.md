# Galaxies of Legend - Starter Kit v0.1.0

**First three-book edition. Status: design review. Date: 2 November 2026.**

## Read these books together

- **Player's Book:** creation, advancement, ancestry placeholders, twelve cultures, twelve backgrounds, ten classes, eighteen disciplines, seventy-eight abilities, equipment and the complete Legend harm foundation. Chapter 7 contains all 280 wound results; Chapter 10 explains the companion books.
- **Starship Manual:** construction, installed/current system dice, optional modules, crew stations, combat, repairs, FTL, three checked ship builds and two ship sheets. Character abilities remain in the Player's Book.
- **Sector Architect's Book:** rulings, sector/faction preparation, situations, encounters, eight proposed threat profiles, hazards, rewards, continuing campaigns and four worksheets.

The books folder contains the three PDFs. Each has a contents page and printed cross-book chapter references. Keep the Player's Book available for personal damage, Grit, Dying, Last Words, conditions, wound treatment and healing; the other books do not replace that foundation.

## This edition's limits

Ancestries await Bruce's authored material and are explicitly incomplete placeholders. Expanded character options and the ship construction system are untested proposals. SA threat profiles and hazard fixtures are authoring seeds without calibrated encounter values. Ship prices and several economic/environmental procedures remain open. Interior artwork remains a direction study. This is not a starter mission or a claim that the game is ready for table playtesting.

## Source and verification

The source archive contains Markdown, Typst, fonts, existing artwork, construction data, regression tests and the release builder. MANIFEST.json records the three PDFs, page counts and SHA-256 hashes. SHA256SUMS covers the review payload. The ZIP was checked for corruption and matching book contents.

To rebuild from the source archive, use Python 3, install `design/player-book/requirements.txt`, provide Typst 0.15.1, and run `python3 release/build-starter-kit.py --books-only`. Run without `--books-only` to create a fresh local package in `output/starter-kit/v0.1.0-review/`. The fonts are bundled. Rendering for visual review uses Poppler separately.

No GitHub publication or public release is implied by this local review package.
