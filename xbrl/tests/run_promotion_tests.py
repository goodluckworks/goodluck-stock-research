#!/usr/bin/env python3
"""Fictional promotion and real-company blocking tests."""

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

from promote_reviewed_fields import run_promotion  # noqa: E402
from review_decision_collector import run_collector  # noqa: E402
from review_quality_scorer import run_scorer  # noqa: E402
from reviewer_workbench import run_workbench  # noqa: E402


EXAMPLE = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP"
MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"
MAPPING_REVIEW = XBRL_DIR / "mapping_review_fixtures" / "mapping_review_approved_v0_3_7.json"


def read(path: Path) -> dict[str, object]:
    """Read JSON."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write(path: Path, value: object) -> None:
    """Write temporary JSON."""
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def normalized_review_package(root: Path, extraction_dir: Path) -> tuple[Path, Path]:
    """Generate a normalized review package from the workbench template."""
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
    """Run promotion tests."""
    candidate_path = EXAMPLE / "extraction_candidates.json"
    manifest_path = EXAMPLE / "extraction_run_manifest.json"
    with tempfile.TemporaryDirectory(prefix="xbrl-promotion-tests-") as temp:
        root = Path(temp)
        output = root / "EXMP"
        review_dir, quality_dir = normalized_review_package(root, EXAMPLE)
        review_file = review_dir / "normalized_review_batch.json"
        decision_log = review_dir / "review_decision_log.json"
        quality_file = quality_dir / "review_quality_score.json"
        paths = run_promotion(
            review_file,
            candidate_path,
            manifest_path,
            MAPPING,
            MAPPING_REVIEW,
            decision_log,
            quality_file,
            "test-package-audit-reference",
            output,
        )
        assert set(paths) == {
            "approved_normalized_draft.json",
            "promotion_manifest.json",
            "promotion_report.md",
        }
        assert all(path.is_file() and path.stat().st_size > 0 for path in paths.values())
        draft = read(output / "approved_normalized_draft.json")
        promotion = read(output / "promotion_manifest.json")
        decisions = {item["reviewer_decision"] for item in draft["fields"]}
        assert decisions == {"approve", "adjust"}
        assert {item["decision"] for item in draft["excluded_records"]} == {
            "reject",
            "unresolved",
            "needs_more_evidence",
        }
        assert all(
            item.get("candidate_id") and item.get("review_record_id")
            for item in draft["fields"]
        )
        assert promotion["fictional_company"] is True
        assert promotion["allow_real_company_promotion_used"] is False

        review = read(review_file)
        candidates = read(candidate_path)
        manifest = read(manifest_path)
        review["ticker"] = "MRVL"
        review["company"] = "Marvell Technology, Inc."
        review["fictional_company"] = False
        manifest["ticker"] = "MRVL"
        manifest["company"] = "Marvell Technology, Inc."
        manifest["cik"] = "0001835632"
        manifest["accession"] = "fictional-mrvl-block-test"
        for record in review["records"]:
            record["ticker"] = "MRVL"
            record["company"] = "Marvell Technology, Inc."
            record["cik"] = "0001835632"
            record["accession"] = "fictional-mrvl-block-test"
        review_path = root / "mrvl-review.json"
        decision_log_doc = read(decision_log)
        decision_log_doc["review_batch_id"] = review["review_batch_id"]
        decision_log_path = root / "mrvl-decision-log.json"
        candidate_copy = root / "mrvl-candidates.json"
        manifest_copy = root / "mrvl-manifest.json"
        write(review_path, review)
        write(decision_log_path, decision_log_doc)
        write(candidate_copy, candidates)
        write(manifest_copy, manifest)
        try:
            run_promotion(
                review_path,
                candidate_copy,
                manifest_copy,
                MAPPING,
                MAPPING_REVIEW,
                decision_log_path,
                quality_file,
                "test-package-audit-reference",
                root / "MRVL",
            )
        except ValueError as exc:
            assert "blocked by default" in str(exc)
        else:
            raise AssertionError("MRVL promotion should be blocked by default.")

        source = (XBRL_DIR / "promote_reviewed_fields.py").read_text(
            encoding="utf-8"
        )
        assert "subprocess" not in source
        for script_name in (
            "ratio_calculator",
            "dcf_sensitivity",
            "peer_comps_table",
            "implied_expectations",
        ):
            assert script_name not in source
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in paths.values()
        ).lower()
        for forbidden in (
            "target price",
            "buy:",
            "sell:",
            "hold:",
            "position size",
            "research status",
        ):
            assert forbidden not in combined

    print("PASS: fictional approve/adjust promotion, exclusion audit, real-ticker block, output and no-calculation tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
