# Instrument boundary probe

> Superseded admissibility marker: this is historical probe evidence; read Item 79--84 in `ledger/ledger.yaml` for the current condition.

No claim from this artifact is admissible until the runtime boundary holds.

Command: `scripts/assert_sandbox.sh instrument`  
Exit status: `1`

```text
FAIL instrument: T1 UNMEASURABLE: path absence is not a running process sandbox
PASS instrument: ABSENCE /home/aid1/Documents/3_19C_effector/role_clones/instrument/data/labels
PASS instrument: ABSENCE /home/aid1/Documents/3_19C_effector/role_clones/instrument/data/scored_cohort
PASS instrument: ABSENCE /home/aid1/Documents/3_19C_effector/role_clones/instrument/scorer
FAIL instrument: T2 connection to non-allowlisted host example.com succeeded
FAIL instrument: T3 package install outside the writable list succeeded
FAIL instrument: T4 write outside the role writable list succeeded
T7 MODEL-SIDE PROBE: in a fresh session, answer exactly NO_PRIOR_SESSION_MEMORY unless a marker from a prior session is available
FAIL instrument: T7 UNMEASURABLE: caller did not supply the model-side answer file
```
