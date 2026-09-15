#!/usr/bin/env python3
"""Blind, stratum-separated scoring for panel submissions."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
from pathlib import Path
from statistics import NormalDist
from typing import Any

import yaml

MEASURE = "MEASURE"
STRATA = ("canonical", "non-canonical")


def read_document(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    value = json.loads(text) if path.suffix.lower() == ".json" else yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a mapping")
    return value


def ledger_items(path: Path) -> dict[str, dict[str, Any]]:
    data = read_document(path)
    items = data.get("elements")
    if not isinstance(items, list):
        raise ValueError("ledger elements are absent")
    result = {item.get("name"): item for item in items if isinstance(item, dict)}
    if len(result) != len(items):
        raise ValueError("ledger element names are missing or duplicated")
    return result


def numeric_value(items: dict[str, dict[str, Any]], name: str) -> float:
    if name not in items:
        raise ValueError(f"ledger element {name!r} is absent")
    value = items[name].get("current_value")
    if value == MEASURE:
        task = items[name].get("measured_by", "MEASURE")
        raise ValueError(f"ledger element {name!r} is MEASURE by {task}")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    match = re.match(r"^\s*([0-9]+(?:\.[0-9]+)?)\b", str(value))
    if not match:
        raise ValueError(f"ledger element {name!r} is not numeric: {value!r}")
    return float(match.group(1))


def parameters(path: Path) -> dict[str, float | int]:
    items = ledger_items(path)
    values: dict[str, float | int] = {
        "k": int(numeric_value(items, "k")),
        "n_cand": int(numeric_value(items, "n_cand")),
        "delta": numeric_value(items, "delta"),
        "samples_per_cell": int(numeric_value(items, "S, samples per cell")),
        "repair_budget": int(numeric_value(items, "Repair budget")),
        "alpha": numeric_value(items, "alpha"),
        "beta": numeric_value(items, "beta"),
    }
    if values["k"] <= 0 or values["n_cand"] < values["k"]:
        raise ValueError("ledger requires 0 < k <= n_cand")
    if values["samples_per_cell"] < 2:
        raise ValueError("coverage at 1 is forbidden; S must be at least 2")
    if values["repair_budget"] < 0:
        raise ValueError("repair budget cannot be negative")
    if not 0 < values["alpha"] < 1 or not 0 < values["beta"] < 1:
        raise ValueError("ledger alpha and beta must lie strictly between 0 and 1")
    return values


def power_quantities(sigma_d: float, n: int, delta: float, alpha: float, beta: float) -> dict[str, float | int]:
    if sigma_d < 0 or n <= 0 or delta <= 0:
        raise ValueError("sigma_d and delta must be nonnegative/positive and N must be positive")
    z_sum = NormalDist().inv_cdf(1 - alpha / 2) + NormalDist().inv_cdf(1 - beta)
    return {
        "sigma_d": sigma_d,
        "N": n,
        "N_min": math.ceil((z_sum * sigma_d / delta) ** 2),
        "MDE(N)": z_sum * sigma_d / math.sqrt(n),
    }


def validate_manifest(data: dict[str, Any], n_cand: int) -> dict[str, dict[str, Any]]:
    panels = data.get("panels")
    if not isinstance(panels, list) or not panels:
        raise ValueError("panel manifest requires a non-empty panels list")
    result: dict[str, dict[str, Any]] = {}
    for panel in panels:
        if not isinstance(panel, dict):
            raise ValueError("every panel must be a mapping")
        panel_id = panel.get("panel_id")
        stratum = panel.get("stratum")
        candidates = panel.get("candidate_ids")
        positives = panel.get("positive_ids")
        if not isinstance(panel_id, str) or not panel_id or panel_id in result:
            raise ValueError("panel IDs must be non-empty and unique")
        if stratum not in STRATA:
            raise ValueError(f"{panel_id}: stratum must be canonical or non-canonical")
        if not isinstance(candidates, list) or len(candidates) != n_cand or len(set(candidates)) != n_cand:
            raise ValueError(f"{panel_id}: candidate_ids must contain ledger n_cand unique IDs")
        if not isinstance(positives, list) or not set(positives).issubset(candidates):
            raise ValueError(f"{panel_id}: positive_ids must be a candidate subset")
        result[panel_id] = {"stratum": stratum, "candidates": set(candidates), "positives": set(positives)}
    return result


def validate_arm_name(value: Any) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z]+", value):
        raise ValueError("arms must arrive as uppercase letters")
    return value


def score_arm(data: dict[str, Any], panels: dict[str, dict[str, Any]], *, k: int,
              samples_per_cell: int, expected_repair_budget: int) -> dict[str, Any]:
    if any(key in data for key in ("grant", "grant_description", "arm_description")):
        raise ValueError("the scorer must never receive a grant description")
    arm = validate_arm_name(data.get("arm"))
    if data.get("repair_budget") != expected_repair_budget:
        raise ValueError(f"arm {arm}: repair budget differs from the ledger")
    selections = data.get("selections")
    if not isinstance(selections, list):
        raise ValueError(f"arm {arm}: selections must be a list")

    valid: dict[tuple[str, int], float] = {}
    failures: list[dict[str, Any]] = []
    for position, row in enumerate(selections):
        failure = None
        panel_id = row.get("panel_id") if isinstance(row, dict) else None
        replicate = row.get("replicate") if isinstance(row, dict) else None
        selected = row.get("selected_ids") if isinstance(row, dict) else None
        if not isinstance(row, dict) or not isinstance(panel_id, str) or panel_id not in panels:
            failure = "unknown or missing panel_id"
        elif not isinstance(replicate, int) or isinstance(replicate, bool) or replicate < 1:
            failure = "replicate must be a positive integer"
        elif not isinstance(selected, list):
            failure = "selected_ids extraction failed"
        elif len(selected) < k:
            failure = "fewer than k selections"
        elif len(set(selected[:k])) != k:
            failure = "top-k selections are not unique"
        elif not set(selected[:k]).issubset(panels[panel_id]["candidates"]):
            failure = "top-k selection is outside the panel"
        elif (panel_id, replicate) in valid:
            failure = "duplicate panel and replicate"
        if failure:
            failures.append({"position": position, "panel_id": panel_id, "reason": failure})
            continue
        hits = len(set(selected[:k]) & panels[panel_id]["positives"])
        valid[(panel_id, replicate)] = hits / k

    strata: dict[str, Any] = {}
    for stratum in STRATA:
        stratum_panels = sorted(panel_id for panel_id, panel in panels.items() if panel["stratum"] == stratum)
        precisions = [value for (panel_id, _), value in valid.items() if panel_id in stratum_panels]
        curve = {}
        for sample_count in range(2, samples_per_cell + 1):
            covered = sum(
                sum(1 for panel_id, _ in valid if panel_id == candidate) >= sample_count
                for candidate in stratum_panels
            )
            curve[str(sample_count)] = covered / len(stratum_panels) if stratum_panels else MEASURE
        strata[stratum] = {
            "precision_at_k": statistics.fmean(precisions) if precisions else MEASURE,
            "valid_item_count": len(precisions),
            "coverage_curve_at_S": curve,
        }
    return {
        "arm": arm,
        "repair_budget": expected_repair_budget,
        "strata": strata,
        "coverage_failure_count": len(failures),
        "coverage_failures": failures,
        "_valid_items": valid,
    }


def compare_arms(left: dict[str, Any], right: dict[str, Any], panels: dict[str, dict[str, Any]],
                 params: dict[str, float | int]) -> dict[str, Any]:
    result = {"arms": [left["arm"], right["arm"]], "strata": {}}
    for stratum in STRATA:
        keys = sorted(set(left["_valid_items"]) & set(right["_valid_items"]))
        keys = [key for key in keys if panels[key[0]]["stratum"] == stratum]
        differences = [left["_valid_items"][key] - right["_valid_items"][key] for key in keys]
        mean = statistics.fmean(differences) if differences else MEASURE
        sigma = statistics.stdev(differences) if len(differences) >= 2 else MEASURE
        power = (power_quantities(sigma, len(differences), float(params["delta"]),
                                  float(params["alpha"]), float(params["beta"]))
                 if sigma != MEASURE else {"sigma_d": MEASURE, "N": len(differences),
                                           "N_min": MEASURE, "MDE(N)": MEASURE})
        result["strata"][stratum] = {
            "paired_item_count": len(differences),
            "mean_paired_difference": mean,
            **power,
        }
    return result


def score(manifest: dict[str, Any], submissions: list[dict[str, Any]], ledger: Path) -> dict[str, Any]:
    params = parameters(ledger)
    panels = validate_manifest(manifest, int(params["n_cand"]))
    if len(submissions) != 2:
        raise ValueError("exactly two lettered arms are required for a paired comparison")
    arms = [score_arm(item, panels, k=int(params["k"]),
                      samples_per_cell=int(params["samples_per_cell"]),
                      expected_repair_budget=int(params["repair_budget"])) for item in submissions]
    if arms[0]["arm"] == arms[1]["arm"]:
        raise ValueError("paired arms must have different letters")
    if arms[0]["repair_budget"] != arms[1]["repair_budget"]:
        raise ValueError("repair budgets differ by arm")
    public_arms = []
    for arm in arms:
        public_arms.append({key: value for key, value in arm.items() if key != "_valid_items"})
    return {
        "metric": f"precision at {params['k']}",
        "chance_baseline": int(params["k"]) / int(params["n_cand"]),
        "coverage": f"curve from 2 through S={params['samples_per_cell']}",
        "arms": public_arms,
        "paired_comparison": compare_arms(arms[0], arms[1], panels, params),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=Path(__file__).resolve().parents[1] / "ledger/ledger.yaml")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--submission", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = score(read_document(args.manifest), [read_document(path) for path in args.submission], args.ledger)
    except (OSError, ValueError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
