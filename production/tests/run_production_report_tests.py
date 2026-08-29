#!/usr/bin/env python3
"""Tests for production report builder."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "report_generation"))

import production_report_builder


def main() -> int:
    report = production_report_builder.build_report(
        "MRVL",
        {"fiscal_period": "FY2026", "rows": [1, 2], "unresolved_fields": []},
        {"fair_value_range": {"low": 1, "high": 2}},
        {"conclusion_label": "constructive", "confidence": "medium", "evidence_basis": ["source"], "valuation_basis": {}, "data_quality_caveats": [], "missing_evidence": [], "key_downside_risks": []},
    )
    assert "Executive Summary" in report
    assert "Not personalized advice" in report
    assert not production_report_builder.audit_report(report)
    bad = report + "\nbuy now"
    assert production_report_builder.audit_report(bad)
    print("PASS: production report tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
