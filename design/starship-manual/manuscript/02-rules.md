# Starships: build and operate

Choose what the ship needs to do before you buy its systems. A crew carrying urgent freight may want room in the hold and a drive that can make the route. A survey crew may spend those same points on detection and navigation. Start with the job, then see which frame can support it.

## 1. Choose a frame

A ship's **frame class** is its physical scale, not a character class or a station job. Frame size fixes Hull, Handling, available module positions and its total Ship Points (SP). These are construction limits, not money and not a pool spent every turn. Hull and Handling are not bought again as systems.

| Frame | Total SP | Modules max | Die ceiling | Hull | Handling | Scale |
|---|---:|---:|---|---:|---:|---:|
| Launch / shuttle | 12 | 8 | d8 | 12 | +2 | 1 |
| Light ship / cutter | 24 | 12 | d10 | 24 | +1 | 2 |
| Medium ship / frigate | 36 | 16 | d12 | 40 | +0 | 4 |
| Heavy ship / cruiser | 50 | 22 | d12 | 64 | -1 | 8 |
| Capital ship | 70 | 30 | d12 | 100 | -2 | 16 |

**Scale** multiplies only life-support capacity and cargo capacity. It is not a combat bonus. A capital ship does not multiply its weapon damage by sixteen. Heavy weapons, very large targets and mixed-scale combat require a later design pass; the current mount table is a review baseline.

## 2. Spend your Ship Points (SP)

| Installed die | SP cost | Equipment quality | Load degradation |
|---|---:|---|---|
| d4 | 1 | one Bane | On a 1, step down |
| d6 | 2 | no modifier | On a 1, step down |
| d8 | 3 | 1 Boon | On a 1, step down |
| d10 | 4 | 2 Boons | On a 1, step down |
| d12 | 5 | 3 Boons | On a 1, step down |

**Ship size gives you SP. Each die you assign to a system spends SP.** Start with the frame's Total SP, subtract each installed die's SP cost, and record what remains. You may finish with unspent SP, but you cannot spend more than the ship has.

For example, a Light ship starts with **24 SP**. Installing a d6 engine spends **2 SP**, leaving **22 SP**. Installing d4 navigation spends **1 SP**, leaving **21 SP**. Do the same for every required and optional system. A die is bought separately for each module; buying one d6 does not supply d6 to every system.

Use the price ladder above for each system. The higher-die prices and frame budgets are provisional.

Costs are total installed costs: d8 costs 3 SP, not 1 + 2 + 3. Upgrading an installed d6 to d8 during construction spends only **1 additional SP**, the difference between 2 and 3. Each module also occupies one module position. SP, module positions and the die ceiling are separate limits; spare SP does not bypass either of the other limits.

### Worked SP spending ledger: Scout Cutter

Start with a Light frame and **24 SP available**. This is the same checked Scout Cutter shown in Chapter 5.

| Install | Die | SP spent on this module | SP remaining |
|---|---|---:|---:|
| Sublight engines | d8 | 3 | 21 |
| Navigation suite | d8 | 3 | 18 |
| Sensors | d8 | 3 | 15 |
| Life support | d6 | 2 | 13 |
| Communications | d4 | 1 | 12 |
| FTL drive | d8 | 3 | 9 |
| Jump capacitors | d8 | 3 | 6 |
| Weapon mount | d6 | 2 | 4 |
| Shield generator | d6 | 2 | 2 |
| Cargo bay | d6 | 2 | 0 |

**Total spent: 24 SP. Remaining: 0 SP.** The first five required systems cost 12 SP, leaving 12 SP for the selected optional systems. Removing the d6 cargo bay during design frees its 2 SP and its module position; losing it to damage during play does not refund SP. Full construction is paid once, not again on every use.

Unspent SP is unused construction capacity. SP is not coins, fuel, capacitor charge or an in-combat power pool. Wear changes the current die, not installed SP cost; an offline system still occupies its place and SP in the build.

**Equipment quality** applies when that system is the primary equipment for a meaningful check. Add its Boons or Bane to the usual Legend pool, cancel modifiers and retain the core limit of three net extra dice. Never add a system die or its size to an attribute total. Use one primary equipment grade per check; do not add grades from several consoles. Abilities and distinct situational modifiers can still contribute within the core limit.

