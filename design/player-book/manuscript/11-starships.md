# Starships and FTL

> **Design review / playtest proposal.** This chapter collects the existing ship concept and proposes the missing procedures. These ship rules and all ship numbers are untested. They are presented for Bruce's review, not as an approved playtest release. The Legend character rules, attributes and DP economy are unchanged.

The ship is a shared character: a hull that takes punishment, shields that reduce damage, and systems whose condition changes under strain. A station is a job, not a class. Your abilities describe what you can do exceptionally well; the basic station actions below let any crew member participate.

## Two rolls, two different questions

The **action check** asks how well the crew member performs: roll 3d6 + one attribute, apply Boons and Banes, and read Weak / Standard / Strong. A system die is never added to that total. Discipline ranks grant access to abilities, not a bonus to this roll.

The **Consumable Die** asks whether the machinery holds up: roll the named system die after meaningful load. Only a 1 steps it down. The order is **resolve the action, then check the system**. If a d4 goes offline, the action just resolved still happened. A successful shot can burn out its weapon; a poor shot can leave the weapon working perfectly.

The ladder is **d12 > d10 > d8 > d6 > d4 > offline**. On any single load roll the chance of degradation is 1 in the die's size: d12 is about 8%, d8 about 13%, d4 is 25%. A large die means endurance, not more damage or a better action check.

## Reading the ship sheet

| Field | What you record |
|---|---|
| Hull | Maximum and current structure; damage remaining after shields reduces this. |
| Shield DR | The amount absorbed per incoming attack while defences are online. |
| Handling | A printed manoeuvring quality; see its use below. |
| Jump rating | Maximum route distance in abstract route units, not light-years. |
| Systems | Installed rating, current die, temporary changes and faults for each system. |
| Weapons | Mount, damage type, range and Weak / Standard / Strong damage. |
| Preparation | Fuel units, capacitor clock, navigation progress and arrival result. |

**Installed rating** is the normal serviced die size. **Current die** records wear and available power. A temporary boost can exceed the installed rating, up to d12; ordinary service cannot. Keep the underlying die and any temporary boost separately so ending a boost never erases actual wear. A missing system is absent, not offline, and cannot be restored by a repair.

## What each system does

| System | Use and consequence of going offline |
|---|---|
| Power capacitors | Charge and hold jump energy. Offline: no charging or jump. This is not the ship's reactor. |
| FTL drive | Executes a prepared jump. Offline: no jump. |
| Navigation suite | Supports route work and gives its stated Boon. Offline: no computer Boon; charts may still permit plotting. |
| Sensors | Active scans and targeting beyond Near. Offline: visual observation and Close / Near fire remain possible. |
| Sublight engines | Change range and evade. Offline: the ship coasts; powered manoeuvres are unavailable. |
| Weapons | Fire the listed mounts. Offline: those mounts cannot fire. |
| Defences | Maintain shield DR. Offline: printed shield DR becomes 0. |
| Life support | Maintains breathable, habitable compartments. Offline: start the emergency procedure below. |
| Communications | Transmit and receive beyond local contact. Offline: no normal radio; physical signals may still work. |

The reactor is assumed to function unless a scene explicitly threatens it. Capacitor wear does not shut down every other system. This distinction keeps jump preparation separate from the Engineer's choice of which system to sacrifice.

## Crew, turns and access

Use the existing turn structure: one Main Action, one Maneuver, movement and one Reaction per character. Alternate turns by side, choosing the order within a side as play proceeds. The ship has no extra turn or action pool. An enemy ship uses its listed crew stations; it does not receive every station action for free.

Choose a station at the start of your turn. Switching adjacent bridge consoles uses your Maneuver; reaching engineering or a damaged compartment uses normal movement and any intervening doors or hazards. Remote access must be established in the fiction. One console has one operator at a time; additional crew need another installed console or mount. Each weapon mount fires at most once per round unless an ability explicitly overrides that limit.

A solo pilot can fly or fire with their Main Action, not both. An unattended station continues its routine setting but makes no checks. Life support, passive communications and maintained shields do not need an operator each round.

## Basic station actions

All actions in this table are **proposed universal Main Actions**. No DP purchase is required. Have the listed system online, explain the task, and roll the listed attribute. An ability's specific action, range and outcomes replace this baseline when that ability is used.

