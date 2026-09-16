# In-cohort false-singleton calibration

Nine uncertain proteins were tested against their own confident close sequence relatives, rather than against an outside collection that never produced enough uncertain known-family proteins. This makes the result directly about the cohort and removes any need to match an outside confidence distribution. It does not establish a general fold-family recovery rate: the relatives share at least the frozen MMseqs2 30%-identity relation and are easier to join than remote members of a fold family, which can make the estimated excess too low and favour continuation. The small test set is heavily non-canonical and smut-derived, so applying its pooled rate to every singleton remains uncertain. No claim from this stage is admissible until the runtime boundary holds.

## Runtime boundary probe

Command: `scripts/assert_sandbox.sh instrument`  
Exit status: `1`

```text
FAIL instrument: T1 UNMEASURABLE: path absence is not a running process sandbox
PASS instrument: ABSENCE /home/aid1/Documents/3_19C_effector/role_clones/instrument/data/labels
PASS instrument: ABSENCE /home/aid1/Documents/3_19C_effector/role_clones/instrument/data/scored_cohort
PASS instrument: ABSENCE /home/aid1/Documents/3_19C_effector/role_clones/instrument/scorer
FAIL instrument: T2 connection to non-allowlisted host example.com succeeded
FAIL instrument: T3 package install outside the writable list succeeded
FAIL instrument: T4 write outside the role writable list succeeded
T7 MODEL-SIDE PROBE: in a fresh session, answer exactly NO_PRIOR_SESSION_MEMORY unless a marker from a prior session is available
FAIL instrument: T7 UNMEASURABLE: caller did not supply the model-side answer file
```

## Ruled test set

The Referee ledger (Items 61--63) requires every low-confidence ESMFold member
(mean pLDDT <0.50) with one or more confident members (>=0.50) in the same frozen
MMseqs2 30%-identity cluster. The resulting set has seven clusters, nine low members,
and eleven confident relatives. Full membership, pLDDT, profile stratum and source
organism are retained in `data/measurements/in_cohort_false_singleton_test_set.tsv`.

| Composition | Count |
|---|---:|
| Low-confidence members | 9 |
| Confident relatives | 11 |
| Mixed-confidence sequence clusters | 7 |
| Low members, canonical | 1 |
| Low members, non-canonical | 8 |
| Low members from Ustilago | 5 |
| Low members from Sporisorium | 2 |
| Low members from Magnaporthe | 2 |

The sample is not representative of all audited low-confidence structural singletons:
at TM 0.50 the target has 47 canonical and 128 non-canonical singleton models, while
this test has only one canonical member and seven of nine members are from sister smut
genera. Its correction is a measured local estimate, not a taxon- or stratum-balanced
estimate.

## Foldseek rate measurement

The carded retained Foldseek artifacts (`corrected_full_tm*.tsv`) use structural
alignment type 1 and cluster mode 1. A false singleton is an eligible member that
sits alone in its Foldseek cluster and does not share that cluster with any confident
member of its own sequence cluster. A wrong join would have been a non-singleton
structural cluster with no member of its own sequence cluster. The baseline is the
same false-singleton definition among the eleven confident relatives. The correction
uses the point excess `max(0, low rate - baseline rate)`; its conservative interval is
`max(0, low lower - baseline upper)` through `max(0, low upper - baseline lower)`,
using two-sided 95% Wilson intervals.

| TM | Low false singleton | Wrong join | Confident baseline | Baseline-subtracted excess, 95% interval |
|---:|---:|---:|---:|---:|
| .40 | 4/9 = 44.4% (.189–.733) | 0/9 = 0% (0–.299) | 2/11 = 18.2% (.051–.477) | 26.3% (0–68.2%) |
| .50 | 8/9 = 88.9% (.565–.980) | 0/9 = 0% (0–.299) | 6/11 = 54.5% (.280–.787) | 34.3% (0–70.0%) |
| .60 | 9/9 = 100.0% (.701–1.000) | 0/9 = 0% (0–.299) | 8/11 = 72.7% (.434–.903) | 27.3% (0–56.6%) |

At frozen TM .50, the raw low-member upper bound (.980) does not clear .8571; the
prespecified baseline-subtracted excess upper bound (.7000) does. This is the quantity
applied below, and the Referee—not the Instrument—determines whether it satisfies
Item 48.

## Corrected supply range

The range applies the baseline-subtracted 95% excess interval to the audited low-confidence
singleton counts 139, 175 and 184, not the superseded Curator counts. `panels_max` is
`floor(clusters / 5)`; MDE uses the ledger's provisional sigma_d .115.

| TM | All-model clusters | Audited low-confidence singletons | Corrected clusters (95% interval) | panels_max | MDE |
|---:|---:|---:|---:|---:|---:|
| .40 | 324 | 139 | 229.2–324.0 | 45–64 | .0480–.0403 |
| .50 (frozen) | 400 | 175 | 277.5–400.0 | 55–80 | .0434–.0360 |
| .60 | 437 | 184 | 332.9–437.0 | 66–87 | .0397–.0345 |

The corresponding baseline-subtracted point readings are 287.5 clusters/57 panels
(MDE .0427), 339.9/67 (.0394), and 386.8/77 (.0367). They are not primary readings.

| TM | Canonical raw clusters → corrected interval | Non-canonical raw clusters → corrected interval | Mixed clusters (unchanged) |
|---:|---:|---:|---:|
| .40 | 95 → 69.8–95.0 | 216 → 146.4–216.0 | 13 |
| .50 | 123 → 90.1–123.0 | 273 → 183.4–273.0 | 4 |
| .60 | 134 → 105.2–134.0 | 299 → 223.8–299.0 | 4 |

The stratum split applies one pooled interval to singleton counts because the calibration
has only one canonical low-confidence test member. It should not be interpreted as a
separate stratum-specific rate.

## Limits and handoff

The rate needs no outside distribution match or transfer assumption because the tested
proteins are themselves part of the corrected cohort. The remaining limitations are
the identity-relative downward bias, n=9, seven clusters, strong Ustilago/Sporisorium
concentration, and a test composition (eight non-canonical, one canonical) that does
not mirror all low-confidence singletons. The three external attempts remain a finding:
structure databases overwhelmingly contain proteins that ESMFold handles confidently.
No external holder is open for this result; the ECOD queue entry was closed by Referee
Item 64 rather than erased. The Instrument makes no Gate 1 or Item-48 ruling.
