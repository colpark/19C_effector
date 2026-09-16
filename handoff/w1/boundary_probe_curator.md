# Curator boundary probe

Command: `scripts/assert_sandbox.sh curator`

Exit status: `1`

Verbatim output:

```text
rendered settings absent; run scripts/render_access.py curator
```

The boundary did not hold. Per the stage instruction, measurement continues, but
no claim from this stage is admissible until this boundary is restored and passes.
