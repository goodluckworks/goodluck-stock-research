#!/usr/bin/env python3
"""Tests for comps auditor."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
COMPS = ROOT / "goodluck-stock-research" / "production" / "comps"
sys.path.insert(0, str(COMPS))

from comps_auditor import audit_comps  # noqa: E402


def main() -> int:
    assert not audit_comps({"status": "blocked", "reason": "insufficient market data blocks comps conclusion"})
    issues = audit_comps({"status": "available", "rows": [{"ticker": "AMD", "data_status": "available"}]})
    assert any("missing market data source" in issue for issue in issues)
    issues = audit_comps({"status": "available", "note": "buy now"})
    assert any("Forbidden" in issue for issue in issues)
    print("PASS: comps auditor tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
