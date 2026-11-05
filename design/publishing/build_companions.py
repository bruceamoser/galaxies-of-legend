#!/usr/bin/env python3
"""Build Starship Manual and SA book using the existing GOL Markdown renderer."""
import sys,json,subprocess,hashlib,re,shutil,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PLAYER=ROOT/'design/player-book'
sys.path.insert(0,str(PLAYER))
import build as g

ROOT_BOOK_TITLE={"starship-manual":"Starship Manual","sa-book":"Sector Architect's Book"}

def cover_source(title,subtitle,art):
    return f'''#let release = json("../../release/version.json")
#set page(width:612pt,height:792pt,margin:0pt,fill:rgb("#0a1018"),header:none,footer:none)
#place(top+left,dx:42pt,dy:46pt,block(width:528pt)[
 #text(font:"Oswald",size:40pt,weight:"bold",fill:white)[GALAXIES OF LEGEND]
 #v(15pt)#text(font:"Oswald",size:26pt,fill:rgb("#65c5df"))[{title.upper()}]
 #v(7pt)#text(font:"Roboto",size:11pt,fill:white)[{subtitle}]
])
#place(top+left,dx:0pt,dy:215pt,image("../player-book/art/interior/{art}.png",width:612pt,height:405pt,fit:"cover"))
#place(top+left,dx:42pt,dy:653pt,block(width:528pt)[
 #line(length:60pt,stroke:3pt+rgb("#d92027"))
 #v(12pt)#text(font:"Oswald",size:15pt,fill:white)[BRUCE A. MOSER]
 #v(6pt)#text(font:"Roboto",size:10pt,fill:rgb("#c2dce4"))[Starter Kit v#release.version · Design Review · #release.date]
])
'''

def book_source(title,description,sheets):
    return f'''#import "../player-book/template.typ": *
#show: setup.with(book-title:{g.q(title)})
#let release = json("../../release/version.json")
#{{ include "cover.typ"; pagebreak() }}
#set document(title: "Galaxies of Legend — {title}",author:"Bruce A. Moser")
#align(center)[
 #v(30pt)#image("../player-book/art/gol-crest.png",width:115pt)
 #v(20pt)#text(font:"Oswald",size:30pt,fill:space)[Galaxies of Legend]
 #v(10pt)#text(font:"Oswald",size:24pt,fill:teal)[{title}]
 #v(16pt)#text(size:12pt)[First three-book Starter Kit · Design Review]
 #v(12pt)#text(size:11pt)[Game design by Bruce A. Moser]
]
#v(28pt)#note[{description}]
#v(12pt)#text(size:9pt)[Version #release.version · #release.date. Companion volumes: Player's Book, Starship Manual and Sector Architect's Book. New ship and SA numbers are playtest proposals.]
#v(10pt)#text(size:8.5pt)[Manuscript and layout prepared with Codex under Bruce's direction. Existing generated review illustrations are reused; font licenses and artwork notes are included in the source archive.]
#pagebreak()#outline(title:[Contents],depth:1)#pagebreak()
#include "generated/body.typ"
#include "{sheets}"
#pagebreak(weak:true)
#set page(header:none,footer:none)
#align(center+horizon)[
 #text(font:"Oswald",size:24pt,fill:space)[Galaxies of Legend]
 #v(10pt)#text(font:"Oswald",size:16pt,fill:teal)[{title}]
 #v(10pt)#text(size:10pt)[Starter Kit v#release.version · Design Review]
]
'''

def source(p,kind='chapter'):
    g.files[p.resolve()]=g.key(p);g.record(p,kind)
    return f'#metadata({g.q(g.key(p))})<{g.key(p)}>\n'


