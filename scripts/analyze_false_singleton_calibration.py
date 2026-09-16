#!/usr/bin/env python3
"""Keep calibration error modes and confidence matching separate."""
from __future__ import annotations
import csv,json,math,statistics
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def wilson(k,n):
 if not n:return [0,1]
 z=1.959963984540054;p=k/n;d=1+z*z/n;c=(p+z*z/(2*n))/d;h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
 return [max(0,c-h),min(1,c+h)]
def w1(a,b):
 a=sorted(a);b=sorted(b);return sum(abs(a[round(i*(len(a)-1)/(len(b)-1))]-b[i]) for i in range(len(b)))/len(b)
def main():
 rows=json.load(open(ROOT/'data/raw/false_singleton_calibration/prediction_manifest.json'))
 target=[x['mean_plddt'] for x in json.load(open(ROOT/'data/raw/esmfold_manifest.json')) if x['mean_plddt']<.5]
 out={'admissibility_statement':'No claim from this artifact is admissible until the runtime boundary holds.','target_n':len(target),'methods':{}}
 for method in sorted({x['method'] for x in rows}):
  xs=[x for x in rows if x['method']==method]; scores=[x['mean_plddt'] for x in xs]
  item={'confidence':{'n':len(xs),'min':min(scores),'q1':statistics.quantiles(scores,n=4,method='inclusive')[0],'median':statistics.median(scores),'q3':statistics.quantiles(scores,n=4,method='inclusive')[2],'max':max(scores),'mean':statistics.mean(scores),'wasserstein_1_to_target':w1(scores,target),'qualifies_match':False},'thresholds':{}}
  fam={x['variant_id']:x['family'] for x in xs}
  for tau in ['0.40','0.50','0.60']:
   clusters=defaultdict(list)
   for line in open(ROOT/f'data/measurements/calibration_{method}_tm{tau}_cluster.tsv'):
    rep,member=line.rstrip().split('\t');clusters[rep].append(member.removesuffix('.pdb'))
   singleton=wrong=0
   for x in xs:
    own=x['variant_id']; cluster=next(v for v in clusters.values() if own in v)
    same=[z for z in cluster if fam[z]==fam[own] and z!=own]
    other=[z for z in cluster if fam[z]!=fam[own]]
    singleton+=not same and len(cluster)==1
    wrong+=not same and bool(other)
   n=len(xs);item['thresholds'][tau]={'n':n,'false_singleton':singleton,'false_singleton_rate':singleton/n,'false_singleton_95_wilson':wilson(singleton,n),'wrong_family':wrong,'wrong_family_rate':wrong/n,'wrong_family_95_wilson':wilson(wrong,n)}
  out['methods'][method]=item
 (ROOT/'data/measurements/false_singleton_calibration_results.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
