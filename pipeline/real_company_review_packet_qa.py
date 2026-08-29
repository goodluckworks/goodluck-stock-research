#!/usr/bin/env python3
"""QA for real-company review-only research packets."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


REAL_TICKERS = ("MRVL", "NVDA", "AVGO")
FORBIDDEN_TERMS = ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:")


@dataclass
class PacketCheck:
    """Packet QA result."""

    ticker: str
    check: str
    passed: bool
    notes: str


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def add(results: list[PacketCheck], ticker: str, check: str, passed: bool, notes: str) -> None:
    """Append check."""
    results.append(PacketCheck(ticker, check, passed, notes))


def qa_one(repo_root: Path, ticker: str) -> list[PacketCheck]:
    """QA one real-company review-only packet."""
    results: list[PacketCheck] = []
    run_dir = repo_root / "goodluck-stock-research" / "examples" / "pipeline_runs" / ticker / "review_only"
    packet_dir = repo_root / "goodluck-stock-research" / "examples" / "research_packets" / ticker
    packet_md = packet_dir / "review_only_packet.md"
    packet_manifest_path = packet_dir / "review_only_packet.manifest.json"
    candidate_path = run_dir / "candidate" / "extraction_candidates.json"
    unresolved_path = run_dir / "candidate" / "unresolved_fields.json"
    quality_path = run_dir / "quality" / "review_quality_score.json"
    workbench_path = run_dir / "workbench" / "review_workbench.md"
    review_path = run_dir / "review" / "normalized_review_batch.json"
    run_manifest_path = run_dir / "pipeline_run_manifest.json"
    required_files = [packet_md, packet_manifest_path, candidate_path, unresolved_path, quality_path, workbench_path, review_path, run_manifest_path]
    for path in required_files:
        add(results, ticker, f"{path.name} exists", path.is_file(), str(path))
    if not all(path.is_file() for path in required_files):
        return results
    text = packet_md.read_text(encoding="utf-8")
    lowered = text.lower()
    packet_manifest = load_json(packet_manifest_path)
    candidates = load_json(candidate_path)
    unresolved = load_json(unresolved_path)
    quality = load_json(quality_path)
    run_manifest = load_json(run_manifest_path)
    candidate_fields = [item.get("normalized_field") for item in candidates.get("candidates", [])]
    unresolved_fields = [item.get("normalized_field") for item in unresolved.get("unresolved_fields", [])]
    add(results, ticker, "review-only packet boundary", "Review-only packet" in text and "Draft / unapproved" in text, "boundary text")
    add(results, ticker, "candidate summary completeness", bool(candidate_fields) and "Candidate fields:" in text and "## Candidate Fields" in text, f"{len(candidate_fields)} candidates")
    add(results, ticker, "unresolved explanation quality", "## Unresolved Field Explanations" in text and all(field in text for field in unresolved_fields), f"{len(unresolved_fields)} unresolved fields")
    add(results, ticker, "quality score references", "Quality package:" in text and "Quality score:" in text and packet_manifest.get("quality_reference"), str(packet_manifest.get("quality_reference")))
    add(results, ticker, "workbench references", "Workbench reference:" in text and packet_manifest.get("workbench_reference"), str(packet_manifest.get("workbench_reference")))
    add(results, ticker, "no approved data", "No approved normalized input." in text and packet_manifest.get("suitable_for_promotion") is False, "promotion suitability false")
    add(results, ticker, "no normalized CSV", not (run_dir / "normalized_csv_sandbox").exists() and "No normalized CSV." in text, "blocked")
    add(results, ticker, "no dry-run", not (run_dir / "v02_ratio_dry_run").exists() and "No v0.2.x dry-run." in text, "blocked")
    add(results, ticker, "no promotion", not (run_dir / "promotion").exists() and "No promotion." in text, "blocked")
    add(results, ticker, "no investment conclusion", not any(term in lowered for term in FORBIDDEN_TERMS) and run_manifest.get("no_investment_conclusion") is True, "forbidden scan")
    add(results, ticker, "review batch traceable", run_manifest["audit_references"].get("review_batch_id") in text, str(run_manifest["audit_references"].get("review_batch_id")))
    add(results, ticker, "quality records present", len(quality.get("records", [])) >= len(candidate_fields), f"{len(quality.get('records', []))} quality records")
    add(results, ticker, "promotion suitability is No", "Suitable for promotion: `No`" in text, "explicit No")
    return results


def run_qa(repo_root: Path) -> list[PacketCheck]:
    """Run real-company packet QA."""
    results: list[PacketCheck] = []
    for ticker in REAL_TICKERS:
        results.extend(qa_one(repo_root, ticker))
    return results


def render(results: list[PacketCheck]) -> str:
    """Render Markdown report."""
    rows = "\n".join(f"| {item.ticker} | {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    failed = [item for item in results if not item.passed]
    return f"""# Real-Company Review Packet QA

## Summary

- Passed: {'Yes' if not failed else 'No'}
- Failed checks: {len(failed)}
- Promotion suitability: No for MRVL, NVDA and AVGO.

## Checks

| Ticker | Check | Result | Notes |
|---|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run real-company review packet QA.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        results = run_qa(args.repo_root.resolve())
        report = render(results)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
        print(report)
        return 0 if all(item.passed for item in results) else 1
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
