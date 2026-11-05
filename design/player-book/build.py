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
for p in (DESIGN / "rules").glob("*.md"):
    if p.name != "recovery.md": files[p.resolve()] = key(p)
for folder in ["ancestries", "origins", "classes", "disciplines", "cards", "equipment"]:
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
    if p.parent.name == "ancestries" and p.name.startswith("trait-"):
        s = re.sub(r"^\*\*Ancestry:\*\*[^\n]*\n", "", s, flags=re.M)
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


PLAYER_TABLE_WIDTHS = {
    "Attribute": "(74pt,1fr)", "Value": "(83pt,1fr)", "Step": "(93pt,1fr)",
    "Choice": "(1fr,42pt)", "Price band / disciplines": "(1fr,59pt)",
    "Price band": "(1fr,44pt,44pt,44pt)", "Death-roll result": "(80pt,1fr)",
    "What you record": "(1fr,1.15fr,1.45fr)", "Condition": "(90pt,1.1fr,1.25fr)",
    "Question": "(1fr,1.2fr)", "Situation": "(100pt,1fr)",
    "Action": "(65pt,1fr)", "Term": "(65pt,1fr)", "Item": "(1.5fr,1fr,42pt,55pt)",
    "Level": "(45pt,1fr,1.15fr)",
}


def render(s, p, base=2, skip_title=True, table_widths=None):
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
        elif t.type == "hr": out.append("#v(3pt)#line(length: 100%, stroke: .4pt + teal)#v(3pt)\n")
        elif t.type in ("fence", "code_block"): out.append("#raw(" + q(t.content) + ", block: true)\n")
        elif t.type == "table_open":
            rows = []; row = []; headers = []; i += 1
            while ts[i].type != "table_close":
                x = ts[i]
                if x.type == "tr_open": row = []
                elif x.type == "inline":
                    if not rows:
                        headers.append(x.content.replace("**", ""))
                    row.append("[" + inline(x.children, p) + "]")
                elif x.type == "tr_close": rows.append(row)
                i += 1
            n = len(rows[0]); head = "(" + ",".join(rows[0]) + ",)"
            rr = "(" + ",".join("(" + ",".join(r) + ",)" for r in rows[1:]) + ",)"
            options = ""
            widths = table_widths
            if widths is None and (p.is_relative_to(BOOK) or p.name in {
                "starting-coins.md", "market.md", "conditions.md"
            } or p.parent == DESIGN / "classes"):
                widths = PLAYER_TABLE_WIDTHS
            if widths and headers[0] in widths:
                options = ",widths:" + widths[headers[0]] + ",pad:4pt"
            if p.name != "wounds.md":
                numeric = [str(j) for j, value in enumerate(headers)
                           if value in {"HP", "Coins", "Bulk", "Cost", "Level", "Total"}
                           or value.startswith("Rank ")]
                if numeric:
                    options += ",numeric:(" + ",".join(numeric) + ",)"
            out.append("#rule-table(" + str(n) + "," + head + "," + rr + options + ")\n\n")
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
    if filename == "01-welcome.md":
        v += '#illustration("crew-on-watch",height:178pt)\n'
    banners = {
        "06-playing.md": ("crew-at-work", 195),
        "08-recovery.md": ("sickbay-watch", 155),
        "10-equipment.md": ("station-market", 155),
    }
    if filename in banners:
        asset, height = banners[filename]
        fit = "contain" if asset == "crew-at-work" else "cover"
        v += f'#illustration({q(asset)},height:{height}pt,fit:{q(fit)})\n'
    if filename == "14-reference.md":
        _, *sections = re.split(r"(?m)(?=^## )", p.read_text())
        quick = [render(section, p, base=1) for section in sections[:3]]
        v += f"#grid(columns:(.8fr,1.4fr,.9fr),gutter:12pt,[{quick[0]}],[{quick[1]}],[{quick[2]}])\n"
        v += render("".join(sections[3:5]), p, base=1)
        v += '#pagebreak(weak:true)\n'
        v += render("".join(sections[5:]), p, base=1)
    elif filename == "appendix-origins.md":
        intro, *systems = re.split(r"(?m)(?=^## )", p.read_text())
        first_left = render(intro + "".join(systems[:2]), p, base=1)
        first_right = render("".join(systems[2:5]), p, base=1)
        next_left = render("".join(systems[5:8]), p, base=1)
        next_right = render("".join(systems[8:]), p, base=1)
        v += f"#grid(columns:(1fr,1fr),gutter:20pt,[{first_left}],[{first_right}])\n"
        v += '#pagebreak(weak:true)\n'
        v += f'#grid(columns:(1fr,1fr),gutter:20pt,[{next_left}],[{next_right}#illustration("jump-watch",height:190pt,fit:"cover")])\n'
    elif filename == "02-creation.md":
        guide, example = p.read_text().split("## Worked character", 1)
        first, finish = guide.split("## 7. Resolve", 1)
        checklist, advancement = finish.split("## Advancement", 1)
        v += reading(first, p)
        v += "#pagebreak(weak:true)\n"
        left = render("## 7. Resolve" + checklist, p, base=1)
        right = render("## Advancement" + advancement, p, base=1)
        v += f"#grid(columns:(1fr,1fr),gutter:20pt,[{left}],[{right}])\n"
        v += '#tail-art("origin-port",limit:235pt)\n#pagebreak(weak:true)\n'
        v += "#block(breakable:false)[" + render("## Worked character" + example, p, base=1) + "]\n"
    elif filename == "05-disciplines.md":
        ranks, examples = p.read_text().split("## Choose what you want to do", 1)
        left = render(ranks, p, base=1)
        right = render("## Choose what you want to do" + examples, p, base=1)
        v += f"#grid(columns:(1fr,1fr),gutter:20pt,[{left}],[{right}])\n"
        v += '#tail-art("ability-coordination",limit:270pt)\n'
    elif filename in {"intro-ancestry.md", "intro-classes.md"}:
        paragraphs = p.read_text().strip().split("\n\n")[1:]
        split = 1 if filename == "intro-ancestry.md" else 2
        left = render("\n\n".join(paragraphs[:split]), p)
        right = render("\n\n".join(paragraphs[split:]), p)
        v += f"#grid(columns:(1fr,1fr),gutter:20pt,[{left}],[{right}])\n"
    else:
        v += reading(p.read_text(), p)
    return v


