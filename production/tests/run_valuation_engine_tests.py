#!/usr/bin/env python3
"""Tests for valuation and scenario engine."""

from pathlib import Path
import copy
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser"))
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "normalization"))
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "data_quality"))
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "valuation"))

import production_xbrl_parser
import financial_statement_builder
import data_quality_engine
import reconciliation_engine
import quality_gate
import valuation_engine


def base_statement():
    package = production_xbrl_parser.load_package(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser" / "fixtures" / "standard_10k_package.json")
    return financial_statement_builder.build(production_xbrl_parser.parse_package(package))


def main() -> int:
    statement = base_statement()
    gate = quality_gate.gate(data_quality_engine.score_quality(statement), reconciliation_engine.reconcile(statement))
    valuation = valuation_engine.value_company(statement, gate)
    assert valuation["scenarios"]
    assert valuation["assumptions"]
    assert valuation["sensitivity"]
    assert valuation["fair_value_range"]["label"] == "scenario output, not recommendation"
    assert valuation["confidence"] in {"high", "medium", "low"}
    assert not valuation_engine.audit_valuation_output(valuation)
    no_revenue = copy.deepcopy(statement)
    no_revenue["rows"] = [row for row in no_revenue["rows"] if row["field"] != "revenue"]
    try:
        valuation_engine.value_company(no_revenue, gate)
        raise AssertionError("missing revenue accepted")
    except ValueError:
        pass
    try:
        valuation_engine.value_company(statement, {"decision": "production_blocked"})
        raise AssertionError("quality failure accepted")
    except ValueError:
        pass
    print("PASS: valuation engine tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
