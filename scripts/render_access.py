#!/usr/bin/env python3
"""Render load-bearing Claude, Codex, and sparse-worktree access settings."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import stat
import sys
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
ACCESS = ROOT / "access"
BUILD = ROOT / "build/access"
ROLES = ("curator", "instrument", "floor", "referee", "adversary")


def load_role(role: str) -> dict:
    if role not in ROLES:
        raise ValueError(f"unknown role: {role}")
    data = yaml.safe_load((ACCESS / f"{role}.yaml").read_text(encoding="utf-8"))
    required = {"role", "worktree", "sparse_include", "sparse_exclude", "writable",
                "commands", "mcp_policy", "network_access", "network_allowlist"}
    if set(data) != required:
        raise ValueError(f"{role}: fields differ; missing={required-set(data)}, extra={set(data)-required}")
    if data["network_access"] not in (True, False):
        raise ValueError(f"{role}: network_access must be boolean")
    if not isinstance(data["network_allowlist"], list):
        raise ValueError(f"{role}: network_allowlist must be a list")
    return data


def absolute_under(base: Path, relative: str) -> str:
    path = (base / relative).resolve()
    if path != base.resolve() and base.resolve() not in path.parents:
        raise ValueError(f"path escapes {base}: {relative}")
    return str(path)


def render(role: str, out_root: Path = BUILD) -> dict[str, Path]:
    data = load_role(role)
    role_root = (WORKSPACE / data["worktree"]).resolve()
    denied = [absolute_under(ROOT, item) for item in data["sparse_exclude"]]
    allowed_read = [str(role_root)] + [absolute_under(role_root, item) for item in data["sparse_include"]]
    allowed_write = [absolute_under(role_root, item) for item in data["writable"]]
    settings = {
        "sandbox": {
            "enabled": True,
            "failIfUnavailable": True,
            "allowUnsandboxedCommands": False,
            "network": {
                "strictAllowlist": True,
                "allowedDomains": data["network_allowlist"],
            },
            "filesystem": {
                "denyRead": denied,
                "allowRead": allowed_read,
                "allowWrite": allowed_write,
            },
        },
        "permissions": {
            "deny": [f"Read({path}/**)" for path in denied]
                    + [f"Bash(* {path}/**)" for path in denied],
        },
    }
    target = out_root / role
    claude = target / ".claude" / f"settings.{role}.json"
    codex = target / ".codex" / f"config.{role}.toml"
    shell = target / f"create_worktree.{role}.sh"
    claude.parent.mkdir(parents=True, exist_ok=True)
    codex.parent.mkdir(parents=True, exist_ok=True)
    claude.write_text(json.dumps(settings, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    network = "true" if data["network_access"] else "false"
    codex.write_text(
        'sandbox_mode = "workspace-write"\n'
        f"network_access = {network}\n\n"
        f'[projects.{json.dumps(str(role_root))}]\n'
        'trust_level = "untrusted"\n',
        encoding="utf-8",
    )
    includes = " ".join(shlex.quote(item) for item in data["sparse_include"])
    shell.write_text(
        "#!/usr/bin/env bash\n"
        "set -Eeuo pipefail\n"
        f"repo={shlex.quote(str(ROOT))}\n"
        f"worktree={shlex.quote(str(role_root))}\n"
        'test ! -e "$worktree"\n'
        'git -C "$repo" worktree add --detach --no-checkout "$worktree" HEAD\n'
        'git -C "$worktree" sparse-checkout init --cone\n'
        f'git -C "$worktree" sparse-checkout set {includes}\n'
        'git -C "$worktree" checkout --detach HEAD\n',
        encoding="utf-8",
    )
    shell.chmod(shell.stat().st_mode | stat.S_IXUSR)
    return {"claude": claude, "codex": codex, "shell": shell}


def self_test() -> int:
    failures: list[str] = []
    for role in ROLES:
        data = load_role(role)
        outputs = render(role)
        role_root = (WORKSPACE / data["worktree"]).resolve()
        settings = json.loads(outputs["claude"].read_text(encoding="utf-8"))
        sandbox = settings["sandbox"]
        if (sandbox.get("enabled"), sandbox.get("failIfUnavailable"),
                sandbox.get("allowUnsandboxedCommands"),
                sandbox.get("network", {}).get("strictAllowlist")) != (True, True, False, True):
            failures.append(f"{role}: fail-closed sandbox flags differ")
        deny_read = set(sandbox["filesystem"]["denyRead"])
        permission_deny = settings.get("permissions", {}).get("deny", [])
        for relative in data["sparse_exclude"]:
            denied = Path(absolute_under(ROOT, relative))
            if str(denied) not in deny_read:
                failures.append(f"{role}: missing denyRead for {relative}")
            if denied == role_root or role_root in denied.parents:
                failures.append(f"{role}: denied source path lies inside role workspace: {relative}")
            if not any(str(denied) in rule for rule in permission_deny):
                failures.append(f"{role}: permissions.deny does not mirror {relative}")
        parsed = tomllib.loads(outputs["codex"].read_text(encoding="utf-8"))
        if parsed.get("sandbox_mode") != "workspace-write" or parsed.get("network_access") != data["network_access"]:
            failures.append(f"{role}: Codex sandbox/network mismatch")
        if parsed.get("projects", {}).get(str(role_root), {}).get("trust_level") != "untrusted":
            failures.append(f"{role}: Codex project is not untrusted")
        holds_labels = "data/labels" in data["sparse_include"]
        if holds_labels and data["network_access"] is True:
            failures.append(f"{role}: holds labels with unrestricted network")
    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)
    if failures:
        return 1
    print("PASS render_access all roles")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("role", nargs="?", choices=ROLES)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    roles = ROLES if args.all else ((args.role,) if args.role else ())
    if not roles:
        parser.error("provide ROLE or --all")
    for role in roles:
        outputs = render(role)
        print(json.dumps({key: str(path) for key, path in outputs.items()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
