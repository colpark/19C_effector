#!/usr/bin/env python3
"""Freeze an unselected SCOP/PDBe PDB pool before ESMFold confidence is observed."""
from __future__ import annotations
import concurrent.futures, csv, hashlib, json, os, shutil, subprocess, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEED='item58-scop-pool-v1'; DRAW=240
def get_json(url):
 with urllib.request.urlopen(url,timeout=30) as h:return json.load(h)
def one(pdb):
 p=pdb.lower()
 try:
  scop=get_json(f'https://www.ebi.ac.uk/pdbe/api/mappings/scop/{p}').get(p,{}).get('SCOP',{})
  e=get_json(f'https://data.rcsb.org/rest/v1/core/polymer_entity/{p}/1')
  seq=e['entity_poly']['pdbx_seq_one_letter_code_can'].replace('\n','').replace(' ','')
  if not scop:return {'pdb_id':pdb,'status':'no_scop_mapping'}
  return {'pdb_id':pdb,'status':'mapped','scop_sunid':sorted(scop)[0],'scop_mappings':sorted(scop), 'sequence':seq,'length':len(seq)}
 except Exception as x:return {'pdb_id':pdb,'status':'fetch_error','error':str(x)}
def main():
 ids=get_json('https://data.rcsb.org/rest/v1/holdings/current/entry_ids')
 draw=sorted(ids,key=lambda x:hashlib.sha256((SEED+x).encode()).hexdigest())[:DRAW]
 with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex: rows=list(ex.map(one,draw))
 mapped=[r for r in rows if r['status']=='mapped']
 # No confidence, fold type or size filter occurred before this point. The carded
 # inference contract is recorded separately for sequences it cannot accept.
 mmseqs=os.environ.get('MMSEQS_BINARY') or shutil.which('mmseqs')
 if not mmseqs: raise RuntimeError('set MMSEQS_BINARY to the pinned MMseqs2 executable')
 query=ROOT/'build/scop_pool.fasta';query.parent.mkdir(exist_ok=True)
 query.write_text(''.join(f'>{r["pdb_id"]}\n{r["sequence"]}\n' for r in mapped))
 result=ROOT/'build/scop_pool_mmseqs.tsv';tmp=ROOT/'build/mmseqs_scop_pool'
 subprocess.run([mmseqs,'easy-search',str(query),str(ROOT/'data/positives/union.fasta'),str(result),str(tmp),'--min-seq-id','0.3','-c','0.8','--cov-mode','0','--format-output','query,target,pident,alnlen'],check=True)
 hits={}
 if result.exists():
  for line in result.read_text().splitlines():
   q,t,p,a=line.split('\t');hits[q.upper()]=(float(p),t,int(a))
 retained=[];removed=[]
 for r in mapped:
  p,t,a=hits.get(r['pdb_id'],(0.,'',0));r.update(maximum_mmseqs_identity_to_cohort=p,closest_cohort_accession=t,aligned_residues=a)
  (removed if p>.3 else retained).append(r)
 fields=['pdb_id','status','scop_sunid','scop_mappings','sequence','length','maximum_mmseqs_identity_to_cohort','closest_cohort_accession','aligned_residues']
 for path,data in [(ROOT/'data/measurements/scop_pool_retained.tsv',retained),(ROOT/'data/measurements/scop_pool_removed.tsv',removed)]:
  with path.open('w',newline='') as h:w=csv.DictWriter(h,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(data)
 (ROOT/'data/measurements/scop_pool_draw.json').write_text(json.dumps({'seed':SEED,'draw_size':DRAW,'draw':draw,'all_results':rows},indent=2)+'\n')
 print(json.dumps({'draw_size':DRAW,'mapped':len(mapped),'retained':len(retained),'removed':len(removed),'families':len({r['scop_sunid'] for r in retained})}))
if __name__=='__main__':main()
