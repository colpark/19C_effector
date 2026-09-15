#!/usr/bin/env python3
"""Append a Referee-authorized amendment while retaining all prior values."""

from __future__ import annotations

import argparse
import copy
import os
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def amend(path: Path, element_name: str, value: str, reason: str, date: str, author: str) -> None:
    if author != "Referee":
        raise ValueError("only Referee may amend the ledger")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    matches = [item for item in data.get("elements", []) if item.get("name") == element_name]
    if len(matches) != 1:
        raise ValueError(f"expected one ledger element named {element_name!r}")
    item = matches[0]
    prior = copy.deepcopy(item.get("current_value"))
    item.setdefault("amendments", []).append({
        "date": date, "by": author, "reason": reason,
        "previous_value": prior, "new_value": value,
    })
    item["current_value"] = value
    item["set_on"] = date
    item["set_by"] = author
    fd, temporary = tempfile.mkstemp(prefix=path.name, suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def self_test() -> int:
    source = ROOT / "ledger/ledger.yaml"
    with tempfile.TemporaryDirectory() as td:
        target = Path(td) / "ledger.yaml"
        target.write_bytes(source.read_bytes())
        amend(target, "S, samples per cell", "7", "coverage curve", "2026-09-16", "Referee")
        item = next(x for x in yaml.safe_load(target.read_text())["elements"] if x["name"] == "S, samples per cell")
        if item["current_value"] != "7" or item["amendments"][0]["previous_value"] != "5 provisional":
            return 1
        try:
            amend(target, "k", "21", "unauthorized", "2026-09-16", "Instrument")
        except ValueError:
            print("PASS amend_ledger self-test")
            return 0
    return 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=ROOT / "ledger/ledger.yaml")
    parser.add_argument("--element")
    parser.add_argument("--value")
    parser.add_argument("--reason")
    parser.add_argument("--date")
    parser.add_argument("--by", dest="author", default="Referee")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not all((args.element, args.value, args.reason, args.date)):
        parser.error("--element, --value, --reason and --date are required")
    try:
        amend(args.ledger, args.element, args.value, args.reason, args.date, args.author)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
