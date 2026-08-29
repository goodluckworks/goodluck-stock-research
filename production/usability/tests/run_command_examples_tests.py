#!/usr/bin/env python3
"""Tests for command examples."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
USABILITY = ROOT / "goodluck-stock-research" / "production" / "usability"
sys.path.insert(0, str(USABILITY))

from command_examples_validator import EXAMPLES, validate_examples  # noqa: E402


def main() -> int:
    assert len(EXAMPLES) >= 3
    assert not validate_examples(), validate_examples()
    assert validate_examples(["python3 goodluck-stock-research/production/cli.py research --mode fixture"])
    print("PASS: command examples tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
