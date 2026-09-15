#!/usr/bin/env python3
"""Fail closed when a stage prompt drops or contradicts the constitution."""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = ROOT / "constitution.md"
AXES = ("positive supply, sequence clusters", "positive supply, structural clusters",
        "negative supply", "contamination exposure", "tool coverage")
TOOL_NAMES = ("signalp", "tmhmm", "phobius", "predector", "peace", "effectorp",
              "foldseek", "esmfold", "prot-t5", "prott5", "alphafold", "boltz")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    expected = CONSTITUTION.read_text(encoding="utf-8").rstrip()
    text = path.read_text(encoding="utf-8")
    if not text.startswith(expected):
        errors.append("the exact ordered constitution is not prepended")
    lower = text.lower()
    count_requested = bool(re.search(r"\b(count|enumerat(?:e|ion)|report)\b", lower))
    mentioned = [axis for axis in AXES if axis in lower]
    if count_requested and 0 < len(mentioned) < len(AXES):
        errors.append("a count request names fewer than all five axes")
    for section in re.split(r"(?im)^##+\s+", text)[1:]:
        title, _, body = section.partition("\n")
        if "stop" in title.lower() and any(re.search(rf"\b{re.escape(tool)}\b", body.lower()) for tool in TOOL_NAMES):
            errors.append("a stop condition names a tool instead of a threat")
    return errors


def self_test() -> int:
    prefix = CONSTITUTION.read_text(encoding="utf-8")
    cases = {
        "valid": prefix + "\n## Stage\nOperate over all five axes.\n",
        "named_tool": prefix + "\n## Stop conditions\nStop if SignalP is present.\n",
        "single_axis": prefix + "\n## Stage\nCount positive supply, structural clusters.\n",
    }
    expected_failure = {"valid": False, "named_tool": True, "single_axis": True}
    with tempfile.TemporaryDirectory() as td:
        for name, body in cases.items():
            path = Path(td) / f"{name}.md"
            path.write_text(body, encoding="utf-8")
            failed = bool(validate(path))
            if failed != expected_failure[name]:
                print(f"self-test failed: {name}", file=sys.stderr)
                return 1
    print("PASS check_constitution self-test")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage_prompt", nargs="?", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.stage_prompt is None:
        parser.error("stage_prompt is required unless --self-test is used")
    errors = validate(args.stage_prompt)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())

