# Role access scopes

The role worktrees use Git sparse checkout in cone mode. Cone mode selects
directories and always includes files at the repository root. Root-level file
entries such as `AGENTS.md` and `constitution.md` in `sparse_include` therefore
narrow nothing. Item 13 observed `.gitignore` and
`stage_prompt_template.md` in the Curator worktree even though neither was
requested.

## Root-file ruling

Every repository-root file is visible to every role worktree. No secret,
answer key, arm mapping, label, scored-cohort content, role-only instruction,
or other role-specific material may be stored in a repository-root file.
Role-specific material must live under a directory that cone mode can include
or exclude, and its access declaration must name that directory.

Listing a root-level file in `sparse_include` documents that a role uses it; it
does not enforce narrower visibility. Sparse checkout controls what appears in
the worktree, not whether a process can traverse to and read the source
repository. Runtime sandbox enforcement must be established separately by a
successful launched boundary probe.
