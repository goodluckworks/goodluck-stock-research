#!/usr/bin/env python3
"""End-to-end XBRL sandbox pipeline audit tests."""

from __future__ import annotations

import csv
import json
import shutil
import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
ROOT = XBRL_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from end_to_end_pipeline_auditor import audit_pipeline  # noqa: E402
from generate_normalized_csv_sandbox import run_generator  # noqa: E402
from run_v02_sandbox_dry_run import run_dry_run  # noqa: E402


EXMP_CANDIDATE_DIR = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP"
EXMP_QUALITY_DIR = ROOT / "examples" / "xbrl_review_quality" / "EXMP"
EXMP_REVIEW_DIR = ROOT / "examples" / "xbrl_review_decisions" / "EXMP"
EXMP_PROMOTION_DIR = ROOT / "examples" / "xbrl_promotion_runs" / "EXMP"


def read_json(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write_json(path: Path, value: object) -> None:
    """Write JSON object."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read CSV rows with fieldnames."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    """Write CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_pipeline(root: Path) -> tuple[Path, Path, Path, Path, Path, Path]:
    """Copy EXMP fixtures and build normalized plus dry-run outputs."""
    candidate_dir = root / "candidate"
    quality_dir = root / "quality"
    review_dir = root / "review"
    promotion_dir = root / "promotion"
    normalized_dir = root / "normalized"
    dry_run_dir = root / "dry-run"
    shutil.copytree(EXMP_CANDIDATE_DIR, candidate_dir)
    shutil.copytree(EXMP_QUALITY_DIR, quality_dir)
    shutil.copytree(EXMP_REVIEW_DIR, review_dir)
    shutil.copytree(EXMP_PROMOTION_DIR, promotion_dir)
    run_generator(
        promotion_dir,
        review_dir / "normalized_review_batch.json",
        candidate_dir / "extraction_candidates.json",
        candidate_dir / "extraction_run_manifest.json",
        normalized_dir,
    )
    run_dry_run(normalized_dir / "normalized_financials_sandbox.csv", dry_run_dir)
    return candidate_dir, quality_dir, review_dir, promotion_dir, normalized_dir, dry_run_dir


def run_audit(paths: tuple[Path, Path, Path, Path, Path, Path], report: Path) -> list[str]:
    """Run pipeline audit."""
    return audit_pipeline(*paths, report)


def main() -> int:
    """Run end-to-end pipeline audit tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-e2e-audit-tests-") as temp_name:
        temp = Path(temp_name)
        paths = build_pipeline(temp / "pass")
        errors = run_audit(paths, temp / "pass" / "audit" / "report.md")
        assert errors == []
        report = (temp / "pass" / "audit" / "report.md").read_text(encoding="utf-8")
        assert "Audit passed: `true`" in report

        mismatch_paths = build_pipeline(temp / "id-mismatch")
        promotion_manifest = read_json(mismatch_paths[3] / "promotion_manifest.json")
        promotion_manifest["review_batch_id"] = "wrong-review-batch"
        write_json(mismatch_paths[3] / "promotion_manifest.json", promotion_manifest)
        errors = run_audit(mismatch_paths, temp / "id-mismatch" / "audit.md")
        assert any("review_batch_id mismatch" in error for error in errors)

        csv_mismatch_paths = build_pipeline(temp / "csv-value-mismatch")
        headers, rows = read_csv_rows(csv_mismatch_paths[4] / "normalized_financials_sandbox.csv")
        rows[0]["revenue"] = "999999"
        write_csv(csv_mismatch_paths[4] / "normalized_financials_sandbox.csv", headers, rows)
        errors = run_audit(csv_mismatch_paths, temp / "csv-value-mismatch" / "audit.md")
        assert any("CSV value mismatch for revenue" in error for error in errors)

        unresolved_paths = build_pipeline(temp / "unresolved-populated")
        headers, rows = read_csv_rows(unresolved_paths[4] / "normalized_financials_sandbox.csv")
        rows[0]["net_income"] = "123"
        write_csv(unresolved_paths[4] / "normalized_financials_sandbox.csv", headers, rows)
        errors = run_audit(unresolved_paths, temp / "unresolved-populated" / "audit.md")
        assert any("Unresolved/rejected field populated" in error for error in errors)

        no_banner_paths = build_pipeline(temp / "no-banner")
        (no_banner_paths[5] / "ratio_output_sandbox.md").write_text("# Ratio Output\n", encoding="utf-8")
        errors = run_audit(no_banner_paths, temp / "no-banner" / "audit.md")
        assert any("dry-run output missing sandbox banner" in error for error in errors)

        real_paths = build_pipeline(temp / "real-ticker")
        manifest = read_json(real_paths[0] / "extraction_run_manifest.json")
        manifest["ticker"] = "MRVL"
        manifest["fictional_company"] = False
        write_json(real_paths[0] / "extraction_run_manifest.json", manifest)
        errors = run_audit(real_paths, temp / "real-ticker" / "audit.md")
        assert any("allows only EXMP" in error for error in errors)

        conclusion_paths = build_pipeline(temp / "conclusion-field")
        dry_manifest = read_json(conclusion_paths[5] / "v02_dry_run_manifest.json")
        dry_manifest["target_price"] = 100
        write_json(conclusion_paths[5] / "v02_dry_run_manifest.json", dry_manifest)
        errors = run_audit(conclusion_paths, temp / "conclusion-field" / "audit.md")
        assert any("forbidden fields" in error for error in errors)

    print("PASS: end-to-end EXMP audit, ID mismatch, CSV mismatch, unresolved field, missing banner, real ticker and conclusion-field failures")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
