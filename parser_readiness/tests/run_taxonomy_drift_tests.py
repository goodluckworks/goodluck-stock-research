#!/usr/bin/env python3
"""Tests for taxonomy drift checker."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "parser_readiness"))

import taxonomy_drift_checker


def main() -> int:
    results = taxonomy_drift_checker.audit(ROOT)
    failed = [item for item in results if not item.passed]
    assert not failed, taxonomy_drift_checker.render(results)
    assert "Production taxonomy coverage: No" in taxonomy_drift_checker.render(results)
    print("PASS: taxonomy drift tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
