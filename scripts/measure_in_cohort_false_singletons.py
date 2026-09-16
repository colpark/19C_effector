#!/usr/bin/env python3
"""Measure Foldseek recovery of confident relatives in frozen MMseqs2 clusters."""
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAUS = ("0.40", "0.50", "0.60")
AUDITED_SINGLETONS = {"0.40": 139, "0.50": 175, "0.60": 184}
RAW_CLUSTERS = {"0.40": 324, "0.50": 400, "0.60": 437}


def accession(model: str) -> str:
    if model.startswith("ESMF-"):
        return model[5:]
    if model.startswith("AF-") and model.endswith("-F1"):
        return model[3:-3]
    raise ValueError(f"unknown model identifier: {model}")


def wilson(k: int, n: int) -> tuple[float, float]:
    if not n:
        return 0.0, 1.0
    z = 1.959963984540054
    p = k / n
    denominator = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denominator
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denominator
    return max(0.0, center - half), min(1.0, center + half)


def mde(panels: int) -> float | None:
    if not panels:
        return None
    # Same fixed alpha=.05, beta=.20, sigma_d=.115 calculation as floor/power.py.
    return (1.959963984540054 + 0.8416212335729143) * .115 / math.sqrt(panels)


def read_structural(path: Path):
    by_member, members = {}, defaultdict(set)
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            rep, member = line.rstrip("\n").split("\t")
            rep, member = accession(rep), accession(member)
            by_member[member] = rep
            members[rep].add(member)
    return by_member, members


