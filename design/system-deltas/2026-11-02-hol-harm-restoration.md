# Restore the HOL harm foundation - 2026-11-02

**Requested correction:** GOL had simplified and changed the shared Legend damage, Grit, wounds, wound tables and healing rules. Restore the current HOL foundation rather than treating those omissions as approved system differences.

Baseline: HOL commit `25b80c9fe77d7baaec3f3a8a548c9663d0f39a30`. File hashes and the full wound-row digest are recorded in `../rules/hol-restoration.json`. The 280 wound rows are preserved exactly, including effects, treatment labels and RV. These are HOL's designer-reviewed working tables, not a new claim of balance validation.

| Incorrect or incomplete GOL draft | Restored foundation | Reason / effect |
|---|---|---|
| Rest refills Grit; Grit buys Boons or reduces damage | Safe breath restores HP only. Grit is a limited Dying-turn full-HP reserve; level grants add without refund | Restore the actual shared survival economy |
| Fortitude against target 10 while Dying | Standard Legend bands; Weak +1 mark, Standard no change, Strong stabilize; retained 111 +2, 666 heal 1 | Remove the invented target number |
| One d6 wound table and no reliable trigger | Every entry into Dying; 3d6 + prior-scar dice, max 5, highest 3 sorted as digits | Restore accumulated-scar risk and full severity |
| Three marks cause immediate death | Last Words: speech only; death at end of second following turn | Restore the farewell window and finality |
| Six placeholder injuries | Five full 56-row tables: Physical, Elemental, Mental, Radiant, Life/Necrotic | Preserve all 280 entries without rewriting alien applicability |
| Generic Medicine success removes a penalty | Six matching treatment capabilities; full hour; one attempt per wound per day across healers; 1/2/3 progress toward RV | Restore capabilities, time and cumulative recovery |
| HP restoration and scars conflated | HP healing does not remove wounds/scars, restore Grit or reverse Last Words | Keep distinct tracks |
| Bleeding at turn start; Frozen/Stunned shortcuts; prone melee bonus | Full HOL conditions, end-turn resolve then decay, starred contributions, Dazed/Grappled categories and 2-movement standing | Remove contradictory summaries and incidental riders |
| Generic armour DR against everything | Physical resistance; highest per type, cap 3; weakness before resistance; minimum 1 total personal damage | Restore the full damage procedure |
| GOL care cards omit healing costs and Field Surgery erases wounds | 1/3/7 HP cost before rolled HP healing, free hand, Life resistance; Field Surgery adds RV progress over a full hour | Remove hidden bypasses of the restored foundation |

## GOL presentations and proposals, explicitly separate from HOL

- Kinetic/Sonic describe Physical; Thermal describes Fire; Cryogenic describes Cold; Electrical describes Lightning. They do not create extra resistance pools.
- **Proposed mapping for review:** Corrosive to Physical; Radiation to Radiant. These mappings are GOL-specific and are not claims about HOL's original fiction.
- Medical Doses are science-fiction presentations of HOL's 6/10/16-HP d4 healing supplies, with the same free-hand, Maneuver, recipient Reaction, Life-resistance and after-use inventory procedure. Retained price proposals are 20/50/120 coins.
- Existing medical card outcomes remain GOL proposals, now subject to the inherited healing cost. Field Triage, Triage and Last Light explicitly retain emergency stabilization; none reverses Last Words. Field Surgery is reconciled to Soft Tissue/Bone RV treatment rather than automatic penalty removal.
- Corroded/Disrupted remain source-defined equipment faults; they do not replace HOL character conditions. Radiation exposure is labeled an unapproved GOL extension, with no invented generic cure.
- Ship Hull, shielding and module damage retain their separate, explicitly proposed ship-scale procedure. The personal wound tables apply to crew, not to ship structure.

The reader receives the complete foundation in Chapter 7, not a mandatory external HOL reference. Canonical inherited references live in `design/rules/`; treatment and universal abilities are included in the catalog and corrected sheets retain Grit, marks, scars, remedy, RV, progress and last-attempt date separately.
