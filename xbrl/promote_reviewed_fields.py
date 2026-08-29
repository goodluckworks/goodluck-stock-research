#!/usr/bin/env python3
"""Promote reviewed fictional candidates into an auditable local draft."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Sequence

from extraction_review_validator import validate_files
from mapping_review import validate_files as validate_mapping_review_files
from xbrl_common import (
    REAL_TICKERS,
    ensure_distinct_paths,
    prepare_output_dir,
    relative_or_absolute,
    utc_now,
    write_json,
)


OUTPUTS = (
    "approved_normalized_draft.json",
    "promotion_manifest.json",
    "promotion_report.md",
)


def run_promotion(
    review_file: Path,
    candidate_file: Path,
    manifest_file: Path,
    mapping_file: Path,
    mapping_review_file: Path,
    review_decision_log_file: Path,
    quality_score_file: Path,
    package_audit_reference: str,
    output_dir: Path,
    allow_real_company_promotion: bool = False,
    overwrite: bool = False,
) -> dict[str, Path]:
    """Promote approved fictional review records."""
    review_file = review_file.expanduser().resolve()
    candidate_file = candidate_file.expanduser().resolve()
    manifest_file = manifest_file.expanduser().resolve()
    mapping_file = mapping_file.expanduser().resolve()
    mapping_review_file = mapping_review_file.expanduser().resolve()
    review_decision_log_file = review_decision_log_file.expanduser().resolve()
    quality_score_file = quality_score_file.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    ensure_distinct_paths(
        review_file,
        candidate_file,
        manifest_file,
        mapping_file,
        mapping_review_file,
        review_decision_log_file,
        quality_score_file,
        output_dir,
    )
    if not str(package_audit_reference).strip():
        raise ValueError("package_audit_reference is required.")
    mapping, mapping_review, mapping_errors = validate_mapping_review_files(
        mapping_file, mapping_review_file
    )
    if mapping_errors:
        raise ValueError("Mapping review validation failed: " + "; ".join(mapping_errors))
    if mapping_review.get("mapping_status") != "approved":
        raise ValueError("Promotion requires approved mapping review.")
    review, candidate_doc, manifest, errors = validate_files(
        review_file, candidate_file, manifest_file
    )
    if errors:
        raise ValueError("Review validation failed: " + "; ".join(errors))
    if review.get("normalized_review_batch") is not True:
        raise ValueError("Promotion requires normalized_review_batch=true.")
    if review.get("decision_source") != "normalized_review_batch":
        raise ValueError("Promotion requires decision_source=normalized_review_batch.")
    if review.get("batch_status") != "approved":
        raise ValueError("Promotion requires review batch_status=approved.")
    decision_log = None
    if not review_decision_log_file.is_file():
        raise FileNotFoundError(f"Review decision log does not exist: {review_decision_log_file}")
    from xbrl_common import load_json

    decision_log = load_json(review_decision_log_file)
    if decision_log.get("review_batch_id") != review.get("review_batch_id"):
        raise ValueError("Review decision log does not match review batch.")
    quality_score = load_json(quality_score_file)
    if quality_score.get("quality_package_id") != review.get("quality_score_reference"):
        raise ValueError("Quality score file does not match review batch reference.")
    if quality_score.get("extraction_run_id") != manifest.get("run_id"):
        raise ValueError("Quality score extraction run does not match manifest.")
    if mapping_review.get("mapping_version") != manifest.get("mapping_version"):
        raise ValueError("Mapping review version does not match manifest.")
    if mapping.get("mapping_version") != manifest.get("mapping_version"):
        raise ValueError("Mapping file version does not match manifest.")
    ticker = str(review["ticker"]).upper()
    fictional = review.get("fictional_company") is True
    if ticker in REAL_TICKERS and not allow_real_company_promotion:
        raise ValueError(f"Real ticker promotion blocked by default: {ticker}")
    if not fictional and not allow_real_company_promotion:
        raise ValueError(
            "Promotion requires fictional_company=true unless explicit real-company override is used."
        )
    overwrite_used = prepare_output_dir(output_dir, overwrite)
    candidate_by_id = {
        item["candidate_id"]: item for item in candidate_doc["candidates"]
    }
    promoted: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    for record in review["records"]:
        decision = record["reviewer_decision"]
        candidate = candidate_by_id[record["candidate_id"]]
        if decision not in {"approve", "adjust"}:
            excluded.append(
                {
                    "candidate_id": record["candidate_id"],
                    "normalized_field": record["normalized_field"],
                    "decision": decision,
                }
            )
            continue
        if record["confidence"] == "low":
            raise ValueError("Low-confidence approval cannot be promoted.")
        promoted.append(
            {
                "normalized_field": record["normalized_field"],
                "approved_value": record["approved_value"],
                "approved_unit": record["approved_unit"],
                "period": record["period"],
                "candidate_id": record["candidate_id"],
                "review_record_id": record["review_record_id"],
                "reviewer_decision": decision,
                "approval_timestamp": record["approval_timestamp"],
                "source_tag": record["source_tag"],
                "source_locator": record["source_locator"],
                "transformation": record["transformation"],
                "confidence": record["confidence"],
            }
        )
        if candidate["normalized_field"] != record["normalized_field"]:
            raise ValueError("Candidate/review field mismatch during promotion.")

    if not promoted:
        raise ValueError("No approved or adjusted records are eligible for promotion.")
    promotion_id = (
        f"promotion-{ticker.lower()}-{manifest['reporting_period'].lower()}-"
        f"{manifest['snapshot_sha256'][:12]}"
    )
    paths = {name: output_dir / name for name in OUTPUTS}
    draft = {
        "status": "fictional_approved_normalized_draft",
        "promotion_id": promotion_id,
        "fictional_company": fictional,
        "company": review["company"],
        "ticker": ticker,
        "reporting_period": manifest["reporting_period"],
        "currency": manifest["currency"],
        "amount_unit": manifest["amount_unit"],
        "per_share_unit": manifest["per_share_unit"],
        "mapping_version": manifest["mapping_version"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "mapping_review_reference": relative_or_absolute(mapping_review_file),
        "review_decision_log_reference": relative_or_absolute(review_decision_log_file),
        "quality_score_reference": relative_or_absolute(quality_score_file),
        "package_audit_reference": package_audit_reference,
        "fields": promoted,
        "excluded_records": excluded,
        "limitations": [
            "Fictional fixture promotion only.",
            "Not a v0.2.x input file.",
            "No calculation or investment conclusion generated.",
        ],
    }
    promotion_manifest = {
        "promotion_id": promotion_id,
        "created_at": utc_now(),
        "generated_at": utc_now(),
        "review_file": relative_or_absolute(review_file),
        "candidate_file": relative_or_absolute(candidate_file),
        "extraction_manifest_file": relative_or_absolute(manifest_file),
        "extraction_run_id": manifest["run_id"],
        "review_batch_id": review["review_batch_id"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "mapping_version": manifest["mapping_version"],
        "mapping_review_reference": relative_or_absolute(mapping_review_file),
        "review_decision_log_reference": relative_or_absolute(review_decision_log_file),
        "quality_score_reference": relative_or_absolute(quality_score_file),
        "package_audit_reference": package_audit_reference,
        "ticker": ticker,
        "fictional_company": fictional,
        "allow_real_company_promotion_used": allow_real_company_promotion,
        "promoted_count": len(promoted),
        "excluded_count": len(excluded),
        "promoted_fields": promoted,
        "excluded_fields": excluded,
        "promotion_status": "fictional_draft_promoted",
        "overwrite_used": overwrite_used,
        "output_files": list(OUTPUTS),
    }
    report = f"""# Fictional Reviewed Field Promotion

