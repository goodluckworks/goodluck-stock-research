#!/usr/bin/env python3
"""Fictional normalized CSV sandbox tests."""

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


def read_first_csv_row(path: Path) -> dict[str, str]:
    """Read first CSV row."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    return rows[0]


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


def expect_failure(args: tuple[Path, Path, Path, Path, Path], expected: str) -> None:
    """Assert generator failure includes expected text."""
    try:
        run_generator(*args)
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        assert expected in str(exc), str(exc)
    else:
        raise AssertionError(f"Expected generator failure containing {expected!r}")


def poison_ticker(path: Path, ticker: str) -> None:
    """Set ticker and fictional flag in a JSON object."""
    doc = read_json(path)
    doc["ticker"] = ticker
    doc["company"] = f"{ticker} real-company block fixture"
    doc["fictional_company"] = False
    write_json(path, doc)


def main() -> int:
    """Run normalized CSV sandbox tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-normalized-csv-tests-") as temp_name:
        temp = Path(temp_name)
        promotion, review, candidates, manifest = copy_inputs(temp)
        output = temp / "normalized"
        paths = run_generator(promotion, review, candidates, manifest, output)

        assert set(paths) == {
            "normalized_financials_sandbox.csv",
            "normalized_csv_audit.json",
            "normalized_csv_manifest.json",
            "normalized_csv_report.md",
        }
        assert all(path.is_file() and path.stat().st_size > 0 for path in paths.values())

        csv_manifest = read_json(output / "normalized_csv_manifest.json")
        csv_audit = read_json(output / "normalized_csv_audit.json")
        row = read_first_csv_row(output / "normalized_financials_sandbox.csv")
        assert csv_manifest["ticker"] == "EXMP"
        assert csv_manifest["prohibited_real_company_flag"] is False
        assert csv_manifest["no_investment_conclusion"] is True
        for field in (
            "fictional",
            "not_investment_data",
            "not_company_fact",
            "not_for_trading",
            "not_production_research",
        ):
            assert row[field] == "true"
        populated = set(csv_manifest["populated_fields"])
        assert populated == {
            "revenue",
            "gross_profit",
            "operating_income",
            "operating_cash_flow",
            "capital_expenditure",
            "cash_and_equivalents",
        }
        for field in populated:
            assert row[field]
        assert "total_debt" in csv_manifest["unresolved_fields"]
        for field in ("net_income", "total_assets", "shares_diluted"):
            assert field in csv_manifest["omitted_fields"]
            assert row.get(field, "") == ""
        assert csv_manifest["downstream_impact"]["ratio_dry_run_allowed"] is True
        assert "gross_margin" in csv_manifest["downstream_impact"]["available_ratios"]
        unavailable = {
            item["ratio"]: item["missing_inputs"]
            for item in csv_manifest["downstream_impact"]["unavailable_ratios"]
        }
        assert unavailable["raw_net_margin"] == ["net_income"]
        audit_records = csv_audit["field_audit_records"]
        assert len(audit_records) == len(populated)
        for record in audit_records:
            assert record["normalized_field"] in populated
            assert record["candidate_id"]
            assert record["review_record_id"]
            assert record["reviewer_decision"] in {"approve", "adjust"}
            assert record["transformation"]
            assert record["provenance_reference"]

        for ticker in ("MRVL", "NVDA", "AVGO"):
            real_root = temp / ticker
            real_promotion, real_review, real_candidates, real_manifest = copy_inputs(real_root)
            poison_ticker(real_promotion / "promotion_manifest.json", ticker)
            poison_ticker(real_promotion / "approved_normalized_draft.json", ticker)
            expect_failure(
                (real_promotion, real_review, real_candidates, real_manifest, real_root / "out"),
                "allows only EXMP",
            )

        missing_root = temp / "missing-manifest"
        missing_promotion, missing_review, missing_candidates, missing_manifest = copy_inputs(missing_root)
        (missing_promotion / "promotion_manifest.json").unlink()
        expect_failure(
            (missing_promotion, missing_review, missing_candidates, missing_manifest, missing_root / "out"),
            "Input file does not exist",
        )

        mapping_root = temp / "mapping-mismatch"
        mapping_promotion, mapping_review, mapping_candidates, mapping_manifest = copy_inputs(mapping_root)
        review_doc = read_json(mapping_review)
        review_doc["mapping_version"] = "wrong-mapping"
        write_json(mapping_review, review_doc)
        expect_failure(
            (mapping_promotion, mapping_review, mapping_candidates, mapping_manifest, mapping_root / "out"),
            "mapping_version",
        )

        snapshot_root = temp / "snapshot-mismatch"
        snapshot_promotion, snapshot_review, snapshot_candidates, snapshot_manifest = copy_inputs(snapshot_root)
        manifest_doc = read_json(snapshot_manifest)
        manifest_doc["snapshot_sha256"] = "0" * 64
        write_json(snapshot_manifest, manifest_doc)
        expect_failure(
            (snapshot_promotion, snapshot_review, snapshot_candidates, snapshot_manifest, snapshot_root / "out"),
            "snapshot_sha256",
        )

        poisoned_root = temp / "conclusion-field"
        poisoned_promotion, poisoned_review, poisoned_candidates, poisoned_manifest = copy_inputs(poisoned_root)
        poisoned_doc = read_json(poisoned_promotion / "approved_normalized_draft.json")
        poisoned_doc["recommendation"] = "buy"
        write_json(poisoned_promotion / "approved_normalized_draft.json", poisoned_doc)
        expect_failure(
            (poisoned_promotion, poisoned_review, poisoned_candidates, poisoned_manifest, poisoned_root / "out"),
            "forbidden conclusion/trading fields",
        )

    print("PASS: normalized CSV sandbox EXMP generation, auditability, unresolved handling, real-ticker blocks and negative validations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
