# Referee Items 71--74

> Superseded admissibility marker: read Item 79--84 in `ledger/ledger.yaml` before relying on this historical ruling.

The challenge identifies a conditional-estimand error in Item 68. The calibration measured
whether a protein fails to join a known relative that is present in this cohort. It cannot
measure that failure for a singleton without such a relative. The reversal below is caused
by this scope challenge, not by a new structural measurement. No claim from this stage is
admissible until the runtime boundary holds.

## Independent recount and Item 71 ruling

| Measure | Challenge | Recount |
|---|---:|---:|
| MMseqs sequence clusters | 430 | 430 |
| Multi-member sequence clusters | 59 | 59 |
| Members with a sequence relative | 150 | 150 |
| Members without one | 371 | 371 |
| Structural singletons, TM .40/.50/.60 | 270 / 357 / 404 | 270 / 357 / 404 |
| Eligible structural singletons | 42 / 65 / 80 | 42 / 65 / 80 |
| Eligible low / other | 33 / 9; 47 / 18; 51 / 29 | same |

The correction applies only to a structural singleton with at least one member of its
frozen MMseqs2 30%-identity sequence cluster present in the cohort, split by the measured
low-confidence and other/confident rates. This is the eligibility condition under which the
rate was measured. Applying it to all singletons would estimate an untested rate among units
that cannot fail to join a known sequence relative.

This does not prove sequence-orphan singletons are genuine folds: a remote fold relative may
exist below sequence detection. The calibration never tested that possibility. Leaving those
units uncorrected therefore has an unquantified upward bias in cluster and panel supply, in
the direction favouring continuation.

## Item 72 audit

The sharper rule is that every preregistered rate or correction names both its population and
the eligibility condition under which it was measured. Two material defects fail this test:
Item 51 omitted both; Item 68 named all structural singletons but omitted known-relative
eligibility. Item 69 correctly found one defect under its weaker population-only test.

## Item 73 supply

| TM | Point clusters / panels / MDE | Wilson-rate sensitivity clusters / panels / MDE | Status |
|---:|---|---|---|
| .40 | 307.7 / 61 / .0413 | 295.5–317.3 / 59–63 / .0419–.0406 | proceeds on supply |
| .50 frozen | 348.4 / 69 / .0388 | 339.8–368.4 / 67–73 / .0394–.0377 | proceeds on supply |
| .60 | 364.9 / 72 / .0380 | 359.8–388.7 / 71–77 / .0382–.0367 | proceeds on supply |

The point reversal makes detection easier, which is why the unmeasured remote-fold residual
is retained rather than treated as zero. The correction reduces canonical/non-canonical-only
structural clusters at frozen TM .50 from 123/273 to approximately 110.8/233.0; four mixed
clusters are unchanged. Alias and mixed-cluster handling means these are descriptive, not
separate stratum-specific rates.

## Item 74 remaining Gate 1 conditions

Supply no longer blocks Gate 1. Remaining conditions are: a passing runtime boundary (Block A,
external holder host sysadmin); a verified-negative axis (requires valid Fetcher deployment and
external experimental evidence sources); dated subject-model cutoffs (tool developers/owners);
and per-species infection RNA-seq, repeat annotation and assembly-quality records (data
providers). The complete five-axis census remains required by Clause 1.
