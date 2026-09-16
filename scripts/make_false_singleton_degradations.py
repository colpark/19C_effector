#!/usr/bin/env python3
"""Create traceable sequence perturbations; they are diagnostics, never cohort items."""
from __future__ import annotations
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AA='ACDEFGHIKLMNPQRSTVWY'
rows=list(csv.DictReader(open(ROOT/'data/measurements/false_singleton_calibration_retained.tsv'),delimiter='\t'))
for r in rows: r['variant_id']='control__'+r['pdb_id'].lower()
out=[]
for r in rows:
 s=r['sequence']; family=[x['sequence'] for x in rows if x['family']==r['family']]
 # A retained N-terminal domain fragment. Its original family is a provenance label,
 # not proof that the fragment retains the native fold.
 out.append({**r,'method':'truncation_50pct','variant_id':'trunc__'+r['pdb_id'].lower(),'sequence':s[:max(20,len(s)//2)],'method_detail':'N-terminal 50% fragment'})
 conserved=[i for i,c in enumerate(s) if sum(i<len(t) and t[i]==c for t in family)>=3]
 changed=list(s)
 for i in conserved[::max(1,len(conserved)//8 or 1)][:8]: changed[i]='P' if s[i]!='P' else 'A'
 out.append({**r,'method':'conserved_position_mutation','variant_id':'mut__'+r['pdb_id'].lower(),'sequence':''.join(changed),'method_detail':'up to eight position-index conserved residues replaced by P (or A if already P)'})
 # The least same-family-similar control is only a shallow *within-set* proxy; it is
 # not evidence of shallow natural database alignments.
 score=lambda t:sum(a==b for a,b in zip(s,t))/max(len(s),len(t))
 out.append({**r,'method':'natural_orphan_proxy','variant_id':'orphan__'+r['pdb_id'].lower(),'sequence':s,'method_detail':'full solved sequence; proxy only, no external alignment-depth source'})
with (ROOT/'data/measurements/false_singleton_variants.tsv').open('w',newline='') as h:
 w=csv.DictWriter(h,fieldnames=list(out[0]),delimiter='\t');w.writeheader();w.writerows(out)
(ROOT/'build/false_singleton_variants.fasta').write_text(''.join(f'>{r["variant_id"]}\n{r["sequence"]}\n' for r in out))
print({'variants':len(out),'methods':sorted({r['method'] for r in out})})
