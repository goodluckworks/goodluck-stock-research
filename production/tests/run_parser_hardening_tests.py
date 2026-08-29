#!/usr/bin/env python3
"""Tests for v2.3 parser hardening."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PARSER = ROOT / "goodluck-stock-research" / "production" / "xbrl_parser"
sys.path.insert(0, str(PARSER))

from parser_hardening import audit_fact, harden_fact_selection  # noqa: E402


def valid_fact(field: str = "revenue") -> dict[str, object]:
    return {
        "issuer_type": "semiconductor",
        "field": field,
        "period_type": "duration" if field in {"revenue", "net_income", "operating_cash_flow", "capital_expenditure"} else "instant",
        "unit": "shares" if field == "diluted_shares" else "USD",
        "context_count": 1,
        "sign": "as_reported",
        "selected_context": "c1",
    }


def main() -> int:
    assert not audit_fact(valid_fact())
    cases = [
        ({"issuer_type": "bank"}, "unsupported issuer type"),
        ({"dimensions": {"Segment": "Cloud"}}, "dimensional fact"),
        ({"context_count": 2, "selected_context": ""}, "multiple contexts"),
        ({"period_type": "instant"}, "duration field"),
        ({"unit": "EUR"}, "unsupported unit"),
        ({"field": "capital_expenditure", "sign": "unknown"}, "capex sign"),
        ({"field": "total_debt", "period_type": "instant", "components_overlap": True}, "debt components"),
        ({"field": "cash_and_equivalents", "period_type": "instant", "includes_restricted_cash": True}, "restricted cash"),
        ({"field": "diluted_shares", "period_type": "instant", "unit": "shares", "share_basis": "basic"}, "basic shares"),
        ({"taxonomy_extension": "CustomRevenue", "extension_mapping_reviewed": False}, "taxonomy extension"),
        ({"amended": True, "amendment_status": ""}, "amendment status"),
    ]
    for patch, expected in cases:
        fact = valid_fact(str(patch.get("field", "revenue")))
        fact.update(patch)
        assert any(expected in issue for issue in audit_fact(fact)), (patch, audit_fact(fact))
    result = harden_fact_selection([valid_fact(), {**valid_fact(), "dimensions": {"Product": "AI"}}])
    assert len(result["accepted"]) == 1
    assert len(result["unresolved"]) == 1
    assert result["first_match_guessing_used"] is False
    print("PASS: parser hardening tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
