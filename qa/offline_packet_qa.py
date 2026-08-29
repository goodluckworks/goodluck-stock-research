#!/usr/bin/env python3
"""QA checks for offline pipeline packets and dashboards."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


SKILL_DIRNAME = "goodluck-stock-research"
REAL_TICKERS = ("MRVL", "NVDA", "AVGO")
FORBIDDEN_CONCLUSION_TERMS = (
    "target price:",
    "buy:",
    "sell:",
    "hold:",
    "position size:",
    "research status:",
)


@dataclass
class CheckResult:
    """Single QA check result."""

    check: str
    passed: bool
    notes: str


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def rel(path: Path, root: Path) -> str:
    """Return repo-relative display path."""
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def add(results: list[CheckResult], check: str, passed: bool, notes: str) -> None:
    """Append a check result."""
    results.append(CheckResult(check, passed, notes))


def require_manifest_fields(manifest: dict[str, Any]) -> list[str]:
    """Return missing required pipeline manifest fields."""
    required = (
        "pipeline_schema_version",
        "pipeline_run_id",
        "mode",
        "ticker",
        "company",
        "fixture_data_status",
        "run_steps",
        "input_paths",
        "output_paths",
        "blocked_steps",
        "warnings",
        "audit_references",
        "no_investment_conclusion",
        "created_at",
        "output_dir",
    )
    return [field for field in required if field not in manifest]


def qa_pipeline_runs(repo_root: Path, results: list[CheckResult]) -> None:
    """Check pipeline run manifests and real-company blocked outputs."""
    run_root = repo_root / SKILL_DIRNAME / "examples" / "pipeline_runs"
    manifests = sorted(run_root.rglob("pipeline_run_manifest.json"))
    add(results, "pipeline run manifests exist", bool(manifests), f"{len(manifests)} manifest(s) found")
    seen_modes: set[str] = set()
    for path in manifests:
        manifest = load_json(path)
        display = rel(path, repo_root)
        missing = require_manifest_fields(manifest)
        add(results, f"{display} complete", not missing, "missing: " + ", ".join(missing) if missing else "complete")
        add(results, f"{display} no investment conclusion", manifest.get("no_investment_conclusion") is True, "manifest flag")
        seen_modes.add(str(manifest.get("mode", "")))
        ticker = str(manifest.get("ticker", "")).upper()
        run_dir = path.parent
        if ticker in REAL_TICKERS:
            for forbidden_dir in ("promotion", "normalized_csv_sandbox", "v02_ratio_dry_run"):
                add(
                    results,
                    f"{ticker} no {forbidden_dir}",
                    not (run_dir / forbidden_dir).exists(),
                    rel(run_dir / forbidden_dir, repo_root),
                )
            blocked = {item.get("step"): item.get("reason") for item in manifest.get("blocked_steps", [])}
            for step in ("promotion", "normalized_csv", "v02_ratio_dry_run"):
                add(results, f"{ticker} blocked step {step}", step in blocked and bool(blocked[step]), str(blocked.get(step)))
        if ticker == "EXMP":
            has_sandbox_note = any("Fictional sandbox" in str(value) for value in manifest.get("warnings", []))
            add(results, f"{display} EXMP sandbox warning", has_sandbox_note, "fictional sandbox warning present")
    for mode in ("fictional_sandbox_full", "fictional_sandbox_partial", "real_company_review_only"):
        add(results, f"mode represented: {mode}", mode in seen_modes, f"seen modes: {sorted(seen_modes)}")


def qa_packets(repo_root: Path, results: list[CheckResult]) -> None:
    """Check research packet Markdown and manifests."""
    packet_root = repo_root / SKILL_DIRNAME / "examples" / "research_packets"
    packets = sorted(packet_root.rglob("*.md"))
    manifests = sorted(packet_root.rglob("*.manifest.json"))
    add(results, "research packet Markdown exists", bool(packets), f"{len(packets)} packet(s)")
    add(results, "research packet manifests exist", bool(manifests), f"{len(manifests)} manifest(s)")
    for packet in packets:
        text = packet.read_text(encoding="utf-8")
        lowered = text.lower()
        display = rel(packet, repo_root)
        is_real = any(f"/{ticker}/" in "/" + display for ticker in REAL_TICKERS)
        is_exmp = "/EXMP/" in "/" + display
        add(results, f"{display} no forbidden conclusion fields", not any(term in lowered for term in FORBIDDEN_CONCLUSION_TERMS), "forbidden scan")
        if is_exmp:
            add(results, f"{display} sandbox disclaimer", "Fictional only" in text and "Not investment advice" in text, "fictional disclaimer")
        if is_real:
            add(results, f"{display} draft-only disclaimer", "Review-only packet" in text and "Draft / unapproved" in text, "draft disclaimer")
            add(results, f"{display} no promotion claim", "No promotion." in text and "No normalized CSV." in text and "No v0.2.x dry-run." in text, "explicit non-outputs")
    for manifest_path in manifests:
        manifest = load_json(manifest_path)
        missing = [field for field in ("packet_schema_version", "packet_type", "pipeline_run_id", "ticker", "mode", "source_pipeline_manifest", "no_investment_conclusion") if field not in manifest]
        add(results, f"{rel(manifest_path, repo_root)} complete", not missing, "missing: " + ", ".join(missing) if missing else "complete")


def qa_dashboard(repo_root: Path, results: list[CheckResult]) -> None:
    """Check dashboard references and blocked matrix."""
    dash_root = repo_root / SKILL_DIRNAME / "examples" / "pipeline_audit_dashboard"
    summary_path = dash_root / "pipeline_audit_summary.json"
    dashboard_path = dash_root / "pipeline_audit_dashboard.md"
    matrix_path = dash_root / "blocked_real_company_matrix.md"
    add(results, "dashboard summary exists", summary_path.is_file(), rel(summary_path, repo_root))
    add(results, "dashboard markdown exists", dashboard_path.is_file(), rel(dashboard_path, repo_root))
    add(results, "blocked matrix exists", matrix_path.is_file(), rel(matrix_path, repo_root))
    if not summary_path.is_file():
        return
    summary = load_json(summary_path)
    runs = summary.get("runs", [])
    tickers = {str(run.get("ticker")) for run in runs}
    add(results, "dashboard references all tracked runs", {"EXMP", "MRVL", "NVDA", "AVGO"}.issubset(tickers), f"tickers: {sorted(tickers)}")
    matrix = summary.get("blocked_real_company_matrix", [])
    expected = {(ticker, step) for ticker in REAL_TICKERS for step in ("promotion", "normalized_csv", "v02_dry_run")}
    actual = {(str(row.get("ticker")), str(row.get("blocked_step"))) for row in matrix if row.get("result") == "pass"}
    add(results, "blocked matrix covers real-company forbidden paths", expected.issubset(actual), f"{len(actual)}/{len(expected)} pass rows")
    for run in runs:
        label = f"dashboard run {run.get('ticker')} {run.get('mode')}"
        add(results, f"{label} packet present", run.get("packet_status") == "present", str(run.get("packet_status")))
        add(results, f"{label} audit complete", run.get("audit_completeness") == "complete", str(run.get("audit_completeness")))
        add(results, f"{label} safety pass", run.get("safety_boundary_result") == "pass", str(run.get("safety_boundary_result")))


def qa_paths(repo_root: Path, results: list[CheckResult]) -> None:
    """Check paths in JSON/Markdown outputs are repo-relative or intentionally temporary."""
    output_roots = [
        repo_root / SKILL_DIRNAME / "examples" / "pipeline_runs",
        repo_root / SKILL_DIRNAME / "examples" / "research_packets",
        repo_root / SKILL_DIRNAME / "examples" / "pipeline_audit_dashboard",
    ]
    offenders: list[str] = []
    for root in output_roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".csv"}:
                text = path.read_text(encoding="utf-8", errors="ignore")
                if "/Users/" in text:
                    offenders.append(rel(path, repo_root))
                if "/private/tmp" in text and "validation" not in rel(path, repo_root):
                    offenders.append(rel(path, repo_root))
    add(results, "tracked outputs do not leak local machine paths", not offenders, ", ".join(offenders[:10]) if offenders else "clean")


def run_qa(repo_root: Path) -> list[CheckResult]:
    """Run all offline packet QA checks."""
    results: list[CheckResult] = []
    qa_pipeline_runs(repo_root, results)
    qa_packets(repo_root, results)
    qa_dashboard(repo_root, results)
    qa_paths(repo_root, results)
    return results


def render(results: list[CheckResult]) -> str:
    """Render Markdown report."""
    rows = "\n".join(
        f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |"
        for item in results
    )
    failed = [item for item in results if not item.passed]
    return f"""# Offline Packet QA Report

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
    parser = argparse.ArgumentParser(description="Run offline packet QA checks.")
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
