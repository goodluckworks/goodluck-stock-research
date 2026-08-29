#!/usr/bin/env python3
"""Review-gate tests for v0.3.4."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
ROOT = XBRL_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from extraction_review_validator import validate_review_documents  # noqa: E402


EXAMPLE = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP"
REVIEWS = XBRL_DIR / "review_fixtures"


def read(path: Path) -> dict[str, object]:
    """Read JSON."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def errors_for(
    review: dict[str, object],
    candidates: dict[str, object],
    manifest: dict[str, object],
) -> list[str]:
    """Validate copied documents."""
    return validate_review_documents(review, candidates, manifest)


def main() -> int:
    """Run review-gate tests."""
    candidates = read(EXAMPLE / "extraction_candidates.json")
    manifest = read(EXAMPLE / "extraction_run_manifest.json")
    approved = read(REVIEWS / "exmp_review_approved.json")
    adjusted = read(REVIEWS / "exmp_review_adjusted.json")
    rejected = read(REVIEWS / "exmp_review_rejected.json")
    unresolved = read(REVIEWS / "exmp_review_unresolved.json")
    invalid = read(REVIEWS / "invalid_review_missing_approval.json")

    assert not errors_for(approved, candidates, manifest)
    assert not errors_for(adjusted, candidates, manifest)
    assert not errors_for(rejected, candidates, manifest)
    assert not errors_for(unresolved, candidates, manifest)
    assert errors_for(invalid, candidates, manifest)

    medium_review = copy.deepcopy(approved)
    medium_review["records"] = [copy.deepcopy(approved["records"][0])]
    medium_candidates = copy.deepcopy(candidates)
    revenue = next(
        item
        for item in medium_candidates["candidates"]
        if item["candidate_id"] == "exmp-revenue-candidate-001"
    )
    revenue["confidence"] = "medium"
    medium_review["records"][0]["confidence"] = "medium"
    assert not errors_for(medium_review, medium_candidates, manifest)

    low_review = copy.deepcopy(medium_review)
    low_candidates = copy.deepcopy(medium_candidates)
    low_review["records"][0]["confidence"] = "low"
    next(
        item
        for item in low_candidates["candidates"]
        if item["candidate_id"] == "exmp-revenue-candidate-001"
    )["confidence"] = "low"
    assert any(
        "low confidence cannot be approved" in error
        for error in errors_for(low_review, low_candidates, manifest)
    )

    mapping_mismatch = copy.deepcopy(approved)
    mapping_mismatch["mapping_version"] = "wrong-version"
    assert any(
        "mapping_version does not match" in error
        for error in errors_for(mapping_mismatch, candidates, manifest)
    )

    checksum_mismatch = copy.deepcopy(approved)
    checksum_mismatch["snapshot_sha256"] = "0" * 64
    assert any(
        "snapshot_sha256 does not match" in error
        for error in errors_for(checksum_mismatch, candidates, manifest)
    )

    company_mismatch = copy.deepcopy(approved)
    company_mismatch["company"] = "Wrong Company"
    assert any(
        "Review company does not match" in error
        for error in errors_for(company_mismatch, candidates, manifest)
    )

    unit_mismatch = copy.deepcopy(approved)
    unit_mismatch["records"] = [copy.deepcopy(approved["records"][0])]
    unit_mismatch["records"][0]["approved_unit"] = "USD"
    assert any(
        "approve must retain the candidate unit" in error
        for error in errors_for(unit_mismatch, candidates, manifest)
    )

    bad_reject = copy.deepcopy(rejected)
    bad_reject["records"][0]["approved_value"] = 240
    assert any(
        "reject requires not_approved" in error
        for error in errors_for(bad_reject, candidates, manifest)
    )

    bad_unresolved = copy.deepcopy(unresolved)
    bad_unresolved["records"][0]["approved_value"] = 260
    assert any(
        "unresolved requires not_approved" in error
        for error in errors_for(bad_unresolved, candidates, manifest)
    )

    print("PASS: review approve, adjust, reject, unresolved, missing approval, low confidence, identity, unit, mapping and checksum tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
