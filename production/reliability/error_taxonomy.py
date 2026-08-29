#!/usr/bin/env python3
"""Production error taxonomy."""

from __future__ import annotations


ERROR_CLASSES = {
    "source_unavailable": "Source unavailable or timed out.",
    "data_quality_blocked": "Data quality gate blocked output.",
    "parser_unresolved": "Parser could not resolve required fields.",
    "market_data_missing": "Market data unavailable.",
    "approval_required": "Human approval required.",
}


def classify_error(code: str) -> dict[str, str]:
    return {"code": code, "description": ERROR_CLASSES.get(code, "Unknown error"), "silent_failure_allowed": "false"}
