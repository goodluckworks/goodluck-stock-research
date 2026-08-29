#!/usr/bin/env python3
"""Tests for repository red-team audit."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "qa"))

import red_team_audit


def main() -> int:
    issues = red_team_audit.audit(ROOT)
    assert not issues, "\n".join(issues)
    print("PASS: red-team audit tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
