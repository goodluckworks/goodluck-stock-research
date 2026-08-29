#!/usr/bin/env python3
"""CLI usability audit helpers."""

from __future__ import annotations


REQUIRED_HELP_TERMS = ("research", "validate", "fixture", "live", "sec", "market-data-csv", "no broker", "position sizing")


def audit_help_text(help_text: str) -> list[str]:
    lowered = help_text.lower()
    return [f"missing help term: {term}" for term in REQUIRED_HELP_TERMS if term not in lowered]


def audit_command_output(output: str) -> list[str]:
    lowered = output.lower()
    issues: list[str] = []
    for required in ("report path:", "audit path:", "data quality status:", "conclusion label:", "caveats:"):
        if required not in lowered:
            issues.append(f"missing output field: {required}")
    for boundary in ("no broker", "no trade instruction", "no position sizing"):
        if boundary not in lowered:
            issues.append(f"missing boundary warning: {boundary}")
    return issues


def audit_error_message(output: str) -> list[str]:
    lowered = output.lower()
    if "failed_with_reason" not in lowered:
        return ["error message missing failed_with_reason"]
    if "explicit --sec-url and --user-agent" not in lowered and "--sec-only is required" not in lowered:
        return ["error message missing clear live-mode remediation"]
    return []
