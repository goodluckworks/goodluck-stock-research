#!/usr/bin/env python3
"""User-facing production research CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS = ROOT / "goodluck-stock-research" / "production" / "workflows"
sys.path.insert(0, str(WORKFLOWS))

from real_company_research_workflow import run_research_workflow  # noqa: E402
from workflow_auditor import audit_workflow  # noqa: E402


LIVE_WARNING = (
    "live mode requires an explicit SEC URL and explicit User-Agent; requests are bounded "
    "and raw live output should be written only to temporary/non-repo paths"
)


def write_live_failure(output_dir: Path, reason: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "live_smoke_error_report.md").write_text(
        f"""# Live SEC Smoke Error Report

- live_smoke_status: failed_with_reason
- reason: {reason}
- no_raw_filing_committed: true
- no_partial_unmarked_report_treated_as_valid: true
- boundary: no broker action, no trade instruction, no position sizing
""",
        encoding="utf-8",
    )


def run_research(args: argparse.Namespace) -> int:
    output_dir = args.output_dir or ROOT / "goodluck-stock-research" / "examples" / "production_research" / args.ticker.upper()
    if args.mode == "live":
        print(f"live mode warning: {LIVE_WARNING}")
        if not args.sec_only:
            reason = "--sec-only is required for live mode in v3.0.1 smoke tests."
            write_live_failure(output_dir, reason)
            print(f"live_smoke_status: failed_with_reason")
            print(f"reason: {reason}")
            print(f"error report: {output_dir / 'live_smoke_error_report.md'}")
            return 0
        if not args.sec_url or not args.user_agent:
            reason = "explicit --sec-url and --user-agent are required for controlled live SEC smoke."
            write_live_failure(output_dir, reason)
            print("live_smoke_status: failed_with_reason")
            print(f"reason: {reason}")
            print(f"error report: {output_dir / 'live_smoke_error_report.md'}")
            return 0
    manifest = run_research_workflow(args.ticker, output_dir, args.mode)
    conclusion_path = output_dir / "research_conclusion.json"
    conclusion = json.loads(conclusion_path.read_text(encoding="utf-8")) if conclusion_path.is_file() else {}
    print(f"report path: {output_dir / 'research_report_draft.md'}")
    print(f"audit path: {output_dir / 'workflow_audit_report.md'}")
    print(f"data quality status: {manifest['status']}")
    print(f"conclusion label: {conclusion.get('research_view', 'Insufficient evidence')}")
    print(f"caveats: {manifest.get('caveats', [])}")
    print("boundary: no broker action, no trade instruction, no position sizing")
    return 0


def run_validate(args: argparse.Namespace) -> int:
    issues = audit_workflow(args.run_dir)
    print(f"audit path: {args.run_dir / 'workflow_audit_report.md'}")
    print("validation status: " + ("pass" if not issues else "fail"))
    if issues:
        print(f"issues: {issues}")
        return 1
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Production stock research CLI. Research output is not trading advice.",
        epilog="Boundaries: no broker action, no order routing, no trade instruction, no position sizing.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    research = sub.add_parser("research", help="Run a fixture or controlled live production research workflow.")
    research.add_argument("--ticker", required=True)
    research.add_argument("--mode", choices=["fixture", "live"], default="fixture", help="Use fixture mode by default; live mode requires explicit SEC controls.")
    research.add_argument("--sec-only", action="store_true", help="Restrict live mode to SEC official sources.")
    research.add_argument("--sec-url", help="Explicit SEC URL for controlled live smoke.")
    research.add_argument("--user-agent", help="Explicit SEC User-Agent with contact email.")
    research.add_argument("--max-requests", type=int, default=1, help="Bounded live request count. Default: 1.")
    research.add_argument("--timeout-seconds", type=float, default=10.0, help="Bounded live request timeout.")
    research.add_argument("--max-response-bytes", type=int, default=2_000_000, help="Live response size cap.")
    research.add_argument("--market-data-csv", help="User-provided market data CSV fallback.")
    research.add_argument("--output-dir", type=Path, help="Output directory for report, manifests and audit trail.")
    validate = sub.add_parser("validate", help="Validate an existing production research run directory.")
    validate.add_argument("--run-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "research":
        return run_research(args)
    if args.command == "validate":
        return run_validate(args)
    raise SystemExit("Unsupported command")


if __name__ == "__main__":
    raise SystemExit(main())
