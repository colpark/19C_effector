#!/usr/bin/env python3
"""Render role policy and build content-filtered standalone Git clones."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import stat
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
ACCESS = ROOT / "access"
BUILD = ROOT / "build/access"
ROLES = ("curator", "instrument", "floor", "referee", "adversary", "fetcher")
UNSANDBOXABLE_COMMANDS = ("docker",)


def load_role(role: str) -> dict:
    if role not in ROLES:
        raise ValueError(f"unknown role: {role}")
    data = yaml.safe_load((ACCESS / f"{role}.yaml").read_text(encoding="utf-8"))
    required = {"role", "clone_name", "sparse_include", "sparse_exclude", "writable",
                "commands", "mcp_policy", "network_access", "network_allowlist"}
    if set(data) != required:
        raise ValueError(f"{role}: fields differ; missing={required-set(data)}, extra={set(data)-required}")
    if data["clone_name"] != role:
        raise ValueError(f"{role}: clone_name must equal the role slug")
    if data["network_access"] not in (True, False):
        raise ValueError(f"{role}: network_access must be boolean")
    if not isinstance(data["network_allowlist"], list):
        raise ValueError(f"{role}: network_allowlist must be a list")
    return data


def absolute_under(base: Path, relative: str) -> str:
    path = (base / relative).resolve()
    resolved_base = base.resolve()
    if path != resolved_base and resolved_base not in path.parents:
        raise ValueError(f"path escapes {base}: {relative}")
    return str(path)


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, text=True, **kwargs)


def git_output(repository: Path, *arguments: str) -> str:
    return run(["git", "-C", str(repository), *arguments], capture_output=True).stdout.strip()


def preparation_host_id() -> str:
    for candidate in (Path("/etc/machine-id"), Path("/var/lib/dbus/machine-id")):
        if candidate.is_file():
            value = candidate.read_text(encoding="utf-8").strip()
            if value:
                return hashlib.sha256(value.encode()).hexdigest()
    raise RuntimeError("a machine-id is required to separate preparation and role-session hosts")


def role_paths(role: str, role_root: Path) -> tuple[dict, list[str], list[str], list[str]]:
    data = load_role(role)
    denied = [absolute_under(role_root, item) for item in data["sparse_exclude"]]
    allowed_read = [str(role_root.resolve())] + [
        absolute_under(role_root, item) for item in data["sparse_include"]
    ]
    allowed_write = [absolute_under(role_root, item) for item in data["writable"]]
    return data, denied, allowed_read, allowed_write


def render_profiles(role: str, role_root: Path, out_root: Path) -> dict[str, Path]:
    data, denied, allowed_read, allowed_write = role_paths(role, role_root)
    command_universe = sorted({command for name in ROLES for command in load_role(name)["commands"]}
                              | set(UNSANDBOXABLE_COMMANDS))
    denied_commands = [command for command in command_universe if command not in data["commands"]]
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
                # These denials are a backstop. Clone-time absence is the control.
                "denyRead": denied,
                "allowRead": allowed_read,
                "allowWrite": allowed_write,
            },
            "excludedCommands": list(UNSANDBOXABLE_COMMANDS),
        },
        "permissions": {
            "allow": [f"Bash({command}:*)" for command in data["commands"]],
            "deny": [f"Read({path}/**)" for path in denied]
                    + [f"Bash(* {path}/**)" for path in denied]
                    + [f"Bash({command}:*)" for command in denied_commands],
        },
        "commandPolicy": {"default": "deny", "allow": data["commands"]},
        "mcpPolicy": data["mcp_policy"],
    }
    claude = out_root / ".claude" / f"settings.{role}.json"
    codex = out_root / ".codex" / f"config.{role}.toml"
    codex_rules = out_root / ".codex" / f"rules.{role}.rules"
    access_policy = out_root / f"access-policy.{role}.json"
    manifest = out_root / "manifest.json"
    claude.parent.mkdir(parents=True, exist_ok=True)
    codex.parent.mkdir(parents=True, exist_ok=True)
    claude.write_text(json.dumps(settings, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    network = "true" if data["network_access"] else "false"
    codex.write_text(
        'sandbox_mode = "workspace-write"\n'
        '\n[sandbox_workspace_write]\n'
        f"network_access = {network}\n"
        f"writable_roots = {json.dumps(allowed_write)}\n\n"
        f'[projects.{json.dumps(str(role_root.resolve()))}]\n'
        'trust_level = "untrusted"\n',
        encoding="utf-8",
    )
    rules = [
        f"prefix_rule(pattern=[{json.dumps(command)}], decision=\"allow\")"
        for command in data["commands"]
    ] + [
        f"prefix_rule(pattern=[{json.dumps(command)}], decision=\"forbidden\")"
        for command in denied_commands
    ]
    codex_rules.write_text("\n".join(rules) + "\n", encoding="utf-8")
    access_policy.write_text(json.dumps({
        "commands": {"default": "deny", "allow": data["commands"], "deny": denied_commands},
        "mcp_policy": data["mcp_policy"],
    }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    manifest.write_text(json.dumps({
        "clone_root": str(role_root.resolve()),
        "network_access": data["network_access"],
        "preparation_host_id_sha256": preparation_host_id(),
        "role": role,
        "sparse_exclude": data["sparse_exclude"],
        "sparse_include": data["sparse_include"],
        "standalone": True,
        "union_repository_allowed_on_session_host": False,
        "writable": data["writable"],
    }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return {"claude": claude, "codex": codex, "codex_rules": codex_rules,
            "access_policy": access_policy, "manifest": manifest}


def write_clone_builder(role: str, target: Path) -> Path:
    shell = target / f"create_clone.{role}.sh"
    shell.write_text(
        "#!/usr/bin/env bash\n"
        "set -Eeuo pipefail\n"
        "if [[ $# -ne 1 ]]; then\n"
        f"  echo \"usage: $0 ABSOLUTE_{role.upper()}_CLONE_DESTINATION\" >&2\n"
        "  exit 2\n"
        "fi\n"
        f"source_repo={shlex.quote(str(ROOT))}\n"
        'destination=$(realpath -m -- "$1")\n'
        'test ! -e "$destination"\n'
        f'python3 "$source_repo/scripts/render_access.py" {shlex.quote(role)} '
        '--create-clone "$destination"\n',
        encoding="utf-8",
    )
    shell.chmod(shell.stat().st_mode | stat.S_IXUSR)
    legacy = target / f"create_worktree.{role}.sh"
    legacy.unlink(missing_ok=True)
    return shell


def render(role: str, out_root: Path = BUILD, clone_root: Path | None = None) -> dict[str, Path]:
    data = load_role(role)
    role_root = clone_root or (WORKSPACE / "role_clones" / data["clone_name"])
    target = out_root / role
    outputs = render_profiles(role, role_root, target)
    outputs["clone_builder"] = write_clone_builder(role, target)
    return outputs


def create_filtered_clone(role: str, destination: Path) -> dict[str, Path]:
    data = load_role(role)
    destination = destination.resolve()
    if destination.exists():
        raise ValueError(f"clone destination already exists: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "init", "--quiet", str(destination)])
    export_command = [
        "git", "-C", str(ROOT), "fast-export", "--signed-tags=strip",
        "--tag-of-filtered-object=rewrite", "--all", "--", *data["sparse_include"],
    ]
    exporter = subprocess.Popen(export_command, stdout=subprocess.PIPE)
    assert exporter.stdout is not None
    importer = subprocess.run(
        ["git", "-C", str(destination), "fast-import", "--quiet"],
        stdin=exporter.stdout,
    )
    exporter.stdout.close()
    export_status = exporter.wait()
    if export_status != 0 or importer.returncode != 0:
        raise RuntimeError(
            f"filtered clone failed: fast-export={export_status}, fast-import={importer.returncode}"
        )
    branch = git_output(ROOT, "symbolic-ref", "--short", "HEAD")
    run(["git", "-C", str(destination), "checkout", "--quiet", "--detach",
         f"refs/heads/{branch}"])
    run(["git", "-C", str(destination), "gc", "--prune=now"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    outputs = render_profiles(role, destination, destination / ".role-access")
    manifest_data = json.loads(outputs["manifest"].read_text(encoding="utf-8"))
    manifest_data["source_commit"] = git_output(ROOT, "rev-parse", "HEAD")
    manifest_data["filtered_commit"] = git_output(destination, "rev-parse", "HEAD")
    outputs["manifest"].write_text(
        json.dumps(manifest_data, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    return outputs


def included_path(path: str, includes: list[str]) -> bool:
    return any(path == include or path.startswith(include.rstrip("/") + "/")
               for include in includes)


def self_test() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="effector-role-clones-") as temporary:
        clone_parent = Path(temporary)
        for role in ROLES:
            data = load_role(role)
            render(role)
            role_root = clone_parent / role
            outputs = create_filtered_clone(role, role_root)
            _, denied, _, allowed_write = role_paths(role, role_root)
            settings = json.loads(outputs["claude"].read_text(encoding="utf-8"))
            sandbox = settings["sandbox"]
            if (sandbox.get("enabled"), sandbox.get("failIfUnavailable"),
                    sandbox.get("allowUnsandboxedCommands"),
                    sandbox.get("network", {}).get("strictAllowlist")) != (True, True, False, True):
                failures.append(f"{role}: fail-closed sandbox flags differ")
            deny_read = set(sandbox["filesystem"]["denyRead"])
            permission_deny = settings.get("permissions", {}).get("deny", [])
            history_paths = set(filter(None, git_output(
                role_root, "log", "--all", "--format=", "--name-only"
            ).splitlines()))
            for tracked_path in history_paths:
                if not included_path(tracked_path, data["sparse_include"]):
                    failures.append(f"{role}: unselected path exists in filtered history: {tracked_path}")
            for relative, denied_path in zip(data["sparse_exclude"], denied):
                matches = list(role_root.glob(f"**/{relative}"))
                if matches:
                    failures.append(f"{role}: excluded path exists in clone: {relative}: {matches}")
                if any(path == relative or path.startswith(relative.rstrip("/") + "/")
                       for path in history_paths):
                    failures.append(f"{role}: excluded path exists in clone history: {relative}")
                if denied_path not in deny_read:
                    failures.append(f"{role}: defence-in-depth denyRead missing for {relative}")
                if not any(denied_path in rule for rule in permission_deny):
                    failures.append(f"{role}: permissions.deny does not mirror {relative}")
            if git_output(role_root, "remote"):
                failures.append(f"{role}: standalone clone retains a remote")
            if (role_root / ".git/objects/info/alternates").exists():
                failures.append(f"{role}: standalone clone shares an object store")
            if Path(git_output(role_root, "rev-parse", "--git-common-dir")).name != ".git":
                failures.append(f"{role}: clone has a shared Git common directory")
            command_universe = sorted({command for name in ROLES
                                       for command in load_role(name)["commands"]}
                                      | set(UNSANDBOXABLE_COMMANDS))
            denied_commands = [command for command in command_universe
                               if command not in data["commands"]]
            for command in denied_commands:
                if f"Bash({command}:*)" not in permission_deny:
                    failures.append(f"{role}: Claude command denial missing for {command}")
            if sandbox.get("excludedCommands") != list(UNSANDBOXABLE_COMMANDS):
                failures.append(f"{role}: Claude excludedCommands mismatch")
            if settings.get("mcpPolicy") != data["mcp_policy"]:
                failures.append(f"{role}: Claude MCP policy mismatch")
            parsed = tomllib.loads(outputs["codex"].read_text(encoding="utf-8"))
            codex_sandbox = parsed.get("sandbox_workspace_write", {})
            if (parsed.get("sandbox_mode") != "workspace-write"
                    or codex_sandbox.get("network_access") != data["network_access"]):
                failures.append(f"{role}: Codex sandbox/network mismatch")
            if codex_sandbox.get("writable_roots") != allowed_write:
                failures.append(f"{role}: Codex writable roots mismatch")
            if parsed.get("projects", {}).get(str(role_root.resolve()), {}).get(
                    "trust_level") != "untrusted":
                failures.append(f"{role}: Codex project is not untrusted")
            rules_text = outputs["codex_rules"].read_text(encoding="utf-8")
            for command in denied_commands:
                expected = f'prefix_rule(pattern=[{json.dumps(command)}], decision="forbidden")'
                if expected not in rules_text:
                    failures.append(f"{role}: Codex command denial missing for {command}")
            policy = json.loads(outputs["access_policy"].read_text(encoding="utf-8"))
            if policy.get("mcp_policy") != data["mcp_policy"]:
                failures.append(f"{role}: emitted MCP policy mismatch")
            if policy.get("commands", {}).get("allow") != data["commands"]:
                failures.append(f"{role}: emitted command policy mismatch")
            manifest = json.loads(outputs["manifest"].read_text(encoding="utf-8"))
            if (manifest.get("standalone") is not True
                    or manifest.get("union_repository_allowed_on_session_host") is not False):
                failures.append(f"{role}: standalone/union-host manifest flags differ")
            holds_labels = "data/labels" in data["sparse_include"]
            if holds_labels and data["network_access"] is True:
                failures.append(f"{role}: holds labels with unrestricted network")
            if data["network_access"] is True and not data["network_allowlist"]:
                failures.append(f"{role}: network access is unrestricted by an allowlist")
    for failure in failures:
        print(f"ERROR: {failure}", file=sys.stderr)
    if failures:
        return 1
    print("PASS render_access all roles: excluded paths absent from standalone clones")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("role", nargs="?", choices=ROLES)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--create-clone", type=Path)
    parser.add_argument("--clone-root", type=Path)
    parser.add_argument("--out-root", type=Path, default=BUILD)
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.create_clone:
        if not args.role or args.all or args.clone_root:
            parser.error("--create-clone requires exactly one ROLE")
        outputs = create_filtered_clone(args.role, args.create_clone)
        print(json.dumps({key: str(path) for key, path in outputs.items()}, sort_keys=True))
        return 0
    roles = ROLES if args.all else ((args.role,) if args.role else ())
    if not roles:
        parser.error("provide ROLE or --all")
    if args.clone_root and len(roles) != 1:
        parser.error("--clone-root requires exactly one ROLE")
    for role in roles:
        outputs = render(role, args.out_root, args.clone_root)
        print(json.dumps({key: str(path) for key, path in outputs.items()}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
