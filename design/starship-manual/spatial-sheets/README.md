# Spatial ship sheet prototype

Five landscape, fillable hull records place system boxes inside a top-down ship outline. A sixth page completes the existing Scout Cutter example. This is a layout proposal; it does not change construction rules or replace the current manual sheets yet.

The builder reads frame budgets, capacities, required systems, prices and the Scout example from `design/ships/`. Launch, Light, Medium, Heavy and Capital have 8, 12, 16, 22 and 30 boxes respectively. Each box represents one module position, not free equipment. Required boxes still need purchased dice. Location labels suggest placement without imposing restrictions. The paired engine housings depict one engine system.

Each box records system name, installed rating (DIE), current rating (NOW), and purchase cost (SP). The ship name, current Hull and SP ledger are also fillable. SP totals are entered manually; the PDF does not calculate or enforce a legal build. Higher-die prices and frame budgets remain proposals.

Run `python3 design/starship-manual/spatial-sheets/build.py` using a Python environment with ReportLab and pypdf. Output: `output/pdf/Galaxies-of-Legend-Spatial-Ship-Sheets-Prototype.pdf`.

The build validates page and box counts, box overlaps, required-system count, all 394 field values, widget counts and appearance streams. All six pages were rendered and visually inspected. The worked Light hull spends 24 SP on 10 modules, with two unused positions and zero remaining SP.