| Station / action | Weak / Standard / Strong |
|---|---|
| Pilot: change range, Agility | Move one band with a declared complication / move one band / move one band and give the next allied station check a Boon. Roll engines after use. |
| Gunner: fire, Agility | Deal the mount's Weak / Standard / Strong damage. Roll weapons after use. |
| Engineer: reroute, Knowledge | See power transfer; roll no additional donor or receiver load die for the transfer itself. |
| Sensors: acquire, Reason | Locate the target, but give the next allied check against it a Bane / identify one active system / identify a system and give the next allied attack a Boon. Roll sensors. |
| Navigator: plot, Reason | Add 1 progress and a recorded arrival complication / add 2 / add 3. Roll navigation after each plotting interval. |
| Commander: coordinate, Guile | Give the chosen ally's next station check a Boon, but your next station check a Bane / give that ally a Boon / give two different allies a Boon each. No system load. |

A granted Boon applies to one check and expires at the end of the recipient's next turn. Only one instance of the same basic support action can benefit a check. A Strong result grants its printed benefit; it does not also grant a free system wound or an extra action.

For a Weak pilot result, declare a consequence before rolling: expose the ship (one Bane on its next defence), take a hazard hit, or lose a safe approach. Avoid complications that silently cancel the printed movement. Scanner information does not grant the stronger information on the Sensor Sweep card.

## Handling and defence

**Proposed use of Handling:** compare the printed values only when one ship contests another ship's powered manoeuvre. The more agile ship gains one Boon; the less agile ship gains one Bane. Equal values change nothing. Do not add Handling to an attribute or to a roll total. A fixed hazard uses the SA's declared Boons or Banes instead of this comparison.

When a player ship is attacked, one crew member at the Pilot station rolls **3d6 + Agility** for defence. This defence does not itself spend a Reaction or trigger an engine load roll. Apply the Handling comparison if the engines are online. Weak defence takes the enemy mount's Strong damage; Standard takes Standard; Strong takes Weak. The attack then uses shields and Hull normally. With no available pilot or offline engines, take Standard damage without a defence roll. Cover and an explicit ability may still apply.

When a player fires at an NPC ship, the player's attack check supplies the damage band. Apply the same Handling comparison if the target can manoeuvre; do not also roll an NPC defence. NPC against NPC can be resolved by the SA without additional player rolls.

**Evasive Manoeuvre** remains a Reaction: its check grants +1 DR against that attack on any result, and Strong also moves one band afterwards. It supplements the ordinary defence; it does not replace it or grant a second Reaction. Roll engines once for using this powered ability. A one-attack DR bonus can apply even when printed shield DR is 0, provided the engines needed to evade are working.

## Range and weapon scale

Space uses **Close, Near, Far and Extreme** as relative bands. These are not the personal-combat square distances with similar names. Close permits docking or boarding once the target is secured; Near is normal engagement; Far requires working sensors to target; Extreme is observation or pursuit beyond these sample weapons.

Set initial range before turns begin. A successful pilot action changes range one band toward or away from one chosen ship; the same pair shares that new range. Other ships keep their relationships unless the SA says the movement changes them. A chase ends when the fiction permits escape; reaching Extreme alone is not automatic invisibility.

| Proposed mount | Type | Range | Weak / Standard / Strong |
|---|---|---|---|
| Light pulse cannon | Thermal | Close to Far | 3 / 5 / 7 |
| Trader defence turret | Kinetic | Close to Near | 2 / 4 / 6 |

These are ship-scale values for these hulls only. Personal weapons do not reduce a starship's Hull in ordinary fire. Exposed crew and accessible components can be attacked at personal scale when the fiction permits; the SA states that target separately. Do not convert personal card ranges or damage to ship scale automatically. Called Shot remains a personal-scale card until a ship-scale version is designed.

## Shields, Hull and system wounds

Apply any printed damage-type resistance first, then subtract shield DR once from the attack's total. The remainder reduces Hull, to a minimum of **0** ship damage. Personal combat's minimum-1 rule does not override a fully absorbed ship hit. The sample ships have no damage-type resistance.

Each incoming attack is one defences load event, even if shields absorb all damage. Resolve its damage with the DR that was online at the start of the hit, then roll defences. A 1 on d4 removes shields for later attacks, not retroactively for this hit.

