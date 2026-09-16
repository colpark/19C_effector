# Canonical profile definition

Frozen 2026-09-15 before computing stratum sizes.

`canonical` means both:

- sequence length is at most 300 amino acids;
- the sequence contains at least 4 cysteine residues.

The length threshold is the EffectorP 2.0 paper's stated small-protein
classifier cutoff (less than or equal to 300 amino acids): Sperschneider et
al. (2018), *Molecular Plant Pathology* 19:2094–2110,
doi:10.1111/mpp.12682, https://pmc.ncbi.nlm.nih.gov/articles/PMC6638006/.

The cysteine threshold is the same paper's stated small, cysteine-rich
classifier cutoff (at least 4 cysteines): Sperschneider et al. (2018),
*Molecular Plant Pathology* 19:2094–2110, doi:10.1111/mpp.12682,
https://pmc.ncbi.nlm.nih.gov/articles/PMC6638006/.

The positive union is already restricted to curated fungal or oomycete
effector records with functional evidence. Secretion is therefore a
source-level eligibility claim in this stage; it is not rerun with SignalP,
TMHMM or Phobius, which remain licence-blocked. The two adjectives left
undefined by `handoff/w1/axes.yaml` are the two numeric predicates above.
