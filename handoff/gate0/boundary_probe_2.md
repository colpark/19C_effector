# Item 19 launched Curator boundary probe

Date: 2026-09-15

The Curator session was started by `scripts/launch_role.sh curator`. Codex
accepted the explicit rendered profile after its unsupported top-level
`network_access` key was moved to `sandbox_workspace_write.network_access`.
The launcher exited `0`, but Bubblewrap could not create the network namespace.
The requested `assert_sandbox.sh curator` process therefore never started.
This is a failed boundary assertion, not a pass.

## Complete launcher output (verbatim)

```text
OpenAI Codex v0.154.0
--------
workdir: /home/aid1/Documents/3_19C_effector/role_worktrees/curator
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, /home/aid1/Documents/3_19C_effector/role_worktrees/curator/handoff, /home/aid1/Documents/3_19C_effector/role_worktrees/curator/data/positives, /home/aid1/Documents/3_19C_effector/role_worktrees/curator/data/labels, /home/aid1/Documents/3_19C_effector/role_worktrees/curator/data/scored_cohort, /home/aid1/Documents/3_19C_effector/role_worktrees/curator/tools/cards]
reasoning effort: none
reasoning summaries: none
session id: 01a0a6c2-4539-7533-9c87-fdd2359a8ec8
--------
user
# Effector Benchmark Constitution

1. Count the scarce unit, not the abundant one. Cluster before counting. Report every axis together or report none.
2. A tool must measure the quantity the task scores on. Justify a substitute against that quantity, never against the tool it replaces.
3. The served checkpoint belongs to the tool's identity. Record its hash, parameter count and revision on the card.
4. No tool that helps produce an answer may also score it.
5. Build and measure the comparator before installing the foundation model.
6. Gates fire on the protected quantity, stated as a threat, never on a tool name.
7. A gate arms only after both its must-fire and its must-not-fire control have run.
8. Hash what the runner emits, compare against the specification, and block the run on divergence.
9. Report the decision metric with its chance baseline and with the strongest existing adjudicator. Publish MDE(N) beside every effect.
10. Invalid answers are coverage failures, never zeros. The repair budget stays identical across arms and gets declared in advance.
11. Arms differ only in grant. Verify every grant from the model's side.
12. Preregistered values live in the ledger. Reports read the ledger rather than restating it.
13. A blocked item is recorded in `handoff/gate0/blocked.md` before the session ends, and silence is not a report.

Run /home/aid1/Documents/3_19C_effector/bench/scripts/assert_sandbox.sh curator exactly once through Bash. Do not modify repository files and do not repair failures. In your final answer, reproduce the command standard output and standard error verbatim, with no summary.

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
I’ll run the specified sandbox assertion once and make no repository changes.
codex
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
tokens used
9,951
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

## Boundary result

```text
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
```

The rendered profile was applied: Codex reported `approval: never` and the
role-specific `workspace-write` roots. Sandboxing then failed closed before the
Bash probe could execute. Denied-path reads have still not been demonstrated to
fail from a working launched role session.
