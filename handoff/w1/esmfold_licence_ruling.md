# ESMFold licence ruling

Boundary status: `scripts/assert_sandbox.sh curator` exited 1; no claim from
this stage is admissible until the boundary holds.

The cached checkpoint snapshot contains only `config.json` and
`pytorch_model.bin`; it ships no licence file. The pinned Hugging Face model
metadata for `facebook/esmfold_v1` revision
`75a3841ee059df2bf4d56688166c8fb459ddd97a` reports licence identifier `mit`.

The actual upstream ESM repository licence was read from
`/tmp/esm-license.oqrjfL/LICENSE`. Its identifier is `MIT License`; its grant
begins verbatim: `Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction`.

Ruling: ESMFold inference on the union positives is permitted. The earlier
statement that ESMFold required an asset outside the permitted scope was wrong:
it incorrectly extended the freeze on SignalP, TMHMM, Phobius, MycoCosm and
EffectorP binaries to the openly released ESMFold checkpoint. The model is
used for structural cohort construction only, not labels or scoring.
