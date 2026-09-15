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
role_relative=$(python3 - "$root/access/$role.yaml" <<'PY'
import sys
import yaml

with open(sys.argv[1], encoding="utf-8") as handle:
    print(yaml.safe_load(handle)["worktree"])
PY
)
worktree=$(realpath -m "$root/../$role_relative")
rendered="$root/build/access/$role/.codex"
rendered_config="$rendered/config.$role.toml"
rendered_rules="$rendered/rules.$role.rules"
runtime_home="$root/build/access/$role/.codex-runtime"
profile_name="role-$role"
codex_state_root=$(python3 - <<'PY'
import os
import pwd

print(os.environ.get("CODEX_HOME", os.path.join(pwd.getpwuid(os.getuid()).pw_dir, ".codex")))
PY
)

python3 "$root/scripts/render_access.py" "$role" >/dev/null
[[ -d $worktree ]] || {
  echo "role worktree absent: $worktree" >&2
  exit 1
}
[[ -f $rendered_config && -f $rendered_rules ]] || {
  echo "rendered Codex profile absent for $role" >&2
  exit 1
}
[[ -f $codex_state_root/auth.json ]] || {
  echo "Codex authentication state absent: $codex_state_root/auth.json" >&2
  exit 1
}

mkdir -p "$runtime_home/rules"
ln -sfn "$rendered_config" "$runtime_home/$profile_name.config.toml"
ln -sfn "$rendered_rules" "$runtime_home/rules/default.rules"
ln -sfn "$codex_state_root/auth.json" "$runtime_home/auth.json"

cleanup_runtime_links() {
  for link in "$runtime_home/$profile_name.config.toml" \
      "$runtime_home/rules/default.rules" "$runtime_home/auth.json"; do
    [[ -L $link ]] && unlink -- "$link"
  done
}
trap cleanup_runtime_links EXIT

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
  --cd "$worktree" -
