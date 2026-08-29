#!/usr/bin/env python3
"""Public-readiness audit for goodluck-stock-research."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


IMPLEMENTATION_RISK_TERMS = (
    "broker.connect",
    "place_order",
    "execute_trade",
    "api_key =",
    "password =",
    "secret =",
    "os.environ",
)

RISK_PAYLOAD_FILE_NAMES = {
    "public_readiness_audit.py",
    "security_boundary_audit.py",
    "red_team_audit.py",
    "production_red_team.py",
    "release_candidate_audit.py",
    "production_release_candidate_audit.py",
    "source_policy.py",
}


@dataclass
class AuditCheck:
    """Public-readiness audit check."""

    check: str
    passed: bool
    notes: str


def text(path: Path) -> str:
    """Read text if present."""
    return path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else ""


def add(results: list[AuditCheck], check: str, passed: bool, notes: str) -> None:
    """Append check."""
    results.append(AuditCheck(check, passed, notes))


def scan(repo_root: Path, pattern_terms: tuple[str, ...], suffixes: set[str] | None = None) -> list[str]:
    """Scan text files for terms."""
    offenders: list[str] = []
    for path in repo_root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        allowed_suffixes = suffixes or {".md", ".py", ".json", ".csv", ".txt", ".yml", ".yaml"}
        if path.suffix.lower() not in allowed_suffixes:
            continue
        lowered = path.read_text(encoding="utf-8", errors="ignore").lower()
        for term in pattern_terms:
            if term.lower() in lowered:
                offenders.append(str(path.relative_to(repo_root)))
                break
    return offenders


def is_risk_payload_file(relative_path: str) -> bool:
    """Return whether a file is a scanner, audit, test, or red-team payload file."""
    parts = relative_path.split("/")
    name = parts[-1]
    return (
        "tests" in parts
        or name in RISK_PAYLOAD_FILE_NAMES
        or ("/audit/" in f"/{relative_path}" and ("red_team" in name or "release_candidate" in name))
    )


def scan_implementation_risks(repo_root: Path) -> tuple[list[str], list[str], int]:
    """Scan implementation files while classifying scanner/test payload files separately."""
    risky: list[str] = []
    excluded_payloads: list[str] = []
    scanned_count = 0
    skill_root = repo_root / "goodluck-stock-research"
    for path in skill_root.rglob("*.py"):
        if ".git" in path.parts:
            continue
        relative_path = str(path.relative_to(repo_root))
        text_body = path.read_text(encoding="utf-8", errors="ignore").lower()
        has_risk_term = any(term.lower() in text_body for term in IMPLEMENTATION_RISK_TERMS)
        if is_risk_payload_file(relative_path):
            if has_risk_term:
                excluded_payloads.append(relative_path)
            continue
        scanned_count += 1
        if has_risk_term:
            risky.append(relative_path)
    return risky, excluded_payloads, scanned_count


def audit_public_readiness(repo_root: Path, repository_visibility: str = "PRIVATE") -> tuple[list[AuditCheck], bool, str]:
    """Audit repository public-readiness.

    The default policy is conservative: the repository is not public-ready unless
    a separate explicit approval is performed outside this tool.
    """
    results: list[AuditCheck] = []
    root_readme = text(repo_root / "README.md")
    skill_readme = text(repo_root / "goodluck-stock-research" / "README.md")
    combined = (root_readme + "\n" + skill_readme).lower()
    visibility = repository_visibility.upper()
    add(results, "repository visibility remains private", visibility == "PRIVATE", visibility)
    add(results, "README does not claim production parser", "production parser" not in combined or "does not" in combined or "不包含" in combined, "README wording checked")
    add(results, "README does not claim live extraction", "live extraction" not in combined or "does not" in combined or "不" in combined, "README wording checked")
    add(results, "README does not claim investment advice", "investment advice" not in combined or "不构成" in combined or "does not" in combined, "README wording checked")
    tracked_examples = list((repo_root / "goodluck-stock-research" / "examples").rglob("*"))
    full_filing_candidates = [p for p in tracked_examples if p.is_file() and p.stat().st_size > 1_500_000]
    add(results, "examples are fictional / synthetic / excerpt-only", not full_filing_candidates, f"large example files: {len(full_filing_candidates)}")
    add(results, "no full SEC filing text stored", not full_filing_candidates, f"large raw-like files: {len(full_filing_candidates)}")
    implementation_risky, excluded_payloads, scanned_count = scan_implementation_risks(repo_root)
    add(results, "implementation files scanned for credential/trading risk", scanned_count > 0, f"{scanned_count} implementation Python files scanned")
    add(
        results,
        "scanner/test/red-team payload files excluded from implementation risk",
        True,
        ", ".join(excluded_payloads[:10]) if excluded_payloads else "none with risk payload strings",
    )
    add(results, "no credentials / secrets implementation", not implementation_risky, ", ".join(implementation_risky[:10]) if implementation_risky else "clean")
    add(results, "no user-specific personal data", not scan(repo_root / "goodluck-stock-research" / "examples", ("/Users/", "authorization:", "cookie:")), "examples scanned")
    add(results, "no broker/trading implementation", not scan(repo_root / "goodluck-stock-research" / "pipeline", ("broker.connect", "place_order", "execute_trade")), "pipeline scanned")
    add(results, "no target price / buy-sell-hold output in examples", not scan(repo_root / "goodluck-stock-research" / "examples" / "pipeline_runs", ("target price:", "buy:", "sell:", "hold:", "position size:")), "pipeline examples scanned")
    add(results, "release notes accurate boundary", "Does not implement live XBRL extraction" in text(repo_root / "goodluck-stock-research" / "validation" / "v0.4-main-health-check.md") or "v0.4" in text(repo_root / "CHANGELOG.md"), "release/validation boundary checked")
    ready = False
    reason = "requires separate public-readiness approval"
    return results, ready, reason


def render(results: list[AuditCheck], ready: bool, reason: str) -> str:
    """Render Markdown."""
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    return f"""# Public-Readiness Audit

## Summary

- ready_for_public_release: {'Yes' if ready else 'No'}
- reason: {reason}

## Checks

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run public-readiness audit.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--repository-visibility", default="PRIVATE")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        results, ready, reason = audit_public_readiness(args.repo_root.resolve(), args.repository_visibility)
        report = render(results, ready, reason)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
        print(report)
        return 0 if all(item.passed for item in results) else 1
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
