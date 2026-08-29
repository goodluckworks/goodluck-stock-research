#!/usr/bin/env python3
"""Tests for historical statement and metrics."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HISTORY = ROOT / "goodluck-stock-research" / "production" / "history"
sys.path.insert(0, str(HISTORY))

from filing_history_builder import build_filing_history  # noqa: E402
from historical_metrics import compute_historical_metrics  # noqa: E402
from historical_statement_builder import build_historical_statement  # noqa: E402


def main() -> int:
    filings = [
        {"period_type": "quarterly", "period_end": f"2026-0{i}-30", "fiscal_period": f"Q{i}", "accession": str(i), "source_url": "sec", "statement": {"revenue": 100 + i, "net_income": 10, "operating_cash_flow": 20}}
        for i in range(1, 9)
    ]
    history = build_filing_history(filings, "quarterly")
    statement = build_historical_statement(history)
    assert len(statement["rows"]) == 8
    assert statement["zero_fill_used"] is False
    metrics = compute_historical_metrics(statement)
    assert metrics["annualization_used"] is False
    assert metrics["metrics"][1]["revenue_growth"] is not None
    filings[0]["statement"] = {"revenue": 1}
    statement = build_historical_statement(build_filing_history(filings, "quarterly"))
    assert any("missing" in item for item in statement["missing_periods_or_fields"])
    print("PASS: historical statement tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
