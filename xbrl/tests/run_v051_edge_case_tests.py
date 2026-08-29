#!/usr/bin/env python3
"""v0.5.1 synthetic edge-case coverage tests."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = ROOT.parent
QA_DIR = REPO_ROOT / "goodluck-stock-research" / "qa"
PIPELINE_DIR = REPO_ROOT / "goodluck-stock-research" / "pipeline"
sys.path.insert(0, str(QA_DIR))
sys.path.insert(0, str(PIPELINE_DIR))

from artifact_hygiene_checker import check_hygiene  # noqa: E402
from dashboard_quality_checker import check_dashboard  # noqa: E402


REQUIRED_CASES = {
    "approved_review_missing_quality_score",
    "quality_ready_missing_checklist",
    "partial_field_downstream_ratio_unavailable",
    "blocked_real_company_dry_run_attempt",
    "blocked_real_company_csv_generation_attempt",
    "stale_mapping_version",
    "superseded_review_batch",
    "artifact_path_leak",
    "raw_filing_accidentally_present",
    "forbidden_conclusion_phrase_in_packet",
}


def load_cases() -> list[dict[str, str]]:
    """Load edge case declarations."""
    path = REPO_ROOT / "goodluck-stock-research" / "xbrl" / "fixtures" / "edge_cases_v051" / "cases.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    assert isinstance(cases, list)
    return cases


def assert_case_declarations_complete() -> None:
    """Every requested edge case must have an expected result."""
    cases = load_cases()
    ids = {case["case_id"] for case in cases}
    assert REQUIRED_CASES == ids
    for case in cases:
        assert case.get("expected_result") in {"fail", "blocked", "pass_with_disclosure"}
        assert case.get("blocking_reason")


def assert_artifact_edge_cases_fail() -> None:
    """Path leaks and raw filing artifacts should be caught."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        examples = tmp_root / "goodluck-stock-research" / "examples"
        examples.mkdir(parents=True)
        (examples / "leak.md").write_text("/Users/example/local-path\n", encoding="utf-8")
        (examples / "raw-filing.html").write_text("<html>full filing placeholder</html>\n", encoding="utf-8")
        results = check_hygiene(tmp_root)
        failed = {item.check for item in results if not item.passed}
        assert "no /Users path leaks" in failed
        assert "no raw full filings committed" in failed


def assert_dashboard_conclusion_phrase_fails() -> None:
    """Forbidden conclusion phrases in dashboard Markdown should fail."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        dash = tmp_root / "goodluck-stock-research" / "examples" / "pipeline_audit_dashboard"
        dash.mkdir(parents=True)
        (dash / "pipeline_audit_dashboard.md").write_text("target price: 123\n", encoding="utf-8")
        (dash / "blocked_real_company_matrix.md").write_text("# Matrix\n", encoding="utf-8")
        (dash / "pipeline_audit_summary.json").write_text('{"runs":[],"blocked_real_company_matrix":[]}\n', encoding="utf-8")
        results = check_dashboard(tmp_root, dash)
        assert any(not item.passed and item.check == "dashboard has no conclusion fields" for item in results)


def main() -> int:
    """Run tests."""
    assert_case_declarations_complete()
    assert_artifact_edge_cases_fail()
    assert_dashboard_conclusion_phrase_fails()
    print("PASS: v0.5.1 edge-case declarations and selected failure checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
