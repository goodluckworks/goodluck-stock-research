#!/usr/bin/env python3
"""Audit consistency across extraction, review and promotion packages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from mapping_review import validate_files as validate_mapping_review_files
from xbrl_common import REAL_TICKERS, ensure_distinct_paths, load_json, relative_or_absolute, utc_now


FORBIDDEN_FIELDS = {
    "target_price",
    "recommendation",
    "buy",
    "sell",
    "hold",
    "position_size",
    "research_status",
}


def find_forbidden(value: Any, path: str = "$") -> list[str]:
    """Return forbidden field locations in a JSON-compatible value."""
    hits: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_FIELDS:
                hits.append(f"{path}.{key}")
            hits.extend(find_forbidden(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            hits.extend(find_forbidden(child, f"{path}[{index}]"))
    return hits


def load_extraction(extraction_dir: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Load an extraction package."""
    return (
        load_json(extraction_dir / "extraction_run_manifest.json"),
        load_json(extraction_dir / "extraction_candidates.json"),
        load_json(extraction_dir / "field_provenance.json"),
        load_json(extraction_dir / "unresolved_fields.json"),
    )


def audit_package(
    extraction_dir: Path,
    review_file: Path | None = None,
    promotion_dir: Path | None = None,
    mapping_file: Path | None = None,
    mapping_review_file: Path | None = None,
    review_decision_log_file: Path | None = None,
    quality_score_file: Path | None = None,
    allow_real_company_promotion: bool = False,
) -> list[str]:
    """Return audit errors."""
    errors: list[str] = []
    manifest, candidates_doc, provenance_doc, unresolved_doc = load_extraction(extraction_dir)
    docs: list[tuple[str, dict[str, Any]]] = [
        ("manifest", manifest),
        ("candidates", candidates_doc),
        ("provenance", provenance_doc),
        ("unresolved", unresolved_doc),
    ]
    for name, doc in docs:
        for hit in find_forbidden(doc):
            errors.append(f"{name}: forbidden conclusion/trading field present at {hit}.")

    run_id = manifest.get("run_id")
    snapshot = manifest.get("snapshot_sha256")
    mapping_version = manifest.get("mapping_version")
    if candidates_doc.get("run_id") != run_id:
        errors.append("candidate package extraction_run_id mismatch.")
    if provenance_doc.get("run_id") != run_id:
        errors.append("provenance package extraction_run_id mismatch.")
    if candidates_doc.get("snapshot_sha256") != snapshot:
        errors.append("candidate package snapshot mismatch.")
    if provenance_doc.get("snapshot_sha256") != snapshot:
        errors.append("provenance package snapshot mismatch.")
    if candidates_doc.get("mapping_version") != mapping_version:
        errors.append("candidate package mapping version mismatch.")
    if provenance_doc.get("mapping_version") != mapping_version:
        errors.append("provenance package mapping version mismatch.")

    candidates = candidates_doc.get("candidates", [])
    provenance = provenance_doc.get("records", [])
    if not isinstance(candidates, list):
        errors.append("candidates must be an array.")
        candidates = []
    if not isinstance(provenance, list):
        errors.append("provenance records must be an array.")
        provenance = []
    candidate_by_id = {
        item.get("candidate_id"): item for item in candidates if isinstance(item, dict)
    }
    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        if not isinstance(candidate.get("taxonomy_relationship"), dict):
            errors.append(f"candidate missing taxonomy relationship metadata: {candidate.get('candidate_id')}.")
        if not isinstance(candidate.get("review_checklist"), dict):
            errors.append(f"candidate missing review checklist: {candidate.get('candidate_id')}.")
    provenance_ids = {
        item.get("candidate_id") for item in provenance if isinstance(item, dict)
    }
    if set(candidate_by_id) != provenance_ids:
        errors.append("candidate/provenance candidate_id sets differ.")

    review: dict[str, Any] | None = None
    review_by_candidate: dict[str, dict[str, Any]] = {}
    if review_file is not None:
        review = load_json(review_file)
        docs.append(("review", review))
        for hit in find_forbidden(review):
            errors.append(f"review: forbidden conclusion/trading field present at {hit}.")
        if review.get("extraction_run_id") != run_id:
            errors.append("review extraction_run_id mismatch.")
        if review.get("snapshot_sha256") != snapshot:
            errors.append("review snapshot mismatch.")
        if review.get("mapping_version") != mapping_version:
            errors.append("review mapping version mismatch.")
        if promotion_dir is not None:
            if review.get("normalized_review_batch") is not True:
                errors.append("promotion audit requires normalized review batch.")
            if review.get("decision_source") != "normalized_review_batch":
                errors.append("promotion audit requires normalized review batch source.")
            if review.get("batch_status") != "approved":
                errors.append("promotion audit requires approved review batch.")
        records = review.get("records", [])
        if not isinstance(records, list):
            errors.append("review records must be an array.")
            records = []
        for record in records:
            if not isinstance(record, dict):
                errors.append("review record must be an object.")
                continue
            candidate_id = record.get("candidate_id")
            if candidate_id not in candidate_by_id:
                errors.append(f"review candidate_id does not exist: {candidate_id}.")
                continue
            review_by_candidate[str(candidate_id)] = record

    if promotion_dir is not None:
        promotion_manifest = load_json(promotion_dir / "promotion_manifest.json")
        draft = load_json(promotion_dir / "approved_normalized_draft.json")
        for name, doc in (("promotion_manifest", promotion_manifest), ("approved_draft", draft)):
            for hit in find_forbidden(doc):
                errors.append(f"{name}: forbidden conclusion/trading field present at {hit}.")
        if promotion_manifest.get("extraction_run_id") != run_id:
            errors.append("promotion extraction_run_id mismatch.")
        if promotion_manifest.get("snapshot_sha256") != snapshot:
            errors.append("promotion snapshot mismatch.")
        if promotion_manifest.get("mapping_version") != mapping_version:
            errors.append("promotion mapping version mismatch.")
        for required_ref in (
            "mapping_review_reference",
            "review_decision_log_reference",
            "quality_score_reference",
            "package_audit_reference",
        ):
            if not str(promotion_manifest.get(required_ref, "")).strip():
                errors.append(f"promotion manifest missing {required_ref}.")
            if not str(draft.get(required_ref, "")).strip():
                errors.append(f"approved draft missing {required_ref}.")
        if review is None:
            errors.append("promotion audit requires review file.")
        elif promotion_manifest.get("review_batch_id") != review.get("review_batch_id"):
            errors.append("promotion review_batch_id mismatch.")
        if review is not None and not str(review.get("quality_score_reference", "")).strip():
            errors.append("promotion audit requires review batch quality score reference.")

        ticker = str(promotion_manifest.get("ticker", "")).upper()
        if ticker in REAL_TICKERS and not allow_real_company_promotion:
            errors.append(f"real-company promotion blocked by default: {ticker}.")
        if draft.get("ticker") in REAL_TICKERS and not allow_real_company_promotion:
            errors.append(f"real-company approved normalized draft blocked: {draft.get('ticker')}.")
        if draft.get("status") != "fictional_approved_normalized_draft":
            errors.append("approved draft status must remain fictional_approved_normalized_draft.")
        if draft.get("fictional_company") is not True and not allow_real_company_promotion:
            errors.append("approved draft requires fictional_company=true by default.")
        for field in draft.get("fields", []):
            if not isinstance(field, dict):
                errors.append("promoted field must be an object.")
                continue
            candidate_id = field.get("candidate_id")
            review_record = review_by_candidate.get(str(candidate_id))
            if review_record is None:
                errors.append(f"promoted candidate lacks matching review record: {candidate_id}.")
                continue
            if review_record.get("reviewer_decision") not in {"approve", "adjust"}:
                errors.append(f"promoted candidate was not approve/adjust: {candidate_id}.")
            if review_record.get("confidence") == "low":
                errors.append(f"low-confidence approved field promoted: {candidate_id}.")
            checklist = review_record.get("review_checklist")
            if not isinstance(checklist, dict) or checklist.get("relationship_checked") is not True:
                errors.append(f"promoted candidate lacks completed relationship checklist: {candidate_id}.")
            quality = review_record.get("review_quality")
            if not isinstance(quality, dict) or quality.get("approval_readiness") != "ready":
                errors.append(f"promoted candidate lacks ready quality score: {candidate_id}.")
            if isinstance(quality, dict) and quality.get("blocking_issues"):
                errors.append(f"promoted candidate has blocking quality issues: {candidate_id}.")
        if mapping_file is None or mapping_review_file is None:
            errors.append("promotion audit requires mapping file and mapping review file.")
        else:
            mapping, mapping_review, mapping_errors = validate_mapping_review_files(
                mapping_file, mapping_review_file
            )
            errors.extend(f"mapping review: {error}" for error in mapping_errors)
            if mapping.get("mapping_version") != mapping_version:
                errors.append("mapping file version mismatch.")
            if mapping_review.get("mapping_status") != "approved":
                errors.append("promotion audit requires approved mapping review.")
        if review_decision_log_file is None:
            errors.append("promotion audit requires review decision log file.")
        else:
            decision_log = load_json(review_decision_log_file)
            if review is not None and decision_log.get("review_batch_id") != review.get("review_batch_id"):
                errors.append("review decision log batch mismatch.")
            if decision_log.get("mapping_version") != mapping_version:
                errors.append("review decision log mapping version mismatch.")
            if review is not None and decision_log.get("quality_score_reference") != review.get("quality_score_reference"):
                errors.append("review decision log quality score reference mismatch.")
        if quality_score_file is None:
            errors.append("promotion audit requires quality score file.")
        else:
            quality_score = load_json(quality_score_file)
            if quality_score.get("extraction_run_id") != run_id:
                errors.append("quality score extraction_run_id mismatch.")
            if quality_score.get("snapshot_sha256") != snapshot:
                errors.append("quality score snapshot mismatch.")
            if quality_score.get("mapping_version") != mapping_version:
                errors.append("quality score mapping version mismatch.")
            if review is not None and quality_score.get("quality_package_id") != review.get("quality_score_reference"):
                errors.append("quality score package id mismatch.")
    return errors


