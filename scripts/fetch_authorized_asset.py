#!/usr/bin/env python3
"""Fetch one explicitly authorized asset and verify its declared SHA-256."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    "PEACE_CHECKPOINT", "PEACE_CURATED_CSVS", "PREDECTOR_CONFIRMED_SET",
    "MYCOCOSM_BULK", "SRA_RUN_MANIFEST", "EFFECTOR_PDB_MANIFEST",
    "NCBI_BLAST_PLUS", "TMALIGN", "ESM_CHECKPOINTS", "PROTT5_CHECKPOINT",
    "EFFECTORP", "DEEPLOC", "DEEPSIG", "TARGETP2", "SIGNALP", "TMHMM",
    "PHOBIUS", "REPEATMASKER", "DNDS_TOOL", "EVO2", "NUCLEOTIDE_TRANSFORMER",
}
LICENCE_BLOCKED = {"SIGNALP", "TMHMM", "PHOBIUS"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def output_inside_repository(path: Path) -> Path:
    resolved = path.resolve()
    if ROOT not in resolved.parents:
        raise ValueError("output must be inside the repository")
    return resolved


def instructions(asset: str) -> None:
    state = "licence clearance and written approval" if asset in LICENCE_BLOCKED else "source URL, written approval"
    print(f"{asset}: resolve {state}, destination, and publisher checksum; then rerun with "
          "--url HTTPS_URL --output REPOSITORY_PATH --expected-sha256 SHA256 "
          "--authorized-by NAME --execute")


def self_test() -> int:
    documented = (ROOT / "docs/assets.md").read_text(encoding="utf-8")
    absent = sorted(asset for asset in ASSETS if f"fetch_authorized_asset.py {asset} --instructions" not in documented)
    if absent:
        print(f"undocumented registry entries: {absent}", file=sys.stderr)
        return 1
    if documented.count("scripts/fetch_authorized_asset.py") != len(ASSETS):
        print("documented fetch invocation count differs from registry", file=sys.stderr)
        return 1
    print("PASS fetch_authorized_asset registry and documentation")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("asset", nargs="?", choices=sorted(ASSETS))
    parser.add_argument("--instructions", action="store_true")
    parser.add_argument("--url")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--expected-sha256")
    parser.add_argument("--authorized-by")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if not args.asset:
        parser.error("ASSET is required")
    if args.instructions:
        instructions(args.asset)
        return 0
    if not args.execute or not all((args.url, args.output, args.expected_sha256, args.authorized_by)):
        parser.error("fetching requires --execute, --url, --output, --expected-sha256 and --authorized-by")
    if not args.url.startswith("https://"):
        parser.error("only HTTPS sources are accepted")
    expected = args.expected_sha256.lower()
    if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
        parser.error("--expected-sha256 must be 64 lowercase hexadecimal characters")
    try:
        output = output_inside_repository(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary_name = tempfile.mkstemp(prefix=output.name, suffix=".partial", dir=output.parent)
        os.close(fd)
        temporary = Path(temporary_name)
        try:
            with urllib.request.urlopen(args.url, timeout=120) as response, temporary.open("wb") as handle:
                while chunk := response.read(1024 * 1024):
                    handle.write(chunk)
            actual = sha256(temporary)
            if actual != expected:
                raise ValueError(f"checksum mismatch: expected {expected}, got {actual}")
            os.replace(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
        receipt = {
            "asset": args.asset, "source_url": args.url, "sha256": expected,
            "authorized_by": args.authorized_by,
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
        }
        output.with_suffix(output.suffix + ".receipt.json").write_text(
            json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, urllib.error.URLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
