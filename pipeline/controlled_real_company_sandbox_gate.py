#!/usr/bin/env python3
"""Controlled, explicit and quarantined real-company sandbox gate."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Sequence


PIPELINE_DIR = Path(__file__).resolve().parent
SKILL_DIR = PIPELINE_DIR.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(PIPELINE_DIR))

import ratio_calculator  # noqa: E402
from real_company_quarantine_policy import QUARANTINE_FLAGS, require_quarantine_flags, validate_policy, load_policy  # noqa: E402


ALLOWED_MODE = "controlled_real_company_sandbox"
TRACKED_EXAMPLE_TICKER = "MRVL"
FORBIDDEN_TERMS = ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:")
REQUIRED_REVIEW_STATUS = "approved_for_quarantine"
CSV_FIELDS = ratio_calculator.REQUIRED_FIELDS + ratio_calculator.OPTIONAL_FIELDS + [
    "ticker",
    "company",
    "quarantined",
    "not_production_data",
    "not_investment_data",
    "not_company_fact_until_verified",
    "manual_review_required",
    "not_for_trading",
    "not_for_public_release",
    "no_recommendation",
]


def utc_now() -> str:
    """Return UTC timestamp string via ratio_calculator's dependency-free clock."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def write_json(path: Path, payload: object) -> None:
    """Write JSON."""
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    """Prefer cwd-relative path."""
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path)


def confidence_rank(value: str) -> int:
    """Return confidence rank."""
    return {"low": 1, "medium": 2, "high": 3}.get(value, 0)


def validate_inputs(
    ticker: str,
    output_dir: Path,
    review_batch: dict[str, Any],
    quality_score: dict[str, Any],
    candidate_package: dict[str, Any],
    approval_policy: dict[str, Any],
    allow_real_company_sandbox: bool,
    quarantine_output: bool,
) -> list[dict[str, Any]]:
    """Validate controlled real-company quarantine inputs."""
    ticker = ticker.upper()
    if not allow_real_company_sandbox:
        raise ValueError("controlled real-company sandbox requires --allow-real-company-sandbox.")
    if not quarantine_output:
        raise ValueError("controlled real-company sandbox requires --quarantine-output.")
    validate_policy(approval_policy, ticker, output_dir)
    if review_batch.get("ticker", "").upper() != ticker:
        raise ValueError("review batch ticker mismatch.")
    if review_batch.get("batch_status") != REQUIRED_REVIEW_STATUS:
        raise ValueError("review batch status must be approved_for_quarantine.")
    if review_batch.get("production_approved") is True:
        raise ValueError("production approved review batch is rejected.")
    if quality_score.get("ticker", "").upper() != ticker:
        raise ValueError("quality score ticker mismatch.")
    if quality_score.get("overall_status") != "ready_for_quarantine":
        raise ValueError("quality score must be ready_for_quarantine.")
    if quality_score.get("checklist_complete") is not True:
        raise ValueError("quality checklist must be complete.")
    if candidate_package.get("ticker") and candidate_package.get("ticker", "").upper() != ticker:
        raise ValueError("candidate package ticker mismatch.")
    snapshot = candidate_package.get("snapshot_sha256")
    if review_batch.get("snapshot_sha256") != snapshot or quality_score.get("snapshot_sha256") != snapshot:
        raise ValueError("snapshot_sha256 mismatch across candidate, review and quality files.")
    if review_batch.get("mapping_version") != candidate_package.get("mapping_version"):
        raise ValueError("mapping version mismatch.")
    provenance_ids = {item.get("candidate_id") for item in candidate_package.get("candidates", [])}
    records = review_batch.get("records", [])
    if not records:
        raise ValueError("review batch contains no records.")
    min_rank = confidence_rank(str(approval_policy.get("minimum_confidence", "medium")))
    approved_records: list[dict[str, Any]] = []
    for record in records:
        if record.get("reviewer_decision") != "approve":
            raise ValueError(f"unresolved promoted field rejected: {record.get('normalized_field')}")
        if record.get("candidate_id") not in provenance_ids:
            raise ValueError(f"candidate package is not traceable for {record.get('candidate_id')}.")
        if confidence_rank(str(record.get("confidence", ""))) < min_rank:
            raise ValueError(f"low-confidence approval rejected: {record.get('normalized_field')}.")
        checklist = record.get("review_checklist", {})
        required_checks = ("period_checked", "unit_checked", "context_checked", "sign_checked", "scale_checked", "relationship_checked", "reviewer_notes_present")
        if any(checklist.get(item) is not True for item in required_checks):
            raise ValueError(f"missing checklist for {record.get('normalized_field')}.")
        if record.get("blocking_issues"):
            raise ValueError(f"blocking issues present for {record.get('normalized_field')}.")
        approved_records.append(record)
    return approved_records


