#!/usr/bin/env python3
"""v1.0 release-candidate audit."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass
class CheckResult:
    check: str
    passed: bool
    notes: str


def add(results: list[CheckResult], check: str, passed: bool, notes: str) -> None:
    results.append(CheckResult(check, passed, notes))


def audit(repo_root: Path) -> list[CheckResult]:
    results: list[CheckResult] = []
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    skill_readme = (repo_root / "goodluck-stock-research" / "README.md").read_text(encoding="utf-8")
    changelog = (repo_root / "CHANGELOG.md").read_text(encoding="utf-8")
    combined = (readme + "\n" + skill_readme + "\n" + changelog).lower()
    add(results, "README accuracy", "not production parser" in combined or "不是 production parser" in combined, "production parser boundary")
    add(results, "no live extraction claim", "live extraction enabled" not in combined, "docs scanned")
    add(results, "no investment advice claim", "不是投资建议" in combined or "not investment" in combined, "docs scanned")
    add(results, "CHANGELOG completeness", "stock-research-v0.9.1" in changelog and "stock-research-v0.8.1" in changelog, "recent phases present")
    add(results, "public readiness not auto true", "ready_for_public_release: yes" not in combined, "technical audit still requires user decision")
    add(results, "reporting exists", (repo_root / "goodluck-stock-research" / "reporting").is_dir(), "reporting module")
    add(results, "parser readiness exists", (repo_root / "goodluck-stock-research" / "parser_readiness").is_dir(), "parser_readiness module")
    return results


def render(results: list[CheckResult]) -> str:
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    failed = [item for item in results if not item.passed]
    return f"""# Release Candidate Audit

- Passed: {'Yes' if not failed else 'No'}
- ready_for_public_release: Needs user decision
- repository_should_remain_private: Yes

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run release-candidate audit.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    results = audit(args.repo_root)
    report = render(results)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    failed = [item for item in results if not item.passed]
    if failed:
        print(report)
        return 1
    print("PASS: release-candidate audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
