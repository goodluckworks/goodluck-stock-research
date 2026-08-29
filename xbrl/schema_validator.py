#!/usr/bin/env python3
"""Validate v0.3.5 XBRL JSON packages with standard-library schema files."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import REAL_TICKERS, ensure_distinct_paths, load_json, relative_or_absolute, utc_now


SCHEMA_TO_PACKAGE_FILE = {
    "extraction_run_manifest_schema": "extraction_run_manifest.json",
    "extraction_candidate_schema": "extraction_candidates.json",
    "unresolved_field_schema": "unresolved_fields.json",
    "field_provenance_schema": "field_provenance.json",
    "mapping_registry_schema": None,
    "review_batch_schema": None,
    "promotion_manifest_schema": "promotion_manifest.json",
    "approved_normalized_draft_schema": "approved_normalized_draft.json",
}


def read_json_any(path: Path) -> Any:
    """Read any JSON value from a local file."""
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def type_matches(value: Any, expected: str) -> bool:
    """Return whether a JSON value matches one schema type."""
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    raise ValueError(f"Unsupported schema type: {expected}")


def validate_node(value: Any, schema: dict[str, Any], path: str) -> list[str]:
    """Validate one JSON node recursively."""
    errors: list[str] = []
    expected_types = schema.get("type", schema.get("root_type"))
    if expected_types is not None:
        if isinstance(expected_types, str):
            expected_list = [expected_types]
        elif isinstance(expected_types, list):
            expected_list = expected_types
        else:
            errors.append(f"{path}: type rule must be string or array.")
            expected_list = []
        if expected_list and not any(type_matches(value, item) for item in expected_list):
            errors.append(f"{path}: expected type {expected_list}, got {type(value).__name__}.")
            return errors

    if schema.get("nonblank") is True and isinstance(value, str) and not value.strip():
        errors.append(f"{path}: string must be nonblank.")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not in enum {schema['enum']!r}.")
    if schema.get("finite") is True:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            errors.append(f"{path}: value must be numeric and finite.")
        elif not math.isfinite(float(value)):
            errors.append(f"{path}: value must be finite.")

    if isinstance(value, dict):
        if schema.get("block_real_company_promotion") is True:
            ticker = str(value.get("ticker", "")).upper()
            if ticker in REAL_TICKERS and value.get("allow_real_company_promotion_used") is not True:
                errors.append(f"{path}: real-company promotion package is blocked by default: {ticker}.")
            if ticker in REAL_TICKERS and value.get("fictional_company") is True:
                errors.append(f"{path}: real-company ticker cannot be marked fictional: {ticker}.")
        for forbidden in schema.get("forbidden_fields", []):
            if forbidden in value:
                errors.append(f"{path}: forbidden field present: {forbidden}.")
        for field in schema.get("required", []):
            if field not in value:
                errors.append(f"{path}: missing required field: {field}.")
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, child_schema in properties.items():
                if key in value and isinstance(child_schema, dict):
                    errors.extend(validate_node(value[key], child_schema, f"{path}.{key}"))
        for condition in schema.get("conditional", []):
            if not isinstance(condition, dict):
                errors.append(f"{path}: conditional rule must be an object.")
                continue
            field = condition.get("if_field")
            values = condition.get("if_in", [])
            if field in value and value[field] in values:
                for key, expected in condition.get("then_equal", {}).items():
                    if value.get(key) != expected:
                        errors.append(f"{path}.{key}: expected {expected!r} when {field}={value[field]!r}.")
                for key, forbidden in condition.get("then_not_equal", {}).items():
                    if value.get(key) == forbidden:
                        errors.append(f"{path}.{key}: cannot equal {forbidden!r} when {field}={value[field]!r}.")
    elif isinstance(value, list):
        item_schema = schema.get("items")
        if item_schema is not None:
            if not isinstance(item_schema, dict):
                errors.append(f"{path}: items rule must be an object.")
            else:
                for index, item in enumerate(value):
                    errors.extend(validate_node(item, item_schema, f"{path}[{index}]"))
    return errors


def validate_file(schema_file: Path, input_file: Path) -> tuple[bool, list[str], list[str]]:
    """Validate a JSON file against one local schema."""
    schema = load_json(schema_file)
    value = read_json_any(input_file)
    errors = validate_node(value, schema, "$")
    warnings: list[str] = []
    if schema.get("schema_version") != "v0.3.5":
        warnings.append("Schema version is not v0.3.5.")
    return not errors, errors, warnings


def schema_input_pairs(schema_dir: Path, input_dir: Path) -> list[tuple[Path, Path]]:
    """Resolve package input files for schemas that map to package files."""
    pairs: list[tuple[Path, Path]] = []
    for schema_file in sorted(schema_dir.glob("*_schema.json")):
        schema = load_json(schema_file)
        package_file = SCHEMA_TO_PACKAGE_FILE.get(str(schema.get("schema_name")))
        if not package_file:
            continue
        input_file = input_dir / package_file
        if input_file.exists():
            pairs.append((schema_file, input_file))
    return pairs


def render_report(results: list[dict[str, Any]], report_path: Path) -> str:
    """Render a compact markdown validation report."""
    passed = all(item["validation_passed"] for item in results)
    rows = "\n".join(
        f"| `{item['input_file']}` | `{item['schema_file']}` | {'Pass' if item['validation_passed'] else 'Fail'} | {len(item['errors'])} |"
        for item in results
    )
    details = []
    for item in results:
        if item["errors"]:
            details.append(f"### {item['input_file']}\n" + "\n".join(f"- {error}" for error in item["errors"]))
    detail_text = "\n\n".join(details) if details else "- None"
    return f"""# XBRL Package Schema Validation

