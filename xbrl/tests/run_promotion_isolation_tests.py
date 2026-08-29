#!/usr/bin/env python3
"""Promotion isolation hardening tests."""

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

from package_auditor import audit_package  # noqa: E402
from promote_reviewed_fields import run_promotion  # noqa: E402
from review_decision_collector import run_collector  # noqa: E402
from review_quality_scorer import run_scorer  # noqa: E402
from reviewer_workbench import run_workbench  # noqa: E402


EXAMPLES = ROOT / "examples" / "xbrl_extraction_runs"
EXMP = EXAMPLES / "EXMP"
MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"
APPROVED_MAPPING = XBRL_DIR / "mapping_review_fixtures" / "mapping_review_approved_v0_3_7.json"
SUPERSEDED_MAPPING = XBRL_DIR / "mapping_review_fixtures" / "mapping_review_superseded_v0_3_7.json"
REJECTED_MAPPING = XBRL_DIR / "mapping_review_fixtures" / "mapping_review_rejected_v0_3_7.json"


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write(path: Path, value: object) -> None:
    """Write JSON."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def review_package(temp: Path, extraction_dir: Path, label: str) -> tuple[Path, Path, Path, Path]:
    """Create workbench template and normalized review package."""
    workbench = temp / f"{label}-workbench"
    quality_dir = temp / f"{label}-quality"
    review_dir = temp / f"{label}-review"
    run_workbench(
        extraction_dir / "extraction_candidates.json",
        extraction_dir / "extraction_run_manifest.json",
        extraction_dir / "field_provenance.json",
        workbench / "review_workbench.md",
        workbench / "review_decision_template.json",
    )
    run_scorer(
        extraction_dir / "extraction_candidates.json",
        extraction_dir / "extraction_run_manifest.json",
        extraction_dir / "field_provenance.json",
        quality_dir,
    )
    run_collector(
        workbench / "review_decision_template.json",
        extraction_dir / "extraction_candidates.json",
        extraction_dir / "extraction_run_manifest.json",
        quality_dir / "review_quality_score.json",
        review_dir,
    )
    return (
        workbench / "review_decision_template.json",
        review_dir / "normalized_review_batch.json",
        review_dir / "review_decision_log.json",
        quality_dir / "review_quality_score.json",
    )


def expect_promotion_failure(args: tuple[object, ...], expected: str) -> None:
    """Assert promotion failure includes expected text."""
    try:
        run_promotion(*args)
    except (ValueError, FileNotFoundError) as exc:
        assert expected in str(exc), str(exc)
    else:
        raise AssertionError(f"Expected promotion failure containing {expected!r}")


def main() -> int:
    """Run promotion isolation tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-promotion-isolation-tests-") as temp_name:
        temp = Path(temp_name)
        raw_template, review_file, decision_log, quality_file = review_package(temp, EXMP, "exmp")
        output = temp / "exmp-promotion"
        run_promotion(
            review_file,
            EXMP / "extraction_candidates.json",
            EXMP / "extraction_run_manifest.json",
            MAPPING,
            APPROVED_MAPPING,
            decision_log,
            quality_file,
            "test-package-audit-reference",
            output,
        )
        assert not audit_package(EXMP, review_file, output, MAPPING, APPROVED_MAPPING, decision_log, quality_file)

        for ticker in ("MRVL", "NVDA", "AVGO"):
            _raw, real_review, real_log, real_quality = review_package(temp, EXAMPLES / ticker, ticker.lower())
            expect_promotion_failure(
                (
                    real_review,
                    EXAMPLES / ticker / "extraction_candidates.json",
                    EXAMPLES / ticker / "extraction_run_manifest.json",
                    MAPPING,
                    APPROVED_MAPPING,
                    real_log,
                    real_quality,
                    "test-package-audit-reference",
                    temp / f"{ticker}-promotion",
                ),
                "Real ticker promotion blocked by default",
            )

        expect_promotion_failure(
            (
                review_file,
                EXMP / "extraction_candidates.json",
                EXMP / "extraction_run_manifest.json",
                MAPPING,
                SUPERSEDED_MAPPING,
                decision_log,
                quality_file,
                "test-package-audit-reference",
                temp / "superseded",
            ),
            "superseded",
        )
        expect_promotion_failure(
            (
                review_file,
                EXMP / "extraction_candidates.json",
                EXMP / "extraction_run_manifest.json",
                MAPPING,
                REJECTED_MAPPING,
                decision_log,
                quality_file,
                "test-package-audit-reference",
                temp / "rejected",
            ),
            "rejected",
        )
        expect_promotion_failure(
            (
                raw_template,
                EXMP / "extraction_candidates.json",
                EXMP / "extraction_run_manifest.json",
                MAPPING,
                APPROVED_MAPPING,
                decision_log,
                quality_file,
                "test-package-audit-reference",
                temp / "raw-template",
            ),
            "Review validation failed",
        )
        expect_promotion_failure(
            (
                review_file,
                EXMP / "extraction_candidates.json",
                EXMP / "extraction_run_manifest.json",
                MAPPING,
                APPROVED_MAPPING,
                decision_log,
                quality_file,
                "",
                temp / "missing-audit-ref",
            ),
            "package_audit_reference is required",
        )

        poisoned = read(review_file)
        poisoned["target_price"] = 100
        poisoned_path = temp / "poisoned-review.json"
        write(poisoned_path, poisoned)
        errors = audit_package(EXMP, poisoned_path, output, MAPPING, APPROVED_MAPPING, decision_log, quality_file)
        assert any("forbidden conclusion/trading field" in error for error in errors)

    print("PASS: promotion isolation EXMP allow, real-ticker blocks, superseded/rejected mapping blocks, raw template block, missing audit reference and conclusion-field audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
