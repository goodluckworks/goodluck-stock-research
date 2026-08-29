#!/usr/bin/env python3
"""QA checks for controlled real-company quarantine output."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


REQUIRED_FLAGS = (
    "quarantined",
    "not_production_data",
    "not_investment_data",
    "not_company_fact_until_verified",
    "manual_review_required",
    "not_for_trading",
    "not_for_public_release",
    "no_recommendation",
)
FORBIDDEN_TERMS = ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:")


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


def qa_quarantine(repo_root: Path, ticker: str = "MRVL") -> list[CheckResult]:
    root = repo_root / "goodluck-stock-research" / "examples" / "real_company_quarantine" / ticker
    manifest = load_json(root / "quarantine_manifest.json")
    results: list[CheckResult] = []
    for flag in REQUIRED_FLAGS:
        add(results, f"{ticker} flag {flag}", manifest.get(flag) is True, str(manifest.get(flag)))
    add(results, f"{ticker} no DCF", manifest.get("no_dcf") is True, str(manifest.get("no_dcf")))
    add(results, f"{ticker} no peer comps", manifest.get("no_peer_comps") is True, str(manifest.get("no_peer_comps")))
    add(results, f"{ticker} no implied expectations", manifest.get("no_implied_expectations") is True, str(manifest.get("no_implied_expectations")))
    outputs = manifest.get("outputs") or {}
    for field in ("quarantined_csv", "csv_audit", "ratio_output", "ratio_manifest", "quarantine_report"):
        add(results, f"{ticker} output {field}", (repo_root / outputs.get(field, "")).exists(), str(outputs.get(field)))
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        add(results, f"{path.name} no conclusion fields", not any(term in text for term in FORBIDDEN_TERMS), "forbidden scan")
    for blocked in ("NVDA", "AVGO"):
        add(results, f"{blocked} no tracked quarantine output", not (repo_root / "goodluck-stock-research" / "examples" / "real_company_quarantine" / blocked).exists(), "blocked by default")
    return results


def render(results: list[CheckResult]) -> str:
    failed = [item for item in results if not item.passed]
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    return f"""# Quarantine QA Report

- Passed: {'Yes' if not failed else 'No'}
- Production readiness: No

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run quarantine QA checks.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--ticker", default="MRVL")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    results = qa_quarantine(args.repo_root, args.ticker.upper())
    report = render(results)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    failed = [item for item in results if not item.passed]
    if failed:
        print(report)
        return 1
    print("PASS: quarantine QA")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
