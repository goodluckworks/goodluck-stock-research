#!/usr/bin/env python3
"""Partial run recovery helpers."""

from __future__ import annotations

from pathlib import Path


REQUIRED_STEPS = ["source_manifest", "filing_identity", "normalized_financials", "data_quality", "valuation", "conclusion", "report"]


def recover_run(run_dir: Path) -> dict[str, object]:
    completed = [step for step in REQUIRED_STEPS if (run_dir / f"{step}.done").exists()]
    remaining = [step for step in REQUIRED_STEPS if step not in completed]
    return {
        "recovery_schema_version": "v2.8.0",
        "completed_steps": completed,
        "remaining_steps": remaining,
        "resumable": bool(remaining),
        "silent_failure": False,
    }
