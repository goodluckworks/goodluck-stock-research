#!/usr/bin/env python3
"""Unit normalization helpers."""

from __future__ import annotations

from typing import Any


def normalize_value(fact: dict[str, Any]) -> tuple[float, list[str]]:
    value = float(fact["value"])
    transformations: list[str] = []
    if fact.get("field") == "capital_expenditure" and value > 0:
        transformations.append("capex sign recorded: positive outflow input retained")
    return value, transformations