## Summary

- validation_passed: `{str(passed).lower()}`
- Generated at: `{utc_now()}`
- Report path: `{relative_or_absolute(report_path)}`

| Input | Schema | Result | Error Count |
|---|---|---:|---:|
{rows}

## Errors

{detail_text}

## Boundary

- Standard-library validation only.
- No network access.
- No field approval, promotion or investment conclusion is generated.
"""


def run_single(schema_file: Path, input_file: Path, output_report: Path) -> bool:
    """Run single-file validation."""
    ensure_distinct_paths(schema_file, input_file, output_report)
    passed, errors, warnings = validate_file(schema_file, input_file)
    result = {
        "schema_file": relative_or_absolute(schema_file),
        "input_file": relative_or_absolute(input_file),
        "validation_passed": passed,
        "errors": errors,
        "warnings": warnings,
    }
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(render_report([result], output_report), encoding="utf-8")
    return passed


def run_package(schema_dir: Path, input_dir: Path, output_report: Path) -> bool:
    """Run package-directory validation."""
    ensure_distinct_paths(schema_dir, input_dir, output_report)
    if not schema_dir.is_dir():
        raise FileNotFoundError(f"Schema directory does not exist: {schema_dir}")
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    pairs = schema_input_pairs(schema_dir, input_dir)
    if not pairs:
        raise ValueError(f"No schema/input pairs found for package: {input_dir}")
    results: list[dict[str, Any]] = []
    for schema_file, input_file in pairs:
        passed, errors, warnings = validate_file(schema_file, input_file)
        results.append(
            {
                "schema_file": relative_or_absolute(schema_file),
                "input_file": relative_or_absolute(input_file),
                "validation_passed": passed,
                "errors": errors,
                "warnings": warnings,
            }
        )
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(render_report(results, output_report), encoding="utf-8")
    return all(item["validation_passed"] for item in results)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Validate local XBRL JSON files using v0.3.5 standard-library schemas."
    )
    parser.add_argument("--schema", type=Path)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--schema-dir", type=Path)
    parser.add_argument("--input-dir", type=Path)
    parser.add_argument("--output-report", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        if args.schema and args.input:
            passed = run_single(args.schema, args.input, args.output_report)
        elif args.schema_dir and args.input_dir:
            passed = run_package(args.schema_dir, args.input_dir, args.output_report)
        else:
            raise ValueError("Use either --schema/--input or --schema-dir/--input-dir.")
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote schema validation report: {args.output_report}")
    print(f"validation_passed={str(passed).lower()}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
