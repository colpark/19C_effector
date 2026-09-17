# SCOP substitute proposal — no calibration run

> Superseded admissibility marker: read Item 79--84 in `ledger/ledger.yaml` before reusing this historical proposal.

ECOD remains unreachable from a rendered Fetcher scope, so the naturally
low-confidence calibration cannot currently meet the ledger's ECOD-family requirement.
No claim from this artifact is admissible until the runtime boundary holds.

SCOP, available through PDBe's `https://www.ebi.ac.uk/pdbe/api/mappings/scop/<PDB>`
endpoint, is proposed as a fallback family source. Like ECOD, SCOP classification is
independent of ESMFold and would supply a pre-prediction family label. It loses ECOD's
intended broad coverage and its ECOD-family granularity; PDBe's mapping also covers
only structures with a SCOP mapping. The earlier rejection of SCOP was not an
independence defect—it was adherence to the then-explicit ECOD requirement.

This proposal does not silently overturn that requirement. Item 51 currently requires
an ECOD calibration, so only the Referee may amend the ledger to authorize SCOP, state
the coverage loss, and decide whether a SCOP-derived rate can satisfy Item 48. No pool,
prediction, confidence selection, rate, or transfer was run.
