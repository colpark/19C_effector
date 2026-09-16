# Block A host escalation: mapped unprivileged user namespaces

Recorded: 2026-09-15
Holder: host sysadmin

## Host and confinement state

This host is not running inside a container. `systemd-detect-virt --container`
and `systemd-detect-virt` both returned `none`; `/.dockerenv` and
`/run/.containerenv` are absent; PID 1 is `systemd` in cgroup `/init.scope`.

The benchmark process has no seccomp profile in force and is not confined by
an AppArmor profile:

```text
NoNewPrivs:	0
Seccomp:	0
Seccomp_filters:	0
self AppArmor profile: unconfined
PID 1 AppArmor profile: unconfined
LSM list: lockdown,capability,landlock,yama,apparmor,ima,evm
AppArmor enabled: Y
```

AppArmor's kernel-level restriction on unprivileged user namespaces still
applies to an otherwise unconfined process:

```text
kernel.apparmor_restrict_unprivileged_userns = 1
kernel.unprivileged_userns_clone = 1
user.max_user_namespaces = 511833
bubblewrap 0.9.0
```

## Network-enabled role relaunch

`access/adversary.yaml` was changed to `network_access: true` with
`github.com` as its declared allowlist. The following command was run through
the repository launcher:

```bash
python3 scripts/render_access.py --self-test && scripts/launch_role.sh adversary "Run python3 -c 'print(\"SANDBOX_STARTED\")' exactly once. Do not modify any file. In the final answer, reproduce its stdout verbatim and add nothing else."
```

Complete output (verbatim):

```text
PASS render_access all roles
OpenAI Codex v0.154.0
--------
workdir: /home/aid1/Documents/3_19C_effector/role_worktrees/adversary
model: gpt-5.6-sol
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, /home/aid1/Documents/3_19C_effector/role_worktrees/adversary/handoff, /home/aid1/Documents/3_19C_effector/role_worktrees/adversary/gates, /home/aid1/Documents/3_19C_effector/role_worktrees/adversary/threats] (network access enabled)
reasoning effort: none
reasoning summaries: none
session id: 01a0a7b1-692c-7a93-97c4-8f2deca338cb
--------
user
# Effector Benchmark Constitution

1. Count the scarce unit, not the abundant one. Cluster before counting. Report every axis together or report none.
2. A tool must measure the quantity the task scores on. Justify a substitute against that quantity, never against the tool it replaces.
3. The served checkpoint belongs to the tool's identity. Record its hash, parameter count and revision on the card.
4. No tool that helps produce an answer may also score it.
5. Build and measure the comparator before installing the foundation model.
6. Gates fire on the protected quantity, stated as a threat, never on a tool name.
7. A gate arms only after both its must-fire and its must-not-fire control have run.
8. Hash what the runner emits, compare against the specification, and block the run on divergence.
9. Report the decision metric with its chance baseline and with the strongest existing adjudicator. Publish MDE(N) beside every effect.
10. Invalid answers are coverage failures, never zeros. The repair budget stays identical across arms and gets declared in advance.
11. Arms differ only in grant. Verify every grant from the model's side.
12. Preregistered values live in the ledger. Reports read the ledger rather than restating it.
13. A blocked item is recorded in `handoff/gate0/blocked.md` before the session ends, and silence is not a report.

Run python3 -c 'print("SANDBOX_STARTED")' exactly once. Do not modify any file. In the final answer, reproduce its stdout verbatim and add nothing else.

warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
codex
I’ll run the single requested read-only command.
codex
bwrap: setting up uid map: Permission denied
tokens used
4,918
bwrap: setting up uid map: Permission denied
```

The launcher process exited `0`, but the sandbox did not start and the requested
Python command did not execute. An outer successful launcher exit is not a
successful sandbox assertion.

## What the two Bubblewrap errors mean

The prior loopback message did not establish that mapped user namespaces were
usable. These direct, unprivileged probes reproduce both first-visible errors:

```text
$ bwrap --ro-bind / / --proc /proc --dev /dev true
bwrap: setting up uid map: Permission denied
$ bwrap --unshare-net --ro-bind / / --proc /proc --dev /dev true
bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted
$ bwrap --unshare-user --ro-bind / / --proc /proc --dev /dev true
bwrap: setting up uid map: Permission denied
```

Network namespace setup can therefore emit its loopback failure before
Bubblewrap reaches the uid-map failure. Removing network isolation merely
reveals the independent mapped-user-namespace blocker; it does not make the
filesystem sandbox available.

## What is blocked, what is not, and cost

Blocked today:

- Bubblewrap cannot create the mapped unprivileged user namespace required by
  the Codex filesystem sandbox. Consequently no launched role has demonstrated
  runtime filesystem read/write denial.
- Network namespaces also fail their loopback setup. This is a second failure,
  not the sole failure.

Not blocked today:

- Standalone process execution, ordinary repository operations, and sparse or
  filtered Git clones work without privilege.
- Rendering role configurations and command policies works, but rendering is
  not runtime enforcement.
- Path absence can be built without Bubblewrap; it does not by itself enforce
  write restrictions, network policy, command policy, MCP policy, or session
  isolation.

The no-root workaround costs runtime filesystem and network sandboxing: a role
can be given only files physically present in its standalone clone, while all
paths present there remain readable to that role and host paths remain outside
the repository's control. Enabling `network_access` also gives that Codex role
network access rather than an enforced domain allowlist.

The root-requiring alternative remains a host-admin decision: temporarily set
`kernel.apparmor_restrict_unprivileged_userns=0`, then verify Bubblewrap as the
benchmark user. Its cost is a host-wide increase in attack surface for all
unprivileged processes, plus sysadmin work and a complete rerun of every role
boundary probe. Persistence would add system configuration and maintenance
cost. No root action was attempted.

The temporary sysadmin action and verification are:

```bash
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
sudo -u aid1 bwrap --ro-bind / / --proc /proc --dev /dev true
```

This is an escalation request, not a command run by the benchmark process.

Block A remains open because the network-enabled relaunch did not start the
sandbox.
