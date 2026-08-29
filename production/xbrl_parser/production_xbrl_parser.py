#!/usr/bin/env python3
"""Production XBRL parser MVP for scoped local filing packages."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

PARSER_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PARSER_DIR))

from fact_candidate_selector import SUPPORTED_FIELDS, select_field  # noqa: E402


SUPPORTED_FORMS = {"10-K", "10-Q"}
UNSUPPORTED_ISSUER_TYPES = {"bank", "insurer", "fund", "foreign_issuer"}


def load_package(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("filing package root must be object")
    return value


def parse_package(package: dict[str, Any]) -> dict[str, Any]:
    if package.get("form") not in SUPPORTED_FORMS:
        raise ValueError("unsupported form")
    if package.get("issuer_type") in UNSUPPORTED_ISSUER_TYPES:
        raise ValueError("unsupported issuer type")
    facts = package.get("facts", [])
    if not isinstance(facts, list):
        raise ValueError("facts must be list")
    period = package.get("fiscal_period")
    parsed = [select_field(facts, field, period) for field in sorted(SUPPORTED_FIELDS)]
    return {
        "parser_schema_version": "v1.3.0",
        "ticker": package.get("ticker"),
        "form": package.get("form"),
        "fiscal_period": period,
        "fields": parsed,
        "financial_extraction_scope": sorted(SUPPORTED_FIELDS),
        "no_investment_conclusion": True,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse local filing package.")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = parse_package(load_package(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS: production XBRL parser MVP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
