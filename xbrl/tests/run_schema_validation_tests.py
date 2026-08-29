#!/usr/bin/env python3
"""Schema validation tests for v0.3.5 XBRL package contracts."""

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
from promote_reviewed_fields import run_promotion  # noqa: E402
from review_decision_collector import run_collector  # noqa: E402
from review_quality_scorer import run_scorer  # noqa: E402
from reviewer_workbench import run_workbench  # noqa: E402
from schema_validator import run_package, validate_file  # noqa: E402


SCHEMAS = XBRL_DIR / "schemas"
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


def extract_exmp(output: Path) -> Path:
    """Create a temporary valid EXMP extraction package."""
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


def assert_invalid(schema: Path, payload: dict[str, object], temp: Path) -> None:
    """Write invalid payload and assert schema failure."""
    target = temp / "invalid.json"
    write(target, payload)
    passed, errors, _ = validate_file(schema, target)
    assert not passed
    assert errors


def normalized_review_package(root: Path, extraction_dir: Path) -> tuple[Path, Path]:
    """Create a v0.3.7 normalized review package."""
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
    """Run schema validation tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-schema-tests-") as temp_name:
        temp = Path(temp_name)
        extraction = extract_exmp(temp / "EXMP")
        assert run_package(SCHEMAS, extraction, temp / "extraction-schema-report.md")
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
        assert run_package(SCHEMAS, promotion, temp / "promotion-schema-report.md")
        assert validate_file(
            SCHEMAS / "review_batch_schema.json", review_file
        )[0]
        assert validate_file(
            SCHEMAS / "review_quality_score_schema.json", quality_file
        )[0]
        assert validate_file(
            SCHEMAS / "mapping_registry_schema.json", MAPPING
        )[0]

        candidates = read(extraction / "extraction_candidates.json")
        relationship_package = {
            "relationship_schema_version": "v0.3.7",
            "relationship_package_id": "test-taxonomy-relationships",
            "mapping_version": candidates["mapping_version"],
            "created_at": "2026-06-29T00:00:00Z",
            "records": [
                candidate["taxonomy_relationship"]
                for candidate in candidates["candidates"]
            ],
        }
        relationship_path = temp / "taxonomy-relationships.json"
        write(relationship_path, relationship_package)
        assert validate_file(
            SCHEMAS / "taxonomy_relationship_schema.json", relationship_path
        )[0]
        checklist_path = temp / "review-checklist.json"
        write(checklist_path, candidates["candidates"][0]["review_checklist"])
        assert validate_file(
            SCHEMAS / "review_checklist_schema.json", checklist_path
        )[0]
        missing = copy.deepcopy(candidates)
        del missing["candidates"][0]["candidate_id"]
        assert_invalid(SCHEMAS / "extraction_candidate_schema.json", missing, temp)

        forbidden = copy.deepcopy(candidates)
        forbidden["candidates"][0]["target_price"] = 100
        assert_invalid(SCHEMAS / "extraction_candidate_schema.json", forbidden, temp)

        nonfinite_text = json.dumps(candidates).replace("1200", "NaN", 1)
        nonfinite_path = temp / "nonfinite.json"
        nonfinite_path.write_text(nonfinite_text, encoding="utf-8")
        passed, errors, _ = validate_file(
            SCHEMAS / "extraction_candidate_schema.json", nonfinite_path
        )
        assert not passed
        assert errors

        wrong_enum = copy.deepcopy(candidates)
        wrong_enum["candidates"][0]["review_status"] = "approved"
        assert_invalid(SCHEMAS / "extraction_candidate_schema.json", wrong_enum, temp)

        blank = copy.deepcopy(candidates)
        blank["candidates"][0]["candidate_id"] = " "
        assert_invalid(SCHEMAS / "extraction_candidate_schema.json", blank, temp)

        review = read(review_file)
        no_approval = copy.deepcopy(review)
        no_approval["records"][0]["approved_value"] = "not_approved"
        assert_invalid(SCHEMAS / "review_batch_schema.json", no_approval, temp)

        real_promotion_manifest = read(promotion / "promotion_manifest.json")
        real_promotion_manifest["ticker"] = "MRVL"
        real_path = temp / "real-promotion.json"
        write(real_path, real_promotion_manifest)
        assert not validate_file(SCHEMAS / "promotion_manifest_schema.json", real_path)[0]

    print("PASS: schema validation valid packages and invalid required, forbidden, non-finite, enum, blank, approval-rule and real promotion schema cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
