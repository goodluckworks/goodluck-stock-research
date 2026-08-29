#!/usr/bin/env python3
"""Valuation and scenario analysis engine."""

from __future__ import annotations

from typing import Any

from assumption_registry import get_assumptions
from scenario_engine import run_scenarios


FORBIDDEN = ("buy", "sell", "hold", "position size", "portfolio action")


def extract_revenue(statement: dict[str, Any]) -> float:
    for row in statement.get("rows", []):
        if row.get("field") == "revenue":
            return float(row["value"])
    raise ValueError("missing critical data: revenue")


def value_company(statement: dict[str, Any], quality_gate: dict[str, Any]) -> dict[str, Any]:
    if quality_gate.get("decision") not in {"usable_internal", "publishable_after_approval"}:
        raise ValueError("quality gate blocks valuation")
    revenue = extract_revenue(statement)
    assumptions = get_assumptions()
    scenarios = run_scenarios(revenue, assumptions)
    values = [item["enterprise_value"] for item in scenarios]
    return {
        "valuation_schema_version": "v1.6.0",
        "scenario_output_not_recommendation": True,
        "assumptions": assumptions,
        "scenarios": scenarios,
        "fair_value_range": {"low": min(values), "high": max(values), "label": "scenario output, not recommendation"},
        "sensitivity": [{"revenue_change": change, "base_ev": revenue * (1 + change) * assumptions["base"]["revenue_multiple"]} for change in (-0.1, 0.0, 0.1)],
        "confidence": "medium",
    }


def audit_valuation_output(output: dict[str, Any]) -> list[str]:
    text = str(output).lower()
    return [term for term in FORBIDDEN if term in text and "not recommendation" not in text]
