#!/usr/bin/env python3
"""Build a pipeline audit dashboard from tracked pipeline runs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence


PIPELINE_DIR = Path(__file__).resolve().parent
SKILL_DIR = PIPELINE_DIR.parent
XBRL_DIR = SKILL_DIR / "xbrl"
sys.path.insert(0, str(XBRL_DIR))

from xbrl_common import prepare_output_dir, relative_or_absolute, utc_now, write_json  # noqa: E402


REAL_TICKERS = ("MRVL", "NVDA", "AVGO")
FORBIDDEN_TERMS = ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:")


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def run_dirs(root: Path) -> list[Path]:
    """Find pipeline run dirs."""
    return sorted(path.parent for path in root.rglob("pipeline_run_manifest.json"))


def packet_status(packet_root: Path, ticker: str, mode: str) -> str:
    """Return packet status for a run."""
    if ticker == "EXMP" and mode == "fictional_sandbox_full":
        return "present" if (packet_root / "EXMP" / "full_sandbox_packet.md").is_file() else "missing"
    if ticker == "EXMP" and mode == "fictional_sandbox_partial":
        return "present" if (packet_root / "EXMP" / "partial_sandbox_packet.md").is_file() else "missing"
    return "present" if (packet_root / ticker / "review_only_packet.md").is_file() else "missing"


def summarize_run(run_dir: Path, packet_root: Path) -> dict[str, Any]:
    """Summarize one pipeline run."""
    manifest = load_json(run_dir / "pipeline_run_manifest.json")
    ticker = manifest["ticker"]
    normalized = run_dir / "normalized_csv_sandbox"
    dry_run = run_dir / "v02_ratio_dry_run"
    promotion = run_dir / "promotion"
    quality = load_json(run_dir / "quality" / "review_quality_score.json") if (run_dir / "quality" / "review_quality_score.json").is_file() else {}
    csv_manifest = load_json(normalized / "normalized_csv_manifest.json") if (normalized / "normalized_csv_manifest.json").is_file() else {}
    return {
        "run_dir": relative_or_absolute(run_dir),
        "pipeline_run_id": manifest["pipeline_run_id"],
        "mode": manifest["mode"],
        "ticker": ticker,
        "company": manifest["company"],
        "fixture_data_status": manifest["fixture_data_status"],
        "promotion_status": "present" if promotion.is_dir() else "blocked_or_not_applicable",
        "normalized_csv_status": "present" if normalized.is_dir() else "blocked_or_not_applicable",
        "dry_run_status": "present" if dry_run.is_dir() else "blocked_or_not_applicable",
        "packet_status": packet_status(packet_root, ticker, manifest["mode"]),
        "blocked_steps": manifest.get("blocked_steps", []),
        "audit_completeness": "complete" if manifest.get("audit_references") else "missing",
        "safety_boundary_result": "pass" if manifest.get("no_investment_conclusion") is True else "fail",
        "unresolved_field_count": len(csv_manifest.get("unresolved_fields", [])),
        "missing_field_count": len(csv_manifest.get("omitted_fields", [])),
        "approval_readiness": quality.get("overall_status", quality.get("approval_readiness", "review_only_or_not_applicable")),
    }


def blocked_matrix(summary: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Build blocked real-company matrix."""
    rows: list[dict[str, str]] = []
    by_ticker = {row["ticker"]: row for row in summary if row["ticker"] in REAL_TICKERS and row["mode"] == "real_company_review_only"}
    for ticker in REAL_TICKERS:
        row = by_ticker.get(ticker)
        for step, status_field in (
            ("promotion", "promotion_status"),
            ("normalized_csv", "normalized_csv_status"),
            ("v02_dry_run", "dry_run_status"),
        ):
            status = "pass" if row and row.get(status_field) == "blocked_or_not_applicable" else "fail"
            rows.append({"ticker": ticker, "blocked_step": step, "result": status})
    return rows


