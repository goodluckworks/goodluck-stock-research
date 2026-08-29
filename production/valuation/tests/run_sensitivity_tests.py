#!/usr/bin/env python3
"""Tests for sensitivity engine."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VAL = ROOT / "goodluck-stock-research" / "production" / "valuation"
sys.path.insert(0, str(VAL))

from sensitivity_engine import build_sensitivity  # noqa: E402


def main() -> int:
    rows = build_sensitivity(100, {"growth": [-0.1, 0.0, 0.1], "margin": [-0.05, 0.05]})
    assert len(rows) == 5
    assert rows[0]["scenario_value"] == 90
    print("PASS: sensitivity tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
