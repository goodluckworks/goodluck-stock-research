#!/usr/bin/env python3
"""Report usability audit."""

from __future__ import annotations


REQUIRED_REPORT_TERMS = (
    "production research report draft",
    "research view:",
    "confidence:",
    "caveats",
    "not personalized advice",
    "not a trade instruction",
    "not position sizing",
)


def audit_report_usability(text: str) -> list[str]:
    lowered = text.lower()
    issues = [f"missing report term: {term}" for term in REQUIRED_REPORT_TERMS if term not in lowered]
    for forbidden in ("buy now", "sell now", "hold this", "position size:", "execute trade", "guaranteed upside"):
        if forbidden in lowered:
            issues.append(f"forbidden report term: {forbidden}")
    return issues