## 3. Install the required systems

Every independent crewed ship needs exactly one of each: **sublight engines, navigation, sensors, life support and communications**. Each starts at least d4 and costs SP. These are not free fittings. They may go offline during play, but an offline required module remains installed and does not refund points.

| Required system | Capability at higher ratings |
|---|---|
| Sublight engines | Better quality on powered manoeuvres; frame Handling remains the ship's size characteristic. |
| Navigation | Better route-plotting equipment quality and endurance. There is no additional automatic computer Boon. |
| Sensors | Better check quality and longer detection reach; reach does not itself identify everything present. |
| Life support | Supports more occupants; installed capacity is multiplied by frame Scale. |
| Communications | Better check quality when punching through noise, concealment or interference; ordinary in-system radio needs no check. |

**Example: d4 versus d6 sensors.** d4 reaches Near and gives one Bane to an active scan. d6 reaches Far and gives no equipment penalty. d6 also has a lower chance of wear per load roll. The upgrade changes what the crew can attempt and how well it can do it, not merely how long the unit lasts.

## 4. Choose optional modules

| Optional system | What the SP buys |
|---|---|
| Cargo bay | Sealed freight handling and cargo units; multiple bays are allowed. |
| Med bay | Treatment beds and appropriate facility support; does not grant medical abilities or automatic healing. |
| Weapon mount | One independently operated ship weapon, with its own die, range and damage. Multiple mounts are allowed. |
| Targeting array | May replace the weapon's equipment quality on a firing check if better. Does not add another grade or an extra attack. |
| FTL drive | Rated jump distance; requires a separately allocated capacitor bank. |
| Jump capacitors | Stores jump charge and sets charging speed; must be paired with an FTL drive in this draft. |
| Shield generator | Supplies shield DR. An unshielded hull has DR 0. |
| Workshop | Equipped project positions; does not supply endless parts or grant engineering cards. |
| Hangar | Launch berths; medium frame or larger, minimum d6. Each docked launch has its own separate SP pool. |

Only cargo bays, med bays, weapon mounts, workshops and hangars can be repeated. Each repeat costs its full SP cost and a module position and is tracked separately. Do not split a required system into several cheap copies. Every weapon mount gets an identifier; roll and repair that mount, not an imaginary shared weapons pool.

The frame includes ordinary crew access, fittings and personal storage, not a commercial cargo bay, clinic, weapon or FTL drive. A targeting array requires at least one weapon mount. A hangar does not grant ships, pilots or extra turns. Dedicated armour plating, stealth systems, reactors and exotic modules are future coverage, not free narrative upgrades.

## 5. Read installed capacities

| Module / capacity | d4 | d6 | d8 | d10 | d12 |
|---|---|---|---|---|---|
| Sensor reach | Near | Far | Extreme | local orbital region | local system survey |
| Cargo units, before Scale | 2 | 4 | 8 | 16 | 32 |
| Occupants, before Scale | 2 | 4 | 8 | 16 | 32 |
| Med-bay beds | 1 | 2 | 3 | 4 | 6 |
| Workshop projects | 1 | 2 | 3 | 4 | 6 |
| Launch berths | 0 | 1 | 2 | 3 | 4 |
| FTL route units | 1 | 2 | 3 | 4 | 5 |
| Capacitor segments | 3 | 6 | 9 | 12 | 15 |
| Minutes per charge segment | 10 | 8 | 6 | 4 | 2 |
| Shield DR | 1 | 2 | 3 | 4 | 5 |

Cargo units are standard pallet spaces, not an exchange rate for personal Bulk or tonnes. Define unusually bulky freight before accepting it. Multiply each bay's units and life-support occupants by frame Scale; do not multiply beds, workshop positions, hangars, jump range or shields. Med bays hold the stated number of concurrent patients; each treatment still uses the healer's action, ability, supplies and check. Workshop positions measure simultaneous projects, not an automatic progress grant.

Larger sensors permit progressively wider searches. Orbital-region and system surveys take ten-minute intervals, require an SA-set progress target, and give broad contacts or leads, not instant real-time firing solutions. A Near-only array can still make a visual Close observation. Weapon targeting beyond Near needs live sensor coverage or a current contact supplied by an ally; information does not expand weapon range.

