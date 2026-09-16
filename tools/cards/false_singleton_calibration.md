# False-singleton calibration card

No claim from this artifact is admissible until the runtime boundary holds.

## Measurement

This attempted to measure the probability that an ESMFold-predicted member of a
known structural family is placed in a singleton Foldseek cluster rather than with
its own family. Twenty public PDB controls were fixed from five PDBe SCOP-mapped
families (four structures each): ubiquitin-like, lysozyme-like, thioredoxin-like,
ribonuclease-A-like and beta-lactamase-like. PDBe SCOP mapping verified the stated
SUNID for every control. MMseqs2 `easy-search --min-seq-id 0.3 -c 0.8 --cov-mode 0`
against all 521 cohort positives removed zero controls at the stated threshold.

The controls are generic globular proteins, not effector folds. Candidate effector
folds did not leave four independent, cohort-nonoverlapping solved members in the
locally available annotation sources. That substitution limits transfer to
disulfide-stabilised effectors.

## Methods and result

ESMFold v1 revision `75a3841ee059df2bf4d56688166c8fb459ddd97a` predicted 20
variants for each separate method: 50% N-terminal truncation, mutation of up to
eight position-index conserved residues, and a full-length within-set orphan proxy.
Foldseek used its carded structural alignment type 1, cluster mode 1 and TM 0.40,
0.50, 0.60 command.

None of the methods matched the frozen cohort target (mean pLDDT <0.50, median
0.408): method medians were 0.895, 0.903 and 0.936, with Wasserstein-1 distances
0.440, 0.459 and 0.518. Each gave 1/20 singletons (5%, 95% Wilson 0.9–23.6%) and
0/20 wrong-family joins (0–16.1%) at every TM threshold. The full-length proxy is
the undegraded control baseline. These rates are recorded but **do not qualify for
transfer**: they measure high-confidence generic control behaviour, not uncertain
effector-like behaviour.

## What this does not cover

Truncation and conserved-site mutation may change a protein's actual fold, so an
original-family label is only provenance, not experimental ground truth for the
variant. The orphan method is a within-set sequence-divergence proxy, not a verified
shallow natural-alignment measurement. No method generated the target confidence
distribution; consequently no corrected cohort count, panel count or MDE is supplied.

## Disagreement list

- Target manifest contains 189, not the prompt's stated 192, models below 0.50.
- The calibration controls are generic globular structures rather than the requested
  effector folds.
- All perturbation methods stayed much more confident than the target; their rates
  disagree in scope, not materially in point estimate.

## Attempt 5 — ruled in-cohort sequence-relative calibration

Referee Items 61--64 retired the external route as structurally infeasible for this
calibration and fixed the eligible population before its Foldseek result was read:
low-confidence ESMFold members (<0.50 mean pLDDT) with at least one confident member
(>=0.50) in their frozen MMseqs2 30%-identity sequence cluster. The cohort recount
has seven such clusters, nine low-confidence members, and eleven confident relatives.
Unlike Attempts 1--4, this is a direct same-cohort measurement and needs neither a
confidence-distribution match nor an external-family transfer.

It measures recovery of a close sequence relative, not a structural family. That is
an important limitation: a high-identity relative is easier for Foldseek to join than
a fold-family relative, so the baseline-subtracted false-singleton excess can be biased
downward, in the direction favouring continuation. The retained implementation,
test-set table and machine-readable rates are `scripts/measure_in_cohort_false_singletons.py`,
`data/measurements/in_cohort_false_singleton_test_set.tsv`, and
`data/measurements/in_cohort_false_singleton_calibration.json`.

At TM 0.40/0.50/0.60, respectively, the low-member false-singleton counts were
4/9, 8/9 and 9/9; confident-relative baseline counts were 2/11, 6/11 and 8/11; no
low member made a wrong-family join. The conservative 95% intervals for the
baseline-subtracted excess were 0--0.6820, 0--0.7000 and 0--0.5656. The Instrument
does not rule on Item 48. The test members are concentrated in Ustilago/Sporisorium
and the non-canonical stratum, so pooled correction across all low-confidence
singletons is a representativeness limitation.

## Attempt 2 — naturally low-confidence ECOD controls

This attempt was specified to avoid degradation entirely: draw an unselected ECOD
pool, predict first, retain members in the frozen target band only when each has three
confident ECOD-family members, and require 385 low-confidence members for a worst-case
95% Wilson half-width no larger than 0.05. It did not begin selection. The official
ECOD complete-domain endpoint was unreachable (curl exit 7; HTTP fallback 404), and
PDBe exposes no ECOD mapping endpoint (HTTP 404). SCOP is not a substitute for an
ECOD-required calibration. The rate and transfer are therefore not estimable; see
`handoff/w1/natural_low_confidence_calibration.md`.

## Attempt 3 — Fetcher ECOD probe and substitute proposal

Item 54 rendered a standalone Fetcher clone with `prodata.swmed.edu` explicitly
allowlisted. Retrieval still failed with curl exit 7, so the ECOD service remains the
external holder; the block is not misfiled against the Instrument permission model.
SCOP via PDBe is proposed as an independent pre-prediction fallback, but it loses
ECOD's broad coverage and family granularity. Item 51 currently says ECOD, so no SCOP
pool or prediction was run pending a Referee amendment. Details and verbatim probe:
`handoff/w1/ecod_fetcher_probe.md` and `handoff/w1/ecod_substitute_proposal.md`.

## Attempt 4 — authorised SCOP natural-confidence pool

After Referee Item 58 authorized SCOP/PDBe, a deterministic unselected 240-PDB draw produced 36 contamination-screen-retained SCOP records and 34 carded ESMFold predictions. One (2CJR, coronavirus nucleocapsid dimerization domain) fell in the frozen pLDDT band. It is one family with no eligible family support, failing the five-family and three-confident-relative conditions. No Foldseek rate or transfer was calculated. This attempt confirms that the SCOP substitute's narrower coverage and natural-low-confidence yield—not induced sequence damage—are the limiting facts. Full report: `handoff/w1/scop_natural_calibration.md`; source card: `tools/cards/scop_pdbe_mapping.md`.
