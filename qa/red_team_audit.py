#!/usr/bin/env python3
"""Repository-level red-team audit for report packets and public readiness."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

REPORTING_DIR = Path(__file__).resolve().parents[1] / "reporting"
sys.path.insert(0, str(REPORTING_DIR))

from report_red_team import red_team_file  # noqa: E402


def audit(repo_root: Path) -> list[str]:
    issues: list[str] = []
    packet_root = repo_root / "goodluck-stock-research" / "examples" / "report_packets"
    for report in sorted(packet_root.glob("*/report_packet.md")):
        for issue in red_team_file(report):
            issues.append(f"{report}: {issue}")
    readiness_files = sorted((repo_root / "goodluck-stock-research" / "validation").glob("*public*")) + [
        repo_root / "goodluck-stock-research" / "validation" / "v0.6-controlled-sandbox-final-validation.md"
    ]
    for path in readiness_files:
        if path.exists() and "ready_for_public_release: Yes" in path.read_text(encoding="utf-8", errors="ignore"):
            issues.append(f"{path}: public readiness wrongly true")
    return issues


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run red-team audit.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    issues = audit(args.repo_root)
    if issues:
        print("\n".join(issues))
        return 1
    print("PASS: red-team audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
