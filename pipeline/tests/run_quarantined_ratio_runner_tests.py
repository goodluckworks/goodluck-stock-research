#!/usr/bin/env python3
"""Tests for quarantined ratio runner policy."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "pipeline"))

import quarantined_ratio_runner


def main() -> int:
    csv_path = ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "MRVL" / "quarantined_normalized_sandbox.csv"
    decision = quarantined_ratio_runner.can_run_ratio(csv_path)
    assert decision["decision"] == "allow"
    text = quarantined_ratio_runner.render_policy(csv_path)
    assert "Ratio only" in text
    assert "No DCF" in text
    assert "no zero-fill" in text.lower()
    print("PASS: quarantined ratio runner tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