def build_csv_row(ticker: str, review_batch: dict[str, Any], records: list[dict[str, Any]]) -> dict[str, str]:
    """Build one quarantined ratio CSV row."""
    by_field = {record["normalized_field"]: record for record in records}
    def value(field: str) -> str:
        record = by_field.get(field)
        return "" if not record else str(record.get("approved_value", record.get("extracted_value", "")))

    row = {field: "" for field in CSV_FIELDS}
    row.update(
        {
            "ticker": ticker,
            "company": str(review_batch.get("company", "")),
            "period": "FY2026",
            "currency": "USD",
            "amount_unit": "USD millions",
            "per_share_unit": "USD/share",
            "basis": "controlled_real_company_quarantine_sandbox",
            "source": "synthetic real-company-shaped review packet; not company fact until verified",
            "source_date": "2026-07-03",
            "source_status": "quarantined_review_fixture",
            "net_debt_basis": "cash_only",
            "special_items_notes": "quarantined sandbox; not production data; raw profitability must not be interpreted as company fact",
            "revenue": value("revenue"),
            "gross_profit": value("gross_profit"),
            "operating_income": value("operating_income"),
            "net_income": value("net_income"),
            "operating_cash_flow": value("operating_cash_flow"),
            "capital_expenditure": value("capital_expenditure"),
            "cash_and_equivalents": value("cash_and_equivalents"),
            "total_debt": value("total_debt"),
            "shares_diluted": value("diluted_shares"),
        }
    )
    for key, expected in QUARANTINE_FLAGS.items():
        row[key] = str(expected).lower()
    return row


def write_csv(path: Path, row: dict[str, str]) -> None:
    """Write one-row CSV."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerow(row)


def write_ratio_dry_run(input_csv: Path, output_md: Path, manifest_path: Path) -> None:
    """Run quarantined ratio dry-run in process."""
    rows = ratio_calculator.read_rows(input_csv)
    body = ratio_calculator.build_report(Path(rel(input_csv)), rows)
    banner = """# QUARANTINED REAL-COMPANY SANDBOX DRY-RUN

Not production data.
Not investment advice.
Not for trading.
Manual review required.

## Boundary

- Quarantined MRVL ratio dry-run only.
- No DCF, peer comps or implied expectations.
- No full research report.
- No investment conclusion.
- No target price, buy/sell/hold, position size or research status.

