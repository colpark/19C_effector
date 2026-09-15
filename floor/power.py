#!/usr/bin/env python3
"""Report N_min and MDE(N) from ledger thresholds and an input sigma_d."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scorer.score import ledger_items, numeric_value, power_quantities


def report(ledger: Path, sigma_d: float, n: int | None = None,
           effect: float | None = None) -> dict[str, object]:
    items = ledger_items(ledger)
    delta = numeric_value(items, "delta")
    alpha = numeric_value(items, "alpha")
    beta = numeric_value(items, "beta")
    if effect is not None and n is None:
        raise ValueError("refusing to print an effect without N and MDE(N) beside it")
    reference_n = n if n is not None else 1
    quantities = power_quantities(sigma_d, reference_n, delta, alpha, beta)
    result: dict[str, object] = {
        "sigma_d": sigma_d,
        "delta": delta,
        "alpha": alpha,
        "beta": beta,
        "N_min": quantities["N_min"],
    }
    if n is not None:
        result["N"] = n
        result["MDE(N)"] = quantities["MDE(N)"]
    if effect is not None:
        result["effect"] = effect
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=REPOSITORY_ROOT / "ledger/ledger.yaml")
    parser.add_argument("--sigma-d", type=float, required=True)
    parser.add_argument("--N", type=int)
    parser.add_argument("--effect", type=float)
    args = parser.parse_args()
    try:
        result = report(args.ledger, args.sigma_d, args.N, args.effect)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
