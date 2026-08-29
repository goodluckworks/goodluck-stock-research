#!/usr/bin/env python3
"""Production research report draft builder."""

from __future__ import annotations

from typing import Any


def build_report(ticker: str, statement: dict[str, Any], valuation: dict[str, Any], conclusion: dict[str, Any]) -> str:
    return f"""# {ticker} Production Research Report Draft

## Executive Summary

Research view: {conclusion.get('conclusion_label')}
Confidence: {conclusion.get('confidence')}

## Company Overview

Ticker: {ticker}

## Business Drivers

- Revenue and margin scenarios are assessed from normalized statements.

## Financial Analysis

- Fiscal period: {statement.get('fiscal_period')}
- Parsed rows: {len(statement.get('rows', []))}
- Unresolved fields: {len(statement.get('unresolved_fields', []))}

## Valuation Scenarios

- Fair value range: {valuation.get('fair_value_range')}
- This is scenario output, not recommendation.

## Research Conclusion

- Evidence basis: {conclusion.get('evidence_basis')}
- Valuation basis: {conclusion.get('valuation_basis')}

## Data Quality and Caveats

- Caveats: {conclusion.get('data_quality_caveats')}
- Missing evidence: {conclusion.get('missing_evidence')}

## Risks

- Key downside risks: {conclusion.get('key_downside_risks')}

## Audit Trail

- Normalized statement builder.
- Data quality gate.
- Valuation scenario engine.
- Conclusion auditor.

## Boundary

Not personalized advice. Not a trading instruction. No broker recommendation. No position sizing.
"""


def audit_report(text: str) -> list[str]:
    issues: list[str] = []
    lowered = text.lower()
    for forbidden in ("buy now", "sell now", "position size:", "trade instruction:", "broker order"):
        if forbidden in lowered:
            issues.append(forbidden)
    for required in ("executive summary", "financial analysis", "valuation scenarios", "research conclusion", "audit trail"):
        if required not in lowered:
            issues.append(f"missing {required}")
    return issues
