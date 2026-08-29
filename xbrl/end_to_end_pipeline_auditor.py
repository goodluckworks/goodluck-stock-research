#!/usr/bin/env python3
"""Audit the EXMP fictional XBRL-to-v0.2 sandbox pipeline end to end."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import REAL_TICKERS, ensure_distinct_paths, load_json, relative_or_absolute, utc_now


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


def find_forbidden(value: Any, path: str = "$") -> list[str]:
    """Return forbidden field locations."""
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


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read CSV rows."""
    if not path.is_file():
        raise FileNotFoundError(f"CSV does not exist: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def add_check(checks: list[dict[str, Any]], name: str, passed: bool, evidence: str) -> None:
    """Append one audit check."""
    checks.append({"check": name, "passed": passed, "evidence": evidence})


def audit_pipeline(
    candidate_dir: Path,
    quality_dir: Path,
    review_dir: Path,
    promotion_dir: Path,
    normalized_dir: Path,
    dry_run_dir: Path,
    output_report: Path,
) -> list[str]:
    """Audit pipeline and write a Markdown report."""
    ensure_distinct_paths(candidate_dir, quality_dir, review_dir, promotion_dir, normalized_dir, dry_run_dir, output_report)
    manifest = load_json(candidate_dir / "extraction_run_manifest.json")
    candidates = load_json(candidate_dir / "extraction_candidates.json")
    quality = load_json(quality_dir / "review_quality_score.json")
    review = load_json(review_dir / "normalized_review_batch.json")
    promotion_manifest = load_json(promotion_dir / "promotion_manifest.json")
    draft = load_json(promotion_dir / "approved_normalized_draft.json")
    csv_manifest = load_json(normalized_dir / "normalized_csv_manifest.json")
    csv_audit = load_json(normalized_dir / "normalized_csv_audit.json")
    dry_manifest = load_json(dry_run_dir / "v02_dry_run_manifest.json")
    dry_output = dry_run_dir / "ratio_output_sandbox.md"
    csv_path = normalized_dir / "normalized_financials_sandbox.csv"
    headers, rows = read_csv(csv_path)
    errors: list[str] = []
    checks: list[dict[str, Any]] = []
    docs = {
        "manifest": manifest,
        "candidates": candidates,
        "quality": quality,
        "review": review,
        "promotion_manifest": promotion_manifest,
        "draft": draft,
        "csv_manifest": csv_manifest,
        "csv_audit": csv_audit,
        "dry_manifest": dry_manifest,
    }
    for name, doc in docs.items():
        hits = find_forbidden(doc)
        if hits:
            errors.append(f"{name} contains forbidden fields: {hits}")
    ticker = str(manifest.get("ticker", "")).upper()
    add_check(checks, "EXMP fictional only", ticker == ALLOWED_TICKER and ticker not in REAL_TICKERS, ticker)
    if ticker != ALLOWED_TICKER:
        errors.append(f"End-to-end sandbox allows only {ALLOWED_TICKER}; got {ticker}.")
    if manifest.get("fictional_company") is False:
        errors.append("Manifest cannot be marked non-fictional for sandbox audit.")
    shared_mapping = manifest.get("mapping_version")
    shared_snapshot = manifest.get("snapshot_sha256")
    for name, doc in docs.items():
        if name == "dry_manifest":
            continue
        if doc.get("mapping_version") != shared_mapping:
            errors.append(f"{name} mapping_version mismatch.")
        if doc.get("snapshot_sha256") != shared_snapshot:
            errors.append(f"{name} snapshot_sha256 mismatch.")
    add_check(checks, "mapping_version chain", not any("mapping_version mismatch" in e for e in errors), str(shared_mapping))
    add_check(checks, "snapshot_sha256 chain", not any("snapshot_sha256 mismatch" in e for e in errors), str(shared_snapshot))
    if quality.get("extraction_run_id") != manifest.get("run_id"):
        errors.append("quality extraction_run_id mismatch.")
    if review.get("extraction_run_id") != manifest.get("run_id"):
        errors.append("review extraction_run_id mismatch.")
    if promotion_manifest.get("extraction_run_id") != manifest.get("run_id"):
        errors.append("promotion extraction_run_id mismatch.")
    if promotion_manifest.get("review_batch_id") != review.get("review_batch_id"):
        errors.append("promotion review_batch_id mismatch.")
    if csv_manifest.get("source_review_batch_id") != review.get("review_batch_id"):
        errors.append("CSV manifest review_batch_id mismatch.")
    if csv_manifest.get("source_promotion_id") != promotion_manifest.get("promotion_id"):
        errors.append("CSV manifest promotion_id mismatch.")
    if dry_manifest.get("source_promotion_id") != promotion_manifest.get("promotion_id"):
        errors.append("dry-run promotion_id mismatch.")
    add_check(checks, "ID chain", not any("mismatch" in e for e in errors), "run/review/promotion/csv/dry-run IDs checked")
    if csv_manifest.get("sandbox_status") != SANDBOX_STATUS or dry_manifest.get("sandbox_status") != SANDBOX_STATUS:
        errors.append("sandbox_status mismatch.")
    if csv_manifest.get("no_investment_conclusion") is not True or dry_manifest.get("no_investment_conclusion") is not True:
        errors.append("no_investment_conclusion flag missing.")
    if not rows:
        errors.append("normalized CSV has no data rows.")
    row = rows[0] if rows else {}
    for flag in ("fictional", "not_investment_data", "not_company_fact", "not_for_trading", "not_production_research"):
        if row.get(flag) != "true":
            errors.append(f"CSV row missing {flag}=true.")
    add_check(checks, "sandbox labels", not any("sandbox" in e or "flag" in e for e in errors), "CSV and dry-run labels checked")
    promoted_fields = {
        field["normalized_field"]: field
        for field in draft.get("fields", [])
        if field.get("reviewer_decision") in {"approve", "adjust"}
    }
    excluded_fields = {
        field["normalized_field"]
        for field in draft.get("excluded_records", [])
    }
    audit_by_field = {
        record["normalized_field"]: record
        for record in csv_audit.get("field_audit_records", [])
    }
    for field, promoted in promoted_fields.items():
        if field not in headers:
            errors.append(f"Promoted field missing from CSV headers: {field}.")
            continue
        if str(row.get(field, "")) != str(promoted.get("approved_value")):
            errors.append(f"CSV value mismatch for {field}.")
        audit_record = audit_by_field.get(field)
        if audit_record is None:
            errors.append(f"Missing audit record for populated field: {field}.")
        elif audit_record.get("candidate_id") != promoted.get("candidate_id") or audit_record.get("review_record_id") != promoted.get("review_record_id"):
            errors.append(f"Audit reference mismatch for {field}.")
        if not str(promoted.get("transformation", "")).strip():
            errors.append(f"Missing transformation for {field}.")
    for field in excluded_fields:
        if row.get(field):
            errors.append(f"Unresolved/rejected field populated in CSV: {field}.")
    add_check(checks, "CSV values and audit records", not any("CSV value mismatch" in e or "audit" in e.lower() for e in errors), "approved values and audit references checked")
    dry_text = dry_output.read_text(encoding="utf-8") if dry_output.is_file() else ""
    if "Sandbox Ratio Dry-Run Banner" not in dry_text or SANDBOX_STATUS not in dry_text:
        errors.append("dry-run output missing sandbox banner.")
    lowered = dry_text.lower()
    for forbidden in ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:"):
        if forbidden in lowered:
            errors.append(f"dry-run output contains forbidden conclusion text: {forbidden}")
    add_check(checks, "dry-run output", not any("dry-run output" in e for e in errors), relative_or_absolute(dry_output))
    passed = not errors
    rows_md = "\n".join(
        f"| {item['check']} | {'Pass' if item['passed'] else 'Fail'} | {item['evidence']} |"
        for item in checks
    )
    error_md = "\n".join(f"- {error}" for error in errors) if errors else "- None"
    report = f"""# EXMP End-to-End XBRL Sandbox Audit

## Summary

- Audit passed: `{str(passed).lower()}`
- Generated at: `{utc_now()}`
- Candidate dir: `{relative_or_absolute(candidate_dir)}`
- Quality dir: `{relative_or_absolute(quality_dir)}`
- Review dir: `{relative_or_absolute(review_dir)}`
- Promotion dir: `{relative_or_absolute(promotion_dir)}`
- Normalized dir: `{relative_or_absolute(normalized_dir)}`
- Dry-run dir: `{relative_or_absolute(dry_run_dir)}`

## Checks

| Check | Result | Evidence |
|---|---:|---|
{rows_md}

## Errors

{error_md}

## Boundary

- EXMP fictional sandbox only.
- No real-company normalized CSV.
- No real-company v0.2.x dry-run.
- No live extraction or production parser claim.
- No investment conclusion, target price, buy/sell/hold, position size or research status.
"""
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(report, encoding="utf-8")
    return errors


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Audit EXMP fictional sandbox pipeline end to end.")
    parser.add_argument("--candidate-dir", required=True, type=Path)
    parser.add_argument("--quality-dir", required=True, type=Path)
    parser.add_argument("--review-dir", required=True, type=Path)
    parser.add_argument("--promotion-dir", required=True, type=Path)
    parser.add_argument("--normalized-dir", required=True, type=Path)
    parser.add_argument("--dry-run-dir", required=True, type=Path)
    parser.add_argument("--output-report", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        errors = audit_pipeline(
            args.candidate_dir,
            args.quality_dir,
            args.review_dir,
            args.promotion_dir,
            args.normalized_dir,
            args.dry_run_dir,
            args.output_report,
        )
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote end-to-end audit report: {args.output_report}")
    print(f"audit_passed={str(not errors).lower()}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
