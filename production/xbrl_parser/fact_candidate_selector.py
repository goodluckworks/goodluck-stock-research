#!/usr/bin/env python3
"""Fact candidate selection without first-match guessing."""

from __future__ import annotations

from typing import Any

from context_selector import context_matches
from unit_normalizer import normalize_value


SUPPORTED_FIELDS = {
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "total_debt",
    "diluted_shares",
}


def select_field(facts: list[dict[str, Any]], field: str, expected_period: str) -> dict[str, Any]:
    candidates = [fact for fact in facts if fact.get("field") == field]
    valid = [fact for fact in candidates if context_matches(fact, expected_period) and fact.get("unit") in {"USD", "shares"}]
    if not candidates:
        return {"field": field, "status": "unresolved", "reason": "missing field"}
    if len(valid) != 1:
        return {"field": field, "status": "unresolved", "reason": "ambiguous, wrong period, wrong unit or dimensional fact", "candidate_count": len(candidates)}
    value, transformations = normalize_value(valid[0])
    return {
        "field": field,
        "status": "parsed",
        "value": value,
        "unit": valid[0].get("unit"),
        "period": valid[0].get("period"),
        "concept_qname": valid[0].get("concept_qname"),
        "source_locator": valid[0].get("source_locator"),
        "confidence": "high",
        "transformations": transformations,
    }
