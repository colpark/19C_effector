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

