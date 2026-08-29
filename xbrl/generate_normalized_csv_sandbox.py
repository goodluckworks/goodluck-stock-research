#!/usr/bin/env python3
"""Generate a fictional-only v0.2.x-compatible normalized CSV sandbox."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import (
    REAL_TICKERS,
    ensure_distinct_paths,
    load_json,
    prepare_output_dir,
    relative_or_absolute,
    require_finite_number,
    utc_now,
    write_json,
)
from partial_field_policy import classify_fields, downstream_impact, grouped_fields
from unresolved_field_reporter import render_unresolved_section


OUTPUTS = (
    "normalized_financials_sandbox.csv",
    "normalized_csv_audit.json",
    "normalized_csv_manifest.json",
    "normalized_csv_report.md",
)
SANDBOX_STATUS = "fictional_sandbox_not_investment_data"
ALLOWED_TICKER = "EXMP"
FORBIDDEN_FIELDS = {
    "target_price",
    "recommendation",
    "buy",
    "sell",
    "hold",
    "position_size",
    "research_status",
    "trading_action",
}
FINANCIAL_COLUMNS = [
    "period",
    "currency",
    "amount_unit",
    "per_share_unit",
    "basis",
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "total_debt",
    "total_assets",
    "shareholders_equity",
    "shares_diluted",
    "stock_based_compensation",
    "accounts_receivable",
    "inventory",
    "current_assets",
    "current_liabilities",
    "source",
    "source_date",
    "source_status",
    "short_term_investments",
    "cash_and_short_term_investments",
    "net_debt_basis",
    "special_items_notes",
    "normalized_net_income",
    "normalized_eps",
    "normalized_operating_income",
    "goodwill",
    "intangible_assets",
    "acquisition_related_amortization",
    "restructuring_and_integration_costs",
    "acquisition_related_costs",
    "acquisition_accounting_notes",
]
AUDIT_COLUMNS = [
    "fictional",
    "sandbox_status",
    "not_investment_data",
    "not_company_fact",
    "not_for_trading",
    "not_production_research",
    "review_batch_id",
    "promotion_id",
    "mapping_version",
    "snapshot_sha256",
    "provenance_references",
    "audit_reference",
]
CSV_COLUMNS = FINANCIAL_COLUMNS + AUDIT_COLUMNS


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


def promoted_by_field(draft: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return promoted records keyed by normalized field."""
    fields = draft.get("fields", [])
    if not isinstance(fields, list):
        raise ValueError("approved_normalized_draft fields must be an array.")
    result: dict[str, dict[str, Any]] = {}
    for field in fields:
        if not isinstance(field, dict):
            raise ValueError("promoted field must be an object.")
        if field.get("reviewer_decision") not in {"approve", "adjust"}:
            raise ValueError("Only approve/adjust fields may be promoted to CSV.")
        normalized_field = str(field.get("normalized_field", ""))
        if not normalized_field:
            raise ValueError("Promoted field missing normalized_field.")
        if normalized_field in result:
            raise ValueError(f"Duplicate promoted field: {normalized_field}")
        require_finite_number(f"{normalized_field}.approved_value", field.get("approved_value"))
        for required in ("candidate_id", "review_record_id", "transformation", "period", "confidence"):
            if not str(field.get(required, "")).strip():
                raise ValueError(f"Promoted field {normalized_field} missing {required}.")
        result[normalized_field] = field
    return result


