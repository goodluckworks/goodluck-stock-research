#!/usr/bin/env python3
"""Policy checks for review-gated offline pipeline modes."""

from __future__ import annotations


MODES = {
    "fictional_sandbox_full",
    "fictional_sandbox_partial",
    "real_company_review_only",
    "blocked_real_company_promotion_attempt",
}
REAL_TICKERS = {"MRVL", "NVDA", "AVGO"}
FICTIONAL_TICKER = "EXMP"


def validate_mode_ticker(mode: str, ticker: str) -> None:
    """Validate mode / ticker boundary."""
    ticker = ticker.upper()
    if mode not in MODES:
        raise ValueError(f"Unsupported pipeline mode: {mode}")
    if mode.startswith("fictional_sandbox") and ticker != FICTIONAL_TICKER:
        raise ValueError("Fictional sandbox modes allow only EXMP.")
    if mode in {"real_company_review_only", "blocked_real_company_promotion_attempt"} and ticker not in REAL_TICKERS:
        raise ValueError("Real-company review modes allow only MRVL, NVDA or AVGO.")


def blocked_steps_for(mode: str, ticker: str) -> list[dict[str, str]]:
    """Return blocked steps for a mode."""
    validate_mode_ticker(mode, ticker)
    if mode.startswith("fictional_sandbox"):
        return []
    return [
        {"step": "promotion", "reason": "real_company_promotion_blocked"},
        {"step": "normalized_csv", "reason": "real_company_csv_generation_blocked"},
        {"step": "v02_ratio_dry_run", "reason": "real_company_dry_run_blocked"},
    ]
