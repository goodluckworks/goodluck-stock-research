#!/usr/bin/env python3
"""Collect reviewer decisions and normalize them into review batches."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import ensure_distinct_paths, load_json, prepare_output_dir, relative_or_absolute, require_finite_number, utc_now, write_json


DECISIONS = {"approve", "adjust", "reject", "unresolved", "needs_more_evidence"}
OUTPUTS = (
    "normalized_review_batch.json",
    "review_decision_log.json",
    "review_collection_report.md",
)
REQUIRED_CHECKS = (
    "period_checked",
    "unit_checked",
    "context_checked",
    "dimensions_checked",
    "sign_checked",
    "scale_checked",
    "relationship_checked",
    "competing_candidates_checked",
    "prior_period_checked",
    "materiality_checked",
    "reviewer_notes_present",
)


def validate_decisions(
    decision_doc: dict[str, Any],
    candidate_doc: dict[str, Any],
    manifest: dict[str, Any],
    quality_doc: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Validate decision template and return normalized records plus errors."""
    errors: list[str] = []
    if decision_doc.get("decision_source") != "reviewer_workbench_template":
        errors.append("decision_source must be reviewer_workbench_template.")
    if decision_doc.get("extraction_run_id") != manifest.get("run_id"):
        errors.append("extraction_run_id does not match manifest.")
    if decision_doc.get("snapshot_sha256") != manifest.get("snapshot_sha256"):
        errors.append("snapshot_sha256 does not match manifest.")
    if decision_doc.get("mapping_version") != manifest.get("mapping_version"):
        errors.append("mapping_version does not match manifest.")
    candidates = candidate_doc.get("candidates", [])
    if not isinstance(candidates, list):
        return [], ["candidates must be an array."]
    candidate_by_id = {
        item.get("candidate_id"): item for item in candidates if isinstance(item, dict)
    }
    quality_by_id: dict[str, dict[str, Any]] = {}
    quality_reference = "not_provided"
    if quality_doc is not None:
        if quality_doc.get("extraction_run_id") != manifest.get("run_id"):
            errors.append("quality score extraction_run_id does not match manifest.")
        if quality_doc.get("snapshot_sha256") != manifest.get("snapshot_sha256"):
            errors.append("quality score snapshot_sha256 does not match manifest.")
        if quality_doc.get("mapping_version") != manifest.get("mapping_version"):
            errors.append("quality score mapping_version does not match manifest.")
        quality_reference = quality_doc.get("quality_package_id", "unverified")
        quality_records = quality_doc.get("records", [])
        if not isinstance(quality_records, list):
            errors.append("quality score records must be an array.")
        else:
            quality_by_id = {
                item.get("candidate_id"): item for item in quality_records if isinstance(item, dict)
            }
    records = decision_doc.get("records", [])
    if not isinstance(records, list) or not records:
        return [], ["decision records must be a non-empty array."]
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, decision_record in enumerate(records, start=1):
        label = f"record {index}"
        if not isinstance(decision_record, dict):
            errors.append(f"{label} must be an object.")
            continue
        candidate_id = decision_record.get("candidate_id")
        if not candidate_id:
            errors.append(f"{label}: missing candidate_id.")
            continue
        if candidate_id in seen:
            errors.append(f"{label}: duplicate candidate_id {candidate_id}.")
        seen.add(str(candidate_id))
        candidate = candidate_by_id.get(candidate_id)
        if candidate is None:
            errors.append(f"{label}: candidate_id not found: {candidate_id}.")
            continue
        reviewer_decision = decision_record.get("reviewer_decision")
        if reviewer_decision not in DECISIONS:
            errors.append(f"{label}: invalid reviewer_decision {reviewer_decision!r}.")
            continue
        reviewer_notes = str(decision_record.get("reviewer_notes", "")).strip()
        checklist = decision_record.get("review_checklist")
        if not isinstance(checklist, dict):
            errors.append(f"{label}: missing review_checklist.")
            checklist = {}
        elif checklist.get("candidate_id") != candidate_id:
            errors.append(f"{label}: review_checklist candidate_id mismatch.")
        quality = quality_by_id.get(candidate_id)
        approved_value = decision_record.get("approved_value", "not_approved")
        approved_unit = decision_record.get("approved_unit", "not_approved")
        approval_timestamp = decision_record.get("approval_timestamp", "not_approved")
        if reviewer_decision in {"approve", "adjust"}:
            if not reviewer_notes or reviewer_notes in {"none", "not_applicable"}:
                errors.append(f"{label}: {reviewer_decision} requires reviewer_notes.")
            if quality_doc is None:
                errors.append(f"{label}: {reviewer_decision} requires quality score file.")
            elif quality is None:
                errors.append(f"{label}: {reviewer_decision} requires quality score record.")
            elif quality.get("approval_readiness") != "ready":
                errors.append(f"{label}: quality score not_ready fails approve.")
            if quality and quality.get("blocking_issues"):
                errors.append(f"{label}: blocking issue fails approve.")
            for check_name in REQUIRED_CHECKS:
                if checklist.get(check_name) is not True:
                    errors.append(f"{label}: {reviewer_decision} requires {check_name}=true.")
            if checklist.get("relationship_checked") is not True:
                errors.append(f"{label}: relationship_checked false fails approve.")
            if candidate.get("confidence") == "low":
                errors.append(f"{label}: low confidence cannot be approved.")
            if approved_value == "not_approved":
                errors.append(f"{label}: {reviewer_decision} requires approved_value.")
            else:
                try:
                    require_finite_number("approved_value", approved_value)
                except ValueError as exc:
                    errors.append(f"{label}: {exc}")
            if approved_unit == "not_approved":
                errors.append(f"{label}: {reviewer_decision} requires approved_unit.")
            if approval_timestamp == "not_approved":
                errors.append(f"{label}: {reviewer_decision} requires approval_timestamp.")
            if reviewer_decision == "approve" and approved_value != candidate.get("extracted_value"):
                errors.append(f"{label}: approve must retain extracted value; use adjust.")
        else:
            if approved_value != "not_approved":
                errors.append(f"{label}: {reviewer_decision} requires approved_value=not_approved.")
            if approved_unit != "not_approved":
                errors.append(f"{label}: {reviewer_decision} requires approved_unit=not_approved.")
            if approval_timestamp != "not_approved":
                errors.append(f"{label}: {reviewer_decision} requires approval_timestamp=not_approved.")
        normalized.append(
            {
                "review_record_id": f"review-{candidate_id}",
                "run_id": manifest["run_id"],
                "company": manifest["company"],
                "ticker": manifest["ticker"],
                "cik": manifest["cik"],
                "accession": manifest["accession"],
                "form_type": manifest["form_type"],
                "normalized_field": candidate["normalized_field"],
                "candidate_id": candidate_id,
                "extracted_value": candidate["extracted_value"],
                "unit": candidate["unit"],
                "period": candidate["period"],
                "source_tag": candidate["concept_qname"],
                "source_context": candidate["context_id"],
                "source_locator": candidate["source_locator"],
                "transformation": candidate["transformation"],
                "confidence": candidate["confidence"],
                "warning_flags": candidate.get("warning_flags", []),
                "competing_candidate_ids": candidate.get("competing_candidate_ids", []),
                "reviewer_decision": reviewer_decision,
                "reviewer_id": decision_record.get("reviewer_id", "fixture-reviewer"),
                "reviewer_notes": reviewer_notes,
                "approved_value": approved_value,
                "approved_unit": approved_unit,
                "approval_timestamp": approval_timestamp,
                "prior_review_record_id": decision_record.get("prior_review_record_id", "not_applicable"),
                "review_checklist": checklist,
                "review_quality": quality or {
                    "approval_readiness": "not_ready",
                    "blocking_issues": ["quality_score_not_provided"],
                },
                "quality_score_reference": quality_reference,
            }
        )
    missing = set(candidate_by_id) - seen
    if missing:
        errors.append(f"decision file omitted candidate_ids: {sorted(missing)}")
    return normalized, errors