If Hull was reduced, roll the wound table once for that attack. Roll each named affected system's current Consumable Die; only a 1 steps it down. An absent or already offline system takes no further effect. A targeted ability that explicitly inflicts a system consequence replaces this random wound unless it says otherwise.

| d6 | System stressed after a Hull hit |
|---|---|
| 1-2 | Hull only: no additional system roll. |
| 3 | Sensors. |
| 4 | Sublight engines. |
| 5 | Weapons. |
| 6 | Capacitors or life support; the SA names the system that fits the hit. |

**Worked hit.** A Scout Cutter at Hull 20 and DR 2 takes a 5-damage shot. It falls to Hull 17. Its defences d6 rolls 4: no degradation. The wound roll is 4, so engines d8 rolls next. A 1 lowers engines to d6. The ship lost structure and engine endurance; its Handling and weapon damage did not change.

**Fully absorbed hit.** A 2-damage shot against DR 2 causes no Hull loss and no wound roll. Defences still rolls once. If its d4 rolls 1, that shot was absorbed, but the next shot meets DR 0.

## When to roll a system die

Roll once per system per meaningful use, after resolving that use: a firing salvo, powered manoeuvre, active scan, plotting interval, jump-charge interval or jump. A multi-system action names each system it strains. A wound is a separate load event and may roll a die already checked earlier that round.

Do not roll every round for passive life support, routine radio, quiet coasting or simply leaving a console switched on. Roll communications for a jammed or emergency long-range transmission; life support for a breach, overload or hazardous atmosphere. The SA names the load before the action. Do not turn the same action into several wear rolls for one system.

## Power transfer: a deliberate sacrifice

The basic Engineer action moves **one die step** from an online donor to an online receiver. Knowledge determines the result: Weak moves one step and the donor goes offline at scene end; Standard moves one step; Strong moves two steps between that same pair. Stop when the donor reaches offline or the receiver reaches d12. You can choose fewer steps.

Transfer changes the current dice and persists until reversed or serviced. It cannot restart an offline receiver, charge the jump clock, restore Hull or change weapon damage. Moving a donor from d4 to offline is allowed. Life support is an eligible donor, but the emergency below begins immediately if it goes offline. Do not roll an extra load check for the transfer itself.

**Worked transfer.** Weapons d4 receives a step from communications d8. Communications becomes d6; weapons becomes d6. With a Strong result the Engineer could instead move two steps: communications d4, weapons d8. The next shot still deals the mount's listed damage. It now has a better chance of leaving the weapon online.

**Spacer distinction.** Power Routing is an ability with its own outcomes and one-scene duration, not the basic action above. Its temporary allocations revert at scene end; on Weak its printed extra donor step-down then applies. Overcharge creates its stated temporary boost without a donor. Neither stacks with another copy of itself on the same system. Record temporary adjustments beside the underlying current die; actual wear lowers the underlying die, not the temporary bonus. If the underlying die goes offline, the boost ends and cannot keep it online. Removing a bonus never repairs wear. A temporary donor reduction cannot exceed the available steps; if it reaches offline, the donor is unavailable for the duration. These bookkeeping interpretations are proposals for review, not revisions to the cards' DP or prerequisites.

## Damage control and repairs

A basic Engineer **containment** action uses Knowledge and tools. Weak contains a named breach or fault for one round with a complication; Standard contains it for the scene; Strong contains it for the scene and gives the next repair of that fault a Boon. Containment does not restore Hull or a die. Restarting an offline system needs a repair ability or service; basic power transfer cannot do it.

Field Repair, Keep It Running, Jury-Rig and Miracle Worker keep their printed actions and outcomes. For ship systems, offline is one step below d4. Normal restoration cannot exceed installed rating; Miracle Worker's explicit minimum d6 / d8 can exceed it. Hull is structure, not a repairable component's HP: Field Repair's HP option does not rebuild Hull during combat. Use a shipyard for structural Hull restoration.

**Proposed repair budget:** before departure, stock spare-parts lots. Each application of a ship repair ability consumes one lot, whether temporary or permanent; a multi-system repair consumes one per affected system. Containment costs no lot. A toolkit enables work but does not supply unlimited replacement hardware. A fragile Field Repair fails on the next 1 rolled by that repaired system: remove that repair's gain as well as the normal wear, stopping at offline. Remove its fragile marker after that failure or full service.

