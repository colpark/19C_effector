# False-singleton calibration card

No claim from this artifact is admissible until the runtime boundary holds.

## Measurement

This attempted to measure the probability that an ESMFold-predicted member of a
known structural family is placed in a singleton Foldseek cluster rather than with
its own family. Twenty public PDB controls were fixed from five PDBe SCOP-mapped
families (four structures each): ubiquitin-like, lysozyme-like, thioredoxin-like,
ribonuclease-A-like and beta-lactamase-like. PDBe SCOP mapping verified the stated
SUNID for every control. MMseqs2 `easy-search --min-seq-id 0.3 -c 0.8 --cov-mode 0`
against all 521 cohort positives removed zero controls at the stated threshold.

The controls are generic globular proteins, not effector folds. Candidate effector
folds did not leave four independent, cohort-nonoverlapping solved members in the
locally available annotation sources. That substitution limits transfer to
disulfide-stabilised effectors.

## Methods and result

ESMFold v1 revision `75a3841ee059df2bf4d56688166c8fb459ddd97a` predicted 20
variants for each separate method: 50% N-terminal truncation, mutation of up to
eight position-index conserved residues, and a full-length within-set orphan proxy.
Foldseek used its carded structural alignment type 1, cluster mode 1 and TM 0.40,
0.50, 0.60 command.

None of the methods matched the frozen cohort target (mean pLDDT <0.50, median
0.408): method medians were 0.895, 0.903 and 0.936, with Wasserstein-1 distances
0.440, 0.459 and 0.518. Each gave 1/20 singletons (5%, 95% Wilson 0.9–23.6%) and
0/20 wrong-family joins (0–16.1%) at every TM threshold. The full-length proxy is
the undegraded control baseline. These rates are recorded but **do not qualify for
transfer**: they measure high-confidence generic control behaviour, not uncertain
effector-like behaviour.

## What this does not cover

Truncation and conserved-site mutation may change a protein's actual fold, so an
original-family label is only provenance, not experimental ground truth for the
variant. The orphan method is a within-set sequence-divergence proxy, not a verified
shallow natural-alignment measurement. No method generated the target confidence
distribution; consequently no corrected cohort count, panel count or MDE is supplied.

## Disagreement list

- Target manifest contains 189, not the prompt's stated 192, models below 0.50.
- The calibration controls are generic globular structures rather than the requested
  effector folds.
- All perturbation methods stayed much more confident than the target; their rates
  disagree in scope, not materially in point estimate.
