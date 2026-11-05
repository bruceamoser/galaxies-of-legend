#!/usr/bin/env python3
"""Draw fillable GOL hull sheets; one spatial box per existing module position."""
from pathlib import Path
import json,math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[3]
DATA=json.loads((ROOT/'design/ships/construction.json').read_text())
SCOUT=json.loads((ROOT/'design/ships/examples.json').read_text())[0]
OUT=ROOT/'output/pdf/Galaxies-of-Legend-Spatial-Ship-Sheets-Prototype.pdf'
W,H=792,612
INK=HexColor('#163441');BLUE=HexColor('#176f8c');PALE=HexColor('#edf2f4');LINE=HexColor('#bacbd2');RED=HexColor('#d92027')
TITLE='Helvetica-Bold'
try:
    pdfmetrics.registerFont(TTFont('GOL-Oswald',str(ROOT/'design/player-book/fonts/Oswald[wght].ttf')));TITLE='GOL-Oswald'
except Exception:pass
# (x,y) centres, forward to aft. Hull geometry is drawn to enclose the usable bays.
CONFIG={
 'launch':{'half':190,'box':108,'pts':[(396,493),(331,425),(461,425),(331,357),(461,357),(331,289),(461,289),(396,205)]},
 'light':{'half':245,'box':104,'pts':[(396,493),(339,425),(453,425)]+[(x,y) for y in [357,289,221] for x in [282,396,510]]},
 'medium':{'half':285,'box':100,'pts':[(396,493),(339,431),(453,431)]+[(x,y) for y in [363,295,227] for x in [231,341,451,561]]+[(396,159)]},
 'heavy':{'half':355,'box':100,'pts':[(396,493),(339,431),(453,431)]+[(x,y) for y in [363,295,227] for x in [121,231,341,451,561,671]]+[(396,159)]},
 'capital':{'half':368,'box':92,'pts':[(396,493),(339,437),(453,437)]+[(x,y) for y in [379,323,267] for x in [96,196,296,396,496,596,696]]+[(x,211) for x in [196,296,396,496,596]]+[(396,155)]}
}
EXPECTED={};BOUNDS=[]

def text(c,x,y,value,size=8,font='Helvetica',color=INK):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,str(value))

def path(c,pts,fill=PALE,stroke=INK,width=1):
    p=c.beginPath();p.moveTo(*pts[0])
    for x,y in pts[1:]:p.lineTo(x,y)
    p.close();c.setFillColor(fill);c.setStrokeColor(stroke);c.setLineWidth(width);c.drawPath(p,fill=1,stroke=1)

def hull(c,frame,cfg):
    h=cfg['half'];cx=396
    left=[(-58,539),(-82,524),(-132,478),(-180,446),(-h*.87,424),(-h,410),(-h,205),(-h+28,180),(-h+45,151),(-126,124),(-102,102)]
    outline=[(cx+x,y) for x,y in left]+[(cx-x,y) for x,y in reversed(left)]
    path(c,outline,width=1.6)
    # Inner armour line, split prow, maintenance seams, lateral hardpoints.
    c.setStrokeColor(LINE);c.setLineWidth(.55)
    p=c.beginPath();p.moveTo(cx-52,531)
    for x,y in left[1:]:p.lineTo(cx+x+7,y-3)
    c.drawPath(p)
    p=c.beginPath();p.moveTo(cx+52,531)
    for x,y in left[1:]:p.lineTo(cx-x-7,y-3)
    c.drawPath(p)
    for sign in [-1,1]:
        # Segmented outboard hull plates and visible radiator hatching.
        outer=cx+sign*(h-10)
        for y in [213,253,293,333,373]:
            c.line(outer,y,cx+sign*(h-32),y+12)
        for k in range(6):c.line(cx+sign*(h-22),240+k*13,cx+sign*(h-9),246+k*13)
        # Paired propulsion housings are one engine system, not free module boxes.
        ex=cx+sign*88
        path(c,[(ex-27,164),(ex-31,122),(ex-24,88),(ex+24,88),(ex+31,122),(ex+27,164)],fill=HexColor('#e2e9ed'),stroke=INK,width=.9)
        c.setFillColor(INK);c.roundRect(ex-18,91,36,12,2,fill=1,stroke=0)
        c.setStrokeColor(BLUE)
        for k in range(5):c.line(ex-14+k*7,93,ex-14+k*7,101)
        # Exterior mounts and docking fittings: unlabeled technical texture only.
        c.setStrokeColor(INK);c.setLineWidth(.8)
        if h>220:
            xx=cx+sign*(h-4)
            c.line(xx,338,xx+sign*13,349);c.line(xx+sign*13,349,xx+sign*13,370)
            c.line(xx+sign*17,347,xx+sign*17,366)
        c.line(cx+sign*55,535,cx+sign*55,543)
    # Dark bridge glass above the forward array. Its location does not add a module.
    for sign in [-1,1]:path(c,[(cx+sign*4,526),(cx+sign*39,526),(cx+sign*47,518),(cx+sign*4,520)],fill=BLUE,stroke=INK,width=.5)
    c.setStrokeColor(LINE)
    c.line(cx,518,cx,142)
    # Aft service spine and small warning marks.
    c.setFillColor(RED);c.rect(cx-17,117,34,3,fill=1,stroke=0)
    text(c,cx-25,107,'DRIVE / AFT',6,font='Helvetica-Bold',color=BLUE)

