# Natural low-confidence ECOD calibration — blocked before selection

The target is unchanged: 189 cohort ESMFold models below mean pLDDT 0.50, with
median 0.408, Q1–Q3 0.368–0.447 and range 0.281–0.500; canonical n=53 and
non-canonical n=136. No claim from this artifact is admissible until the runtime
boundary holds. No candidate pool was assembled and no confidence selection occurred,
because the independent ECOD family assignment required by this method was unavailable.

## Frozen target

This attempt uses `data/measurements/false_singleton_target.yaml` unchanged. It does
not refit the target to any candidate data.

## Required external input and failed retrieval

The required official ECOD complete-domain endpoint,
`https://prodata.swmed.edu/ecod/complete/ecod.latest.domains.txt`, failed with curl
exit status 7 (connection refused). The ECOD complete-directory endpoint failed with
the same status. The HTTP fallback returned status 404. PDBe's public mapping route
`https://www.ebi.ac.uk/pdbe/api/mappings/ecod/1ubq` returned HTTP 404, so it cannot
substitute for ECOD. SCOP is deliberately not substituted: this stage requires ECOD
family membership independent of the predictor.

Thus pool size, family-draw mechanism, contamination removals, low-confidence yield,
ECOD composition, Foldseek rates, and transfer are **not estimable**. The external
holder is the ECOD data service. This is recorded in `handoff/gate0/blocked.md`.

## Prespecified precision requirement

Before drawing a pool, this attempt defined a usable rate interval as a two-sided 95%
Wilson interval with worst-case half-width at most 0.05. The normal worst-case
approximation gives `n = ceil(1.96^2 * 0.25 / 0.05^2) = 385` low-confidence members.
Each would also require at least three confident ECOD-family members. No smaller pool
is claimed adequate; the prior n=20 interval is explicitly inadequate.

## Boundary

`scripts/assert_sandbox.sh instrument` again exited 1 with the verbatim output in
`handoff/w1/boundary_probe_instrument.md`: T1 is unmeasurable without a running
process sandbox, T2–T4 fail, and T7 was not supplied. This report does not rule on
Item 48 or convene Gate 1.
