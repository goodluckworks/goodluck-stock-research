#!/usr/bin/env python3
"""Tests for release candidate audit."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "qa"))

import release_candidate_audit


def main() -> int:
    results = release_candidate_audit.audit(ROOT)
    failed = [item for item in results if not item.passed]
    assert not failed, release_candidate_audit.render(results)
    assert "Needs user decision" in release_candidate_audit.render(results)
    print("PASS: release candidate audit tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