def main() -> int:
    with (ROOT / "data/raw/esmfold_manifest.json").open(encoding="utf-8") as h:
        scores = {r["accession"]: float(r["mean_plddt"]) for r in json.load(h)}
    provenance, aliases = {}, {}
    with (ROOT / "data/positives/provenance.tsv").open(encoding="utf-8", newline="") as h:
        for row in csv.DictReader(h, delimiter="\t"):
            provenance[row["accession"]] = row
            aliases[row["accession"]] = row["accession"]
            if row.get("uniprot_accession"):
                aliases[row["uniprot_accession"]] = row["accession"]
    sequence_cluster = defaultdict(set)
    with (ROOT / "data/measurements/mmseqs30/union_cluster.tsv").open(encoding="utf-8") as h:
        for line in h:
            rep, member = line.rstrip("\n").split("\t")
            sequence_cluster[rep].add(member)

    eligible = {}
    for rep, members in sequence_cluster.items():
        low = sorted(x for x in members if x in scores and scores[x] < .5)
        high = sorted(x for x in members if x in scores and scores[x] >= .5)
        if low and high:
            eligible[rep] = {"members": sorted(members), "low": low, "high": high}
    low_test = sorted(x for value in eligible.values() for x in value["low"])
    high_test = sorted(x for value in eligible.values() for x in value["high"])
    eligible_by_member = {x: rep for rep, value in eligible.items() for x in value["members"]}

    detail = []
    for rep, value in sorted(eligible.items()):
        for member in value["members"]:
            row = provenance[member]
            detail.append({"sequence_cluster": rep, "accession": member,
                           "mean_plddt": scores[member],
                           "confidence": "low" if scores[member] < .5 else "high",
                           "profile_stratum": row["profile_stratum"],
                           "organism": row["organism"]})

    result = {
        "method": "Direct same-cohort recovery of a confident frozen-MMseqs2-30%-identity relative; not a fold-family or distribution-transfer estimate.",
        "eligibility": {"mixed_sequence_clusters": len(eligible), "low_members": len(low_test),
                        "high_members": len(high_test), "criterion": "low <0.50 and high >=0.50 mean pLDDT"},
        "members": detail, "thresholds": {}}
    for tau in TAUS:
        by_member, structural = read_structural(ROOT / f"data/measurements/foldseek/corrected_full_tm{tau}_cluster.tsv")
        def has_relative(member: str) -> bool:
            own = eligible[eligible_by_member[member]]["members"]
            return any(other != member and by_member.get(other) == by_member[member] for other in own)
        def singleton(member: str) -> bool:
            return len(structural[by_member[member]]) == 1
        def wrong_join(member: str) -> bool:
            own = set(eligible[eligible_by_member[member]]["members"])
            return len(structural[by_member[member]]) > 1 and not bool(structural[by_member[member]] & (own - {member}))

        failures = [x for x in low_test if singleton(x) and not has_relative(x)]
        wrong = [x for x in low_test if wrong_join(x)]
        baseline = [x for x in high_test if singleton(x) and not has_relative(x)]
        low_lo, low_hi = wilson(len(failures), len(low_test))
        base_lo, base_hi = wilson(len(baseline), len(high_test))
        # Conservative interval for the excess of low-confidence failure over baseline.
        excess_point = max(0.0, len(failures)/len(low_test) - len(baseline)/len(high_test))
        excess_lo, excess_hi = max(0.0, low_lo-base_hi), max(0.0, low_hi-base_lo)

        singleton_strata = defaultdict(int)
        cluster_strata = defaultdict(int)
        for members in structural.values():
            cohort_members = {aliases[x] for x in members if x in aliases}
            # The Foldseek input names AlphaFold models by UniProt accession whereas
            # provenance may use the union accession.  Alias back before any stratum
            # accounting; no structural member without a provenance alias is counted.
            ss = {provenance[x]["profile_stratum"] for x in cohort_members}
            if not ss:
                continue
            cluster_strata["mixed" if len(ss) > 1 else next(iter(ss))] += 1
            if len(members) == 1:
                x = aliases.get(next(iter(members)))
                if x in scores and scores[x] < .5:
                    singleton_strata[provenance[x]["profile_stratum"]] += 1
        corrected = {}
        for label, rate in (("point", excess_point), ("lower", excess_lo), ("upper", excess_hi)):
            clusters = RAW_CLUSTERS[tau] - rate * AUDITED_SINGLETONS[tau]
            panels = math.floor(clusters / 5)
            corrected[label] = {"excess_rate": rate, "clusters": clusters, "panels_max": panels,
                                "MDE": mde(panels)}
        stratum_range = {}
        for stratum in ("canonical", "non-canonical"):
            raw = cluster_strata[stratum]
            singles = singleton_strata[stratum]
            stratum_range[stratum] = {"raw_clusters": raw, "low_confidence_singletons": singles,
                "corrected_clusters_interval": [raw - excess_hi*singles, raw - excess_lo*singles]}
        result["thresholds"][tau] = {
            "raw_clusters": len(structural), "audited_low_confidence_singletons": AUDITED_SINGLETONS[tau],
            "low_false_singleton": {"k": len(failures), "n": len(low_test), "rate": len(failures)/len(low_test),
                                    "wilson_95": [low_lo, low_hi], "members": failures},
            "low_wrong_join": {"k": len(wrong), "n": len(low_test), "rate": len(wrong)/len(low_test),
                               "wilson_95": list(wilson(len(wrong), len(low_test))), "members": wrong},
            "high_baseline_false_singleton": {"k": len(baseline), "n": len(high_test),
                                                "rate": len(baseline)/len(high_test), "wilson_95": [base_lo, base_hi], "members": baseline},
            "baseline_subtracted_excess": {"point": excess_point, "conservative_95_interval": [excess_lo, excess_hi]},
            "corrected_supply": corrected, "stratum_supply": stratum_range,
        }
    output = ROOT / "data/measurements/in_cohort_false_singleton_calibration.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    rows = ROOT / "data/measurements/in_cohort_false_singleton_test_set.tsv"
    with rows.open("w", encoding="utf-8", newline="") as h:
        writer = csv.DictWriter(h, fieldnames=["sequence_cluster", "accession", "mean_plddt", "confidence", "profile_stratum", "organism"], delimiter="\t")
        writer.writeheader(); writer.writerows(detail)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
