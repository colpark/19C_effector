#!/usr/bin/env python3
"""Generate deterministic synthetic panels and blinded submissions."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml


def synthetic_ledger(source: Path) -> dict[str, Any]:
    data = yaml.safe_load(source.read_text(encoding="utf-8"))
    items = {item["name"]: item for item in data["elements"]}
    k = int(items["k"]["current_value"])
    for name, value in (
        ("S, samples per cell", 3),
        ("Repair budget", 0),
        ("alpha", 1 / k),
        ("beta", 1 / k),
        ("positives_per_panel", 5),
    ):
        if name in items:
            items[name]["current_value"] = value
            items[name].pop("measured_by", None)
        else:
            data["elements"].append({"name": name, "current_value": value,
                                     "set_by": "synthetic fixture", "amendments": []})
    return data


def fixtures(ledger_data: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], float]:
    items = {item["name"]: item for item in ledger_data["elements"]}
    k = int(items["k"]["current_value"])
    n_cand = int(items["n_cand"]["current_value"])
    samples = int(items["S, samples per cell"]["current_value"])
    repair = int(items["Repair budget"]["current_value"])
    positives_per_panel = int(items["positives_per_panel"]["current_value"])
    panels = []
    left_rows = []
    right_rows = []
    increments = (1, 2)
    for panel_index in range(4):
        panel_id = f"synthetic-{panel_index}"
        profile_stratum = "canonical" if panel_index < 2 else "non-canonical"
        candidates = [f"{panel_id}-candidate-{index}" for index in range(n_cand)]
        positives = candidates[:positives_per_panel]
        panels.append({"panel_id": panel_id, "profile_stratum": profile_stratum,
                       "candidate_ids": candidates, "positive_ids": positives})
        for replicate in range(1, samples + 1):
            base_hits = 1
            increment = increments[(panel_index + replicate) % len(increments)]
            for rows, hits in ((right_rows, base_hits), (left_rows, base_hits + increment)):
                selected = positives[:hits] + candidates[positives_per_panel:
                                                          positives_per_panel + (k - hits)]
                rows.append({"panel_id": panel_id, "replicate": replicate,
                             "selected_ids": selected})
    left = {"arm": "A", "repair_budget": repair, "selections": left_rows}
    right = {"arm": "B", "repair_budget": repair, "selections": right_rows}
    planted_effect = statistics_mean(increments) / k
    return {"panels": panels}, left, right, planted_effect


def statistics_mean(values: tuple[int, ...]) -> float:
    return sum(values) / len(values)


def malformed_extraction(submission: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(submission)
    row = result["selections"][0]
    row["choices"] = row.pop("selected_ids")
    return result
