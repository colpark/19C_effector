# Structured arm-surface contract

This contract implements Items 92, 94, 98 and 99. It is a pre-build specification, not evidence that the current command-enabled role surface complies. All operations are local, typed, candidate-scoped, and return evidence—not a ranking, aggregate, or selected set.

| Operation | Typed arguments | Returns | Card / status |
|---|---|---|---|
| `get_candidate_record` | `candidate_id: CandidateId` | frozen sequence, organism, length, opaque ID | cohort manifest; build required |
| `signal_peptide_evidence` | `candidate_id: CandidateId` | component call and confidence for one candidate | SignalP card; licence-blocked |
| `profile_hmm_hits` | `candidate_id: CandidateId, profile_set: Enum` | named hit records and alignments | HMMER card; card required |
| `sequence_homology_hits` | `candidate_id: CandidateId, database: Enum, limit: Int[1,20]` | fixed-database hit records | MMseqs2 / BLAST+ cards; BLAST card required |
| `physicochemical_features` | `candidate_id: CandidateId` | declared simple features | pepstats component; card required |
| `carbohydrate_domain_hits` | `candidate_id: CandidateId` | named dbCAN/HMM hits | dbCAN component; card required |
| `structure_coordinates` (arm 4) | `candidate_id: CandidateId` | local coordinates and pLDDT, no class score | ESMFold card |
| `structure_similarity_hits` (arm 4) | `candidate_id: CandidateId, database: Enum, limit: Int[1,20]` | fixed-database structural hit records | Foldseek card |
| `protein_embedding` (arm 4) | `candidate_id: CandidateId, pooling: Enum` | carded fixed ProtT5 representation vector, without class prototypes or score | ProtT5 card; model hash, pooling, dimension and determinism must be carded |

`CandidateId`, `Enum`, and bounded `Int` are schemas, not strings interpreted by a shell. The server maps IDs to frozen local records and databases; it accepts neither arbitrary paths nor URLs. Uncarded or licence-blocked operations are unavailable, not silently substituted.

## Excluded operations

| Excluded operation | Reason |
|---|---|
| Predector rank / candidate list | Floor C composite; returns completed decision. |
| PEACE calibrated probability | trained integrated ensemble score, not component evidence. |
| EffectorP class score / label | trained soft-voted class likelihood; sorting completes the decision. |
| PEACE prototype distance or per-view class-prototype distance | label-targeted score; sorting by the effector prototype completes the decision before calibration or aggregation. |
| aggregate score, rank, top-k, recommendation, selected set | pre-solves composition. |
| shell, Python, arbitrary code, package install, write | enables unbounded network/file escape. |
| URL, filesystem path, arbitrary database, dynamic MCP registration | can dereference content or create capability. |
| remote model-derived score or raw fetched error body | can relay withheld output/content. |

## Mandatory negative probes and grant verification

The Instrument must retain rejection traces for: command/shell requests; code-bearing or shell-metacharacter arguments; URL or path arguments; dynamic tool/MCP registration; induced upstream errors whose body is replaced with a fixed local error code; and a request for a remotely derived score. All fail closed without outbound content.

Model-side arm-3 grant verification is a recorded attempt to invoke each withheld foundation tool, followed by the typed registry and call trace showing no such tool exists or ran. This proves exposed-surface absence only; unlike a network refusal, it does not prove every host process lacks the endpoint. That weakening is part of every resulting claim.
