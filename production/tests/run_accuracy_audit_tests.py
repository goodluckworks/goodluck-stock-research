#!/usr/bin/env python3
"""Tests for accuracy audit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "goodluck-stock-research" / "production" / "audit"
sys.path.insert(0, str(AUDIT))

from accuracy_audit import audit_accuracy  # noqa: E402


def main() -> int:
    statement = {"rows": [{"field": "revenue", "value": 100, "source": "sec"}, {"field": "net_income", "value": 10}]}
    issues = audit_accuracy(statement, {"revenue": 101, "net_income": 10})
    assert any("wrong financial value" in issue for issue in issues)
    assert any("missing source" in issue for issue in issues)
    assert not audit_accuracy({"rows": [{"field": "revenue", "value": 100, "source": "sec"}]}, {"revenue": 100})
    print("PASS: accuracy audit tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
