#!/usr/bin/env python3
"""Tests for controlled market data source."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "goodluck-stock-research" / "production" / "sources"
sys.path.insert(0, str(SRC))

from market_data_source import MarketDataConfig, fetch_mockable_market_data, insufficient_market_data, load_user_csv  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "market.csv"
        path.write_text("ticker,price,currency,timestamp,market_session,source_status\nMRVL,70,USD,2026-07-07T20:00:00Z,regular_close,indicative\n", encoding="utf-8")
        result = load_user_csv(path)
        assert result["rows"][0]["ticker"] == "MRVL"
        bad = Path(tmp) / "bad.csv"
        bad.write_text("ticker,price\nMRVL,70\n", encoding="utf-8")
        try:
            load_user_csv(bad)
            raise AssertionError("missing fields should fail")
        except ValueError:
            pass
    config = MarketDataConfig(mode="mocked_live", source="https://finance.yahoo.com/quote/MRVL")
    mocked = fetch_mockable_market_data(config, lambda request, timeout: b"mock market data")
    assert mocked["manifest"]["reliability"] == "indicative"
    try:
        fetch_mockable_market_data(MarketDataConfig(mode="mocked_live", source="https://evil.example.com/MRVL"), lambda request, timeout: b"bad")
        raise AssertionError("non-allowlisted source should fail")
    except ValueError:
        pass
    assert insufficient_market_data("missing")["manifest"]["status"] == "insufficient_market_data"
    print("PASS: market data source tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