def worked_scout_sheet(book):
    data=json.loads((ROOT/'design/ships/construction.json').read_text())
    ship=json.loads((ROOT/'design/ships/examples.json').read_text())[0]
    frame=data['frames'][ship['frame']]
    spent=sum(data['die_sp_cost'][m['die']] for m in ship['modules'])
    abilities={'engines':'1 Boon: powered manoeuvres','navigation':'1 Boon: plotting','sensors':'Extreme reach; 1 Boon','life_support':'8 occupants (4 x Scale 2)','communications':'1 Bane: pressured radio','ftl':'3 route units','capacitors':'9 segments; 6 min/segment','weapons':'Thermal 3 / 5 / 7','defences':'Shield DR 2','cargo':'8 cargo units (4 x Scale 2)'}
    def cell(value):return '[#text('+g.q(str(value))+')]'
    rows=[]
    for m in ship['modules']:
        title=data['systems'][m['type']]['name']
        if m['type'] in data['required']:title='* '+title
        rows.extend(map(cell,(title,m['die'],data['die_sp_cost'][m['die']],m['die'],abilities[m['type']])))
    rows += ['[]']*(5*(16-len(ship['modules'])))
    body='''#import "../../player-book/template.typ": *
#import "../ship-sheets.typ": sheet,title,band,table-blank
#let value(label,body,height:35pt) = block(width:100%,height:height,inset:5pt,stroke:.5pt+teal,breakable:false)[
 #text(size:7.5pt,weight:"bold",fill:teal,label)#v(2pt)#text(size:11pt,weight:"bold",body)
]
#sheet([
 #title("WORKED BUILD / Scout Cutter")
 #v(7pt)#grid(columns:(2fr,1fr,1fr),gutter:6pt,value("SHIP NAME / REGISTRY","Scout Cutter",height:31pt),value("FRAME CLASS","Light",height:31pt),value("SCALE","2",height:31pt))
 #v(6pt)#grid(columns:(1fr,1fr,1fr,1.2fr,1fr),gutter:6pt,value("TOTAL SP","SP_TOTAL"),value("SP SPENT","SP_SPENT"),value("SP REMAINING","SP_LEFT"),value("MODULES USED / MAX","10 / 12"),value("DIE CEILING","d10"))
 #v(6pt)#grid(columns:(1fr,1fr,1fr,1fr),gutter:6pt,value("HULL: CURRENT / MAX","24 / 24"),value("EFFECTIVE SHIELD DR","2"),value("EFFECTIVE JUMP RANGE","3"),value("HANDLING","+1"))
 #band("SP SPENDING & SYSTEM CONDITION",subtitle:"Required rows are marked *. Every installed die is already paid for. Current dice start at their installed ratings.")
 #set text(size:8pt)
 #table(columns:(130pt,48pt,34pt,50pt,1fr),rows:(auto,)+(18pt,)*16,inset:4pt,stroke:.4pt+rgb("#9aaeb5"),
 table.header(..([MODULE / ID],[RATED],[SP],[CURRENT],[CAPABILITY / FAULT / TEMP]).map(c=>table.cell(fill:ivory,strong(c)))),
 ROWS)
 #band("WEAPON MOUNTS",subtitle:"This pulse mount costs 2 SP. It is one installed weapon, not a free extra system.")
 #table(columns:(1.4fr,.8fr,1.2fr,1fr),rows:(auto,20pt,20pt),inset:4pt,stroke:.4pt+rgb("#9aaeb5"),
 table.header(..([MOUNT / TYPE],[RANGE],[WEAK / STD / STRONG],[OPERATOR]).map(c=>table.cell(fill:ivory,strong(c)))),
 [Pulse / Thermal],[Close-Near],[3 / 5 / 7],[Assign crew],[],[],[],[])
 #band("CREW / STATIONS")
 #grid(columns:(1fr,1fr,1fr),gutter:6pt,value("PILOT / NAVIGATOR","Assign crew",height:32pt),value("GUNNERS / SENSORS","Assign crew",height:32pt),value("ENGINEER / COMMANDER","Assign crew",height:32pt))
 #v(7pt)#text(size:8pt)[24 starting SP - 12 SP required systems - 12 SP optional systems = 0 SP remaining. Empty rows grant no extra module positions. Fuel, parts and crew are not included in SP. Wear changes current condition without refunding spent SP.]
])
'''
    body=body.replace('SP_TOTAL',str(frame['sp'])).replace('SP_SPENT',str(spent)).replace('SP_LEFT',str(frame['sp']-spent)).replace(' ROWS)', ' '+','.join(rows)+')')
    (book/'generated/worked-scout.typ').write_text(body)

