#!/usr/bin/env python3
"""Tests for v2.1 source registry."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "goodluck-stock-research" / "production" / "sources"
sys.path.insert(0, str(SRC))

from source_registry import register_source, resolve_market_data, write_registered_manifest  # noqa: E402


def main() -> int:
    manifest = {"source_type": "sec", "source": "https://www.sec.gov", "reliability": "primary_official"}
    entry = register_source("sec", "https://www.sec.gov", manifest)
    assert entry["source_reliability_score"] == 0.95
    try:
        register_source("unknown", "x", {})
        raise AssertionError("unsupported source should fail")
    except ValueError:
        pass
    try:
        register_source("sec", "x", {"api_key": "secret"})
        raise AssertionError("forbidden payload should fail")
    except ValueError:
        pass
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "market.csv"
        path.write_text("ticker,price,currency,timestamp,market_session,source_status\nMRVL,70,USD,2026-07-07T20:00:00Z,regular_close,indicative\n", encoding="utf-8")
        csv_entry = resolve_market_data(path)
        assert csv_entry["source_type"] == "market_data_csv"
        out = Path(tmp) / "manifest.json"
        write_registered_manifest(csv_entry, out)
        assert out.is_file()
    missing = resolve_market_data(None)
    assert missing["manifest"]["status"] == "insufficient_market_data"
    print("PASS: source registry tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
