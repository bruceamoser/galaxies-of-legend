# Authoring rules

The Markdown in this directory is the approved source for *Galaxies of Legend*. The Player's Book consumes it. Git history is the archive. Do not treat generated Typst or PDF files as editable sources.

## Voice

- Describe what a character actually does. A vivid sentence is good; a slogan is not a procedure.
- Put the mechanical permission in the **Rules** section. Flavor never grants a sense, item, movement mode, resistance or immunity.
- Use **Sector Architect (SA)** for the facilitator.
- Use **ancestry**, **culture**, **background**, **class**, **discipline**, **ability**, **station**, **Hull**, **DR** and **Consumable Die** consistently.

## Structure

- Ancestry: HP, base Speed, coin contribution, five traits, choose two. Current placeholders await Bruce's material; do not invent alien benefits. Legacy homeworlds are reference only.
- Culture and background: one paired rank-1 discipline and ability. Do not mix pairs.
- Class: two attribute minimums, HP, coins, two starting rank-1 disciplines, rank prices, signatures at 1/3/7.
- Discipline: ranks 1–3 are prerequisites. They grant no passive bonus by default.
- Ability: action, attribute, target, outcomes, duration, equipment, tier, DP, requirements, limits, ID.
- Equipment: category, damage type, Bulk, hands, cost, explicit effect.

## Review

- Every rule is labeled **playtest** if it has not been tested at a table.
- New mechanics require a system delta with rule changed, replacement, reason and balance impact.
- Do not silently add a bonus to a homeworld trait or class feature to fix a different problem.
- Run `python3 design/index.py` and `python3 design/audit.py` before committing.
