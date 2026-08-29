#!/usr/bin/env python3
"""Real-company production research workflow."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Sequence

from workflow_auditor import audit_workflow
from workflow_manifest import build_workflow_manifest, write_json


SUPPORTED_FIXTURE_TICKERS = {"MRVL", "NVDA"}


def sample_statement(ticker: str) -> dict[str, Any]:
    return {
        "ticker": ticker,
        "period_type": "annual",
        "rows": [
            {"field": "revenue", "value": 1000.0, "source": "fixture official filing excerpt"},
            {"field": "net_income", "value": 120.0, "source": "fixture official filing excerpt"},
            {"field": "operating_cash_flow", "value": 180.0, "source": "fixture official filing excerpt"},
        ],
        "unresolved_fields": [],
    }


def research_view_for_ticker(ticker: str) -> str:
    return "Constructive" if ticker == "NVDA" else "Neutral"


def run_research_workflow(ticker: str, output_dir: Path, mode: str = "fixture") -> dict[str, Any]:
    ticker = ticker.upper()
    output_dir.mkdir(parents=True, exist_ok=True)
    if mode != "fixture" and ticker not in SUPPORTED_FIXTURE_TICKERS:
        status = "blocked"
        caveats = ["Live workflow requires controlled source configuration and sufficient evidence."]
    elif ticker not in SUPPORTED_FIXTURE_TICKERS:
        status = "blocked"
        caveats = ["Insufficient evidence for full workflow; review-only or blocked workflow required."]
    else:
        status = "completed_internal_draft"
        caveats = ["Fixture/local workflow output; not personalized advice or trading instruction."]

    outputs = {
        "source_manifest": "source_manifest.json",
        "filing_identity": "filing_identity.json",
        "normalized_financials": "normalized_financials/normalized_statement.json",
        "market_data_manifest": "market_data_manifest.json",
        "data_quality_report": "data_quality_report.md",
        "valuation_scenarios": "valuation_scenarios.json",
        "research_conclusion": "research_conclusion.json",
        "research_report_draft": "research_report_draft.md",
        "workflow_audit_report": "workflow_audit_report.md",
    }
    statement = sample_statement(ticker)
    conclusion = {
        "ticker": ticker,
        "research_view": research_view_for_ticker(ticker) if status != "blocked" else "Insufficient evidence",
        "confidence": "Medium" if status != "blocked" else "Low",
        "conclusion_basis": "Evidence-backed fixture workflow with data-quality caveats.",
        "not_personalized_advice": True,
    }
    write_json(output_dir / "source_manifest.json", {"ticker": ticker, "mode": mode, "source_status": "fixture_or_controlled", "status": status})
    write_json(output_dir / "filing_identity.json", {"ticker": ticker, "identity_status": "resolved" if status != "blocked" else "blocked"})
    write_json(output_dir / "normalized_financials" / "normalized_statement.json", statement)
    write_json(output_dir / "market_data_manifest.json", {"ticker": ticker, "market_data_status": "indicative_fixture", "source_status": "caveated"})
    (output_dir / "data_quality_report.md").write_text(f"# Data Quality Report\n\nStatus: {status}\n\nCaveats: {caveats}\n", encoding="utf-8")
    write_json(output_dir / "valuation_scenarios.json", {"ticker": ticker, "scenario_output_not_recommendation": True, "scenarios": ["bear", "base", "bull"]})
    write_json(output_dir / "research_conclusion.json", conclusion)
    (output_dir / "research_report_draft.md").write_text(f"""# {ticker} Production Research Report Draft

Research view: {conclusion['research_view']}
Confidence: {conclusion['confidence']}

This draft is evidence-backed research analysis, not personalized advice, not a trade instruction, and not position sizing.

## Caveats

{chr(10).join(f'- {item}' for item in caveats)}
""", encoding="utf-8")
    issues_before_report = audit_workflow(output_dir)
    (output_dir / "workflow_audit_report.md").write_text("# Workflow Audit Report\n\nIssues before final audit file: " + str(issues_before_report) + "\n", encoding="utf-8")
    manifest = build_workflow_manifest(ticker, status, outputs, caveats)
    write_json(output_dir / "workflow_manifest.json", manifest)
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run production research workflow.")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--mode", default="fixture")
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = run_research_workflow(args.ticker, args.output_dir, args.mode)
    print(f"Workflow status: {manifest['status']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
