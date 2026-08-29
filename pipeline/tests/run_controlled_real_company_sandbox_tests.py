#!/usr/bin/env python3
"""Tests for controlled real-company sandbox gate."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PIPELINE_DIR = ROOT / "goodluck-stock-research" / "pipeline"
sys.path.insert(0, str(PIPELINE_DIR))

from controlled_real_company_sandbox_gate import run_gate  # noqa: E402


MRVL_DIR = ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "MRVL"
REVIEW = MRVL_DIR / "approval_inputs" / "review_batch_approved_for_quarantine.json"
QUALITY = MRVL_DIR / "approval_inputs" / "quality_score_ready_for_quarantine.json"
CANDIDATES = ROOT / "goodluck-stock-research" / "examples" / "pipeline_runs" / "MRVL" / "review_only" / "candidate" / "extraction_candidates.json"
POLICY = MRVL_DIR / "approval_inputs" / "approval_policy.json"


def load(path: Path) -> dict:
    """Load JSON."""
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict) -> Path:
    """Write JSON."""
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def expect_error(message: str, func, *args, **kwargs) -> None:
    """Assert function raises matching error."""
    try:
        func(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001 - test helper
        assert message in str(exc), f"expected {message!r}, got {exc!r}"
        return
    raise AssertionError(f"expected error containing {message!r}")


def call_gate(**overrides):
    """Call gate with defaults and optional overrides."""
    params = {
        "mode": "controlled_real_company_sandbox",
        "ticker": "MRVL",
        "output_dir": MRVL_DIR,
        "review_batch_path": REVIEW,
        "quality_score_path": QUALITY,
        "candidate_package_path": CANDIDATES,
        "approval_policy_path": POLICY,
        "allow_real_company_sandbox": True,
        "quarantine_output": True,
    }
    params.update(overrides)
    return run_gate(**params)


def assert_mrvl_outputs_complete() -> None:
    """Tracked MRVL quarantine artifacts should be complete."""
    required = [
        "quarantine_manifest.json",
        "quarantined_normalized_sandbox.csv",
        "quarantined_csv_audit.json",
        "quarantined_ratio_dry_run.md",
        "quarantined_ratio_dry_run_manifest.json",
        "quarantine_report.md",
    ]
    for name in required:
        assert (MRVL_DIR / name).is_file(), name
    manifest = load(MRVL_DIR / "quarantine_manifest.json")
    for key in (
        "quarantined",
        "not_production_data",
        "not_investment_data",
        "not_company_fact_until_verified",
        "manual_review_required",
        "not_for_trading",
        "not_for_public_release",
        "no_recommendation",
        "no_dcf",
        "no_peer_comps",
        "no_implied_expectations",
        "no_investment_conclusion",
    ):
        assert manifest.get(key) is True, key
    dry_run = (MRVL_DIR / "quarantined_ratio_dry_run.md").read_text(encoding="utf-8")
    assert "QUARANTINED REAL-COMPANY SANDBOX DRY-RUN" in dry_run
    assert "Not production data." in dry_run
    assert "Not investment advice." in dry_run
    assert "Not for trading." in dry_run
    assert "Manual review required." in dry_run
    assert not (ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "NVDA").exists()
    assert not (ROOT / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "AVGO").exists()


def assert_boundary_failures() -> None:
    """Required block cases should fail before output generation."""
    expect_error("requires --allow-real-company-sandbox", call_gate, allow_real_company_sandbox=False)
    expect_error("tracked v0.6 drill only allows MRVL", call_gate, ticker="NVDA")
    expect_error("tracked v0.6 drill only allows MRVL", call_gate, ticker="AVGO")
    expect_error("controlled output must be", call_gate, output_dir=Path("/private/tmp/not-quarantine"))
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        review = load(REVIEW)
        review["production_approved"] = True
        expect_error("production approved", call_gate, review_batch_path=write(tmp_path / "production.json", review))
        review = load(REVIEW)
        review["records"][0]["reviewer_decision"] = "unresolved"
        expect_error("unresolved promoted field", call_gate, review_batch_path=write(tmp_path / "unresolved.json", review))
        review = load(REVIEW)
        review["records"][0]["confidence"] = "low"
        expect_error("low-confidence", call_gate, review_batch_path=write(tmp_path / "low.json", review))
        review = load(REVIEW)
        review["records"][0]["review_checklist"]["unit_checked"] = False
        expect_error("missing checklist", call_gate, review_batch_path=write(tmp_path / "checklist.json", review))
        quality = load(QUALITY)
        quality["overall_status"] = "needs_review"
        expect_error("ready_for_quarantine", call_gate, quality_score_path=write(tmp_path / "quality.json", quality))
        policy = load(POLICY)
        policy["mapping_review_status"] = "draft"
        expect_error("mapping review must be approved", call_gate, approval_policy_path=write(tmp_path / "policy_draft.json", policy))
        policy = load(POLICY)
        policy["mapping_lifecycle_status"] = "superseded"
        expect_error("superseded mapping", call_gate, approval_policy_path=write(tmp_path / "policy_superseded.json", policy))


def assert_no_disallowed_outputs() -> None:
    """No DCF/peer/implied or conclusion output should exist."""
    names = {path.name for path in MRVL_DIR.iterdir() if path.is_file()}
    assert not any("dcf" in name for name in names)
    assert not any("peer" in name for name in names)
    assert not any("implied" in name for name in names)
    combined = "\n".join(path.read_text(encoding="utf-8", errors="ignore").lower() for path in MRVL_DIR.glob("*.md"))
    for term in ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:"):
        assert term not in combined


def main() -> int:
    """Run tests."""
    assert_mrvl_outputs_complete()
    assert_boundary_failures()
    assert_no_disallowed_outputs()
    print("PASS: controlled real-company sandbox MRVL quarantine and blocked boundary tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
