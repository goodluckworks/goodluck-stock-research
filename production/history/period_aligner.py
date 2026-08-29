#!/usr/bin/env python3
"""Fiscal period alignment helpers."""

from __future__ import annotations

from typing import Any


def align_periods(filings: list[dict[str, Any]], period_type: str) -> list[dict[str, Any]]:
    if period_type not in {"annual", "quarterly"}:
        raise ValueError("period_type must be annual or quarterly.")
    aligned: list[dict[str, Any]] = []
    seen: set[str] = set()
    for filing in sorted(filings, key=lambda item: item["period_end"]):
        if filing.get("period_type") != period_type:
            raise ValueError("mismatched fiscal period blocked")
        key = str(filing.get("fiscal_period"))
        if key in seen:
            raise ValueError("duplicate fiscal period blocked")
        seen.add(key)
        aligned.append(filing)
    return aligned


def select_history(filings: list[dict[str, Any]], period_type: str) -> tuple[list[dict[str, Any]], list[str]]:
    aligned = align_periods(filings, period_type)
    limit = 3 if period_type == "annual" else 8
    selected = aligned[-limit:]
    missing: list[str] = []
    if len(selected) < limit:
        missing.append(f"Only {len(selected)} {period_type} periods available; expected up to {limit}.")
    return selected, missing
