#!/usr/bin/env python3
"""Audit comparable-company outputs."""

from __future__ import annotations

from typing import Any

from comps_policy import ensure_no_forbidden_output


def audit_comps(output: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    try:
        ensure_no_forbidden_output(str(output))
    except ValueError as exc:
        issues.append(str(exc))
    if output.get("status") == "available":
        for row in output.get("rows", []):
            if row.get("data_status") == "available" and not row.get("market_data_source"):
                issues.append(f"{row.get('ticker')} missing market data source")
    if output.get("status") == "blocked" and "insufficient market data" not in output.get("reason", ""):
        issues.append("blocked comps output missing market-data reason")
    return issues
