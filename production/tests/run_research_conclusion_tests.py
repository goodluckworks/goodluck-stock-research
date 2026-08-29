#!/usr/bin/env python3
"""Tests for research conclusion engine."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "conclusion"))

import research_conclusion_engine
import conclusion_auditor


def main() -> int:
    quality = {"status": "usable_internal", "score": 90, "issues": []}
    valuation = {"fair_value_range": {"low": 1, "high": 2, "label": "scenario output, not recommendation"}}
    constructive = research_conclusion_engine.generate_conclusion(quality, valuation, ["source manifest", "normalized statement"])
    assert constructive["conclusion_label"] == "constructive"
    assert not conclusion_auditor.audit(constructive)
    insufficient = research_conclusion_engine.generate_conclusion({"status": "production_blocked", "score": 20, "issues": ["low quality"]}, valuation, [])
    assert insufficient["conclusion_label"] == "insufficient_evidence"
    missing_valuation = research_conclusion_engine.generate_conclusion(quality, None, ["source"])
    assert missing_valuation["conclusion_label"] == "insufficient_evidence"
    bad = dict(constructive)
    bad["note"] = "buy now"
    assert conclusion_auditor.audit(bad)
    print("PASS: research conclusion tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