def doc(p, kind="entry", wide=False):
    record(p, kind); s = clean(p)
    if kind in ("ancestry", "trait", "culture", "background", "discipline", "equipment"):
        icons = "[ #discipline-mark(" + q(p.stem) + ",\"\",size:28pt) ]" if kind == "discipline" else "[]"
        if kind == "discipline":
            examples = DISCIPLINE_EXAMPLES[p.stem]
            names = [f"[{name(DESIGN / 'cards' / (slug + '.md'))}](../cards/{slug}.md)" for slug in examples]
            s += "\n**Example abilities:** " + ", ".join(names) + ".\n"
        text = "#catalog-card(" + q(name(p)) + "," + q(key(p)) + ",icons: " + icons + ")[" + render(s, p) + "]\n"
    else:
        text = "#entry(" + q(name(p)) + "," + q(key(p)) + ")\n" + render(s, p)
    return text if wide else "#twocol[\n" + text + "]\n"


def card(p, *, compact=False):
    record(p, "ability"); s = clean(p)
    def field(label, default=""):
        m = re.search(r"\*\*" + re.escape(label) + r":\*\*\s*(.*?)(?=\s*·\s*\*\*|\n|$)", s)
        return m.group(1).strip() if m else default
    tier = field("Tier / minimum level"); req = field("Requirements to learn")
    action = field("Action"); attr = field("Attribute"); tags = " / ".join(dict.fromkeys(t.strip() for t in (field("Type") + "/" + field("Tags")).split("/") if t.strip())); price = field("DP")
    card_records.append({"path": rel(p), "name": name(p), "tier": tier, "action": action,
                         "requirements": req, "key": key(p)})
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
    match = re.search(r"(?m)^- \*\*Weak:\*\* (.+)\n- \*\*Standard:\*\* (.+)\n- \*\*Strong:\*\* (.+)",s)
    if match:
        body = render(s[:match.start()],p)
        body += "#outcome-rows((" + ",".join("[" + render("**" + label + ":** " + value,p) + "]" for label,value in zip(("Weak","Standard","Strong"),match.groups())) + ",), compact:" + str(compact).lower() + ")\n"
        body += render(s[match.end():],p)
    else:
        body = render(s,p)
    return "#card(compact: " + str(compact).lower() + ", icons: [" + icons + "]," + ",".join(map(q, [name(p), "B" if tier == "Universal" else tier, req, action, attr, tags, "Basic action" if tier == "Universal" else price + " DP", key(p)])) + ")[\n" + body + "]\n"



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
    costs = rank_costs(p)
    band_names = {(1, 2, 4): "Home", (2, 4, 8): "Adjacent", (3, 6, 12): "Foreign", (4, 8, 16): "Opposed"}
    cost_table = "| Price band / disciplines | DP: 1 / 2 / 3 |\n|---|---|\n"
    for values, band_name in band_names.items():
        disciplines = ", ".join(d.title() for d in sorted(costs) if costs[d] == values)
        if disciplines:
            cost_table += "| " + band_name + ": " + disciplines + " | " + " / ".join(map(str, values)) + " |\n"
    core = "*" + narrative + "*\n\n**Attributes:** " + attrs + ". **HP:** +" + hp + ". **Coins:** +" + coins + ".\n\n"
    core += "**Starting ranks:** Choose two distinct rank-1 disciplines from " + starting + ".\n\n"
    role = re.search(r"(?m)^\*\*In the crew\.\*\* (.+)$", raw).group(1)
    core += role + "\n"
    core = "#grid(columns:(1fr,1fr),gutter:18pt,[" + render(core, p, base=1) + "],[" + render("### Discipline costs · DP per rank\n" + cost_table, p, base=1) + "])"
    return "#pagebreak(weak:true)\n#class-panel(" + q(name(p)) + "," + q(key(p)) + ")[" + core + "]\n"


