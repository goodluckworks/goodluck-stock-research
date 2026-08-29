#!/usr/bin/env python3
"""Policy for review-gated report packets."""

from __future__ import annotations


FORBIDDEN_TERMS = (
    "target price:",
    "buy:",
    "sell:",
    "hold:",
    "recommendation:",
    "position size:",
    "research status:",
    "portfolio action:",
)


def forbidden_hits(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in FORBIDDEN_TERMS if term in lowered]


def packet_type_for(ticker: str) -> str:
    if ticker.upper() == "EXMP":
        return "fictional_full_report_packet"
    if ticker.upper() == "MRVL":
        return "real_company_quarantine_report_packet"
    return "real_company_review_only_packet"
