#!/usr/bin/env python3
"""Security boundary audit for goodluck-stock-research."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Sequence


RISK_PATTERNS = (
    re.compile(r"api_key\s*=", re.I),
    re.compile(r"password\s*=", re.I),
    re.compile(r"secret\s*=", re.I),
    re.compile(r"os\.environ"),
    re.compile(r"broker\.connect"),
    re.compile(r"place_order"),
    re.compile(r"execute_trade"),
)


def audit(repo_root: Path) -> list[str]:
    issues: list[str] = []
    roots = ["goodluck-stock-research/scripts", "goodluck-stock-research/pipeline", "goodluck-stock-research/qa", "goodluck-stock-research/reporting", "goodluck-stock-research/parser_readiness"]
    for root_name in roots:
        root = repo_root / root_name
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if "tests" in path.parts:
                continue
            if path.name in {"public_readiness_audit.py", "security_boundary_audit.py", "red_team_audit.py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern in RISK_PATTERNS:
                if pattern.search(text):
                    issues.append(f"{path}: {pattern.pattern}")
    return issues


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run security boundary audit.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    issues = audit(args.repo_root)
    if issues:
        print("\n".join(issues))
        return 1
    print("PASS: security boundary audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
