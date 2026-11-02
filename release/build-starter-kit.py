#!/usr/bin/env python3
"""Build, verify and package the three-book Galaxies of Legend review Starter Kit."""
import argparse,hashlib,itertools,json,os,re,shutil,subprocess,sys,zipfile
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
BOOKS=[
 ('player','Player\'s Book','design/player-book/output/galaxies-of-legend-players-book.pdf','Galaxies-of-Legend-Players-Book.pdf'),
 ('starship','Starship Manual','design/starship-manual/output/galaxies-of-legend-starship-manual.pdf','Galaxies-of-Legend-Starship-Manual.pdf'),
 ('sa','Sector Architect\'s Book','design/sa-book/output/galaxies-of-legend-sa-book.pdf','Galaxies-of-Legend-Sector-Architects-Book.pdf')]
sha=lambda data:hashlib.sha256(data).hexdigest()

def run(args):subprocess.run(args,cwd=ROOT,check=True)
def verify_books():
    result=[];texts={}
    for ident,title,source,name in BOOKS:
        p=ROOT/source;r=PdfReader(p);pages=[page.extract_text() or '' for page in r.pages]
        assert len(pages)>5,(title,'Unexpectedly short')
        assert title.replace('’',"'") in r.metadata.title.replace('’',"'"),(title,r.metadata.title)
        texts[ident]=pages
        result.append({'id':ident,'title':title,'file':'books/'+name,'pages':len(pages),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size})
    player='\n'.join(texts['player']);ship='\n'.join(texts['starship']);sa='\n'.join(texts['sa'])
    assert 'Using the Starship Manual' in player
    assert '1. Choose a frame' not in player
    assert 'SHIP RECORD / construction' not in player and 'SHIP OPERATIONS / preparation' not in player
    for term in ['WORKED BUILD / Scout Cutter','SP SPENT','SP REMAINING','Build Your Ship','Operate Your Ship','FTL Preparation and Travel','Scout Cutter','Free Trader','System Shuttle','SHIP RECORD / construction','SHIP OPERATIONS / preparation']:
        assert term in ship,('Missing from Starship Manual',term)
    for p in (ROOT/'design/sa-book/threats').glob('*.md'):
        title=p.read_text().splitlines()[0][2:];assert title in sa,('Missing threat',title)
    for title in ['Sector record','Scene preparation','Encounter roster','Session and design review']:assert title in sa
    expected={''.join(map(str,t)) for t in itertools.combinations_with_replacement(range(1,7),3)}
    families=['Physical','Elemental','Mental','Radiant','Life/Necrotic'];starts=[]
    for family in families:
        starts.append(next(i for i,t in enumerate(texts['player']) if re.search(r'(?m)^'+re.escape(family)+r'\s*$',t)))
    harm_end=next(i for i,t in enumerate(texts['player']) if 'CHAPTER 8' in t)
    for family,a,b in zip(families,starts,starts[1:]+[harm_end]):
        found=set(re.findall(r'(?m)^([1-6]{3})\b','\n'.join(texts['player'][a:b])))
        assert found==expected,('Incomplete wound family',family,expected-found)
    for i,t in enumerate(texts['player']):
        if 'Discipline costs by class -' in t:
            rows=[line for line in t.splitlines() if re.search(r'\d/\d/\d',line)]
            assert len(rows)==18,('Cost matrix row count',i+1)
            for row in rows:assert len(re.findall(r'\b[1-4]/[2468]/(?:4|8|12|16)\b',row))==5,('Cost matrix columns',row)
    return result

