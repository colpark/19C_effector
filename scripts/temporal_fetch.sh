#!/usr/bin/env bash
# Fail-closed temporal isolation wrapper.  Copy this script outside REPO before --execute.
set -Eeuo pipefail

usage() {
  echo "usage: copy script outside repo; $0 --execute --repo REPO --credentials FILE --offline-root DIR -- FETCHER_COMMAND..." >&2
  exit 2
}
[[ ${1:-} == --execute ]] || usage
shift
repo= credentials= offline=
while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) repo=$2; shift 2;;
    --credentials) credentials=$2; shift 2;;
    --offline-root) offline=$2; shift 2;;
    --) shift; break;;
    *) usage;;
  esac
done
[[ -n $repo && -n $credentials && -n $offline && $# -gt 0 ]] || usage
repo=$(realpath -e "$repo"); credentials=$(realpath -e "$credentials")
mkdir -p "$offline"; offline=$(realpath -e "$offline")
[[ $repo != / && $credentials != / && $offline != / ]] || { echo 'refusing broad target' >&2; exit 2; }
[[ $offline != "$repo"/* && $repo != "$offline"/* ]] || { echo 'offline root overlaps repo' >&2; exit 2; }
self=$(realpath -e "$0")
[[ $self != "$repo"/* ]] || { echo 'refusing: copy temporal_fetch.sh outside the union repository before execution' >&2; exit 1; }

stamp=$(date -u +%Y%m%dT%H%M%SZ)
txn="$offline/temporal-fetch-$stamp"
mkdir -p "$txn"
inventory="$txn/inventory.sha256"
probe="$txn/absence-probe.txt"
repo_offline="$txn/union-repository"; cred_offline="$txn/credentials"

inventory_target() { find "$1" -type f -print0 | sort -z | xargs -0 sha256sum; }
inventory_target "$repo" > "$inventory"
printf 'repo=%s\ncredentials=%s\n' "$repo" "$credentials" >> "$txn/targets.txt"

restore() {
  [[ -e $repo_offline ]] && mv "$repo_offline" "$repo"
  [[ -e $cred_offline ]] && mv "$cred_offline" "$credentials"
  [[ -e $repo ]] && inventory_target "$repo" > "$txn/restored-inventory.sha256"
  [[ -e $repo ]] && cmp -s "$inventory" "$txn/restored-inventory.sha256" || {
    echo 'RESTORE INVENTORY MISMATCH' >&2; return 1;
  }
}
trap restore EXIT

mv "$repo" "$repo_offline"
mv "$credentials" "$cred_offline"
for path in "$repo" "$repo/labels" "$repo/scorer" "$credentials"; do
  if [[ -e $path || -r $path ]]; then
    printf 'UNEXPECTED PRESENT %s\n' "$path" | tee -a "$probe" >&2
    exit 1
  fi
  printf 'ABSENT %s: bash test -e/-r failed\n' "$path" | tee -a "$probe"
done
"$@"
