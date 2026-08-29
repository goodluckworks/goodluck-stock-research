#!/usr/bin/env python3
"""Research conclusion policy."""

from __future__ import annotations


ALLOWED_LABELS = {"constructive", "neutral", "cautious", "negative", "insufficient_evidence"}
FORBIDDEN_TERMS = ("buy now", "sell now", "hold", "position size", "trade instruction", "use margin")


def forbidden_hits(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in FORBIDDEN_TERMS if term in lowered]
