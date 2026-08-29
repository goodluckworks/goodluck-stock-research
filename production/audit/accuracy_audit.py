#!/usr/bin/env python3
"""Accuracy audit for production research outputs."""

from __future__ import annotations

from typing import Any


def audit_accuracy(statement: dict[str, Any], source_values: dict[str, float]) -> list[str]:
    issues: list[str] = []
    for row in statement.get("rows", []):
        field = row.get("field")
        if field in source_values and float(row.get("value", 0)) != float(source_values[field]):
            issues.append(f"wrong financial value detected: {field}")
        if not row.get("source"):
            issues.append(f"missing source: {field}")
    return issues
