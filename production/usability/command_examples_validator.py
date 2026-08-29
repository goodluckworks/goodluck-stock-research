#!/usr/bin/env python3
"""Command example validator for docs and smoke tests."""

from __future__ import annotations

import shlex


EXAMPLES = [
    "python3 goodluck-stock-research/production/cli.py --help",
    "python3 goodluck-stock-research/production/cli.py research --ticker MRVL --mode fixture",
    "python3 goodluck-stock-research/production/cli.py validate --run-dir goodluck-stock-research/examples/production_research/MRVL",
]


def validate_example(command: str) -> list[str]:
    parts = shlex.split(command)
    issues: list[str] = []
    if not parts or parts[0] != "python3":
        issues.append("example must start with python3")
    if "goodluck-stock-research/production/cli.py" not in parts:
        issues.append("example must use production CLI")
    if "research" in parts and "--ticker" not in parts:
        issues.append("research example missing --ticker")
    if "validate" in parts and "--run-dir" not in parts:
        issues.append("validate example missing --run-dir")
    return issues


def validate_examples(commands: list[str] = EXAMPLES) -> list[str]:
    issues: list[str] = []
    for command in commands:
        issues.extend(f"{command}: {issue}" for issue in validate_example(command))
    return issues
