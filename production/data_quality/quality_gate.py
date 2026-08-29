#!/usr/bin/env python3
"""Quality gate decisions."""

from __future__ import annotations

from typing import Any


def gate(quality: dict[str, Any], reconciliation: dict[str, Any]) -> dict[str, Any]:
    if reconciliation.get("status") != "pass":
        return {"decision": "production_blocked", "reason": "reconciliation failed"}
    status = quality.get("status")
    if status == "usable_internal":
        return {"decision": "usable_internal", "reason": "quality usable for internal research"}
    if status == "review_required":
        return {"decision": "review_required", "reason": "unresolved fields require review"}
    return {"decision": "production_blocked", "reason": "; ".join(quality.get("issues", []))}
