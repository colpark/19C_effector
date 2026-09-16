# Candidate 3 recheck: host-target assignment

PHI-base 4.19 was filtered to fungal or oomycete pathogen taxonomy, a nonempty
`Tested Host_target`, and a positive interaction result. Explicit `no binding`
and `no interaction` records were excluded. The result is 19 distinct
effector–host-target–host-species pairs from 24 source rows, 10 effector
proteins, 14 recorded host-species labels and 11 pathogen species.

The source has no fold-family field. Its fold axis is therefore bounded by the
10 unique effector proteins rather than relabelled from gene names. AlphaFold
DB covers 2/10 of those proteins; Foldseek TM-score 0.50 assigns those two
(Q6PQG3 and Q6PQH2) to separate clusters. The remaining 8 are conservatively
held as singleton fold families. Thus the most generous measured upper bound is
10 fold families, not the approximately 50 independent units required.

The task remains **killed, now on a count**. The 19 pairs are also strongly
concentrated in host systems and do not satisfy the independent-supply claim.
Q4 is `no`: target pairs found by screening an effector nominated through the
classical small-secreted-cysteine-rich lineage are downstream of the instrument
under test.

The surveillance filing in the plan is corrected here: the defect is absence of
a per-item outcome label, an epistemic-label condition, not structural
condition 3.
