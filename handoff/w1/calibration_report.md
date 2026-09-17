# Instrument false-singleton calibration — no transfer

> Superseded admissibility marker: read Item 79--84 in `ledger/ledger.yaml`; the historical runtime caveat below is not the current condition.

The cohort target is 189 ESMFold models with mean pLDDT below 0.50 (median 0.408,
Q1–Q3 0.368–0.447; range 0.281–0.500), not 192. Twenty SCOP-mapped solved PDB
controls from five generic non-effector families passed a MMseqs2 30%-identity,
80%-coverage exclusion check against the 521-positive cohort; none was removed.
However, no induced-uncertainty method resembled the target: 50% truncation,
conserved-position mutation, and the natural-orphan proxy had median pLDDT 0.895,
0.903 and 0.936, respectively. No claim from this stage is admissible until the
runtime boundary holds. More importantly, no rate below is transferable to the
cohort because its confidence distribution was not matched.

The Instrument boundary probe failed (`handoff/w1/boundary_probe_instrument.md`):
T1 is unmeasurable without a running process sandbox, T2–T4 failed, and T7 was not
supplied. This report does not rule on Item 48 or convene Gate 1.

## Frozen target and achieved distributions

| Population / method | n | Q1 | median | Q3 | range | mean | Wasserstein-1 to target | qualifies |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Cohort target | 189 | .368 | .408 | .447 | .281–.500 | .408 | 0 | yes |
| Truncation 50% | 20 | .872 | .895 | .932 | .586–.944 | .844 | .440 | no |
| Conserved-position mutation | 20 | .841 | .903 | .910 | .608–.934 | .863 | .459 | no |
| Natural-orphan proxy | 20 | .915 | .936 | .948 | .764–.954 | .923 | .518 | no |

The target split is canonical n=53, median .399 (Q1–Q3 .367–.441), and
non-canonical n=136, median .413 (Q1–Q3 .369–.449). The calibration has no
corresponding cohort-profile stratum, another transfer limitation.

## Foldseek error modes

The same result occurred at TM 0.40, 0.50 and 0.60 for every method.

| Method | False singleton | Wrong-family join | Undegraded control baseline |
|---|---|---|---|
| Truncation | 1/20 = 5.0% (95% Wilson .9–23.6%) | 0/20 = 0% (0–16.1%) | 1/20 = 5.0% (.9–23.6%) |
| Conserved-position mutation | 1/20 = 5.0% (.9–23.6%) | 0/20 = 0% (0–16.1%) | 1/20 = 5.0% (.9–23.6%) |
| Natural-orphan proxy / control | 1/20 = 5.0% (.9–23.6%) | 0/20 = 0% (0–16.1%) | 1/20 = 5.0% (.9–23.6%) |

The apparent perturbation excess over the control is zero, but it is not evidence
that the cohort low-confidence singleton rate is zero: all calibrations are
high-confidence and generic. The requested transfer to cohort singletons therefore
has no corrected cluster count, panels_max or MDE range. Those values are **not
estimable from this calibration**, rather than zero or unchanged.

## Materials and limitation

Candidates and SCOP IDs: `data/measurements/false_singleton_calibration_candidates.tsv`.
Retained/removed identity audit: `data/measurements/false_singleton_calibration_retained.tsv`
and `..._removed.tsv`. Per-variant predictions and rates are in
`data/measurements/false_singleton_calibration_results.json`. No external holder
blocked the public PDB/PDBe/MMseqs2 steps. The remaining limitation is methodological:
a verified low-confidence, effector-like calibration set is not present, so it is a
task for a future data acquisition rather than a block entry under clause 14.
