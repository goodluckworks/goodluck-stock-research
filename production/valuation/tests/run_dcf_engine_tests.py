#!/usr/bin/env python3
"""Tests for DCF engine."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VAL = ROOT / "goodluck-stock-research" / "production" / "valuation"
sys.path.insert(0, str(VAL))

from dcf_engine import run_dcf  # noqa: E402


ASSUMPTIONS = {
    "bear": {"growth_rates": [0.02, 0.02], "discount_rate": 0.11, "terminal_growth": 0.02},
    "base": {"growth_rates": [0.05, 0.04], "discount_rate": 0.10, "terminal_growth": 0.025},
    "bull": {"growth_rates": [0.08, 0.06], "discount_rate": 0.09, "terminal_growth": 0.03},
}


def main() -> int:
    output = run_dcf(100, ASSUMPTIONS, {"decision": "usable_internal"})
    assert output["status"] == "available"
    assert len(output["scenarios"]) == 3
    blocked = run_dcf(100, ASSUMPTIONS, {"decision": "production_blocked"})
    assert blocked["status"] == "blocked"
    bad = {**ASSUMPTIONS, "bear": {"growth_rates": [0.02], "discount_rate": 0.02, "terminal_growth": 0.02}}
    try:
        run_dcf(100, bad, {"decision": "usable_internal"})
        raise AssertionError("invalid discount rate should fail")
    except ValueError:
        pass
    print("PASS: DCF engine tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
