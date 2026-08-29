#!/usr/bin/env python3
"""Pipeline orchestrator tests."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR))

from pipeline_orchestrator import run_pipeline  # noqa: E402


COMPANIES = {
    "EXMP": "Example Semiconductor Corp.",
    "MRVL": "Marvell Technology, Inc.",
    "NVDA": "NVIDIA Corporation",
    "AVGO": "Broadcom Inc.",
}


def read(path: Path) -> dict[str, object]:
    """Read JSON."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def assert_no_forbidden(path: Path) -> None:
    """Assert no forbidden conclusion fields in markdown."""
    for markdown in path.rglob("*.md"):
        lowered = markdown.read_text(encoding="utf-8").lower()
        for term in ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:"):
            assert term not in lowered, f"{term} in {markdown}"


def main() -> int:
    """Run pipeline orchestrator tests."""
    with tempfile.TemporaryDirectory(prefix="pipeline-orchestrator-tests-") as temp_name:
        temp = Path(temp_name)
        for mode, dirname in (
            ("fictional_sandbox_full", "full"),
            ("fictional_sandbox_partial", "partial"),
        ):
            run_pipeline(mode, "EXMP", COMPANIES["EXMP"], temp / "EXMP" / dirname)
            manifest = read(temp / "EXMP" / dirname / "pipeline_run_manifest.json")
            assert manifest["mode"] == mode
            assert manifest["ticker"] == "EXMP"
            assert manifest["no_investment_conclusion"] is True
            assert not manifest["blocked_steps"]
            assert (temp / "EXMP" / dirname / "normalized_csv_sandbox" / "normalized_csv_manifest.json").is_file()
            assert (temp / "EXMP" / dirname / "v02_ratio_dry_run" / "v02_dry_run_manifest.json").is_file()
            assert (temp / "EXMP" / dirname / "end_to_end_audit" / "end_to_end_audit_report.md").is_file()
            assert_no_forbidden(temp / "EXMP" / dirname)

        for ticker in ("MRVL", "NVDA", "AVGO"):
            run_pipeline("real_company_review_only", ticker, COMPANIES[ticker], temp / ticker / "review_only")
            manifest = read(temp / ticker / "review_only" / "pipeline_run_manifest.json")
            assert manifest["mode"] == "real_company_review_only"
            assert {item["step"] for item in manifest["blocked_steps"]} == {
                "promotion",
                "normalized_csv",
                "v02_ratio_dry_run",
            }
            assert not (temp / ticker / "review_only" / "promotion").exists()
            assert not (temp / ticker / "review_only" / "normalized_csv_sandbox").exists()
            assert not (temp / ticker / "review_only" / "v02_ratio_dry_run").exists()
            assert_no_forbidden(temp / ticker / "review_only")

            run_pipeline(
                "blocked_real_company_promotion_attempt",
                ticker,
                COMPANIES[ticker],
                temp / ticker / "blocked_attempt",
            )
            blocked = read(temp / ticker / "blocked_attempt" / "pipeline_run_manifest.json")
            assert blocked["mode"] == "blocked_real_company_promotion_attempt"
            assert len(blocked["blocked_steps"]) == 3
            assert_no_forbidden(temp / ticker / "blocked_attempt")

    source = (PIPELINE_DIR / "pipeline_orchestrator.py").read_text(encoding="utf-8")
    assert "subprocess" not in source
    assert "os.environ" not in source
    print("PASS: pipeline orchestrator EXMP full/partial, MRVL/NVDA/AVGO review-only and blocked attempts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
