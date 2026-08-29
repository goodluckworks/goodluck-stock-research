#!/usr/bin/env python3
"""Red-team checks for report packets."""

from __future__ import annotations

from pathlib import Path

from report_policy import forbidden_hits


def red_team_text(text: str) -> list[str]:
    issues: list[str] = []
    issues.extend(f"forbidden conclusion term: {hit}" for hit in forbidden_hits(text))
    lowered = text.lower()
    if "quarantined data is production" in lowered or "production data: yes" in lowered:
        issues.append("quarantined data treated as production")
    if "draft candidates are facts" in lowered or "candidate fact: yes" in lowered:
        issues.append("draft candidate treated as fact")
    if "audit" not in lowered and "evidence" not in lowered:
        issues.append("audit references omitted")
    if "unresolved" not in lowered and "missing evidence" not in lowered and "fictional" not in lowered:
        issues.append("unresolved fields or missing evidence omitted")
    if "not investment" not in lowered and "not for trading" not in lowered:
        issues.append("no-investment boundary omitted")
    if "/users/" in lowered:
        issues.append("personal local path leak")
    return issues


def red_team_file(path: Path) -> list[str]:
    return red_team_text(path.read_text(encoding="utf-8", errors="ignore"))
