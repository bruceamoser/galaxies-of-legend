#!/usr/bin/env python3
"""Read authored Markdown and emit Typst. Never rewrite the catalog."""
import argparse, hashlib, json, re, shutil, subprocess, os
from pathlib import Path
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
BOOK = Path(__file__).resolve().parent
DESIGN = ROOT / "design"
GEN = BOOK / "generated"; GEN.mkdir(exist_ok=True)
OUT = BOOK / "output"; OUT.mkdir(exist_ok=True)
ART = BOOK / "art/interior"; ART.mkdir(parents=True, exist_ok=True)
(GEN / "art-files.json").write_text(json.dumps(sorted(p.stem for p in ART.glob("*.png"))) + "\n")
(GEN / "space-art.json").write_text("[]\n")
md = MarkdownIt("commonmark").enable("table")
q = lambda s: json.dumps(str(s), ensure_ascii=False)
key = lambda p: "s-" + hashlib.sha1(str(Path(p).resolve().relative_to(ROOT)).encode()).hexdigest()[:12]
name = lambda p: Path(p).read_text().splitlines()[0].lstrip("# ").strip()
rel = lambda p: str(Path(p).resolve().relative_to(ROOT))

files = {}; links = []; excluded = set(); card_records = []; included = []
for folder in ["homeworlds", "origins", "classes", "disciplines", "cards", "equipment"]:
    for p in (DESIGN / folder).glob("*.md"):
        files[p.resolve()] = key(p)
for p in (BOOK / "manuscript").glob("*.md"):
    files[p.resolve()] = key(p)
for f in ["market.md", "starting-coins.md", "card-conventions.md"]:
    p = DESIGN / f
    if p.exists():
        files[p.resolve()] = key(p)


