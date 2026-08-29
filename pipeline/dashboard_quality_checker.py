#!/usr/bin/env python3
"""Quality checks for pipeline audit dashboard artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


PIPELINE_DIR = Path(__file__).resolve().parent
SKILL_DIR = PIPELINE_DIR.parent
REAL_TICKERS = ("MRVL", "NVDA", "AVGO")
EXPECTED_MODES = ("fictional_sandbox_full", "fictional_sandbox_partial", "real_company_review_only")
REAL_FORBIDDEN_STEPS = ("promotion", "normalized_csv", "v02_dry_run")
STEP_ALIASES = {"v02_dry_run": ("v02_dry_run", "v02_ratio_dry_run")}
FORBIDDEN_TERMS = ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:")


@dataclass
class DashboardCheck:
    """Dashboard quality check result."""

    check: str
    passed: bool
    notes: str


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def rel(path: Path, root: Path) -> str:
    """Return root-relative path."""
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def add(results: list[DashboardCheck], check: str, passed: bool, notes: str) -> None:
    """Append a result."""
    results.append(DashboardCheck(check, passed, notes))


def load_summary(dashboard_dir: Path) -> dict[str, Any]:
    """Load dashboard summary."""
    return load_json(dashboard_dir / "pipeline_audit_summary.json")


def run_manifest_path(repo_root: Path, run_dir: str) -> Path:
    """Return run manifest path."""
    return repo_root / run_dir / "pipeline_run_manifest.json"


def packet_path(repo_root: Path, ticker: str, mode: str) -> Path:
    """Return expected packet path."""
    if ticker == "EXMP" and mode == "fictional_sandbox_full":
        return repo_root / "goodluck-stock-research" / "examples" / "research_packets" / "EXMP" / "full_sandbox_packet.md"
    if ticker == "EXMP" and mode == "fictional_sandbox_partial":
        return repo_root / "goodluck-stock-research" / "examples" / "research_packets" / "EXMP" / "partial_sandbox_packet.md"
    return repo_root / "goodluck-stock-research" / "examples" / "research_packets" / ticker / "review_only_packet.md"


def check_dashboard(repo_root: Path, dashboard_dir: Path) -> list[DashboardCheck]:
    """Run dashboard quality checks."""
    results: list[DashboardCheck] = []
    summary = load_summary(dashboard_dir)
    runs = summary.get("runs", [])
    modes = {str(run.get("mode")) for run in runs}
    add(results, "all pipeline modes represented", set(EXPECTED_MODES).issubset(modes), f"modes: {sorted(modes)}")
    by_ticker_mode = {(str(run.get("ticker")), str(run.get("mode"))): run for run in runs}
    for ticker in REAL_TICKERS:
        run = by_ticker_mode.get((ticker, "real_company_review_only"))
        add(results, f"{ticker} review-only run represented", run is not None, "present" if run else "missing")
        if not run:
            continue
        manifest = load_json(run_manifest_path(repo_root, str(run["run_dir"])))
        blocked = {item.get("step"): item.get("reason") for item in manifest.get("blocked_steps", [])}
        for step in REAL_FORBIDDEN_STEPS:
            aliases = STEP_ALIASES.get(step, (step,))
            reason = next((blocked.get(alias) for alias in aliases if blocked.get(alias)), None)
            add(results, f"{ticker} blocked {step} has reason", bool(reason), str(reason))
        add(results, f"{ticker} review-only packet has no dry-run", run.get("dry_run_status") == "blocked_or_not_applicable", str(run.get("dry_run_status")))
        add(results, f"{ticker} review-only has no promotion", run.get("promotion_status") == "blocked_or_not_applicable", str(run.get("promotion_status")))
        add(results, f"{ticker} review-only has no normalized CSV", run.get("normalized_csv_status") == "blocked_or_not_applicable", str(run.get("normalized_csv_status")))
    for run in runs:
        label = f"{run.get('ticker')} {run.get('mode')}"
        add(results, f"{label} audit completeness", run.get("audit_completeness") == "complete", str(run.get("audit_completeness")))
        add(results, f"{label} packet status", run.get("packet_status") == "present", str(run.get("packet_status")))
        packet = packet_path(repo_root, str(run.get("ticker")), str(run.get("mode")))
        if packet.is_file():
            packet_text = packet.read_text(encoding="utf-8").lower()
            add(results, f"{label} packet no conclusion fields", not any(term in packet_text for term in FORBIDDEN_TERMS), rel(packet, repo_root))
    exmp_full = by_ticker_mode.get(("EXMP", "fictional_sandbox_full"))
    exmp_partial = by_ticker_mode.get(("EXMP", "fictional_sandbox_partial"))
    add(results, "EXMP full promotion preserved", bool(exmp_full and exmp_full.get("promotion_status") == "present"), str(exmp_full.get("promotion_status") if exmp_full else "missing"))
    add(results, "EXMP partial promotion preserved", bool(exmp_partial and exmp_partial.get("promotion_status") == "present"), str(exmp_partial.get("promotion_status") if exmp_partial else "missing"))
    if exmp_partial:
        partial_manifest = load_json(repo_root / str(exmp_partial["run_dir"]) / "normalized_csv_sandbox" / "normalized_csv_manifest.json")
        impact = partial_manifest.get("downstream_impact", {})
        unavailable = impact.get("unavailable_ratios", [])
        add(results, "partial-field run displays downstream impact", bool(unavailable), f"unavailable ratios: {len(unavailable)}")
        add(results, "partial unresolved count matches dashboard", exmp_partial.get("unresolved_field_count") == len(partial_manifest.get("unresolved_fields", [])), "dashboard vs manifest")
        add(results, "partial omitted count matches dashboard", exmp_partial.get("missing_field_count") == len(partial_manifest.get("omitted_fields", [])), "dashboard vs manifest")
    dashboard_text = "\n".join(path.read_text(encoding="utf-8").lower() for path in dashboard_dir.glob("*.md"))
    add(results, "dashboard has no conclusion fields", not any(term in dashboard_text for term in FORBIDDEN_TERMS), "markdown scan")
    matrix = summary.get("blocked_real_company_matrix", [])
    expected_matrix = {(ticker, step) for ticker in REAL_TICKERS for step in REAL_FORBIDDEN_STEPS}
    actual_matrix = {(row.get("ticker"), row.get("blocked_step")) for row in matrix if row.get("result") == "pass"}
    add(results, "blocked matrix covers every real-company forbidden path", expected_matrix.issubset(actual_matrix), f"{len(actual_matrix)}/{len(expected_matrix)} pass rows")
    return results


def render(results: list[DashboardCheck]) -> str:
    """Render Markdown."""
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    failed = [item for item in results if not item.passed]
    return f"""# Dashboard Quality Report

## Summary

- Passed: {'Yes' if not failed else 'No'}
- Failed checks: {len(failed)}

## Checks

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Check pipeline dashboard quality.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--dashboard-dir", type=Path, default=Path("goodluck-stock-research/examples/pipeline_audit_dashboard"))
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        repo_root = args.repo_root.resolve()
        results = check_dashboard(repo_root, (repo_root / args.dashboard_dir).resolve())
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