def render_dashboard(summary: list[dict[str, Any]]) -> str:
    """Render dashboard Markdown."""
    rows = "\n".join(
        "| {ticker} | {mode} | {fixture} | {promotion} | {csv} | {dry} | {packet} | {audit} | {safety} | {unresolved} | {missing} | {readiness} |".format(
            ticker=row["ticker"],
            mode=row["mode"],
            fixture=row["fixture_data_status"],
            promotion=row["promotion_status"],
            csv=row["normalized_csv_status"],
            dry=row["dry_run_status"],
            packet=row["packet_status"],
            audit=row["audit_completeness"],
            safety=row["safety_boundary_result"],
            unresolved=row["unresolved_field_count"],
            missing=row["missing_field_count"],
            readiness=row["approval_readiness"],
        )
        for row in summary
    )
    return f"""# Pipeline Audit Dashboard

Generated at: `{utc_now()}`

| Ticker | Mode | Fixture status | Promotion | Normalized CSV | Dry-run | Packet | Audit | Safety | Unresolved fields | Missing fields | Approval readiness |
|---|---|---|---|---|---|---|---|---|---:|---:|---|
{rows}

## Boundary

- EXMP may have fictional sandbox promotion, normalized CSV and ratio dry-run.
- MRVL / NVDA / AVGO must remain review-only.
- No real-company promotion, normalized CSV or v0.2.x dry-run should be present.
- No target price, buy/sell/hold, position size, research status or trading action.
"""


def render_matrix(rows: list[dict[str, str]]) -> str:
    """Render blocked matrix."""
    body = "\n".join(f"| {row['ticker']} | {row['blocked_step']} | {row['result']} |" for row in rows)
    return f"""# Blocked Real-Company Matrix

| Ticker | Blocked step | Result |
|---|---|---:|
{body}
"""


def scan_forbidden(path: Path) -> None:
    """Scan generated dashboard files."""
    for markdown in path.rglob("*.md"):
        lowered = markdown.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_TERMS:
            if term in lowered:
                raise ValueError(f"Forbidden conclusion text in {markdown}: {term}")


def build_dashboard(pipeline_root: Path, packet_root: Path, output_dir: Path, overwrite: bool = False) -> dict[str, Path]:
    """Build dashboard files."""
    pipeline_root = pipeline_root.expanduser().resolve()
    packet_root = packet_root.expanduser().resolve()
    output_dir = output_dir.expanduser().resolve()
    prepare_output_dir(output_dir, overwrite)
    summary = [summarize_run(path, packet_root) for path in run_dirs(pipeline_root)]
    matrix = blocked_matrix(summary)
    if any(row["result"] != "pass" for row in matrix):
        raise ValueError("Blocked real-company matrix failed.")
    payload = {
        "dashboard_schema_version": "v0.3.12",
        "created_at": utc_now(),
        "pipeline_root": relative_or_absolute(pipeline_root),
        "packet_root": relative_or_absolute(packet_root),
        "runs": summary,
        "blocked_real_company_matrix": matrix,
        "no_investment_conclusion": True,
    }
    paths = {
        "dashboard": output_dir / "pipeline_audit_dashboard.md",
        "summary": output_dir / "pipeline_audit_summary.json",
        "matrix": output_dir / "blocked_real_company_matrix.md",
    }
    paths["dashboard"].write_text(render_dashboard(summary), encoding="utf-8")
    write_json(paths["summary"], payload)
    paths["matrix"].write_text(render_matrix(matrix), encoding="utf-8")
    scan_forbidden(output_dir)
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Build review-gated pipeline audit dashboard.")
    parser.add_argument("--pipeline-root", required=True, type=Path)
    parser.add_argument("--packet-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = build_dashboard(args.pipeline_root, args.packet_root, args.output_dir, args.overwrite)
    except (FileNotFoundError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("Wrote pipeline audit dashboard:")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
