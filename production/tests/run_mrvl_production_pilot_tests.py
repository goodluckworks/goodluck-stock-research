#!/usr/bin/env python3
"""Tests for MRVL production pilot."""

from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "pilot"))

import mrvl_production_pilot


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp)
        result = mrvl_production_pilot.run_pilot(ROOT, output, human_approval=False)
        assert result["approval"]["state"] == "review_required"
        approved = mrvl_production_pilot.run_pilot(ROOT, output / "approved", human_approval=True)
        assert approved["approval"]["state"] == "publishable_research_packet"
        report = (output / "mrvl_internal_research_packet.md").read_text(encoding="utf-8").lower()
        for forbidden in ("buy now", "sell now", "position size:", "broker order"):
            assert forbidden not in report
        assert "not personalized advice" in report
        assert "not a trading instruction" in report
    print("PASS: MRVL production pilot tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
