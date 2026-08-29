#!/usr/bin/env python3
"""Tests for implied expectations."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VAL = ROOT / "goodluck-stock-research" / "production" / "valuation"
sys.path.insert(0, str(VAL))

from implied_expectations_engine import build_implied_expectations, implied_scale_up  # noqa: E402


def main() -> int:
    result = implied_scale_up(20, 5, 5)
    assert result["required_scale_up"] == 4
    full = build_implied_expectations({"ev_sales_current": 20, "target_ev_sales_mature": 5, "pe_current": 60, "target_pe_mature": 20, "p_fcf_current": 50, "target_p_fcf_mature": 25, "years_to_maturity": 5})
    assert full["no_deterministic_target_price"] is True
    try:
        implied_scale_up(0, 5, 5)
        raise AssertionError("non-positive multiple should fail")
    except ValueError:
        pass
    print("PASS: implied expectations tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
