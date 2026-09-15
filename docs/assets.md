# Asset inventory

Week 0 inventory only. No command below has been executed. Every checksum remains `PENDING` until T0.5 is reopened under an approved fetch stage. Licence-restricted assets must not be substituted silently.

| Asset | Source or repository | Licence status | Future fetch command | Checksum |
|---|---|---|---|---|
| PEACE code | Project release/contact named in the PEACE preprint (Dai, Lin, Yoo, Liu, 2026) | Confirm with BNL authors | `git clone <PEACE_REPOSITORY_URL> vendor/PEACE` | PENDING |
| PEACE served checkpoint | Xin Dai / BNL model release | Permission and redistribution status pending | `python3 scripts/fetch_authorized_asset.py PEACE_CHECKPOINT` | PENDING |
| PEACE curated CSVs | Xin Dai / BNL project record | Permission and lineage audit pending | `python3 scripts/fetch_authorized_asset.py PEACE_CURATED_CSVS` | PENDING |
| Predector source and workflow | https://github.com/ccdmb/predector | Open-source components; inspect per-tool licences | `git clone https://github.com/ccdmb/predector.git vendor/predector` | PENDING |
| Predector container | Predector release/container registry | Confirm image and embedded-tool licences | `docker pull ghcr.io/ccdmb/predector:<PINNED_TAG>` | PENDING |
| Predector confirmed effector set | Predector publication supplements | Source citation required | `python3 scripts/fetch_authorized_asset.py PREDECTOR_CONFIRMED_SET` | PENDING |
| PHI-base | https://www.phi-base.org/downloadLink.htm | PHI-base terms; functional evidence must be audited | `curl -fL <PINNED_PHI_BASE_URL> -o data/raw/phi-base.zip` | PENDING |
| UniProt reviewed fungal/oomycete records | https://rest.uniprot.org/ | CC BY 4.0 | `curl -fL '<FROZEN_UNIPROT_QUERY>' -o data/raw/uniprot.tsv` | PENDING |
| MycoCosm proteomes and genomes | https://mycocosm.jgi.doe.gov/ | JGI account/terms and project permissions required | `python3 scripts/fetch_authorized_asset.py MYCOCOSM_BULK` | PENDING |
| In-planta RNA-seq | https://www.ncbi.nlm.nih.gov/sra | Public records; individual study terms apply | `python3 scripts/fetch_authorized_asset.py SRA_RUN_MANIFEST` | PENDING |
| Protein Data Bank effector structures | https://www.rcsb.org/ | RCSB PDB data-use policy | `python3 scripts/fetch_authorized_asset.py EFFECTOR_PDB_MANIFEST` | PENDING |
| Pfam profiles | https://www.ebi.ac.uk/interpro/download/Pfam/ | Pfam/InterPro licence terms | `curl -fL <PINNED_PFAM_URL> -o data/raw/Pfam-A.hmm.gz` | PENDING |
| CD-HIT | https://github.com/weizhongli/cdhit | GPL-2.0 | `git clone https://github.com/weizhongli/cdhit.git vendor/cdhit` | PENDING |
| Foldseek | https://github.com/steineggerlab/foldseek | GPL-3.0 | `git clone https://github.com/steineggerlab/foldseek.git vendor/foldseek` | PENDING |
| MMseqs2 | https://github.com/soedinglab/MMseqs2 | GPL-3.0 | `git clone https://github.com/soedinglab/MMseqs2.git vendor/MMseqs2` | PENDING |
| BLAST+ | https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ | Public domain / NCBI terms | `python3 scripts/fetch_authorized_asset.py NCBI_BLAST_PLUS` | PENDING |
| HMMER | https://github.com/EddyRivasLab/hmmer | BSD-3-Clause | `git clone https://github.com/EddyRivasLab/hmmer.git vendor/hmmer` | PENDING |
| TM-align / US-align | https://zhanggroup.org/TM-align/ | Academic use; verify redistribution | `python3 scripts/fetch_authorized_asset.py TMALIGN` | PENDING |
| HH-suite / HHpred client | https://github.com/soedinglab/hh-suite | GPL-3.0; HHpred service terms separately | `git clone https://github.com/soedinglab/hh-suite.git vendor/hh-suite` | PENDING |
| ESMFold | https://github.com/facebookresearch/esm | MIT code; model licence and weights must be pinned | `git clone https://github.com/facebookresearch/esm.git vendor/esm` | PENDING |
| ESM-2 / ESM-IF | https://github.com/facebookresearch/esm | MIT code; model licences and revisions must be pinned | `python3 scripts/fetch_authorized_asset.py ESM_CHECKPOINTS` | PENDING |
| ProtT5 / ProtTrans | https://huggingface.co/Rostlab/prot_t5_xl_uniref50 | Model-card licence; pin revision | `python3 scripts/fetch_authorized_asset.py PROTT5_CHECKPOINT` | PENDING |
| AlphaFold 3 | https://github.com/google-deepmind/alphafold3 | Source/model parameters subject to AF3 terms | `git clone https://github.com/google-deepmind/alphafold3.git vendor/alphafold3` | PENDING |
| Boltz | https://github.com/jwohlwend/boltz | MIT code; pin model revision | `git clone https://github.com/jwohlwend/boltz.git vendor/boltz` | PENDING |
| EffectorP | https://effectorp.csiro.au/ | Academic server/software terms; version pin required | `python3 scripts/fetch_authorized_asset.py EFFECTORP` | PENDING |
| WideEffHunter | Published project repository/release | Confirm source and licence before use | `git clone <WIDEEFFHUNTER_REPOSITORY_URL> vendor/WideEffHunter` | PENDING |
| DeepLoc | https://services.healthtech.dtu.dk/services/DeepLoc-2.1/ | Service/model terms; version pin required | `python3 scripts/fetch_authorized_asset.py DEEPLOC` | PENDING |
| DeepSig | https://deepsig.biocomp.unibo.it/ | Confirm code/model licence | `python3 scripts/fetch_authorized_asset.py DEEPSIG` | PENDING |
| TargetP 2 | https://services.healthtech.dtu.dk/services/TargetP-2.0/ | Academic/service terms | `python3 scripts/fetch_authorized_asset.py TARGETP2` | PENDING |
| SignalP 6 and SignalP 3 HMM | https://services.healthtech.dtu.dk/services/SignalP-6.0/ | **LICENCE-BLOCKED pending clearance** | `python3 scripts/fetch_authorized_asset.py SIGNALP` | PENDING |
| TMHMM | https://services.healthtech.dtu.dk/services/TMHMM-2.0/ | **LICENCE-BLOCKED pending clearance** | `python3 scripts/fetch_authorized_asset.py TMHMM` | PENDING |
| Phobius | https://phobius.sbc.su.se/ | **LICENCE-BLOCKED pending clearance** | `python3 scripts/fetch_authorized_asset.py PHOBIUS` | PENDING |
| RepeatMasker | https://www.repeatmasker.org/ | Open Source License plus repeat-library terms | `python3 scripts/fetch_authorized_asset.py REPEATMASKER` | PENDING |
| OcculterCut | Published project repository/release | Confirm source and licence | `git clone <OCCULTERCUT_REPOSITORY_URL> vendor/OcculterCut` | PENDING |
| dN/dS implementation | PAML or HyPhy, to be ruled before T3 | GPL-compatible/open-source options; choose by construct validity | `python3 scripts/fetch_authorized_asset.py DNDS_TOOL` | PENDING |
| Evo 2 | Official Arc Institute/NVIDIA release | Model licence and endpoint access pending | `python3 scripts/fetch_authorized_asset.py EVO2` | PENDING |
| Nucleotide Transformer | Official InstaDeep model release | Model-card licence; pin revision | `python3 scripts/fetch_authorized_asset.py NUCLEOTIDE_TRANSFORMER` | PENDING |

