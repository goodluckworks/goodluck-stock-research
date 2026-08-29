#!/usr/bin/env python3
"""Human approval gate for production report packets."""

from __future__ import annotations

from typing import Any


def evaluate_approval(quality_gate: dict[str, Any], conclusion_issues: list[str], report_issues: list[str], human_approval: dict[str, Any] | None) -> dict[str, str]:
    if quality_gate.get("decision") not in {"usable_internal", "publishable_after_approval"}:
        return {"state": "blocked", "reason": "quality gate failed"}
    if conclusion_issues:
        return {"state": "blocked", "reason": "conclusion audit failed"}
    if report_issues:
        return {"state": "blocked", "reason": "report audit failed"}
    if not human_approval:
        return {"state": "review_required", "reason": "missing human approval"}
    if human_approval.get("approved") is True:
        return {"state": "publishable_research_packet", "reason": "human approval record present"}
    return {"state": "reviewed_internal", "reason": "reviewed but not approved for publication"}
