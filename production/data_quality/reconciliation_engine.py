#!/usr/bin/env python3
"""Reconciliation checks for normalized statements."""

from __future__ import annotations

from typing import Any


def reconcile(statement: dict[str, Any]) -> dict[str, Any]:
    rows = statement.get("rows", [])
    missing_links = [row.get("field", "unknown") for row in rows if not row.get("source_locator") or not row.get("concept_qname")]
    return {
        "reconciliation_schema_version": "v1.5.0",
        "status": "fail" if missing_links else "pass",
        "missing_links": missing_links,
    }
