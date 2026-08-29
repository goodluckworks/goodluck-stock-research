#!/usr/bin/env python3
"""Tests for data quality and reconciliation."""

from pathlib import Path
import copy
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser"))
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "normalization"))
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "data_quality"))

import production_xbrl_parser
import financial_statement_builder
import data_quality_engine
import reconciliation_engine
import quality_gate


def base_statement():
    package = production_xbrl_parser.load_package(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser" / "fixtures" / "standard_10k_package.json")
    return financial_statement_builder.build(production_xbrl_parser.parse_package(package))


def main() -> int:
    statement = base_statement()
    quality = data_quality_engine.score_quality(statement)
    recon = reconciliation_engine.reconcile(statement)
    assert quality_gate.gate(quality, recon)["decision"] == "usable_internal"
    amended = data_quality_engine.score_quality(statement, {"restatement_found": True})
    assert quality_gate.gate(amended, recon)["decision"] == "production_blocked"
    unresolved = copy.deepcopy(statement)
    unresolved["unresolved_fields"] = [{"field": "revenue", "reason": "missing"}]
    assert quality_gate.gate(data_quality_engine.score_quality(unresolved), reconciliation_engine.reconcile(unresolved))["decision"] == "review_required"
    low = copy.deepcopy(statement)
    low["rows"][0]["confidence"] = "low"
    assert quality_gate.gate(data_quality_engine.score_quality(low), reconciliation_engine.reconcile(low))["decision"] == "production_blocked"
    missing = copy.deepcopy(statement)
    missing["rows"][0]["source_locator"] = ""
    assert quality_gate.gate(data_quality_engine.score_quality(missing), reconciliation_engine.reconcile(missing))["decision"] == "production_blocked"
    unit = copy.deepcopy(statement)
    unit["rows"][0]["amount_unit"] = ""
    assert quality_gate.gate(data_quality_engine.score_quality(unit), reconciliation_engine.reconcile(unit))["decision"] == "production_blocked"
    print("PASS: data quality tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
