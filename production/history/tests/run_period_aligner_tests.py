#!/usr/bin/env python3
"""Tests for period aligner."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HISTORY = ROOT / "goodluck-stock-research" / "production" / "history"
sys.path.insert(0, str(HISTORY))

from period_aligner import select_history  # noqa: E402


def main() -> int:
    filings = [{"period_type": "annual", "period_end": f"202{i}-01-31", "fiscal_period": f"FY202{i}"} for i in range(1, 5)]
    selected, missing = select_history(filings, "annual")
    assert len(selected) == 3 and selected[0]["fiscal_period"] == "FY2022" and not missing
    selected, missing = select_history(filings[:2], "annual")
    assert len(selected) == 2 and missing
    try:
        select_history([{"period_type": "quarterly", "period_end": "2026-01-31", "fiscal_period": "FY2026"}], "annual")
        raise AssertionError("mismatched fiscal period should fail")
    except ValueError:
        pass
    print("PASS: period aligner tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
