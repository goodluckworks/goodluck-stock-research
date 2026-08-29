#!/usr/bin/env python3
"""Tests for market multiples."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
COMPS = ROOT / "goodluck-stock-research" / "production" / "comps"
sys.path.insert(0, str(COMPS))

from market_multiples import compute_multiples  # noqa: E402
from peer_set_builder import build_peer_set  # noqa: E402


def main() -> int:
    peer_set = build_peer_set("NVDA", [
        {"ticker": "AMD", "company": "AMD", "peer_group": "core", "comparability_status": "core", "source": "user"},
        {"ticker": "AVGO", "company": "Broadcom", "peer_group": "adjacent", "comparability_status": "reference", "source": "user"},
    ])
    blocked = compute_multiples(peer_set, [])
    assert blocked["status"] == "blocked"
    output = compute_multiples(peer_set, [
        {"ticker": "AMD", "ev_sales": "8", "ev_ebitda": "25", "pe": "30", "p_fcf": "28", "source": "indicative", "timestamp": "2026-07-07"},
        {"ticker": "AVGO", "ev_sales": "-1", "ev_ebitda": "20", "pe": "25", "p_fcf": "24", "source": "indicative", "timestamp": "2026-07-07"},
    ])
    assert output["core_stats"]["ev_sales"]["median"] == 8.0
    assert output["rows"][1]["ev_sales"] is None
    print("PASS: market multiples tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
