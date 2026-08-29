#!/usr/bin/env python3
"""Artifact hygiene checker for tracked goodluck-stock-research files."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


TEXT_SUFFIXES = {".md", ".json", ".csv", ".txt", ".yaml", ".yml"}
GENERATED_CACHE_NAMES = {".ds_store", "__pycache__"}
RAW_FILING_SUFFIXES = {".htm", ".html", ".xml", ".xhtml"}


@dataclass
class HygieneCheck:
    """Hygiene check result."""

    check: str
    passed: bool
    notes: str


def rel(path: Path, root: Path) -> str:
    """Repo-relative display path."""
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def add(results: list[HygieneCheck], check: str, passed: bool, notes: str) -> None:
    """Append check."""
    results.append(HygieneCheck(check, passed, notes))


def iter_files(repo_root: Path) -> list[Path]:
    """Return files excluding .git."""
    return [path for path in repo_root.rglob("*") if path.is_file() and ".git" not in path.parts]


def check_hygiene(repo_root: Path) -> list[HygieneCheck]:
    """Run artifact hygiene checks."""
    results: list[HygieneCheck] = []
    files = iter_files(repo_root)
    cache = [path for path in files if path.name.lower() in GENERATED_CACHE_NAMES or ".pyc" == path.suffix]
    ds_store = [path for path in files if path.name == ".DS_Store"]
    raw_filings = [
        path
        for path in files
        if path.suffix.lower() in RAW_FILING_SUFFIXES
        and "fixtures" not in path.parts
        and "validation" not in path.parts
    ]
    users_paths: list[str] = []
    tmp_paths: list[str] = []
    artifact_roots = (
        repo_root / "goodluck-stock-research" / "examples",
        repo_root / "goodluck-stock-research" / "validation",
    )
    for path in files:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if not any(path.resolve().is_relative_to(root.resolve()) for root in artifact_roots):
            continue
        display = rel(path, repo_root)
        content = path.read_text(encoding="utf-8", errors="ignore")
        if "/Users/" in content and "/validation/" not in "/" + display:
            users_paths.append(display)
        if "/private/tmp" in content and "/validation/" not in "/" + display:
            tmp_paths.append(display)
    add(results, "no .DS_Store tracked", not ds_store, ", ".join(rel(p, repo_root) for p in ds_store[:10]) if ds_store else "clean")
    add(results, "no generated cache files tracked", not cache, ", ".join(rel(p, repo_root) for p in cache[:10]) if cache else "clean")
    add(results, "no raw full filings committed", not raw_filings, ", ".join(rel(p, repo_root) for p in raw_filings[:10]) if raw_filings else "clean")
    add(results, "no /Users path leaks", not users_paths, ", ".join(users_paths[:10]) if users_paths else "clean")
    add(results, "no /private/tmp raw evidence committed", not tmp_paths, ", ".join(tmp_paths[:10]) if tmp_paths else "clean")
    return results


def render(results: list[HygieneCheck]) -> str:
    """Render Markdown."""
    rows = "\n".join(f"| {item.check} | {'Pass' if item.passed else 'Fail'} | {item.notes} |" for item in results)
    failed = [item for item in results if not item.passed]
    return f"""# Artifact Hygiene Report

## Summary

- Passed: {'Yes' if not failed else 'No'}
- Failed checks: {len(failed)}

## Checks

| Check | Result | Notes |
|---|---:|---|
{rows}
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Run artifact hygiene checks.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        results = check_hygiene(args.repo_root.resolve())
        report = render(results)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
        print(report)
        return 0 if all(item.passed for item in results) else 1
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
