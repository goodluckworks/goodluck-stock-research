#!/usr/bin/env python3
"""Tests for evidence reconciliation."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "parser_readiness"))

import evidence_reconciliation_checker


def main() -> int:
    results = evidence_reconciliation_checker.audit(ROOT)
    failed = [item for item in results if not item.passed]
    assert not failed, evidence_reconciliation_checker.render(results)
    text = evidence_reconciliation_checker.render(results)
    assert "Draft candidates are not facts" in text
    assert "Quarantined data is not production data" in text
    print("PASS: evidence reconciliation tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