def hp_reference():
    p = BOOK / "manuscript/02-creation.md"
    home = ["| All ten playtest ancestries | +2 |"]
    cls = []
    for slug, _ in CLASSES:
        f = DESIGN / "classes" / (slug + ".md")
        hp = re.search(r"HP contribution \+(\d+)", f.read_text()).group(1)
        cls.append("| " + name(f) + " | +" + hp + " |")
    intro = "#heading(level:2)[Starting HP]\n#label(\"starting-hp\")\nAll ten playtest ancestries contribute +2 HP. Add the class contribution, Fortitude and any explicit benefits.\n\n#note[#align(center)[#text(size:15pt,weight:\"bold\")[12 + ancestry + class + Fortitude + explicit benefits]]]\n"
    table = lambda title, rows: render("## " + title + "\n| Choice | HP |\n|---|---:|\n" + "\n".join(rows), p, base=1)
    intro += "#grid(columns:(1fr,1fr),gutter:18pt,[" + table("Ancestry", home) + "#heading(level:3)[Fortitude and benefits]\nAdd your Fortitude, including a negative value. Then add only benefits you actually chose. HP does not increase automatically with level. Record current HP separately from your maximum.],[" + table("Class", cls) + "])\n"
    return intro


def coin_reference():
    p = DESIGN / "starting-coins.md"; record(p, "market-reference"); t = clean(p)
    sections = dict((m.group(1), m.group(2)) for m in re.finditer(r"## ([^\n]+)\n(.*?)(?=\n## |\Z)", t, re.S))
    def table(title):
        return render("### " + title.replace(" contribution", "") + "\n" + sections[title], p, base=1)
    intro = ("Add the contributions from ancestry, culture, background and class to 40 coins. "
             "Record any equipment granted by your abilities before you shop.\n")
    result = "#pagebreak(weak:true)\n#entry(\"Starting coins\"," + q(key(p)) + ")\n" + render(intro, p) + "\n"
    result += "#grid(columns:(1fr,1fr),gutter:12pt,["
    result += table("Ancestry contribution") + table("Class contribution")
    result += '#illustration("station-market",height:145pt,fit:"cover")\n'
    result += "],[" + table("Culture contribution") + table("Background contribution") + "])\n"
    return result


