#!/usr/bin/env python3
"""Tests for parser-readiness audit."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "parser_readiness"))

import parser_readiness_audit


def main() -> int:
    results = parser_readiness_audit.audit(ROOT)
    failed = [item for item in results if not item.passed]
    assert not failed, parser_readiness_audit.render(results)
    report = parser_readiness_audit.render(results)
    assert "production_parser_ready: No" in report
    assert "fixture-first" in report
    print("PASS: parser-readiness audit tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
