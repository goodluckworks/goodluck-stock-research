#!/usr/bin/env python3
"""Tests for source quality audit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "goodluck-stock-research" / "production" / "audit"
sys.path.insert(0, str(AUDIT))

from source_quality_audit import audit_source_quality  # noqa: E402


def main() -> int:
    issues = audit_source_quality({"issuer_type": "bank", "market_data_status": "unavailable"})
    assert "unsupported issuer type" in issues
    assert "market data unavailable" in issues
    assert "missing source URL" in issues
    assert not audit_source_quality({"issuer_type": "semiconductor", "market_data_status": "available", "source_url": "https://www.sec.gov"})
    print("PASS: source quality audit tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
