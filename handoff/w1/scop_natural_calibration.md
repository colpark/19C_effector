# Instrument SCOP natural-confidence calibration — transfer refused

> Superseded admissibility marker: read Item 79--84 in `ledger/ledger.yaml`; the historical runtime caveat below is not the current condition.

A deterministic, confidence-blind draw of 240 current PDB entries produced 38 PDBe SCOP-mapped entity-1 sequences. Thirty-six passed the predeclared MMseqs2 contamination screen against the 521-positive cohort; two were removed above 30% identity and 80% coverage. ESMFold could predict 34 of the 36 without degradation; one was over 600 residues and one contained `X`. Exactly one of the 34 predictions fell in the frozen target band, a 2.9% yield. It is a coronavirus nucleocapsid protein dimerization-domain SCOP class, not an effector-like class. This does not meet five-family or three-confident-relative transfer validity, and one value cannot match a distribution. No claim from this artifact is admissible until the runtime boundary holds.

## Source and pool

The authorised source is SCOP through the PDBe mapping endpoint, authorised by Referee Item 58 after the official ECOD endpoint failed from a Fetcher allowlist (curl exit 7) and a Fetcher GitHub mirror candidate returned HTTP 404. SCOP is independent of ESMFold but has narrower coverage and coarser families; its downward false-singleton bias must accompany any derived number.

| Pool stage | Count |
|---|---:|
| Deterministic PDB draw, no confidence/fold/size prefilter | 240 |
| PDBe SCOP-mapped | 38 |
| Removed by >30% identity and 80% coverage | 2 |
| Contamination-screen retained | 36 |
| Carded ESMFold-input eligible | 34 |
| In frozen pLDDT band | 1 |

The sole selected record is PDB `2CJR`, SCOP SUNID `143508`: alpha-and-beta (a+b), coronavirus nucleocapsid protein dimerization domain. It has mean pLDDT 0.3482. The target has n=189, median 0.4084, Q1–Q3 0.3684–0.4470, range 0.2813–0.4996. A one-member set has no quartiles; its Wasserstein-1 distance to the target is 0.0656, but that is not a distributional-match claim.

## Transfer decision

The pool has one low-confidence member from one family and no same-family low-confidence replicate. It fails both preregistered transfer conditions: at least five families, and three confident relatives for every retained low-confidence member. It cannot reach the Item 60 20-member stopping ceiling. Foldseek clustering, false-singleton and wrong-family rates, high-confidence baseline subtraction, Wilson intervals, corrected clusters, panels_max, and MDE are **not estimable**. No rate can be compared with 0.8571.

This refusal is due to inadequate SCOP low-confidence yield and family support, not a confidence-match calculation. It does not alter Item 48 and does not convene Gate 1. The Instrument boundary still fails; ECOD remains the only external holder.
