#!/usr/bin/env python3
"""Package audit tests for extraction, review and promotion consistency."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
ROOT = XBRL_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from offline_xbrl_candidate_extractor import Config, run as run_extraction  # noqa: E402
from package_auditor import audit_package  # noqa: E402
from promote_reviewed_fields import run_promotion  # noqa: E402
from review_decision_collector import run_collector  # noqa: E402
from review_quality_scorer import run_scorer  # noqa: E402
from reviewer_workbench import run_workbench  # noqa: E402


MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"
FIXTURE = XBRL_DIR / "fixtures" / "exmp_fictional_inline_xbrl.html"
REVIEW = XBRL_DIR / "review_fixtures" / "exmp_review_approved.json"
MAPPING_REVIEW = XBRL_DIR / "mapping_review_fixtures" / "mapping_review_approved_v0_3_7.json"


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write(path: Path, value: object) -> None:
    """Write JSON."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def extract(output: Path) -> Path:
    """Create extraction package."""
    run_extraction(
        Config(
            input_file=FIXTURE,
            mapping_file=MAPPING,
            company="Example Semiconductor Corp.",
            ticker="EXMP",
            cik="0000000000",
            accession="fictional-exmp-001",
            form_type="10-K",
            reporting_period="FY2025",
            fiscal_year="2025",
            fiscal_quarter="FY",
            currency="USD",
            amount_unit="USD millions",
            per_share_unit="USD/share",
            fixture_format="data_attr",
            output_dir=output,
        )
    )
    return output


def copy_package(source: Path, dest: Path) -> Path:
    """Copy JSON package files."""
    dest.mkdir()
    for name in (
        "extraction_run_manifest.json",
        "extraction_candidates.json",
        "field_provenance.json",
        "unresolved_fields.json",
    ):
        (dest / name).write_text((source / name).read_text(encoding="utf-8"), encoding="utf-8")
    return dest


def normalized_review_package(root: Path, extraction_dir: Path) -> tuple[Path, Path]:
    """Create a v0.3.7 normalized review package for an extraction."""
    workbench_dir = root / "workbench"
    quality_dir = root / "quality"
    decision_dir = root / "review-decisions"
    run_workbench(
        extraction_dir / "extraction_candidates.json",
        extraction_dir / "extraction_run_manifest.json",
        extraction_dir / "field_provenance.json",
        workbench_dir / "review_workbench.md",
        workbench_dir / "review_decision_template.json",
    )
    run_scorer(
        extraction_dir / "extraction_candidates.json",
        extraction_dir / "extraction_run_manifest.json",
        extraction_dir / "field_provenance.json",
        quality_dir,
    )
    run_collector(
        workbench_dir / "review_decision_template.json",
        extraction_dir / "extraction_candidates.json",
        extraction_dir / "extraction_run_manifest.json",
        quality_dir / "review_quality_score.json",
        decision_dir,
    )
    return decision_dir, quality_dir


def main() -> int:
    """Run package audit tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-package-audit-tests-") as temp_name:
        temp = Path(temp_name)
        extraction = extract(temp / "EXMP")
        review_dir, quality_dir = normalized_review_package(temp, extraction)
        review_file = review_dir / "normalized_review_batch.json"
        decision_log = review_dir / "review_decision_log.json"
        quality_file = quality_dir / "review_quality_score.json"
        promotion = temp / "promotion"
        run_promotion(
            review_file,
            extraction / "extraction_candidates.json",
            extraction / "extraction_run_manifest.json",
            MAPPING,
            MAPPING_REVIEW,
            decision_log,
            quality_file,
            "test-package-audit-reference",
            promotion,
        )
        assert not audit_package(extraction, review_file, promotion, MAPPING, MAPPING_REVIEW, decision_log, quality_file)

        mismatch = copy_package(extraction, temp / "candidate-mismatch")
        candidates = read(mismatch / "extraction_candidates.json")
        candidates["candidates"][0]["candidate_id"] = "bad-id"
        write(mismatch / "extraction_candidates.json", candidates)
        assert audit_package(mismatch)

        checksum = copy_package(extraction, temp / "checksum")
        manifest = read(checksum / "extraction_run_manifest.json")
        manifest["snapshot_sha256"] = "0" * 64
        write(checksum / "extraction_run_manifest.json", manifest)
        assert audit_package(checksum, review_file, promotion, MAPPING, MAPPING_REVIEW, decision_log, quality_file)

        mapping = copy_package(extraction, temp / "mapping")
        manifest = read(mapping / "extraction_run_manifest.json")
        manifest["mapping_version"] = "wrong"
        write(mapping / "extraction_run_manifest.json", manifest)
        assert audit_package(mapping, review_file, promotion, MAPPING, MAPPING_REVIEW, decision_log, quality_file)

        bad_review = read(review_file)
        bad_review["records"][0]["reviewer_decision"] = "reject"
        bad_review_path = temp / "bad-review.json"
        write(bad_review_path, bad_review)
        assert audit_package(extraction, bad_review_path, promotion, MAPPING, MAPPING_REVIEW, decision_log, quality_file)

        low_review = read(review_file)
        low_review["records"][0]["confidence"] = "low"
        low_review_path = temp / "low-review.json"
        write(low_review_path, low_review)
        assert audit_package(extraction, low_review_path, promotion, MAPPING, MAPPING_REVIEW, decision_log, quality_file)

        real_promotion = temp / "real-promotion"
        real_promotion.mkdir()
        promo_manifest = read(promotion / "promotion_manifest.json")
        draft = read(promotion / "approved_normalized_draft.json")
        promo_manifest["ticker"] = "MRVL"
        draft["ticker"] = "MRVL"
        write(real_promotion / "promotion_manifest.json", promo_manifest)
        write(real_promotion / "approved_normalized_draft.json", draft)
        assert audit_package(extraction, review_file, real_promotion, MAPPING, MAPPING_REVIEW, decision_log, quality_file)

        conclusion = copy_package(extraction, temp / "conclusion")
        manifest = read(conclusion / "extraction_run_manifest.json")
        manifest["research_status"] = "候选"
        write(conclusion / "extraction_run_manifest.json", manifest)
        assert audit_package(conclusion)

    print("PASS: package audit valid EXMP, candidate mismatch, checksum mismatch, mapping mismatch, rejected promotion, low confidence, real ticker promotion and conclusion-field tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
