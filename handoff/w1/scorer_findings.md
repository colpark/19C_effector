# Scorer repair findings

Date: 2026-09-15

The framework expression `k / n_cand` is chance recall, not chance precision at
`k`. With five planted positives among 500 candidates, chance precision at 20 is
`5 / 500 = 0.01`; the former implementation reported `20 / 500 = 0.04`. The
scorer now reads `positives_per_panel` from the ledger and reports
`positives_per_panel / n_cand`, so a later change to `k` cannot reintroduce this
constant error.

Replicate identifiers are not pairing keys. Valid replicates now aggregate to
one mean precision-at-k value per arm and panel, and the primary arm comparison
pairs those cell means on `panel_id`. Every reported cell includes its valid
replicate count.
