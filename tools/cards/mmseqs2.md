# MMseqs2

- **Identity:** MMseqs2 `8cc5ce367b5638c4306c2d7cfc652dd099a4643f`, from the
  pinned `18-8cc5c` archive (SHA-256
  `06c9a031331562e37eed3da79ef859d30a1a3ac5c5e334411dfaee5da5e9c0d0`).
- **Use in Tier 1:** the 30% sequence-identity axis, replacing CD-HIT outside
  its supported word-size range.
- **Command:** `mmseqs easy-cluster union.fasta OUT TMP --min-seq-id 0.3 -c 0.8 --cov-mode 0`.
- **Quantity returned:** sequence-similarity clusters, not structural-fold
  families.  The 80% coverage requirement uses coverage mode 0.
- **Observed result:** 430 clusters among 521 retained positives.  This repairs
  the missing 30% sequence-axis measurement; it does not substitute for
  Foldseek on the structural axis.
