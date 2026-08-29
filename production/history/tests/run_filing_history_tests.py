#!/usr/bin/env python3
"""Tests for filing history builder."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HISTORY = ROOT / "goodluck-stock-research" / "production" / "history"
sys.path.insert(0, str(HISTORY))

from filing_history_builder import build_filing_history  # noqa: E402


def main() -> int:
    filings = [
        {"period_type": "annual", "period_end": "2024-01-31", "fiscal_period": "FY2024", "accession": "1", "source_url": "sec", "superseded_by": "2"},
        {"period_type": "annual", "period_end": "2024-01-31", "fiscal_period": "FY2024A", "accession": "2", "source_url": "sec"},
        {"period_type": "annual", "period_end": "2025-01-31", "fiscal_period": "FY2025", "accession": "3", "source_url": "sec"},
        {"period_type": "annual", "period_end": "2026-01-31", "fiscal_period": "FY2026", "accession": "4", "source_url": "sec"},
    ]
    history = build_filing_history(filings, "annual")
    assert len(history["selected_filings"]) == 3
    assert len(history["superseded_filings"]) == 1
    assert history["all_periods_trace_to_accession"] is True
    print("PASS: filing history tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