def field(c,name,x,y,w,h,value='',font=9):
    EXPECTED[name]=str(value)
    c.acroForm.textfield(name=name,tooltip=name.replace('_',' '),x=x,y=y,width=w,height=h,value=str(value),
        fontName='Helvetica',fontSize=font,textColor=INK,borderWidth=0,borderStyle='solid',fillColor=white,
        forceBorder=False,fieldFlags=0)

def box(c,prefix,index,pt,width,system=None,location='',module=None):
    x,y=pt[0]-width/2,pt[1]-25;h=50
    BOUNDS.append((prefix,index,x,y,width,h))
    required=system in DATA['required']
    c.setFillColor(white);c.setStrokeColor(BLUE if required else LINE);c.setLineWidth(1 if required else .65)
    c.roundRect(x,y,width,h,3,fill=1,stroke=1)
    c.setFillColor(BLUE if required else INK);c.roundRect(x,y+h-11,width,11,3,fill=1,stroke=0)
    c.rect(x,y+h-11,width,4,fill=1,stroke=0)
    label=f'{index:02d} '+('* REQUIRED' if required else location)
    text(c,x+4,y+h-8,label[:28],6.3,font='Helvetica-Bold',color=white)
    name=DATA['systems'][system]['name'] if required else ''
    if module:name=DATA['systems'][module['type']]['name']
    if required:text(c,x+4,y+23,name.upper(),7.4,font='Helvetica-Bold')
    else:field(c,f'{prefix}_{index:02d}_system',x+4,y+19,width-8,16,name if module else '',8.5)
    # Three compact writable values use the same coordinates on every size.
    text(c,x+4,y+7,'DIE',5.5,font='Helvetica-Bold');text(c,x+38,y+7,'NOW',5.5,font='Helvetica-Bold');text(c,x+73,y+7,'SP',5.5,font='Helvetica-Bold')
    die=module['die'] if module else ''
    cost=DATA['die_sp_cost'][die] if die else ''
    field(c,f'{prefix}_{index:02d}_rated',x+17,y+3,19,13,die,8)
    field(c,f'{prefix}_{index:02d}_current',x+53,y+3,19,13,die,8)
    field(c,f'{prefix}_{index:02d}_sp',x+83,y+3,max(7,width-87),13,cost,8)
    if prefix.endswith('worked') and not module:
        text(c,x+4,y+24,'EMPTY BAY',7.5,font='Helvetica-Bold',color=LINE)

def slots(frame):
    pts=CONFIG[frame]['pts'];n=len(pts)
    result=[{'system':None,'location':'UTILITY BAY'} for _ in pts]
    for index,system in [(0,'sensors'),(1,'navigation'),(2,'communications'),(3,'life_support')]:result[index]['system']=system
    engine=10 if frame=='light' else n-1;result[engine]['system']='engines'
    for i,(x,y) in enumerate(pts):
        if result[i]['system']:continue
        result[i]['location']=('PORT BAY' if x<360 else 'STBD BAY' if x>432 else 'CORE BAY')
        if y<250:result[i]['location']='DRIVE / UTILITY'
    return result

