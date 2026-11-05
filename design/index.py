"""Rebuild navigation only. Authored records are never overwritten."""
from pathlib import Path
import re

R = Path(__file__).resolve().parent


def field(s, k):
    m = re.search(r"\*\*" + re.escape(k) + r":\*\* ([^\n]+)", s)
    return m[1].split(" · **")[0].strip() if m else ""


def title(p):
    return p.read_text().splitlines()[0].removeprefix("# ")


def link(p):
    return f"[{title(p)}]({p.relative_to(R)})"


def main():
    cards = []
    for p in sorted((R / "cards").glob("*.md")):
        cards.append((p, p.read_text()))

    txt = "# Abilities\n\nStart with the character you imagine, or browse by tier.\nEach card is an editable Markdown record. Class signatures remain exclusive;\nshared abilities are open to anyone who meets the printed requirements.\n\n"
    for label, test in [
        ("Basic Actions", lambda s: field(s, "Tier / minimum level") == "Universal"),
        ("Universal Abilities", lambda s: field(s, "Tier / minimum level") != "Universal"
         and field(s, "Type") != "Signature" and field(s, "Requirements to learn") == "None"),
        ("Discipline abilities", lambda s: field(s, "Tier / minimum level") != "Universal"
         and field(s, "Type") != "Signature" and field(s, "Requirements to learn") != "None"),
        ("Class signatures", lambda s: field(s, "Type") == "Signature"),
    ]:
        txt += "## " + label + "\n\n"
        for p, s in cards:
            if test(s):
                tier = field(s, "Tier / minimum level")
                cost = "already known; no DP" if tier == "Universal" else f"level {tier}; {field(s, 'DP')} DP; {field(s, 'Requirements to learn')}"
                txt += f"- {link(p)} — {field(s, 'Action')}; {cost}.\n"
        txt += "\n"
    (R / "catalog.md").write_text(txt.rstrip() + "\n")

    txt = "# Ancestries\n\nTen playtest ancestries. Choose two of five traits. See the [origin atlas](player-book/manuscript/appendix-origins.md) for species and star systems.\n\n"
    for p in sorted((R / "ancestries").glob("*.md")):
        txt += f"- {link(p)}\n"
    (R / "ancestry.md").write_text(txt.rstrip() + "\n")

    txt = "# Classes\n\nChoose one class. Each grants two starting disciplines and signatures at levels 1, 3 and 7.\n\n"
    for p in sorted((R / "classes").glob("*.md")):
        txt += f"- {link(p)}\n"
    (R / "class.md").write_text(txt.rstrip() + "\n")

    txt = "# Cultures and backgrounds\n\nChoose one culture and one background. Each is a paired rank-1 discipline and ability.\n\n"
    for kind in ("culture", "background"):
        ps = sorted((R / "origins").glob(kind + "-*.md"))
        txt += f"## {len(ps)} " + ("cultures" if kind == "culture" else "backgrounds") + "\n\n"
        for p in ps:
            txt += f"- {link(p)}\n"
        txt += "\n"
    (R / "culture-background.md").write_text(txt.rstrip() + "\n")

    txt = "# Disciplines\n\nBuy ranks in order. A rank is a prerequisite; it grants no passive bonus.\n\n"
    for p in sorted((R / "disciplines").glob("*.md")):
        d = title(p)
        txt += f"## {link(p)}\n\n"
        for cp, s in cards:
            if re.search(r"\b" + re.escape(d) + r" [123]\b", field(s, "Requirements to learn")):
                txt += f"- {link(cp)} — level {field(s, 'Tier / minimum level')}; {field(s, 'Action')}.\n"
        txt += "\n"
    (R / "disciplines.md").write_text(txt.rstrip() + "\n")

    txt = "# Equipment\n\nFollow the printed requirements. Buying gear does not grant training.\n\n"
    for p in sorted((R / "equipment").glob("*.md")):
        txt += f"- {link(p)}\n"
    (R / "equipment.md").write_text(txt.rstrip() + "\n")

    print(f"Navigation rebuilt for {len(cards)} cards; authored entries unchanged.")


if __name__ == "__main__":
    main()
