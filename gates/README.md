# Gate controls

A gate is unarmed until both its must-fire and must-not-fire controls have run successfully. At least one control for every gate must derive from a seed in `seeds.yaml`.

Stop-condition files use this schema:

```yaml
stop_conditions:
  - id: unique-condition-id
    threat: T5
    predicate: "T5 occurs when an arm reaches a capability withheld by its grant"
```

Predicates identify a protected threat, not a tool, package, or filename. Validate every declaration before arming it:

```bash
python3 scripts/validate_stop_conditions.py gates/fixtures/pass.yaml
```

T1, T2, T3, and T4 are platform-enforced threats. They receive startup assertions in `scripts/assert_sandbox.sh` and do not receive project gates. A gate over a platform-enforced threat is a proxy and fails validation. Only project-enforced threats T5, T6, T7, and T8 may appear in gate declarations.

The runtime must attest `SANDBOX_ACTIVE=1`, `SANDBOX_NETWORK_ALLOWLIST_ENFORCED=1`, `SANDBOX_PACKAGE_INSTALL_BLOCKED=1`, and `SANDBOX_WRITE_BOUNDARY_ENFORCED=1`; fallback and unsandboxed retry must remain off. These assertions bind platform enforcement to the running process rather than to configuration text alone.
