#!/usr/bin/env python3
"""Valuation output auditor."""

from __future__ import annotations

from typing import Any


FORBIDDEN = ("buy now", "sell now", "position size", "guaranteed return", "execute trade")


def audit_valuation(output: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    text = str(output).lower()
    for term in FORBIDDEN:
        if term in text:
            issues.append(f"forbidden valuation output: {term}")
    if output.get("status") == "available" and "assumptions" not in text:
        issues.append("valuation assumptions not explicit")
    if "scenario output" not in text and output.get("status") == "available":
        issues.append("valuation range missing scenario label")
    return issues
