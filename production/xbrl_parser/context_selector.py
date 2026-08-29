#!/usr/bin/env python3
"""Context selection helpers for production XBRL parser MVP."""

from __future__ import annotations

from typing import Any


def context_matches(fact: dict[str, Any], expected_period: str) -> bool:
    return fact.get("period") == expected_period and fact.get("entity") and not fact.get("dimensions")
