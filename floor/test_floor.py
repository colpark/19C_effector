#!/usr/bin/env python3

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from headroom import analyze, read_design
from power import report
from scorer.synthetic import synthetic_ledger

ROOT = Path(__file__).resolve().parents[1]


def add_channel_count(ledger: dict, count: int) -> None:
    item = next(value for value in ledger["elements"] if value["name"] == "C, channel count")
    item["current_value"] = count
    item.pop("measured_by", None)


def design_fixture(adaptive: bool) -> dict:
    items = []
    for index in range(4):
        first_stratum = index % 2 == 0
        labels = [0, 1] if adaptive and not first_stratum else [1, 0]
        channels = {"channel_a": [1, 0], "channel_b": [0, 1]}
        items.append({"item_id": f"synthetic-{index}",
                      "stratum": "first" if first_stratum else "second",
                      "labels": labels, "channels": channels})
    return {"split_role": "design", "eligible_for_scoring": False, "items": items}


class FloorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "design"
        self.root.mkdir()
        ledger = synthetic_ledger(ROOT / "ledger/ledger.yaml")
        add_channel_count(ledger, 2)
        next(item for item in ledger["elements"] if item["name"] == "k")["current_value"] = 1
        next(item for item in ledger["elements"] if item["name"] == "n_cand")["current_value"] = 2
        delta = next(item for item in ledger["elements"] if item["name"] == "delta")
        delta["current_value"] = 0.25
        self.ledger = Path(self.temp.name) / "ledger.yaml"
        self.ledger.write_text(yaml.safe_dump(ledger, sort_keys=False), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_design(self, name: str, adaptive: bool) -> Path:
        path = self.root / name
        path.write_text(json.dumps(design_fixture(adaptive)), encoding="utf-8")
        return path

    def test_planted_headroom_above_delta_is_detected(self) -> None:
        path = self.write_design("above.json", True)
        result = analyze(read_design(path, self.root), self.ledger)
        self.assertGreater(result["H"], result["delta"])
        self.assertEqual(result["decision"], "above delta")
        self.assertIn("lower", result["interval"])
        self.assertIn("upper", result["interval"])

    def test_planted_headroom_below_delta_is_not_detected(self) -> None:
        path = self.write_design("below.json", False)
        result = analyze(read_design(path, self.root), self.ledger)
        self.assertLessEqual(result["H"], result["delta"])
        self.assertEqual(result["decision"], "not above delta")

    def test_scored_path_is_rejected_before_read(self) -> None:
        scored_root = Path(self.temp.name) / "scored_cohort"
        scored_root.mkdir()
        path = scored_root / "must_not_read.json"
        path.write_text("not JSON and must not be read", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "outside the declared design root"):
            read_design(path, self.root)

    def test_effect_requires_mde(self) -> None:
        with self.assertRaisesRegex(ValueError, "MDE"):
            report(self.ledger, sigma_d=0.1, effect=0.2)
        result = report(self.ledger, sigma_d=0.1, n=8, effect=0.2)
        self.assertIn("effect", result)
        self.assertIn("MDE(N)", result)


if __name__ == "__main__":
    unittest.main()
