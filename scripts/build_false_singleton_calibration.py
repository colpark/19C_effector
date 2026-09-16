#!/usr/bin/env python3
"""Fetch fixed SCOP-mapped PDB controls and exclude cohort-overlapping sequences."""
from __future__ import annotations
import csv, json, os, shutil, subprocess, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def get(url):
    with urllib.request.urlopen(url,timeout=60) as h:return h.read()
def main():
    candidates=list(csv.DictReader(open(ROOT/'data/measurements/false_singleton_calibration_candidates.tsv'),delimiter='\t'))
    out=ROOT/'data/raw/false_singleton_calibration/pdb';out.mkdir(parents=True,exist_ok=True)
    downloaded=[]
    for row in candidates:
        p=row['pdb_id'].lower()
        entity=json.loads(get(f'https://data.rcsb.org/rest/v1/core/polymer_entity/{p}/1'))
        seq=entity['entity_poly']['pdbx_seq_one_letter_code_can'].replace('\n','').replace(' ','')
        scop=json.loads(get(f'https://www.ebi.ac.uk/pdbe/api/mappings/scop/{p}'))[p]['SCOP']
        if row['scop_sunid'] not in scop: raise RuntimeError(f'{p}: expected SCOP {row["scop_sunid"]}, got {list(scop)}')
        item={**row,'sequence':seq,'length':len(seq)}
        (out/f'{p.upper()}.pdb').write_bytes(get(f'https://files.rcsb.org/download/{p.upper()}.pdb'))
        downloaded.append(item)
    query=ROOT/'build/false_singleton_calibration_candidates.fasta';query.parent.mkdir(exist_ok=True)
    query.write_text(''.join(f'>{r["pdb_id"]}\n{r["sequence"]}\n' for r in downloaded))
    result=ROOT/'build/false_singleton_calibration_mmseqs.tsv'; tmp=ROOT/'build/mmseqs_false_singleton'
    mmseqs = os.environ.get('MMSEQS_BINARY') or shutil.which('mmseqs')
    if not mmseqs:
        raise RuntimeError('MMseqs2 is required; set MMSEQS_BINARY to the pinned executable in docs/assets.md')
    subprocess.run([mmseqs,'easy-search',str(query),str(ROOT/'data/positives/union.fasta'),str(result),str(tmp),'--min-seq-id','0.3','-c','0.8','--cov-mode','0','--format-output','query,target,pident,alnlen'],check=True)
    hits={}
    if result.exists():
        for line in result.read_text().splitlines():
            q,target,pident,alnlen=line.split('\t'); hits.setdefault(q,[]).append((float(pident),target,int(alnlen)))
    retained=[]; removed=[]
    for item in downloaded:
        h=max(hits.get(item['pdb_id'].lower(),[]) or [(0.0,'',0)])
        item.update(maximum_mmseqs_identity_to_cohort=round(h[0],4),closest_cohort_accession=h[1],aligned_residues=h[2])
        (removed if h[0]>.30 else retained).append(item)
    for path,rows in [(ROOT/'data/measurements/false_singleton_calibration_retained.tsv',retained),(ROOT/'data/measurements/false_singleton_calibration_removed.tsv',removed)]:
        with path.open('w',newline='') as h:
            w=csv.DictWriter(h,fieldnames=['family','pdb_id','scop_sunid','selection_note','sequence','length','maximum_mmseqs_identity_to_cohort','closest_cohort_accession','aligned_residues'],delimiter='\t');w.writeheader();w.writerows(rows)
    print(json.dumps({'retained':len(retained),'removed_over_30_percent':len(removed),'families':sorted({r['family'] for r in retained})}))
if __name__=='__main__':main()
