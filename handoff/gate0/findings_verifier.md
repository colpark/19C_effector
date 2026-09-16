# Gate 0 remediation verification

Verdict: **BLOCKED**. One factual finding rests on direct Bash reads of every rendered denied path.

## Self-tests

| Script | Result |
|---|---|
| `scripts/check_constitution.py --self-test` | PASS |
| `scripts/amend_ledger.py --self-test` | PASS |
| `scripts/validate_stop_conditions.py --self-test` | PASS |
| `scripts/provenance.py --self-test` | PASS |
| `scripts/render_access.py --self-test` | PASS |
| `scripts/fetch_authorized_asset.py --self-test` | PASS |
| `scripts/assert_sandbox.sh` | NO SELF-TEST EXPOSED |

## Findings

### F1 — FACTUAL — BLOCKING

Every `sandbox.filesystem.denyRead` path emitted by `scripts/render_access.py` was readable with `bash --noprofile --norc -c 'ls -A -- "$1"'`. The generated worktree snippet creates a sparse checkout, but it does not launch Bash, Claude, or Codex with either rendered settings file. The policy files therefore do not enforce the Bash boundary in the tested file state.

| Role | Readable denied path |
|---|---|
| Curator | `/home/aid1/Documents/3_19C_effector/bench/scorer` |
| Curator | `/home/aid1/Documents/3_19C_effector/bench/runs` |
| Curator | `/home/aid1/Documents/3_19C_effector/bench/data/design_split` |
| Instrument | `/home/aid1/Documents/3_19C_effector/bench/data/labels` |
| Instrument | `/home/aid1/Documents/3_19C_effector/bench/data/scored_cohort` |
| Instrument | `/home/aid1/Documents/3_19C_effector/bench/scorer` |
| Floor | `/home/aid1/Documents/3_19C_effector/bench/data/labels` |
| Floor | `/home/aid1/Documents/3_19C_effector/bench/data/scored_cohort` |
| Floor | `/home/aid1/Documents/3_19C_effector/bench/scorer` |
| Floor | `/home/aid1/Documents/3_19C_effector/bench/runs` |
| Referee | `/home/aid1/Documents/3_19C_effector/bench/runs` |
| Referee | `/home/aid1/Documents/3_19C_effector/bench/data/design_split` |
| Referee | `/home/aid1/Documents/3_19C_effector/bench/tools` |
| Adversary | `/home/aid1/Documents/3_19C_effector/bench/data` |
| Adversary | `/home/aid1/Documents/3_19C_effector/bench/scorer` |

Evidence paths: `access/*.yaml`; `build/access/*/.claude/settings.*.json`; `build/access/*/.codex/config.*.toml`; `build/access/*/create_worktree.*.sh`; `scripts/render_access.py`; `scripts/assert_sandbox.sh`.

## Checks with no finding

- `AGENTS.md:3` says role scopes are declared and not yet enforced. That no longer claims present enforcement. Its narrower claim that Item 3 renders sandbox settings and sparse-checkout setup matches the three artifacts emitted per role by `scripts/render_access.py`.
- `threats/threats.yaml` marks T1-T4 `platform` and T5-T8 `project`. No active gate declares T1-T4. `gates/fixtures/fail_platform.yaml` is an intentional negative fixture, and the validator rejects it with exit 1.
- Ledger values required to remain unmeasured are `MEASURE`: C by T2.4; S by T4.3; Repair budget by T4.3; sigma_d/N_min/MDE by T2.5. The numeric `delta`, `k`, `n_cand`, and clustering thresholds are frozen initiation values rather than unmeasured quantities.
- The S amendment is append-only: it retains `previous_value: 5 provisional`, records `new_value: MEASURE`, and adds `new_measured_by: T4.3` with the correction reason.
- Every local helper or sibling-source file referenced by `docs/assets.md` exists. The unresolved angle-bracket values are documented future URLs, queries, or release pins rather than filenames asserted to exist.

No reasoning finding was raised in this verification.
