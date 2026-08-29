#!/usr/bin/env python3
"""Tests for filing identity and amendment discovery."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "identity"))

import amendment_discovery
import filing_identity_resolver


def main() -> int:
    source = {
        "source_url": "https://www.sec.gov/Archives/edgar/data/1835632/0001835632-26-000011.txt",
        "sha256": "abc",
    }
    identity = filing_identity_resolver.resolve_identity(source, ticker="MRVL", cik="0001835632", form="10-K", filing_date="2026-03-11")
    assert identity["accession"] == "0001835632-26-000011"
    assert identity["latest_effective_claim"] is False
    status = amendment_discovery.discover(identity, [{"form": "10-K/A", "amends_accession": "0001835632-26-000011"}])
    assert status["amendment_found"] is True
    assert status["latest_effective_established"] is False
    clean = amendment_discovery.discover(identity, [])
    assert clean["latest_effective_established"] is True
    print("PASS: filing identity resolver tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
