# Tier 1 axes census — not released

> Superseded admissibility marker: read Item 79--84 in `ledger/ledger.yaml`; this record's historical runtime caveat is not the current condition.

This 521-positive fungal/oomycete cohort has 502 model structures (96.4%), but the number of independent fold families is sensitive to the TM threshold and may be inflated by low-confidence singleton models. At frozen TM 0.50, all models give 400 clusters (80 five-positive panels; MDE 0.036), while the 310-model high-confidence diagnostic subset gives 218 (43 panels; MDE 0.049). The direct annotation-based recovery test cannot estimate the correction: only four structurally mapped positives retain an explicit known-family annotation, none low-confidence. Negative verification and per-species coverage data are also absent. No claim from this stage is admissible until the runtime boundary holds; because Clause 1 requires all five axes, this is not a released census.

## Boundary

`scripts/assert_sandbox.sh curator` exited 1; its verbatim record is in `handoff/w1/boundary_probe_curator.md`. It found no running process sandbox for T1, and T2–T4 also failed. Every count below is therefore inadmissible for the benchmark.

## Structural supply and confidence diagnostic

Foldseek version `10-941cd33` used structural alignment type 1, cluster mode 1, and logged coverage `-c 0.8 --cov-mode 0`; the exact command is carded in `tools/cards/foldseek.md`. It returns model-structure clusters—a proxy for independent fold families, never a functional label. The old 89-model 79-cluster claim has no retained command output and cannot be reproduced. The retained command returns 71; full input is the 502 manifest-valid structures, not the prior 503-member staging directory containing stray invalid-residue H1VSQ9.

| TM | Reading | Clusters | canonical-only / non-canonical-only / mixed | panels_max | MDE |
|---:|---|---:|---:|---:|---:|
| 0.40 | all 502 | 324 | 95 / 216 / 13 | 64 | 0.0403 |
| 0.50 (frozen) | all 502 | 400 | 123 / 273 / 4 | 80 | 0.0360 |
| 0.60 | all 502 | 437 | 134 / 299 / 4 | 87 | 0.0345 |
| 0.40 | high-confidence diagnostic (310) | 180 | 60 / 111 / 9 | 36 | 0.0537 |
| 0.50 | high-confidence diagnostic (310) | 218 | 74 / 141 / 3 | 43 | 0.0491 |
| 0.60 | high-confidence diagnostic (310) | 248 | 81 / 163 / 4 | 49 | 0.0460 |

MDE uses alpha 0.05, beta 0.20, delta 0.05, provisional sigma_d 0.115 and N_min 42. At TM 0.40/0.50/0.60, observed low-low within-cluster pairs were 109/4/2 versus conditional-permutation expectations 178.3/50.7/14.2. Low-confidence models do not clump; they are unusually singleton (142/178/187), compatible with failed recovery rather than a confidence-driven false merge.

### Known-family recovery and corrected range

Ground truth was fixed from explicit Predector annotation text and PEACE source names, then exact-sequence mapped to provenance before clusters were read. It recovered MAX=1 and RxLR=3; NLP, LysM, Crinkler and ToxA-like had zero structurally mapped annotated members. All four were high-confidence; the three RxLR members occupied three clusters. There were zero eligible low-confidence known-family singletons. The intended false-singleton rate has a 95% Wilson interval of 0–1 because its denominator is zero. A point-corrected reading would be invented.

| TM | all models | high-confidence diagnostic | correction-compatible range (all clusters minus 0 to every low singleton) |
|---:|---|---|---|
| 0.40 | 324; 64 panels; MDE 0.0403 | 180; 36; 0.0537 | 182–324; 36–64; MDE 0.0537–0.0403 |
| 0.50 | 400; 80 panels; MDE 0.0360 | 218; 43; 0.0491 | 222–400; 44–80; MDE 0.0486–0.0360 |
| 0.60 | 437; 87 panels; MDE 0.0345 | 248; 49; 0.0460 | 250–437; 50–87; MDE 0.0456–0.0345 |

