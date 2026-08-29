#!/usr/bin/env python3
"""Audit research conclusions."""

from __future__ import annotations

from typing import Any

from conclusion_policy import ALLOWED_LABELS, forbidden_hits


def audit(conclusion: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if conclusion.get("conclusion_label") not in ALLOWED_LABELS:
        issues.append("invalid conclusion label")
    for field in ("confidence", "evidence_basis", "data_quality_caveats", "key_downside_risks", "missing_evidence"):
        if field not in conclusion:
            issues.append(f"missing {field}")
    hits = forbidden_hits(str(conclusion))
    if hits:
        issues.append("forbidden terms: " + ", ".join(hits))
    if conclusion.get("not_trade_instruction") is not True:
        issues.append("missing not_trade_instruction")
    return issues
