# Canonical profile definition

Frozen 2026-09-15 before computing stratum sizes.

`canonical` means all three:

- sequence length is at most 300 amino acids;
- the sequence contains at least 4 cysteine residues.
- no pinned curated source record explicitly identifies the protein as
  non-classically secreted.

The length threshold is the EffectorP 2.0 paper's stated small-protein
classifier cutoff (less than or equal to 300 amino acids): Sperschneider et
al. (2018), *Molecular Plant Pathology* 19:2094–2110,
doi:10.1111/mpp.12682, https://pmc.ncbi.nlm.nih.gov/articles/PMC6638006/.

The cysteine threshold is the same paper's stated small, cysteine-rich
classifier cutoff (at least 4 cysteines): Sperschneider et al. (2018),
*Molecular Plant Pathology* 19:2094–2110, doi:10.1111/mpp.12682,
https://pmc.ncbi.nlm.nih.gov/articles/PMC6638006/.

The positive union is already restricted to curated fungal or oomycete
effector records with functional evidence. Classical secretion is evaluated
from those pinned records; it is not rerun with SignalP, TMHMM or Phobius,
which remain licence-blocked. The two adjectives left undefined by
`handoff/w1/axes.yaml` are the two numeric predicates above.

## Prespecified exception check and revision

The initial numeric-only rule called two named exceptions canonical:
FolSix12 (42 aa, 4 cysteines) and BgtAVRa10 (286 aa, 4 cysteines). Predector's
pinned records explicitly describe both as non-classically secreted. The
definition was therefore revised before cohort counting to include the third
predicate above. BghBEC3 (114 aa, 1 cysteine), FocSix8 (187 aa, 2 cysteines)
and Vdlsc1 (190 aa, 1 cysteine) already failed the numeric predicates; Vdlsc1
is also explicitly annotated as non-classically secreted.
