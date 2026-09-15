#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 ROLE" >&2
  exit 2
fi

role=$1
case "$role" in
  curator|instrument|floor|referee|adversary) ;;
  *) echo "unknown role: $role" >&2; exit 2 ;;
esac

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
settings="$root/build/access/$role/.claude/settings.$role.json"
failures=0

fail() {
  echo "FAIL $role: $*" >&2
  failures=$((failures + 1))
}

[[ -f "$settings" ]] || {
  echo "rendered settings absent; run scripts/render_access.py $role" >&2
  exit 1
}

jq -e '.sandbox.enabled == true and .sandbox.failIfUnavailable == true' "$settings" >/dev/null \
  || fail "sandbox is disabled or permits fallback when unavailable"
[[ ${SANDBOX_ACTIVE:-0} == 1 ]] || fail "T1 startup assertion failed: sandbox is not active"
[[ ${SANDBOX_FALLBACK_USED:-1} == 0 ]] || fail "runtime reports sandbox fallback"

jq -e '.sandbox.allowUnsandboxedCommands == false' "$settings" >/dev/null \
  || fail "unsandboxed commands are permitted"
[[ ${SANDBOX_UNSANDBOXED_RETRY:-1} == 0 ]] || fail "unsandboxed retry escape hatch is active"

mapfile -t denied_paths < <(jq -r '.sandbox.filesystem.denyRead[]' "$settings")
[[ ${#denied_paths[@]} -gt 0 ]] || fail "denyRead is empty"
for denied in "${denied_paths[@]}"; do
  # This probe deliberately goes through a new Bash process. A file-tool-only
  # denial is insufficient because an agent can invoke shell readers instead.
  if bash --noprofile --norc -c '
      target=$1
      if [[ -d "$target" ]]; then
        find "$target" -mindepth 1 -maxdepth 1 -print -quit >/dev/null
      else
        head -c 1 "$target" >/dev/null
      fi
    ' bash "$denied" 2>/dev/null; then
    fail "Bash read succeeded for denied path $denied"
  fi
done

jq -e '.sandbox.network.strictAllowlist == true' "$settings" >/dev/null \
  || fail "network strict allowlist is disabled"
# T2 is platform-enforced: the runtime, not only the settings file, must bind
# network access to the strict allowlist.
[[ ${SANDBOX_NETWORK_ALLOWLIST_ENFORCED:-0} == 1 ]] || fail "T2 startup assertion failed"
while IFS= read -r host; do
  if [[ ${host,,} =~ (phi-?base|label|answer|scored|cohort|scorer) ]]; then
    fail "network allowlist contains protected host $host"
  fi
done < <(jq -r '.sandbox.network.allowedDomains[]?' "$settings")

# T3 and T4 are platform-enforced. Package installation and writes outside
# cell scratch are unavailable before any project-level gate can run.
[[ ${SANDBOX_PACKAGE_INSTALL_BLOCKED:-0} == 1 ]] || fail "T3 startup assertion failed"
[[ ${SANDBOX_WRITE_BOUNDARY_ENFORCED:-0} == 1 ]] || fail "T4 startup assertion failed"

[[ ${SANDBOX_MEMORY_DISABLED:-0} == 1 ]] || fail "persistent memory is not disabled"
[[ -n ${SANDBOX_SESSION_ID:-} ]] || fail "current session identity is absent"
if [[ -n ${SANDBOX_PREVIOUS_SESSION_ID:-} && ${SANDBOX_PREVIOUS_SESSION_ID} == "${SANDBOX_SESSION_ID:-}" ]]; then
  fail "session identity persisted across sessions"
fi
[[ -z ${SANDBOX_MEMORY_PATHS:-} ]] || fail "memory paths are mounted: ${SANDBOX_MEMORY_PATHS}"

if (( failures > 0 )); then
  exit 1
fi
echo "PASS $role sandbox assertions"
