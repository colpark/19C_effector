# Asset inventory

Stage 2 records fetched open assets in place. `PENDING` still means not fetched; licence-restricted assets remain untouched and must not be substituted silently. Download blobs stay outside Git and are reproducible from the pinned source plus SHA-256 below.

| Asset | Source or repository | Licence status | Future fetch command | Checksum |
|---|---|---|---|---|
| PEACE defining preprint | Dai, Lin, Yoo and Liu, bioRxiv DOI `10.64898/2026.04.19.719514`, posted 22 April 2026; local file `docs/papers/peace_2026.pdf` | CC BY-NC-ND 4.0 | Already supplied; no fetch required | `6fa3458d7e9bb2a72827934a7e014cd97e13ef5015820d8cbb2876768b414a48` |
| PEACE code | https://github.com/Structurebiology-BNL/PEACE commit `90b8fc902f0b444e7f21adf75dae41a05931cc5f` | MIT | `https://github.com/Structurebiology-BNL/PEACE/archive/90b8fc902f0b444e7f21adf75dae41a05931cc5f.tar.gz` | `e9f4d15d77c7fdc01a218c06062acdcac02427eb50b8346913cbb07447a50e19` |
| PEACE served checkpoint | Xin Dai / BNL model release; the defining preprint is present but does not resolve the checkpoint artifact | Permission and redistribution status pending | `python3 scripts/fetch_authorized_asset.py PEACE_CHECKPOINT --instructions` | PENDING |
| PEACE curated CSVs | PEACE commit `90b8fc902f0b444e7f21adf75dae41a05931cc5f`, `src/data/dataset_construction/` | Repository data at pinned MIT commit | Same pinned source archive as PEACE code | `combined_positives.csv` `897069cfda43458ef43b4c26124ea199c631afc03032ed8beab0d8a1425062fb`; deduplicated FASTA `3f0dfa6b1ebb8ae6409c6330d77a715ab0989f588d42094234fefaaa3cf63ada` |
| Predector source and workflow | https://github.com/ccdmb/predector commit `3d2a591fadbe7c398c1ac398371b3b2610a60d46` | Open-source components; inspect per-tool licences | `https://github.com/ccdmb/predector/archive/3d2a591fadbe7c398c1ac398371b3b2610a60d46.tar.gz` | `14cd861dd61f4dee19575ebb38f69a4f38a8190c44014996ee8d22243355ed5b` |
| Predector container | Predector release/container registry | Confirm image and embedded-tool licences. `<PINNED_TAG>` remains unresolved because the source documents name no release tag; T3.2 must pin it after licence review. | `docker pull ghcr.io/ccdmb/predector:<PINNED_TAG>` | PENDING |
| Predector confirmed effector set | Predector commit `3d2a591fadbe7c398c1ac398371b3b2610a60d46`, `data/fungal_effectors.tsv` | Repository data at pinned source commit | Same pinned source archive as Predector | `428448f7582462872a00f7ba9bdcd0d92e5e8e15cdc04f7eb763c1de020a82bf` |
| PHI-base | https://github.com/PHI-base/data tag `PHIbase_release_v4.19` (`d1170ed3e2ba59237fc797a3dd506c72b85809a8`); FASTA addition commit `d6b295dc1023e9db7a754029f877d827d4229528` | PHI-base terms; functional evidence audited during T1.2 | Raw release CSV and FASTA from the pinned tag/commit | CSV `465082bd2d8091f6a0d9546eac6ac8d780253b1c8d1957f47a0fac7a7d9b33dd`; FASTA `a4f9585b0e82ad13ae26d8f86dc1767c31b4ee98da0a344c963fca39dc1e4bde` |
| UniProt reviewed fungal/oomycete records | https://rest.uniprot.org/, fetched 2026-09-15 | CC BY 4.0 | Frozen queries: `taxonomy_id:4751 AND reviewed:true` and `taxonomy_id:4762 AND reviewed:true`; fields `accession,id,protein_name,gene_names,organism_name,organism_id,length,sequence`; compressed TSV | Fungi `c6a57b04c6884f77f440f137905a954945088212bb35f4cc7032a37d26ae248a` (31,932 records); Oomycota `c503ffb8bea7d1db8e581c8a0b19dea55317751e47dbf2a20b1ec2951be61a69` (393 records) |
| AlphaFold DB models | https://alphafold.ebi.ac.uk/api/prediction/`<UniProt accession>`, fetched 2026-09-15 | AlphaFold DB terms / CC BY 4.0 model data | `python3 scripts/fetch_alphafold_models.py --provenance data/positives/provenance.tsv --output-dir data/raw/alphafold --manifest data/raw/alphafold_manifest.tsv` | Manifest `3513b14da0d7d959c27ae68071b27040832cee927d1e45caa4428f6eb08c4dfc`; 89/91 fetched, per-model SHA-256 in manifest |
| MycoCosm proteomes and genomes | https://mycocosm.jgi.doe.gov/ | JGI account/terms and project permissions required | `python3 scripts/fetch_authorized_asset.py MYCOCOSM_BULK --instructions` | PENDING |
| In-planta RNA-seq | https://www.ncbi.nlm.nih.gov/sra | Public records; individual study terms apply | `python3 scripts/fetch_authorized_asset.py SRA_RUN_MANIFEST --instructions` | PENDING |
| Protein Data Bank effector structures | https://www.rcsb.org/ | RCSB PDB data-use policy | `python3 scripts/fetch_authorized_asset.py EFFECTOR_PDB_MANIFEST --instructions` | PENDING |
| Pfam profiles | https://www.ebi.ac.uk/interpro/download/Pfam/ | Pfam/InterPro licence terms. `<PINNED_PFAM_URL>` remains unresolved because the source documents name no release; T3.1 must pin the card revision. | `curl -fL <PINNED_PFAM_URL> -o data/raw/Pfam-A.hmm.gz` | PENDING |
| CD-HIT | https://github.com/weizhongli/cdhit release `V4.8.1` | GPL-2.0 | Release source archive; locally built binary reports 4.8.1 | `26172dba3040d1ae5c73ff0ac6c3be8c8e60cc49fc7379e434cdf9cb1e7415de` |
| Foldseek | https://github.com/steineggerlab/foldseek release `10-941cd33` | GPL-3.0 | `foldseek-linux-arm64.tar.gz`; binary reports `941cd33ff0771cd2e3f144e3293e22a2b87e9fda` | `c71907a7ea06cb6e93d8eb000b0c3689e5e25f5edeb3969e2553cdb8f42982c1` |
| MMseqs2 | https://github.com/soedinglab/MMseqs2 release `18-8cc5c` | GPL-3.0 | `mmseqs-linux-arm64.tar.gz`; binary reports `8cc5ce367b5638c4306c2d7cfc652dd099a4643f` | `06c9a031331562e37eed3da79ef859d30a1a3ac5c5e334411dfaee5da5e9c0d0` |
| BLAST+ | https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ release `2.17.0+` | Public domain / NCBI terms | `ncbi-blast-2.17.0+-aarch64-linux.tar.gz`; `blastp` reports 2.17.0+ | `cb9ac252a1ac8767d90b0bf0a38486f3cb94f71ef9b6b8d194ded19b30250daf` |
| HMMER | https://github.com/EddyRivasLab/hmmer | BSD-3-Clause | `git clone https://github.com/EddyRivasLab/hmmer.git vendor/hmmer` | PENDING |
| TM-align / US-align | https://zhanggroup.org/TM-align/ | Academic use; verify redistribution | `python3 scripts/fetch_authorized_asset.py TMALIGN --instructions` | PENDING |
| HH-suite / HHpred client | https://github.com/soedinglab/hh-suite | GPL-3.0; HHpred service terms separately | `git clone https://github.com/soedinglab/hh-suite.git vendor/hh-suite` | PENDING |
| ESMFold | https://github.com/facebookresearch/esm | MIT code; model licence and weights must be pinned | `git clone https://github.com/facebookresearch/esm.git vendor/esm` | PENDING |
| ESM-2 / ESM-IF | https://github.com/facebookresearch/esm | MIT code; model licences and revisions must be pinned | `python3 scripts/fetch_authorized_asset.py ESM_CHECKPOINTS --instructions` | PENDING |
| ProtT5 / ProtTrans | https://huggingface.co/Rostlab/prot_t5_xl_uniref50 | Model-card licence; pin revision | `python3 scripts/fetch_authorized_asset.py PROTT5_CHECKPOINT --instructions` | PENDING |
| AlphaFold 3 | https://github.com/google-deepmind/alphafold3 | Source/model parameters subject to AF3 terms | `git clone https://github.com/google-deepmind/alphafold3.git vendor/alphafold3` | PENDING |
| Boltz | https://github.com/jwohlwend/boltz | MIT code; pin model revision | `git clone https://github.com/jwohlwend/boltz.git vendor/boltz` | PENDING |
| EffectorP | https://effectorp.csiro.au/ | Academic server/software terms; version pin required | `python3 scripts/fetch_authorized_asset.py EFFECTORP --instructions` | PENDING |
| WideEffHunter | Published project repository/release | `<WIDEEFFHUNTER_REPOSITORY_URL>` remains unresolved because the source documents name no repository or release; T3.1 must identify it from the defining paper. | `git clone <WIDEEFFHUNTER_REPOSITORY_URL> vendor/WideEffHunter` | PENDING |
| DeepLoc | https://services.healthtech.dtu.dk/services/DeepLoc-2.1/ | Service/model terms; version pin required | `python3 scripts/fetch_authorized_asset.py DEEPLOC --instructions` | PENDING |
| DeepSig | https://deepsig.biocomp.unibo.it/ | Confirm code/model licence | `python3 scripts/fetch_authorized_asset.py DEEPSIG --instructions` | PENDING |
| TargetP 2 | https://services.healthtech.dtu.dk/services/TargetP-2.0/ | Academic/service terms | `python3 scripts/fetch_authorized_asset.py TARGETP2 --instructions` | PENDING |
| SignalP 6 and SignalP 3 HMM | https://services.healthtech.dtu.dk/services/SignalP-6.0/ | **LICENCE-BLOCKED pending clearance** | `python3 scripts/fetch_authorized_asset.py SIGNALP --instructions` | PENDING |
| TMHMM | https://services.healthtech.dtu.dk/services/TMHMM-2.0/ | **LICENCE-BLOCKED pending clearance** | `python3 scripts/fetch_authorized_asset.py TMHMM --instructions` | PENDING |
| Phobius | https://phobius.sbc.su.se/ | **LICENCE-BLOCKED pending clearance** | `python3 scripts/fetch_authorized_asset.py PHOBIUS --instructions` | PENDING |
| RepeatMasker | https://www.repeatmasker.org/ | Open Source License plus repeat-library terms | `python3 scripts/fetch_authorized_asset.py REPEATMASKER --instructions` | PENDING |
| OcculterCut | Published project repository/release | `<OCCULTERCUT_REPOSITORY_URL>` remains unresolved because the source documents name no repository or release; T3.1 must resolve it from the defining paper. | `git clone <OCCULTERCUT_REPOSITORY_URL> vendor/OcculterCut` | PENDING |
| dN/dS implementation | PAML or HyPhy, to be ruled before T3 | GPL-compatible/open-source options; choose by construct validity | `python3 scripts/fetch_authorized_asset.py DNDS_TOOL --instructions` | PENDING |
| Evo 2 | Official Arc Institute/NVIDIA release | Model licence and endpoint access pending | `python3 scripts/fetch_authorized_asset.py EVO2 --instructions` | PENDING |
| Nucleotide Transformer | Official InstaDeep model release | Model-card licence; pin revision | `python3 scripts/fetch_authorized_asset.py NUCLEOTIDE_TRANSFORMER --instructions` | PENDING |

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
