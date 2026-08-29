#!/usr/bin/env python3
"""Hardening checks for production XBRL parser inputs."""

from __future__ import annotations

from typing import Any


SUPPORTED_ISSUER_TYPES = {"industrial", "technology", "retail", "semiconductor"}


def audit_fact(fact: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if fact.get("issuer_type") not in SUPPORTED_ISSUER_TYPES:
        issues.append("unsupported issuer type")
    if fact.get("dimensions"):
        issues.append("dimensional fact requires explicit mapping")
    if fact.get("context_count", 1) > 1 and not fact.get("selected_context"):
        issues.append("multiple contexts unresolved")
    if fact.get("period_type") not in {"duration", "instant"}:
        issues.append("invalid period type")
    if fact.get("field") in {"revenue", "net_income", "operating_cash_flow"} and fact.get("period_type") != "duration":
        issues.append("duration field has non-duration context")
    if fact.get("field") in {"cash_and_equivalents", "total_debt", "diluted_shares"} and fact.get("period_type") != "instant":
        issues.append("instant field has non-instant context")
    if fact.get("unit") not in {"USD", "shares"}:
        issues.append("unsupported unit")
    if fact.get("field") == "capital_expenditure" and fact.get("sign") not in {"as_reported", "cash_outflow_positive", "cash_outflow_negative"}:
        issues.append("capex sign unresolved")
    if fact.get("field") == "total_debt" and fact.get("components_overlap") is True:
        issues.append("debt components overlap")
    if fact.get("field") == "cash_and_equivalents" and fact.get("includes_restricted_cash") is True:
        issues.append("cash includes restricted cash")
    if fact.get("field") == "diluted_shares" and fact.get("share_basis") == "basic":
        issues.append("basic shares cannot fill diluted shares")
    if fact.get("taxonomy_extension") and not fact.get("extension_mapping_reviewed"):
        issues.append("taxonomy extension requires reviewed mapping")
    if fact.get("amended") is True and not fact.get("amendment_status"):
        issues.append("amendment status missing")
    return issues


def harden_fact_selection(facts: list[dict[str, Any]]) -> dict[str, Any]:
    accepted: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for fact in facts:
        issues = audit_fact(fact)
        if issues:
            unresolved.append({"fact": fact, "issues": issues})
        else:
            accepted.append(fact)
    return {
        "hardening_schema_version": "v2.3.0",
        "accepted": accepted,
        "unresolved": unresolved,
        "first_match_guessing_used": False,
    }
