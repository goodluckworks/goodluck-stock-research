#!/usr/bin/env python3
"""Offline review-gated pipeline orchestrator."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Sequence


PIPELINE_DIR = Path(__file__).resolve().parent
SKILL_DIR = PIPELINE_DIR.parent
XBRL_DIR = SKILL_DIR / "xbrl"
sys.path.insert(0, str(XBRL_DIR))
sys.path.insert(0, str(PIPELINE_DIR))

from end_to_end_pipeline_auditor import audit_pipeline  # noqa: E402
from generate_normalized_csv_sandbox import run_generator  # noqa: E402
from run_v02_sandbox_dry_run import run_dry_run  # noqa: E402
from xbrl_common import prepare_output_dir, relative_or_absolute, utc_now, write_json  # noqa: E402
from pipeline_manifest import write_manifest  # noqa: E402
from pipeline_policy import FICTIONAL_TICKER, REAL_TICKERS, blocked_steps_for, validate_mode_ticker  # noqa: E402
from pipeline_run_report import render_report  # noqa: E402


EXAMPLES = SKILL_DIR / "examples"
FORBIDDEN_TERMS = ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:")


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def copy_dir(source: Path, destination: Path) -> None:
    """Copy an example directory into the run output."""
    if not source.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {source}")
    shutil.copytree(source, destination)


def source_dirs(ticker: str) -> dict[str, Path]:
    """Return source example directories for a ticker."""
    ticker = ticker.upper()
    return {
        "candidate": EXAMPLES / "xbrl_extraction_runs" / ticker,
        "workbench": EXAMPLES / "xbrl_review_workbenches" / ticker,
        "quality": EXAMPLES / "xbrl_review_quality" / ticker,
        "review": EXAMPLES / "xbrl_review_decisions" / ticker,
        "promotion": EXAMPLES / "xbrl_promotion_runs" / ticker,
    }


def scan_forbidden_text(path: Path) -> None:
    """Reject forbidden conclusion text in generated Markdown reports."""
    for markdown in path.rglob("*.md"):
        lowered = markdown.read_text(encoding="utf-8").lower()
        for term in FORBIDDEN_TERMS:
            if term in lowered:
                raise ValueError(f"Forbidden conclusion text in {markdown}: {term}")


def base_manifest(mode: str, ticker: str, company: str, output_dir: Path) -> dict[str, Any]:
    """Build base pipeline manifest."""
    ticker = ticker.upper()
    return {
        "pipeline_schema_version": "v0.3.10",
        "pipeline_run_id": f"pipeline-{mode}-{ticker.lower()}-{utc_now().replace(':', '').replace('+', 'z')}",
        "mode": mode,
        "ticker": ticker,
        "company": company,
        "fixture_data_status": "fictional_sample" if ticker == FICTIONAL_TICKER else "synthetic_or_excerpt_review_only",
        "run_steps": [],
        "input_paths": {},
        "output_paths": {},
        "blocked_steps": blocked_steps_for(mode, ticker),
        "warnings": [],
        "audit_references": {},
        "no_investment_conclusion": True,
        "created_at": utc_now(),
        "output_dir": relative_or_absolute(output_dir),
    }


def add_step(manifest: dict[str, Any], step: str, status: str, path: Path | None = None) -> None:
    """Append a run step and optional output path."""
    manifest["run_steps"].append({"step": step, "status": status})
    if path is not None:
        manifest["output_paths"][step] = relative_or_absolute(path)


def run_fictional(mode: str, ticker: str, company: str, output_dir: Path) -> dict[str, Any]:
    """Run EXMP fictional sandbox pipeline."""
    sources = source_dirs(ticker)
    manifest = base_manifest(mode, ticker, company, output_dir)
    for name in ("candidate", "workbench", "quality", "review", "promotion"):
        copy_dir(sources[name], output_dir / name)
        manifest["input_paths"][name] = relative_or_absolute(sources[name])
        add_step(manifest, name, "copied_local_fixture", output_dir / name)
    normalized = output_dir / "normalized_csv_sandbox"
    dry_run = output_dir / "v02_ratio_dry_run"
    audit = output_dir / "end_to_end_audit"
    run_generator(
        output_dir / "promotion",
        output_dir / "review" / "normalized_review_batch.json",
        output_dir / "candidate" / "extraction_candidates.json",
        output_dir / "candidate" / "extraction_run_manifest.json",
        normalized,
    )
    add_step(manifest, "normalized_csv_sandbox", "passed", normalized)
    run_dry_run(normalized / "normalized_financials_sandbox.csv", dry_run)
    add_step(manifest, "v02_ratio_dry_run", "passed", dry_run)
    audit.mkdir(parents=True, exist_ok=True)
    errors = audit_pipeline(
        output_dir / "candidate",
        output_dir / "quality",
        output_dir / "review",
        output_dir / "promotion",
        normalized,
        dry_run,
        audit / "end_to_end_audit_report.md",
    )
    if errors:
        raise ValueError(f"End-to-end audit failed: {errors}")
    add_step(manifest, "end_to_end_audit", "passed", audit)
    csv_manifest = load_json(normalized / "normalized_csv_manifest.json")
    dry_manifest = load_json(dry_run / "v02_dry_run_manifest.json")
    manifest["audit_references"] = {
        "mapping_version": csv_manifest["mapping_version"],
        "snapshot_sha256": csv_manifest["snapshot_sha256"],
        "review_batch_id": csv_manifest["source_review_batch_id"],
        "promotion_id": csv_manifest["source_promotion_id"],
        "normalized_csv_manifest": relative_or_absolute(normalized / "normalized_csv_manifest.json"),
        "v02_dry_run_manifest": relative_or_absolute(dry_run / "v02_dry_run_manifest.json"),
        "dry_run_id": dry_manifest["dry_run_id"],
    }
    manifest["warnings"].append(
        "Fictional sandbox only; partial fields may make ratios unavailable."
        if mode == "fictional_sandbox_partial"
        else "Fictional sandbox only; not production research."
    )
    return manifest


def run_real_review_only(mode: str, ticker: str, company: str, output_dir: Path) -> dict[str, Any]:
    """Run real-company-shaped review-only pipeline."""
    sources = source_dirs(ticker)
    manifest = base_manifest(mode, ticker, company, output_dir)
    for name in ("candidate", "workbench", "quality", "review"):
        copy_dir(sources[name], output_dir / name)
        manifest["input_paths"][name] = relative_or_absolute(sources[name])
        add_step(manifest, name, "review_only_copied_local_fixture", output_dir / name)
    manifest["warnings"].extend(
        [
            "Real-company-shaped fixture remains draft/review-only.",
            "No promotion, no normalized CSV and no v0.2.x dry-run were generated.",
        ]
    )
    review = load_json(output_dir / "review" / "normalized_review_batch.json")
    candidate = load_json(output_dir / "candidate" / "extraction_run_manifest.json")
    manifest["audit_references"] = {
        "mapping_version": candidate["mapping_version"],
        "snapshot_sha256": candidate["snapshot_sha256"],
        "review_batch_id": review["review_batch_id"],
        "promotion_id": "blocked_not_applicable",
        "normalized_csv_manifest": "blocked_not_applicable",
        "v02_dry_run_manifest": "blocked_not_applicable",
    }
    block_report = output_dir / "blocked_steps_report.md"
    block_report.write_text(render_block_report(manifest), encoding="utf-8")
    add_step(manifest, "blocked_steps_report", "passed", block_report)
    return manifest


def render_block_report(manifest: dict[str, Any]) -> str:
    """Render blocked step proof."""
    rows = "\n".join(f"| {item['step']} | {item['reason']} |" for item in manifest["blocked_steps"])
    return f"""# Blocked Real-Company Pipeline Steps

