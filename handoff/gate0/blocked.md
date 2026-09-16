# Blocked remediation items

This file records remediation items that could not produce a commit. A later
retry does not erase the original blocked event.

| Item | Required input | Input holder | Blocked on | Status |
|---|---|---|---|---|
| Item 10 | PEACE preprint PDF, bioRxiv DOI 10.64898/2026.04.19.719514 | PI | 2026-09-15 | RESOLVED 2026-09-15 by Item 29: supplied as `Fungus.pdf`, content-identified and moved to `docs/papers/peace_2026.pdf` |
| Item 11 | Current `19C_effector_bench_agent_prompts.md` pack containing Section 7, "Sandbox mapping" | PI | 2026-09-15 | OPEN |
| Item 10 retry | PEACE preprint PDF, bioRxiv DOI 10.64898/2026.04.19.719514; the claimed working-directory file was not present in any accessible workspace or attachment path | PI | 2026-09-15 | RESOLVED 2026-09-15 by Item 29: supplied as `Fungus.pdf`, content-identified and moved to `docs/papers/peace_2026.pdf` |
| Item 11 retry | Current `19C_effector_bench_agent_prompts.md` pack containing Section 7, "Sandbox mapping"; the only accessible copies remained the identical 413-line pack without that section | PI | 2026-09-15 | OPEN |
| T1.2 | PHI-base release, PEACE curated CSVs, Predector confirmed set, and frozen source versions | Fetcher and PI | 2026-09-15 | RESOLVED 2026-09-15: pinned sources and functionally filtered union are recorded in `docs/assets.md` and `data/positives/` |
| T1.4 | Candidate evidence records and an operational canonical-profile definition | Fetcher, PI, and Curator | 2026-09-15 | RESOLVED 2026-09-15: functional evidence and the frozen canonical profile are recorded per sequence in `data/positives/provenance.tsv` |
| T1.5 | Publication dates, deposition dates, retained positives, and every subject cutoff | Fetcher and subject-tool owners | 2026-09-15 | OPEN |
| Block A | Root-authorized change to `kernel.apparmor_restrict_unprivileged_userns`, followed by an unprivileged Bubblewrap uid-map verification; network-enabled Item 30 relaunch still failed | Host sysadmin | 2026-09-15 | OPEN |
| Block D licence clearance | Human dispatch of the prepared SignalP, TMHMM and Phobius requests and written licensor rulings | PI or project licensing officer, then each licensor | 2026-09-15 | OPEN |
