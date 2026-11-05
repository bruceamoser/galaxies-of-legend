"""Exact dice enumeration and provisional encounter estimates for the SA book."""
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import isqrt
from pathlib import Path
import re

BOOK = Path(__file__).resolve().parent
OUTCOMES = ("Weak", "Standard", "Strong")
DIFFICULTY = {
    "easy": Fraction(3, 4), "standard": Fraction(1),
    "hard": Fraction(3, 2), "extreme": Fraction(2),
}
PHYSICAL = {"Physical", "Kinetic", "Sonic", "Corrosive"}


def outcome_probabilities(attribute=1, net_dice=0):
    if not -3 <= net_dice <= 3:
        raise ValueError("Expected at most three net Boons or Banes")
    counts = Counter()
    for roll in product(range(1, 7), repeat=3 + abs(net_dice)):
        dice = sorted(roll, reverse=net_dice > 0)[:3]
        total = sum(dice) + attribute
        band = 0 if dice == [1] * 3 or total <= 8 else 2 if dice == [6] * 3 or total >= 15 else 1
        counts[band] += 1
    return tuple(Fraction(counts[i], counts.total()) for i in range(3))


def expected_damage(damage, resistance, probabilities):
    return sum(probability * max(1, amount - resistance)
               for amount, probability in zip(damage, probabilities))


@dataclass(frozen=True)
class Seed:
    attacks_to_defeat: Fraction
    damage_per_round: Fraction
    utility: Fraction
    value: int


def estimate(hp, physical_resistance, damage, damage_type, utility=Fraction(1)):
    reference = outcome_probabilities()
    incoming = expected_damage((2, 3, 5), physical_resistance, reference)
    outgoing = expected_damage(damage, int(damage_type in PHYSICAL), reference[::-1])
    endurance = Fraction(hp) / incoming
    squared = 9 * endurance * outgoing * utility**2
    floor = isqrt(squared.numerator // squared.denominator)
    value = floor if floor**2 == squared else floor + 1
    return Seed(endurance, outgoing, utility, max(1, value))


# Judgments are visible and revisable. Shared no-roll abilities are assessed in
# the matchup, so a menu of mutually exclusive options cannot inflate U by count.
UTILITY = {
    "barricade-walker": (Fraction(11, 10), "Stable lane blocker"),
    "contract-sharpshooter": (Fraction(11, 10), "Long range from a prepared perch"),
    "echo-knot": (Fraction(5, 4), "Strong result can deny action categories"),
    "fixed-sentry": (Fraction(11, 10), "Long firing lane; assumes target enters its arc"),
    "industrial-loader": (Fraction(11, 10), "Strong displacement and Stability 2"),
    "prism-nestkeeper": (Fraction(5, 4), "Strong blindness can deny sight-required actions"),
    "clear-block": (Fraction(5, 4), "Engulfment restricts movement and uses an alternate damaging action"),
    "blanket-mold": (Fraction(5, 4), "Overhead grapple and hoist change positioning"),
    "shatter-jelly": (Fraction(11, 10), "One division creates another position without adding HP or actions"),
    "hull-grazer": (Fraction(5, 4), "Exterior positioning and a maintained grapple"),
    "white-cinder": (Fraction(5, 4), "Strong blindness and light-following movement"),
}


def attack_record(text):
    """Use the first damaging Main Action with one damage type in all bands."""
    for section in re.split(r"(?m)^## ", text)[1:]:
        if not re.search(r"(?m)^\*\*Action:\*\* Main Action\b", section):
            continue
        rows = re.findall(r"(?m)^- \*\*(Weak|Standard|Strong):\*\* (\d+) ([\w/]+) damage\b", section)
        if tuple(row[0] for row in rows) == OUTCOMES and len({row[2] for row in rows}) == 1:
            return section.splitlines()[0], tuple(int(row[1]) for row in rows), rows[0][2]
    return None


def read_catalog(book=BOOK):
    catalog = {}
    for path in sorted((book / "threats").glob("*.md")):
        text = path.read_text()
        title = text.splitlines()[0].removeprefix("# ")
        attack = attack_record(text)
        utility, note = UTILITY.get(path.stem, (Fraction(1), "Baseline; review special options in the matchup"))
        seed = None
        if attack:
            _, damage, damage_type = attack
            hp = int(re.search(r"\*\*HP:\*\* (\d+)", text)[1])
            resistance = int(re.search(r"\*\*Physical resistance:\*\* (\d+)", text)[1])
            seed = estimate(hp, resistance, damage, damage_type, utility)
        catalog[path.stem] = (title, attack, seed, note)
    return catalog


def party_budget(levels, dock_watch_value, difficulty="standard"):
    if not levels or any(not 1 <= level <= 10 for level in levels):
        raise ValueError("Expected a nonempty party with levels 1–10")
    # Anchor on four Dock Watch. HoL's linear slope is a testing hypothesis.
    raw = sum(Fraction(4 * dock_watch_value + 8 * (level - 1), 4) for level in levels)
    return raw * DIFFICULTY[difficulty]


def encounter_roster(path, catalog):
    text = path.read_text()
    levels = [int(value) for value in re.search(r"(?m)^\*\*Test party levels:\*\* ([\d, ]+)$", text)[1].split(",")]
    difficulty = re.search(r"(?m)^\*\*Comparison budget:\*\* (\w+)$", text)[1]
    entries = re.findall(r"(?m)^- (\d+) × \[([^]]+)\]\(\.\./threats/([^/)]+)\.md\)$", text)
    if not entries:
        raise ValueError(f"{path}: missing roster")
    total = 0
    unrated = []
    for count, label, slug in entries:
        title, _, seed, _ = catalog[slug]
        if label != title or int(count) < 1:
            raise ValueError(f"{path}: invalid roster entry {label}")
        if seed is None:
            unrated.append(f"{count} × {title}")
        else:
            total += int(count) * seed.value
    budget = party_budget(levels, catalog["dock-watch"][2].value, difficulty)
    return total, unrated, budget


if __name__ == "__main__":
    catalog = read_catalog()
    print(f"{sum(row[2] is not None for row in catalog.values())}/{len(catalog)} profiles with damage-based seeds")
    for path in sorted((BOOK / "encounters").glob("*.md")):
        total, unrated, budget = encounter_roster(path, catalog)
        pending = f" + unrated: {', '.join(unrated)}" if unrated else ""
        print(f"{path.stem}: {total}{pending}; comparison budget {budget}")
