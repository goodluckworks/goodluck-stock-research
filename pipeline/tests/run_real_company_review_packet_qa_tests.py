#!/usr/bin/env python3
"""Tests for real-company review packet QA."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "goodluck-stock-research" / "pipeline"
sys.path.insert(0, str(PIPELINE_DIR))

from real_company_review_packet_qa import run_qa  # noqa: E402


def assert_current_packets_pass() -> None:
    """Current MRVL/NVDA/AVGO packets should pass QA."""
    results = run_qa(ROOT)
    failed = [item for item in results if not item.passed]
    assert not failed, "\n".join(f"{item.ticker} {item.check}: {item.notes}" for item in failed[:20])


def assert_missing_packet_fails() -> None:
    """Missing packet should be reported."""
    with tempfile.TemporaryDirectory() as tmp:
        results = run_qa(Path(tmp))
        assert any(not item.passed and item.check == "review_only_packet.md exists" for item in results)


def main() -> int:
    """Run tests."""
    assert_current_packets_pass()
    assert_missing_packet_fails()
    print("PASS: real-company review packet QA current and missing-packet tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
