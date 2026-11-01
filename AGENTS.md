# Galaxies of Legend

We are writing a science-fiction TTRPG on the Legend System. Bruce is the lead designer.

- Canonical rules and catalog: `design/**/*.md`.
- Player's Book: `design/player-book/`; built with Typst 0.15.1.
- Core roll: 3d6 + one attribute, with Boons/Banes; no skill bonus.
- The six attributes, character chassis and DP economy are inherited from the Legend System. A change to them needs a system delta.
- The ship is a shared character: Hull, DR, systems and Consumable Dice. A station is a job in the scene, not a class.
- Workflow: edit Markdown → run `python3 design/index.py` and `python3 design/audit.py` → build the PDF → review → commit.

Do not edit `design/player-book/generated/` or `design/player-book/output/`; they are disposable build artifacts. Git history is the archive.
