"""Structural audit for the initial Galaxies of Legend data set."""
from pathlib import Path
import itertools, re, sys

R = Path(__file__).resolve().parent
errors = []
warnings = []


def field(s, k):
    m = re.search(r"\*\*" + re.escape(k) + r":\*\* ([^\n]+)", s)
    return m[1].split(" · **")[0].strip() if m else ""


def title(p):
    return p.read_text().splitlines()[0].removeprefix("# ")


def check_links():
    for p in R.rglob("*.md"):
        s = p.read_text()
        for m in re.finditer(r"\]\(([^)]+)\)", s):
            link = m.group(1)
            if link.startswith(("http", "#", "mailto")):
                continue
            target = link.split("#")[0]
            if not target:
                continue
            if not (p.parent / target).resolve().exists():
                errors.append(f"{p.relative_to(R)}: broken link {link}")


def check_cards():
    cards = sorted((R / "cards").glob("*.md"))
    ids = set()
    for p in cards:
        s = p.read_text()
        cid = field(s, "ID")
        if not cid:
            errors.append(f"{p.name}: missing ID")
        elif cid in ids:
            errors.append(f"{p.name}: duplicate ID {cid}")
        ids.add(cid)
        for k in ("Action", "Attribute", "Target / range / shape", "Duration", "Tier / minimum level", "DP", "Requirements to learn", "Type"):
            if not field(s, k) and k != "DP":
                errors.append(f"{p.name}: missing {k}")
        tier = field(s, "Tier / minimum level")
        dp = field(s, "DP")
        if tier in ("1", "3", "7") and dp != {"1": "2", "3": "4", "7": "8"}[tier]:
            if not (tier == "1" and dp == "1"):
                errors.append(f"{p.name}: tier {tier} has DP {dp}")
        if tier == "Universal" and dp != "Not purchased":
            errors.append(f"{p.name}: universal card has DP {dp}")
    return cards


def check_homeworlds():
    homes = [p for p in sorted((R / "homeworlds").glob("*.md")) if not p.name.startswith("trait-")]
    for p in homes:
        s = p.read_text()
        links = re.findall(r"\]\((trait-[^)]+\.md)\)", s)
        if len(links) != 5:
            errors.append(f"{p.name}: {len(links)} traits, expected 5")
        for t in links:
            if not (p.parent / t).exists():
                errors.append(f"{p.name}: missing {t}")
        for k in ("Starting values", "Starting coin contribution"):
            if k not in s:
                errors.append(f"{p.name}: missing {k}")
    return homes


def check_classes():
    classes = sorted((R / "classes").glob("*.md"))
    for p in classes:
        s = p.read_text()
        sigs = re.findall(r"\]\(\.\./cards/(signature-[^)]+\.md)\)", s)
        if len(sigs) != 3:
            errors.append(f"{p.name}: {len(sigs)} signature links, expected 3")
        if not re.search(r"minimum 0 in [^;]+;", s):
            errors.append(f"{p.name}: missing attribute minimums")
        if not re.search(r"HP contribution \+\d+", s):
            errors.append(f"{p.name}: missing HP contribution")
        if not re.search(r"choose two distinct rank-1 disciplines from [^.]+\.", s):
            errors.append(f"{p.name}: missing starting disciplines")
    return classes


def check_coins(homes, classes):
    def coin(p, label):
        m = re.search(r"\+?(\d+) coins", p.read_text())
        return int(m.group(1)) if m else None
    hcoins = {p.stem: coin(p, "homeworld") for p in homes}
    ccoins = {p.stem: coin(p, "culture") for p in (R / "origins").glob("culture-*.md")}
    bcoins = {p.stem: coin(p, "background") for p in (R / "origins").glob("background-*.md")}
    clcoins = {p.stem: coin(p, "class") for p in classes}
    values = []
    for h, c, b, cl in itertools.product(hcoins, ccoins, bcoins, clcoins):
        values.append(40 + hcoins[h] + ccoins[c] + bcoins[b] + clcoins[cl])
    if not values:
        errors.append("no coin combinations")
    elif min(values) < 50 or max(values) > 70:
        warnings.append(f"coin range {min(values)}–{max(values)} outside 50–70 target")
    return min(values), max(values), len(values)


def main():
    check_links()
    cards = check_cards()
    homes = check_homeworlds()
    classes = check_classes()
    lo, hi, n = check_coins(homes, classes)
    print(f"Cards: {len(cards)}")
    print(f"Homeworlds: {len(homes)}; traits: {len(list((R / 'homeworlds').glob('trait-*.md')))}")
    print(f"Cultures: {len(list((R / 'origins').glob('culture-*.md')))}; backgrounds: {len(list((R / 'origins').glob('background-*.md')))} ")
    print(f"Classes: {len(classes)}; disciplines: {len(list((R / 'disciplines').glob('*.md')))}; equipment: {len(list((R / 'equipment').glob('*.md')))}")
    print(f"Coin combinations: {n}; range {lo}–{hi}")
    for w in warnings:
        print("WARN:", w)
    if errors:
        print("\nERRORS:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("Audit passed.")


if __name__ == "__main__":
    main()
