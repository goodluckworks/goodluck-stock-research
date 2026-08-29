#!/usr/bin/env python3
"""Build historical normalized statement table."""

from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = ("revenue", "net_income", "operating_cash_flow")


def build_historical_statement(history: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    missing: list[str] = list(history.get("missing_periods", []))
    for filing in history.get("selected_filings", []):
        statement = filing.get("statement", {})
        row = {
            "fiscal_period": filing["fiscal_period"],
            "period_end": filing["period_end"],
            "accession": filing["accession"],
            "source_url": filing["source_url"],
        }
        for field in REQUIRED_FIELDS:
            if field not in statement:
                missing.append(f"{filing['fiscal_period']} missing {field}")
                row[field] = None
            else:
                row[field] = statement[field]
        rows.append(row)
    return {
        "statement_schema_version": "v2.2.0",
        "period_type": history["period_type"],
        "rows": rows,
        "missing_periods_or_fields": missing,
        "zero_fill_used": False,
    }