def starship(book):
    intro=book/'manuscript/01-welcome.md';rules=book/'manuscript/02-rules.md';ref=book/'manuscript/03-reference.md'
    parts=['#import "../../player-book/template.typ": *\n']
    parts += ['#chapter("1","A Ship the Crew Can Understand")\n', source(intro),
              '#illustration("ship-review-cutter",height:145pt,fit:"cover")\n',
              g.render(intro.read_text(),intro,base=1)]
    sections=re.split(r'(?=^## )',rules.read_text(),flags=re.M)
    parts += [source(rules,'ship-rule'),g.render(sections[0],rules,base=1)]
    groups=[('2','Build Your Ship',1,6),('3','Operate Your Ship',6,10),('4','FTL Preparation and Travel',10,11),('5','Example Builds',11,12)]
    for n,title,start,end in groups:
        if n=='3': parts.append('#include "worked-scout.typ"\n')
        parts.append(f'#chapter({g.q(n)},{g.q(title)})\n')
        for index,section in enumerate(sections[start:end]):
            if n == '2' and index == 1:
                pricing, ledger = section.split("### Worked SP spending ledger", 1)
                parts.append(g.render(pricing,rules,base=1))
                parts.append('#pagebreak(weak:true)\n')
                parts.append(g.render("### Worked SP spending ledger" + ledger,rules,base=1))
                continue
            if n=='5':
                profiles=re.split(r'(?=^### )',section,flags=re.M)
                parts.append(g.render(profiles[0],rules,base=1))
                for profile in profiles[1:]:parts.append('#block(breakable:false)['+g.render(profile,rules,base=1)+']\n')
            else:parts.append(g.render(section,rules,base=1))
    parts += ['#chapter("6","Reference and Ship Records")\n',source(ref),g.render(ref.read_text(),ref,base=1)]
    parts += ['#heading(level:2)[Character abilities aboard ship]\n',
              'The complete cards and purchase requirements remain in the Player\'s Book: class signatures in Chapter 4, shared abilities in Chapter 8. These are reading pointers, not substitute outcomes. Called Shot stays personal scale unless a separately authored ship ability says otherwise.\n\n']
    slugs=['read-the-drift','plot-course','emergency-jump','master-navigator','evasive-maneuver','shipboard-familiarity','sensor-sweep','field-repair','keep-it-running','jury-rig','overcharge','miracle-worker','signature-spacer-drift-pilot','signature-spacer-power-routing','signature-spacer-through-the-storm']
    rows=[]
    for slug in slugs:
        p=ROOT/'design/cards'/f'{slug}.md';g.record(p,'ability-reference')
        text=p.read_text()
        value=lambda key:re.search(r'\*\*'+re.escape(key)+r':\*\*\s*([^\n]+)',text)[1].split(' · **')[0]
        rows.append((g.name(p),value('Action'),value('Attribute'),'Player\'s Book Ch. '+('4' if slug.startswith('signature-') else '8')))
    tuple_rows='('+','.join('('+','.join('[#text('+g.q(v)+')]'  for v in row)+',)' for row in rows)+',)'
    parts.append('#rule-table(4,([Ability],[Action],[Attribute],[Full card]),'+tuple_rows+')\n')
    parts += [g.render(sections[12],rules,base=1)]
    return ''.join(parts)


def profile_body(text,p):
    pattern=r"(?m)^- \*\*Weak:\*\* (.+)\n- \*\*Standard:\*\* (.+)\n- \*\*Strong:\*\* (.+)"
    pieces=[];cursor=0
    for match in re.finditer(pattern,text):
        pieces.append(g.render(text[cursor:match.start()],p))
        rows=",".join("["+g.render("**"+label+":** "+value,p)+"]" for label,value in zip(("Weak","Standard","Strong"),match.groups()))
        pieces.append("#outcome-rows(("+rows+",))\n")
        cursor=match.end()
    pieces.append(g.render(text[cursor:],p))
    return "".join(pieces)

def expanded_profile(threat, abilities):
    """Inline canonical ability rules so the printed profile runs independently."""
    text = g.clean(threat)

    def expand(match):
        ability = abilities[match[2]]
        _, _, rules = g.clean(ability).partition("\n")
        return f"### {match[1]}\n\n{rules.strip()}\n"

    return re.sub(r"(?m)^- \[([^]]+)\]\(\.\./adversary-abilities/([^/)]+)\.md\)$", expand, text)


