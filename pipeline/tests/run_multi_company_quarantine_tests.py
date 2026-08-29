#!/usr/bin/env python3
"""Tests for controlled multi-company quarantine dashboard."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "pipeline"))

import multi_company_quarantine_runner


def main() -> int:
    statuses = multi_company_quarantine_runner.evaluate(ROOT)
    by_ticker = {item.ticker: item for item in statuses}
    assert by_ticker["MRVL"].result == "pass"
    assert by_ticker["NVDA"].result == "blocked"
    assert by_ticker["AVGO"].result == "blocked"
    assert not (ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "NVDA").exists()
    assert not (ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "AVGO").exists()
    text = multi_company_quarantine_runner.render(statuses)
    for forbidden in ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:"):
        assert forbidden not in text.lower()
    assert "No production normalized input" in text
    print("PASS: multi-company quarantine tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
