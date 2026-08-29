#!/usr/bin/env python3
"""Validate fixture-only XBRL mapping review batches."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import ensure_distinct_paths, load_json, prepare_output_dir, relative_or_absolute, require_text, utc_now, write_json


STATUSES = {"draft", "reviewed", "approved", "superseded", "rejected"}
DECISIONS = {
    "approve_mapping",
    "reject_mapping",
    "request_more_evidence",
    "supersede_mapping",
}


def mapping_records_by_id(mapping: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return mapping records keyed by mapping_id."""
    records = mapping.get("records")
    if not isinstance(records, list):
        raise ValueError("Mapping records must be an array.")
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Mapping record must be an object.")
        mapping_id = require_text("mapping_id", record.get("mapping_id"))
        result[mapping_id] = record
    return result


def validate_mapping_review(
    mapping: dict[str, Any], review: dict[str, Any]
) -> list[str]:
    """Return mapping review errors."""
    errors: list[str] = []
    required = {
        "mapping_review_schema_version",
        "mapping_review_batch_id",
        "mapping_version",
        "mapping_status",
        "created_at",
        "reviewer_id",
        "records",
    }
    missing = required - review.keys()
    if missing:
        return [f"Mapping review missing fields: {sorted(missing)}"]
    mapping_version = mapping.get("mapping_version")
    if review.get("mapping_version") != mapping_version:
        errors.append("mapping_version does not match mapping file.")
    status = review.get("mapping_status")
    if status not in STATUSES:
        errors.append(f"Invalid mapping_status: {status!r}.")
    records = review.get("records")
    if not isinstance(records, list) or not records:
        errors.append("Mapping review records must be a non-empty array.")
        return errors
    mapping_by_id = mapping_records_by_id(mapping)
    seen: set[str] = set()
    approved_count = 0
    for index, record in enumerate(records, start=1):
        label = f"record {index}"
        if not isinstance(record, dict):
            errors.append(f"{label} must be an object.")
            continue
        for field in (
            "mapping_review_record_id",
            "mapping_id",
            "normalized_field",
            "reviewer_decision",
            "review_status",
            "evidence_notes",
            "reviewer_notes",
            "review_timestamp",
        ):
            if field not in record:
                errors.append(f"{label} missing field: {field}.")
        mapping_id = str(record.get("mapping_id", ""))
        if mapping_id in seen:
            errors.append(f"{label}: duplicate mapping_id {mapping_id}.")
        seen.add(mapping_id)
        mapping_record = mapping_by_id.get(mapping_id)
        if mapping_record is None:
            errors.append(f"{label}: mapping_id does not exist: {mapping_id}.")
            continue
        if record.get("normalized_field") != mapping_record.get("normalized_field"):
            errors.append(f"{label}: normalized_field does not match mapping.")
        relationship_metadata = mapping_record.get("relationship_metadata")
        if not isinstance(relationship_metadata, dict):
            errors.append(f"{label}: mapping record missing relationship_metadata.")
        elif relationship_metadata.get("relationship_review_status") in {"unsupported", "needs_more_evidence"}:
            errors.append(f"{label}: mapping relationship evidence is not approval-ready.")
        decision = record.get("reviewer_decision")
        if decision not in DECISIONS:
            errors.append(f"{label}: invalid reviewer_decision {decision!r}.")
        review_status = record.get("review_status")
        if review_status not in STATUSES:
            errors.append(f"{label}: invalid review_status {review_status!r}.")
        evidence_notes = str(record.get("evidence_notes", "")).strip()
        reviewer_notes = str(record.get("reviewer_notes", "")).strip()
        if decision == "approve_mapping":
            approved_count += 1
            if review_status != "approved":
                errors.append(f"{label}: approve_mapping requires review_status=approved.")
            if not evidence_notes or evidence_notes in {"none", "not_applicable"}:
                errors.append(f"{label}: approve_mapping requires evidence_notes.")
            if not reviewer_notes or reviewer_notes in {"none", "not_applicable"}:
                errors.append(f"{label}: approve_mapping requires reviewer_notes.")
            if mapping_record.get("relationship_metadata") and record.get("relationship_reviewed") is not True:
                errors.append(f"{label}: approve_mapping requires relationship_reviewed=true.")
            relationship_notes = str(record.get("relationship_evidence_notes", "")).strip()
            if mapping_record.get("relationship_metadata") and not relationship_notes:
                errors.append(f"{label}: approve_mapping requires relationship_evidence_notes.")
        if decision == "reject_mapping" and review_status != "rejected":
            errors.append(f"{label}: reject_mapping requires review_status=rejected.")
        if decision == "supersede_mapping" and review_status != "superseded":
            errors.append(f"{label}: supersede_mapping requires review_status=superseded.")
        if decision == "request_more_evidence" and review_status not in {"draft", "reviewed"}:
            errors.append(f"{label}: request_more_evidence requires draft or reviewed status.")
    if status == "approved":
        if approved_count != len(mapping_by_id):
            errors.append("approved mapping review must approve every mapping record.")
    if status in {"superseded", "rejected"}:
        errors.append(f"mapping_status={status} blocks promotion.")
    return errors