def adversary_library(abilities):
    parts = [
        '#pagebreak(weak:true)\n#heading(level:2)[Adversary ability library]\n',
        "Assign an ability only when the actor can meet its trigger and has the necessary "
        "body, equipment or access. The ability spends the listed action. A Reaction "
        "competes with opportunity attacks. Movement follows ordinary terrain and "
        "occupancy rules unless the ability explicitly says otherwise. The abilities "
        "are untested SA options.\n",
    ]
    for action in ("Maneuver", "Reaction", "Passive"):
        cards = []
        for ability in abilities.values():
            if f"**Action:** {action} ·" not in ability.read_text():
                continue
            _, _, rules = g.clean(ability).partition("\n")
            cards.append(f"#catalog-card({g.q(g.name(ability))},{g.q(g.key(ability))})["
                         + g.render(rules, ability) + "]")
        parts.append(f"#heading(level:3)[{action}]\n" + g.flow(cards))
    return "".join(parts)


SA_TABLE_WIDTHS = {
    "Book": "(105pt,1fr)",
    "Record": "(90pt,1fr)",
    "d6": "(25pt,1fr,1.1fr,1.1fr)",
    "Pressure": "(82pt,2.1fr,1fr)",
    "Hazard fixture": "(85pt,1fr,1.35fr,1.2fr)",
}

def companion_appendix(book):
    profiles = sorted((book / "companions").glob("*.md"), key=g.name)
    parts = [
        '#chapter("A","Drones, Sprites and Companions")\n',
        "Choose a personal-scale profile and use the command procedure in the Player's Book, "
        "Chapter 9. These prices, access gates and profiles are untested. A hired companion "
        "joins by agreement. Record the job, shift, payment, equipment and what makes them "
        "withdraw before the crew takes them into danger.\n",
    ]
    for family, title in (("Drone", "Personal drones"), ("Sprite", "Software sprites"),
                          ("Hire", "Hired companions")):
        cards = []
        for profile in profiles:
            text = profile.read_text()
            if f"**Family:** {family} ·" not in text:
                continue
            g.record(profile, "companion-profile")
            cards.append(f"#catalog-card({g.q(g.name(profile))},{g.q(g.key(profile))})["
                         + profile_body(g.clean(profile), profile) + "]")
        parts.append("#pagebreak(weak:true)\n#heading(level:2," + g.q(title) + ")\n")
        parts.append(g.flow(cards))
    return "".join(parts)


def encounter_examples(book):
    import runpy

    cv = runpy.run_path(str(book / "cv.py"))
    catalog = cv["read_catalog"](book)
    parts = ['#pagebreak(weak:true)\n#heading(level:2)[Worked encounters]\n']
    for path in sorted((book / "encounters").glob("*.md")):
        g.record(path, "worked-encounter")
        total, unrated, budget = cv["encounter_roster"](path, catalog)
        rating = f"Rated seed subtotal {total}. Comparison budget {budget}."
        if unrated:
            rating += " Unrated contribution: " + ", ".join(unrated) + "."
        parts.append("#entry(" + g.q(g.name(path)) + "," + g.q(g.key(path)) + ")\n")
        parts.append(g.render(rating + "\n\n" + path.read_text(), path, base=1))
    parts.append('#pagebreak(weak:true)\n#heading(level:2)[Provisional CV reference]\n')
    rows = [
        "| Profile | Reference attack | E | O | U | Seed CV |",
        "|---|---|---:|---:|---:|---:|",
    ]
    notes = []
    for slug, (title, attack, seed, note) in sorted(catalog.items(), key=lambda item: item[1][0]):
        profile = f"[{title}](../threats/{slug}.md)"
        if seed:
            rows.append(f"| {profile} | {attack[0]} | {float(seed.attacks_to_defeat):.2f} | "
                        f"{float(seed.damage_per_round):.2f} | {float(seed.utility):.2f} | {seed.value} |")
            if seed.utility != 1:
                notes.append(f"- **{title}:** {note}.")
        else:
            rows.append(f"| {profile} | Support profile | — | — | — | Unrated |")
    reference = "\n".join(rows + ["", "### Utility judgments", "", *notes])
    parts.append(g.render(reference, book / "encounters" / "01-berth-hold.md", base=1,
                          table_widths={"Profile": "(1.3fr,1.3fr,36pt,36pt,36pt,50pt)"}))
    return "".join(parts)


