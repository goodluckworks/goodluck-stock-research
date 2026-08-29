#!/usr/bin/env python3
"""Tests for approval gate."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "approval_gate"))

import approval_gate
import publication_manifest


def main() -> int:
    quality = {"decision": "usable_internal"}
    assert approval_gate.evaluate_approval(quality, [], [], None)["state"] == "review_required"
    assert approval_gate.evaluate_approval({"decision": "production_blocked"}, [], [], {"approved": True})["state"] == "blocked"
    assert approval_gate.evaluate_approval(quality, ["bad"], [], {"approved": True})["state"] == "blocked"
    approved = approval_gate.evaluate_approval(quality, [], [], {"approved": True, "reviewer": "human"})
    assert approved["state"] == "publishable_research_packet"
    manifest = publication_manifest.build_manifest("MRVL", approved)
    assert manifest["not_trading_instruction"] is True
    assert manifest["no_position_sizing"] is True
    print("PASS: approval gate tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
