#!/usr/bin/env python3
"""Build user-provided peer sets."""

from __future__ import annotations

from typing import Any

from comps_policy import validate_peer


def build_peer_set(target_ticker: str, peers: list[dict[str, Any]]) -> dict[str, Any]:
    if not peers:
        raise ValueError("User-provided peers are required.")
    for peer in peers:
        validate_peer(peer)
    return {
        "peer_set_schema_version": "v2.4.0",
        "target_ticker": target_ticker,
        "peers": peers,
        "auto_peer_selection_used": False,
        "caveat": "Peer quality depends on user-provided comparability classification.",
    }