def mapping_review_is_approved(mapping: dict[str, Any], review: dict[str, Any]) -> bool:
    """Return whether review fully approves the mapping."""
    return not validate_mapping_review(mapping, review) and review.get("mapping_status") == "approved"


def render_report(mapping_file: Path, review_file: Path, review: dict[str, Any], errors: list[str]) -> str:
    """Render mapping review report."""
    decisions: dict[str, int] = {}
    for record in review.get("records", []):
        if isinstance(record, dict):
            decision = str(record.get("reviewer_decision", "missing"))
            decisions[decision] = decisions.get(decision, 0) + 1
    decision_lines = "\n".join(f"- `{key}`: {value}" for key, value in sorted(decisions.items())) or "- None"
    return f"""# Mapping Review Report

## Summary

- Review passed: `{str(not errors).lower()}`
- Mapping file: `{relative_or_absolute(mapping_file)}`
- Review file: `{relative_or_absolute(review_file)}`
- Mapping version: `{review.get('mapping_version', 'unverified')}`
- Mapping status: `{review.get('mapping_status', 'unverified')}`
- Generated at: `{utc_now()}`

## Decisions

{decision_lines}

## Errors

{chr(10).join(f"- {error}" for error in errors) if errors else "- None"}

## Boundary

- Mapping review does not extract financial fields.
- Mapping review does not create normalized output.
- Mapping review does not produce investment conclusions.
"""


def render_decision_log(mapping_file: Path, review_file: Path, review: dict[str, Any], errors: list[str]) -> dict[str, Any]:
    """Return a machine-readable mapping decision log."""
    decisions: dict[str, int] = {}
    for record in review.get("records", []):
        if isinstance(record, dict):
            decision = str(record.get("reviewer_decision", "missing"))
            decisions[decision] = decisions.get(decision, 0) + 1
    return {
        "mapping_decision_log_id": f"mapping-decision-log-{review.get('mapping_review_batch_id', 'unverified')}",
        "created_at": utc_now(),
        "mapping_file": relative_or_absolute(mapping_file),
        "review_file": relative_or_absolute(review_file),
        "mapping_review_batch_id": review.get("mapping_review_batch_id", "unverified"),
        "mapping_version": review.get("mapping_version", "unverified"),
        "mapping_status": review.get("mapping_status", "unverified"),
        "review_passed": not errors,
        "decision_counts": decisions,
        "errors": errors,
        "boundary": [
            "Mapping review validates mapping governance only.",
            "No field extraction, normalized output, investment conclusion, or real-company approval is generated.",
        ],
    }


def write_artifacts(
    mapping_file: Path,
    review_file: Path,
    output_dir: Path,
    overwrite: bool = False,
) -> dict[str, Path]:
    """Write mapping review batch, report and decision log artifacts."""
    ensure_distinct_paths(mapping_file, review_file, output_dir)
    _mapping, review, errors = validate_files(mapping_file, review_file)
    prepare_output_dir(output_dir, overwrite)
    paths = {
        "mapping_review_batch.json": output_dir / "mapping_review_batch.json",
        "mapping_review_report.md": output_dir / "mapping_review_report.md",
        "mapping_decision_log.json": output_dir / "mapping_decision_log.json",
    }
    batch = dict(review)
    batch["review_passed"] = not errors
    batch["source_mapping_file"] = relative_or_absolute(mapping_file)
    batch["source_review_file"] = relative_or_absolute(review_file)
    batch["generated_at"] = utc_now()
    batch["errors"] = errors
    write_json(paths["mapping_review_batch.json"], batch)
    paths["mapping_review_report.md"].write_text(
        render_report(mapping_file, review_file, review, errors),
        encoding="utf-8",
    )
    write_json(
        paths["mapping_decision_log.json"],
        render_decision_log(mapping_file, review_file, review, errors),
    )
    if errors:
        raise ValueError("Mapping review validation failed: " + "; ".join(errors))
    return paths


def validate_files(mapping_file: Path, review_file: Path) -> tuple[dict[str, Any], dict[str, Any], list[str]]:
    """Load and validate mapping review files."""
    mapping = load_json(mapping_file)
    review = load_json(review_file)
    return mapping, review, validate_mapping_review(mapping, review)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Validate local XBRL mapping review batch.")
    parser.add_argument("--mapping-file", required=True, type=Path)
    parser.add_argument("--review-file", required=True, type=Path)
    parser.add_argument("--output-report", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        if not args.output_report and not args.output_dir:
            raise ValueError("Use --output-report and/or --output-dir.")
        mapping, review, errors = validate_files(args.mapping_file, args.review_file)
        if args.output_report:
            ensure_distinct_paths(args.mapping_file, args.review_file, args.output_report)
            args.output_report.parent.mkdir(parents=True, exist_ok=True)
            args.output_report.write_text(
                render_report(args.mapping_file, args.review_file, review, errors),
                encoding="utf-8",
            )
        if args.output_dir:
            write_artifacts(args.mapping_file, args.review_file, args.output_dir, args.overwrite)
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.output_report:
        print(f"Wrote mapping review report: {args.output_report}")
    if args.output_dir:
        print(f"Wrote mapping review artifacts: {args.output_dir}")
    print(f"mapping_review_passed={str(not errors).lower()}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
