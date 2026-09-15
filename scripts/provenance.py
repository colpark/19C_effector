#!/usr/bin/env python3
"""Block a run unless emitted prompt/config bytes match a frozen manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_inside(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"path escapes repository: {relative}")
    return path


def verify(manifest_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot parse manifest: {exc}"]
    root = manifest_path.parent.resolve()
    for kind in ("prompt", "config"):
        record = manifest.get(kind)
        if not isinstance(record, dict) or set(record) != {"path", "sha256"}:
            errors.append(f"{kind} must contain exactly path and sha256")
            continue
        try:
            path = resolve_inside(root, record["path"])
        except (TypeError, ValueError) as exc:
            errors.append(str(exc))
            continue
        expected = record["sha256"]
        if not isinstance(expected, str) or not re_full_sha(expected):
            errors.append(f"{kind} has malformed sha256")
        elif not path.is_file():
            errors.append(f"{kind} emission is missing: {path}")
        elif digest(path) != expected:
            errors.append(f"{kind} hash divergence")
    return errors


def re_full_sha(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def self_test() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        prompt = root / "prompt.txt"
        config = root / "config.json"
        prompt.write_text("frozen prompt\n", encoding="utf-8")
        config.write_text('{"temperature":0}\n', encoding="utf-8")
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps({
            "prompt": {"path": prompt.name, "sha256": digest(prompt)},
            "config": {"path": config.name, "sha256": digest(config)},
        }), encoding="utf-8")
        if verify(manifest):
            return 1
        prompt.write_bytes(prompt.read_bytes()[:-1] + b"X")
        if not verify(manifest):
            return 1
    print("PASS provenance one-byte mutation blocked")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.manifest is None:
        parser.error("manifest is required unless --self-test is used")
    errors = verify(args.manifest)
    for error in errors:
        print(f"BLOCK: {error}", file=sys.stderr)
    if errors:
        return 1
    print("PASS emitted prompt and configuration match frozen specification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
