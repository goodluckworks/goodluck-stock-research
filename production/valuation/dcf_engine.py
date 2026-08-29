#!/usr/bin/env python3
"""DCF scenario engine."""

from __future__ import annotations

from typing import Any


def run_dcf(base_fcf: float, assumptions: dict[str, Any], quality_gate: dict[str, Any]) -> dict[str, Any]:
    if quality_gate.get("decision") not in {"usable_internal", "publishable_after_approval"}:
        return {"status": "blocked", "reason": "valuation blocked if data quality insufficient"}
    scenarios: list[dict[str, Any]] = []
    for name in ("bear", "base", "bull"):
        case = assumptions[name]
        discount_rate = float(case["discount_rate"])
        terminal_growth = float(case["terminal_growth"])
        if discount_rate <= terminal_growth:
            raise ValueError("discount_rate must exceed terminal_growth.")
        fcf = base_fcf
        present_value = 0.0
        for year, growth in enumerate(case["growth_rates"], start=1):
            fcf *= 1 + float(growth)
            present_value += fcf / ((1 + discount_rate) ** year)
        terminal_value = fcf * (1 + terminal_growth) / (discount_rate - terminal_growth)
        enterprise_value = present_value + terminal_value / ((1 + discount_rate) ** len(case["growth_rates"]))
        scenarios.append({"case": name, "enterprise_value": enterprise_value, "assumptions": case})
    values = [row["enterprise_value"] for row in scenarios]
    return {
        "status": "available",
        "scenario_output_not_recommendation": True,
        "fair_value_range": {"low": min(values), "high": max(values), "label": "scenario output, not trading instruction"},
        "scenarios": scenarios,
    }
