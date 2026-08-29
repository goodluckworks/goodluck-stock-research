#!/usr/bin/env python3
"""Pipeline policy tests."""

from __future__ import annotations

import sys
from pathlib import Path


PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR))

from pipeline_policy import blocked_steps_for, validate_mode_ticker  # noqa: E402


def expect_failure(mode: str, ticker: str, expected: str) -> None:
    """Assert policy failure."""
    try:
        validate_mode_ticker(mode, ticker)
    except ValueError as exc:
        assert expected.casefold() in str(exc).casefold(), str(exc)
    else:
        raise AssertionError("Expected policy failure")


def main() -> int:
    """Run policy tests."""
    validate_mode_ticker("fictional_sandbox_full", "EXMP")
    validate_mode_ticker("fictional_sandbox_partial", "EXMP")
    for ticker in ("MRVL", "NVDA", "AVGO"):
        validate_mode_ticker("real_company_review_only", ticker)
        validate_mode_ticker("blocked_real_company_promotion_attempt", ticker)
        blocked = blocked_steps_for("real_company_review_only", ticker)
        assert {item["step"] for item in blocked} == {"promotion", "normalized_csv", "v02_ratio_dry_run"}
    expect_failure("fictional_sandbox_full", "MRVL", "allow only EXMP")
    expect_failure("real_company_review_only", "EXMP", "MRVL, NVDA or AVGO")
    expect_failure("unknown", "EXMP", "Unsupported")
    print("PASS: pipeline policy mode/ticker gates and blocked steps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