def load_and_validate(
    promotion_dir: Path,
    review_file: Path,
    candidate_file: Path,
    manifest_file: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    """Load and validate source packages for EXMP sandbox generation."""
    promotion_manifest = load_json(promotion_dir / "promotion_manifest.json")
    draft = load_json(promotion_dir / "approved_normalized_draft.json")
    review = load_json(review_file)
    candidate_doc = load_json(candidate_file)
    manifest = load_json(manifest_file)
    for name, doc in (
        ("promotion_manifest", promotion_manifest),
        ("approved_normalized_draft", draft),
        ("review", review),
        ("candidates", candidate_doc),
        ("manifest", manifest),
    ):
        hits = find_forbidden(doc)
        if hits:
            raise ValueError(f"{name} contains forbidden conclusion/trading fields: {hits}")
    ticker = str(promotion_manifest.get("ticker", "")).upper()
    if ticker != ALLOWED_TICKER:
        raise ValueError(f"Normalized CSV sandbox is fictional-only and allows only {ALLOWED_TICKER}; got {ticker}.")
    if ticker in REAL_TICKERS:
        raise ValueError(f"Real-company normalized CSV sandbox is blocked: {ticker}.")
    if promotion_manifest.get("fictional_company") is not True or draft.get("fictional_company") is not True:
        raise ValueError("Normalized CSV sandbox requires fictional_company=true.")
    if promotion_manifest.get("promotion_id") != draft.get("promotion_id"):
        raise ValueError("Promotion manifest and draft promotion_id mismatch.")
    if promotion_manifest.get("review_batch_id") != review.get("review_batch_id"):
        raise ValueError("Promotion manifest and review batch mismatch.")
    if promotion_manifest.get("extraction_run_id") != manifest.get("run_id"):
        raise ValueError("Promotion manifest and extraction manifest run mismatch.")
    for doc_name, doc in (("review", review), ("candidates", candidate_doc), ("draft", draft)):
        if doc.get("mapping_version") != manifest.get("mapping_version"):
            raise ValueError(f"{doc_name} mapping_version does not match manifest.")
        if doc.get("snapshot_sha256") != manifest.get("snapshot_sha256"):
            raise ValueError(f"{doc_name} snapshot_sha256 does not match manifest.")
    if candidate_doc.get("review_status") != "draft_extracted_unreviewed":
        raise ValueError("Candidate package must remain draft_extracted_unreviewed.")
    promoted = promoted_by_field(draft)
    review_by_id = {record.get("review_record_id"): record for record in review.get("records", [])}
    candidate_by_id = {candidate.get("candidate_id"): candidate for candidate in candidate_doc.get("candidates", [])}
    for normalized_field, field in promoted.items():
        review_record = review_by_id.get(field["review_record_id"])
        candidate = candidate_by_id.get(field["candidate_id"])
        if review_record is None:
            raise ValueError(f"Missing review record for {normalized_field}.")
        if candidate is None:
            raise ValueError(f"Missing candidate record for {normalized_field}.")
        if review_record.get("reviewer_decision") not in {"approve", "adjust"}:
            raise ValueError(f"Non-approved review record attempted CSV population: {normalized_field}.")
        if review_record.get("normalized_field") != normalized_field or candidate.get("normalized_field") != normalized_field:
            raise ValueError(f"Field identity mismatch for {normalized_field}.")
    return promotion_manifest, draft, review, candidate_doc, manifest, promoted


def build_csv_row(
    promotion_manifest: dict[str, Any],
    review: dict[str, Any],
    manifest: dict[str, Any],
    promoted: dict[str, dict[str, Any]],
    audit_reference: str,
) -> dict[str, str]:
    """Build one v0.2.x-compatible sandbox CSV row."""
    row = {column: "" for column in CSV_COLUMNS}
    row.update(
        {
            "period": str(manifest["reporting_period"]),
            "currency": str(manifest["currency"]),
            "amount_unit": str(manifest["amount_unit"]),
            "per_share_unit": str(manifest["per_share_unit"]),
            "basis": (
                "GAAP-like fictional sandbox; populated only from EXMP approved-field "
                "promotion; not company fact; not investment data"
            ),
            "source": f"fictional EXMP XBRL promotion sandbox {promotion_manifest['promotion_id']}",
            "source_date": str(promotion_manifest.get("created_at", utc_now())),
            "source_status": "fictional_sandbox",
            "net_debt_basis": "unknown",
            "special_items_notes": "fictional sandbox; unsupported fields left blank/unresolved",
            "fictional": "true",
            "sandbox_status": SANDBOX_STATUS,
            "not_investment_data": "true",
            "not_company_fact": "true",
            "not_for_trading": "true",
            "not_production_research": "true",
            "review_batch_id": str(review["review_batch_id"]),
            "promotion_id": str(promotion_manifest["promotion_id"]),
            "mapping_version": str(manifest["mapping_version"]),
            "snapshot_sha256": str(manifest["snapshot_sha256"]),
            "audit_reference": audit_reference,
        }
    )
    provenance_references: list[str] = []
    for field, promoted_record in promoted.items():
        if field not in FINANCIAL_COLUMNS:
            continue
        row[field] = str(promoted_record["approved_value"])
        provenance_references.append(
            f"{field}:{promoted_record['candidate_id']}:{promoted_record['review_record_id']}"
        )
    row["provenance_references"] = ";".join(provenance_references)
    return row


def build_audit_records(
    csv_row: dict[str, str],
    promoted: dict[str, dict[str, Any]],
    candidate_doc: dict[str, Any],
) -> list[dict[str, Any]]:
    """Build field-level CSV audit records."""
    candidate_by_id = {candidate.get("candidate_id"): candidate for candidate in candidate_doc.get("candidates", [])}
    records: list[dict[str, Any]] = []
    for field, promoted_record in sorted(promoted.items()):
        if field not in FINANCIAL_COLUMNS:
            continue
        candidate = candidate_by_id[promoted_record["candidate_id"]]
        records.append(
            {
                "normalized_field": field,
                "csv_column": field,
                "csv_value": csv_row[field],
                "candidate_id": promoted_record["candidate_id"],
                "review_record_id": promoted_record["review_record_id"],
                "reviewer_decision": promoted_record["reviewer_decision"],
                "approved_value": promoted_record["approved_value"],
                "transformation": promoted_record["transformation"],
                "unit": promoted_record["approved_unit"],
                "period": promoted_record["period"],
                "confidence": promoted_record["confidence"],
                "provenance_reference": f"provenance-{promoted_record['candidate_id']}",
                "source_tag": promoted_record["source_tag"],
                "source_locator": promoted_record["source_locator"],
                "source_fact_ids": candidate.get("source_fact_ids", []),
            }
        )
    return records


def run_generator(
    promotion_dir: Path,
    review_file: Path,
    candidate_file: Path,
    manifest_file: Path,
    output_dir: Path,
    overwrite: bool = False,
) -> dict[str, Path]:
    """Generate EXMP fictional normalized CSV sandbox package."""
    ensure_distinct_paths(promotion_dir, review_file, candidate_file, manifest_file, output_dir)
    promotion_dir = promotion_dir.expanduser().resolve()
    review_file = review_file.expanduser().resolve()
    candidate_file = candidate_file.expanduser().resolve()
    manifest_file = manifest_file.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    promotion_manifest, draft, review, candidate_doc, manifest, promoted = load_and_validate(
        promotion_dir, review_file, candidate_file, manifest_file
    )
    overwrite_used = prepare_output_dir(output_dir, overwrite)
    paths = {name: output_dir / name for name in OUTPUTS}
    csv_row = build_csv_row(
        promotion_manifest,
        review,
        manifest,
        promoted,
        relative_or_absolute(paths["normalized_csv_audit.json"]),
    )
    if csv_row["sandbox_status"] != SANDBOX_STATUS or csv_row["fictional"] != "true":
        raise ValueError("Generated CSV row is missing fictional/sandbox flags.")
    audit_records = build_audit_records(csv_row, promoted, candidate_doc)
    if len(audit_records) != len([field for field in promoted if field in FINANCIAL_COLUMNS]):
        raise ValueError("Every populated CSV field must have an audit record.")
    field_statuses = classify_fields(FINANCIAL_COLUMNS, promoted, draft.get("excluded_records", []))
    grouped = grouped_fields(field_statuses)
    unresolved_fields = sorted(grouped.get("unresolved", []))
    omitted_fields = sorted(
        grouped.get("missing", [])
        + grouped.get("unsupported", [])
        + grouped.get("rejected", [])
    )
    blocked_fields = sorted(grouped.get("blocked", []))
    impact = downstream_impact(field_statuses)
    paths["normalized_financials_sandbox.csv"].parent.mkdir(parents=True, exist_ok=True)
    with paths["normalized_financials_sandbox.csv"].open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerow(csv_row)
    audit = {
        "audit_schema_version": "v0.3.8",
        "csv_path": relative_or_absolute(paths["normalized_financials_sandbox.csv"]),
        "audit_path": relative_or_absolute(paths["normalized_csv_audit.json"]),
        "field_audit_records": audit_records,
        "source_review_batch_id": review["review_batch_id"],
        "source_promotion_id": promotion_manifest["promotion_id"],
        "mapping_version": manifest["mapping_version"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "sandbox_status": SANDBOX_STATUS,
    }
    manifest_out = {
        "csv_schema_version": "v0.3.8",
        "company": manifest["company"],
        "ticker": ALLOWED_TICKER,
        "fixture_data_status": manifest["fixture_data_status"],
        "sandbox_status": SANDBOX_STATUS,
        "period": manifest["reporting_period"],
        "currency": manifest["currency"],
        "amount_unit": manifest["amount_unit"],
        "per_share_unit": manifest["per_share_unit"],
        "populated_fields": sorted(record["normalized_field"] for record in audit_records),
        "omitted_fields": omitted_fields,
        "unresolved_fields": unresolved_fields,
        "blocked_fields": blocked_fields,
        "field_statuses": field_statuses,
        "downstream_impact": impact,
        "source_review_batch_id": review["review_batch_id"],
        "source_promotion_id": promotion_manifest["promotion_id"],
        "mapping_version": manifest["mapping_version"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "prohibited_real_company_flag": False,
        "no_investment_conclusion": True,
        "csv_file": relative_or_absolute(paths["normalized_financials_sandbox.csv"]),
        "audit_file": relative_or_absolute(paths["normalized_csv_audit.json"]),
        "created_at": utc_now(),
        "overwrite_used": overwrite_used,
        "labels": [
            "fictional",
            "sandbox",
            "not investment data",
            "not company fact",
            "not for production research",
            "not for trading",
        ],
    }
    report = f"""# Fictional Normalized CSV Sandbox

## Summary

- Company: `{manifest['company']}`
- Ticker: `{ALLOWED_TICKER}`
- Sandbox status: `{SANDBOX_STATUS}`
- Promotion ID: `{promotion_manifest['promotion_id']}`
- Review batch ID: `{review['review_batch_id']}`
- Mapping version: `{manifest['mapping_version']}`
- Snapshot SHA-256: `{manifest['snapshot_sha256']}`
- Populated fields: `{', '.join(manifest_out['populated_fields'])}`
- Omitted fields: `{', '.join(omitted_fields) or 'none'}`
- Unresolved fields: `{', '.join(unresolved_fields) or 'none'}`
- Blocked fields: `{', '.join(blocked_fields) or 'none'}`
- Ratio dry-run allowed: `{str(impact['ratio_dry_run_allowed']).lower()}`
- Overwrite used: `{str(overwrite_used).lower()}`

{render_unresolved_section(manifest_out)}

## Boundary

- Fictional only.
- Sandbox.
- Not investment data.
- Not real company fact.
- Not for trading.
- Not production normalization.
- Promotion did not call v0.2.x scripts.
- Unsupported fields are blank or unresolved; they are not guessed.
"""
    write_json(paths["normalized_csv_audit.json"], audit)
    write_json(paths["normalized_csv_manifest.json"], manifest_out)
    paths["normalized_csv_report.md"].write_text(report, encoding="utf-8")
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Generate EXMP fictional normalized CSV sandbox.")
    parser.add_argument("--promotion-dir", required=True, type=Path)
    parser.add_argument("--review-file", required=True, type=Path)
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--manifest-file", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run_generator(
            args.promotion_dir,
            args.review_file,
            args.candidate_file,
            args.manifest_file,
            args.output_dir,
            args.overwrite,
        )
    except (FileNotFoundError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("Wrote fictional normalized CSV sandbox:")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
