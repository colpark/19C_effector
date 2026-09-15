# Block A host escalation: unprivileged user namespaces

Recorded: 2026-09-15
Holder: host sysadmin

## Measured host state

```text
kernel.apparmor_restrict_unprivileged_userns=1
kernel.unprivileged_userns_clone=1
user.max_user_namespaces=511833
apparmor_status=Y
bubblewrap 0.9.0
```

The host does not currently permit this unprivileged process to create a user
namespace. Both probes failed:

```text
$ unshare --user --map-root-user true
unshare: write failed /proc/self/uid_map: Operation not permitted

$ unshare --user --map-root-user --net true
unshare: write failed /proc/self/uid_map: Operation not permitted
```

The general kernel switch permits unprivileged user namespaces and the quota is
nonzero, but AppArmor's additional restriction is enabled. Changing that
system-wide setting requires root and was not attempted in this session.

## Exact sysadmin action

For a temporary change lasting until reboot, the host sysadmin must run:

```bash
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
```

Then the sysadmin must verify the effective capability as the benchmark user:

```bash
sudo -u aid1 unshare --user --map-root-user --net true
```

If and only if the temporary change is approved for persistence, the sysadmin
must run:

```bash
printf '%s\n' 'kernel.apparmor_restrict_unprivileged_userns=0' | sudo tee /etc/sysctl.d/90-19c-bubblewrap.conf
sudo sysctl --system
```

## Scope and cost of the change

The change disables AppArmor's system-wide restriction on unprivileged user
namespace creation. It permits Bubblewrap to attempt the namespace setup used
by the Codex Linux sandbox. It also expands the host attack surface for every
unprivileged process, not only this repository.

It does not enable or validate the repository's role profile, denied-read
rules, command rules, MCP policy, network allowlist, sparse checkout, session
isolation, or benchmark gates. It does not prove that
`scripts/assert_sandbox.sh` will pass. After the host change, the Curator launch
and every Bash denial probe must still be rerun and recorded.