def sa(book):
    abilities = {path.stem: path for path in sorted(
        (book / "adversary-abilities").glob("*.md"), key=g.name)}
    for ability in abilities.values():
        g.files[ability.resolve()] = g.key(ability)
        g.record(ability, "adversary-ability")
    for threat in (book / "threats").glob("*.md"):
        g.files[threat.resolve()] = g.key(threat)
    parts=['#import "../../player-book/template.typ": *\n']
    parts.append('#set par(leading:.38em,spacing:.5em)\n')
    for index,p in enumerate(sorted((book/'manuscript').glob('*.md')),1):
        parts.append(f'#chapter({g.q(str(index))},{g.q(g.name(p))})\n')
        parts.append(source(p))
        if index == 1:
            parts.append('#illustration("origin-port",height:150pt,fit:"cover")\n')
        parts.append(g.render(p.read_text(),p,base=1,table_widths=SA_TABLE_WIDTHS))
        if p.name.startswith("05-"):
            parts.append(encounter_examples(book))
        if p.name.startswith('06-'):
            families = ("Crews", "Security and synthetics", "Station fauna", "Void entities", "Alien ecology", "The Slop")
            profiles = {family: [] for family in families}
            for threat in sorted((book / "threats").glob("*.md"), key=g.name):
                family = re.search(r"(?m)^\*\*Family:\*\* (.+)$", threat.read_text())[1]
                g.files[threat.resolve()] = g.key(threat)
                g.record(threat, "threat-seed")
                profiles[family].append(
                    "#catalog-card(" + g.q(g.name(threat)) + "," + g.q(g.key(threat)) + ")["
                    + profile_body(expanded_profile(threat, abilities), threat) + "]"
                )
            for family, cards in profiles.items():
                parts.append("#pagebreak(weak:true)\n#heading(level:2," + g.q(family) + ")\n")
                parts.append(g.flow(cards))
            parts.append(adversary_library(abilities))
    parts.append(companion_appendix(book))
    return ''.join(parts)

def build(kind, *, source_only=False):
    book=ROOT/'design'/kind;gen=book/'generated';gen.mkdir(exist_ok=True);out=book/'output';out.mkdir(exist_ok=True)
    # Each companion runs in a fresh process, so manifests record only its own inputs.
    if kind=='starship-manual': worked_scout_sheet(book)
    body=starship(book) if kind=='starship-manual' else sa(book)
    (gen/'body.typ').write_text(body)
    sheets='ship-sheets.typ' if kind=='starship-manual' else 'sheets.typ'
    (book/'cover.typ').write_text(cover_source(ROOT_BOOK_TITLE[kind], 'Construction · crew · combat · travel' if kind=='starship-manual' else 'Rulings · sectors · encounters · consequences','ship-review-cutter' if kind=='starship-manual' else 'frontier-crew-review'))
    (book/'book.typ').write_text(book_source(ROOT_BOOK_TITLE[kind], 'Ship rules and records live in this volume. The complete personal Legend foundation and learned character abilities remain in the Player\'s Book.' if kind=='starship-manual' else 'Prepare the next job, run scenes with clear stakes and follow the consequences of the crew’s decisions. Threat profiles and hazard values are marked for playtest review.',sheets))
    manifest={'book':kind,'title':ROOT_BOOK_TITLE[kind],'included':g.included,'links':g.links,'sheets':str((book/sheets).relative_to(ROOT)),'threats':sum(item['kind'] == 'threat-seed' for item in g.included),'status':'design-review'}
    (gen/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if source_only:
        print(f'Generated {kind} sources')
        return
    target=out/f'galaxies-of-legend-{kind}.pdf'
    subprocess.run([os.environ.get('TYPST') or shutil.which('typst'),'compile','--root',str(ROOT),'--font-path',str(PLAYER/'fonts'),str(book/'book.typ'),str(target)],check=True)
    if kind=='starship-manual':
        subprocess.run([os.environ.get('GOL_ART_PYTHON',sys.executable),str(book/'art/build-sheets.py'),str(target)],check=True)
    print(f'Built {target}')

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("book", choices=ROOT_BOOK_TITLE)
    parser.add_argument("--source-only", action="store_true")
    args = parser.parse_args()
    build(args.book, source_only=args.source_only)
