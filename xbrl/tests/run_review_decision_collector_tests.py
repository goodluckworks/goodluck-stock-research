#!/usr/bin/env python3
"""Review decision collector tests."""

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

from review_decision_collector import run_collector  # noqa: E402
from review_quality_scorer import run_scorer  # noqa: E402
from reviewer_workbench import run_workbench  # noqa: E402


EXMP = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP"


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write(path: Path, value: object) -> None:
    """Write JSON."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def expect_failure(decision: dict[str, object], temp: Path, quality_file: Path, text: str) -> None:
    """Write a bad decision file and assert collector failure."""
    target = temp / f"bad-{text.replace(' ', '-')}.json"
    write(target, decision)
    try:
        run_collector(
            target,
            EXMP / "extraction_candidates.json",
            EXMP / "extraction_run_manifest.json",
            quality_file,
            temp / f"out-{text.replace(' ', '-')}",
        )
    except ValueError as exc:
        assert text in str(exc), str(exc)
    else:
        raise AssertionError(f"Expected collector failure containing {text!r}")


def main() -> int:
    """Run collector tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-review-collector-tests-") as temp_name:
        temp = Path(temp_name)
        workbench = temp / "workbench"
        quality = temp / "quality"
        run_workbench(
            EXMP / "extraction_candidates.json",
            EXMP / "extraction_run_manifest.json",
            EXMP / "field_provenance.json",
            workbench / "review_workbench.md",
            workbench / "review_decision_template.json",
        )
        run_scorer(
            EXMP / "extraction_candidates.json",
            EXMP / "extraction_run_manifest.json",
            EXMP / "field_provenance.json",
            quality,
        )
        quality_file = quality / "review_quality_score.json"
        template = read(workbench / "review_decision_template.json")
        paths = run_collector(
            workbench / "review_decision_template.json",
            EXMP / "extraction_candidates.json",
            EXMP / "extraction_run_manifest.json",
            quality_file,
            temp / "valid",
        )
        assert set(paths) == {
            "normalized_review_batch.json",
            "review_decision_log.json",
            "review_collection_report.md",
        }
        batch = read(temp / "valid" / "normalized_review_batch.json")
        assert batch["normalized_review_batch"] is True
        assert batch["decision_source"] == "normalized_review_batch"

        no_notes = copy.deepcopy(template)
        first_approve = next(record for record in no_notes["records"] if record["reviewer_decision"] == "approve")
        first_approve["reviewer_notes"] = ""
        expect_failure(no_notes, temp, quality_file, "requires reviewer_notes")

        no_adjust_value = copy.deepcopy(template)
        first_adjust = next(record for record in no_adjust_value["records"] if record["reviewer_decision"] == "adjust")
        first_adjust["approved_value"] = "not_approved"
        expect_failure(no_adjust_value, temp, quality_file, "requires approved_value")

        bad_candidate = copy.deepcopy(template)
        bad_candidate["records"][0]["candidate_id"] = "missing-candidate"
        expect_failure(bad_candidate, temp, quality_file, "candidate_id not found")

        bad_snapshot = copy.deepcopy(template)
        bad_snapshot["snapshot_sha256"] = "0" * 64
        expect_failure(bad_snapshot, temp, quality_file, "snapshot_sha256 does not match")

        bad_mapping = copy.deepcopy(template)
        bad_mapping["mapping_version"] = "wrong"
        expect_failure(bad_mapping, temp, quality_file, "mapping_version does not match")

        missing_checklist = copy.deepcopy(template)
        first_approve = next(record for record in missing_checklist["records"] if record["reviewer_decision"] == "approve")
        del first_approve["review_checklist"]
        expect_failure(missing_checklist, temp, quality_file, "missing review_checklist")

        relationship_false = copy.deepcopy(template)
        first_approve = next(record for record in relationship_false["records"] if record["reviewer_decision"] == "approve")
        first_approve["review_checklist"]["relationship_checked"] = False
        expect_failure(relationship_false, temp, quality_file, "relationship_checked false fails approve")

        bad_quality = read(quality_file)
        first_approve_id = next(record["candidate_id"] for record in template["records"] if record["reviewer_decision"] == "approve")
        for record in bad_quality["records"]:
            if record["candidate_id"] == first_approve_id:
                record["approval_readiness"] = "not_ready"
        bad_quality_path = temp / "bad-quality.json"
        write(bad_quality_path, bad_quality)
        expect_failure(template, temp, bad_quality_path, "quality score not_ready fails approve")

        blocked_quality = read(quality_file)
        for record in blocked_quality["records"]:
            if record["candidate_id"] == first_approve_id:
                record["blocking_issues"] = ["test_block"]
        blocked_quality_path = temp / "blocked-quality.json"
        write(blocked_quality_path, blocked_quality)
        expect_failure(template, temp, blocked_quality_path, "blocking issue fails approve")

        low_confidence = copy.deepcopy(template)
        candidates = read(EXMP / "extraction_candidates.json")
        approved_id = next(record["candidate_id"] for record in low_confidence["records"] if record["reviewer_decision"] == "approve")
        for candidate in candidates["candidates"]:
            if candidate["candidate_id"] == approved_id:
                candidate["confidence"] = "low"
        candidate_path = temp / "low-candidates.json"
        write(candidate_path, candidates)
        decision_path = temp / "low-decision.json"
        write(decision_path, low_confidence)
        try:
            run_collector(
                decision_path,
                candidate_path,
                EXMP / "extraction_run_manifest.json",
                quality_file,
                temp / "low-out",
            )
        except ValueError as exc:
            assert "low confidence cannot be approved" in str(exc)
        else:
            raise AssertionError("Expected low confidence approve failure.")

    print("PASS: review decision collector valid normalization and invalid notes, adjust, candidate, snapshot, mapping and low-confidence cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
