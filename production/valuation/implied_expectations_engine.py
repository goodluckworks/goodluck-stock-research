#!/usr/bin/env python3
"""Market-implied expectations engine."""

from __future__ import annotations

from typing import Any


def implied_scale_up(current_multiple: float, mature_multiple: float, years: int) -> dict[str, Any]:
    if current_multiple <= 0 or mature_multiple <= 0 or years <= 0:
        raise ValueError("Multiples and years must be positive.")
    required_scale = current_multiple / mature_multiple
    required_cagr = required_scale ** (1 / years) - 1
    return {
        "required_scale_up": required_scale,
        "required_cagr": required_cagr,
        "interpretation": "reverse-engineered market-implied expectation, not forecast",
    }


def build_implied_expectations(inputs: dict[str, Any]) -> dict[str, Any]:
    return {
        "ev_sales": implied_scale_up(float(inputs["ev_sales_current"]), float(inputs["target_ev_sales_mature"]), int(inputs["years_to_maturity"])),
        "pe": implied_scale_up(float(inputs["pe_current"]), float(inputs["target_pe_mature"]), int(inputs["years_to_maturity"])),
        "p_fcf": implied_scale_up(float(inputs["p_fcf_current"]), float(inputs["target_p_fcf_mature"]), int(inputs["years_to_maturity"])),
        "no_deterministic_target_price": True,
    }
