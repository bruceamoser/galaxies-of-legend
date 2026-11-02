#!/usr/bin/env python3
"""Validate proposed ship allocations. No dependencies beyond Python 3."""
import argparse, json
from collections import Counter
from pathlib import Path
ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT/'ships/construction.json').read_text())

def validate(ship):
    errors=[]
    if ship.get('frame') not in DATA['frames']:
        return {'name':ship.get('name','Unnamed'),'valid':False,'errors':['Unknown frame']}
    frame=DATA['frames'][ship['frame']]; modules=ship.get('modules',[])
    if not isinstance(modules,list):
        return {'name':ship.get('name','Unnamed'),'valid':False,'errors':['Modules must be a list']}
    counts=Counter(); ids=set(); spent=0
    for m in modules:
        if not isinstance(m,dict):
            errors.append('Each module must be an object');continue
        ident=m.get('id');kind=m.get('type');die=m.get('die')
        if not isinstance(ident,str) or not ident or ident in ids: errors.append('Every module needs a unique non-empty id')
        if isinstance(ident,str):ids.add(ident)
        if kind not in DATA['systems']:errors.append(f'{ident}: unknown system {kind}');continue
        counts[kind]+=1
        if die not in DATA['die_cost']:errors.append(f'{ident}: invalid die {die}');continue
        spent+=DATA['die_cost'][die]
        if DATA['die_cost'][die]>DATA['die_cost'][frame['max_die']]:errors.append(f'{ident}: exceeds frame die ceiling')
        if kind=='hangar' and DATA['performance']['hangar_launches'][die]==0:errors.append(f'{ident}: hangar requires at least d6')
        if kind=='hangar' and frame['scale']<4:errors.append(f'{ident}: hangar requires medium frame or larger')
    for kind in DATA['required']:
        if counts[kind]!=1:errors.append(f'Required system {kind} must occur exactly once')
    for kind,count in counts.items():
        if count>1 and not DATA['systems'][kind]['repeatable']:errors.append(f'{kind}: not repeatable')
    if bool(counts['ftl'])!=bool(counts['capacitors']):errors.append('FTL drive and jump capacitors must be installed together')
    if counts['targeting'] and not counts['weapons']:errors.append('Targeting requires a weapon mount')
    if len(modules)>frame['max_modules']:errors.append('Module limit exceeded')
    if spent>frame['budget']:errors.append('Allocation budget exceeded')
    return {'name':ship.get('name','Unnamed'),'frame':ship['frame'],'valid':not errors,'spent':spent,'budget':frame['budget'],'unspent':frame['budget']-spent,'modules':len(modules),'hull':frame['hull'],'handling':frame['handling'],'errors':errors}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',nargs='?',type=Path,default=ROOT/'ships/examples.json',help='JSON ship or list of ships; default: sample builds')
    a=p.parse_args();ships=json.loads(a.file.read_text());ships=ships if isinstance(ships,list) else [ships]
    results=[validate(s) for s in ships]
    print(json.dumps(results,indent=2));return 0 if all(r['valid'] for r in results) else 1
if __name__=='__main__':raise SystemExit(main())
