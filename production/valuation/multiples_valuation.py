#!/usr/bin/env python3
"""Multiples valuation helpers."""

from __future__ import annotations

from typing import Any


def value_from_multiples(metric_value: float, multiple_range: dict[str, float], metric_name: str) -> dict[str, Any]:
    if metric_value <= 0:
        return {"status": "blocked", "reason": f"{metric_name} unavailable or non-positive"}
    low = metric_value * float(multiple_range["low"])
    high = metric_value * float(multiple_range["high"])
    return {
        "status": "available",
        "metric": metric_name,
        "range": {"low": low, "high": high, "label": "scenario output, not recommendation"},
        "assumptions": multiple_range,
    }
