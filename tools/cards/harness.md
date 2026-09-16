# Harness identity card

## Coding agent

- Agent: OpenAI Codex
- Local CLI version: `codex-cli 0.154.0` (`codex --version`, measured 2026-09-15)
- Model: `gpt-5.6-sol`
- Host: `Linux 6.11.0-1014-nvidia aarch64`
- Card source revision: `1389f5d906e745221f320489bbc90dcdfc1672e7`

This identifies the Week 0 remediation authoring harness. It is not a subject-model checkpoint or an effector tool card.

## Resolved authoring sandbox

- Filesystem sandbox: `danger-full-access` / unrestricted
- Network access: enabled
- Approval policy: `never`
- Shell: Bash

The authoring harness is intentionally recorded as it actually ran. These permissions must not be inferred for any benchmark role.

## Rendered role sandbox

All six Codex profiles resolve to `sandbox_mode = "workspace-write"` and
`trust_level = "untrusted"` for the standalone role clone. The Fetcher and the Item 30
Adversary probe resolve `sandbox_workspace_write.network_access = true`; the
other four roles resolve it to `false`. The Fetcher's narrow domain
allowlist is represented in the Claude profile; Codex 0.154.0 exposes a Boolean
workspace-write network setting rather than the rendered domain allowlist. All
six Claude settings resolve `sandbox.enabled = true`,
`sandbox.failIfUnavailable = true`, `sandbox.allowUnsandboxedCommands = false`,
and `sandbox.network.strictAllowlist = true`. Filesystem paths, command rules,
and MCP-policy values remain role-specific. Docker is an excluded command for
every Claude profile and a forbidden Codex command for every role.

The aggregate below is SHA-256 over the lexically sorted `sha256sum` records
for all thirty-six rendered artifacts: six each of the Claude JSON settings,
Codex TOML configs, Codex execpolicy rule files, framework-neutral access
policies, standalone manifests, and clone builders.

`715cb4756ca06a759ee22e12c7349fdfe5008f2bbfebbeb6f4e626cb67574348`

Regenerate with `python3 scripts/render_access.py --all`. A changed aggregate
changes the harness identity and must be recorded before a run.

## Role launcher

`scripts/launch_role.sh` starts an ephemeral Codex session in the selected
standalone clone on a different, union-free host, explicitly layers the
rendered TOML with `--profile`, loads the
rendered exec-policy rules from the isolated runtime home, selects
`workspace-write`, and sets approval to `never`. It prepends the current
constitution to the supplied stage body.

The 2026-09-15 Curator launch failed at network-namespace loopback setup. The
Item 30 network-enabled Adversary relaunch exposed the independent Bubblewrap
uid-map denial. Neither requested assertion command started. Verbatim results
are retained in `handoff/gate0/boundary_probe_2.md` and
`handoff/gate0/host_escalation.md`; these are not evidence that denied reads are
enforced.