**Service proposal:** one uninterrupted hour and one parts lot restore one current system step, without a check in a safe workshop. Stop at installed rating. Remove temporary repair and transfer markers when full service restores a system to installed rating. A yard repairs 4 Hull per eight-hour work shift using one structural materials lot, up to maximum. Parts, materials, fuel and labour prices remain open economic decisions; record quantities separately from coins rather than inventing a conversion.

## Disabled ships and life-support emergencies

At **0 Hull**, the ship is disabled: weapons, engines and FTL cannot operate, even if their dice remain online. It does not explode automatically. The SA establishes a visible emergency clock of **3 rounds** in combat or **3 ten-minute intervals** outside it, and states the consequence: breakup, fire or loss of a compartment. Containment stops that clock for its stated duration; towing, evacuation or yard support may resolve the danger. In combat it cannot regain operational Hull through a routine component repair.

When life support goes offline, mark **3 ten-minute air intervals** for sealed occupied compartments. This is an abstract reserve, not a vacuum-survival rule. A breached compartment requires immediate suits or evacuation; use the personal hazard rules for exposure. Restoring life support stops the air countdown. Containment can seal a leak but does not create new air. Record oxygen reserves and suits before sacrificing life support for power.

## FTL: prepare, commit, arrive

A jump requires **two completed tracks**, an online capacitor system and FTL drive, and a destination within the drive's rated range. Navigation work and capacitor charging can happen at the same time. Transit itself is instantaneous. Range is a network abstraction: the SA assigns route distance and hazards before the crew spends resources.

| Route distance | Capacitor segments | Navigation progress |
|---|---|---|
| 1 route unit | 3 | 3 |
| 2 route units | 6 | 6 |
| 3 route units | 9 | 9 |

Do not attempt a route beyond the ship's Jump rating in this review draft. Pushing drive range needs a separately reviewed rule. A shuttle without FTL cannot jump, regardless of navigation progress or external power.

### Track A: charging

**Proposed baseline:** one fuel unit and ten minutes fill one capacitor segment. Tick a segment, spend the fuel, then roll capacitors once. A staffed port charger takes one minute per segment at a locally quoted fee; it supplies the energy and feedstock instead of consuming onboard fuel, but still checks the ship's capacitors per segment. Ordinary charging needs no action check. Filling a clock does not restore the capacitor die.

A d4 that goes offline leaves the newly completed segment on the sheet but blocks further charging and the jump. Repair it to resume. Store charge until the next jump; going offline makes charge inaccessible rather than erasing it. The clock is set for the planned route; longer rerouting needs extra segments, while shorter routing retains excess charge but still empties the bank on jump. After any successful jump, reset charge to zero.

**Emergency charging proposal:** an Engineer's Main Action and Knowledge check forces one segment in a combat round, consuming two fuel units. Weak fills it but steps capacitors down once automatically; Standard fills it and checks the capacitor die; Strong fills it without wear. Do not also make the normal charge load roll. This makes a hurried escape costly without requiring dozens of combat rounds.

### Track B: navigation

One normal plotting interval is ten minutes. Use Reason and add 1 / 2 / 3 progress on Weak / Standard / Strong. An online nav computer gives one Boon; charts alone permit a check without it. Roll navigation once after an interval using the suite. Routine route progress cannot be farmed during combat: Emergency Jump is the ability that permits Main Action hurried plotting.

Record Weak complications as they occur; completing a route later does not erase them. The check that reaches the progress target determines arrival quality. Keep its band on the sheet. A Plot Course Strong also gives its printed next-jump Boon; if there is no further check before transit, carry it to the first navigation or piloting check on arrival. Master Navigator can spend a Main Action once both tracks are ready to replace the arrival band, checking navigation for that use. It does not fill either track.

### Commit to the jump

The Pilot spends a Main Action to commit once the two tracks are complete and the required systems are online. No extra basic navigation roll is required. Resolve arrival from the recorded band: Weak arrives off target with a complication; Standard arrives at the intended system and approach; Strong arrives in a favourable position agreed with the SA. Then roll FTL drive once. If the drive goes offline, the ship has arrived but cannot jump again until repaired.

