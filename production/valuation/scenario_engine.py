#!/usr/bin/env python3
"""Scenario valuation engine."""

from __future__ import annotations

from typing import Any


def run_scenarios(revenue: float, assumptions: dict[str, dict[str, float]]) -> list[dict[str, Any]]:
    scenarios = []
    for name, values in assumptions.items():
        enterprise_value = revenue * values["revenue_multiple"]
        fcf = revenue * values["fcf_margin"]
        scenarios.append(
            {
                "case": name,
                "revenue": revenue,
                "revenue_multiple": values["revenue_multiple"],
                "fcf_margin": values["fcf_margin"],
                "enterprise_value": enterprise_value,
                "fcf": fcf,
            }
        )
    return scenarios
