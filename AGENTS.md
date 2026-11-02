# Galaxies of Legend

We are writing a science-fiction TTRPG on the Legend System. Bruce is the lead designer.

- Canonical rules and catalog: `design/**/*.md`.
- Player's Book: `design/player-book/`; built with Typst 0.15.1.
- Core roll: 3d6 + one attribute, with Boons/Banes; no skill bonus.
- The six attributes, character chassis and DP economy are inherited from the Legend System. A change to them needs a system delta.
- The ship is a shared character: Hull, DR, systems and Consumable Dice. A station is a job in the scene, not a class.
- Workflow: edit Markdown → run `python3 design/index.py` and `python3 design/audit.py` → build the PDF → review → commit.

Do not edit `design/player-book/generated/` or `design/player-book/output/`; they are disposable build artifacts. Git history is the archive.

## Preserve the shared survival foundation

Damage/resistance/weakness, Grit, Dying, Last Words, conditions, all five 56-entry wound tables and six RV treatment capabilities inherit the full HOL rules in `design/rules/`. Do not replace them with compact invented procedures or omit wound tables from the reading book. Grit never refreshes through ordinary rest. Any deliberate change must be explicit in a system delta and distinguish a proposal from Bruce's accepted foundation. `design/test_hol_restoration.py` protects all 280 wound rows against the recorded HOL baseline.
