#!/usr/bin/env python3
"""Taxonomy drift checks for fixture mappings."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


@dataclass
class CheckResult:
    check: str
    passed: bool
    notes: str


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def audit(repo_root: Path) -> list[CheckResult]:
    mapping_path = repo_root / "goodluck-stock-research" / "xbrl" / "mappings" / "us_gaap_core_v0_3_7.json"
    mapping = load_json(mapping_path)
    results: list[CheckResult] = []
    versions = set()
    weak: list[str] = []
    for record in mapping.get("records", []):
        rel = record.get("relationship_metadata") or {}
        versions.add(str(rel.get("taxonomy_version", "")))
        if rel.get("relationship_review_status") != "reviewed":
            weak.append(str(record.get("normalized_field")))
        if not record.get("mapping_id") or not record.get("normalized_field"):
            weak.append("missing-id")
    results.append(CheckResult("taxonomy version declared", versions == {"fixture-v0.3.7"}, ", ".join(sorted(versions))))
    results.append(CheckResult("relationship review status", not weak, ", ".join(weak) if weak else "reviewed"))
    results.append(CheckResult("production taxonomy coverage not claimed", mapping.get("review_status") == "prototype_fixture_only", str(mapping.get("review_status"))))
    return results


def render(results: list[CheckResult]) -> str:
    failed = [item for item in results if not item.passed]
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    return f"""# Taxonomy Drift Check

- Passed: {'Yes' if not failed else 'No'}
- Production taxonomy coverage: No

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run taxonomy drift checks.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    results = audit(args.repo_root)
    report = render(results)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    failed = [item for item in results if not item.passed]
    if failed:
        print(report)
        return 1
    print("PASS: taxonomy drift checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
