#!/usr/bin/env python3
"""Predict a frozen SCOP pool without confidence-based preselection."""
from __future__ import annotations
import csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'2_19C_biology/benchmark-mcp'))
import esmfold_worker as sibling
import torch
from transformers import EsmForProteinFolding
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'data/raw/scop_natural_pool';out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(open(ROOT/'data/measurements/scop_pool_retained.tsv'),delimiter='\t'));eligible=[];unsupported=[]
for r in rows:
 bad=set(r['sequence'])-sibling.AA
 if int(r['length'])>600 or bad: unsupported.append({**r,'reason':'>600' if int(r['length'])>600 else 'noncanonical:'+''.join(sorted(bad))})
 else:eligible.append(r)
result=[];pending=[]
for r in eligible:
 p=out/(r['pdb_id']+'.pdb')
 if p.exists():
  ca=[float(x[60:66]) for x in p.read_text().splitlines() if x.startswith('ATOM') and x[12:16].strip()=='CA']
  if len(ca)==len(r['sequence']): result.append({**r,'mean_plddt':sum(ca)/len(ca),'pdb_path':str(p)});continue
 pending.append(r)
if pending:
 if not torch.cuda.is_available():raise RuntimeError('CUDA unavailable')
 torch.manual_seed(0);model=EsmForProteinFolding.from_pretrained(sibling.MODEL,revision=sibling.REVISION,local_files_only=True).eval().cuda();model.esm=model.esm.half();model.trunk.set_chunk_size(64)
 for r in pending:
  with torch.inference_mode():pdb=model.infer_pdb(r['sequence'])
  p=out/(r['pdb_id']+'.pdb');p.write_text(pdb);ca=[float(x[60:66]) for x in pdb.splitlines() if x.startswith('ATOM') and x[12:16].strip()=='CA']
  if len(ca)!=len(r['sequence']):raise RuntimeError(r['pdb_id'])
  result.append({**r,'mean_plddt':sum(ca)/len(ca),'pdb_path':str(p)})
  (out/'manifest.json').write_text(json.dumps(result,indent=2)+'\n')
(out/'unsupported.json').write_text(json.dumps(unsupported,indent=2)+'\n')
print(json.dumps({'pool_retained':len(rows),'eligible':len(eligible),'unsupported':len(unsupported),'completed':len(result),'pending':len(pending)}))
