#!/usr/bin/env python3
"""Run the carded local ESMFold once for calibration variants, resumably."""
from __future__ import annotations
import csv,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'2_19C_biology/benchmark-mcp'))
import esmfold_worker as sibling
import torch
from transformers import EsmForProteinFolding
ROOT=Path(__file__).resolve().parents[1]; out=ROOT/'data/raw/false_singleton_calibration/predicted';out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(open(ROOT/'data/measurements/false_singleton_variants.tsv'),delimiter='\t')); result=[];pending=[]
for r in rows:
 p=out/(r['variant_id']+'.pdb')
 if p.exists():
  ca=[float(x[60:66]) for x in p.read_text().splitlines() if x.startswith('ATOM') and x[12:16].strip()=='CA']
  if len(ca)==len(r['sequence']):result.append({**r,'mean_plddt':sum(ca)/len(ca),'pdb_path':str(p)});continue
 pending.append(r)
if pending:
 if not torch.cuda.is_available():raise RuntimeError('CUDA unavailable for carded calibration inference')
 torch.manual_seed(0); model=EsmForProteinFolding.from_pretrained(sibling.MODEL,revision=sibling.REVISION,local_files_only=True).eval().cuda();model.esm=model.esm.half();model.trunk.set_chunk_size(64)
 for r in pending:
  with torch.inference_mode(): pdb=model.infer_pdb(r['sequence'])
  p=out/(r['variant_id']+'.pdb');p.write_text(pdb)
  ca=[float(x[60:66]) for x in pdb.splitlines() if x.startswith('ATOM') and x[12:16].strip()=='CA']
  if len(ca)!=len(r['sequence']):raise RuntimeError(r['variant_id'])
  result.append({**r,'mean_plddt':sum(ca)/len(ca),'pdb_path':str(p)})
  (ROOT/'data/raw/false_singleton_calibration/prediction_manifest.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'completed':len(result),'pending':len(pending)}))