def discipline_matrix():
    result = ""
    for offset in range(0,len(CLASSES),5):
        classes = [DESIGN / "classes" / (slug + ".md") for slug,_ in CLASSES[offset:offset+5]]
        head = ["[Discipline]"] + ["[#text(" + q(name(p)) + ")]" for p in classes]
        rows=[]
        for d in DISCIPLINES:
            row = ["[#xref(" + q(key(DESIGN / "disciplines" / (d + ".md"))) + ")[#text(" + q(d.title()) + ")]]"]
            row += ["[" + "/".join(map(str,rank_costs(p)[d])) + "]" for p in classes]
            assert len(row) == len(head)
            rows.append("(" + ",".join(row) + ",)")
        result += "#pagebreak(weak:true)\n#heading(level:2)[Discipline costs by class - " + str(offset//5+1) + "]\n"
        result += "Each cell gives *rank 1 / rank 2 / rank 3*, in DP. Pay each rank separately.\n\n"
        result += "#cost-matrix((" + ",".join(head) + ",),(" + ",".join(rows) + ",))\n"
    return result

CLASSES = [(p.stem,name(p)) for p in sorted((DESIGN/"classes").glob("*.md"))]

DISCIPLINES = sorted(p.stem for p in (DESIGN / "disciplines").glob("*.md"))

DISCIPLINE_EXAMPLES = {
    "armor": ("wear-light-armor", "read-the-impact"),
    "arms": ("reverse-grip", "measure-the-reach"),
    "athletics": ("catch-the-ledge", "rig-the-haul"),
    "command": ("clear-orders", "set-the-rendezvous"),
    "computing": ("read-the-warning", "recover-an-autosave"),
    "engineering": ("field-repair", "bridge-the-service-gap"),
    "gunnery": ("overwatch", "check-the-backstop"),
    "influence": ("make-the-introduction", "find-the-shared-interest"),
    "investigation": ("bag-the-fragment", "reconstruct-the-route"),
    "medicine": ("patch-wounds", "assess-for-transport"),
    "navigation": ("mark-the-return", "cross-check-the-landmark"),
    "piloting": ("read-the-controls", "rehearse-the-abort"),
    "robotics": ("check-the-gripper", "audit-the-routine"),
    "science": ("sensor-sweep", "test-the-boundary"),
    "subterfuge": ("shadow-step", "watch-the-shift-change"),
    "survival": ("make-camp", "read-the-weather-break"),
    "trade": ("find-a-market", "cost-the-detour"),
    "xenology": ("establish-protocol", "compare-the-greeting"),
}


def ability_browser(paths, tier):
    title = {"Universal": "Basic Actions", "open": "Universal Abilities", "1": "Novice abilities", "3": "Adept abilities", "7": "Master abilities"}[tier]
    result = "#pagebreak(weak:true)\n#heading(level:2," + q(title) + ")\n"
    result += "Select an ability name to read its full rules. "
    result += ("Everyone knows these actions. They cost no DP.\n\n" if tier == "Universal"
               else "Learn these abilities at their printed level and DP cost. They require no discipline rank.\n\n" if tier == "open"
               else "Check the requirements and printed DP price before learning.\n\n")
    rows = []
    for p in paths:
        s = p.read_text()
        field = lambda label: re.search(r"\*\*" + re.escape(label) + r":\*\*\s*(.*?)(?=\s*·\s*\*\*|\n|$)", s).group(1).strip()
        rows.append("([#xref(" + q(key(p)) + ")[#text(" + q(name(p)) + ")]], [#text(" + q(field("Requirements to learn")) + ")], [#text(" + q(field("Action")) + ") #action-mark(" + q(field("Action")) + ")], [#text(" + q(field("Target / range / shape")) + ")])")
    result += "#ability-directory((" + ",".join(rows) + ",))\n#v(10pt)\n"
    cards = [card(p, compact=True) for p in paths]
    result += "#ability-pages((" + ",".join("[" + item + "]" for item in cards) + ",))\n"
    art = {"1": "ability-breach", "3": "ability-coordination", "7": "ability-rescue"}
    if tier in art:
        result += f'#tail-art({q(art[tier])},limit:200pt)\n'
    return result



def restored_rule(p, title, *, new_page=True):
    record(p,"inherited-rule")
    copy = p.read_text()
    if p.name == "conditions.md":
        copy = re.sub(r"(?s)Agreed condition rules,.*?(?=## Ratings)", "", copy)
    elif p.name == "damage.md":
        copy = copy.replace("GOL terms and the inherited damage families", "Damage types and equipment labels")
        copy = copy.replace("The seven HOL families remain", "The seven damage families are")
        copy = copy.replace("Existing GOL weapon cards can keep those descriptive labels.", "")
        copy = copy.replace("**GOL mapping proposals, not claims about HOL:**", "**Playtest damage labels.**")
        copy = copy.replace(" These two assignments require Bruce's review. The full Mental, Radiant and Life/Necrotic rules remain present even where the current weapon catalog has little coverage.", "")
        copy = copy.replace("GOL extension conditions", "Equipment faults")
        copy = copy.replace("Earlier GOL uses of Frozen mean the HOL Freezing condition; Stunned means Dazed.", "Read Frozen as Freezing and Stunned as Dazed.")
    elif p.name == "healing.md":
        copy = copy.replace("Applying the foundation in GOL", "Medical care")
        copy = copy.replace("The inherited cost is", "The healer pays")
        copy = copy.replace(" GOL's medical presentation does not waive that shared economy.", "")
        copy = copy.replace("A fixed-dose medical supply uses HOL's potion procedure:", "To administer a medical dose, use the following procedure.")
        copy = copy.replace(" This is a science-fiction presentation of the inherited consumable, not an additional stronger healing system.", "")
        copy = copy.replace("follows HOL's transfer rule:", "follows this rule.")
    return ("#pagebreak(weak:true)\n" if new_page else "") + "#entry(" + q(title) + "," + q(key(p)) + ")\n" + (reading(copy, p) if p.name == "damage.md" else render(copy,p,base=1))

def wound_reference():
    p=DESIGN/"rules/wounds.md";record(p,"wound-reference")
    sections=re.split(r"(?=^## (?:Physical|Elemental|Mental|Radiant|Life/Necrotic)\s*$)",p.read_text(),flags=re.M)
    result="#pagebreak(weak:true)\n#entry(\"Complete wound tables\"," + q(key(p)) + ")\n" + render(re.sub(r"(?s)Designer-reviewed working entries.*?(?=## Procedure)", "", re.sub(r"(?m)^(?:\*\*)?Open test concerns:[^\n]*(?:\n(?!\n)[^\n]*)*", "", sections[0])),p,base=1)
    for section in sections[1:]:
        # Each row is retained; only the table renderer changes for reading width and repeated captions.
        chunks=re.split(r"(?=^### )",section,flags=re.M)
        result+=render(chunks[0],p,base=1)
        for chunk in chunks[1:]:
            caption=chunk.splitlines()[0].lstrip("# ")
            body=render(chunk,p,base=1)
            body=body.replace("#rule-table(5,", "#wound-table(" + q(caption) + ",")
            result+=body
    return result

def ancestry_profile(p):
    record(p, "ancestry")
    intro, rules = clean(p).split("---", 1)
    intro, example = intro.split("**At the table.**", 1)
    intro, paths = intro.split("**Common paths.**", 1)
    intro, lore = intro.split("## Appearance", 1)
    lore = "## Appearance" + lore
    intro += "\n\n[Explore the associated system in Appendix A.](../player-book/manuscript/appendix-origins.md)"
    traits = re.findall(r"(?m)^\d+\. \*\*([^*]+)\*\* (.+)$", rules)
    assert len(traits) == 5, p
    panels = ", ".join("(" + q(title.rstrip(".")) + ", [" + render(copy, p) + "])" for title, copy in traits)
    appearance, society = lore.split("## Society and relations", 1)
    return (f"#ancestry-profile({q(name(p))}, {q(key(p))}, {q('lineage-' + p.stem)}, "
            f"({panels},), [{render(intro, p)}])\n"
            f"#ancestry-society({q(name(p))}, {q('place-' + p.stem)}, [{render(appearance,p,base=1)}], "
            f"[{render('## Society and relations' + society,p,base=1)}], "
            f"[{render(paths.strip(),p)}], [{render(example.strip(),p)}])\n")



def build_player():
    parts = ['#import "../template.typ": *\n']
    parts.append(manuscript("01-welcome.md", "1", "Welcome to Galaxies of Legend"))
    parts.append(manuscript("02-creation.md", "2", "Create Your Explorer"))
    parts.append(hp_reference())
    parts.append('#tail-art("crew-at-work",limit:155pt)\n')
    parts.append(coin_reference())

    parts.append(manuscript("intro-ancestry.md", "3", "Ancestry, Culture and Background"))
    parts.append('#tail-art("crew-lineages",limit:315pt)\n')
    ancestries = sorted((DESIGN / "ancestries").glob("*.md"), key=lambda p: (p.stem != "human", p.stem))
    lineage_heights = {
        "human": 1.75, "ambril": 1.65, "inkleaf": 1.25, "lethren": 1.85,
        "nacreth": 1.50, "orivane": 2.05, "pellori": 1.60, "silev": 1.55,
        "tessari": 1.55, "weldkin": 1.90,
    }
    lineup = ", ".join(
        f"({q(name(p))}, {q(key(p))}, {q('lineage-' + p.stem)}, {lineage_heights[p.stem]})"
        for p in ancestries
    )
    parts.append(f"#ancestry-lineup(({lineup},))\n")
    parts.extend(ancestry_profile(p) for p in ancestries)
    for typ, title in [("culture", "Cultures"), ("background", "Backgrounds")]:
        parts.append("#pagebreak(weak:true)\n#heading(level:2," + q(title) + ")\n")
        intro = BOOK / "manuscript" / ("intro-" + typ + ".md"); record(intro, "section")
        entries = ["#metadata(" + q(key(intro)) + ")<" + key(intro) + ">\n" + render(intro.read_text(), intro)]
        entries += [doc(p, typ, wide=True) for p in sorted((DESIGN / "origins").glob(typ + "-*.md"), key=name)]
        intro_text, *cards = entries
        parts.append(intro_text)
        parts.append("#grid(columns:(1fr,1fr),column-gutter:18pt,row-gutter:8pt,"
                     + ",".join("[" + item + "]" for item in cards) + ")\n")
        parts.append('#tail-art("' + ("place-nacreth" if typ == "culture" else "place-weldkin") + '",limit:220pt)\n')

    parts.append(manuscript("intro-classes.md", "4", "Classes"))
    parts.append('#tail-art("frontier-crew-review")\n')
    for c in CLASSES:
        p = DESIGN / "classes" / (c[0] + ".md")
        parts.append(class_page(p) + "#v(10pt)\n")
        sigs = re.findall(r"\]\(\.\./cards/(signature-[^)]+\.md)\)", p.read_text())
        if p.stem == "medic":
            briefing = BOOK / "manuscript" / "medic-briefing.md"
            record(briefing, "section")
            parts.append("#heading(level:2)[Field example · Medic]\n")
            _, triage, signatures = re.split(r"(?m)(?=^## )", briefing.read_text())
            left = render(triage, briefing)
            right = render(signatures, briefing)
            parts.append(f"#grid(columns:(1fr,1fr),gutter:20pt,[{left}],[{right}])\n")
            parts.append('#tail-art("sickbay-watch",limit:260pt)\n')
            parts.append("#pagebreak(weak:true)\n#heading(level:2)[Medic signatures]\n")
        menus = [sigs]
        if len(sigs) > 3:
            menus = [sigs[offset:offset + 3] for offset in range(0, len(sigs), 3)]
            parts.append("Choose one signature at each milestone. Additional signatures cost 2, 4 or 8 DP according to their level.\n")
        for level, menu in zip((1, 3, 7), menus):
            if len(menus) > 1:
                if level != 1 or p.stem == "medic":
                    parts.append("#pagebreak(weak:true)\n")
                parts.append(f"#heading(level:2)[{name(p)} signatures · Level {level}]\n")
            cards = [card(DESIGN / "cards" / slug, compact=True) for slug in menu]
            parts.append("#grid(columns:(1fr,1fr,1fr),gutter:10pt,"
                         + ",".join("[" + item + "]" for item in cards) + ")\n")

    parts.append(manuscript("05-disciplines.md", "5", "Disciplines"))
    parts.append(discipline_matrix())
    discipline_files = sorted((DESIGN / "disciplines").glob("*.md"), key=name)
    for offset in range(0,len(discipline_files),4):
        group = discipline_files[offset:offset + 4]
        parts.append("#pagebreak(weak:true)\n#grid(columns:(1fr,1fr),gutter:18pt,[" + "".join(doc(p, "discipline", wide=True) for p in group[:2]) + "],[" + "".join(doc(p, "discipline", wide=True) for p in group[2:]) + "])\n")

    parts.append(manuscript("06-playing.md", "6", "Playing the Game"))
    for filename in ("perception.md", "cover.md", "environment.md"):
        rule = DESIGN / "rules" / filename
        record(rule, "scene-procedure")
        parts.append("#pagebreak(weak:true)\n#entry(" + q(name(rule)) + "," + q(key(rule)) + ")\n")
        parts.append(reading(rule.read_text(), rule))
    language_rule = DESIGN / "rules/languages.md"
    record(language_rule, "scene-procedure")
    parts.append("#pagebreak(weak:true)\n#entry(" + q(name(language_rule)) + "," + q(key(language_rule)) + ")\n")
    opening, local, trade, translation, learning = re.split(
        r"(?m)(?=^## (?:Ordinary languages of the ten systems|Languages across systems|Translation and first contact|Learn in play)$)",
        language_rule.read_text(),
    )
    parts.append(reading(opening, language_rule))
    parts.append(render(local, language_rule, base=1, table_widths={
        "Language": "(110pt,125pt,1fr)",
    }))
    parts.append(render(trade, language_rule, base=1, table_widths={
        "Language": "(125pt,1fr)",
    }))
    parts.append(reading(translation + "\n" + learning, language_rule))
    parts.append(manuscript("08-recovery.md", "7", "Harm and Recovery"))
    parts.append(restored_rule(DESIGN / "rules/damage.md", "Damage, resistance and forced injury"))
    parts.append(restored_rule(DESIGN / "rules/healing.md", "Complete healing economy", new_page=False))
    parts.append(restored_rule(DESIGN / "rules/conditions.md", "Full condition reference"))
    parts.append(restored_rule(DESIGN / "rules/stability.md", "Stability and collisions", new_page=False))
    parts.append(wound_reference())


    parts.append(manuscript("09-abilities.md", "8", "Abilities"))
    for tier in ["Universal", "open", "1", "3", "7"]:
        paths = []
        for p in sorted((DESIGN / "cards").glob("*.md"), key=name):
            if p.name.startswith("signature-"): continue
            m = re.search(r"\*\*Tier / minimum level:\*\*\s*(\w+)", p.read_text())
            if m:
                unrestricted = m.group(1) != "Universal" and "**Requirements to learn:** None" in p.read_text()
                group = "open" if unrestricted else m.group(1)
                if group == tier:
                    paths.append(p)
        parts.append(ability_browser(paths, tier))

    parts.append(manuscript("10-equipment.md", "9", "Equipment and the Market"))
    parts.append(doc(DESIGN / "market.md", "market-reference", wide=True))
    parts.append("#pagebreak(weak:true)\n#heading(level:2)[Equipment entries]\n")
    intro = BOOK / "manuscript" / "intro-equipment.md"; record(intro, "section")
    parts.append("#metadata(" + q(key(intro)) + ")<" + key(intro) + ">\n" + render(intro.read_text(), intro))
    equipment = sorted((DESIGN / "equipment").glob("*.md"), key=name)
    groups = (
        ("Weapons", {"Weapon"}),
        ("Protection and mobility", {"Protection", "Mobility"}),
        ("Tools, sensors and communications", {"Tool", "Sensor", "Communications"}),
        ("Supplies", {"Supply"}),
    )
    for title, categories in groups:
        cards = []
        for item in equipment:
            category = re.search(r"\*\*Category:\*\* ([^·\n]+)", item.read_text())[1].strip()
            if category in categories:
                cards.append(doc(item, "equipment", wide=True))
        parts.append("#heading(level:2," + q(title) + ")\n")
        parts.append("#grid(columns:(1fr,1fr),column-gutter:18pt,row-gutter:8pt,"
                     + ",".join("[" + item + "]" for item in cards) + ")\n")


    companions = DESIGN / "rules/companions.md"
    record(companions, "companion-rules")
    parts.append("#pagebreak(weak:true)\n#entry(" + q(name(companions)) + "," + q(key(companions)) + ")\n")
    parts.append(reading(companions.read_text(), companions))

    parts.append(manuscript("11-starship-reference.md", "10", "Using the Starship Manual"))
    parts.append('#tail-art("jump-watch",limit:215pt)\n')
    parts.append(manuscript("14-reference.md", "11", "Table References"))
    parts.append(manuscript("appendix-origins.md", "A", "Star Systems and Species"))
    parts.append('#include "../sheets.typ"\n')

    (GEN / "body.typ").write_text("".join(parts))
    manifest = {"included": included, "cards": card_records, "internal_links": links,
                "external_design_references_rendered_as_text": sorted(excluded),
                "expected": {"ability": len(card_records), "ancestry": len(list((DESIGN/"ancestries").glob("*.md"))), "trait": 0,
                             "culture": len(list((DESIGN/"origins").glob("culture-*.md"))), "background": len(list((DESIGN/"origins").glob("background-*.md"))), "class": len(CLASSES), "discipline": len(DISCIPLINES),
                             "equipment": len(list((DESIGN/"equipment").glob("*.md")))}}
    (GEN / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print("Included", len(included), "records;", len(card_records), "abilities;", len(links), "internal links.")
    return manifest

if __name__ == "__main__":
    build_player()
    if "--compile" in os.sys.argv:
        typst = os.environ.get("TYPST") or shutil.which("typst") or "/tmp/hol-typst/typst-x86_64-unknown-linux-musl/typst"
        from export import export
        export(typst, ROOT, BOOK)
