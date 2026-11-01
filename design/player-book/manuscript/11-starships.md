# Starships and FTL

The ship is a shared character. It has a hull, shields, systems and a history of repairs. The crew operates it through stations. A station is a job in the current scene, not a class: anyone qualified can take the Pilot's seat, and a class ability makes a character especially good at it without making the station exclusive.

## The ship sheet

| Value | Meaning |
|---|---|
| **Hull** | The ship's HP. At 0 Hull, the ship is disabled and in danger of breaking up. |
| **DR** | Shields. Reduces incoming damage. |
| **Handling** | The ship's Agility for manoeuvres and defence. |
| **Jump range** | The maximum route length the drive can safely take. |
| **Systems** | Each system has a Consumable Die: d12, d10, d8, d6, d4 or offline. |

A ship's systems are **power capacitors, FTL drive, navigation suite, sensors, sublight engines, weapons, defences, life support and communications**. Not every ship has every system; a shuttle may have no FTL drive, and a mining rig may have no weapons.

## Using a system

When a character uses a system under meaningful load, make the normal **3d6 + attribute** check and then roll that system's Consumable Die. On a **1**, step the die down one size. A d4 that steps down goes **offline** until repaired, recharged or serviced.

A combat salvo, a jump, a deep sensor sweep or an emergency power surge counts as meaningful load. Passive life support does not roll every round; roll when it is strained or failing.

## Stations

| Station | Example actions |
|---|---|
| **Pilot** | Change range, evade, pursue, line up a shot, control atmospheric flight |
| **Gunner** | Attack hull, or target a system with an appropriate ability or Strong outcome |
| **Engineer** | Reroute power, stabilise a failing system, contain a breach, repair |
| **Sensor Operator** | Scan, lock a target, identify a weakness, interfere with targeting |
| **Navigator** | Plot a route, calculate an emergency jump, track hazards |
| **Commander** | Coordinate crew actions, create an opening, keep morale |

Each crew member uses their own turn and abilities. A Strong result can add an advantage: better position, a stepped-down enemy system die, or a useful opening. A Weak result can still make progress but brings a complication.

## Ship combat

Ship combat uses the same Legend roll and the same three bands. It uses abstract **range bands** instead of a separate tactical map.

| Band | Meaning |
|---|---|
| **Close** | Boarding, docking, knife-range |
| **Near** | Standard engagement range |
| **Far** | Long-range fire; sensors matter |
| **Extreme** | Beyond most weapons; a chase or a scan |

Apply shield DR to incoming damage, then subtract any remaining damage from **Hull**. A called shot, a critical or a specific ability may damage a **system** instead. Hull loss and system loss are separate consequences: Hull is repaired in a yard; a system can be jury-rigged in the field.

## Hull hits and system wounds

When an attack reduces Hull, roll **1d6** on the wound chart after damage is applied. Roll each affected system’s Consumable Die: only a 1 steps it down. Damage fully absorbed by DR causes no wound roll. These wound results and ship values are **playtest** rules.

| d6 | Result |
|---:|---|
| 1–2 | **Hull only** — no system effect. |
| 3 | **Sensors** — roll the sensor Consumable Die. |
| 4 | **Engines** — roll the sublight engine Consumable Die. |
| 5 | **Weapons** — roll the weapon Consumable Die. |
| 6 | **Power or life support** — roll the capacitor or life-support Consumable Die; the SA chooses the system that fits the hit. |

A system that goes offline cannot be used until repaired. Repairing a system in combat is an Engineer action; repairing it fully requires a yard or a long stop.

## Power transfer

Power is a set of die sizes, not a separate pool. An Engineer can shift **one step** of power from one system to another as a Main Action and a Knowledge check. The donor system steps down one size; the receiving system steps up one size. A system cannot be raised above d12. The total number of steps stays the same.

On a Strong result, shift two steps. On a Weak result, the transfer happens but the donor system goes offline at the end of the scene.

## FTL travel

FTL is a two-track preparation procedure. Both tracks must be complete before the jump.

### Track 1: the Jump Capacitor Clock

The capacitors must be charged. The clock has **3, 6 or 9 segments** depending on route length and drive rating. Filling it costs **fuel** and **time**. A starport can charge the capacitors faster for money. The fuel is an exotic feedstock; the SA sets the local price and availability.

### Track 2: the Navigator's progress task

The Navigator plots the route. The task needs **3, 6 or 9 progress** depending on the route. Each check adds **1 / 2 / 3** progress on Weak / Standard / Strong. The nav computer grants a **Boon** but does not do the work or remove the time. Class abilities can add progress.

### The jump

When both tracks are complete, transit is **instantaneous**. The navigation result determines arrival:

- **Weak:** arrive off target or with a complication.
- **Standard:** arrive at the intended system and approach.
- **Strong:** arrive in a favourable position.

A triple natural 1 on the final navigation check can mean a damaged FTL drive or a hazardous arrival. The drive's rated range limits how far one jump can go; pushing it or using incomplete charts adds Banes or increases the clock.

## Sample ships

| Ship | Hull | DR | Handling | Jump | Systems |
|---|---:|---:|---:|---:|---|
| **Scout Cutter** | 20 | 2 | +1 | 3 | capacitors d8, FTL d8, nav d10, sensors d10, engines d8, weapons d6, defences d6, life support d8, comms d8 |
| **Free Trader** | 32 | 3 | 0 | 2 | capacitors d10, FTL d8, nav d8, sensors d6, engines d8, weapons d4, defences d8, life support d10, comms d8 |
| **System Shuttle** | 12 | 1 | +2 | — | capacitors d6, nav d6, sensors d6, engines d10, defences d4, life support d6, comms d6 |

## Running a ship scene

The ship should create decisions, not homework. Put one system under pressure, give the crew two ways to respond, and let the Engineer choose what to sacrifice. A chase is not a second combat system; it is a series of station actions with range bands and consequences. A jump is not a travel cutscene; it is the moment the crew finds out whether the preparation was enough.
