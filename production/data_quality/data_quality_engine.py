#!/usr/bin/env python3
"""Production data quality scoring."""

from __future__ import annotations

from typing import Any


DIMENSIONS = (
    "source_quality",
    "filing_identity_confidence",
    "amendment_restatement_status",
    "parser_confidence",
    "field_completeness",
    "reconciliation_status",
    "unit_sign_consistency",
    "period_consistency",
    "unresolved_severity",
    "downstream_usability",
)


def score_quality(statement: dict[str, Any], amendment: dict[str, Any] | None = None) -> dict[str, Any]:
    rows = statement.get("rows", [])
    unresolved = statement.get("unresolved_fields", [])
    issues: list[str] = []
    if amendment and amendment.get("restatement_found"):
        issues.append("restatement conflict")
    if any(not row.get("source_locator") for row in rows):
        issues.append("missing provenance")
    if any(row.get("confidence") == "low" for row in rows):
        issues.append("low parser confidence")
    if any(not row.get("amount_unit") for row in rows):
        issues.append("unit mismatch")
    if unresolved:
        issues.append("unresolved fields")
    if "restatement conflict" in issues or "missing provenance" in issues or "low parser confidence" in issues or "unit mismatch" in issues:
        status = "production_blocked"
    elif unresolved:
        status = "review_required"
    else:
        status = "usable_internal"
    return {
        "quality_schema_version": "v1.5.0",
        "status": status,
        "issues": issues,
        "dimensions": {dimension: "checked" for dimension in DIMENSIONS},
        "score": 90 if status == "usable_internal" else 60 if status == "review_required" else 20,
    }
