#!/usr/bin/env python3
"""Normalization policy for production financial statements."""

from __future__ import annotations


INCOME_FIELDS = {"revenue", "gross_profit", "operating_income", "net_income", "diluted_shares"}
BALANCE_FIELDS = {"cash_and_equivalents", "total_debt"}
CASH_FLOW_FIELDS = {"operating_cash_flow", "capital_expenditure"}


def statement_for(field: str) -> str:
    if field in INCOME_FIELDS:
        return "income_statement"
    if field in BALANCE_FIELDS:
        return "balance_sheet"
    if field in CASH_FLOW_FIELDS:
        return "cash_flow"
    return "unknown"
