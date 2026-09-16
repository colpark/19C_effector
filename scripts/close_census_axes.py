#!/usr/bin/env python3
"""Materialise the negative, cutoff, coverage, and taxon census from retained inputs."""
from __future__ import annotations
import csv, gzip, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def primary_org(s): return s.split(';',1)[0].strip()
def main():
 p=list(csv.DictReader(open(ROOT/'data/positives/provenance.tsv'),delimiter='\t'))
 posacc={r['accession'] for r in p}|{r['uniprot_accession'] for r in p if r['uniprot_accession']}
 possha={r['sequence_sha256'] for r in p}
 import hashlib
 candidates={}
 for f in ['uniprot_reviewed_taxonomy_4751.tsv.gz','uniprot_reviewed_taxonomy_4762.tsv.gz']:
  with gzip.open(ROOT/'data/raw/sources'/f,'rt',encoding='utf-8',newline='') as h:
   for r in csv.DictReader(h,delimiter='\t'):
    sha=hashlib.sha256(r['Sequence'].encode()).hexdigest()
    if r['Entry'] not in posacc and sha not in possha: candidates[r['Entry']]=r
 out=ROOT/'data/measurements'; out.mkdir(exist_ok=True)
 with open(out/'candidate_negatives.tsv','w',newline='',encoding='utf-8') as h:
  w=csv.writer(h,delimiter='\t');w.writerow(['accession','organism','length','status'])
  for r in sorted(candidates.values(),key=lambda x:x['Entry']):w.writerow([r['Entry'],r['Organism'],r['Length'],'unlabelled_candidate_not_verified_negative'])
 cards=sorted((ROOT/'tools/cards').glob('*.md'))
 with open(out/'subject_cutoff_registry.tsv','w',newline='',encoding='utf-8') as h:
  w=csv.writer(h,delimiter='\t');w.writerow(['tool_card','cutoff_date','status'])
  for c in cards:w.writerow([c.name,'','UNFILLED: no subject-model cutoff date in retained card'])
 species=defaultdict(list)
 for r in p:species[primary_org(r['organism'])].append(r)
 with open(out/'species_channel_coverage.tsv','w',newline='',encoding='utf-8') as h:
  w=csv.writer(h,delimiter='\t');w.writerow(['species','positives','canonical','non_canonical','in_planta_rnaseq','repeat_annotation','assembly_quality','structural_available','structural_high_confidence','fewer_than_three_channels'])
  manifest={x['accession']:x for x in json.load(open(ROOT/'data/raw/esmfold_manifest.json'))}
  models=set(manifest)
  with open(ROOT/'data/raw/alphafold_manifest.tsv',encoding='utf-8',newline='') as ah:
   models |= {r['accession'] for r in csv.DictReader(ah,delimiter='\t') if r['status']=='fetched'}
  for s,rs in sorted(species.items()):
   m=sum(r['accession'] in models or r['uniprot_accession'] in models for r in rs)
   hi=sum((r['accession'] in manifest and manifest[r['accession']]['mean_plddt']>=.7) for r in rs)
   w.writerow([s,len(rs),sum(r['profile_stratum']=='canonical' for r in rs),sum(r['profile_stratum']=='non-canonical' for r in rs),0,0,0,m,hi,'yes'])
 genera=Counter(primary_org(r['organism']).split()[0] for r in p)
 years=[int(r['publication_year']) for r in p if r['publication_year'].isdigit()]
 summary={'negatives':{'unlabelled_candidates':len(candidates),'verified_negatives':0},'cutoffs':{'cards':len(cards),'dated_cutoffs':0,'pre_cutoff':'not_computable','post_cutoff':'not_computable','post_2025_positives':sum(y>2025 for y in years)},'coverage':{'species':len(species),'rna_seq_species':0,'repeat_annotation_species':0,'assembly_quality_species':0,'species_fewer_than_three_channels':len(species)},'taxonomy':{'genera':len(genera),'species_strings':len(species),'top_genera':genera.most_common(5),'smut_total':genera['Ustilago']+genera['Sporisorium']}}
 (out/'census_axis_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
