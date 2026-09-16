# SCOP family source card — Item 58 substitute

No claim from this artifact is admissible until the runtime boundary holds.

- Source: PDBe SCOP mapping endpoint, `https://www.ebi.ac.uk/pdbe/api/mappings/scop/<PDB_ID>`.
- It supplies: a SCOP structural-family assignment independently of ESMFold, fixed before prediction.
- Authorization: Item 51 amendment `288ba20`, after official ECOD access failed from an allowlisted Fetcher scope (curl exit 7) and an attempted Fetcher GitHub mirror returned HTTP 404.
- Loss versus ECOD: only PDB structures with a SCOP mapping qualify, and SCOP family granularity is coarser. Coarser families are easier to join, bias false-singleton rates downward, and make continuation easier. Every SCOP-based adjusted supply number must carry this substitution.
- It does not supply: complete PDB coverage, ECOD family granularity, an outcome label, or evidence that a SCOP-derived rate transfers to fungal/oomycete effectors.