def run_collector(
    decision_file: Path,
    candidate_file: Path,
    manifest_file: Path,
    quality_score_file: Path | None,
    output_dir: Path,
    overwrite: bool = False,
) -> dict[str, Path]:
    """Collect reviewer decisions."""
    if quality_score_file is not None:
        ensure_distinct_paths(decision_file, candidate_file, manifest_file, quality_score_file, output_dir)
    else:
        ensure_distinct_paths(decision_file, candidate_file, manifest_file, output_dir)
    decision_doc = load_json(decision_file)
    candidate_doc = load_json(candidate_file)
    manifest = load_json(manifest_file)
    quality_doc = load_json(quality_score_file) if quality_score_file is not None else None
    records, errors = validate_decisions(decision_doc, candidate_doc, manifest, quality_doc)
    if errors:
        raise ValueError("Review decision collection failed: " + "; ".join(errors))
    overwrite_used = prepare_output_dir(output_dir, overwrite)
    paths = {name: output_dir / name for name in OUTPUTS}
    decision_counts: dict[str, int] = {}
    for record in records:
        decision = record["reviewer_decision"]
        decision_counts[decision] = decision_counts.get(decision, 0) + 1
    batch = {
        "review_schema_version": "v0.3.6-normalized-review-batch",
        "normalized_review_batch": True,
        "decision_source": "normalized_review_batch",
        "source_decision_file": relative_or_absolute(decision_file),
        "quality_score_reference": quality_doc.get("quality_package_id", "not_provided") if quality_doc else "not_provided",
        "quality_score_file": relative_or_absolute(quality_score_file) if quality_score_file else "not_provided",
        "review_batch_id": f"normalized-review-{str(manifest['ticker']).lower()}-{manifest['snapshot_sha256'][:12]}",
        "extraction_run_id": manifest["run_id"],
        "raw_snapshot_id": manifest["snapshot_sha256"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "mapping_version": manifest["mapping_version"],
        "batch_status": "approved",
        "company": manifest["company"],
        "ticker": manifest["ticker"],
        "fictional_company": manifest["ticker"] == "EXMP",
        "created_at": utc_now(),
        "records": records,
    }
    decision_log = {
        "decision_log_id": f"decision-log-{str(manifest['ticker']).lower()}-{manifest['snapshot_sha256'][:12]}",
        "created_at": utc_now(),
        "source_decision_file": relative_or_absolute(decision_file),
        "quality_score_file": relative_or_absolute(quality_score_file) if quality_score_file else "not_provided",
        "quality_score_reference": batch["quality_score_reference"],
        "candidate_file": relative_or_absolute(candidate_file),
        "manifest_file": relative_or_absolute(manifest_file),
        "review_batch_id": batch["review_batch_id"],
        "extraction_run_id": manifest["run_id"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "mapping_version": manifest["mapping_version"],
        "ticker": manifest["ticker"],
        "decision_counts": decision_counts,
        "overwrite_used": overwrite_used,
    }
    report = f"""# Review Decision Collection Report

## Summary

- Collection passed: `true`
- Ticker: `{manifest['ticker']}`
- Review batch ID: `{batch['review_batch_id']}`
- Extraction run ID: `{manifest['run_id']}`
- Mapping version: `{manifest['mapping_version']}`
- Quality score reference: `{batch['quality_score_reference']}`
- Snapshot SHA-256: `{manifest['snapshot_sha256']}`
- Generated at: `{utc_now()}`

## Decisions

{chr(10).join(f"- `{key}`: {value}" for key, value in sorted(decision_counts.items()))}

## Boundary

- Collector validates reviewer decisions but does not promote fields.
- Real-company decision batches remain blocked by promotion isolation.
- No investment conclusion or v0.2.x populated CSV is generated.
"""
    write_json(paths["normalized_review_batch.json"], batch)
    write_json(paths["review_decision_log.json"], decision_log)
    paths["review_collection_report.md"].write_text(report, encoding="utf-8")
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Collect XBRL reviewer decisions.")
    parser.add_argument("--decision-file", required=True, type=Path)
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--manifest-file", required=True, type=Path)
    parser.add_argument("--quality-score-file", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run_collector(
            args.decision_file,
            args.candidate_file,
            args.manifest_file,
            args.quality_score_file,
            args.output_dir,
            args.overwrite,
        )
    except (FileNotFoundError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote review decision package: {args.output_dir}")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
