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
`trust_level = "untrusted"` for the role worktree. The five panel roles resolve
`network_access = false`; the Fetcher resolves `network_access = true` with a
non-empty allowlist. All six Claude settings resolve `sandbox.enabled = true`,
`sandbox.failIfUnavailable = true`, `sandbox.allowUnsandboxedCommands = false`,
and `sandbox.network.strictAllowlist = true`. Filesystem paths, command rules,
and MCP-policy values remain role-specific. Docker is an excluded command for
every Claude profile and a forbidden Codex command for every role.

The aggregate below is SHA-256 over the lexically sorted `sha256sum` records
for all twenty-four rendered settings and policy artifacts: six Claude JSON
settings, six Codex TOML configs, six Codex execpolicy rule files, and six
framework-neutral access-policy manifests.

`fee1414f9cdaca15858febd94c3bc63d17ee8eee78ffe4cb701d0cba111531a6`

Regenerate with `python3 scripts/render_access.py --all`. A changed aggregate
changes the harness identity and must be recorded before a run.
