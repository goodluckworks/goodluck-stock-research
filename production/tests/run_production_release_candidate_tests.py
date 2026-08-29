#!/usr/bin/env python3
"""Tests for production release-candidate audit."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "audit"))

import release_candidate_audit


def main() -> int:
    issues = release_candidate_audit.audit(ROOT)
    assert not issues, "\n".join(issues)
    print("PASS: production release-candidate tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
