#!/usr/bin/env python3
"""Tests for source monitor."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REL = ROOT / "goodluck-stock-research" / "production" / "reliability"
sys.path.insert(0, str(REL))

from source_monitor import monitor_sources  # noqa: E402


def main() -> int:
    report = monitor_sources([{"source": "sec", "status": "available"}, {"source": "market", "status": "unavailable"}])
    assert report["unavailable_count"] == 1
    assert report["partial_report_allowed"] is True
    assert report["silent_failure"] is False
    print("PASS: reliability source monitor tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