The all-model result contradicts the prediction of a large fold collapse relative to 430 sequence clusters at 40% identity: TM 0.50 has 400 clusters (about 7% fewer), not a large collapse. The AlphaFold DB subset is non-random, so this conclusion remains conditional on model quality and threshold.

## Other axes

| Axis | canonical | non-canonical | total / status |
|---|---:|---:|---|
| Positives | 164 | 357 | 521, functionally filtered |
| Structure coverage | 163/164 | 339/357 | 502/521; 18 >600-aa and one non-standard-residue exclusion |
| pLDDT Q1 / median / Q3; mean | .441 / .633 / .810; .628 | .436 / .563 / .719; .587 | weaker evidence on majority non-canonical stratum; no filter or weight |
| Unlabelled negatives | MEASURE | MEASURE | no retained candidate-negative cohort |
| Verified negatives | 0 | 0 | an unlabelled candidate is not a verified negative |
| Publication years | — | — | 510 known, 11 unknown; 81 >=2024, zero >2025; model cutoffs absent |
| RNA-seq / repeat annotation / assembly quality | MEASURE | MEASURE | per-species source metadata absent |

The structural channel accepts only canonical amino-acid strings up to 600 residues, removing one channel from 19 items. A primary-genus parser finds 66 raw species strings and 34 genera, not the independently quoted 37; taxonomy normalization is needed. It confirms Ustilago 96, Phytophthora 78 and Sporisorium 75. Ustilago plus sister smut genus Sporisorium is 171/521 (32.8%), a T5.2 concentration risk; their canonical/non-canonical splits are 19/77, 17/61 and 12/63.

## Clause 1 outcome

The structural and descriptive axes are recorded together, but the five-axis census is **not released**: negative verification, subject cutoff registry and per-species channel coverage remain unmeasured, and the runtime boundary fails. Nothing here convenes Gate 1.

## Curator completion audit — census withheld

The candidate-negative build has 32,225 unlabelled reviewed fungal/oomycete proteins and zero verified negatives. Precision against these candidates is a lower bound with species-dependent bias, not verified-negative precision. All 22 retained model cards lack a dated cutoff, so the 510 known publication years cannot form model-specific pre/post strata; zero positives are dated later than 2025, but that is not a prospective split. RNA-seq, repeat annotation and assembly-quality metadata cover 0/66 species, leaving every species below three documented evidence channels. No claim from this stage is admissible until the runtime boundary holds.

Frozen-taxonomy normalization gives 37 genera and 66 species strings. Ustilago (96) plus sister genus Sporisorium (75) total 171/521 (32.8%): 31 canonical and 140 non-canonical positives. The structural channel retains its 600-residue/non-standard-residue limit, and only 95/413 ESMFold predictions meet mean pLDDT >=.70.

At frozen TM .50, Item 65 holds supply: the preregistered raw 8/9 Wilson upper bound is .9801, above .8571. The baseline-subtracted 277.5--400.0 cluster / 55--80 panel range remains descriptive sensitivity only. Clause 1 therefore still prevents release and Gate 1 cannot proceed.

Item 68 now applies rates to both audited singleton populations. At frozen TM .50 the point
estimate is 145.2 clusters / 29 panels, with independent Wilson-rate sensitivity 85.2--250.1
clusters / 17--50 panels: close at the point estimate, close-to-hold across uncertainty, never
proceed. The three missing axes remain uncollected in valid Fetcher scope; see
`handoff/w1/three_axis_collection.md`.

**Admissibility update (Item 79--84, 2026-09-17):** the prior runtime-boundary sentence is superseded for non-arm retained-input measurements. This census remains unreleased because Clause-1 axes are incomplete, not because namespace isolation is unavailable. It cannot support an arm-separation claim on this host.