def render_report(
    extraction_dir: Path,
    review_file: Path | None,
    promotion_dir: Path | None,
    mapping_review_file: Path | None,
    review_decision_log_file: Path | None,
    quality_score_file: Path | None,
    errors: list[str],
) -> str:
    """Render package audit report."""
    return f"""# XBRL Package Audit

## Summary

- Audit passed: `{str(not errors).lower()}`
- Extraction dir: `{relative_or_absolute(extraction_dir)}`
- Review file: `{relative_or_absolute(review_file) if review_file else 'not_provided'}`
- Promotion dir: `{relative_or_absolute(promotion_dir) if promotion_dir else 'not_provided'}`
- Mapping review file: `{relative_or_absolute(mapping_review_file) if mapping_review_file else 'not_provided'}`
- Review decision log file: `{relative_or_absolute(review_decision_log_file) if review_decision_log_file else 'not_provided'}`
- Quality score file: `{relative_or_absolute(quality_score_file) if quality_score_file else 'not_provided'}`
- Generated at: `{utc_now()}`

## Errors

{chr(10).join(f"- {error}" for error in errors) if errors else "- None"}

## Boundary

- Audit checks consistency only.
- Audit does not approve facts, create v0.2.x CSV files, or produce investment conclusions.
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Audit local XBRL extraction/review/promotion packages.")
    parser.add_argument("--extraction-dir", required=True, type=Path)
    parser.add_argument("--review-file", type=Path)
    parser.add_argument("--promotion-dir", type=Path)
    parser.add_argument("--mapping-file", type=Path)
    parser.add_argument("--mapping-review-file", type=Path)
    parser.add_argument("--review-decision-log-file", type=Path)
    parser.add_argument("--quality-score-file", type=Path)
    parser.add_argument("--output-report", required=True, type=Path)
    parser.add_argument("--allow-real-company-promotion", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = [args.extraction_dir, args.output_report]
        if args.review_file:
            paths.append(args.review_file)
        if args.promotion_dir:
            paths.append(args.promotion_dir)
        if args.mapping_file:
            paths.append(args.mapping_file)
        if args.mapping_review_file:
            paths.append(args.mapping_review_file)
        if args.review_decision_log_file:
            paths.append(args.review_decision_log_file)
        if args.quality_score_file:
            paths.append(args.quality_score_file)
        ensure_distinct_paths(*paths)
        errors = audit_package(
            args.extraction_dir,
            args.review_file,
            args.promotion_dir,
            args.mapping_file,
            args.mapping_review_file,
            args.review_decision_log_file,
            args.quality_score_file,
            args.allow_real_company_promotion,
        )
        args.output_report.parent.mkdir(parents=True, exist_ok=True)
        args.output_report.write_text(
            render_report(
                args.extraction_dir,
                args.review_file,
                args.promotion_dir,
                args.mapping_review_file,
                args.review_decision_log_file,
                args.quality_score_file,
                errors,
            ),
            encoding="utf-8",
        )
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote package audit report: {args.output_report}")
    print(f"audit_passed={str(not errors).lower()}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
