#!/usr/bin/env python3
"""Validate local human review records against draft extraction candidates."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import (
    ensure_distinct_paths,
    load_json,
    relative_or_absolute,
    require_finite_number,
    require_text,
    utc_now,
)


DECISIONS = {
    "approve",
    "adjust",
    "reject",
    "unresolved",
    "needs_more_evidence",
}
REQUIRED_RECORD_FIELDS = {
    "review_record_id",
    "run_id",
    "company",
    "ticker",
    "cik",
    "accession",
    "form_type",
    "normalized_field",
    "candidate_id",
    "extracted_value",
    "unit",
    "period",
    "source_tag",
    "source_context",
    "source_locator",
    "transformation",
    "confidence",
    "warning_flags",
    "competing_candidate_ids",
    "reviewer_decision",
    "reviewer_id",
    "reviewer_notes",
    "approved_value",
    "approved_unit",
    "approval_timestamp",
    "prior_review_record_id",
}


def validate_review_documents(
    review: dict[str, Any],
    candidate_doc: dict[str, Any],
    manifest: dict[str, Any],
) -> list[str]:
    """Return all review validation errors."""
    errors: list[str] = []
    required_document = {
        "review_schema_version",
        "review_batch_id",
        "extraction_run_id",
        "snapshot_sha256",
        "mapping_version",
        "company",
        "ticker",
        "fictional_company",
        "created_at",
        "records",
    }
    missing_document = required_document - review.keys()
    if missing_document:
        errors.append(f"Review document missing fields: {sorted(missing_document)}")
        return errors

    if review["extraction_run_id"] != manifest.get("run_id"):
        errors.append("extraction_run_id does not match manifest.")
    if review["snapshot_sha256"] != manifest.get("snapshot_sha256"):
        errors.append("snapshot_sha256 does not match manifest.")
    if review["mapping_version"] != manifest.get("mapping_version"):
        errors.append("mapping_version does not match manifest.")
    if candidate_doc.get("run_id") != manifest.get("run_id"):
        errors.append("Candidate document run_id does not match manifest.")
    if candidate_doc.get("snapshot_sha256") != manifest.get("snapshot_sha256"):
        errors.append("Candidate document snapshot checksum does not match manifest.")
    if candidate_doc.get("mapping_version") != manifest.get("mapping_version"):
        errors.append("Candidate document mapping version does not match manifest.")
    if review["company"] != manifest.get("company"):
        errors.append("Review company does not match manifest.")
    if review["ticker"].upper() != str(manifest.get("ticker", "")).upper():
        errors.append("Review ticker does not match manifest.")

    candidates = candidate_doc.get("candidates")
    if not isinstance(candidates, list):
        errors.append("Candidate document candidates must be an array.")
        return errors
    candidate_by_id = {
        candidate.get("candidate_id"): candidate
        for candidate in candidates
        if isinstance(candidate, dict)
    }
    records = review["records"]
    if not isinstance(records, list) or not records:
        errors.append("Review records must be a non-empty array.")
        return errors

    seen_review_ids: set[str] = set()
    seen_candidates: set[str] = set()
    for index, record in enumerate(records, start=1):
        label = f"record {index}"
        if not isinstance(record, dict):
            errors.append(f"{label} must be an object.")
            continue
        missing = REQUIRED_RECORD_FIELDS - record.keys()
        if missing:
            errors.append(f"{label} missing fields: {sorted(missing)}")
            continue
        try:
            review_id = require_text("review_record_id", record["review_record_id"])
            candidate_id = require_text("candidate_id", record["candidate_id"])
            decision = require_text(
                "reviewer_decision", record["reviewer_decision"]
            )
            confidence = require_text("confidence", record["confidence"])
        except ValueError as exc:
            errors.append(f"{label}: {exc}")
            continue
        if review_id in seen_review_ids:
            errors.append(f"{label}: duplicate review_record_id {review_id}.")
        seen_review_ids.add(review_id)
        if candidate_id in seen_candidates:
            errors.append(f"{label}: candidate reviewed more than once: {candidate_id}.")
        seen_candidates.add(candidate_id)
        candidate = candidate_by_id.get(candidate_id)
        if candidate is None:
            errors.append(f"{label}: candidate_id not found: {candidate_id}.")
            continue
        if decision not in DECISIONS:
            errors.append(f"{label}: unsupported reviewer_decision {decision!r}.")
        if record["run_id"] != manifest.get("run_id"):
            errors.append(f"{label}: run_id does not match manifest.")
        if record["company"] != review["company"]:
            errors.append(f"{label}: company does not match review document.")
        if str(record["ticker"]).upper() != str(review["ticker"]).upper():
            errors.append(f"{label}: ticker does not match review document.")
        if str(record["cik"]).zfill(10) != str(manifest.get("cik", "")).zfill(10):
            errors.append(f"{label}: cik does not match manifest.")
        if record["accession"] != manifest.get("accession"):
            errors.append(f"{label}: accession does not match manifest.")
        if record["form_type"] != manifest.get("form_type"):
            errors.append(f"{label}: form_type does not match manifest.")
        if record["normalized_field"] != candidate.get("normalized_field"):
            errors.append(f"{label}: normalized_field does not match candidate.")
        if record["extracted_value"] != candidate.get("extracted_value"):
            errors.append(f"{label}: extracted_value does not match candidate.")
        if record["unit"] != candidate.get("unit"):
            errors.append(f"{label}: unit does not match candidate.")
        if record["period"] != candidate.get("period"):
            errors.append(f"{label}: period does not match candidate.")
        if record["source_tag"] != candidate.get("concept_qname"):
            errors.append(f"{label}: source_tag does not match candidate.")
        if record["source_context"] != candidate.get("context_id"):
            errors.append(f"{label}: source_context does not match candidate.")
        if record["source_locator"] != candidate.get("source_locator"):
            errors.append(f"{label}: source_locator does not match candidate.")
        if record["transformation"] != candidate.get("transformation"):
            errors.append(f"{label}: transformation does not match candidate.")
        if confidence != candidate.get("confidence"):
            errors.append(f"{label}: confidence does not match candidate.")
        if not isinstance(record["warning_flags"], list):
            errors.append(f"{label}: warning_flags must be an array.")
        elif not set(candidate.get("warning_flags", [])) <= set(
            record["warning_flags"]
        ):
            errors.append(f"{label}: review omits candidate warning flags.")
        if not isinstance(record["competing_candidate_ids"], list):
            errors.append(f"{label}: competing_candidate_ids must be an array.")
        elif record["competing_candidate_ids"] != candidate.get(
            "competing_candidate_ids"
        ):
            errors.append(f"{label}: competing candidate IDs do not match.")
        for text_field in ("reviewer_id", "reviewer_notes"):
            try:
                require_text(text_field, record[text_field])
            except ValueError as exc:
                errors.append(f"{label}: {exc}")

        approved = record["approved_value"]
        if decision in {"approve", "adjust"}:
            if approved == "not_approved":
                errors.append(f"{label}: {decision} requires approved_value.")
            else:
                try:
                    require_finite_number("approved_value", approved)
                except ValueError as exc:
                    errors.append(f"{label}: {exc}")
            if record["approved_unit"] == "not_approved":
                errors.append(f"{label}: {decision} requires approved_unit.")
            elif (
                decision == "approve"
                and record["approved_unit"] != candidate.get("unit")
            ):
                errors.append(
                    f"{label}: approve must retain the candidate unit; use adjust otherwise."
                )
            if record["approval_timestamp"] == "not_approved":
                errors.append(f"{label}: {decision} requires approval_timestamp.")
            else:
                try:
                    parsed = datetime.fromisoformat(
                        str(record["approval_timestamp"]).replace("Z", "+00:00")
                    )
                    if parsed.tzinfo is None:
                        raise ValueError
                except ValueError:
                    errors.append(
                        f"{label}: approval_timestamp must include timezone."
                    )
            if confidence == "low":
                errors.append(f"{label}: low confidence cannot be approved.")
            if candidate.get("review_status") != "draft_extracted_unreviewed":
                errors.append(f"{label}: candidate is not an unreviewed draft.")
            if decision == "approve" and approved != candidate.get(
                "extracted_value"
            ):
                errors.append(
                    f"{label}: approve must retain the extracted value; use adjust otherwise."
                )
        elif decision in {"reject", "unresolved", "needs_more_evidence"}:
            if approved != "not_approved":
                errors.append(f"{label}: {decision} requires not_approved.")
            if record["approved_unit"] != "not_approved":
                errors.append(
                    f"{label}: {decision} requires approved_unit=not_approved."
                )
            if record["approval_timestamp"] != "not_approved":
                errors.append(
                    f"{label}: {decision} requires approval_timestamp=not_approved."
                )
    return errors


def render_report(
    review_file: Path,
    candidate_file: Path,
    manifest_file: Path,
    review: dict[str, Any],
    errors: list[str],
) -> str:
    """Render validation report."""
    status = "Pass" if not errors else "Fail"
    error_lines = (
        "\n".join(f"- {error}" for error in errors) if errors else "- None"
    )
    decisions: dict[str, int] = {}
    for record in review.get("records", []):
        if isinstance(record, dict):
            decision = str(record.get("reviewer_decision", "missing"))
            decisions[decision] = decisions.get(decision, 0) + 1
    decision_lines = (
        "\n".join(f"- `{key}`: {value}" for key, value in sorted(decisions.items()))
        or "- No valid records"
    )
    return f"""# Extraction Review Validation Report