## 6. Installed rating, current die and load

A cutter leaves the yard with d8 sensors. After a hard scan, their current die can fall to d6. The ship still carries a d8 array, but the operator has to work with the reduced reach and quality until someone repairs it. Keep both numbers on the sheet so you can see what the system can do now and what it can recover.

**Installed rating** is the hardware bought at construction. **Current die** is its operating condition. A serviced system starts at its installed die. Wear steps its current die down: d12 > d10 > d8 > d6 > d4 > offline. Its **effective die** is the lower of installed rating and current die, after any permitted temporary modifiers. Current may be boosted above installed rating for endurance, but this never creates a physically larger bay or a better installed array.

Use the effective die for operating quality, active sensor reach, shield DR, weapon damage, FTL range and capacitor storage/rate. Thus worn d8 sensors operating at d6 have Far reach and normal quality; their larger installed hardware remains d8 and can be restored. Cargo space, berths and the installed number of life-support occupants do not shrink when a die wears. An offline bay becomes inaccessible or unsafe to handle, not a hole that deletes cargo; an offline life-support system starts the reserve clock.

Resolve the crew's **3d6 + attribute action first**, then roll the current system die once for meaningful load. Only a 1 steps it down. A d4 action still resolves before the system goes offline. Roll a weapon mount after a salvo; engines after a powered manoeuvre; sensors after an active scan; navigation after a plotting interval; capacitors after a charging interval; FTL after arrival. Med bays and workshops roll when used for a pressured treatment or project interval; cargo handling, targeting and communications roll when strained. The SA names each strained system before the action.

A firing check that actively uses a targeting array checks both the mount and that array after the shot. Do not also check passive sensors for merely holding a live contact. Routine storage, ordinary radio and passive life support do not check every round. A Hull wound is a separate stress event and can roll a module already checked this round.

## 7. Crew stations and actions

Tell the crew which stations are staffed as the scene begins. An explorer can take a station they can reach and operate. Each character keeps one Main Action, one Maneuver, movement and one Reaction. Alternate turns by side as in Legend. The ship grants no separate free turn. Choose a station at turn start; switching adjacent consoles uses your Maneuver, while reaching another compartment uses normal movement. One console has one operator at a time.

A pilot may fly or fire with their Main Action, not both. Each mount fires at most once per round unless an explicit ability overrides that limit. More mounts create choices; they do not invent crew. An unattended system holds its routine setting and makes no action checks. The SA states enemy crew and mount limits before a ship scene.

| Universal station action | Weak / Standard / Strong |
|---|---|
| Pilot: change range, Agility | Move one band with a declared complication / move one band / move one band and give the next allied station check a Boon. Use engines quality; roll engines. |
| Gunner: fire, Agility | Use mount damage by band. Use mount quality, or targeting quality if better. Check every actively used firing system once. |
| Engineer: transfer, Knowledge | One step and donor offline at scene end / one step / up to two steps between the same pair. See transfer limits. |
| Sensors: acquire, Reason | Locate contact with a declared complication / identify an active system / identify one and give the next allied attack a Boon. Use sensors quality; roll sensors. |
| Navigator: plot, Reason | 1 progress and recorded complication / 2 / 3. Use navigation quality; roll navigation after an interval. |
| Commander: coordinate, Guile | One ally's next station check gains a Boon, your next check a Bane / one ally gains a Boon / two different allies gain a Boon each. |

Unless stated otherwise, station Boons expire at the end of the recipient's next turn; a Weak command Bane expires after use or at scene end. No repeated copy of the same support action stacks on one check. Cards replace the baseline where their specific text applies. A Strong result grants its printed benefit, not an additional unlisted system wound.

## 8. Handling, weapons and damage

When an opposing ship comes into range, establish what each crew wants. A trader trying to leave the area may spend its pilot's turn opening the range. A cutter covering an evacuation may have to stay where it is even after taking a hit. Keep the current range and each side's available stations visible as you resolve turns.

