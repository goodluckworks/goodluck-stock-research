#!/usr/bin/env python3
"""Partial-field policy for fictional normalized CSV sandbox outputs."""

from __future__ import annotations

from typing import Any


FIELD_STATUSES = (
    "approved",
    "adjusted",
    "rejected",
    "unresolved",
    "missing",
    "unsupported",
    "blocked",
    "not_required_for_this_script",
)

BASELINE_FIELDS = {
    "period",
    "currency",
    "amount_unit",
    "per_share_unit",
    "basis",
    "source",
    "source_date",
    "source_status",
    "net_debt_basis",
    "special_items_notes",
}

RATIO_DEPENDENCIES = {
    "gross_margin": ("gross_profit", "revenue"),
    "operating_margin": ("operating_income", "revenue"),
    "raw_net_margin": ("net_income", "revenue"),
    "operating_cash_flow_margin": ("operating_cash_flow", "revenue"),
    "free_cash_flow": ("operating_cash_flow", "capital_expenditure"),
    "fcf_margin": ("operating_cash_flow", "capital_expenditure", "revenue"),
    "raw_roe": ("net_income", "shareholders_equity"),
    "raw_roa": ("net_income", "total_assets"),
    "net_debt": ("total_debt", "cash_and_equivalents"),
    "debt_to_equity": ("total_debt", "shareholders_equity"),
    "current_ratio": ("current_assets", "current_liabilities"),
    "sbc_to_revenue": ("stock_based_compensation", "revenue"),
    "ar_to_revenue": ("accounts_receivable", "revenue"),
    "inventory_to_revenue": ("inventory", "revenue"),
    "diluted_shares_trend": ("shares_diluted",),
}

MINIMUM_RATIO_RUN_FIELDS = {
    "period",
    "currency",
    "amount_unit",
    "per_share_unit",
    "basis",
    "revenue",
    "source",
    "source_date",
    "source_status",
}


def classify_fields(
    financial_columns: list[str],
    promoted: dict[str, dict[str, Any]],
    excluded_records: list[dict[str, Any]],
) -> dict[str, str]:
    """Classify financial columns for partial-field UX."""
    statuses = {field: "missing" for field in financial_columns}
    for field in BASELINE_FIELDS:
        if field in statuses:
            statuses[field] = "not_required_for_this_script"
    for field, record in promoted.items():
        if field in statuses:
            decision = str(record.get("reviewer_decision", ""))
            statuses[field] = "adjusted" if decision == "adjust" else "approved"
    for record in excluded_records:
        field = str(record.get("normalized_field", ""))
        decision = str(record.get("decision", record.get("reviewer_decision", "")))
        if field in statuses:
            if decision == "reject":
                statuses[field] = "rejected"
            elif decision in {"unresolved", "needs_more_evidence"}:
                statuses[field] = "unresolved"
            else:
                statuses[field] = "blocked"
    return statuses


def downstream_impact(field_statuses: dict[str, str]) -> dict[str, Any]:
    """Return available and unavailable ratio impact from field statuses."""
    populated_statuses = {"approved", "adjusted", "not_required_for_this_script"}
    available: list[str] = []
    unavailable: list[dict[str, Any]] = []
    for ratio, fields in RATIO_DEPENDENCIES.items():
        missing = [
            field
            for field in fields
            if field_statuses.get(field, "missing") not in populated_statuses
        ]
        if missing:
            unavailable.append(
                {
                    "ratio": ratio,
                    "missing_inputs": missing,
                    "reason": "missing_or_unresolved_inputs",
                }
            )
        else:
            available.append(ratio)
    missing_minimum = [
        field
        for field in sorted(MINIMUM_RATIO_RUN_FIELDS)
        if field_statuses.get(field, "missing") not in populated_statuses
    ]
    return {
        "minimum_ratio_run_fields": sorted(MINIMUM_RATIO_RUN_FIELDS),
        "ratio_dry_run_allowed": not missing_minimum,
        "missing_minimum_fields": missing_minimum,
        "available_ratios": available,
        "unavailable_ratios": unavailable,
    }


def grouped_fields(field_statuses: dict[str, str]) -> dict[str, list[str]]:
    """Group fields by status."""
    grouped = {status: [] for status in FIELD_STATUSES}
    for field, status in sorted(field_statuses.items()):
        grouped.setdefault(status, []).append(field)
    return grouped
