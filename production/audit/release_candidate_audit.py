#!/usr/bin/env python3
"""Production release-candidate audit."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def audit(repo_root: Path) -> list[str]:
    issues: list[str] = []
    required = [
        "production/ingestion/sec_live_ingestor.py",
        "production/xbrl_parser/production_xbrl_parser.py",
        "production/normalization/financial_statement_builder.py",
        "production/data_quality/data_quality_engine.py",
        "production/valuation/valuation_engine.py",
        "production/conclusion/research_conclusion_engine.py",
        "production/report_generation/production_report_builder.py",
        "production/approval_gate/approval_gate.py",
        "production/pilot/mrvl_production_pilot.py",
    ]
    for rel in required:
        if not (repo_root / "goodluck-stock-research" / rel).exists():
            issues.append(f"missing {rel}")
    for path in (repo_root / "goodluck-stock-research").rglob("*"):
        if path.name == ".DS_Store" or "__pycache__" in path.parts:
            issues.append(f"cache artifact: {path}")
        if path.is_file() and path.stat().st_size > 2_000_000:
            issues.append(f"large artifact: {path}")
    return issues


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run production release-candidate audit.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    issues = audit(args.repo_root)
    if issues:
        print("\n".join(issues))
        return 1
    print("PASS: production release-candidate audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
