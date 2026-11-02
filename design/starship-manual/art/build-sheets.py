#!/usr/bin/env python3
"""Typeset interactive system fields over generated raster hull artwork."""
import json, sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[3]
ART = Path(__file__).resolve().parent
DATA = json.loads((ROOT/'design/ships/construction.json').read_text())
SCOUT = json.loads((ROOT/'design/ships/examples.json').read_text())[0]
LAYOUT = json.loads((ART/'panels.json').read_text())
OUT = ROOT/'output/pdf/Galaxies-of-Legend-Painted-Ship-Sheets.pdf'
INK = HexColor('#163441')
EXPECTED = {}

def text(c,x,y,s,size=8,bold=False):
    c.setFillColor(INK); c.setFont('Helvetica-Bold' if bold else 'Helvetica',size)
    c.drawString(x,y,str(s))

def field(c,name,x,y,w,h,value='',size=8):
    EXPECTED[name] = str(value)
    c.acroForm.textfield(name=name,tooltip=name.replace('_',' '),x=x,y=y,width=w,height=h,
        value=str(value),fontName='Helvetica',fontSize=size,textColor=INK,fillColor=white,
        borderWidth=0,forceBorder=False)

def page(c,key,worked=False):
    cfg=LAYOUT[key]; f=DATA['frames'][key]; prefix=key+('_worked' if worked else '_blank')
    width=1224 if key in ('heavy','capital') else 612
    c.setPageSize((width,792))
    title='SCOUT CUTTER / COMPLETED BUILD' if worked else f['name'].upper()
    c.bookmarkPage(prefix); c.addOutlineEntry(title,prefix)
    # Scale the original PNG without modifying it; coordinates are image pixels.
    scale=min((width-52)/cfg['hull_width'],618/1024)
    ox=width/2-768*scale; oy=88+(618-1024*scale)/2
    c.drawImage(str(ART/cfg['image']),ox,oy,width=1536*scale,height=1024*scale)
    text(c,24,766,'GALAXIES OF LEGEND',19,True)
    text(c,24,748,title,11,True)
    text(c,24,731,f"{f['sp']} SP | {f['max_modules']} module positions | Die ceiling {f['max_die']} | Scale {f['scale']}",9)
    text(c,24,713,'SHIP',7,True);field(c,prefix+'_name',48,709,190,14,'Scout Cutter' if worked else '',9)
    text(c,265,713,f"HULL MAX {f['hull']}  / NOW",7,True)
    field(c,prefix+'_hull',365,709,30,14,f['hull'] if worked else '',9)
    text(c,425,713,f"HANDLING {f['handling']:+d}",8,True)
    assigned={}; required={0:'sensors',1:'navigation',2:'communications',3:'life_support',cfg['engine']:'engines'}
    if worked:
        modules={m['type']:m for m in SCOUT['modules']}
        assigned={i:modules[k] for i,k in required.items()}
        assigned.update({i:modules[k] for i,k in [(4,'cargo'),(6,'weapons'),(7,'defences'),(9,'capacitors'),(11,'ftl')]})
    short={'sensors':'SENSORS','navigation':'NAVIGATION','communications':'COMMS','life_support':'LIFE SUPPORT','engines':'ENGINES'}
    for i,(x1,y1,x2,y2) in enumerate(cfg['panels']):
        x=ox+x1*scale; y=oy+(1024-y2)*scale; w=(x2-x1)*scale; h=(y2-y1)*scale
        assert w>=42 and h>=21,(key,i,w,h)
        module=assigned.get(i); req=required.get(i)
        compact=h<34
        text(c,x+2,y+h-8,f'{i+1:02d} '+(('* '+short[req]) if req else ('' if compact else 'OPTIONAL')),min(6.5,w/11),True)
        if not req:
            names={'cargo':'Cargo','weapons':'Weapon','defences':'Shields','capacitors':'Capacitors','ftl':'FTL drive'}
            name=names[module['type']] if module else ''
            if compact:field(c,f'{prefix}_{i}_system',x+13,y+h-10,w-15,9,name,6)
            else:field(c,f'{prefix}_{i}_system',x+2,y+16,w-4,h-26,name,7)
        die=module['die'] if module else '';sp=DATA['die_sp_cost'][die] if die else ''
        # Three evenly divided columns; values sit below labels.
        for j,(label,suffix,value) in enumerate([('DIE','rated',die),('NOW','current',die),('SP','sp',sp)]):
            cell=w/3; xx=x+j*cell
            text(c,xx+1,y+(3 if compact else 10),label,4 if compact else 5,True)
            field(c,f'{prefix}_{i}_{suffix}',xx+(8 if compact else 1),y+1,cell-(9 if compact else 2),9,value,6 if compact else 7)
    text(c,24,72,'TOTAL SP',7,True);text(c,80,71,f['sp'],11,True)
    text(c,123,72,'SP SPENT',7,True);field(c,prefix+'_spent',182,67,28,17,f['sp'] if worked else 0,10)
    text(c,233,72,'SP REMAINING',7,True);field(c,prefix+'_remaining',320,67,28,17,0 if worked else f['sp'],10)
    text(c,373,72,'d4:1 / d6:2 / d8:3 / d10:4 / d12:5 SP',8,True)
    text(c,24,52,'* Required systems must be purchased. One box = one module position. Locations are suggestions.',7.5)
    text(c,24,39,'DIE: installed rating. NOW: current die. SP: purchase cost. Totals are manual. Multiple thrusters share one engine system.',7)
    text(c,24,26,'Scout: 12 SP required + 12 SP optional = 24 SP; two unused bays, zero SP left.' if worked else 'Record detailed capabilities, weapon mounts, crew and temporary faults on the companion operations / ledger sheets.',7)
    text(c,24,13,'Starter Kit v0.1.0 | Design review | Frame budgets and new ship values are untested proposals.',7)
    c.showPage()

def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUT),pagesize=(612,792),pageCompression=1)
    c.setTitle('Galaxies of Legend - Painted Ship Sheets');c.setAuthor('Bruce A. Moser')
    for key,f in DATA['frames'].items():
        assert len(LAYOUT[key]['panels'])==f['max_modules']
        page(c,key)
    page(c,'light',True);c.save()
    r=PdfReader(OUT); fields=r.get_fields();assert len(r.pages)==6
    assert set(fields)==set(EXPECTED)
    for k,v in EXPECTED.items():assert str(fields[k].get('/V',''))==v
    widgets=0
    for p in r.pages:
        for ref in p.get('/Annots',[]):
            a=ref.get_object()
            if a.get('/Subtype')=='/Widget':
                widgets+=1;assert str(a.get('/V',''))==EXPECTED[str(a['/T'])]
                assert a.get('/AP',{}).get('/N') is not None
    assert widgets==len(EXPECTED)
    print(f'{OUT}: six pages, {widgets} verified interactive fields')

def append_to_manual(path):
    r=PdfReader(path);w=PdfWriter();w.clone_document_from_reader(r)
    w.merge(len(r.pages)-1,OUT,import_outline=True)
    temp=path.with_suffix('.painted.tmp.pdf')
    with temp.open('wb') as stream:w.write(stream)
    check=PdfReader(temp)
    assert len(check.pages)==len(r.pages)+6
    fields=check.get_fields();assert set(fields)==set(EXPECTED)
    for k,v in EXPECTED.items():assert str(fields[k].get('/V',''))==v
    temp.replace(path)
    print(f'Integrated painted ship records into {path}')

if __name__=='__main__':
    build()
    if len(sys.argv)>1:append_to_manual(Path(sys.argv[1]))
