#!/usr/bin/env python3
"""Fixture-first parser-readiness audit."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


SKILL = "goodluck-stock-research"
PRODUCTION_READY = False


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


def add(results: list[CheckResult], check: str, passed: bool, notes: str) -> None:
    results.append(CheckResult(check, passed, notes))


def audit(repo_root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    skill = repo_root / SKILL
    mapping = load_json(skill / "xbrl" / "mappings" / "us_gaap_core_v0_3_7.json")
    records = mapping.get("records", [])
    add(results, "fixture-first mapping status", mapping.get("review_status") == "prototype_fixture_only", str(mapping.get("review_status")))
    add(results, "production parser ready", PRODUCTION_READY is False, "production_parser_ready: No")
    readme_text = "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in [repo_root / "README.md", skill / "README.md", skill / "xbrl" / "README.md"] if path.exists()).lower()
    add(results, "no production parser claim", "production parser ready: yes" not in readme_text and "production parser is ready" not in readme_text, "docs scanned")
    add(results, "no live extraction claim", "live extraction enabled" not in readme_text, "docs scanned")
    required_rel = ("concept_label", "taxonomy_namespace", "relationship_confidence", "relationship_review_status", "taxonomy_version")
    missing_rel = [str(item.get("normalized_field")) for item in records if not all((item.get("relationship_metadata") or {}).get(field) for field in required_rel)]
    add(results, "taxonomy relationship metadata complete", not missing_rel, ", ".join(missing_rel) if missing_rel else "complete")
    required_mapping = ("mapping_version", "taxonomy_family", "supported_forms", "records")
    add(results, "mapping version lineage present", all(mapping.get(field) for field in required_mapping), str(mapping.get("mapping_version")))
    candidate_files = sorted((skill / "examples" / "pipeline_runs").glob("*/review_only/candidate/extraction_candidates.json"))
    add(results, "real-company candidate packages exist", len(candidate_files) >= 3, f"{len(candidate_files)} package(s)")
    for path in candidate_files:
        package = load_json(path)
        candidates = package.get("candidates", [])
        missing = [
            str(c.get("candidate_id"))
            for c in candidates
            if not c.get("source_locator")
            or not c.get("concept_qname")
            or not c.get("period")
            or not c.get("unit")
            or "dimensions" not in c
        ]
        add(results, f"{path.parent.parent.parent.name} candidate provenance", not missing, ", ".join(missing) if missing else "complete")
    return results


def render(results: list[CheckResult]) -> str:
    failed = [item for item in results if not item.passed]
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    return f"""# Parser Readiness Audit

## Summary

- Passed: {'Yes' if not failed else 'No'}
- production_parser_ready: No
- reason: fixture-first prototype; production parser requires separate implementation and validation

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run parser-readiness audit.")
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
    print("PASS: parser-readiness audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
