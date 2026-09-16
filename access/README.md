# Role access scopes

## Control: path absence

Each role receives a standalone Git repository whose object history and working
tree are filtered during creation. `scripts/render_access.py ROLE
--create-clone DESTINATION` uses Git's `fast-export` path selection and
`fast-import`; it does not make a linked worktree, retain a remote, use an
alternate object store, or leave excluded history in the role clone. For every
role, every `sparse_exclude` path must be absent both from the checkout and from
all history in that clone.

Absence is the confidentiality control. The rendered `denyRead` and command
denials remain as defence in depth for accidental co-location, but they are not
counted as enforcement unless a launched runtime probe demonstrates that the
sandbox is working. Current host evidence does not demonstrate that.

Clone construction and role execution occur on different hosts. The union
repository exists only on the preparation host. A completed role clone is
transferred to a role-session host at the same absolute path recorded in its
manifest, and that host must not contain the union repository. The launcher
refuses the union checkout, any clone with a remote or shared object store, a
relocated clone, and the preparation host's machine identity. Host provisioning
is responsible for verifying that no separately copied union repository exists
under another path on the role-session host.

Cross-role state moves only as new material under `handoff/`. Role clones do
not share a working tree, Git object store, writable mount, or handoff directory;
the coordinator exports and imports handoff additions between hosts. No other
role path is a transfer channel.

## Co-location encryption decision

Decision: use **age** (`age` / `age-keygen`) for file encryption if a role-held
path must be physically co-located with a role that must not read it. This is an
established tool, not a repository-designed cryptosystem. The decrypting age
identity must be provisioned by the host secret mechanism outside the reading
role's clone, environment, process credentials, and handoff scope; identities
must never be committed. If that separation cannot be provided, co-location is
not approved. The `age` binary is not installed on the current preparation
host, so this decision does not claim an exercised encryption control.

## Building and deploying clones

On the preparation host:

```bash
python3 scripts/render_access.py --self-test
python3 scripts/render_access.py instrument --create-clone /srv/effector/instrument
```

Transfer `/srv/effector/instrument` as a complete standalone repository to the
same absolute path on a different, union-free role-session host. Then launch
from inside that clone:

```bash
scripts/launch_role.sh instrument 'STAGE PROMPT'
```

The constitution is still prepended by the launcher. The `.role-access/`
manifest and profiles are clone-specific deployment material and are not part
of the filtered Git history.
