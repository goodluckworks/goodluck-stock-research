#!/usr/bin/env python3
"""Render pipeline run reports."""

from __future__ import annotations

from typing import Any


def rows(items: list[dict[str, Any]], key_field: str = "step") -> str:
    """Render step rows."""
    if not items:
        return "| None | None |"
    return "\n".join(f"| {item.get(key_field, 'unknown')} | {item.get('status', item.get('reason', 'unknown'))} |" for item in items)


def render_report(manifest: dict[str, Any]) -> str:
    """Render a pipeline Markdown report."""
    return f"""# Review-Gated Pipeline Run Report

## Summary

- Pipeline run ID: `{manifest['pipeline_run_id']}`
- Mode: `{manifest['mode']}`
- Ticker: `{manifest['ticker']}`
- Company: `{manifest['company']}`
- Fixture data status: `{manifest['fixture_data_status']}`
- No investment conclusion: `{str(manifest['no_investment_conclusion']).lower()}`

## Run Steps

| Step | Status |
|---|---|
{rows(manifest.get('run_steps', []))}

## Blocked Steps

| Step | Reason |
|---|---|
{rows(manifest.get('blocked_steps', []))}

## Warnings

{chr(10).join(f"- {item}" for item in manifest.get('warnings', [])) or "- None"}

## Boundary

- Offline / fixture-first pipeline.
- Not investment data.
- Not production research.
- No target price, buy/sell/hold, position size, research status or trading action.
- Real-company-shaped runs are review-only and not approved.
"""
