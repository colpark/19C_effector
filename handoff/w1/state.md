# State at recovery

## Files absent from `8b108b1`

| Path | Purpose |
|---|---|
| `docs/papers/peace_2026.pdf` | Supplied PEACE preprint, DOI `10.64898/2026.04.19.719514`. |
| `handoff/gate0/findings_verifier.md` | Verifier findings recovered from the interrupted worktree. |
| `handoff/w1/grant_verification.md` | Four-arm, trace-based grant checks, including the coupled arm 3 negative and arm 4 positive checks. |
| `handoff/w1/scorer_findings.md` | Records the corrected chance-precision formula and panel-level pairing rule. |
| `scripts/build_union_positives.py` | Interrupted union-positive curator; parses PHI-base, Predector, PEACE, taxonomy and UniProt inputs and emits FASTA, provenance and a count summary. It has not yet met T1.2's exit criterion. |
| `data/raw/peace/docs/DATASET_CONSTRUCTION_GUIDE.md` | PEACE dataset-construction documentation. |
| `data/raw/peace/src/data/dataset_construction/combined_positives.csv` | PEACE combined positive metadata. |
| `data/raw/peace/src/data/dataset_construction/combined_positives_deduplicated.fasta` | PEACE deduplicated positive sequences. |
| `data/raw/peace/src/data/dataset_construction/positive_seqs/*.fasta` | Ten PEACE input sets: EffectorP 1/2/2-validation/3, EffHunter, Predector, WideEffHunter, Fungtion, FunEffector-Pred and POOE. |
| `data/raw/predector/data/fungal_effectors.tsv` | Predector's confirmed fungal-effector table. |
| `data/raw/sources/phi-base_v4-19_2026-02-27.csv` | PHI-base 4.19 interaction records. |
| `data/raw/sources/phi-base_v4-19_2026-03-01.fas` | PHI-base 4.19 protein sequences. |
| `data/raw/sources/ncbi-taxdump-2026-09-15.tar.gz.md5` | Publisher checksum for the taxonomy snapshot used for clade filtering. |

## Step 1 execution check

| Part | Files checked | Executed result |
|---|---|---|
| 1a | `ledger/ledger.yaml` | The seven values are present with amendment chains: alpha 0.05, beta 0.20, five positives per panel, arm4-minus-arm3 panel pairing, within-cell mean aggregation, leave-one-item-out H, and lifestyle grouping. |
| 1b, scorer pairing and chance | `scorer/score.py`, `scorer/synthetic.py`, `scorer/test_score.py` | `python3 -m unittest -v test_score` from `scorer/`: 7 tests ran, all passed, including the two regression tests. |
| 1b, headroom and split fields | `floor/headroom.py`, `floor/test_floor.py` | `python3 -m unittest -v test_floor` from `floor/`: 6 tests ran, all passed, including the two regression tests. |
| 1c | `handoff/w1/grant_verification.md`, `tasks/register.csv` | The document contains checks for all four arms and makes failed arm-4 verification a coverage failure. T3.7 is amended to `specified`. |

Step 1 is already implemented and verified. It will not be redone.

## Real checksums in `docs/assets.md`

| Asset | SHA-256 |
|---|---|
| PEACE defining preprint | `6fa3458d7e9bb2a72827934a7e014cd97e13ef5015820d8cbb2876768b414a48` |

All other asset checksum cells still read `PENDING` at this checkpoint.
