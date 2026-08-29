#!/usr/bin/env python3
"""Historical metrics for normalized statements."""

from __future__ import annotations

from typing import Any


def growth(current: float | None, previous: float | None) -> float | None:
    if current is None or previous in {None, 0}:
        return None
    return (current - previous) / previous


def compute_historical_metrics(statement: dict[str, Any]) -> dict[str, Any]:
    rows = statement.get("rows", [])
    metrics: list[dict[str, Any]] = []
    previous: dict[str, Any] | None = None
    for row in rows:
        item = {
            "fiscal_period": row["fiscal_period"],
            "revenue_growth": growth(row.get("revenue"), previous.get("revenue") if previous else None),
            "net_margin": None if row.get("revenue") in {None, 0} or row.get("net_income") is None else row["net_income"] / row["revenue"],
            "ocf_margin": None if row.get("revenue") in {None, 0} or row.get("operating_cash_flow") is None else row["operating_cash_flow"] / row["revenue"],
        }
        metrics.append(item)
        previous = row
    return {"metrics_schema_version": "v2.2.0", "metrics": metrics, "annualization_used": False}
