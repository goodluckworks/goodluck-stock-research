#!/usr/bin/env python3
"""Audit real-company workflow outputs."""

from __future__ import annotations

import json
from pathlib import Path


REQUIRED_OUTPUTS = {
    "source_manifest.json",
    "filing_identity.json",
    "normalized_financials/normalized_statement.json",
    "market_data_manifest.json",
    "data_quality_report.md",
    "valuation_scenarios.json",
    "research_conclusion.json",
    "research_report_draft.md",
    "workflow_audit_report.md",
}


def audit_workflow(run_dir: Path) -> list[str]:
    issues: list[str] = []
    for rel in REQUIRED_OUTPUTS:
        if not (run_dir / rel).is_file():
            issues.append(f"missing {rel}")
    manifest_path = run_dir / "workflow_manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("broker_trading_order_workflow") != "none":
            issues.append("broker/trading/order workflow present")
        if manifest.get("personalized_advice") != "none":
            issues.append("personalized advice present")
    report = (run_dir / "research_report_draft.md").read_text(encoding="utf-8", errors="ignore") if (run_dir / "research_report_draft.md").is_file() else ""
    lowered = report.lower()
    for forbidden in ("buy now", "sell now", "position size:", "execute trade", "guaranteed upside"):
        if forbidden in lowered:
            issues.append(f"forbidden report term: {forbidden}")
    return issues
