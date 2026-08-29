#!/usr/bin/env python3
"""Source quality audit."""

from __future__ import annotations

from typing import Any


def audit_source_quality(manifest: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if manifest.get("issuer_type") in {"bank", "insurer", "fund", "foreign_issuer"}:
        issues.append("unsupported issuer type")
    if manifest.get("market_data_status") == "unavailable":
        issues.append("market data unavailable")
    if not manifest.get("source_url"):
        issues.append("missing source URL")
    return issues
