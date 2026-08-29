#!/usr/bin/env python3
"""Tests for report red-team checks."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "reporting"))

import report_red_team


def main() -> int:
    cases = {
        "target price: 10": "forbidden conclusion",
        "buy: now": "forbidden conclusion",
        "position size: 5%": "forbidden conclusion",
        "quarantined data is production": "production",
        "draft candidates are facts": "fact",
        "no context": "audit references omitted",
        "/Users/example/path": "personal",
    }
    for text, expected in cases.items():
        issues = report_red_team.red_team_text(text)
        assert any(expected in issue for issue in issues), (text, issues)
    clean = "Not investment advice. Not for trading. Evidence and audit references. Missing evidence listed."
    assert not report_red_team.red_team_text(clean)
    print("PASS: report red-team tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
