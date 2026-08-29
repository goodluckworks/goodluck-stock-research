#!/usr/bin/env python3
"""Production red-team checks."""

from __future__ import annotations

from typing import Any


def red_team_payload(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    text = str(payload).lower()
    if payload.get("parser_guessed_value") is True:
        issues.append("parser guesses values")
    if payload.get("missing_provenance") is True:
        issues.append("missing provenance")
    if payload.get("low_quality_used") is True:
        issues.append("low quality data used")
    if payload.get("conclusion_without_evidence") is True:
        issues.append("conclusion without evidence")
    if payload.get("valuation_without_assumptions") is True:
        issues.append("valuation without assumptions")
    if payload.get("approval_gate_bypassed") is True:
        issues.append("approval gate bypass")
    if payload.get("live_without_user_agent") is True:
        issues.append("live ingestion without User-Agent")
    if payload.get("non_sec_url") is True:
        issues.append("non-SEC URL")
    for forbidden in ("trade instruction", "position size", "buy now", "sell now", "broker.connect", "place_order", "execute_trade", "api_key =", "password =", "secret ="):
        if forbidden in text:
            issues.append(forbidden)
    return issues
