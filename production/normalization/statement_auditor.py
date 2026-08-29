#!/usr/bin/env python3
"""Audit normalized statement artifacts."""

from __future__ import annotations

import json
from pathlib import Path


def audit(output_dir: Path) -> list[str]:
    issues: list[str] = []
    manifest = json.loads((output_dir / "normalization_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("no_zero_fill") is not True:
        issues.append("no_zero_fill flag missing")
    rows = []
    for name in ("normalized_income_statement.json", "normalized_balance_sheet.json", "normalized_cash_flow.json"):
        rows.extend(json.loads((output_dir / name).read_text(encoding="utf-8")))
    for row in rows:
        for field in ("source_locator", "concept_qname", "confidence", "review_status", "amount_unit"):
            if not row.get(field):
                issues.append(f"{row.get('field')}: missing {field}")
    return issues
