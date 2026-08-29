#!/usr/bin/env python3
"""Partial-field sandbox policy tests."""

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

from generate_normalized_csv_sandbox import run_generator  # noqa: E402
from run_v02_sandbox_dry_run import run_dry_run  # noqa: E402


EXMP_PROMOTION = ROOT / "examples" / "xbrl_promotion_runs" / "EXMP"
EXMP_REVIEW = ROOT / "examples" / "xbrl_review_decisions" / "EXMP" / "normalized_review_batch.json"
EXMP_CANDIDATES = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP" / "extraction_candidates.json"
EXMP_MANIFEST = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP" / "extraction_run_manifest.json"


def read_json(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write_json(path: Path, value: object) -> None:
    """Write JSON object."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def copy_inputs(root: Path) -> tuple[Path, Path, Path, Path]:
    """Copy EXMP source packages to a temporary root."""
    promotion = root / "promotion"
    shutil.copytree(EXMP_PROMOTION, promotion)
    review = root / "review.json"
    candidates = root / "candidates.json"
    manifest = root / "manifest.json"
    shutil.copy2(EXMP_REVIEW, review)
    shutil.copy2(EXMP_CANDIDATES, candidates)
    shutil.copy2(EXMP_MANIFEST, manifest)
    return promotion, review, candidates, manifest


def csv_row(path: Path) -> dict[str, str]:
    """Read first CSV row."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    return rows[0]


def approve_existing_field(root: Path, field: str, value: float) -> None:
    """Move an existing candidate/review field into promoted fields."""
    promotion = read_json(root / "promotion" / "approved_normalized_draft.json")
    review = read_json(root / "review.json")
    candidates = read_json(root / "candidates.json")
    candidate = next(item for item in candidates["candidates"] if item["normalized_field"] == field)
    review_record = next(item for item in review["records"] if item["normalized_field"] == field)
    review_record["reviewer_decision"] = "approve"
    review_record["approved_value"] = value
    review_record["approved_unit"] = candidate["unit"]
    review_record["approval_readiness"] = "ready"
    review_record["reviewer_notes"] = "Fictional partial-field test approval."
    review_record["review_quality"]["approval_readiness"] = "ready"
    review_record["review_quality"]["blocking_issues"] = []
    promotion["excluded_records"] = [
        item for item in promotion["excluded_records"] if item.get("normalized_field") != field
    ]
    promotion["fields"].append(
        {
            "normalized_field": field,
            "candidate_id": candidate["candidate_id"],
            "review_record_id": review_record["review_record_id"],
            "reviewer_decision": "approve",
            "approved_value": value,
            "approved_unit": candidate["unit"],
            "transformation": candidate["transformation"],
            "period": candidate["period"],
            "confidence": "medium",
            "source_tag": review_record["source_tag"],
            "source_locator": review_record["source_locator"],
        }
    )
    write_json(root / "review.json", review)
    write_json(root / "promotion" / "approved_normalized_draft.json", promotion)


def expect_failure(input_csv: Path, output_dir: Path, expected: str) -> None:
    """Assert dry-run failure includes expected text."""
    try:
        run_dry_run(input_csv, output_dir)
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        assert expected in str(exc), str(exc)
    else:
        raise AssertionError(f"Expected failure containing {expected!r}")


def main() -> int:
    """Run partial-field tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-partial-field-tests-") as temp_name:
        temp = Path(temp_name)
        full_root = temp / "full-ish"
        promotion, review, candidates, manifest = copy_inputs(full_root)
        for field, value in (("net_income", 210.0), ("total_debt", 190.0), ("diluted_shares", 100.0)):
            approve_existing_field(full_root, field, value)
        run_generator(promotion, review, candidates, manifest, full_root / "normalized")
        full_manifest = read_json(full_root / "normalized" / "normalized_csv_manifest.json")
        assert "raw_net_margin" in full_manifest["downstream_impact"]["available_ratios"]
        assert "net_debt" in full_manifest["downstream_impact"]["available_ratios"]
        assert csv_row(full_root / "normalized" / "normalized_financials_sandbox.csv")["net_income"] == "210.0"

        partial_root = temp / "partial"
        promotion, review, candidates, manifest = copy_inputs(partial_root)
        run_generator(promotion, review, candidates, manifest, partial_root / "normalized")
        partial_manifest = read_json(partial_root / "normalized" / "normalized_csv_manifest.json")
        partial_row = csv_row(partial_root / "normalized" / "normalized_financials_sandbox.csv")
        assert partial_manifest["downstream_impact"]["ratio_dry_run_allowed"] is True
        assert partial_row["net_income"] == ""
        assert partial_row["net_income"] != "0"
        assert "net_income" in partial_manifest["omitted_fields"]
        assert "total_debt" in partial_manifest["unresolved_fields"]
        unavailable = {
            item["ratio"]: item["missing_inputs"]
            for item in partial_manifest["downstream_impact"]["unavailable_ratios"]
        }
        assert unavailable["raw_net_margin"] == ["net_income"]
        assert "gross_margin" in partial_manifest["downstream_impact"]["available_ratios"]
        run_dry_run(
            partial_root / "normalized" / "normalized_financials_sandbox.csv",
            partial_root / "dry-run",
        )
        report = (partial_root / "dry-run" / "ratio_output_sandbox.md").read_text(encoding="utf-8")
        assert "Partial-field caution" in report
        assert "Unavailable ratios" in report
        assert "raw_net_margin" in report

        blocked_root = temp / "missing-minimum"
        shutil.copytree(partial_root / "normalized", blocked_root)
        rows = [csv_row(blocked_root / "normalized_financials_sandbox.csv")]
        rows[0]["revenue"] = ""
        with (blocked_root / "normalized_financials_sandbox.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        manifest_doc = read_json(blocked_root / "normalized_csv_manifest.json")
        manifest_doc["downstream_impact"]["ratio_dry_run_allowed"] = False
        manifest_doc["downstream_impact"]["missing_minimum_fields"] = ["revenue"]
        write_json(blocked_root / "normalized_csv_manifest.json", manifest_doc)
        expect_failure(blocked_root / "normalized_financials_sandbox.csv", temp / "blocked-dry-run", "minimum ratio")

    print("PASS: full-ish and partial EXMP sandbox handling, no zero-fill, downstream impact and dry-run missing-minimum block")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
