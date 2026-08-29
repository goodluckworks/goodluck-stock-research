#!/usr/bin/env python3
"""Calculation guardrails for quarantined real-company sandbox."""

from __future__ import annotations

ALLOWED = {"ratio"}
BLOCKED = {"dcf", "peer_comps", "implied_expectations", "target_price", "recommendation", "position_size", "research_status"}


def evaluate_calculation(tool: str, *, quarantined_csv_exists: bool, quarantined: bool) -> dict[str, str]:
    """Return allow/block decision for a quarantined calculation."""
    normalized = tool.strip().lower()
    if normalized in ALLOWED and quarantined and quarantined_csv_exists:
        return {"decision": "allow", "reason": "ratio-only quarantined dry-run with no-investment banner required"}
    if normalized in ALLOWED:
        return {"decision": "block", "reason": "ratio requires quarantined CSV and quarantine flags"}
    if normalized in BLOCKED:
        return {"decision": "block", "reason": f"{normalized} is not allowed for real-company quarantine sandbox"}
    return {"decision": "block", "reason": "unknown calculation tool"}
