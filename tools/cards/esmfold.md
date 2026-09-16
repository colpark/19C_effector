# ESMFold tool card

- Quantity returned: predicted PDB coordinates with per-residue pLDDT encoded in CA B-factors
- Defining paper: UNFILLED — established by T3.1
- Benchmark accuracy against the scored measurement: MEASURE — measured by T3.1
- Served checkpoint hash: `2ee07356b125d1e3e57503c204111fd7323347fc4735d41d3caac57c2a78e116` — SHA-256 of locally loaded `pytorch_model.bin`
- Parameter count: `3,525,038,915` — measured by `sum(p.numel() for p in EsmForProteinFolding.from_pretrained(...).parameters())`
- Revision: `facebook/esmfold_v1` revision `75a3841ee059df2bf4d56688166c8fb459ddd97a`
- Origin: local Hugging Face cache `~/.cache/huggingface/hub/models--facebook--esmfold_v1/snapshots/75a3841ee059df2bf4d56688166c8fb459ddd97a/`; reused through sibling wrapper `../../2_19C_biology/benchmark-mcp/esmfold_worker.py` (directory exists but is not a Git checkout, so no commit SHA is available)
- Disagreement list: []
