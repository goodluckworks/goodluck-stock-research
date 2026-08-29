#!/usr/bin/env python3
"""Tests for production XBRL parser MVP."""

from pathlib import Path
import copy
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser"))

import production_xbrl_parser


def parsed_fields(result):
    return {item["field"]: item for item in result["fields"]}


def main() -> int:
    fixture = ROOT / "goodluck-stock-research" / "production" / "xbrl_parser" / "fixtures" / "standard_10k_package.json"
    package = production_xbrl_parser.load_package(fixture)
    result = production_xbrl_parser.parse_package(package)
    fields = parsed_fields(result)
    assert fields["revenue"]["status"] == "parsed"
    assert fields["capital_expenditure"]["transformations"]
    q = production_xbrl_parser.load_package(ROOT / "goodluck-stock-research" / "production" / "xbrl_parser" / "fixtures" / "standard_10q_package.json")
    q_result = production_xbrl_parser.parse_package(q)
    assert parsed_fields(q_result)["revenue"]["status"] == "parsed"
    wrong_period = copy.deepcopy(package)
    wrong_period["facts"][0]["period"] = "FY2025"
    assert parsed_fields(production_xbrl_parser.parse_package(wrong_period))["revenue"]["status"] == "unresolved"
    wrong_unit = copy.deepcopy(package)
    wrong_unit["facts"][0]["unit"] = "EUR"
    assert parsed_fields(production_xbrl_parser.parse_package(wrong_unit))["revenue"]["status"] == "unresolved"
    dimensional = copy.deepcopy(package)
    dimensional["facts"][0]["dimensions"] = ["SegmentAxis"]
    assert parsed_fields(production_xbrl_parser.parse_package(dimensional))["revenue"]["status"] == "unresolved"
    multiple = copy.deepcopy(package)
    multiple["facts"].append(copy.deepcopy(multiple["facts"][0]))
    assert parsed_fields(production_xbrl_parser.parse_package(multiple))["revenue"]["status"] == "unresolved"
    missing = copy.deepcopy(package)
    missing["facts"] = [fact for fact in missing["facts"] if fact["field"] != "gross_profit"]
    assert parsed_fields(production_xbrl_parser.parse_package(missing))["gross_profit"]["status"] == "unresolved"
    bank = copy.deepcopy(package)
    bank["issuer_type"] = "bank"
    try:
        production_xbrl_parser.parse_package(bank)
        raise AssertionError("unsupported issuer accepted")
    except ValueError:
        pass
    assert result["no_investment_conclusion"] is True
    print("PASS: production XBRL parser tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
