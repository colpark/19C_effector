# Referee Items 79--84: runtime boundary and claim scope

This host cannot provide runtime process isolation: Bubblewrap fails after namespace creation at loopback setup, the sandbox will not start, the PI has ruled out the kernel change, and no second machine exists. Treating the old boundary condition as eventually satisfiable would make every result permanently inadmissible. The replacement condition below admits only non-arm measurements whose relevant risks are absent; it does not make an arm-separation experiment valid on this host. No claim beyond that scope is admissible.

## Threat-by-threat ruling

| Threat | Current status | Replacement / residual |
|---|---|---|
| T1 execution outside sandbox | lost | Host protection only; no benchmark measurement claim depends on it. |
| T2 unrestricted network | lost | No adequate arm-execution replacement here. Offline operation would be required; trace detects rather than prevents. |
| T3 package installation | lost | Host/tool-surface protection only; no measurement-validity claim depends on it. |
| T4 writes outside scratch | lost | Host/shared-state protection only; no measurement-validity claim depends on it. |
| T5 withheld grant | lost for arms | Credentials/server absence is weaker than network denial. Arm 3 cannot run validly here. Trace-side review is diagnostic only. |
| T6 label leakage | clone absence passes | scorer, runs and design split are absent from Curator clone; residual: same-UID process can read union repository elsewhere. Needs separate account or physical temporal removal for sensitive execution. |
| T7 cross-cell memory | independently unverified | Fresh-session trace and model-side memory probe required. It never depended on namespaces. |
| T8 scorer contact | clone absence passes | Same residual as T6: clone-level absence is not machine-wide absence. |

Separate OS accounts with 0700 role directories would be a meaningful replacement, but no such
separate account is available and creating one requires administration. Temporal separation can
support a Fetcher-only retrieval if the union repository, labels, scorer and credentials are
offline and an absence inventory is retained. It is weaker than process isolation because the
same user can restore material and because it does not constrain network reach. It cannot validate
an arm-3/arm-4 comparison. Endpoint withholding and credentials absence help only if the machine
is offline; otherwise public or alternate endpoints remain reachable. Trace checks detect attempts
but cannot prevent a successful undisclosed one.

## Rewritten admissibility condition

A **non-arm measurement** counts when inputs and commands are retained and hashed; no arm or
sensitive answer-key process runs; its relevant sensitive paths are absent from the execution
directory; and, where Fetcher network access is used, the union repository, labels, scorer and
credentials are physically offline with a retained pre/post absence inventory. T7 is verified
by a fresh-session model-side trace when an agent session is involved.

Under that condition the existing sequence and structural census, calibration, and supply
calculations stand as non-arm methodological measurements, subject to their scientific caveats,
unreleased axes, and Item 71 residual bias. They do **not** become admissible arm-comparison
results. Any existing measurement that required arm withholding, label protection against a
same-UID process, or scorer isolation remains provisional and cannot support a benchmark effect.

## Claim boundary and Fetcher determination

This deployment may claim retained-input cohort counts, clustering results, calibration arithmetic,
and conditional supply decisions. It may not claim that arm 4 differs from arm 3, that arm 3 was
withheld from a foundation-model capability, or that item labels/scoring were process-isolated.
Those claims require a verified process-scope T2/T5/T6/T8 control and a T7 trace.

The launcher refusal remains correct. A Fetcher session can produce admissible source data only
under the temporal Fetcher condition above; no launcher relaxation is authorized. On the current
union host without that condition, verified negatives, cutoff dates and per-species channels stay
blocked. Block A is closed as unavailable; remaining external data holders are the relevant
evidence repositories, tool developers/owners, and RNA/repeat/assembly data providers.
