#!/usr/bin/env python3
"""Package a local official filing file into an auditable evidence bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence


ADAPTER_NAME = "local_official_filing_adapter"
ADAPTER_VERSION = "v0.3.1"
SOURCE_STATUSES = {
    "verified",
    "partially_verified",
    "indicative",
    "unverified",
    "fictional_sample",
}
DATA_STATUSES = {
    "available",
    "partial",
    "stale",
    "conflicting",
    "superseded",
    "missing",
    "not_applicable",
}
UNRESOLVED_FINANCIAL_FIELDS = (
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "total_debt",
    "diluted_shares",
)
DISCLAIMER = (
    "This evidence package does not contain an investment conclusion, target "
    "price, portfolio action, or trading instruction."
)


@dataclass(frozen=True)
class AdapterConfig:
    """Validated local adapter inputs."""

    input_file: Path
    company: str
    ticker: str
    source_type: str
    form_type: str
    filing_date: str
    reporting_period: str
    fiscal_year: str
    fiscal_quarter: str
    source_url: str
    currency: str
    amount_unit: str
    per_share_unit: str
    output_dir: Path
    source_status: str = "verified"
    data_status: str = "available"
    retrieved_at: str = ""
    notes: str = "none"
    overwrite: bool = False


def utc_now() -> str:
    """Return an ISO 8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_timestamp(value: str) -> str:
    """Validate an ISO 8601 timestamp and require timezone information."""
    candidate = value or utc_now()
    normalized = candidate.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            f"retrieved_at must be ISO 8601 with timezone; got {candidate!r}."
        ) from exc
    if parsed.tzinfo is None:
        raise ValueError("retrieved_at must include timezone information.")
    return candidate


def require_text(name: str, value: str) -> str:
    """Return stripped text or raise a clear validation error."""
    stripped = value.strip()
    if not stripped:
        raise ValueError(f"{name} must not be blank.")
    return stripped


