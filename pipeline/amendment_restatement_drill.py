#!/usr/bin/env python3
"""Amendment and restatement drill policy."""

from __future__ import annotations

from typing import Any


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    """Evaluate amendment/restatement flags."""
    warnings: list[str] = []
    blockers: list[str] = []
    if payload.get("amendment_present") is True:
        warnings.append("amendment_present: do not claim latest-effective without reviewer decision")
    if payload.get("restatement_conflict") is True:
        blockers.append("restatement_conflict: production readiness blocked")
    if payload.get("claims_latest_effective") is True and payload.get("latest_effective_established") is not True:
        blockers.append("latest_effective_not_established")
    return {
        "status": "blocked" if blockers else "warning" if warnings else "pass",
        "warnings": warnings,
        "blockers": blockers,
        "production_ready": False,
    }
