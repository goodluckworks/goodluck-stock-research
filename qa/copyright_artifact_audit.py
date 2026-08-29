#!/usr/bin/env python3
"""Copyright and artifact hygiene audit for release candidates."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


FORBIDDEN_SUFFIXES = {".pyc"}
RAW_FILING_MARKERS = ("<html", "<xbrl", "document and entity information")


def audit(repo_root: Path) -> list[str]:
    issues: list[str] = []
    skill = repo_root / "goodluck-stock-research"
    for path in skill.rglob("*"):
        if path.name == ".DS_Store" or "__pycache__" in path.parts:
            issues.append(f"cache/system artifact: {path}")
        if path.is_file() and path.suffix in FORBIDDEN_SUFFIXES:
            issues.append(f"compiled artifact: {path}")
        if path.is_file() and path.stat().st_size > 1_000_000:
            issues.append(f"large artifact: {path}")
        if path.is_file() and "/raw/" in path.as_posix() and path.suffix.lower() in {".html", ".htm", ".txt"}:
            text = path.read_text(encoding="utf-8", errors="ignore")[:5000].lower()
            if any(marker in text for marker in RAW_FILING_MARKERS):
                issues.append(f"possible full filing text: {path}")
    return issues


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run copyright artifact audit.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    issues = audit(args.repo_root)
    if issues:
        print("\n".join(issues))
        return 1
    print("PASS: copyright artifact audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
