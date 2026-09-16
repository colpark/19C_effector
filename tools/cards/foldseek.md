# Foldseek tool card

- Version: `10-941cd33`; local binary reports `941cd33ff0771cd2e3f144e3293e22a2b87e9fda`.
- Tier-1 command: `foldseek easy-cluster INPUT OUTPUT TMP --alignment-type 1 --tmscore-threshold TAU --cluster-mode 1`.
- Alignment type: `1`; cluster mode: `1`; logged coverage is `-c 0.8 --cov-mode 0`; TM-score thresholds: 0.40, 0.50, and 0.60.
- Quantity returned: clusters of model structures under the stated structural-alignment and
  TM-score threshold. It is a proxy for independent fold families, not an assay label.
- Reproducibility finding: the earlier 79-cluster claim for the 89-model TM 0.50 subset has no
  retained command output and cannot be reproduced. The logged current command returns 71. The
  corrected 502-model inputs exclude the stray uncontracted `H1VSQ9` PDB.
- Defining paper: UNFILLED — established by T3.1.
- Benchmark accuracy against the scored measurement: MEASURE — measured by T3.1.
- Disagreement list: []
