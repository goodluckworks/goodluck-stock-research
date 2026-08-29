#!/usr/bin/env python3
"""Run ratio_calculator as an in-process EXMP sandbox dry-run only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import ensure_distinct_paths, load_json, prepare_output_dir, relative_or_absolute, utc_now, write_json
from unresolved_field_reporter import render_unresolved_section


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ratio_calculator  # noqa: E402


OUTPUTS = (
    "ratio_output_sandbox.md",
    "v02_dry_run_manifest.json",
    "v02_dry_run_report.md",
)
SANDBOX_STATUS = "fictional_sandbox_not_investment_data"
ALLOWED_TICKER = "EXMP"
FORBIDDEN_TERMS = (
    "target price:",
    "buy:",
    "sell:",
    "hold:",
    "position size:",
    "research status:",
)


def read_csv_first_row(path: Path) -> dict[str, str]:
    """Read the first CSV row."""
    if not path.is_file():
        raise FileNotFoundError(f"Input CSV does not exist: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    if not rows:
        raise ValueError("Sandbox CSV contains no data rows.")
    return {key: value for key, value in rows[0].items()}


def validate_sandbox_input(input_csv: Path) -> dict[str, Any]:
    """Validate CSV manifest and row before ratio dry-run."""
    manifest_path = input_csv.parent / "normalized_csv_manifest.json"
    manifest = load_json(manifest_path)
    row = read_csv_first_row(input_csv)
    if manifest.get("ticker") != ALLOWED_TICKER:
        raise ValueError("v0.2 sandbox dry-run allows only EXMP.")
    if manifest.get("sandbox_status") != SANDBOX_STATUS:
        raise ValueError("Input manifest is not a fictional sandbox CSV.")
    if manifest.get("no_investment_conclusion") is not True:
        raise ValueError("Input manifest must set no_investment_conclusion=true.")
    if manifest.get("prohibited_real_company_flag") is not False:
        raise ValueError("Real-company sandbox dry-run is blocked.")
    impact = manifest.get("downstream_impact", {})
    if impact and impact.get("ratio_dry_run_allowed") is not True:
        missing = ", ".join(impact.get("missing_minimum_fields", []))
        raise ValueError(f"Sandbox CSV missing minimum ratio dry-run fields: {missing}")
    if row.get("sandbox_status") != SANDBOX_STATUS:
        raise ValueError("Input CSV row is missing sandbox_status.")
    for field in ("fictional", "not_investment_data", "not_company_fact", "not_for_trading", "not_production_research"):
        if row.get(field) != "true":
            raise ValueError(f"Input CSV row missing {field}=true.")
    return manifest


def run_dry_run(input_csv: Path, output_dir: Path, overwrite: bool = False) -> dict[str, Path]:
    """Run EXMP sandbox ratio dry-run in-process without shell execution."""
    ensure_distinct_paths(input_csv, output_dir)
    input_csv = input_csv.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    manifest = validate_sandbox_input(input_csv)
    overwrite_used = prepare_output_dir(output_dir, overwrite)
    paths = {name: output_dir / name for name in OUTPUTS}
    rows = ratio_calculator.read_rows(input_csv)
    report_body = ratio_calculator.build_report(input_csv, rows)
    banner = f"""# Sandbox Ratio Dry-Run Banner

- Sandbox status: `{SANDBOX_STATUS}`
- Ticker: `{ALLOWED_TICKER}`
- Fictional only.
- Not investment data.
- Not company fact.
- Not for trading.
- Not production research.
- Partial-field caution: missing, unresolved and blocked fields remain blank and are never filled with zero.
- No target price, buy/sell/hold, position size or research status.

{render_unresolved_section(manifest)}

"""
    report = banner + report_body
    lower_report = report.lower()
    for term in FORBIDDEN_TERMS:
        if term in lower_report:
            raise ValueError(f"Dry-run output contains forbidden conclusion term: {term}")
    paths["ratio_output_sandbox.md"].write_text(report, encoding="utf-8")
    dry_run_id = f"v02-ratio-sandbox-{ALLOWED_TICKER.lower()}-{manifest['snapshot_sha256'][:12]}"
    manifest_out = {
        "dry_run_id": dry_run_id,
        "input_csv": relative_or_absolute(input_csv),
        "input_manifest": relative_or_absolute(input_csv.parent / "normalized_csv_manifest.json"),
        "output_markdown": relative_or_absolute(paths["ratio_output_sandbox.md"]),
        "script": "ratio_calculator.py",
        "run_status": "passed",
        "sandbox_status": SANDBOX_STATUS,
        "no_investment_conclusion": True,
        "created_at": utc_now(),
        "source_promotion_id": manifest["source_promotion_id"],
        "source_review_batch_id": manifest["source_review_batch_id"],
        "mapping_version": manifest["mapping_version"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "available_ratios": manifest.get("downstream_impact", {}).get("available_ratios", []),
        "unavailable_ratios": manifest.get("downstream_impact", {}).get("unavailable_ratios", []),
        "missing_inputs": manifest.get("downstream_impact", {}).get("missing_minimum_fields", []),
        "overwrite_used": overwrite_used,
    }
    dry_report = f"""# v0.2.x Sandbox Dry-Run Report

## Summary

- Dry-run ID: `{dry_run_id}`
- Input CSV: `{relative_or_absolute(input_csv)}`
- Output Markdown: `{relative_or_absolute(paths['ratio_output_sandbox.md'])}`
- Script: `ratio_calculator.py`
- Run status: `passed`
- Sandbox status: `{SANDBOX_STATUS}`
- Available ratios: `{len(manifest.get('downstream_impact', {}).get('available_ratios', []))}`
- Unavailable ratios: `{len(manifest.get('downstream_impact', {}).get('unavailable_ratios', []))}`
- Overwrite used: `{str(overwrite_used).lower()}`

## Boundary

- EXMP fictional sandbox only.
- Not investment data.
- Not company fact.
- Not for trading.
- Not production research.
- No DCF, peer comps or implied expectations script was run.
- No target price, buy/sell/hold, position size or research status.
"""
    write_json(paths["v02_dry_run_manifest.json"], manifest_out)
    paths["v02_dry_run_report.md"].write_text(dry_report, encoding="utf-8")
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run EXMP v0.2 ratio dry-run from fictional sandbox CSV.")
    parser.add_argument("--input-csv", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run_dry_run(args.input_csv, args.output_dir, args.overwrite)
    except (FileNotFoundError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("Wrote EXMP sandbox ratio dry-run:")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
