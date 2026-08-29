#!/usr/bin/env python3
"""Market multiples calculation."""

from __future__ import annotations

from statistics import median
from typing import Any


MULTIPLE_FIELDS = ("ev_sales", "ev_ebitda", "pe", "p_fcf")


def positive(value: Any) -> float | None:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return numeric if numeric > 0 else None


def compute_multiples(peer_set: dict[str, Any], market_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not market_rows:
        return {"status": "blocked", "reason": "insufficient market data blocks comps conclusion"}
    by_ticker = {row["ticker"]: row for row in market_rows}
    rows: list[dict[str, Any]] = []
    for peer in peer_set["peers"]:
        market = by_ticker.get(peer["ticker"])
        if not market:
            rows.append({**peer, "data_status": "missing_market_data"})
            continue
        row = {**peer, "data_status": "available", "market_data_source": market.get("source"), "market_data_timestamp": market.get("timestamp")}
        for field in MULTIPLE_FIELDS:
            row[field] = positive(market.get(field))
        rows.append(row)
    stats: dict[str, Any] = {}
    for field in MULTIPLE_FIELDS:
        values = [row[field] for row in rows if row.get("comparability_status") == "core" and row.get(field) is not None]
        stats[field] = {"median": median(values) if values else None, "count": len(values)}
    return {
        "multiples_schema_version": "v2.4.0",
        "status": "available",
        "rows": rows,
        "core_stats": stats,
        "market_data_dependent": True,
        "caveat": "Blended and core medians are reference points, not valuation instructions.",
    }
