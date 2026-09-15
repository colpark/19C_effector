# Effector Benchmark Panel Charter

The constitution is prepended to every stage prompt. Role scopes are declared by `access/*.yaml` but are not yet enforced; remediation Item 3 will render the load-bearing sandbox settings and sparse-checkout setup. Cross-role state moves only through append-only files under `handoff/`. The Instrument alone holds the mapping from blinded arm letters to grants.

No panel session is launched during Week 0. The role worktrees are materialized only so their filesystem boundaries can be verified.

## Curator

- Holds: PHI-base, UniProt, MycoCosm, RNA-seq archives, CD-HIT, Foldseek, ESMFold, positive provenance, functional labels, and the scored cohort.
- Denied: `scorer/`, `runs/`, every arm output, and the design split after freeze.
- Owns: T1.1-T1.6, T3.4, T5.2, T5.3, TL.1.
- Bound by: T2 network reach beyond the allowlist, T6 label leakage, and the Gate 1 supply predicate.

## Instrument

- Holds: filesystem state, served endpoints, tool source, cards, configurations, run traces, and blinded arm mapping.
- Denied: `data/labels/` and answer keys.
- Owns: T0.4, T2.3 checkpoint verification, T3.1-T3.3, T4.3, T5.4.
- Bound by: T1-T5, T7-T8; a hash or served-checkpoint mismatch blocks execution directly.

## Floor

- Holds: fixed tools and `data/design_split/`.
- Denied: `data/scored_cohort/`, `data/labels/`, `runs/`, and agentic arm output.
- Owns: T2.1-T2.7.
- Bound by: T5-T6 and the Gate 2 headroom predicate. It reports H but does not rule on continuation.

## Referee

- Holds: preregistration, ledger, labels, scored cohort, and `scorer/`.
- Denied: `runs/`, tool traces, the arm identity map, and unblinded arm names.
- Owns: T0.1, T0.2, T4.2, T5.1, T5.5, T5.6; only this role may amend the ledger.
- Bound by: T6-T8, metric primacy, coverage semantics, and identical repair budgets.

## Adversary

- Holds: traces, gate declarations and controls, served configuration, and literature.
- Denied: authoring items, floors, labels, cohorts, or scorer state; `data/` and `scorer/` are absent.
- Owns: T0.3, T3.5-T3.7, T4.1, TV.2.
- Bound by: all eight threats. It refuses to arm a gate until must-fire and must-not-fire controls both pass.

## Convening and decision rights

- Findings are written independently to `handoff/gate_N/findings_<agent>.md` before synthesis.
- Findings sharing one evidence source count once. Instrument or Adversary findings grounded in files, traces, or served state are factual and block; design arguments are reasoning findings and go to discussion.
- The Referee rules on the Floor's H and alone appends ledger amendments.
- The Instrument blocks prompt/config divergence before execution.
- The Adversary controls gate arming.
