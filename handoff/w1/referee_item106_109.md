# Referee Items 106--109: label-score symmetry

An operation is inadmissible when it returns a label-targeted class probability, score, label,
rank, or class-prototype distance for the scored task such that one call per candidate followed
by sorting yields the completed answer. The criterion does not depend on a tool's provenance or
on how many internal models it aggregates. Aggregation is diagnostic only: a single-model class
score also fails, while a multi-model representation of a different quantity may pass.

## Surface status

| Operation class | Status | Reason |
|---|---|---|
| Candidate record; signal component; HMM, homology, physicochemical, domain evidence | admitted when carded | evidence is not itself the scored-task answer |
| Structure coordinates/pLDDT; structural hit records | admitted for arm 4 | structural quantities, not effector-likelihood labels |
| Fixed unlabeled ProtT5 embedding | conditional arm-4 admission | card model hash, pooling, dimension, determinism; expose no class head/prototypes |
| EffectorP soft-voted class score | excluded | label likelihood; sorting completes decision |
| Predector rank | excluded / Floor C only | fixed composite completed decision |
| PEACE calibrated probability | excluded | calibrated prototype-distance classifier score |
| PEACE uncalibrated prototype or per-view class distance | excluded | class-targeted distance; sorting toward effector prototype completes decision |

PEACE can re-enter only through the fixed raw ProtT5 embedding interface, not through a
prototype-derived value. This is a narrower foundation-model capability and requires carding the
served model, extraction/pooling rule, vector dimension, determinism, and proof that class
prototypes and score heads are unreachable.

## Structural-channel test before arms

On the frozen design split, compare the fixed classical mechanical composition with the same
composition plus structural coordinates/hits, using paired precision@20 per panel. The structural
channel is judged to add nothing if its paired mean gain is below .01 **or** its paired 95% interval
includes zero. This threshold is fixed before implementation. If it fails, arm 4 has no
demonstrated signal-bearing unique grant, so the structured-agent benchmark closes without arm
calls. If it passes, the remaining claim is a structured-agent comparison using representation
and structural evidence, not PEACE/Predector decision scores.

## Claim boundaries

| Outcome | Claim | Worth making? |
|---|---|---|
| Carded unlabeled PEACE embedding plus structural signal | structured-agent benefit from foundation representations/structure, not PEACE classifier access | yes, narrow and testable |
| PEACE stays out; structural signal passes | structured-agent benefit from structural evidence only | yes, narrower but direct |
| PEACE stays out; structural signal fails | no unique signal-bearing arm-4 capability | no; close before arms |

These rulings strengthen the validity of the composition claim while weakening arm-4 power and
the breadth of the eventual claim. Overall they push toward closure unless the preregistered
mechanical structural-channel test shows signal.