SignalP, TMHMM, and Phobius remain unavailable until a human licence ruling. Any substitute must be justified against the scored quantity—precision at twenty—and must quote the relevant recall/precision spread; similarity to the replaced package is not sufficient.

## Reusable local MCP infrastructure

The sibling project `../../2_19C_biology/benchmark-mcp/` is the audited source for reusable implementation patterns. It is referenced, not copied or executed in Week 0.

| Capability | Local source | Reuse decision |
|---|---|---|
| STDIO server factory and role-separated servers | `benchmark-mcp/server.py` | Adapt for effector-specific servers at T3.1-T3.5 |
| `{result,error,receipt}` envelope, argument hash and content cache | `benchmark-mcp/common.py` | Reuse contract; change artifact root and tool implementations |
| Classical search/scoring | `benchmark-mcp/classical.py` | Reuse MMseqs/BLAST, motif and identity components after construct-validity review |
| Structural analysis | `benchmark-mcp/analysis.py` | Reuse TM-align wrapper; add Foldseek cohort clustering |
| Foundation-model services | `benchmark-mcp/predictive.py`, `generative.py` | Reuse ESMFold, ESM-2 and ESM-IF wrappers with pinned hashes |
| Literature and record channels | `benchmark-mcp/lit.py`, `record.py` | Reuse separation between retrieval and unscored submission |
| Agent-side smoke controls | `benchmark-mcp/run_smokes.py`, `certify_*.py` | Port positive, negative, repeat and resolvable-receipt controls |
| Executable prompt freeze | `benchmark-mcp/stage4step1_prepare.py` | Reuse fail-closed byte hashing; never freeze only a source template |

