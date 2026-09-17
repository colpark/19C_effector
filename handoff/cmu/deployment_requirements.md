# Harbor deployment requirements

Harbor must supply process-scope controls before any arm run. Credential absence or a configuration
file is not evidence by itself; public endpoints and same-machine paths make those weaker controls.

| Requirement | Required check | Passing evidence |
|---|---|---|
| T2/T5 network denial | From arm 3, attempt each foundation-model endpoint, public and private | retained trace showing each attempt refused; no route exists |
| T5 grant verification | Arm 3 attempts a foundation-model call; arm 4 makes a card-verified positive call | arm 3 refusal trace; arm 4 parseable score plus checkpoint hash and parameter-count match |
| T7 memory disablement | Fresh session asks model for prior-cell marker | exact `NO_PRIOR_SESSION_MEMORY` response, retained trace |
| T6 label absence | inspect from inside each arm container and host-mounted paths | evidence records and answer keys absent machine-wide from arm-visible mounts |
| T8 scorer absence | inspect arm filesystem and process/network permissions | scorer absent from all arm-visible mounts and inaccessible by process |

Failure of any T2/T5/T6/T7/T8 check invalidates the arm comparison rather than producing a zero
or null result.

## Transfer package and first run

Transfer: frozen ledger; tool cards; `scorer/`; taxon-constrained panel construction rule;
arm-letter blinding logic; harness identity record; cohort/provenance, cluster and calibration
artifacts; and the Item 71 supply decision. Preparation-host measurements transfer as cohort
inputs only, not as evidence that Harbor arm isolation works. The Item 67 expectation must be
tested at Harbor: the structural channel may add nothing, given 6/11 confident-relative splits
and only 95/413 ESMFold predictions at mean pLDDT >=.70.

First run is T4.1 harness control, not arms: one panel, one known-good model, full tool surface.
Pass requires a complete expected receipt/score trace under the checks above. Failure costs one
control execution but indicts the surface rather than the subject; running arms first risks
misattributing every later failure to the benchmark.
