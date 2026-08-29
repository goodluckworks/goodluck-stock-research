#!/usr/bin/env python3
"""Tests for normalized financial statement builder."""

from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser"))
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "normalization"))

import production_xbrl_parser
import financial_statement_builder
import statement_auditor


def main() -> int:
    package = production_xbrl_parser.load_package(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser" / "fixtures" / "standard_10k_package.json")
    parsed = production_xbrl_parser.parse_package(package)
    result = financial_statement_builder.build(parsed)
    assert result["rows"]
    assert result["no_zero_fill"] is True
    for row in result["rows"]:
        assert row["source_locator"] and row["concept_qname"] and row["confidence"]
    partial = dict(parsed)
    partial["fields"] = [item for item in parsed["fields"] if item["field"] != "gross_profit"] + [{"field": "gross_profit", "status": "unresolved", "reason": "missing field"}]
    partial_result = financial_statement_builder.build(partial)
    assert partial_result["unresolved_fields"]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        financial_statement_builder.write_artifacts(result, out)
        assert not statement_auditor.audit(out)
        assert (out / "normalized_metrics_input.csv").exists()
        assert (out / "statement_audit_report.md").exists()
    print("PASS: normalized financial statement builder tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
