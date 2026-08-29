#!/usr/bin/env python3
"""Tests for valuation auditor."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VAL = ROOT / "goodluck-stock-research" / "production" / "valuation"
sys.path.insert(0, str(VAL))

from valuation_auditor import audit_valuation  # noqa: E402


def main() -> int:
    clean = {"status": "available", "assumptions": {}, "range": {"label": "scenario output, not recommendation"}}
    assert not audit_valuation(clean)
    assert audit_valuation({"status": "available", "note": "buy now"})
    assert audit_valuation({"status": "available", "range": {"label": "range"}})
    print("PASS: valuation auditor tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
