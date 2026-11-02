#!/usr/bin/env python3
"""Package a compiled reading proof and a ship-only excerpt without hard-coded page numbers."""
from pathlib import Path
import shutil
from pypdf import PdfReader, PdfWriter

root = Path(__file__).resolve().parents[1]
source = root / 'design/player-book/output/galaxies-of-legend-players-book.pdf'
out = root / 'output/pdf'
out.mkdir(parents=True, exist_ok=True)
reader = PdfReader(source)
texts = [(p.extract_text() or '') for p in reader.pages]
start = next(i for i, t in enumerate(texts) if 'CHAPTER 10' in t and ('Starships and FTL' in t or 'Starships: build and operate' in t))
end = next(i for i, t in enumerate(texts[start+1:], start+1) if 'CHAPTER 11' in t)
sheets = [i for i, t in enumerate(texts) if ('SHIP RECORD / condition' in t or 'SHIP RECORD / construction' in t) or 'SHIP OPERATIONS / preparation' in t]
assert len(sheets) == 2, f'Expected two ship sheets, found {sheets}'
writer = PdfWriter()
for i in list(range(start, end)) + sheets:
    writer.add_page(reader.pages[i])
writer.add_metadata({'/Title': 'Galaxies of Legend - Ship Systems Reading Review', '/Author': 'Bruce A. Moser', '/Subject': 'Proposed ship mechanics and printable ship record - 2026-11-02'})
writer.add_outline_item('Proposed ship mechanics', 0)
writer.add_outline_item('Ship record and operations sheets', end-start)
ship = out / 'Galaxies-of-Legend-Ship-Review-r2-2026-11-02.pdf'
with ship.open('wb') as stream:
    writer.write(stream)
full = out / 'Galaxies-of-Legend-Players-Book-Review-r2-2026-11-02.pdf'
shutil.copy2(source, full)
# Verify the excerpt preserved every chapter and sheet's text.
extracted = PdfReader(ship)
assert len(extracted.pages) == end-start+2
for page, original in zip(extracted.pages, list(range(start, end))+sheets):
    assert page.extract_text() == reader.pages[original].extract_text()
print(f'Full book: {len(reader.pages)} pages. Ship rules: book pages {start+1}-{end}. Ship sheets: {[i+1 for i in sheets]}. Excerpt: {len(extracted.pages)} pages.')
print(full)
print(ship)
