#!/usr/bin/env python3
"""Evidence-chain reconciliation checks for review-gated artifacts."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


SKILL = "goodluck-stock-research"


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


def exists(repo_root: Path, rel_path: str) -> bool:
    return (repo_root / rel_path).exists()


def check_review_packet(repo_root: Path, ticker: str, results: list[CheckResult]) -> None:
    manifest_path = repo_root / SKILL / "examples" / "research_packets" / ticker / "review_only_packet.manifest.json"
    manifest = load_json(manifest_path)
    audit = manifest.get("audit_references", {})
    add(results, f"{ticker} packet links source manifest", exists(repo_root, manifest.get("source_pipeline_manifest", "")), str(manifest.get("source_pipeline_manifest")))
    for field in ("mapping_version", "snapshot_sha256", "review_batch_id"):
        add(results, f"{ticker} packet audit {field}", bool(audit.get(field)), str(audit.get(field)))
    add(results, f"{ticker} candidates listed", bool(manifest.get("candidate_fields")), ", ".join(manifest.get("candidate_fields", [])))
    add(results, f"{ticker} unresolved fields listed", "unresolved_fields" in manifest, ", ".join(manifest.get("unresolved_fields", [])))
    add(results, f"{ticker} not suitable for promotion", manifest.get("suitable_for_promotion") is False, str(manifest.get("suitable_for_promotion")))


def check_quarantine(repo_root: Path, ticker: str, results: list[CheckResult]) -> None:
    manifest_path = repo_root / SKILL / "examples" / "real_company_quarantine" / ticker / "quarantine_manifest.json"
    manifest = load_json(manifest_path)
    for field in ("review_batch", "quality_score", "candidate_package", "approval_policy"):
        add(results, f"{ticker} quarantine links {field}", exists(repo_root, manifest.get(field, "")), str(manifest.get(field)))
    outputs = manifest.get("outputs", {})
    for field in ("quarantined_csv", "csv_audit", "ratio_output", "ratio_manifest", "quarantine_report"):
        add(results, f"{ticker} quarantine output {field}", exists(repo_root, outputs.get(field, "")), str(outputs.get(field)))
    for flag in ("quarantined", "not_production_data", "not_investment_data", "not_for_trading", "no_recommendation"):
        add(results, f"{ticker} quarantine flag {flag}", manifest.get(flag) is True, str(manifest.get(flag)))


def audit(repo_root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    for ticker in ("MRVL", "NVDA", "AVGO"):
        check_review_packet(repo_root, ticker, results)
    check_quarantine(repo_root, "MRVL", results)
    return results


def render(results: list[CheckResult]) -> str:
    failed = [item for item in results if not item.passed]
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    return f"""# Evidence Reconciliation Report

- Passed: {'Yes' if not failed else 'No'}
- Draft candidates are not facts.
- Quarantined data is not production data.

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run evidence reconciliation checks.")
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
    print("PASS: evidence reconciliation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
