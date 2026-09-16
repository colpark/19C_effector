#!/usr/bin/env python3
"""Measure Foldseek recovery for families named independently in Predector annotations.

This deliberately recognises only explicit NLP, LysM, RxLR, Crinkler, MAX and
ToxA-like text.  It does not infer a family from a structure or a Foldseek result.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    "NLP": re.compile(r"\bNLP\b|necrosis.?and.?ethylene", re.I),
    "LysM": re.compile(r"\bLysM\b", re.I),
    "RxLR": re.compile(r"\bRxLR\b", re.I),
    "Crinkler": re.compile(r"\bCrinkler\b|\bCRN\b", re.I),
    "MAX": re.compile(r"\bMAX(?:[- ]?(?:like|effector))?\b", re.I),
    "ToxA-like": re.compile(r"\bToxA(?:-like)?\b", re.I),
}


def model_accession(value: str) -> str:
    if value.startswith("ESMF-"):
        return value[5:]
    if value.startswith("AF-") and value.endswith("-F1"):
        return value[3:-3]
    raise ValueError(f"unrecognised Foldseek member {value!r}")


def wilson(successes: int, total: int) -> tuple[float, float]:
    """Approximate two-sided 95% Wilson interval."""
    if not total:
        return (0.0, 1.0)
    z = 1.959963984540054
    p = successes / total
    den = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / den
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / den
    return max(0.0, centre - half), min(1.0, centre + half)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provenance", type=Path, default=ROOT / "data/positives/provenance.tsv")
    parser.add_argument("--annotations", type=Path, default=ROOT / "data/raw/predector/data/fungal_effectors.tsv")
    parser.add_argument("--manifest", type=Path, default=ROOT / "data/raw/esmfold_manifest.json")
    parser.add_argument("--clusters", type=Path, nargs="+", required=True,
                        help="threshold:path pairs, e.g. 0.50:path.tsv")
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    with args.provenance.open(encoding="utf-8", newline="") as h:
        provenance = list(csv.DictReader(h, delimiter="\t"))
    aliases: dict[str, str] = {}
    for row in provenance:
        aliases[row["accession"]] = row["accession"]
        if row.get("uniprot_accession"):
            aliases[row["uniprot_accession"]] = row["accession"]
    with args.manifest.open(encoding="utf-8") as h:
        esm = {x["accession"]: float(x["mean_plddt"]) for x in json.load(h)}
    # AF models have pLDDT in the CA B-factor, recorded on the 0..100 scale.
    af_scores: dict[str, float] = {}
    for path in (ROOT / "data/raw/alphafold").glob("AF-*-F1.pdb"):
        scores = [float(line[60:66]) / 100 for line in path.read_text(encoding="utf-8").splitlines()
                  if line.startswith("ATOM") and line[12:16].strip() == "CA"]
        if scores:
            af_scores[path.name[3:-7]] = sum(scores) / len(scores)
    scores = {**af_scores, **esm}

    assignments: dict[str, set[str]] = defaultdict(set)
    evidence: dict[tuple[str, str], str] = {}
    with args.annotations.open(encoding="utf-8", newline="") as h:
        for row in csv.DictReader(h, delimiter="\t"):
            text = " ".join(row.get(k, "") for k in ("gene", "names", "notes", "phibase_terms"))
            tokens = []
            for key in ("uniprot", "genbank"):
                tokens.extend(x.strip() for x in row.get(key, "").split(";") if x.strip())
            for family, pattern in FAMILIES.items():
                if not pattern.search(text):
                    continue
                for token in tokens:
                    accession = aliases.get(token)
                    if accession and accession in scores:
                        assignments[family].add(accession)
                        evidence[(family, accession)] = text

    args.ground_truth.parent.mkdir(parents=True, exist_ok=True)
    with args.ground_truth.open("w", encoding="utf-8", newline="") as h:
        writer = csv.writer(h, delimiter="\t")
        writer.writerow(["family", "accession", "mean_plddt", "confidence_band", "annotation_text"])
        for family in FAMILIES:
            for accession in sorted(assignments[family]):
                p = scores[accession]
                writer.writerow([family, accession, f"{p:.6f}", "high" if p >= .5 else "low",
                                 evidence[(family, accession)]])

    result: dict[str, object] = {
        "method": "Explicit annotation regexes only; cluster results are read after family labels are fixed.",
        "family_patterns": {k: v.pattern for k, v in FAMILIES.items()},
        "families_recovered": {k: len(v) for k, v in assignments.items()},
        "structurally_mapped_members": sum(map(len, assignments.values())),
        "thresholds": {},
    }
    for raw_spec in args.clusters:
        spec = str(raw_spec)
        threshold, path_s = spec.split(":", 1)
        cluster_of: dict[str, str] = {}
        members: dict[str, set[str]] = defaultdict(set)
        with Path(path_s).open(encoding="utf-8") as h:
            for line in h:
                rep, member = line.rstrip("\n").split("\t")
                a = model_accession(member)
                cluster_of[a] = model_accession(rep)
                members[model_accession(rep)].add(a)
        family_result: dict[str, object] = {}
        low_singletons = 0
        low_singletons_with_high_relatives = 0
        for family, family_members in assignments.items():
            by_band = {"high": sorted(a for a in family_members if scores[a] >= .5),
                       "low": sorted(a for a in family_members if scores[a] < .5)}
            bands: dict[str, object] = {}
            for band, xs in by_band.items():
                if not xs:
                    bands[band] = {"members": 0, "largest_same_family_cluster_fraction": None}
                    continue
                counts = Counter(cluster_of[a] for a in xs)
                bands[band] = {"members": len(xs),
                               "largest_same_family_cluster_fraction": max(counts.values()) / len(xs),
                               "clusters_occupied": len(counts)}
            high_clustered = any(sum(1 for a in family_members if scores[a] >= .5 and
                                     cluster_of[a] == cluster_of[h]) >= 2
                                 for h in family_members if scores[h] >= .5)
            flagged = []
            for a in by_band["low"]:
                if len(members[cluster_of[a]]) == 1:
                    low_singletons += 1
                    if high_clustered:
                        low_singletons_with_high_relatives += 1
                        flagged.append(a)
            family_result[family] = {"members": len(family_members), "by_confidence": bands,
                                     "low_singletons_with_confident_clustered_relatives": flagged}
        all_low_singletons = sum(1 for a, rep in cluster_of.items()
                                 if scores.get(a, 1) < .5 and len(members[rep]) == 1)
        lo, hi = wilson(low_singletons_with_high_relatives, low_singletons)
        rate = (low_singletons_with_high_relatives / low_singletons) if low_singletons else 0.0
        result["thresholds"][threshold] = {
            "families": family_result,
            "low_known_family_singletons": low_singletons,
            "low_singletons_with_confident_relatives_clustered": low_singletons_with_high_relatives,
            "estimated_false_singleton_rate": rate,
            "estimated_false_singleton_rate_95_wilson": [lo, hi],
            "all_low_confidence_singletons": all_low_singletons,
            "estimated_nonreal_singleton_clusters": rate * all_low_singletons,
            "estimated_nonreal_singleton_clusters_95_wilson": [lo * all_low_singletons, hi * all_low_singletons],
        }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
