#!/usr/bin/env python3
"""Fetch AlphaFold DB models for UniProt accessions in the positive provenance."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

API = "https://alphafold.ebi.ac.uk/api/prediction/{accession}"
USER_AGENT = "19C-effector-gate1/1.0"


def fetch_bytes(url: str, attempts: int = 3) -> tuple[bytes, int]:
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read(), response.status
        except urllib.error.HTTPError as error:
            if error.code == 404:
                return b"", error.code
            if attempt == attempts - 1:
                raise
        except (TimeoutError, urllib.error.URLError):
            if attempt == attempts - 1:
                raise
        time.sleep(2 ** attempt)
    raise RuntimeError("unreachable retry state")


def fetch_one(accession: str, output_dir: Path) -> dict[str, str | int]:
    api_url = API.format(accession=accession)
    try:
        payload, api_status = fetch_bytes(api_url)
        if api_status == 404:
            return {"accession": accession, "status": "not_in_afdb", "api_http_status": 404,
                    "model_version": "", "model_url": "", "sha256": "", "bytes": 0}
        records = json.loads(payload)
        if not records:
            return {"accession": accession, "status": "not_in_afdb",
                    "api_http_status": api_status, "model_version": "", "model_url": "",
                    "sha256": "", "bytes": 0}
        record = records[0]
        model_url = record.get("pdbUrl", "")
        if not model_url:
            return {"accession": accession, "status": "no_pdb_url",
                    "api_http_status": api_status,
                    "model_version": record.get("latestVersion", ""), "model_url": "",
                    "sha256": "", "bytes": 0}
        model, model_status = fetch_bytes(model_url)
        destination = output_dir / f"AF-{accession}-F1.pdb"
        destination.write_bytes(model)
        return {"accession": accession, "status": "fetched",
                "api_http_status": api_status, "model_http_status": model_status,
                "model_version": record.get("latestVersion", ""), "model_url": model_url,
                "sha256": hashlib.sha256(model).hexdigest(), "bytes": len(model)}
    except Exception as error:  # preserve partial coverage and a machine-readable failure
        return {"accession": accession, "status": "error",
                "api_http_status": "", "model_version": "", "model_url": "",
                "sha256": "", "bytes": 0, "error": f"{type(error).__name__}: {error}"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provenance", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    with args.provenance.open(encoding="utf-8", newline="") as handle:
        accessions = sorted({row.get("uniprot_accession", "").strip()
                             for row in csv.DictReader(handle, delimiter="\t")
                             if row.get("uniprot_accession", "").strip()})
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(fetch_one, accession, args.output_dir): accession
                   for accession in accessions}
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda row: str(row["accession"]))
    fields = ["accession", "status", "api_http_status", "model_http_status",
              "model_version", "model_url", "sha256", "bytes", "error"]
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    with args.manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields, delimiter="\t", lineterminator="\n",
                                extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    counts = {status: sum(row["status"] == status for row in rows)
              for status in ("fetched", "not_in_afdb", "no_pdb_url", "error")}
    print(json.dumps({"requested": len(rows), **counts}, sort_keys=True))
    return 1 if counts["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