## Summary

- Promotion ID: `{promotion_id}`
- Company: `{review['company']}`
- Ticker: `{ticker}`
- Fictional company: `{str(fictional).lower()}`
- Extraction run: `{manifest['run_id']}`
- Review batch: `{review['review_batch_id']}`
- Mapping version: `{manifest['mapping_version']}`
- Mapping review: `{relative_or_absolute(mapping_review_file)}`
- Review decision log: `{relative_or_absolute(review_decision_log_file)}`
- Quality score: `{relative_or_absolute(quality_score_file)}`
- Package audit reference: `{package_audit_reference}`
- Promoted fields: `{len(promoted)}`
- Excluded review records: `{len(excluded)}`
- Real-company override used: `{str(allow_real_company_promotion).lower()}`
- Overwrite used: `{str(overwrite_used).lower()}`

## Output Files

{chr(10).join(f"- `{name}`" for name in OUTPUTS)}

## Boundary

- Fictional approved normalized draft only.
- Existing v0.2.x inputs are not replaced.
- No calculation script is invoked.
- No investment conclusion is generated.
"""
    write_json(paths["approved_normalized_draft.json"], draft)
    write_json(paths["promotion_manifest.json"], promotion_manifest)
    paths["promotion_report.md"].write_text(report, encoding="utf-8")
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Promote validated review records into a fictional local draft."
    )
    parser.add_argument("--review-file", required=True, type=Path)
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--manifest-file", required=True, type=Path)
    parser.add_argument("--mapping-file", required=True, type=Path)
    parser.add_argument("--mapping-review-file", required=True, type=Path)
    parser.add_argument("--review-decision-log-file", required=True, type=Path)
    parser.add_argument("--quality-score-file", required=True, type=Path)
    parser.add_argument("--package-audit-reference", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--allow-real-company-promotion", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run_promotion(
            args.review_file,
            args.candidate_file,
            args.manifest_file,
            args.mapping_file,
            args.mapping_review_file,
            args.review_decision_log_file,
            args.quality_score_file,
            args.package_audit_reference,
            args.output_dir,
            args.allow_real_company_promotion,
            args.overwrite,
        )
    except (FileNotFoundError, FileExistsError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote fictional promotion package: {args.output_dir}")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
