#!/usr/bin/env python3
"""Sensitivity table generation."""

from __future__ import annotations


def build_sensitivity(base_value: float, variables: dict[str, list[float]]) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for variable, changes in variables.items():
        for change in changes:
            rows.append({"variable": variable, "change": change, "scenario_value": base_value * (1 + change)})
    return rows
