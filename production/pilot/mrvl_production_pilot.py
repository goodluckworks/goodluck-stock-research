#!/usr/bin/env python3
"""MRVL production research pilot using local fixture pipeline."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

PROD = Path(__file__).resolve().parents[1]
for sub in ("xbrl_parser", "normalization", "data_quality", "valuation", "conclusion", "report_generation", "approval_gate"):
    sys.path.insert(0, str(PROD / sub))

import production_xbrl_parser  # noqa: E402
import financial_statement_builder  # noqa: E402
import data_quality_engine  # noqa: E402
import reconciliation_engine  # noqa: E402
import quality_gate  # noqa: E402
import valuation_engine  # noqa: E402
import research_conclusion_engine  # noqa: E402
import conclusion_auditor  # noqa: E402
import production_report_builder  # noqa: E402
import approval_gate  # noqa: E402
import publication_manifest  # noqa: E402


def run_pilot(repo_root: Path, output_dir: Path, human_approval: bool = False) -> dict[str, Any]:
    package_path = repo_root / "goodluck-stock-research" / "production" / "xbrl_parser" / "fixtures" / "standard_10k_package.json"
    package = production_xbrl_parser.load_package(package_path)
    parsed = production_xbrl_parser.parse_package(package)
    statement = financial_statement_builder.build(parsed)
    quality = data_quality_engine.score_quality(statement)
    recon = reconciliation_engine.reconcile(statement)
    gate = quality_gate.gate(quality, recon)
    valuation = valuation_engine.value_company(statement, gate)
    conclusion = research_conclusion_engine.generate_conclusion(quality, valuation, ["fixture filing package", "normalized statement", "quality gate"])
    conclusion_issues = conclusion_auditor.audit(conclusion)
    report = production_report_builder.build_report("MRVL", statement, valuation, conclusion)
    report_issues = production_report_builder.audit_report(report)
    approval = approval_gate.evaluate_approval(gate, conclusion_issues, report_issues, {"approved": True, "reviewer": "fixture_reviewer"} if human_approval else None)
    manifest = publication_manifest.build_manifest("MRVL", approval)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "mrvl_internal_research_packet.md").write_text(report, encoding="utf-8")
    (output_dir / "mrvl_publication_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (output_dir / "mrvl_pilot_audit.json").write_text(
        json.dumps(
            {
                "pilot_schema_version": "v1.9.0",
                "ticker": "MRVL",
                "quality_gate": gate,
                "conclusion_issues": conclusion_issues,
                "report_issues": report_issues,
                "approval": approval,
                "not_personalized_advice": True,
                "not_trading_instruction": True,
                "not_broker_recommendation": True,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return {"quality_gate": gate, "approval": approval, "manifest": manifest, "report": report}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MRVL production pilot.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--human-approval", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    run_pilot(args.repo_root, args.output_dir, human_approval=args.human_approval)
    print("PASS: MRVL production pilot")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
