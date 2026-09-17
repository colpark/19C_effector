# Referee ruling: in-cohort false-singleton calibration

> Superseded admissibility marker: read Item 79--84 in `ledger/ledger.yaml`; the historical runtime caveat below is not the current condition.

The external route cannot produce the population it was designed to calibrate: damaging deeply known proteins did not make them uncertain, ECOD could not be reached from an allowlisted Fetcher, and the authorised SCOP route found only one target-band protein among 34 predictions. The Referee therefore authorises a direct measurement on the cohort's own frozen sequence relatives. It avoids a confidence-distribution transfer, but it is not a fold-family test: close sequence relatives are easier for Foldseek to join, so the resulting false-singleton rate can be biased downward and can favour continuation. No claim from this stage is admissible until the runtime boundary holds.

## Recount and ruled conditions

The retained `data/measurements/mmseqs30/union_cluster.tsv`, joined by accession to
`data/raw/esmfold_manifest.json`, has 430 sequence clusters. Fifty-nine contain more
than one member; seven contain both an ESMFold model below 0.50 mean pLDDT and one at
or above 0.50; those seven contain nine eligible low-confidence members. This confirms
the supplied recount (59, 7, 9).

Item 61 accepts membership in the frozen MMseqs2 30%-identity sequence cluster as the
predictor-independent relatedness label. Item 62 requires one, rather than three,
confident same-cluster relatives. The old three-relative condition established a
fold-family relationship; one high-identity counterpart establishes the narrower
relation now tested. The estimand is consequently “failure to join an available
confident sequence relative,” not fold-family recovery. Every downstream corrected
rate, cluster count, `panels_max`, MDE and Item-48 statement must name the resulting
downward bias.

The three failed external routes remain recorded: (1) truncation and conserved-site
mutation left lysozyme, ubiquitin and RNase A above 0.89 pLDDT; (2) the official ECOD
endpoint failed from an allowlisted Fetcher with curl exit 7 (with HTTP and PDBe
fallbacks also unavailable); and (3) SCOP/PDBe produced one target-band coronavirus
nucleocapsid member in 34 predictions, with no eligible family support. Item 64 closes
the ECOD action-queue record as structurally infeasible for this calibration; the
original outage evidence remains in the closed row.

## Prespecified n=9 outcome rule

| False-singleton failures / 9 | Two-sided 95% Wilson upper bound | Clears 0.8571? |
|---:|---:|---|
| 0 | .2991 | yes |
| 1 | .4350 | yes |
| 2 | .5474 | yes |
| 3 | .6458 | yes |
| 4 | .7333 | yes |
| 5 | .8112 | yes |
| 6 | .8794 | no |
| 7 | .9368 | no |
| 8 | .9801 | no |
| 9 | 1.0000 | no |

The Instrument measures all nine and may not enlarge the set. At most five failures
clear the Item-48 calibration condition. Six or more do not clear it, but cannot close
the task at frozen TM 0.50: even a rate of one leaves 225 clusters and 45 panels, above
`N_min = 42`. A high result is therefore a non-clearing hold-band result, not a closure.

## Ledger amendments

Items 48, 51 and 60 were appended with Item-61--63 reasons; Items 61--64 were added
with initial amendment records. The current ledger, not this summary, is authoritative.
No Gate 1 is convened.
