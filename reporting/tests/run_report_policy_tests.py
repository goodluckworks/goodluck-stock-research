#!/usr/bin/env python3
"""Tests for report policy."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "reporting"))

import report_policy


def main() -> int:
    assert report_policy.forbidden_hits("target price: 10")
    assert report_policy.packet_type_for("EXMP") == "fictional_full_report_packet"
    assert report_policy.packet_type_for("MRVL") == "real_company_quarantine_report_packet"
    assert report_policy.packet_type_for("NVDA") == "real_company_review_only_packet"
    print("PASS: report policy tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
