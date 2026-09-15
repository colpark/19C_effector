# Gate 0 verification findings

## Factual findings

1. **Role scopes were declared but not enforced.** Evidence: `AGENTS.md:3`, `access/*.yaml`, and the absence of a repository-owned renderer or assertion path at review time. Remediation: `scripts/render_access.py` now renders fail-closed Claude/Codex settings and sparse-worktree launchers; `scripts/assert_sandbox.sh` tests the running boundary through Bash.
2. **The threat file did not distinguish platform enforcement from project gates.** Evidence: `threats/threats.yaml`, `gates/README.md`, and `scripts/validate_stop_conditions.py`. Remediation: T1-T4 are marked `platform`, T5-T8 are marked `project`, and a platform-threat gate now fails validation.
3. **The ledger asserted a provisional sample count instead of an unmeasured value.** Evidence: `ledger/ledger.yaml`, element `S, samples per cell`. Remediation: the ledger CLI appended the prior value and exact correction reason, then set `current_value: MEASURE` and `measured_by: T4.3`.
4. **The documented authorized-asset helper did not exist.** Evidence: `docs/assets.md` references to `scripts/fetch_authorized_asset.py`. Remediation: `scripts/fetch_authorized_asset.py` now requires explicit authorization, HTTPS, destination, and publisher checksum, and its registry self-test covers every documented invocation.
5. **Asset procedures contained unresolved placeholders without explanations.** Evidence: `docs/assets.md`. Remediation: the PEACE repository is resolved; every remaining placeholder states the task or ruling needed to resolve it and why it remains open.
6. **The Curator charter mislabeled T2 as label leakage.** Evidence: `AGENTS.md`, Curator `Bound by` entry. Remediation: T2 is now described as network reach beyond the allowlist; T6 remains label leakage.
7. **The repository held no defining papers for T3.1.** Evidence: previously absent `docs/papers/`. Remediation: `docs/papers/predector_2021.pdf` is present with citation metadata. The requested PEACE preprint cannot be supplied: `docs/papers/PEACE_preprint_UNAVAILABLE.md` records that the official repository calls it unpublished, carries a `TBD` DOI, and contains no manuscript or release asset. This unresolved external dependency remains explicit and blocks a PEACE tool card.

## Reasoning findings — recorded, not changed

1. **The Adversary is denied data yet owns T4.1.** Evidence: `AGENTS.md`, Adversary holdings/denials and owned tasks; `tasks/register.csv`, row T4.1.
2. **The Referee is denied tools yet must read cards to judge a substitution under clause 2.** Evidence: `AGENTS.md`, Referee holdings/denials; `constitution.md`, clause 2; `docs/19C_effector_bench_agent_prompts.md`, “Licence substitutions.”
