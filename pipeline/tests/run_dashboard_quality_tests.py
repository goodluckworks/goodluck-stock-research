#!/usr/bin/env python3
"""Tests for dashboard quality checker."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "goodluck-stock-research" / "pipeline"
sys.path.insert(0, str(PIPELINE_DIR))

from dashboard_quality_checker import check_dashboard  # noqa: E402


def assert_current_dashboard_passes() -> None:
    """Current dashboard should satisfy quality checks."""
    results = check_dashboard(ROOT, ROOT / "goodluck-stock-research" / "examples" / "pipeline_audit_dashboard")
    failed = [item for item in results if not item.passed]
    assert not failed, "\n".join(f"{item.check}: {item.notes}" for item in failed[:20])


def write_json(path: Path, payload: object) -> None:
    """Write JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def assert_missing_blocked_reason_fails() -> None:
    """Missing blocked reasons should fail."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        dash = tmp_root / "goodluck-stock-research" / "examples" / "pipeline_audit_dashboard"
        run_dir = tmp_root / "goodluck-stock-research" / "examples" / "pipeline_runs" / "MRVL" / "review_only"
        packet = tmp_root / "goodluck-stock-research" / "examples" / "research_packets" / "MRVL" / "review_only_packet.md"
        packet.parent.mkdir(parents=True)
        packet.write_text("# Review-Only Research Packet: MRVL\n", encoding="utf-8")
        write_json(
            run_dir / "pipeline_run_manifest.json",
            {
                "ticker": "MRVL",
                "mode": "real_company_review_only",
                "blocked_steps": [{"step": "promotion", "reason": ""}],
            },
        )
        write_json(
            dash / "pipeline_audit_summary.json",
            {
                "runs": [
                    {
                        "ticker": "MRVL",
                        "mode": "real_company_review_only",
                        "run_dir": "goodluck-stock-research/examples/pipeline_runs/MRVL/review_only",
                        "dry_run_status": "blocked_or_not_applicable",
                        "promotion_status": "blocked_or_not_applicable",
                        "normalized_csv_status": "blocked_or_not_applicable",
                        "audit_completeness": "complete",
                        "packet_status": "present",
                    }
                ],
                "blocked_real_company_matrix": [],
            },
        )
        (dash / "pipeline_audit_dashboard.md").write_text("# Dashboard\n", encoding="utf-8")
        (dash / "blocked_real_company_matrix.md").write_text("# Matrix\n", encoding="utf-8")
        results = check_dashboard(tmp_root, dash)
        assert any(not item.passed and "blocked promotion has reason" in item.check for item in results)


def main() -> int:
    """Run tests."""
    assert_current_dashboard_passes()
    assert_missing_blocked_reason_fails()
    print("PASS: dashboard quality current and negative tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
