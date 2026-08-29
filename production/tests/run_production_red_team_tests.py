#!/usr/bin/env python3
"""Tests for production red-team audit."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "audit"))

import production_red_team


def main() -> int:
    cases = [
        {"parser_guessed_value": True},
        {"missing_provenance": True},
        {"low_quality_used": True},
        {"conclusion_without_evidence": True},
        {"valuation_without_assumptions": True},
        {"approval_gate_bypassed": True},
        {"live_without_user_agent": True},
        {"non_sec_url": True},
        {"text": "trade instruction"},
        {"text": "position size"},
        {"text": "broker.connect"},
    ]
    for case in cases:
        assert production_red_team.red_team_payload(case), case
    assert not production_red_team.red_team_payload({"clean": True, "note": "scenario output not recommendation"})
    print("PASS: production red-team tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
