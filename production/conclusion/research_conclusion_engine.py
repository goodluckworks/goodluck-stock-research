#!/usr/bin/env python3
"""Evidence-backed research conclusion engine."""

from __future__ import annotations

from typing import Any

from conclusion_policy import ALLOWED_LABELS


def generate_conclusion(quality: dict[str, Any], valuation: dict[str, Any] | None, evidence_basis: list[str]) -> dict[str, Any]:
    if quality.get("status") == "production_blocked" or quality.get("score", 0) < 50:
        label = "insufficient_evidence"
    elif valuation is None:
        label = "insufficient_evidence"
    elif quality.get("status") == "review_required":
        label = "cautious"
    else:
        label = "constructive"
    assert label in ALLOWED_LABELS
    return {
        "conclusion_schema_version": "v1.7.0",
        "conclusion_label": label,
        "confidence": "medium" if label != "insufficient_evidence" else "low",
        "evidence_basis": evidence_basis,
        "valuation_basis": valuation.get("fair_value_range") if valuation else None,
        "data_quality_caveats": quality.get("issues", []),
        "key_upside_factors": ["scenario revenue growth", "margin expansion"] if label == "constructive" else [],
        "key_downside_risks": ["data quality caveats", "valuation sensitivity"],
        "missing_evidence": [] if label != "insufficient_evidence" else ["valuation or data quality support"],
        "not_personalized_advice": True,
        "not_trade_instruction": True,
    }