def sha256_file(path: Path) -> str:
    """Calculate SHA-256 for a local file without loading it all into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_id(value: str) -> str:
    """Return a filesystem- and manifest-friendly identifier."""
    cleaned = "".join(
        character.lower() if character.isalnum() else "-"
        for character in value.strip()
    )
    return "-".join(part for part in cleaned.split("-") if part) or "unknown"


def display_path(path: Path) -> str:
    """Prefer a repository-relative path when the path is under the cwd."""
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(resolved)


def write_json(path: Path, payload: object) -> None:
    """Write deterministic, human-readable JSON."""
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def validate_config(config: AdapterConfig) -> AdapterConfig:
    """Validate local-only boundaries and required metadata."""
    input_file = config.input_file.expanduser().resolve()
    output_dir = config.output_dir.expanduser().resolve()
    if not input_file.is_file():
        raise FileNotFoundError(f"Input filing does not exist: {input_file}")
    if output_dir == input_file:
        raise ValueError("output_dir cannot equal input_file.")

    required = {
        "company": config.company,
        "ticker": config.ticker,
        "source_type": config.source_type,
        "form_type": config.form_type,
        "filing_date": config.filing_date,
        "reporting_period": config.reporting_period,
        "fiscal_year": config.fiscal_year,
        "fiscal_quarter": config.fiscal_quarter,
        "source_url": config.source_url,
        "currency": config.currency,
        "amount_unit": config.amount_unit,
        "per_share_unit": config.per_share_unit,
        "source_status": config.source_status,
        "data_status": config.data_status,
    }
    cleaned = {name: require_text(name, value) for name, value in required.items()}
    if cleaned["source_type"] != "official_filing":
        raise ValueError(
            "source_type must be 'official_filing' for this adapter."
        )
    if cleaned["source_status"] not in SOURCE_STATUSES:
        raise ValueError(
            f"Unsupported source_status: {cleaned['source_status']!r}."
        )
    if cleaned["data_status"] not in DATA_STATUSES:
        raise ValueError(f"Unsupported data_status: {cleaned['data_status']!r}.")
    retrieved_at = parse_timestamp(config.retrieved_at)

    return AdapterConfig(
        input_file=input_file,
        company=cleaned["company"],
        ticker=cleaned["ticker"].upper(),
        source_type=cleaned["source_type"],
        form_type=cleaned["form_type"],
        filing_date=cleaned["filing_date"],
        reporting_period=cleaned["reporting_period"],
        fiscal_year=cleaned["fiscal_year"],
        fiscal_quarter=cleaned["fiscal_quarter"],
        source_url=cleaned["source_url"],
        currency=cleaned["currency"],
        amount_unit=cleaned["amount_unit"],
        per_share_unit=cleaned["per_share_unit"],
        output_dir=output_dir,
        source_status=cleaned["source_status"],
        data_status=cleaned["data_status"],
        retrieved_at=retrieved_at,
        notes=config.notes.strip() or "none",
        overwrite=config.overwrite,
    )


def prepare_output_dir(config: AdapterConfig) -> bool:
    """Create the output directory and enforce no-silent-overwrite behavior."""
    output_dir = config.output_dir
    existing_files = list(output_dir.iterdir()) if output_dir.is_dir() else []
    if existing_files and not config.overwrite:
        raise FileExistsError(
            f"Output directory is not empty: {output_dir}. "
            "Use --overwrite to update generated manifests while preserving "
            "versioned raw snapshots."
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    return bool(existing_files and config.overwrite)


def build_unresolved_fields() -> list[dict[str, str]]:
    """Return the deliberately unresolved financial extraction fields."""
    return [
        {
            "field_name": field,
            "reason": (
                "v0.3.1 packages local filing evidence only and does not perform "
                "full financial or XBRL extraction."
            ),
            "required_for": "financials_input_schema and downstream research",
            "severity": "blocking_for_normalized_financials",
            "suggested_manual_action": (
                "Manually normalize this field from the packaged official filing "
                "or use a separately approved extraction adapter."
            ),
        }
        for field in UNRESOLVED_FINANCIAL_FIELDS
    ]


def build_report(
    config: AdapterConfig,
    snapshot_path: Path,
    checksum: str,
    source_id: str,
    snapshot_id: str,
    overwrite_used: bool,
    generated_files: Sequence[str],
) -> str:
    """Build the adapter run Markdown report."""
    unresolved_lines = "\n".join(
        f"- `{field}`: requires manual normalization."
        for field in UNRESOLVED_FINANCIAL_FIELDS
    )
    generated_lines = "\n".join(f"- `{name}`" for name in generated_files)
    return f"""# Local Official Filing Adapter Run

## Run Summary

- Adapter: `{ADAPTER_NAME}`
- Version: `{ADAPTER_VERSION}`
- Input file: `{display_path(config.input_file)}`
- Output directory: `{display_path(config.output_dir)}`
- Raw snapshot: `{display_path(snapshot_path)}`
- SHA-256: `{checksum}`
- Source ID: `{source_id}`
- Snapshot ID: `{snapshot_id}`
- Retrieved at: `{config.retrieved_at}`
- Overwrite used: `{str(overwrite_used).lower()}`

## Source Metadata

- Company: {config.company}
- Ticker: {config.ticker}
- Source type: {config.source_type}
- Form type: {config.form_type}
- Filing date: {config.filing_date}
- Reporting period: {config.reporting_period}
- Fiscal year / quarter: {config.fiscal_year} / {config.fiscal_quarter}
- Source URL string: `{config.source_url}`
- Currency: {config.currency}
- Amount unit: {config.amount_unit}
- Per-share unit: {config.per_share_unit}
- Source status: {config.source_status}
- Data status: {config.data_status}
- Verification basis: user-supplied metadata plus local file checksum only
- Notes: {config.notes}

The source URL is retained only as citation metadata. This adapter does not open
URLs or perform network access. The adapter does not independently verify that
the local file is authentic, complete, or the latest effective filing.

## Generated Files

{generated_lines}

## Safety Boundary

