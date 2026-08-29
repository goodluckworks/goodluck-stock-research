#!/usr/bin/env python3
"""Tests for multiples valuation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VAL = ROOT / "goodluck-stock-research" / "production" / "valuation"
sys.path.insert(0, str(VAL))

from multiples_valuation import value_from_multiples  # noqa: E402


def main() -> int:
    output = value_from_multiples(100, {"low": 5, "high": 8}, "revenue")
    assert output["range"]["low"] == 500
    assert value_from_multiples(0, {"low": 5, "high": 8}, "revenue")["status"] == "blocked"
    print("PASS: multiples valuation tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
