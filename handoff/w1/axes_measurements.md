# Tier-1 measurements in progress

Union positives: 521 (164 canonical; 357 non-canonical).

| Axis | Result | Coverage / command result |
|---|---:|---|
| CD-HIT 30% | unavailable | `cd-hit -c 0.30 -n 2` exited 1: `Fatal Error: invalid clstr`. Bundled `psi-cd-hit.pl` also failed before BLAST, exit 2: `No input ... psi-cd-hit-local.pl line 149`. |
| CD-HIT 40% | 430 clusters | 521/521 sequences. |
| CD-HIT 50% | 460 clusters | 521/521 sequences. |
| Foldseek TM-score 0.50 | 79 clusters | 89/521 models (17.1%) from AlphaFold DB. |
| Foldseek conservative | 511 clusters | 79 covered clusters + 432 uncovered positives held as singletons. `panels_max = floor(511 / 5) = 102`. |

The Foldseek command was `foldseek easy-cluster data/raw/alphafold ... --alignment-type 1 --tmscore-threshold 0.5 --cluster-mode 1`; it reported 79 clusters over 89 models. No ESMFold prediction was started: that would require a model asset outside the permitted licence scope.