Compare frame **Handling** when one powered ship contests another: higher Handling grants one Boon, lower gives one Bane, equal gives neither. Combine it with one primary system's equipment quality within the core cap. Fixed hazards use declared situational modifiers instead. Offline engines remove the Handling comparison and prevent powered manoeuvres.

When the player fires, their attack band sets damage; do not also roll an NPC defence. For a contested attack, compare equipment on both sides: use the firing mount's grade (or its targeting grade if better), and invert the defending engine grade as an opposing modifier if an available pilot can manoeuvre. A d8 enemy engine therefore gives your attack one Bane; a d4 enemy engine gives it one Boon. Use only one primary grade per side, not several of that side's consoles. When the player's ship is attacked, its pilot rolls Agility, using engines quality and the Handling comparison. Invert the enemy firing grade on this defence roll as well: enemy d8 weapons impose one Bane; d4 weapons grant one Boon. Weak defence takes the attacker's Strong damage; Standard takes Standard; Strong takes Weak. Defence itself spends no Reaction and causes no extra engine wear. No available pilot or offline engines means Standard incoming damage without that roll.

**Evasive Manoeuvre** still spends a Reaction for its printed +1 DR and Strong movement. It does not replace the normal defence. Check engines once after using that powered ability. Its one-attack DR can operate without a shield generator if engines work.

All standard mounts in this builder use Close-Near range and one chosen damage type, Kinetic or Thermal. A mount's damage follows its effective die. Far-range mounts and specialised damage types need separately costed designs; a larger sensor or targeting array alone does not extend a weapon.

| Effective weapon die | Weak | Standard | Strong |
|---|---:|---:|---:|
| d4 | 2 | 3 | 4 |
| d6 | 3 | 5 | 7 |
| d8 | 4 | 6 | 8 |
| d10 | 5 | 7 | 9 |
| d12 | 6 | 8 | 10 |

These are ship-scale values. Personal cards keep their printed personal targets and ranges; Called Shot does not automatically become a ship-scale precision cannon. Ships use relative Close, Near, Far and Extreme bands, not personal square ranges. A pilot action changes one band relative to one chosen ship. Docking or boarding also requires the target to be secured; reaching Extreme does not automatically end pursuit.

Apply resistance if printed, then current shield DR, then remaining damage to Hull. Ship damage can be **0**; the personal minimum-1 rule does not override a fully absorbed ship hit. Check the shield generator after each incoming attack while online, even if it absorbed all damage. Use its effective DR before the hit; degradation affects later hits.

If the attack reduces Hull, roll one wound d6: 1-2 Hull only; 3 sensors; 4 engines; 5 one weapon mount chosen to fit the hit; 6 capacitors or life support, named by the SA. Roll that module's current die: only 1 degrades it. An absent or offline module has no further effect. An explicit targeted-system consequence replaces the random wound unless its ability says otherwise.

**Worked shot.** The cutter's d6 pulse mount fires at Near. Its mount adds no quality modifier. The cutter and trader both have Handling +1, so no Handling modifier applies. A Strong check deals 7 Thermal. The trader's effective d8 shields have DR 3, leaving 4 Hull loss: 24 to 20. Shields roll 1 and fall to d6, so subsequent attacks meet DR 2. The wound is 5; the trader's d4 turret rolls 3 and holds. The cutter then checks its own mount for firing load.

## 9. Transfer, repair and emergencies

Basic power transfer moves one current die step from an online donor to an online receiver; a Strong Knowledge check may move two between that pair. Stop at donor offline or receiver d12. Weak also puts the donor offline at scene end. The receiver cannot be restarted by transfer. The transfer itself needs no extra load roll. Record actual die changes; construction SP, installed size and module positions never change in combat.

A receiver improves performance only up to installed rating. Transferring to an installed d4 gun cannot turn it into a d6 gun. It can add endurance above installed rating. To gain permanently better damage, replace or upgrade its hardware using available frame SP and suitable yard work. A service visit cannot recover a transferred point and leave a recipient permanently above installed rating: full service resets each system to its purchased hardware rating.

Power Routing and Overcharge keep their printed temporary outcomes. Record underlying wear separately; removing the temporary modifier never heals wear. If the underlying die goes offline the boost ends. An effective capacitor capacity loss vents charge above the new limit with no fuel refund, including loss caused by a deliberate transfer. Sacrificing life support starts its reserve countdown. Engineering choices should have visible consequences.