"""
    report = banner + body
    lowered = report.lower()
    for term in FORBIDDEN_TERMS:
        if term in lowered:
            raise ValueError(f"quarantined dry-run contains forbidden conclusion term: {term}")
    output_md.write_text(report, encoding="utf-8")
    write_json(
        manifest_path,
        {
            "dry_run_schema_version": "v0.6.0",
            "ticker": TRACKED_EXAMPLE_TICKER,
            "input_csv": rel(input_csv),
            "output_markdown": rel(output_md),
            "script": "ratio_calculator.py",
            "run_status": "passed",
            **QUARANTINE_FLAGS,
            "no_dcf": True,
            "no_peer_comps": True,
            "no_implied_expectations": True,
            "no_investment_conclusion": True,
            "created_at": utc_now(),
        },
    )


def run_gate(
    mode: str,
    ticker: str,
    output_dir: Path,
    review_batch_path: Path,
    quality_score_path: Path,
    candidate_package_path: Path,
    approval_policy_path: Path,
    allow_real_company_sandbox: bool,
    quarantine_output: bool,
) -> dict[str, Path]:
    """Run controlled real-company sandbox gate."""
    ticker = ticker.upper()
    if mode != ALLOWED_MODE:
        raise ValueError("mode must be controlled_real_company_sandbox.")
    if ticker != TRACKED_EXAMPLE_TICKER:
        raise ValueError("tracked v0.6 drill only allows MRVL; other tickers remain blocked.")
    output_dir = output_dir.expanduser().resolve()
    if not output_dir.as_posix().endswith("goodluck-stock-research/examples/real_company_quarantine/MRVL"):
        raise ValueError("controlled output must be goodluck-stock-research/examples/real_company_quarantine/MRVL.")
    output_dir.mkdir(parents=True, exist_ok=True)
    review_batch = load_json(review_batch_path)
    quality_score = load_json(quality_score_path)
    candidate_package = load_json(candidate_package_path)
    approval_policy = load_policy(approval_policy_path)
    require_quarantine_flags(approval_policy.get("required_quarantine_flags", {}))
    records = validate_inputs(
        ticker,
        output_dir,
        review_batch,
        quality_score,
        candidate_package,
        approval_policy,
        allow_real_company_sandbox,
        quarantine_output,
    )
    paths = {
        "quarantine_manifest": output_dir / "quarantine_manifest.json",
        "quarantined_csv": output_dir / "quarantined_normalized_sandbox.csv",
        "csv_audit": output_dir / "quarantined_csv_audit.json",
        "ratio_output": output_dir / "quarantined_ratio_dry_run.md",
        "ratio_manifest": output_dir / "quarantined_ratio_dry_run_manifest.json",
        "quarantine_report": output_dir / "quarantine_report.md",
    }
    row = build_csv_row(ticker, review_batch, records)
    write_csv(paths["quarantined_csv"], row)
    write_json(
        paths["csv_audit"],
        {
            "csv_audit_schema_version": "v0.6.0",
            "ticker": ticker,
            "approved_fields": [record["normalized_field"] for record in records],
            "review_batch_id": review_batch["review_batch_id"],
            "snapshot_sha256": review_batch["snapshot_sha256"],
            "mapping_version": review_batch["mapping_version"],
            "field_count": len(records),
            **QUARANTINE_FLAGS,
            "no_investment_conclusion": True,
            "created_at": utc_now(),
        },
    )
    write_ratio_dry_run(paths["quarantined_csv"], paths["ratio_output"], paths["ratio_manifest"])
    write_json(
        paths["quarantine_manifest"],
        {
            "quarantine_schema_version": "v0.6.0",
            "ticker": ticker,
            "company": review_batch.get("company"),
            "review_batch": rel(review_batch_path),
            "quality_score": rel(quality_score_path),
            "candidate_package": rel(candidate_package_path),
            "approval_policy": rel(approval_policy_path),
            "outputs": {key: rel(value) for key, value in paths.items()},
            "review_batch_status": review_batch.get("batch_status"),
            "quality_status": quality_score.get("overall_status"),
            "approved_fields": [record["normalized_field"] for record in records],
            **QUARANTINE_FLAGS,
            "no_dcf": True,
            "no_peer_comps": True,
            "no_implied_expectations": True,
            "no_investment_conclusion": True,
            "created_at": utc_now(),
        },
    )
    paths["quarantine_report"].write_text(
        f"""# MRVL Controlled Real-Company Quarantine Report

## Boundary

- quarantined=true
- not_production_data=true
- not_investment_data=true
- not_company_fact_until_verified=true
- manual_review_required=true
- not_for_trading=true
- not_for_public_release=true
- no_recommendation=true

## Result

- Ticker: `{ticker}`
- Review batch status: `{review_batch.get('batch_status')}`
- Quality status: `{quality_score.get('overall_status')}`
- Approved quarantine fields: `{', '.join(record['normalized_field'] for record in records)}`
- Ratio dry-run: `generated`

## Hard Limits

- No DCF.
- No peer comps.
- No implied expectations.
- No full research report.
- No investment conclusion.
- No target price, buy/sell/hold, position size or research status.
""",
        encoding="utf-8",
    )
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI args."""
    parser = argparse.ArgumentParser(description="Run controlled real-company quarantine sandbox gate.")
    parser.add_argument("--mode", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--review-batch", required=True, type=Path)
    parser.add_argument("--quality-score", required=True, type=Path)
    parser.add_argument("--candidate-package", required=True, type=Path)
    parser.add_argument("--approval-policy", required=True, type=Path)
    parser.add_argument("--allow-real-company-sandbox", action="store_true")
    parser.add_argument("--quarantine-output", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run_gate(
            args.mode,
            args.ticker,
            args.output_dir,
            args.review_batch,
            args.quality_score,
            args.candidate_package,
            args.approval_policy,
            args.allow_real_company_sandbox,
            args.quarantine_output,
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("Wrote controlled real-company quarantine sandbox:")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
