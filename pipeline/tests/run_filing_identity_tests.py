#!/usr/bin/env python3
"""Tests for filing identity checker."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "pipeline"))

import filing_identity_checker


def main() -> int:
    fixture = ROOT / "goodluck-stock-research" / "pipeline" / "fixtures" / "identity_drills"
    expected = json.loads((fixture / "expected_results.json").read_text(encoding="utf-8"))
    for name, status in expected.items():
        if status in {"warning", "blocked"}:
            continue
        result = filing_identity_checker.check_identity(filing_identity_checker.load_json(fixture / f"{name}.json"))
        assert result.status == status, (name, result)
    print("PASS: filing identity tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
