# Tier-1 measurements in progress

Union positives: 521 (164 canonical; 357 non-canonical).

| Axis | Result | Coverage / command result |
|---|---:|---|
| MMseqs2 30% | 430 clusters | 521/521 sequences; `easy-cluster --min-seq-id 0.3 -c 0.8 --cov-mode 0`. This replaces CD-HIT, whose `-c 0.30 -n 2` range failure was exit 1 (`Fatal Error: invalid clstr`) and whose bundled PSI fallback exited 2. |
| CD-HIT 40% | 430 clusters | 521/521 sequences. |
| CD-HIT 50% | 460 clusters | 521/521 sequences. |
| Foldseek TM-score 0.50 (covered subset) | 79 clusters | 89/521 AlphaFold DB models (17.1%). This is not the full-cohort measurement. |
| `upper_bound_singleton_assumption` (superseded when full Foldseek completes) | 511 clusters | Assumption: 79 covered clusters plus every one of 432 uncovered positives as an independent singleton. It is maximally optimistic about independence; `panels_max = floor(511 / 5) = 102` is not a measured structural supply. |

The covered-subset command was `foldseek easy-cluster data/raw/alphafold ... --alignment-type 1 --tmscore-threshold 0.5 --cluster-mode 1`.
The local carded ESMFold run is active and resumable. At this snapshot it has 367
residual PDBs, for 456/521 total structures (87.5%); it is not a final coverage or
cluster result. pLDDT is retained as a covariate and is not used as a filter.
