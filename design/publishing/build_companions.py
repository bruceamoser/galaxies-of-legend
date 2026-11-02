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
    return f'''#set page(width:612pt,height:792pt,margin:0pt,fill:rgb("#0a1018"),header:none,footer:none)
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
#v(12pt)#text(size:9pt)[Version #release.version · #release.date. Companion volumes: Player's Book, Starship Manual and Sector Architect's Book. Ancestries remain placeholders; new ship and SA numbers are untested proposals.]
#v(10pt)#text(size:8.5pt)[Manuscript and layout prepared with Codex under Bruce's direction. Existing generated review illustrations are reused; font licenses and artwork notes are included in the source archive.]
#pagebreak()#outline(title:[Contents],depth:1)#pagebreak()
#include "generated/body.typ"
#include "{sheets}"
#pagebreak(weak:true)
#align(center+horizon)[
 #text(font:"Oswald",size:24pt,fill:space)[Galaxies of Legend]
 #v(10pt)#text(font:"Oswald",size:16pt,fill:teal)[{title}]
 #v(10pt)#text(size:10pt)[Starter Kit v#release.version · Design Review]
]
'''

def source(p,kind='chapter'):
    g.files[p.resolve()]=g.key(p);g.record(p,kind)
    return f'#metadata({g.q(g.key(p))})<{g.key(p)}>\n'

def starship(book):
    intro=book/'manuscript/01-welcome.md';rules=book/'manuscript/02-rules.md';ref=book/'manuscript/03-reference.md'
    parts=['#import "../../player-book/template.typ": *\n']
    parts += ['#chapter("1","A Ship the Crew Can Understand")\n',source(intro),g.render(intro.read_text(),intro,base=1)]
    sections=re.split(r'(?=^## )',rules.read_text(),flags=re.M)
    parts += [source(rules,'ship-rule'),g.render(sections[0],rules,base=1)]
    groups=[('2','Build Your Ship',1,6),('3','Operate Your Ship',6,10),('4','FTL Preparation and Travel',10,11),('5','Example Builds',11,12)]
    for n,title,start,end in groups:
        parts.append(f'#chapter({g.q(n)},{g.q(title)})\n')
        for index,section in enumerate(sections[start:end]):
            if index:parts.append('#pagebreak(weak:true)\n')
            if n=='5':
                profiles=re.split(r'(?=^### )',section,flags=re.M)
                parts.append(g.render(profiles[0],rules,base=1))
                for profile in profiles[1:]:parts.append('#block(breakable:false)['+g.render(profile,rules,base=1)+']\n')
            else:parts.append(g.render(section,rules,base=1))
    parts += ['#chapter("6","Reference and Ship Records")\n',source(ref),g.render(ref.read_text(),ref,base=1)]
    parts += ['#pagebreak(weak:true)\n#heading(level:2)[Character abilities aboard ship]\n',
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
    parts += ['#pagebreak(weak:true)\n',g.render(sections[12],rules,base=1)]
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

def sa(book):
    parts=['#import "../../player-book/template.typ": *\n']
    for index,p in enumerate(sorted((book/'manuscript').glob('*.md')),1):
        parts.append(f'#chapter({g.q(str(index))},{g.q(g.name(p))})\n')
        parts += [source(p),g.render(p.read_text(),p,base=1)]
        if p.name.startswith('06-'):
            profiles=[]
            for threat in sorted((book/'threats').glob('*.md')):
                g.files[threat.resolve()]=g.key(threat);g.record(threat,'threat-seed')
                profiles.append('#catalog-card('+g.q(g.name(threat))+','+g.q(g.key(threat))+')['+profile_body(g.clean(threat),threat)+']\n')
            parts.append('#pagebreak(weak:true)\n'+g.flow(profiles))
    return ''.join(parts)

def build(kind):
    book=ROOT/'design'/kind;gen=book/'generated';gen.mkdir(exist_ok=True);out=book/'output';out.mkdir(exist_ok=True)
    # Each companion runs in a fresh process, so manifests record only its own inputs.
    body=starship(book) if kind=='starship-manual' else sa(book)
    (gen/'body.typ').write_text(body)
    sheets='ship-sheets.typ' if kind=='starship-manual' else 'sheets.typ'
    (book/'cover.typ').write_text(cover_source(ROOT_BOOK_TITLE[kind], 'Construction · crew · combat · travel' if kind=='starship-manual' else 'Rulings · sectors · encounters · consequences','ship-review-cutter' if kind=='starship-manual' else 'frontier-crew-review'))
    (book/'book.typ').write_text(book_source(ROOT_BOOK_TITLE[kind], 'Ship rules and records live in this volume. The complete personal Legend foundation and learned character abilities remain in the Player\'s Book.' if kind=='starship-manual' else 'A base SA book for preparing and adjudicating a lived-in frontier. Threat profiles, hazard values and encounter guidance are authoring seeds, not calibrated encounters.',sheets))
    manifest={'book':kind,'title':ROOT_BOOK_TITLE[kind],'included':g.included,'links':g.links,'sheets':str((book/sheets).relative_to(ROOT)),'threats':8 if kind=='sa-book' else 0,'status':'design-review'}
    (gen/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    target=out/f'galaxies-of-legend-{kind}.pdf'
    subprocess.run([os.environ.get('TYPST') or shutil.which('typst'),'compile','--root',str(ROOT),'--font-path',str(PLAYER/'fonts'),str(book/'book.typ'),str(target)],check=True)
    print(f'Built {target}')

if __name__=='__main__':
    if len(sys.argv)!=2 or sys.argv[1] not in ROOT_BOOK_TITLE:raise SystemExit('Usage: build_companions.py starship-manual|sa-book')
    build(sys.argv[1])
