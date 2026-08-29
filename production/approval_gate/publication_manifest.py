#!/usr/bin/env python3
"""Publication manifest helper."""

from __future__ import annotations

from typing import Any


def build_manifest(ticker: str, approval: dict[str, str]) -> dict[str, Any]:
    return {
        "publication_manifest_schema_version": "v1.8.0",
        "ticker": ticker,
        "publication_state": approval["state"],
        "reason": approval["reason"],
        "not_personalized_advice": True,
        "not_trading_instruction": True,
        "no_position_sizing": True,
    }
