#!/usr/bin/env python3
"""Mapping review workflow tests."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from mapping_review import validate_files, write_artifacts  # noqa: E402


MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"
FIXTURES = XBRL_DIR / "mapping_review_fixtures"


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write(path: Path, value: object) -> None:
    """Write JSON."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    """Run mapping review tests."""
    _mapping, _review, errors = validate_files(MAPPING, FIXTURES / "mapping_review_approved_v0_3_7.json")
    assert not errors
    _mapping, _review, errors = validate_files(MAPPING, FIXTURES / "invalid_mapping_review_missing_evidence_v0_3_7.json")
    assert errors and any("evidence_notes" in error for error in errors)
    _mapping, _review, errors = validate_files(MAPPING, FIXTURES / "mapping_review_rejected_v0_3_7.json")
    assert errors and any("mapping_status=rejected" in error for error in errors)
    _mapping, _review, errors = validate_files(MAPPING, FIXTURES / "mapping_review_superseded_v0_3_7.json")
    assert errors and any("mapping_status=superseded" in error for error in errors)

    approved = read(FIXTURES / "mapping_review_approved_v0_3_7.json")
    with tempfile.TemporaryDirectory(prefix="xbrl-mapping-review-tests-") as temp_name:
        temp = Path(temp_name)
        paths = write_artifacts(MAPPING, FIXTURES / "mapping_review_approved_v0_3_7.json", temp / "artifacts")
        assert set(paths) == {
            "mapping_review_batch.json",
            "mapping_review_report.md",
            "mapping_decision_log.json",
        }
        assert all(path.is_file() and path.stat().st_size > 0 for path in paths.values())

        mismatch = copy.deepcopy(approved)
        mismatch["records"][0]["mapping_id"] = "does-not-exist"
        mismatch_path = temp / "mismatch.json"
        write(mismatch_path, mismatch)
        _mapping, _review, errors = validate_files(MAPPING, mismatch_path)
        assert errors and any("mapping_id does not exist" in error for error in errors)

        invalid_decision = copy.deepcopy(approved)
        invalid_decision["records"][0]["reviewer_decision"] = "approve_without_review"
        invalid_path = temp / "invalid-decision.json"
        write(invalid_path, invalid_decision)
        _mapping, _review, errors = validate_files(MAPPING, invalid_path)
        assert errors and any("invalid reviewer_decision" in error for error in errors)

    print("PASS: mapping review approved, artifacts, missing evidence, rejected, superseded, mapping mismatch and decision enum tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