| Step | Reason |
|---|---|
{rows}

## Boundary

- Ticker `{manifest['ticker']}` remains draft/review-only.
- No promotion output.
- No normalized CSV.
- No v0.2.x dry-run.
- Not investment data.
"""


def run_pipeline(mode: str, ticker: str, company: str, output_dir: Path, overwrite: bool = False) -> dict[str, Path]:
    """Run a review-gated offline pipeline mode."""
    validate_mode_ticker(mode, ticker)
    output_dir = output_dir.expanduser().resolve()
    prepare_output_dir(output_dir, overwrite)
    if mode.startswith("fictional_sandbox"):
        manifest = run_fictional(mode, ticker, company, output_dir)
    else:
        manifest = run_real_review_only(mode, ticker, company, output_dir)
    manifest_path = output_dir / "pipeline_run_manifest.json"
    report_path = output_dir / "pipeline_run_report.md"
    write_manifest(manifest_path, manifest)
    report_path.write_text(render_report(manifest), encoding="utf-8")
    scan_forbidden_text(output_dir)
    return {
        "pipeline_run_manifest": manifest_path,
        "pipeline_run_report": report_path,
    }


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run offline review-gated stock research pipeline.")
    parser.add_argument("--mode", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--company", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run_pipeline(args.mode, args.ticker, args.company, args.output_dir, args.overwrite)
    except (FileNotFoundError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("Wrote pipeline run:")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
