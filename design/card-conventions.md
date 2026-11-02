# Card conventions

Every learned ability uses the same fields. The card is the complete procedure; the book's general rules are the context, not a substitute.

## The fields

- **Action:** Main Action, Maneuver, Reaction, Passive or a stated full time.
- **Attribute:** exactly one attribute, or `None (no roll)`.
- **Target / range / shape:** who or what is affected, in squares or range bands.
- **Effect:** the procedure and the three outcomes.
- **Duration:** when the effect ends. Instant damage happens once.
- **Equipment / acquisition:** what the ability requires or grants.
- **Tier / DP / Requirements:** when and how the ability is bought.
- **Type and Tags:** sorting aids only; they do not grant rules.
- **Limits:** how often it can be used.

## Outcomes

Use the shared bands:

- **Weak** — the action costs something, changes the situation, or partly succeeds.
- **Standard** — the stated intent is achieved.
- **Strong** — the intent is achieved with a defined advantage.

Each bullet is a complete result. Apply only the rolled bullet. If a result says "also," apply the stated addition. Do not turn a Strong result into an extra full turn.

## Prices and gates

| Tier | DP | Minimum level |
|---|---:|---:|
| Novice | 2 | 1 |
| Adept | 4 | 3 |
| Master | 8 | 7 |

A 1-DP exception must be named individually. Class signatures require only the class and the listed level; they do not require an earlier signature or a discipline rank. Shared abilities require the printed discipline ranks and must be bought in rank order.

## Equipment

A grant supplies one missing ordinary item on acquisition. It does not supply a second copy after the item is sold. A requirement without a grant must be met with coins, salvage or a story permission from the SA.

## Damage and conditions

Use Physical, Fire, Cold, Lightning, Mental, Radiant and Life/Necrotic with the descriptive GOL aliases in [damage](rules/damage.md). Conditions follow the complete [condition reference](rules/conditions.md). A card applying a condition names its rating and duration; a permanent wound remedy is not temporary condition decay.

Rolled HP healing follows [Moser's law and healing](rules/healing.md): 1/3/7 HP paid before the roll by Novice/Adept/Master, bypassing resistance and leaving the healer above 0, with a free hand. Life resistance reduces ordinary healing; minimum 1 if HP is missing, cap at missing HP. Fixed medical doses use their own inventory procedure, no healer cost or outcome roll. Treatment progress is not HP healing. A long action takes its printed full time; Main Action does not compress an hour into a turn.


## Signatures

A signature should be recognizably better than a shared card of the same tier in one of these ways: action efficiency, reliability, scope, positioning, or a distinctive permission. It should not be a bigger number with no new decision.

## IDs

Every record ends with a stable `**ID:**` line. IDs do not change when a name changes. The build and audit use them for navigation and duplicate checks.
