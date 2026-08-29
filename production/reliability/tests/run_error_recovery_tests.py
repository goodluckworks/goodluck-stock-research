#!/usr/bin/env python3
"""Tests for error taxonomy and recovery."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REL = ROOT / "goodluck-stock-research" / "production" / "reliability"
sys.path.insert(0, str(REL))

from error_taxonomy import classify_error  # noqa: E402
from retry_policy import retry_schedule  # noqa: E402
from run_recovery import recover_run  # noqa: E402


def main() -> int:
    assert classify_error("source_unavailable")["silent_failure_allowed"] == "false"
    assert retry_schedule(3) == [0.0, 0.2, 0.4]
    try:
        retry_schedule(10)
        raise AssertionError("unbounded retry should fail")
    except ValueError:
        pass
    with tempfile.TemporaryDirectory() as tmp:
        run_dir = Path(tmp)
        (run_dir / "source_manifest.done").write_text("", encoding="utf-8")
        recovery = recover_run(run_dir)
        assert recovery["resumable"] is True
        assert "filing_identity" in recovery["remaining_steps"]
    print("PASS: reliability error recovery tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
