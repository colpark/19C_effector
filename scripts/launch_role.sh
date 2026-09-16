#!/usr/bin/env bash
set -Eeuo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 ROLE [PROMPT ...]" >&2
  exit 2
fi

role=$1
shift
case "$role" in
  curator|instrument|floor|referee|adversary|fetcher) ;;
  *) echo "unknown role: $role" >&2; exit 2 ;;
esac

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
manifest="$root/.role-access/manifest.json"
rendered="$root/.role-access/.codex"
rendered_config="$rendered/config.$role.toml"
rendered_rules="$rendered/rules.$role.rules"
profile_name="role-$role"

[[ -f $manifest ]] || {
  echo "refusing union checkout: standalone role manifest absent: $manifest" >&2
  exit 1
}
python3 - "$manifest" "$role" "$root" <<'PY'
import hashlib
import json
import pathlib
import sys

manifest_path, expected_role, root = sys.argv[1:]
manifest = json.loads(pathlib.Path(manifest_path).read_text(encoding="utf-8"))
if manifest.get("role") != expected_role:
    raise SystemExit(f"role manifest mismatch: {manifest.get('role')} != {expected_role}")
if manifest.get("standalone") is not True:
    raise SystemExit("role repository is not marked standalone")
if manifest.get("union_repository_allowed_on_session_host") is not False:
    raise SystemExit("manifest does not forbid the union repository on the session host")
if pathlib.Path(manifest.get("clone_root", "")).resolve() != pathlib.Path(root).resolve():
    raise SystemExit("role clone must be deployed at its prepared absolute path")
machine_id = None
for candidate in (pathlib.Path("/etc/machine-id"), pathlib.Path("/var/lib/dbus/machine-id")):
    if candidate.is_file():
        value = candidate.read_text(encoding="utf-8").strip()
        if value:
            machine_id = hashlib.sha256(value.encode()).hexdigest()
            break
if machine_id is None:
    raise SystemExit("cannot verify role-session host identity")
if machine_id == manifest.get("preparation_host_id_sha256"):
    raise SystemExit("refusing preparation host: role sessions require a separate host without the union repository")
PY

[[ $(git -C "$root" rev-parse --show-toplevel) == "$root" ]] || {
  echo "role clone is not a repository root: $root" >&2
  exit 1
}
[[ -z $(git -C "$root" remote) ]] || {
  echo "standalone role clone must not retain a Git remote" >&2
  exit 1
}
[[ ! -e $root/.git/objects/info/alternates ]] || {
  echo "standalone role clone must not share a Git object store" >&2
  exit 1
}
[[ -f $rendered_config && -f $rendered_rules ]] || {
  echo "rendered Codex profile absent for $role" >&2
  exit 1
}

codex_state_root=$(python3 - <<'PY'
import os
import pwd

print(os.environ.get("CODEX_HOME", os.path.join(pwd.getpwuid(os.getuid()).pw_dir, ".codex")))
PY
)
[[ -f $codex_state_root/auth.json ]] || {
  echo "Codex authentication state absent: $codex_state_root/auth.json" >&2
  exit 1
}

runtime_home=$(mktemp -d "${TMPDIR:-/tmp}/effector-$role-codex.XXXXXX")
mkdir -p "$runtime_home/rules"
ln -s "$rendered_config" "$runtime_home/$profile_name.config.toml"
ln -s "$rendered_rules" "$runtime_home/rules/default.rules"
ln -s "$codex_state_root/auth.json" "$runtime_home/auth.json"

cleanup_runtime() {
  case "$runtime_home" in
    "${TMPDIR:-/tmp}"/effector-"$role"-codex.*)
      find "$runtime_home" -depth -delete
      ;;
    *)
      echo "refusing to clean unexpected runtime path: $runtime_home" >&2
      ;;
  esac
}
trap cleanup_runtime EXIT

if [[ $# -gt 0 ]]; then
  stage_body=$*
else
  stage_body=$(</dev/stdin)
fi
[[ -n $stage_body ]] || {
  echo "a stage prompt is required" >&2
  exit 2
}

{
  cat "$root/constitution.md"
  printf '\n%s\n' "$stage_body"
} | env CODEX_HOME="$runtime_home" codex --profile "$profile_name" \
  --ask-for-approval never exec \
  --ephemeral --strict-config --model gpt-5.6-sol \
  --sandbox workspace-write \
  --cd "$root" -