- Local input only.
- No network request, SEC API, live EDGAR fetch, browser automation, or web scraping.
- No credential, API key, token, password, secret, or environment-variable read.
- No subprocess, broker connection, order routing, or trading execution.
- {DISCLAIMER}

## Unresolved Fields

{unresolved_lines}

## Next Manual Step

Review the raw snapshot and source manifest, then manually map supported values
into the appropriate v0.2.x input schema. A future extraction adapter would
require separate approval and its own field-level tests.

## Mapping to v0.2.x

- `financials_input_schema`: financial fields remain unresolved.
- `valuation_input_schema`: requires separate market and financial evidence.
- `peer_comps_input_schema`: requires separate market snapshots and comparability judgment.
- `assumptions_schema`: analyst assumptions must be supplied separately.
- `normalized_input_draft.json` records this evidence-only status and contains no financial values.
"""


def run_adapter(config: AdapterConfig) -> dict[str, Path]:
    """Create an evidence package from one local filing file."""
    config = validate_config(config)
    overwrite_used = prepare_output_dir(config)
    checksum = sha256_file(config.input_file)
    ticker_id = safe_id(config.ticker)
    form_id = safe_id(config.form_type)
    date_id = safe_id(config.filing_date)
    source_id = f"{ticker_id}-{form_id}-{date_id}-{checksum[:12]}"
    snapshot_id = f"raw-{source_id}"

    raw_dir = config.output_dir / "raw"
    raw_dir.mkdir(exist_ok=True)
    suffix = config.input_file.suffix.lower() or ".bin"
    snapshot_path = raw_dir / f"{snapshot_id}{suffix}"
    if not snapshot_path.exists():
        shutil.copy2(config.input_file, snapshot_path)
    elif sha256_file(snapshot_path) != checksum:
        raise ValueError(
            f"Existing raw snapshot checksum mismatch: {snapshot_path}"
        )

    created_at = utc_now()
    content_type = mimetypes.guess_type(config.input_file.name)[0] or (
        "application/octet-stream"
    )
    raw_manifest = {
        "snapshot_id": snapshot_id,
        "adapter_name": ADAPTER_NAME,
        "adapter_version": ADAPTER_VERSION,
        "input_file": display_path(config.input_file),
        "raw_snapshot_path": display_path(snapshot_path),
        "sha256": checksum,
        "created_at": created_at,
        "source_url": config.source_url,
        "immutable": True,
        "overwrite_used": overwrite_used,
        "content_type": content_type,
        "byte_size": snapshot_path.stat().st_size,
        "notes": config.notes,
    }
    source_manifest = {
        "source_id": source_id,
        "source_name": f"{config.company} {config.form_type} {config.reporting_period}",
        "source_type": config.source_type,
        "source_url": config.source_url,
        "retrieved_at": config.retrieved_at,
        "source_date": config.filing_date,
        "filing_date": config.filing_date,
        "form_type": config.form_type,
        "reporting_period": config.reporting_period,
        "fiscal_period": config.reporting_period,
        "fiscal_year": config.fiscal_year,
        "fiscal_quarter": config.fiscal_quarter,
        "currency": config.currency,
        "amount_unit": config.amount_unit,
        "per_share_unit": config.per_share_unit,
        "market_session": "not_applicable",
        "source_status": config.source_status,
        "data_status": config.data_status,
        "verification_basis": (
            "user_supplied_metadata_and_local_file_checksum_only"
        ),
        "confidence": (
            "high"
            if config.source_status == "verified"
            else "medium"
            if config.source_status in {"partially_verified", "indicative"}
            else "low"
        ),
        "data_nature": "regulatory_filing",
        "transformation_notes": (
            "Local file copied byte-for-byte to a checksum-addressed raw snapshot; "
            "no financial extraction performed."
        ),
        "notes": config.notes,
    }
    field_provenance = {
        "records": [
            {
                "field_name": "raw_filing_text",
                "value_status": "raw_snapshot_available",
                "source_id": source_id,
                "source_field_name": "full filing text / local excerpt",
                "source_locator": display_path(snapshot_path),
                "transformation": "raw file copied and checksum recorded",
                "confidence": "high",
                "notes": (
                    "Evidence packaging only; no financial field was inferred "
                    "from the filing text."
                ),
            }
        ]
    }
    unresolved_payload = {
        "unresolved_fields": build_unresolved_fields(),
        "warnings": [
            (
                "Financial fields remain unresolved because v0.3.1 does not "
                "perform full filing or XBRL extraction."
            ),
            (
                "Source and data status are user-supplied metadata. The adapter "
                "records checksum integrity but does not verify filing authenticity, "
                "completeness, or latest-effective status."
            )
        ],
        "errors": [],
    }
    normalized_draft = {
        "status": "draft_unpopulated",
        "reason": (
            "This adapter packages evidence only; financial fields require "
            "manual normalization or a separately approved extraction adapter."
        ),
        "target_schemas": [
            "financials_input_schema",
            "valuation_input_schema",
            "peer_comps_input_schema",
            "assumptions_schema",
        ],
    }

    output_paths = {
        "raw_snapshot_manifest.json": config.output_dir
        / "raw_snapshot_manifest.json",
        "source_manifest.json": config.output_dir / "source_manifest.json",
        "field_provenance.json": config.output_dir / "field_provenance.json",
        "unresolved_fields.json": config.output_dir / "unresolved_fields.json",
        "normalized_input_draft.json": config.output_dir
        / "normalized_input_draft.json",
        "adapter_run_report.md": config.output_dir / "adapter_run_report.md",
    }
    write_json(output_paths["raw_snapshot_manifest.json"], raw_manifest)
    write_json(output_paths["source_manifest.json"], source_manifest)
    write_json(output_paths["field_provenance.json"], field_provenance)
    write_json(output_paths["unresolved_fields.json"], unresolved_payload)
    write_json(output_paths["normalized_input_draft.json"], normalized_draft)
    output_paths["adapter_run_report.md"].write_text(
        build_report(
            config=config,
            snapshot_path=snapshot_path,
            checksum=checksum,
            source_id=source_id,
            snapshot_id=snapshot_id,
            overwrite_used=overwrite_used,
            generated_files=tuple(output_paths),
        ),
        encoding="utf-8",
    )
    return output_paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Package one local official filing file into a local evidence bundle. "
            "No network access or financial extraction is performed."
        )
    )
    parser.add_argument("--input-file", required=True, type=Path)
    parser.add_argument("--company", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--source-type", required=True)
    parser.add_argument("--form-type", required=True)
    parser.add_argument("--filing-date", required=True)
    parser.add_argument("--reporting-period", required=True)
    parser.add_argument("--fiscal-year", required=True)
    parser.add_argument("--fiscal-quarter", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--currency", required=True)
    parser.add_argument("--amount-unit", required=True)
    parser.add_argument("--per-share-unit", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--source-status", default="verified")
    parser.add_argument("--data-status", default="available")
    parser.add_argument("--retrieved-at", default="")
    parser.add_argument("--notes", default="none")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Update generated manifests/reports in a non-empty output directory. "
            "Checksum-addressed raw snapshots are preserved."
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the adapter CLI."""
    args = parse_args(argv)
    config = AdapterConfig(
        input_file=args.input_file,
        company=args.company,
        ticker=args.ticker,
        source_type=args.source_type,
        form_type=args.form_type,
        filing_date=args.filing_date,
        reporting_period=args.reporting_period,
        fiscal_year=args.fiscal_year,
        fiscal_quarter=args.fiscal_quarter,
        source_url=args.source_url,
        currency=args.currency,
        amount_unit=args.amount_unit,
        per_share_unit=args.per_share_unit,
        output_dir=args.output_dir,
        source_status=args.source_status,
        data_status=args.data_status,
        retrieved_at=args.retrieved_at,
        notes=args.notes,
        overwrite=args.overwrite,
    )
    try:
        output_paths = run_adapter(config)
    except (FileNotFoundError, FileExistsError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote local filing evidence package: {config.output_dir}")
    for path in output_paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