Emergency Jump's Strong permits immediate commitment as part of that ability's action **when the capacitor clock is full**, its progress target is met and the drive is online. It bypasses the extra commitment action, not fuel or charging. Retained triple natural 1s on the completing navigation check add a complication as in the Legend core; the SA may damage the drive after transit or establish a hazardous arrival, but does not silently delete completed tracks.

### Worked preparation

A Scout Cutter with Jump 3 chooses a two-unit route: both targets are 6. It carries eight fuel units. Charging takes six ten-minute intervals, consumes six units and checks capacitors six times if they stay online. A d8 roll of 1 reduces capacitors to d6; the next interval uses d6. Die size never changes the six-segment target.

Meanwhile the Navigator, Reason +2, uses the online suite's Boon. Retained dice total 10: 12 is Standard, for 2 progress. The next interval is Strong for 3, reaching 5. The third is Standard for 2, reaching 7; cap recorded progress at 6 and record Standard arrival. Navigation is ready after thirty minutes, but the crew waits for the sixty-minute charge. The Pilot commits, arrives as intended, clears both tracks and checks the FTL drive. Fuel remaining: two units.

## Proposed ship profiles

These profiles retain the existing seed Hull, DR, Handling, Jump ratings and system dice. The weapon mounts are new review proposals. Record each listed die as both installed and current before damage or transfers.

### Scout Cutter

**Hull 20 / Shield DR 2 / Handling +1 / Jump 3.** One light pulse cannon, Thermal, Close-Far, damage 3 / 5 / 7. Capacitors d8; FTL d8; navigation d10; sensors d10; engines d8; weapons d6; defences d6; life support d8; communications d8.

A capable survey and courier ship. Its navigation and sensors endure better than its weapon and shield systems. A crew can plot a longer route, but still needs nine fuel units for a full three-unit charge. Fuel and parts are purchased quantities; neither profile grants a free starting stock.

### Free Trader

**Hull 32 / Shield DR 3 / Handling 0 / Jump 2.** One defence turret, Kinetic, Close-Near, damage 2 / 4 / 6. Capacitors d10; FTL d8; navigation d8; sensors d6; engines d8; weapons d4; defences d8; life support d10; communications d8.

Tougher structure and dependable shields support a working crew. The d4 turret is a warning: each firing risks putting that weapon offline. It benefits from power transfer, at the cost of another system's endurance.

### System Shuttle

**Hull 12 / Shield DR 1 / Handling +2 / no Jump.** No weapon mount. Capacitors d6; no FTL; navigation d6; sensors d6; engines d10; no weapons; defences d4; life support d6; communications d6.

A local transport whose high Handling and engines help it manoeuvre. Its shields are fragile, and it cannot manufacture an interstellar escape by rolling well. It needs a carrier or a larger vessel to leave the system.

## Reading a round across the crew

The Cutter is at Near range from a Handling-0 attacker. Its Pilot uses a Main Action to move to Far. Handling +1 gives a Boon; a Standard check moves it one band, then engines d8 rolls 5 and holds. The opposing Gunner attacks. The Cutter's Pilot defends with the Handling Boon; Standard defence takes the enemy turret's 4 damage. DR 2 leaves 2 Hull loss. Defences d6 holds; the wound is 1, Hull only.

The Cutter's Engineer then transfers one step from communications d8 to weapons d6 on Standard: communications d6, weapons d8. Another enemy station takes its turn. Finally the Cutter's Gunner fires its pulse cannon at Far using online sensors. Its Handling advantage gives a Boon; Strong deals 7 before enemy DR. Weapons d8 rolls 1 and falls to d6. The crew gained position, absorbed damage, sacrificed communications endurance and fired, using their own turns throughout.

## Decisions this draft asks you to review

Does Handling as a Boon / Bane comparison feel right? Should shield endurance and DR remain separate? Does power transfer make a meaningful sacrifice when it improves endurance rather than damage? Is a parts budget the right repair limit? Do the ten-minute preparation intervals and costly emergency charging create the tension you want?

The sheet at the back makes these decisions visible. Fuel prices, weapon variety, ship acquisition, cargo capacity, boarding procedures, precise repair economies and long-term ship advancement remain to be designed. None of those gaps is evidence that the ship system is ready for a mission or table playtest.
