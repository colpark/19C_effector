#!/usr/bin/env python3
"""Validate that stop conditions are predicates over T1-T8, never names."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECT_THREATS = {f"T{i}" for i in range(5, 9)}
PLATFORM_THREATS = {f"T{i}" for i in range(1, 5)}
PROHIBITED_NAMES = {
    "signalp", "tmhmm", "phobius", "predector", "peace", "effectorp", "foldseek",
    "esmfold", "esm-2", "esm2", "prot-t5", "prott5", "alphafold", "boltz",
    "docker", "conda", "nextflow", "pytorch", "tensorflow",
}
PATH_PATTERN = re.compile(r"(?:^|\s)(?:[./~][\w./-]+|[\w.-]+\.(?:py|json|ya?ml|csv|fa(?:sta)?|pdb|txt|md))(?:\s|$)", re.I)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return [f"cannot parse {path}: {exc}"]
    conditions = data.get("stop_conditions") if isinstance(data, dict) else None
    if not isinstance(conditions, list) or not conditions:
        return ["top-level stop_conditions must be a non-empty list"]
    seen: set[str] = set()
    for index, condition in enumerate(conditions):
        where = f"condition {index + 1}"
        if not isinstance(condition, dict):
            errors.append(f"{where} is not a mapping")
            continue
        unknown = set(condition) - {"id", "threat", "predicate"}
        if unknown:
            errors.append(f"{where} has name-based selectors: {sorted(unknown)}")
        cid = condition.get("id")
        if not isinstance(cid, str) or not cid.strip() or cid in seen:
            errors.append(f"{where} has a missing or duplicate id")
        else:
            seen.add(cid)
        threat = condition.get("threat")
        if threat in PLATFORM_THREATS:
            errors.append(f"{where} gates a platform-enforced threat; this proxy is invalid")
        elif threat not in PROJECT_THREATS:
            errors.append(f"{where} threat must be a project-enforced threat T5-T8")
        predicate = condition.get("predicate")
        if not isinstance(predicate, str) or not predicate.strip():
            errors.append(f"{where} predicate is empty")
            continue
        lower = predicate.lower()
        named = sorted(name for name in PROHIBITED_NAMES if re.search(rf"\b{re.escape(name)}\b", lower))
        if named:
            errors.append(f"{where} names tools or packages: {', '.join(named)}")
        if PATH_PATTERN.search(predicate):
            errors.append(f"{where} names a path or file")
        if isinstance(threat, str) and not re.search(rf"\b{re.escape(threat)}\b", predicate):
            errors.append(f"{where} predicate does not state its threat identifier")
    return errors


def self_test() -> int:
    good = validate(ROOT / "gates/fixtures/pass.yaml")
    bad = validate(ROOT / "gates/fixtures/fail.yaml")
    platform = validate(ROOT / "gates/fixtures/fail_platform.yaml")
    if good or not bad or not platform:
        print(f"self-test failed: pass={good!r} fail={bad!r} platform={platform!r}", file=sys.stderr)
        return 1
    print("PASS validate_stop_conditions self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.files:
        parser.error("at least one stop-condition YAML file is required")
    failed = False
    for path in args.files:
        errors = validate(path)
        for error in errors:
            print(f"{path}: ERROR: {error}", file=sys.stderr)
        failed |= bool(errors)
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
