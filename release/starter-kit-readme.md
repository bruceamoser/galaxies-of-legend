# Galaxies of Legend Starter Kit v0.1.1

**Design review edition · 5 November 2026**

## Read these books together

- **Player’s Book** covers creation and advancement, ten illustrated ancestries and their systems, 18 cultures, 16 backgrounds, ten classes, 18 disciplines, 296 ability cards, and the personal harm and recovery rules. Chapter 7 contains all 280 wound results. Chapter 8 separates Basic Actions from learned Universal Abilities.
- **Starship Manual** covers construction, systems and wear, stations, combat, repairs, FTL, and three checked ship builds. It includes the worked 24-SP Scout Cutter and six fillable painted hull records.
- **Sector Architect’s Book** covers adjudication, sector preparation, hazards, campaigns, 67 adversary profiles including The Slop, 81 reusable adversary abilities, 27 companions, and six worked encounters. It includes four SA worksheets and a provisional Combat Value reference.

The books folder contains the three PDFs. The examples and sheets folders also provide the worked cutter and painted ship records as separate files.

## Review status

Character options, ship procedures, environmental fixtures, and adversaries include untested proposals. Encounter CVs are estimates for comparison. A starter adventure, pregenerated crew, and encounter calibration remain open.

## Source and verification

The source archive contains the editable manuscripts, Typst templates, fonts, art, data, tests, and release builder. MANIFEST.json records the source commit, book page counts, and hashes. SHA256SUMS covers the package payload.

To rebuild, install the dependencies in `design/player-book/requirements.txt`, provide Typst 0.15.1, and run `python3 release/build-starter-kit.py --books-only`. Omit `--books-only` to generate the full package under `output/starter-kit/v0.1.1-review/`.
