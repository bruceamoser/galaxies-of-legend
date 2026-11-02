#!/usr/bin/env python3
"""Extract the SP ledger, completed Scout Cutter sheet and matching blank sheet."""
from pathlib import Path
from pypdf import PdfReader,PdfWriter
ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'design/starship-manual/output/galaxies-of-legend-starship-manual.pdf'
r=PdfReader(source);texts=[p.extract_text() or '' for p in r.pages]
terms=['Worked SP spending ledger: Scout Cutter','WORKED BUILD / Scout Cutter','SHIP RECORD / construction']
selected=[]
for term in terms:
    pages=[i for i,t in enumerate(texts) if term in t]
    assert len(pages)==1,(term,pages)
    selected.append(pages[0])
w=PdfWriter()
for i in selected:w.add_page(r.pages[i])
w.add_metadata({'/Title':'Galaxies of Legend - Scout Cutter: Spend SP and Fill the Ship Sheet','/Author':'Bruce A. Moser'})
for i,title in enumerate(['Spend the 24 SP','Completed ship sheet','Blank construction sheet']):w.add_outline_item(title,i)
out=ROOT/'output/pdf/Galaxies-of-Legend-Scout-Cutter-SP-Worked-Build.pdf';out.parent.mkdir(parents=True,exist_ok=True)
with out.open('wb') as stream:w.write(stream)
check=PdfReader(out);assert len(check.pages)==3
for page,original in zip(check.pages,selected):assert page.extract_text()==r.pages[original].extract_text()
print(out)
