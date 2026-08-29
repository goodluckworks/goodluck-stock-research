#!/usr/bin/env python3
"""Tests for peer set builder."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
COMPS = ROOT / "goodluck-stock-research" / "production" / "comps"
sys.path.insert(0, str(COMPS))

from peer_set_builder import build_peer_set  # noqa: E402


def main() -> int:
    peers = [{"ticker": "AMD", "company": "AMD", "peer_group": "core_ai_accelerator", "comparability_status": "core", "source": "user"}]
    result = build_peer_set("NVDA", peers)
    assert result["auto_peer_selection_used"] is False
    try:
        build_peer_set("NVDA", [{"ticker": "AMD"}])
        raise AssertionError("missing peer fields should fail")
    except ValueError:
        pass
    print("PASS: peer set tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
