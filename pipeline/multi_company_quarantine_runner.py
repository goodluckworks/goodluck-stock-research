#!/usr/bin/env python3
"""Controlled multi-company quarantine drill summary."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


TRACKED = ("MRVL", "NVDA", "AVGO")


@dataclass
class CompanyQuarantineStatus:
    ticker: str
    result: str
    reason: str
    tracked_output: str


def evaluate(repo_root: Path) -> list[CompanyQuarantineStatus]:
    root = repo_root / "goodluck-stock-research" / "examples" / "real_company_quarantine"
    statuses: list[CompanyQuarantineStatus] = []
    mrvl = root / "MRVL" / "quarantine_manifest.json"
    statuses.append(
        CompanyQuarantineStatus(
            ticker="MRVL",
            result="pass" if mrvl.exists() else "blocked",
            reason="controlled quarantine manifest present" if mrvl.exists() else "missing MRVL quarantine manifest",
            tracked_output="goodluck-stock-research/examples/real_company_quarantine/MRVL" if mrvl.exists() else "none",
        )
    )
    for ticker in ("NVDA", "AVGO"):
        path = root / ticker
        statuses.append(
            CompanyQuarantineStatus(
                ticker=ticker,
                result="blocked" if not path.exists() else "fail",
                reason="insufficient explicit quarantine gate data; no tracked output created" if not path.exists() else "unexpected tracked quarantine output exists",
                tracked_output="none" if not path.exists() else str(path),
            )
        )
    return statuses


def render(statuses: list[CompanyQuarantineStatus]) -> str:
    rows = "\n".join(f"| {item.ticker} | {item.result} | {item.reason} | {item.tracked_output} |" for item in statuses)
    return f"""# Real-Company Quarantine Dashboard

All real-company outputs are non-production, non-investment, not for trading and not for public release.

| Ticker | Result | Reason | Tracked Output |
|---|---|---|---|
{rows}

## Boundary

- No production normalized input.
- No full research report.
- No investment conclusion.
- No target price, buy/sell/hold, position size or research status.
"""


def write_outputs(repo_root: Path, output_dir: Path) -> None:
    statuses = evaluate(repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "multi_company_quarantine_dashboard.md").write_text(render(statuses), encoding="utf-8")
    (output_dir / "multi_company_quarantine_summary.json").write_text(
        json.dumps([item.__dict__ for item in statuses], indent=2) + "\n",
        encoding="utf-8",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render controlled multi-company quarantine dashboard.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    write_outputs(args.repo_root, args.output_dir)
    statuses = evaluate(args.repo_root)
    if any(item.result == "fail" for item in statuses):
        print(render(statuses))
        return 1
    print("PASS: multi-company quarantine drill")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
