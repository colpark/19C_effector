#!/usr/bin/env python3
"""Cross-fit global and per-lifestyle mechanical weights on a guarded design split."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import statistics
import sys
from pathlib import Path
from statistics import NormalDist
from typing import Any

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scorer.score import ledger_items, numeric_value

PROTECTED_PATH_PARTS = {"scored_cohort", "labels", "runs"}


def guard_design_path(input_path: Path, design_root: Path) -> Path:
    candidate = input_path.resolve()
    root = design_root.resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("input is outside the declared design root")
    if PROTECTED_PATH_PARTS & set(candidate.parts):
        raise ValueError("protected scored or labelled path is forbidden for fitting")
    return candidate


def read_design(input_path: Path, design_root: Path) -> dict[str, Any]:
    candidate = guard_design_path(input_path, design_root)
    data = json.loads(candidate.read_text(encoding="utf-8"))
    if data.get("split_role") != "design" or data.get("eligible_for_scoring") is not False:
        raise ValueError("input must declare split_role=design and eligible_for_scoring=false")
    return data


def precision_at_k(item: dict[str, Any], weights: tuple[float, ...], channels: list[str], k: int) -> float:
    labels = item.get("labels")
    values = item.get("channels")
    if not isinstance(labels, list) or not isinstance(values, dict):
        raise ValueError("each item requires labels and channels")
    if set(values) != set(channels):
        raise ValueError("channel sets differ between items")
    if len(labels) < k or any(len(values[name]) != len(labels) for name in channels):
        raise ValueError("channel vectors must match labels and contain at least k candidates")
    scores = [sum(weight * float(values[name][index]) for weight, name in zip(weights, channels))
              for index in range(len(labels))]
    ranking = sorted(range(len(scores)), key=lambda index: (-scores[index], index))[:k]
    return sum(1 for index in ranking if bool(labels[index])) / k


def candidate_weights(channel_count: int) -> list[tuple[float, ...]]:
    result = []
    for mask in itertools.product((0, 1), repeat=channel_count):
        selected = sum(mask)
        if selected:
            result.append(tuple(value / selected for value in mask))
    return result


def fit(items: list[dict[str, Any]], channels: list[str], k: int) -> tuple[tuple[float, ...], float]:
    if not items:
        raise ValueError("cannot fit weights without design items")
    candidates = candidate_weights(len(channels))
    scored = [(statistics.fmean(precision_at_k(item, weights, channels, k) for item in items), weights)
              for weights in candidates]
    best_score = max(value for value, _ in scored)
    best_weights = min(weights for value, weights in scored if value == best_score)
    return best_weights, best_score


def analyze(data: dict[str, Any], ledger: Path) -> dict[str, Any]:
    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("design data requires items")
    channels = sorted(items[0].get("channels", {}))
    if not channels:
        raise ValueError("design data has no channels")
    ledger_data = ledger_items(ledger)
    k = int(numeric_value(ledger_data, "k"))
    delta = numeric_value(ledger_data, "delta")
    alpha = numeric_value(ledger_data, "alpha")
    lifestyles = sorted({item.get("lifestyle") for item in items})
    if any(not isinstance(value, str) or not value for value in lifestyles):
        raise ValueError("every design item requires a lifestyle")
    for lifestyle in lifestyles:
        if sum(item["lifestyle"] == lifestyle for item in items) < 2:
            raise ValueError("leave-one-item-out fitting requires at least two items per lifestyle")

    global_weights, global_precision = fit(items, channels, k)
    oracle_weights = {}
    oracle_precision = {}
    in_sample_differences = []
    for lifestyle in lifestyles:
        group = [item for item in items if item["lifestyle"] == lifestyle]
        weights, precision = fit(group, channels, k)
        oracle_weights[lifestyle] = dict(zip(channels, weights))
        oracle_precision[lifestyle] = precision
        in_sample_differences.extend(
            precision_at_k(item, weights, channels, k)
            - precision_at_k(item, global_weights, channels, k)
            for item in group
        )

    cross_fitted_differences = []
    cross_fitted_items = []
    for held_out_index, item in enumerate(items):
        training = [candidate for index, candidate in enumerate(items) if index != held_out_index]
        lifestyle_training = [
            candidate for candidate in training
            if candidate["lifestyle"] == item["lifestyle"]
        ]
        fold_global_weights, _ = fit(training, channels, k)
        fold_lifestyle_weights, _ = fit(lifestyle_training, channels, k)
        global_score = precision_at_k(item, fold_global_weights, channels, k)
        lifestyle_score = precision_at_k(item, fold_lifestyle_weights, channels, k)
        difference = lifestyle_score - global_score
        cross_fitted_differences.append(difference)
        cross_fitted_items.append({
            "item_id": item.get("item_id", f"item-{held_out_index}"),
            "lifestyle": item["lifestyle"],
            "global_precision_at_k": global_score,
            "lifestyle_precision_at_k": lifestyle_score,
            "difference": difference,
        })

    headroom = statistics.fmean(cross_fitted_differences)
    in_sample_headroom = statistics.fmean(in_sample_differences)
    sigma = (statistics.stdev(cross_fitted_differences)
             if len(cross_fitted_differences) >= 2 else 0.0)
    z = NormalDist().inv_cdf(1 - alpha / 2)
    half_width = z * sigma / math.sqrt(len(cross_fitted_differences))
    return {
        "metric": f"precision at {k}",
        "channels": channels,
        "C": len(channels),
        "global": {"weights": dict(zip(channels, global_weights)), "precision": global_precision},
        "per_lifestyle_oracle_in_sample": {
            lifestyle: {
                "weights": oracle_weights[lifestyle],
                "precision": oracle_precision[lifestyle],
            }
            for lifestyle in lifestyles
        },
        "H_estimator": "leave-one-item-out cross-fitted",
        "H": headroom,
        "H_cross_fitted": headroom,
        "H_in_sample": in_sample_headroom,
        "H_in_sample_minus_cross_fitted": in_sample_headroom - headroom,
        "cross_fitted_items": cross_fitted_items,
        "interval": {"alpha": alpha, "lower": headroom - half_width,
                     "upper": headroom + half_width},
        "delta": delta,
        "decision": "above delta" if headroom > delta else "not above delta",
        "design_only_guard": "passed",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=REPOSITORY_ROOT / "ledger/ledger.yaml")
    parser.add_argument("--design-root", type=Path, required=True)
    parser.add_argument("--input", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = analyze(read_design(args.input, args.design_root), args.ledger)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