def record(p, kind):
    entry = {"path": rel(p), "kind": kind, "key": key(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
    if entry["path"] not in [r["path"] for r in included]:
        included.append(entry)


def clean(p):
    s = p.read_text()
    if p.parent == BOOK / "manuscript":
        return s
    s = re.sub(r"\*\*ID:\*\*[^\n]*", "", s)
    s = re.sub(r"(?:- )?\*\*Status:\*\*[^\n]*", "", s)
    s = "\n".join(line for line in s.splitlines() if not (line.startswith("[") and "](" in line))
    s = s.replace("## Rules", "---")
    s = s.replace("No multiclassing.", "")
    if p.parent.name == "origins":
        s = re.sub(r"^\*\*Type:\*\*[^\n]*\n", "", s, flags=re.M)
        s = re.sub(r"^The discipline rank and the card are one grant\..*\n", "", s, flags=re.M)
    if p.parent.name == "homeworlds" and p.name.startswith("trait-"):
        s = re.sub(r"^\*\*Homeworld:\*\*[^\n]*\n", "", s, flags=re.M)
    s = re.sub(r"^\s*-\s*$", "", s, flags=re.M)
    return s.strip() + "\n"


def inline(tokens, p):
    out = []; i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.type in ("text", "code_inline"):
            out.append("#text(" + q(t.content) + ")")
        elif t.type in ("softbreak", "hardbreak"):
            out.append(" " if t.type == "softbreak" else "#linebreak()")
        elif t.type == "strong_open": out.append("#strong[")
        elif t.type == "em_open": out.append("#emph[")
        elif t.type in ("strong_close", "em_close"): out.append("]")
        elif t.type == "link_open":
            j = i + 1; depth = 1
            while j < len(tokens):
                if tokens[j].type == "link_open": depth += 1
                if tokens[j].type == "link_close": depth -= 1
                if not depth: break
                j += 1
            body = inline(tokens[i + 1:j], p); href = t.attrGet("href")
            if href.startswith(("http:", "https:")):
                out.append("#link(" + q(href) + ")[" + body + "]")
            else:
                dest = (p.parent / href.split("#")[0]).resolve()
                if dest in files:
                    out.append("#xref(" + q(files[dest]) + ")[" + body + "]"); links.append((rel(p), rel(dest)))
                else:
                    out.append(body); excluded.add(rel(dest) if dest.is_relative_to(ROOT) else str(dest))
            i = j
        elif t.type == "html_inline": out.append("#text(" + q(t.content) + ")")
        elif t.type == "image": out.append("#text(" + q(t.content) + ")")
        i += 1
    return "".join(out)


def render(s, p, base=2, skip_title=True):
    ts = md.parse(s); out = []; i = 0
    while i < len(ts):
        t = ts[i]
        if t.type == "heading_open":
            lev = int(t.tag[1]); body = inline(ts[i + 1].children, p)
            if not (skip_title and lev == 1):
                out.append("#heading(level: " + str(min(3, base + lev - 1)) + ")[" + body + "]\n")
            i += 2
        elif t.type == "paragraph_open": pass
        elif t.type == "inline": out.append(inline(t.children, p))
        elif t.type == "paragraph_close": out.append("\n\n")
        elif t.type == "blockquote_open": out.append("#note[\n")
        elif t.type == "blockquote_close": out.append("]\n")
        elif t.type in ("bullet_list_open", "ordered_list_open"):
            out.append("#" + ("list" if t.type == "bullet_list_open" else "enum") + "(\n")
        elif t.type in ("bullet_list_close", "ordered_list_close"): out.append(")\n")
        elif t.type == "list_item_open": out.append("[")
        elif t.type == "list_item_close": out.append("],\n")
        elif t.type == "hr": out.append("#v(3pt)#line(length: 100%, stroke: .4pt + gold)#v(3pt)\n")
        elif t.type in ("fence", "code_block"): out.append("#raw(" + q(t.content) + ", block: true)\n")
        elif t.type == "table_open":
            rows = []; row = []; i += 1
            while ts[i].type != "table_close":
                x = ts[i]
                if x.type == "tr_open": row = []
                elif x.type == "inline": row.append("[" + inline(x.children, p) + "]")
                elif x.type == "tr_close": rows.append(row)
                i += 1
            n = len(rows[0]); head = "(" + ",".join(rows[0]) + ",)"
            rr = "(" + ",".join("(" + ",".join(r) + ",)" for r in rows[1:]) + ",)"
            out.append("#rule-table(" + str(n) + "," + head + "," + rr + ")\n\n")
        i += 1
    return "".join(out)


def flow(entries, gap="5pt"):
    return "#reading-columns((" + ",".join("[" + c + "]" for c in entries) + ",), gap:" + gap + ")\n"


def reading(s, p):
    chunks = []; pending = ""
    for part in re.split(r"\n\s*\n", s.strip()):
        if re.match(r"^# [^\n]+$", part): continue
        if re.match(r"^#{2,3} [^\n]+$", part): pending += part + "\n\n"; continue
        chunks.append(render(pending + part, p)); pending = ""
    if pending: chunks.append(render(pending, p))
    return "#reading-columns((" + ",".join("[" + c + "]" for c in chunks) + ",))\n"


def manuscript(filename, n, title):
    p = BOOK / "manuscript" / filename; record(p, "chapter")
    v = "#chapter(" + q(n) + "," + q(title) + ")\n#metadata(" + q(key(p)) + ")<" + key(p) + ">\n"
    v += reading(p.read_text(), p)
    return v


def doc(p, kind="entry", wide=False):
    record(p, kind); s = clean(p)
    if kind in ("homeworld", "trait", "culture", "background", "discipline", "equipment"):
        icons = "[ #discipline-mark(" + q(p.stem) + ",\"\",size:28pt) ]" if kind == "discipline" else "[]"
        text = "#catalog-card(" + q(name(p)) + "," + q(key(p)) + ",icons: " + icons + ")[" + render(s, p) + "]\n"
    else:
        text = "#entry(" + q(name(p)) + "," + q(key(p)) + ")\n" + render(s, p)
    return text if wide else "#twocol[\n" + text + "]\n"


def card(p):
    record(p, "ability"); s = clean(p)
    def field(label, default=""):
        m = re.search(r"\*\*" + re.escape(label) + r":\*\*\s*(.*?)(?=\s*·\s*\*\*|\n|$)", s)
        return m.group(1).strip() if m else default
    tier = field("Tier / minimum level"); req = field("Requirements to learn")
    action = field("Action"); attr = field("Attribute"); tags = field("Type"); price = field("DP")
    card_records.append({"path": rel(p), "name": name(p), "tier": tier, "action": action,
                         "requirements": req, "key": key(p)})
    if field("Tags"): tags += " / " + field("Tags")
    s = re.sub(r"^\*\*(?:Action|Tier / minimum level|Type|Tags):\*\*.*\n", "", s, flags=re.M)
    s = s.replace("## Rules", "---")
    s = s.replace("**Equipment / acquisition:**", "**Gear:**").replace("**Target / range / shape:**", "**Target:**")
    s = s.replace("**Limits:** Repeatable; pay the action and any stated costs each use.", "")
    s = s.replace("**Equipment / acquisition:** None.", "").replace("**Gear:** None.", "")
    icons = "".join(
        "#discipline-mark(" + q(d.lower()) + "," + q(r) + ")"
        for d, r in re.findall(r"([A-Za-z]+) ([123])", req)
        if (DESIGN / "disciplines" / (d.lower() + ".md")).exists()
    )
    return "#card(icons: [" + icons + "]," + ",".join(map(q, [name(p), "U" if tier == "Universal" else tier, req, action, attr, tags, "Universal" if tier == "Universal" else price + " DP", key(p)])) + ")[\n" + render(s, p) + "]\n"


def rank_costs(p):
    text = p.read_text()
    result = {d: (3, 6, 12) for d in DISCIPLINES}
    for band, cost in [("Home", (1, 2, 4)), ("Adjacent", (2, 4, 8)), ("Opposed", (4, 8, 16))]:
        m = re.search(band + r": ([^.]+)\.", text)
        if m:
            for item in m.group(1).split(","):
                d = item.strip().lower()
                if d in result:
                    result[d] = cost
    return result


def class_page(p):
    record(p, "class"); s = clean(p); raw = p.read_text()
    narrative = re.search(r"^\*([^*]+)\*$", s, re.M).group(1)
    attrs = re.search(r"minimum 0 in ([^;]+);", raw)
    attrs = (attrs.group(1).replace(" and ", ", ") + " ≥ 0") if attrs else "No minimums"
    hp = re.search(r"HP contribution \+(\d+)", raw).group(1)
    coins = re.search(r"\*\*Starting coin contribution:\*\* \+(\d+)", raw).group(1)
    starting = re.search(r"choose two distinct rank-1 disciplines from ([^.]+)", raw).group(1)
    cost_table = "| Discipline | 1 | 2 | 3 |\n|---|---:|---:|---:|\n" + "\n".join(
        "| [" + d.title() + "](../disciplines/" + d + ".md) | " + " | ".join(map(str, rank_costs(p)[d])) + " |"
        for d in sorted(rank_costs(p))
    )
    core = "*" + narrative + "*\n\n**Attributes:** " + attrs + ". **HP:** +" + hp + ". **Coins:** +" + coins + ".\n\n"
    core += "**Starting ranks:** Choose two distinct rank-1 disciplines from " + starting + ".\n\n"
    core += "### Discipline costs · DP per rank\n" + cost_table
    choices = []
    for lvl in (1, 3, 7):
        m = re.search(r"## Level " + str(lvl) + r"\n\n((?:- .*\n?)+)", raw)
        choices.append((lvl, m.group(1) if m else ""))
    sigs = "#grid(columns:(1fr,1fr,1fr),gutter:12pt," + ",".join(
        "[" + render("## Level " + str(lvl) + "\n" + body, p, base=1) + "]" for lvl, body in choices
    ) + ")"
    result = "#pagebreak(weak:true)\n#class-panel(" + q(name(p)) + "," + q(key(p)) + ")[\n#grid(columns:(1.05fr,1fr),gutter:16pt,[" + render(core, p, base=1) + "],[#illustration(" + q("class-" + p.stem) + ",height:420pt)])]\n"
    result += "#v(8pt)\n#signature-menu[" + sigs + "]\n"
    return result


def hp_reference():
    p = BOOK / "manuscript/02-creation.md"
    home = []
    for f in sorted((DESIGN / "homeworlds").glob("*.md")):
        if f.name.startswith("trait-"): continue
        t = f.read_text(); hp = re.search(r"HP \+(\d+)", t).group(1)
        home.append("| " + name(f) + " | +" + hp + " |")
    cls = []
    for slug, _ in CLASSES:
        f = DESIGN / "classes" / (slug + ".md")
        hp = re.search(r"HP contribution \+(\d+)", f.read_text()).group(1)
        cls.append("| " + name(f) + " | +" + hp + " |")
    intro = "#heading(level:2)[Starting HP]\n#label(\"starting-hp\")\nYour maximum HP brings together your homeworld, training and endurance. Calculate it after choosing your traits and purchases; then start at that maximum.\n\n#note[#align(center)[#text(size:15pt,weight:\"bold\")[12 + homeworld + class + Fortitude + explicit benefits]]]\n"
    table = lambda title, rows: render("## " + title + "\n| Choice | HP |\n|---|---:|\n" + "\n".join(rows), p, base=1)
    intro += "#grid(columns:(1fr,1fr),gutter:18pt,[" + table("Homeworld", home) + "#heading(level:3)[Fortitude and benefits]\nAdd your Fortitude, including a negative value. Then add only benefits you actually chose. HP does not increase automatically with level. Record current HP separately from your maximum.],[" + table("Class", cls) + "])\n"
    return intro


def coin_reference():
    p = DESIGN / "starting-coins.md"; record(p, "market-reference"); t = clean(p)
    sections = dict((m.group(1), m.group(2)) for m in re.finditer(r"## ([^\n]+)\n(.*?)(?=\n## |\Z)", t, re.S))
    def table(title):
        return render("### " + title.replace(" contribution", "") + "\n" + sections[title], p, base=1)
    intro = t.split("## Homeworld")[0]
    result = "#pagebreak(weak: true)\n#entry(\"Starting coins\"," + q(key(p)) + ")\n" + render(intro, p) + "\n"
    result += "#grid(columns:(1fr,1fr),gutter:12pt,["
    result += table("Homeworld contribution") + table("Class contribution")
    result += "],[" + table("Culture contribution") + table("Background contribution") + "])\n"
    return result


def discipline_matrix():
    classes = [DESIGN / "classes" / (c[0] + ".md") for c in CLASSES]
    costs = {p.stem: rank_costs(p) for p in classes}
    head = ["[Discipline]"] + ["[#text(" + q(name(p)) + ")]" for p in classes]
    rows = []
    for d in sorted(DISCIPLINES):
        row = ["[#xref(" + q(key(DESIGN / "disciplines" / (d + ".md"))) + ")[#text(" + q(d.title()) + ")]]"]
        row += ["[" + "/".join(map(str, costs[p.stem][d])) + "]" for p in classes]
        rows.append("(" + ",".join(row) + ",)")
    result = "#pagebreak(weak:true)\n#heading(level:2)[Discipline costs by class]\n"
    result += "Each cell gives *rank 1 / rank 2 / rank 3*, in DP. These are separate purchases, not cumulative totals.\n\n"
    result += "#cost-matrix((" + ",".join(head) + ",),(" + ",".join(rows) + ",))\n"
    return result


CLASSES = [
    ("soldier", "Soldier"), ("scientist", "Scientist"), ("spacer", "Spacer"),
    ("explorer", "Explorer"), ("medic", "Medic"), ("envoy", "Envoy"),
]
DISCIPLINES = sorted(p.stem for p in (DESIGN / "disciplines").glob("*.md"))


def summary(p):
    m = re.search(r"^\*([^*]+)\*$", p.read_text(), re.M)
    if not m: return ""
    s = m.group(1)
    return s.split(". ")[0].rstrip(".") + "."


def ability_browser(paths, tier):
    title = {"Universal": "Universal actions", "1": "Novice abilities", "3": "Adept abilities", "7": "Master abilities"}[tier]
    result = "#pagebreak(weak:true)\n#heading(level:2," + q(title) + ")\n"
    result += "Find a useful option here, then follow its name to the complete card. Summaries help you choose; the card supplies the exact targets, costs and outcomes.\n\n"
    rows = []
    for p in paths:
        s = p.read_text()
        field = lambda label: re.search(r"\*\*" + re.escape(label) + r":\*\*\s*(.*?)(?=\s*·\s*\*\*|\n|$)", s).group(1).strip()
        rows.append("([#xref(" + q(key(p)) + ")[#text(" + q(name(p)) + ")]], [#text(" + q(field("Requirements to learn")) + ")], [#text(" + q(field("Action")) + ")], [#text(" + q(summary(p)) + ")])")
    result += "#ability-directory((" + ",".join(rows) + ",))\n#pagebreak(weak:true)\n"
    result += flow([card(p) for p in paths])
    return result


parts = ['#import "../template.typ": *\n']
parts.append(manuscript("01-welcome.md", "1", "Welcome to Galaxies of Legend"))
parts.append(manuscript("02-creation.md", "2", "Create Your Explorer"))
parts.append(hp_reference())
parts.append(coin_reference())

parts.append("#chapter(\"3\",\"Homeworld, Culture and Background\")\n")
parts.append("#twocol[Choose the place that made you, the community that shaped you, and the work that taught you something before the first session. Your homeworld gives you a body and a history; culture and background give you paired training. None of these choices dictates your class or your personality.]\n")
for h in [p for p in sorted((DESIGN / "homeworlds").glob("*.md")) if not p.name.startswith("trait-")]:
    parts.append("#pagebreak(weak:true)\n#grid(columns:(1fr,1fr),gutter:18pt,[" + doc(h, "homeworld", wide=True) + "],[#illustration(" + q("homeworld-" + h.stem) + ",height:245pt)])\n")
    traits = re.findall(r"\]\((trait-[^)]+\.md)\)", h.read_text())
    parts.append("#twocol[\n" + "".join(doc(DESIGN / "homeworlds" / t, "trait", wide=True) for t in traits) + "]\n")
for typ, title in [("culture", "Cultures"), ("background", "Backgrounds")]:
    parts.append("#pagebreak(weak:true)\n#heading(level:2," + q(title) + ")\n")
    intro = BOOK / "manuscript" / ("intro-" + typ + ".md"); record(intro, "section")
    entries = ["#metadata(" + q(key(intro)) + ")<" + key(intro) + ">\n" + render(intro.read_text(), intro)]
    entries += [doc(p, typ, wide=True) for p in sorted((DESIGN / "origins").glob(typ + "-*.md"), key=name)]
    parts.append(flow(entries) + "#tail-art(" + q(typ + "s") + ")\n")

parts.append("#chapter(\"4\",\"Classes\")\n")
parts.append("#twocol[Choose the identity you want to bring to the crew. Each class grants two starting discipline choices and a signature at levels 1, 3 and 7. Shared abilities remain open to anyone who qualifies. Signatures belong only to their class. Choose one free signature at each milestone. Meet both attribute minimums before choosing your class; choose one class and do not multiclass.]\n")
for c in CLASSES:
    p = DESIGN / "classes" / (c[0] + ".md")
    parts.append(class_page(p) + "#pagebreak(weak:true)\n")
    sigs = re.findall(r"\]\(\.\./cards/(signature-[^)]+\.md)\)", p.read_text())
    parts.append(flow([card(DESIGN / "cards" / s) for s in sigs]))

parts.append(manuscript("05-disciplines.md", "5", "Disciplines"))
parts.append(discipline_matrix())
discipline_files = sorted((DESIGN / "disciplines").glob("*.md"), key=name)
for offset in (0, 5):
    group = discipline_files[offset:offset + 5]
    parts.append("#pagebreak(weak:true)\n#grid(columns:(1fr,1fr),gutter:18pt,[" + "".join(doc(p, "discipline", wide=True) for p in group[:3]) + "],[" + "".join(doc(p, "discipline", wide=True) for p in group[3:]) + "])\n")

parts.append(manuscript("06-playing.md", "6", "Playing the Game"))
parts.append(manuscript("08-recovery.md", "7", "Harm and Recovery"))

parts.append(manuscript("09-abilities.md", "8", "Abilities"))
for tier in ["Universal", "1", "3", "7"]:
    paths = []
    for p in sorted((DESIGN / "cards").glob("*.md"), key=name):
        if p.name.startswith("signature-"): continue
        m = re.search(r"\*\*Tier / minimum level:\*\*\s*(\w+)", p.read_text())
        if m and m.group(1) == tier: paths.append(p)
    parts.append(ability_browser(paths, tier))

parts.append(manuscript("10-equipment.md", "9", "Equipment and the Market"))
parts.append(doc(DESIGN / "market.md", "market-reference", wide=True))
parts.append("#pagebreak(weak:true)\n#heading(level:2)[Equipment entries]\n")
intro = BOOK / "manuscript" / "intro-equipment.md"; record(intro, "section")
entries = ["#metadata(" + q(key(intro)) + ")<" + key(intro) + ">\n" + render(intro.read_text(), intro)]
entries += [doc(p, "equipment", wide=True) for p in sorted((DESIGN / "equipment").glob("*.md"), key=name)]
parts.append(flow(entries))

parts.append(manuscript("11-starships.md", "10", "Starships and FTL"))
parts.append(manuscript("14-reference.md", "11", "Table References"))
parts.append('#include "../sheets.typ"\n')

(GEN / "body.typ").write_text("".join(parts))
manifest = {"included": included, "cards": card_records, "internal_links": links,
            "external_design_references_rendered_as_text": sorted(excluded),
            "expected": {"ability": len(card_records), "homeworld": 4, "trait": 20,
                         "culture": 4, "background": 4, "class": 6, "discipline": 9,
                         "equipment": 10}}
(GEN / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
print("Included", len(included), "records;", len(card_records), "abilities;", len(links), "internal links.")

if "--compile" in os.sys.argv:
    typst = os.environ.get("TYPST") or shutil.which("typst") or "/tmp/hol-typst/typst-x86_64-unknown-linux-musl/typst"
    from export import export
    export(typst, ROOT, BOOK)
