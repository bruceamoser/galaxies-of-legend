#!/usr/bin/env python3
"""Package the full HOL restoration and a focused, self-contained reading excerpt."""
from pathlib import Path
import re,shutil,itertools
from pypdf import PdfReader,PdfWriter
root=Path(__file__).resolve().parents[1]
source=root/'design/player-book/output/galaxies-of-legend-players-book.pdf'
out=root/'output/pdf';out.mkdir(parents=True,exist_ok=True)
r=PdfReader(source);texts=[p.extract_text() or '' for p in r.pages]
start=next(i for i,t in enumerate(texts) if 'CHAPTER 7' in t and 'Harm and Recovery' in t)
end=next(i for i,t in enumerate(texts[start+1:],start+1) if 'CHAPTER 8' in t)
names=['Stabilize','Administer a Medical Dose','One More Dawn','Treat Soft Tissue','Treat Bone','Treat Mental Trauma','Treat Elemental Injury','Treat Radiant Injury','Treat Life Injury','Patch Wounds','Field Triage','Combat Medic','Triage','Field Surgery','Last Light']
care=[]
for name in names:
    pattern=r'(?m)^[U137]\s+'+r'\s+'.join(map(re.escape,name.split()))+r'\s*$'
    pages=[i for i,t in enumerate(texts) if re.search(pattern,t)]
    assert len(pages)==1,(name,pages)
    care.extend(pages)
supplies=[i for i,t in enumerate(texts) if re.search(r'(?m)^(Basic|Greater|Superior) Medical Dose\s*$',t)]
assert supplies
refs=next(i for i,t in enumerate(texts) if 'CHAPTER 11' in t and 'Table References' in t)
sheet_start=next(i for i,t in enumerate(texts) if 'Hero & encounter' in t)
sheets=[i for i,t in enumerate(texts) if 'Hero & encounter' in t or 'Belongings & scars' in t]
assert len(sheets)==2
selected=list(range(start,end))+sorted(set(care+supplies))+list(range(refs,sheet_start))+sheets
assert len(selected)==len(set(selected))
w=PdfWriter()
for i in selected:w.add_page(r.pages[i])
w.add_metadata({'/Title':'Galaxies of Legend - Complete HOL Harm and Healing Review','/Author':'Bruce A. Moser','/Subject':'Full inherited damage, Grit, wounds, all 280 wound entries and healing - revision 3'})
w.add_outline_item('Full harm, damage, healing and wound reference',0)
w.add_outline_item('Treatment and care abilities; medical supplies',end-start)
w.add_outline_item('Quick references and corrected sheets',len(selected)-((sheet_start-refs)+len(sheets)))
focused=out/'Galaxies-of-Legend-Harm-and-Healing-Review-r3-2026-11-02.pdf'
with focused.open('wb') as f:w.write(f)
full=out/'Galaxies-of-Legend-Players-Book-Review-r3-2026-11-02.pdf';shutil.copy2(source,full)
check=PdfReader(focused);assert len(check.pages)==len(selected)
for page,i in zip(check.pages,selected):assert page.extract_text()==r.pages[i].extract_text()
# PDF completeness gate: every sorted wound code appears within each printed family.
family_starts=[]
for family in ['Physical','Elemental','Mental','Radiant','Life/Necrotic']:
    family_starts.append(next(i for i in range(start,end) if re.search(r'(?m)^'+re.escape(family)+r'\s*$',texts[i])))
expected={''.join(map(str,t)) for t in itertools.combinations_with_replacement(range(1,7),3)}
for family,a,b in zip(['Physical','Elemental','Mental','Radiant','Life/Necrotic'],family_starts,family_starts[1:]+[end]):
    found=set(re.findall(r'(?m)^([1-6]{3})\b','\n'.join(texts[a:b])))
    assert found==expected,(family,expected-found)
print(f'Full book: {len(r.pages)} pages; Chapter 7: {start+1}-{end}; focused review: {len(check.pages)} pages.')
print('All five families contain all 56 wound codes in the exported PDF; source rows pass the HOL digest check.')
print(full);print(focused)
