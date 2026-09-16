#!/usr/bin/env python3
"""Run the sibling project's pinned ESMFold revision once over residual positives."""
import csv, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '2_19C_biology/benchmark-mcp'))
import esmfold_worker as sibling
import torch
from transformers import EsmForProteinFolding

root = Path(__file__).resolve().parents[1]
out = root / 'data/raw/esmfold'; out.mkdir(parents=True, exist_ok=True)
af = {r['accession'] for r in csv.DictReader(open(root/'data/raw/alphafold_manifest.tsv'), delimiter='\t') if r['status']=='fetched'}
rows = list(csv.DictReader(open(root/'data/positives/provenance.tsv'), delimiter='\t'))
seqs = {}
name = None
for line in open(root/'data/positives/union.fasta'):
    if line.startswith('>'): name=line[1:].strip(); seqs[name]=''
    else: seqs[name]+=line.strip()
todo = sorted([r for r in rows if r.get('uniprot_accession','') not in af], key=lambda r:int(r['length']))
torch.manual_seed(0)
model=EsmForProteinFolding.from_pretrained(sibling.MODEL, revision=sibling.REVISION, local_files_only=True).eval().cuda(); model.esm=model.esm.half()
result=[]
for r in todo:
    seq=seqs[r['accession']]
    path=out/f"ESMF-{r['accession']}.pdb"
    if path.exists(): pdb=path.read_text()
    else:
        with torch.inference_mode(): pdb=model.infer_pdb(seq)
        path.write_text(pdb)
    ca=[float(x[60:66]) for x in pdb.splitlines() if x.startswith('ATOM') and x[12:16].strip()=='CA']
    result.append({'accession':r['accession'],'profile_stratum':r['profile_stratum'],'length':len(seq),'mean_plddt':sum(ca)/len(ca),'sha256':hashlib.sha256(pdb.encode()).hexdigest(),'path':str(path)})
json.dump(result, open(root/'data/raw/esmfold_manifest.json','w'), indent=2)
print(json.dumps({'predicted':len(result),'model':sibling.MODEL,'revision':sibling.REVISION}))