## Result

- Status: `{status}`
- Review file: `{relative_or_absolute(review_file)}`
- Candidate file: `{relative_or_absolute(candidate_file)}`
- Manifest file: `{relative_or_absolute(manifest_file)}`
- Ticker: `{review.get('ticker', 'unverified')}`
- Mapping version: `{review.get('mapping_version', 'unverified')}`
- Generated at: `{utc_now()}`

## Decisions

{decision_lines}

## Errors

{error_lines}

## Boundary

- This validator does not produce normalized output.
- Validation does not itself approve or promote any field.
"""


def validate_files(
    review_file: Path,
    candidate_file: Path,
    manifest_file: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[str]]:
    """Load files and validate review records."""
    review = load_json(review_file)
    candidate_doc = load_json(candidate_file)
    manifest = load_json(manifest_file)
    errors = validate_review_documents(review, candidate_doc, manifest)
    return review, candidate_doc, manifest, errors


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Validate human review records for local draft candidates."
    )
    parser.add_argument("--review-file", required=True, type=Path)
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--manifest-file", required=True, type=Path)
    parser.add_argument("--output-report", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    review_file = args.review_file.expanduser().resolve()
    candidate_file = args.candidate_file.expanduser().resolve()
    manifest_file = args.manifest_file.expanduser().resolve()
    output_report = args.output_report.expanduser().resolve()
    try:
        ensure_distinct_paths(
            review_file, candidate_file, manifest_file, output_report
        )
        review, _, _, errors = validate_files(
            review_file, candidate_file, manifest_file
        )
        output_report.parent.mkdir(parents=True, exist_ok=True)
        output_report.write_text(
            render_report(
                review_file,
                candidate_file,
                manifest_file,
                review,
                errors,
            ),
            encoding="utf-8",
        )
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote review validation report: {output_report}")
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