def page(c,frame,worked=False):
    f=DATA['frames'][frame];cfg=CONFIG[frame];prefix=frame+('_worked' if worked else '_blank')
    c.setPageSize((W,H));c.bookmarkPage(prefix);c.addOutlineEntry((f['name']+' - '+('Scout Cutter example' if worked else 'blank spatial sheet')),prefix,0)
    text(c,28,584,'GALAXIES OF LEGEND',22,font=TITLE)
    text(c,28,566,('SCOUT CUTTER / WORKED BUILD' if worked else f['name'].upper()+' / SPATIAL SHIP RECORD'),10,font='Helvetica-Bold',color=BLUE)
    c.setFont(TITLE,12);c.setFillColor(INK);c.drawRightString(764,585,f"{f['sp']} SP  /  {f['max_modules']} SYSTEM BOXES")
    c.setStrokeColor(BLUE);c.setLineWidth(.7);c.line(28,555,764,555)
    # Identity field outside the hull; current Hull and SP totals remain readable.
    text(c,28,537,'SHIP NAME',6.5,font='Helvetica-Bold');field(c,prefix+'_name',28,517,155,17,'Scout Cutter' if worked else '',10)
    text(c,610,538,f"HULL MAX {f['hull']}   HANDLING {f['handling']:+d}",8,font='Helvetica-Bold')
    text(c,610,525,f"SCALE {f['scale']}   DIE CEILING {f['max_die']}",8)
    text(c,610,510,'HULL NOW',6.5);field(c,prefix+'_hull',674,505,36,16,f['hull'] if worked else '',10)
    hull(c,frame,cfg)
    # Spatially anchor the actual Scout build to fitting positions on the Light hull.
    assigned={}
    if worked:
        modules={m['type']:m for m in SCOUT['modules']}
        for i,s in enumerate(slots(frame)):
            if s['system']:assigned[i]=modules[s['system']]
        for i,kind in [(4,'cargo'),(6,'weapons'),(7,'defences'),(9,'capacitors'),(11,'ftl')]:assigned[i]=modules[kind]
    for i,(pt,s) in enumerate(zip(cfg['pts'],slots(frame))):box(c,prefix,i+1,pt,cfg['box'],s['system'],s['location'],assigned.get(i))
    # SP accounting strip stays outside the hull, not buried in the module fields.
    c.setStrokeColor(LINE);c.line(28,75,764,75)
    text(c,28,58,'TOTAL SP',7,font='Helvetica-Bold');text(c,86,56,f['sp'],12,font='Helvetica-Bold')
    text(c,133,58,'SP SPENT',7,font='Helvetica-Bold');field(c,prefix+'_spent',194,51,35,18,f['sp'] if worked else 0,11)
    text(c,263,58,'SP LEFT',7,font='Helvetica-Bold');field(c,prefix+'_remaining',311,51,35,18,0 if worked else f['sp'],11)
    text(c,375,58,'PRICES: d4 1 / d6 2 / d8 3 / d10 4 / d12 5 SP',8,font='Helvetica-Bold',color=BLUE)
    note='Required boxes still need purchased dice. Bay locations are suggestions; the silhouette grants no equipment.'
    if worked:note='Scout: required systems 12 SP + optional systems 12 SP = 24 SP. Two bays are empty; no SP remains.'
    text(c,28,34,note,7.4)
    text(c,28,21,'DIE = installed rating. NOW = current die. Fields are fillable; SP totals are manual. Higher-die prices and frame totals remain proposals.',7)
    text(c,28,9,'SPATIAL SHEET PROTOTYPE / 2026-11-02 / Layout does not change the ship rules. Paired thrusters use one engine system.',6.4,color=BLUE)
    c.showPage()

def build():
    OUT.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
    c.setTitle('Galaxies of Legend - Spatial Ship Sheets: Five Sizes and Worked Scout')
    c.setAuthor('Bruce A. Moser')
    for frame in DATA['frames']:
        assert len(CONFIG[frame]['pts'])==DATA['frames'][frame]['max_modules']
        assert len([s for s in slots(frame) if s['system']])==5
        page(c,frame)
    page(c,'light',True);c.save()
    r=PdfReader(OUT);fields=r.get_fields();assert len(r.pages)==6
    assert set(fields)==set(EXPECTED)
    for name,value in EXPECTED.items():assert str(fields[name].get('/V',''))==value,(name,value)
    widgets=0
    for p in r.pages:
        for ref in p.get('/Annots',[]):
            item=ref.get_object()
            if item.get('/Subtype')=='/Widget':
                widgets+=1;assert item.get('/AP',{}).get('/N') is not None
                assert str(item.get('/V',''))==EXPECTED[str(item['/T'])]
    assert widgets==len(EXPECTED)
    # Boxes must not overlap one another; a spatial design should remain writable.
    for prefix in {b[0] for b in BOUNDS}:
        boxes=[b for b in BOUNDS if b[0]==prefix]
        for i,a in enumerate(boxes):
            for b in boxes[i+1:]:
                overlap=min(a[2]+a[4],b[2]+b[4])-max(a[2],b[2])>0 and min(a[3]+a[5],b[3]+b[5])-max(a[3],b[3])>0
                assert not overlap,(prefix,a[1],b[1])
    print(f'{OUT}\n6 pages; {len(fields)} validated interactive fields; module counts 8/12/16/22/30 plus worked Light.')
if __name__=='__main__':build()
