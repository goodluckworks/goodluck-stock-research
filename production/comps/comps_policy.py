#!/usr/bin/env python3
"""Comparable company policy."""

from __future__ import annotations

from typing import Any


FORBIDDEN_OUTPUTS = ("buy now", "sell now", "position size", "trade instruction")


def validate_peer(peer: dict[str, Any]) -> None:
    required = {"ticker", "company", "peer_group", "comparability_status", "source"}
    missing = required - set(peer)
    if missing:
        raise ValueError(f"Peer missing fields: {sorted(missing)}")
    if peer.get("comparability_status") not in {"core", "adjacent", "reference", "weak", "exclude"}:
        raise ValueError("Invalid comparability_status.")


def ensure_no_forbidden_output(text: str) -> None:
    lowered = text.lower()
    for term in FORBIDDEN_OUTPUTS:
        if term in lowered:
            raise ValueError(f"Forbidden comps output: {term}")
