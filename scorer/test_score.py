#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import yaml

from score import MEASURE, parameters, score
from synthetic import fixtures, malformed_extraction, synthetic_ledger

ROOT = Path(__file__).resolve().parents[1]


class ScorerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.ledger_path = Path(self.temp.name) / "ledger.yaml"
        ledger = synthetic_ledger(ROOT / "ledger/ledger.yaml")
        self.ledger_path.write_text(yaml.safe_dump(ledger, sort_keys=False), encoding="utf-8")
        self.manifest, self.left, self.right, self.planted = fixtures(ledger)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_known_effect_is_recovered_within_its_mde(self) -> None:
        result = score(self.manifest, [self.left, self.right], self.ledger_path)
        self.assertNotIn("pooled_result", result)
        self.assertNotIn("1", result["arms"][0]["strata"]["canonical"]["coverage_curve_at_S"])
        for stratum in ("canonical", "non-canonical"):
            comparison = result["paired_comparison"]["strata"][stratum]
            self.assertNotEqual(comparison["MDE(N)"], MEASURE)
            self.assertLessEqual(abs(comparison["mean_paired_difference"] - self.planted),
                                 comparison["MDE(N)"])

    def test_unexpected_valid_shape_is_coverage_failure_not_zero(self) -> None:
        malformed = malformed_extraction(self.left)
        result = score(self.manifest, [malformed, self.right], self.ledger_path)
        arm = result["arms"][0]
        self.assertEqual(arm["coverage_failure_count"], 1)
        self.assertEqual(arm["coverage_failures"][0]["reason"], "selected_ids extraction failed")
        valid_total = sum(value["valid_item_count"] for value in arm["strata"].values())
        self.assertEqual(valid_total, len(self.left["selections"]) - 1)

    def test_unequal_or_nonledger_repair_budget_refuses(self) -> None:
        altered = dict(self.left)
        altered["repair_budget"] = self.left["repair_budget"] + 1
        with self.assertRaisesRegex(ValueError, "repair budget"):
            score(self.manifest, [altered, self.right], self.ledger_path)

    def test_grant_description_is_refused(self) -> None:
        described = dict(self.left)
        described["grant_description"] = "must never reach scorer"
        with self.assertRaisesRegex(ValueError, "grant description"):
            score(self.manifest, [described, self.right], self.ledger_path)

    def test_real_ledger_fails_closed_while_measurements_are_absent(self) -> None:
        with self.assertRaisesRegex(ValueError, "MEASURE"):
            parameters(ROOT / "ledger/ledger.yaml")


if __name__ == "__main__":
    unittest.main()
