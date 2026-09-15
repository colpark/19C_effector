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

All five Item 3 Codex profiles resolve to `sandbox_mode = "workspace-write"`, `network_access = false`, and `trust_level = "untrusted"` for the role worktree. All five Claude settings resolve `sandbox.enabled = true`, `sandbox.failIfUnavailable = true`, `sandbox.allowUnsandboxedCommands = false`, and `sandbox.network.strictAllowlist = true` with an empty host allowlist. Filesystem allow/deny paths remain role-specific.

The aggregate hash below is SHA-256 over the lexically sorted `sha256sum` records for all ten rendered settings files:

`69d639591f8c794a7c7d6462e1ca8f64755d295821227c5e696b685b31fa33ef`

| Role | Claude settings SHA-256 | Codex config SHA-256 |
|---|---|---|
| Curator | `bc9751fb914f28f90f301e54b1ccad4ab562e703b426b4de59cd8a504464a0e9` | `888fa5146e02fa373c2d5f51929804640c641d251712ac7e85114c574a18befb` |
| Instrument | `102a4bdaf9b59898df2c58fab03f593cff3ca2f7ae7a7e5c62e12bc9a839e675` | `d9094e6ce6a259075e01ca5988be125044cacd2092476d6a6a8305d8a0968120` |
| Floor | `bba9b836e34ee8fc2ea1782a1851801b55c5e304139b09f41549acbb2e663a52` | `af16076845e03b75f056d536d1f7d099e6238c16a828c040c409b93115623d12` |
| Referee | `fed49dfed2109009b344da67fd841716390e939bf51034784391ccd6b0e7fc06` | `5f73e7ab4271d21ba1bef304d9b71f7f6378a332bb25cb9a290db8fcf05f6669` |
| Adversary | `1c3986c31d44ec0a81dbe475e286b6392188e24e2b8671bccf65d6ed040755b3` | `bfc377f0eb9708d6f0fee9efd30f0cb947c6789b58305f0ad61e7ae252b4b03f` |

Regenerate with `python3 scripts/render_access.py --all`. A changed aggregate or per-file hash changes the harness identity and must be recorded before a run.