Basic containment is a Main Action, Knowledge and tools: Weak stops a named breach or fire for one round with a complication; Standard contains it for the scene; Strong also gives its next repair a Boon. It restores no Hull or die. Repair abilities use their cards; offline is one step below d4. Ship-system repairs consume one spare-parts lot per affected module per application. Medical treatment of people does not consume ship repair lots. Normal restoration stops at installed rating; Miracle Worker's explicit minima can raise current endurance but not installed capability.

Field Repair's component-HP option does not rebuild Hull. A fragile ship repair fails on that system's next load roll of 1: remove its restored steps and apply ordinary wear, stopping at offline. Temporary repairs cannot be repeatedly stacked on the same module. Safe service takes one hour and one parts lot per restored die step; a yard rebuilds 4 Hull per eight-hour shift and one structural materials lot. Prices and construction labour times remain open economic decisions.

At **0 Hull**, engines, weapons and FTL are disabled regardless of their recorded dice. Declare a three-round emergency clock in combat or three ten-minute intervals outside it, and name breakup, fire or compartment loss. Containment pauses the clock for its duration; towing and evacuation may resolve it. There is no automatic explosion. Hull repair in a yard is needed to operate again.

Offline life support gives sealed occupied compartments three ten-minute reserve intervals at or below installed occupant capacity. Above capacity, declare the shortage before departure; no automatic reserve is guaranteed. A breached compartment needs suits or immediate evacuation under personal exposure rules. Restoring life support stops the clock; sealing a leak does not create air.

## 10. Prepare an FTL jump

Plan a jump before the crew needs it. The navigator checks the route and plots the approach while the engineer brings the bank up to charge. Either job can finish first. Tell the pilot when both tracks are ready and check the system dice again before committing.

Install both an FTL drive and jump capacitors. Required navigation is already on the ship. A route must fit the effective drive range and capacitor capacity. Both **charge** and **navigation progress** must equal **3 times route distance**: route units 1/2/3/4/5 need 3/6/9/12/15 each. An offline capacitor bank or drive blocks jumping.

Normal charging spends one fuel unit per segment and takes the effective capacitor die's minutes per segment. Tick the segment, spend fuel, then check capacitors once. Wear can reduce storage or slow later intervals; vent excess safely to the new capacity with no refund. An ordinary port charger takes one minute per segment for a locally quoted fee, supplies the fuel, and still checks your bank after every segment.

Emergency charging spends an Engineer's Main Action, Knowledge and two fuel units for one segment in a combat round: Weak fills it then automatically steps capacitors down; Standard fills it and rolls capacitors; Strong fills it with no wear. Do not also make a normal charge load roll. Apply any capacity loss after that result. No roll adds more than one segment.

Navigation normally takes ten minutes per Reason check, adding 1/2/3 progress; use the effective navigation equipment grade, not an extra automatic computer Boon. Charts alone allow plotting without that equipment grade, provided suitable information exists. Check the suite after an interval in which it is used. Record Weak complications; the check completing the target records the arrival band. Emergency Jump permits its printed hurried plotting as a Main Action.

The Pilot commits with a Main Action once both tracks are complete and systems remain eligible. Arrive instantly: Weak off target with a complication; Standard intended approach; Strong a favourable agreed position. Clear both tracks and check the FTL drive after arrival. A drive that fails has still completed that transit. Emergency Jump Strong can include commitment if both targets and system requirements are met; it does not waive fuel or charge. Master Navigator can replace the recorded arrival band with its check once preparation is complete, but fills neither track.

Plot Course's Strong Boon applies to the next relevant navigation check on the route; if there is none before transit, carry it to the first navigation or piloting check on arrival. Retained triple natural 1s add the core complication, not automatic deletion of all progress. Changing destination invalidates the old plot. Retained charge can be used for a shorter eligible route; a longer route needs more charge, storage and a fresh plot.

