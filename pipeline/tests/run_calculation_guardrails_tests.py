#!/usr/bin/env python3
"""Tests for quarantined calculation guardrails."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "pipeline"))

import calculation_guardrails


def main() -> int:
    assert calculation_guardrails.evaluate_calculation("ratio", quarantined_csv_exists=True, quarantined=True)["decision"] == "allow"
    assert calculation_guardrails.evaluate_calculation("ratio", quarantined_csv_exists=False, quarantined=True)["decision"] == "block"
    for tool in ("dcf", "peer_comps", "implied_expectations", "target_price", "recommendation", "position_size", "research_status"):
        decision = calculation_guardrails.evaluate_calculation(tool, quarantined_csv_exists=True, quarantined=True)
        assert decision["decision"] == "block", tool
    print("PASS: calculation guardrails tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
