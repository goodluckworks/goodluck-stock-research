#!/usr/bin/env python3
"""Policy helpers for controlled real-company quarantine sandbox."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_ALLOWLIST = {"MRVL", "NVDA", "AVGO"}
QUARANTINE_FLAGS = {
    "quarantined": True,
    "not_production_data": True,
    "not_investment_data": True,
    "not_company_fact_until_verified": True,
    "manual_review_required": True,
    "not_for_trading": True,
    "not_for_public_release": True,
    "no_recommendation": True,
}


def load_policy(path: Path) -> dict[str, Any]:
    """Load approval policy JSON."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Approval policy root must be object: {path}")
    return value


def allowed_tickers(policy: dict[str, Any]) -> set[str]:
    """Return effective allowlist."""
    raw = policy.get("allowlist", sorted(DEFAULT_ALLOWLIST))
    if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
        raise ValueError("approval policy allowlist must be a list of tickers.")
    return {item.upper() for item in raw}


def validate_policy(policy: dict[str, Any], ticker: str, output_dir: Path) -> None:
    """Validate quarantine approval policy."""
    ticker = ticker.upper()
    if policy.get("policy_schema_version") != "v0.6.0":
        raise ValueError("approval policy must use policy_schema_version v0.6.0.")
    if ticker not in allowed_tickers(policy):
        raise ValueError(f"{ticker} is not allowlisted for controlled sandbox.")
    if policy.get("sandbox_enabled") is not True:
        raise ValueError("approval policy must set sandbox_enabled=true.")
    if policy.get("approval_scope") != "quarantine_only":
        raise ValueError("approval policy approval_scope must be quarantine_only.")
    if policy.get("not_public_release") is not True:
        raise ValueError("approval policy must set not_public_release=true.")
    if policy.get("mapping_review_status") != "approved":
        raise ValueError("mapping review must be approved.")
    if policy.get("mapping_lifecycle_status") == "superseded":
        raise ValueError("superseded mapping is not allowed.")
    if policy.get("minimum_confidence") not in {"medium", "high"}:
        raise ValueError("minimum_confidence must be medium or high.")
    expected_output = str(policy.get("quarantine_output_dir", ""))
    if expected_output and output_dir.as_posix().endswith(expected_output) is False:
        raise ValueError("output_dir does not match approval policy quarantine_output_dir.")


def require_quarantine_flags(flags: dict[str, Any]) -> None:
    """Validate required quarantine flags."""
    for key, expected in QUARANTINE_FLAGS.items():
        if flags.get(key) is not expected:
            raise ValueError(f"Missing quarantine flag {key}={expected}.")
