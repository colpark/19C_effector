#!/usr/bin/env python3
"""Predict residual proteins only within the carded ESMFold length contract."""
import csv, hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / '2_19C_biology/benchmark-mcp'))
import esmfold_worker as sibling
import torch
from transformers import EsmForProteinFolding

root = Path(__file__).resolve().parents[1]
out = root / 'data/raw/esmfold'; out.mkdir(parents=True, exist_ok=True)
manifest = root / 'data/raw/esmfold_manifest.json'
unsupported_manifest = root / 'data/raw/esmfold_unsupported.json'
maximum_residues = 600
chunk_size = 64

def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    temporary.replace(path)

af = {r['accession'] for r in csv.DictReader(open(root/'data/raw/alphafold_manifest.tsv'), delimiter='\t') if r['status']=='fetched'}
rows = list(csv.DictReader(open(root/'data/positives/provenance.tsv'), delimiter='\t'))
seqs = {}
name = None
for line in open(root/'data/positives/union.fasta'):
    if line.startswith('>'): name=line[1:].strip(); seqs[name]=''
    else: seqs[name]+=line.strip()
residual = [r for r in rows if r.get('uniprot_accession','') not in af]
todo = sorted([r for r in residual if int(r['length']) <= maximum_residues], key=lambda r:int(r['length']))
unsupported = [{'accession': r['accession'], 'length': int(r['length']),
                'profile_stratum': r['profile_stratum'], 'reason': '>600 aa carded limit'}
               for r in residual if int(r['length']) > maximum_residues]
atomic_json(unsupported_manifest, unsupported)

result=[]
pending=[]
for r in todo:
    seq=seqs[r['accession']]
    path=out/f"ESMF-{r['accession']}.pdb"
    if not path.exists():
        pending.append(r)
        continue
    pdb=path.read_text()
    ca=[float(x[60:66]) for x in pdb.splitlines() if x.startswith('ATOM') and x[12:16].strip()=='CA']
    if len(ca) != len(seq):
        pending.append(r)
        continue
    result.append({'accession':r['accession'],'profile_stratum':r['profile_stratum'],'length':len(seq),'mean_plddt':sum(ca)/len(ca),'sha256':hashlib.sha256(pdb.encode()).hexdigest(),'path':str(path)})
atomic_json(manifest, result)
if pending:
    if not torch.cuda.is_available(): raise RuntimeError('CUDA is required for the authorised residual prediction run')
    torch.manual_seed(0)
    model=EsmForProteinFolding.from_pretrained(sibling.MODEL, revision=sibling.REVISION, local_files_only=True).eval().cuda()
    model.esm=model.esm.half(); model.trunk.set_chunk_size(chunk_size)
    for r in pending:
        seq=seqs[r['accession']]
        path=out/f"ESMF-{r['accession']}.pdb"
        with torch.inference_mode(): pdb=model.infer_pdb(seq)
        path.write_text(pdb)
        ca=[float(x[60:66]) for x in pdb.splitlines() if x.startswith('ATOM') and x[12:16].strip()=='CA']
        if len(ca) != len(seq): raise RuntimeError(f"{r['accession']}: expected {len(seq)} CA atoms, found {len(ca)}")
        result.append({'accession':r['accession'],'profile_stratum':r['profile_stratum'],'length':len(seq),'mean_plddt':sum(ca)/len(ca),'sha256':hashlib.sha256(pdb.encode()).hexdigest(),'path':str(path)})
        atomic_json(manifest, result)
print(json.dumps({'completed_within_contract':len(result),'pending':len(pending),'unsupported_over_600':len(unsupported),'chunk_size':chunk_size,'model':sibling.MODEL,'revision':sibling.REVISION}))
