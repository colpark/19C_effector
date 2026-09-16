#!/usr/bin/env python3
"""Apply the frozen canonical-profile definition to positive provenance."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

MAX_LENGTH = 300
MIN_CYSTEINES = 4
NAMED_CHECKS = ("FolSix12", "Vdlsc1", "BgtAVRa10", "FocSix8", "BghBEC3")
NONCLASSICAL = re.compile(r"\bnon[- ]classical(?:ly)?\b", re.IGNORECASE)


def sequence_hash(sequence: str) -> str:
    return hashlib.sha256(sequence.strip().upper().replace("*", "").encode()).hexdigest()


def classify(length: int, cysteines: int, explicitly_nonclassical: bool) -> tuple[str, str]:
    failures = []
    if length > MAX_LENGTH:
        failures.append("length>300")
    if cysteines < MIN_CYSTEINES:
        failures.append("cysteines<4")
    if explicitly_nonclassical:
        failures.append("source_explicitly_nonclassical")
    if failures:
        return "non-canonical", ";".join(failures)
    return "canonical", "length<=300;cysteines>=4;source_not_explicitly_nonclassical"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--predector", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    nonclassical_hashes: set[str] = set()
    named: dict[str, dict[str, object]] = {}
    with args.predector.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            sequence = row.get("sequence", "").strip().upper().replace("*", "")
            if not sequence:
                continue
            digest = sequence_hash(sequence)
            annotation = " ".join((row.get("notes", ""), row.get("entry_kind", "")))
            explicit = bool(NONCLASSICAL.search(annotation))
            if explicit:
                nonclassical_hashes.add(digest)
            gene = row.get("gene", "")
            if gene in NAMED_CHECKS:
                stratum, basis = classify(len(sequence), sequence.count("C"), explicit)
                named[gene] = {
                    "length": len(sequence),
                    "cysteine_count": sequence.count("C"),
                    "explicitly_nonclassical": explicit,
                    "profile_stratum": stratum,
                    "basis": basis,
                    "sequence_sha256": digest,
                }

    with args.provenance.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    for row in rows:
        digest = row["sequence_sha256"]
        stratum, basis = classify(int(row["length"]), int(row["cysteine_count"]),
                                  digest in nonclassical_hashes)
        row["profile_stratum"] = stratum
        row["canonical_profile_basis"] = basis
    for field in ("profile_stratum", "canonical_profile_basis"):
        if field not in fields:
            fields.append(field)
    temporary = args.provenance.with_suffix(args.provenance.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(args.provenance)

    retained_hashes = {row["sequence_sha256"] for row in rows}
    for result in named.values():
        result["retained_in_union"] = result["sequence_sha256"] in retained_hashes
    missing_named = sorted(set(NAMED_CHECKS) - set(named))
    if missing_named:
        raise ValueError(f"named profile checks absent from Predector source: {missing_named}")
    if any(result["profile_stratum"] != "non-canonical" for result in named.values()):
        raise ValueError("a prespecified non-canonical effector classified canonical")

    counts = Counter(row["profile_stratum"] for row in rows)
    report = {
        "definition": {
            "max_length": MAX_LENGTH,
            "min_cysteines": MIN_CYSTEINES,
            "exclude_explicit_nonclassical_secretion": True,
        },
        "profile_stratum_counts": dict(sorted(counts.items())),
        "named_checks": {name: named[name] for name in NAMED_CHECKS},
    }
    args.summary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                            encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
