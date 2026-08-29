#!/usr/bin/env python3
"""Tests for amendment/restatement drill."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "pipeline"))

import amendment_restatement_drill


def load(name: str) -> dict:
    path = ROOT / "goodluck-stock-research" / "pipeline" / "fixtures" / "identity_drills" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    amendment = amendment_restatement_drill.evaluate(load("mrvl_amendment_present"))
    assert amendment["status"] == "warning"
    assert amendment["production_ready"] is False
    restatement = amendment_restatement_drill.evaluate(load("mrvl_restatement_conflict"))
    assert restatement["status"] == "blocked"
    assert restatement["blockers"]
    print("PASS: amendment/restatement drill tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
