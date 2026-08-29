#!/usr/bin/env python3
"""Final red-team checks before v3.0 release."""

from __future__ import annotations

from pathlib import Path


FORBIDDEN_REPORT_TERMS = ("buy now", "sell now", "hold this", "position size", "personalized advice", "execute trade", "guaranteed upside")


def audit_report_text(text: str) -> list[str]:
    lowered = text.lower()
    issues = [f"forbidden report term: {term}" for term in FORBIDDEN_REPORT_TERMS if term in lowered]
    if "caveat" not in lowered and "caveats" not in lowered:
        issues.append("report missing caveats")
    if "low" in lowered and "insufficient evidence" not in lowered and "blocked" not in lowered:
        issues.append("low confidence conclusion not blocked or caveated")
    return issues


def audit_artifact_paths(root: Path) -> list[str]:
    issues: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if path.stat().st_size > 1_500_000 and "raw" in path.name.lower():
            issues.append(f"raw filing committed: {path}")
        if any(term in text.lower() for term in ("api_key =", "password =", "secret =")):
            issues.append(f"secret leakage: {path}")
        if "/users/" in text.lower():
            issues.append(f"local path leakage: {path}")
    return issues
