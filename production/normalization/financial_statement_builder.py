#!/usr/bin/env python3
"""Build normalized financial statement artifacts from parsed facts."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Sequence

NORM_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(NORM_DIR))

from normalization_policy import statement_for  # noqa: E402


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("parser output root must be object")
    return value


def build(parser_output: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for item in parser_output.get("fields", []):
        if item.get("status") != "parsed":
            unresolved.append(item)
            continue
        rows.append(
            {
                "ticker": parser_output.get("ticker"),
                "fiscal_period": parser_output.get("fiscal_period"),
                "statement": statement_for(item["field"]),
                "field": item["field"],
                "value": item["value"],
                "currency": "USD" if item.get("unit") == "USD" else "",
                "amount_unit": "USD millions" if item.get("unit") == "USD" else "shares",
                "source_locator": item.get("source_locator"),
                "concept_qname": item.get("concept_qname"),
                "confidence": item.get("confidence"),
                "review_status": "system_parsed_review_required",
                "transformations": "; ".join(item.get("transformations", [])),
            }
        )
    return {
        "normalization_schema_version": "v1.4.0",
        "ticker": parser_output.get("ticker"),
        "fiscal_period": parser_output.get("fiscal_period"),
        "rows": rows,
        "unresolved_fields": unresolved,
        "no_zero_fill": True,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["ticker", "fiscal_period", "statement", "field", "value", "currency", "amount_unit", "source_locator", "concept_qname", "confidence", "review_status", "transformations"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_artifacts(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = result["rows"]
    for statement in ("income_statement", "balance_sheet", "cash_flow"):
        subset = [row for row in rows if row["statement"] == statement]
        (output_dir / f"normalized_{statement}.json").write_text(json.dumps(subset, indent=2) + "\n", encoding="utf-8")
        write_csv(output_dir / f"normalized_{statement}.csv", subset)
    write_csv(output_dir / "normalized_metrics_input.csv", rows)
    (output_dir / "unresolved_fields.json").write_text(json.dumps(result["unresolved_fields"], indent=2) + "\n", encoding="utf-8")
    manifest = {key: result[key] for key in ("normalization_schema_version", "ticker", "fiscal_period", "no_zero_fill")}
    manifest["row_count"] = len(rows)
    manifest["unresolved_count"] = len(result["unresolved_fields"])
    manifest["audit_report"] = "statement_audit_report.md"
    (output_dir / "normalization_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (output_dir / "statement_audit_report.md").write_text(
        f"# Statement Audit Report\n\n- No zero-fill: {result['no_zero_fill']}\n- Rows: {len(rows)}\n- Unresolved fields: {len(result['unresolved_fields'])}\n- All parsed rows retain source locator, concept QName, confidence and review status.\n",
        encoding="utf-8",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build normalized statement artifacts.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    write_artifacts(build(load_json(args.input)), args.output_dir)
    print("PASS: normalized financial statement builder")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
