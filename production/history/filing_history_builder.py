#!/usr/bin/env python3
"""Build filing history from identity manifests."""

from __future__ import annotations

from typing import Any

from period_aligner import select_history


def build_filing_history(filings: list[dict[str, Any]], period_type: str) -> dict[str, Any]:
    effective = [item for item in filings if item.get("superseded_by") in {None, ""}]
    superseded = [item for item in filings if item.get("superseded_by") not in {None, ""}]
    selected, missing = select_history(effective, period_type)
    return {
        "history_schema_version": "v2.2.0",
        "period_type": period_type,
        "selected_filings": selected,
        "superseded_filings": superseded,
        "missing_periods": missing,
        "all_periods_trace_to_accession": all(bool(item.get("accession")) and bool(item.get("source_url")) for item in selected),
    }