def package(books):
    version=json.loads((ROOT/'release/version.json').read_text())
    dest=ROOT/'output/starter-kit'/('v'+version['version']+'-review');(dest/'books').mkdir(parents=True,exist_ok=True)
    for ident,title,source,name in BOOKS:shutil.copy2(ROOT/source,dest/'books'/name)
    shutil.copy2(ROOT/'release/starter-kit-readme.md',dest/'README.md')
    shutil.copy2(ROOT/'release/starter-kit-notes.md',dest/'RELEASE-NOTES.md')
    # Reproducible source snapshot includes tracked and authorised new source files,
    # never .git, ignored render files, PDFs or output archives.
    tracked=subprocess.run(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT,capture_output=True)
    if tracked.returncode==0:
        listing=tracked.stdout.decode().split('\0')
        listing=sorted({p for p in listing if p and (ROOT/p).is_file()})
    else:
        excluded={'.git','.venv','__pycache__','generated','output','tmp','dist','tools'}
        listing=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and not any(part in excluded for part in p.relative_to(ROOT).parts))
    example_source=ROOT/'output/pdf/Galaxies-of-Legend-Scout-Cutter-SP-Worked-Build.pdf'
    (dest/'examples').mkdir(exist_ok=True)
    example=dest/'examples'/example_source.name
    shutil.copy2(example_source,example)
    source_zip=dest/'Galaxies-of-Legend-Source.zip'
    with zipfile.ZipFile(source_zip,'w',zipfile.ZIP_DEFLATED) as archive:
        for relative in listing:archive.write(ROOT/relative,relative)
    with zipfile.ZipFile(source_zip) as archive:assert archive.testzip() is None
    head=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True)
    source_head=head.stdout.strip() if head.returncode==0 else None
    dirty=bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()) if source_head else None
    manifest={'product':'Galaxies of Legend Starter Kit','version':version['version'],'date':version['date'],'status':version['status'],
              'review_revision':version.get('review_revision','initial'),'books':books,'source_commit':source_head,'source_has_uncommitted_changes':dirty,
              'worked_example':{'file':str(example.relative_to(dest)),'pages':3,'sha256':sha(example.read_bytes())},
              'source_archive':{'file':source_zip.name,'sha256':sha(source_zip.read_bytes()),'files':len(listing)},
              'checks':['catalog and source links','31 source/ship/book-boundary regression tests','three independent Typst builds','all 280 wound codes present','correct book ownership','18x5 cost tables','8 threat profiles and 4 SA worksheets','ZIP integrity and SHA-256'],
              'limits':['ancestries incomplete','new ship/SA values untested','encounter CV uncalibrated','no starter mission','local design review; no public publication']}
    (dest/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    payload=[dest/'README.md',dest/'RELEASE-NOTES.md',dest/'MANIFEST.json',source_zip,example]+[dest/b['file'] for b in books]
    checksums=''.join(sha(p.read_bytes())+'  '+str(p.relative_to(dest))+'\n' for p in sorted(payload))
    (dest/'SHA256SUMS').write_text(checksums)
    kit=dest.parent/('Galaxies-of-Legend-Starter-Kit-v'+version['version']+'-review'+('-'+version['review_revision'] if version.get('review_revision') else '')+'.zip')
    with zipfile.ZipFile(kit,'w',zipfile.ZIP_DEFLATED) as archive:
        for p in payload+[dest/'SHA256SUMS']:archive.write(p,p.relative_to(dest))
    with zipfile.ZipFile(kit) as archive:
        assert archive.testzip() is None
        for book in books:assert sha(archive.read(book['file']))==book['sha256']
        for line in checksums.splitlines():
            digest,name=line.split('  ',1);assert sha(archive.read(name))==digest,name
    print(json.dumps({'kit':str(kit),'bytes':kit.stat().st_size,'sha256':sha(kit.read_bytes()),'books':books},indent=2))

def main():
    args=argparse.ArgumentParser(description=__doc__);args.add_argument('--books-only',action='store_true');args=args.parse_args()
    py=os.environ.get('GOL_BUILD_PYTHON',sys.executable)
    run([py,'design/index.py']);run([py,'design/audit.py']);run([py,'-m','unittest','discover','-s','design','-p','test_*.py'])
    run([py,'design/player-book/build.py','--compile'])
    run([py,'design/publishing/build_companions.py','starship-manual'])
    run([py,'design/publishing/build_companions.py','sa-book'])
    books=verify_books();run([sys.executable,'release/export-worked-ship.py']);print('Three-book content checks passed: '+', '.join(b['title']+' '+str(b['pages'])+' pages' for b in books))
    if not args.books_only:package(books)
if __name__=='__main__':main()
