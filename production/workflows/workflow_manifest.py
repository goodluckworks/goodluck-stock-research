#!/usr/bin/env python3
"""Workflow manifest helpers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def build_workflow_manifest(ticker: str, status: str, outputs: dict[str, str], caveats: list[str]) -> dict[str, Any]:
    return {
        "workflow_schema_version": "v2.6.0",
        "ticker": ticker,
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "outputs": outputs,
        "caveats": caveats,
        "broker_trading_order_workflow": "none",
        "personalized_advice": "none",
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
