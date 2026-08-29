#!/usr/bin/env python3
"""Tests for quarantine QA."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "pipeline"))

import quarantine_qa


def main() -> int:
    results = quarantine_qa.qa_quarantine(ROOT, "MRVL")
    failed = [item for item in results if not item.passed]
    assert not failed, quarantine_qa.render(results)
    assert not (ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "NVDA").exists()
    assert not (ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "AVGO").exists()
    print("PASS: quarantine QA tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
