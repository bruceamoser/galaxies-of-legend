# Layout notes

## Construction

This book uses the same construction mechanism as the *Heroes of Legend* Player's Book: authored Markdown is parsed by `build.py` into disposable Typst, assembled by `book.typ`, and compiled with Typst 0.15.1. The source records are never rewritten by the builder.

## Geometry and type

- US Letter, 612 × 792 pt; 42 pt outer margins.
- EB Garamond body, Cinzel headings, Almendra optional display.
- Two-column reading columns for prose and catalog entries.
- Ability cards use the same tier diamond, header bar and Weak/Standard/Strong structure as the HOL cards.

## GOL identity

The palette replaces the HOL forest/ivory with deep space, teal and gold. The cover uses the Galaxies of Legend logo-free illustration with native editable type and the orbital crest. Interior illustrations are placeholders in this initial edition; the template falls back to a bordered production box.

## Current proof

The initial build is 55 pages: cover, title, contents, eleven chapters, printable sheets. It is a digital playtest proof, not a print-production certification.

## Brand alignment for initial release

The supplied Galaxies of Legend Brand Guide governs this edition. Stellar White replaces parchment; Void Black is primary text, Nebula Teal headings/UI, Mythic Gold borders, Warning Crimson reserved for danger. Roboto body and data, Oswald ordinary headings and cover display, Cinzel chapter titles and LEGEND. Fonts and OFL notices are bundled. Keep the existing letter page and two-column structure for digital playtesting.

## Tech vector revision

Reusable SVG rails, table caps and page frame now live in art/vector/. Decoration uses black, Nebula Teal blue and Warning Crimson; gold remains only in rules callout bars. Cards use white panels, cool grids and square corners. Oswald replaces fantasy display type in chapter titles and printable sheets at Bruce’s direction.
