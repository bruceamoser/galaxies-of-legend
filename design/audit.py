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


def check_discipline_coverage(cards):
    disciplines = {p.stem.title() for p in (R / "disciplines").glob("*.md")}
    counts = {(discipline, rank): 0 for discipline in disciplines for rank in (1, 2, 3)}
    for card in cards:
        copy = card.read_text()
        requirement = field(copy, "Requirements to learn")
        match = re.fullmatch(r"([A-Za-z]+) ([123])", requirement)
        if not match:
            continue
        discipline, rank_text = match.groups()
        rank = int(rank_text)
        if discipline not in disciplines:
            errors.append(f"{card.name}: unknown discipline {discipline}")
            continue
        if field(copy, "Tier / minimum level") == {1: "1", 2: "3", 3: "7"}[rank]:
            counts[discipline, rank] += 1
    for (discipline, rank), count in sorted(counts.items()):
        if count < 2:
            errors.append(f"{discipline} {rank}: expected at least two matching-tier shared choices, found {count}")
    print(f"Discipline ranks with at least two shared choices: {sum(count >= 2 for count in counts.values())}/{len(counts)}")
    return counts


def check_ancestries():
    entries = sorted((R / "ancestries").glob("*.md"))
    for p in entries:
        content = p.read_text()
        traits = re.findall(r"(?m)^([1-5])\. \*\*[^*]+\*\* .+", content)
        if traits != list("12345"):
            errors.append(f"{p.name}: expected five numbered traits")
        if not re.search(r"HP \+\d+, base Speed \d+, \+\d+ coins", content):
            errors.append(f"{p.name}: missing starting values")
    return entries


def check_classes():
    classes = sorted((R / "classes").glob("*.md"))
    for p in classes:
        s = p.read_text()
        sigs = re.findall(r"\]\(\.\./cards/(signature-[^)]+\.md)\)", s)
        options = 3
        for level in (1, 3, 7):
            section = re.search(rf"(?ms)^## Level {level}\s*\n(.*?)(?=^## |\Z)", s)
            links = re.findall(r"\]\(\.\./cards/(signature-[^)]+\.md)\)", section[1]) if section else []
            if len(links) != options or len(set(links)) != options:
                errors.append(f"{p.name}: expected {options} distinct level-{level} signatures")
            for link in links:
                card = R / "cards" / link
                if card.exists() and field(card.read_text(), "Tier / minimum level") != str(level):
                    errors.append(f"{p.name}: {link} is in the wrong milestone")
        if not re.search(r"minimum 0 in [^;]+;", s):
            errors.append(f"{p.name}: missing attribute minimums")
        if not re.search(r"HP contribution \+\d+", s):
            errors.append(f"{p.name}: missing HP contribution")
        if not re.search(r"choose two distinct rank-1 disciplines from [^.]+\.", s):
            errors.append(f"{p.name}: missing starting disciplines")
        known = {p.stem.replace('-', ' ').lower() for p in (R / 'disciplines').glob('*.md')}
        start=re.search(r'choose two distinct rank-1 disciplines from ([^.]+)',s)
        if start:
            for discipline in start[1].split(','):
                if discipline.strip().lower() not in known: errors.append(f'{p.name}: unknown starting discipline {discipline}')
        for sig in sigs:
            target=p.parent.parent/'cards'/sig
            if target.exists() and 'Class '+title(p)+';' not in field(target.read_text(),'Requirements to learn'):
                errors.append(f'{p.name}: signature belongs to another class')
        for label in ('Starting disciplines', 'Discipline pricing'):
            if not field(s,label): errors.append(f'{p.name}: missing {label}')
    return classes


def check_coins(homes, classes):
    def coin(p, label):
        m = re.search(r"\+?(\d+) coins", p.read_text())
        return int(m.group(1)) if m else None
    hcoins = {p.stem: coin(p, "ancestry") for p in homes}
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
    check_discipline_coverage(cards)
    for p in (R/'origins').glob('*.md'):
        text=p.read_text()
        grants=re.findall(r'\*\*([A-Za-z]+) 1\*\* and \[([^]]+)\]\(\.\./cards/([^)]+)\)',text)
        if len(grants)!=1:
            errors.append(f'{p.name}: expected one complete discipline/card pair');continue
        discipline,_,card=grants[0]
        if not (R/'disciplines'/f'{discipline.lower()}.md').exists(): errors.append(f'{p.name}: unknown discipline')
        cp=R/'cards'/card
        if cp.exists() and discipline+' 1' not in field(cp.read_text(),'Requirements to learn'):
            errors.append(f'{p.name}: paired card does not belong to granted discipline')
    homes = check_ancestries()
    classes = check_classes()
    lo, hi, n = check_coins(homes, classes)
    print(f"Cards: {len(cards)}")
    print(f"Playtest ancestries: {len(homes)}; legacy homeworlds excluded")
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
