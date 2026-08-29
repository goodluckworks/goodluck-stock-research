#!/usr/bin/env python3
"""Tests for report usability audit."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
USABILITY = ROOT / "goodluck-stock-research" / "production" / "usability"
sys.path.insert(0, str(USABILITY))

from report_usability_audit import audit_report_usability  # noqa: E402


def main() -> int:
    good = """# MRVL Production Research Report Draft
Research view: Neutral
Confidence: Medium
This draft is not personalized advice, not a trade instruction, and not position sizing.
## Caveats
- Source limited.
"""
    assert not audit_report_usability(good), audit_report_usability(good)
    bad = "buy now\nposition size: 10%\n"
    assert audit_report_usability(bad)
    print("PASS: report usability tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
