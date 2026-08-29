#!/usr/bin/env python3
"""Taxonomy relationship metadata tests for v0.3.7."""

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

from mapping_review import validate_files as validate_mapping_review_files  # noqa: E402
from review_quality_scorer import run_scorer  # noqa: E402


MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"
MAPPING_REVIEW = XBRL_DIR / "mapping_review_fixtures" / "mapping_review_approved_v0_3_7.json"
EXMP = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP"


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write(path: Path, value: object) -> None:
    """Write JSON."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    """Run taxonomy relationship tests."""
    mapping = read(MAPPING)
    records = mapping["records"]
    assert isinstance(records, list) and records
    for record in records:
        relationship = record.get("relationship_metadata")
        assert isinstance(relationship, dict), record.get("mapping_id")
        for field in (
            "concept_label",
            "concept_type",
            "taxonomy_namespace",
            "closest_standard_concept",
            "presentation_parent",
            "calculation_parent",
            "anchor_concept",
            "relationship_basis",
            "relationship_confidence",
            "relationship_review_status",
            "relationship_evidence_notes",
        ):
            assert relationship.get(field), (record.get("mapping_id"), field)

    revenue = next(record for record in records if record["normalized_field"] == "revenue")
    assert revenue["relationship_metadata"]["concept_type"] == "standard"
    assert revenue["relationship_metadata"]["relationship_confidence"] == "high"

    total_debt = next(record for record in records if record["normalized_field"] == "total_debt")
    assert total_debt["relationship_metadata"]["concept_type"] in {"standard", "fixture_local"}
    assert total_debt["relationship_metadata"]["anchor_concept"].startswith("us-gaap:")

    _mapping, _mapping_review, errors = validate_mapping_review_files(MAPPING, MAPPING_REVIEW)
    assert not errors, errors

    with tempfile.TemporaryDirectory(prefix="xbrl-taxonomy-relationship-tests-") as temp_name:
        temp = Path(temp_name)
        candidates = read(EXMP / "extraction_candidates.json")
        bad = copy.deepcopy(candidates)
        bad["candidates"][0]["taxonomy_relationship"] = {
            "relationship_review_status": "unsupported",
            "relationship_confidence": "low",
        }
        bad_path = temp / "bad-candidates.json"
        write(bad_path, bad)
        quality_dir = temp / "quality"
        run_scorer(
            bad_path,
            EXMP / "extraction_run_manifest.json",
            EXMP / "field_provenance.json",
            quality_dir,
        )
        quality = read(quality_dir / "review_quality_score.json")
        first = quality["records"][0]
        assert first["approval_readiness"] == "not_ready"
        assert "weak_relationship_evidence" in first["blocking_issues"]

    print("PASS: taxonomy relationship metadata, approved mapping relationship review and unsupported relationship readiness block")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
