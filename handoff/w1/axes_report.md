# T1.1-T1.6 five-axis report

Recorded: 2026-09-15

## Boundary assertion

`scripts/assert_sandbox.sh curator` exited `1`. Its output was:

```text
FAIL curator: T1 outside-boundary Bash execution succeeded
FAIL curator: Bash read succeeded for denied path /home/aid1/Documents/3_19C_effector/bench/scorer
FAIL curator: Bash read succeeded for denied path /home/aid1/Documents/3_19C_effector/bench/runs
FAIL curator: Bash read succeeded for denied path /home/aid1/Documents/3_19C_effector/bench/data/design_split
FAIL curator: T2 connection to non-allowlisted host example.com succeeded
FAIL curator: T3 package install outside the writable list succeeded
FAIL curator: T4 write outside the role writable list succeeded
T7 MODEL-SIDE PROBE: in a fresh session, answer exactly NO_PRIOR_SESSION_MEMORY unless a marker from a prior session is available
FAIL curator: T7 UNMEASURABLE: caller did not supply the model-side answer file
```

No claim in this report is admissible to the benchmark until the boundary
holds.

## Five-axis census

No numeric axis count is released. The only available files in
`data/positives/`, `data/labels/`, and `data/scored_cohort/` are repository
placeholders; `docs/assets.md` still records every required asset checksum as
`PENDING`; and no Week 1 fetch report exists. The canonical profile also lacks
an operational definition for “small” and “cysteine-rich.”

| Axis | Required resolution | Canonical | Non-canonical | Total or distinction | Measuring task | Blocking evidence |
|---|---|---|---|---|---|---|
| Positives, sequence clusters | 30, 40 and 50 percent identity | MEASURE | MEASURE | MEASURE at every threshold; retained count MEASURE; removed count MEASURE | T1.2, T1.3, T1.4 | Union positive FASTA, provenance, and functional-evidence eligibility decisions absent |
| Positives, structural clusters | Foldseek TM-score 0.50, binding count | MEASURE | MEASURE | MEASURE; panel support by stratum is MEASURE | T1.3, T1.4 | Union positive set, predicted structures, and Foldseek all-versus-all result absent |
| Negatives | Unlabelled, not verified; quantify both | MEASURE | MEASURE | Unlabelled count MEASURE; verified-negative count MEASURE; distinction MEASURE | T1.1 | Negative cohort and negative provenance and verification records absent |
| Contamination exposure | Publication and deposition date against every subject cutoff | Pre-cutoff MEASURE; post-cutoff MEASURE | Pre-cutoff MEASURE; post-cutoff MEASURE | Subject cutoffs and combined strata MEASURE | T1.5 | Dates, retained positives, and subject-cutoff registry absent |
| Tool coverage | Per channel, per species: in planta RNA-seq, repeat annotation, assembly quality | MEASURE per channel and species | MEASURE per channel and species | Species list and combined coverage MEASURE | T1.6 | Species cohort and per-channel source metadata absent |

T1.4 permits a hypersensitive response assay, knockout virulence phenotype, or
validated host-target interaction. Computational evidence codes do not
qualify. T1.4 did not retain or remove any record because no candidate record
with an evidence code was available. That is not a zero count; both quantities
remain `MEASURE` by T1.4. No sequence clustering, structure prediction,
Foldseek run, or other count-producing computation was performed.

## Gate 1 convening

Gate 1 is convened as **BLOCKED**. The complete five-axis census is unmeasured,
the T1.3 binding structural-cluster count is absent, canonical and
non-canonical panel support cannot be evaluated, and the Curator boundary
assertion failed. No panel was built.