**Worked jump.** The scout cutter's d8 drive permits three route units. Its d8 bank stores nine segments and charges one every six minutes. A two-unit route needs six fuel, six segments and six navigation progress. With no degradation, charging takes 36 minutes. The d8 suite grants one Boon on each plot check; Standard, Strong, Standard reaches 2, 5, then 6 progress in thirty minutes. The crew waits six more minutes for charge, commits and arrives using the final Standard band. Every charge interval checked the bank; a 1 would have changed later rate and capacity.

## 11. Three budgeted builds

Each module below is bought from the same table. These replace the old unbudgeted scout, trader and shuttle seed profiles. Starting fuel, spare parts, cargo and hired crew are separate purchases and remain unpriced.

### Scout Cutter

**Light ship / cutter / 24 of 24 SP spent / 10 of 12 modules / Hull 24 / Handling +1.**

| Module | Installed die | SP cost |
|---|---|---:|
| Sublight engines (engines) | d8 | 3 |
| Navigation suite (nav) | d8 | 3 |
| Sensors (sensors) | d8 | 3 |
| Life support (air) | d6 | 2 |
| Communications (comms) | d4 | 1 |
| FTL drive (jump) | d8 | 3 |
| Jump capacitors (bank) | d8 | 3 |
| Weapon mount (pulse) | d6 | 2 |
| Shield generator (shield) | d6 | 2 |
| Cargo bay (hold) | d6 | 2 |

### Free Trader

**Light ship / cutter / 24 of 24 SP spent / 12 of 12 modules / Hull 24 / Handling +1.**

| Module | Installed die | SP cost |
|---|---|---:|
| Sublight engines (engines) | d6 | 2 |
| Navigation suite (nav) | d6 | 2 |
| Sensors (sensors) | d4 | 1 |
| Life support (air) | d6 | 2 |
| Communications (comms) | d4 | 1 |
| Cargo bay (hold) | d10 | 4 |
| FTL drive (jump) | d6 | 2 |
| Jump capacitors (bank) | d6 | 2 |
| Weapon mount (turret) | d4 | 1 |
| Shield generator (shield) | d8 | 3 |
| Med bay (clinic) | d6 | 2 |
| Workshop (shop) | d6 | 2 |

### System Shuttle

**Launch / shuttle / 12 of 12 SP spent / 8 of 8 modules / Hull 12 / Handling +2.**

| Module | Installed die | SP cost |
|---|---|---:|
| Sublight engines (engines) | d8 | 3 |
| Navigation suite (nav) | d4 | 1 |
| Sensors (sensors) | d4 | 1 |
| Life support (air) | d6 | 2 |
| Communications (comms) | d4 | 1 |
| Cargo bay (hold) | d6 | 2 |
| Shield generator (shield) | d4 | 1 |
| Med bay (clinic) | d4 | 1 |


The **scout** spends heavily on survey and jump capability; its d6 cargo bay holds 4 × Scale 2 = 8 cargo units and life support supports 4 × 2 = 8 people. Its d6 shield starts at DR 2. The **trader** uses the same light frame and budget but buys a d10 hold: 16 × 2 = 32 cargo units. Better shields, a clinic and a workshop come at the cost of weaker sensing and weapons. Its d6 drive and bank support a two-unit jump. The **shuttle** spends its full launch budget on eight modules, no FTL and no weapon; d6 life support supports four occupants and d6 cargo holds four units. A good Piloting roll cannot invent a missing drive.

## 12. Build worksheet and review questions

Use the two-page ship record at the back. Record frame, Total SP and ceiling; fill every required row; list each optional module separately; add the SP costs and subtract from Total SP; check module count; then copy installed dice to current dice. Derive cargo and occupant capacity, shield DR, weapon damage and jump limits. Record actual crew and supplies before departure.

The source includes a working allocation checker: `python3 design/ship_builder.py` checks the three examples; passing it a JSON ship validates your own allocation. It rejects missing required systems, repeated unique systems, SP overspending, excess modules, die ceilings and invalid FTL or targeting combinations. The printed worksheet permits the same checks by hand.

Questions for Bruce: do the five sizes and SP totals leave meaningful sacrifices? Are quality Boons too strong when combined with Handling? Should current condition reduce active capability at every die step? Are cargo and medical facilities distinct enough to justify their allocation? Pricing, hull construction time, oversized weapons, ship advancement and mixed-scale combat remain future work. No new mission or table playtest is assumed.
