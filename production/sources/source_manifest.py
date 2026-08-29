#!/usr/bin/env python3
"""Source manifest helpers."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_manifest(source_type: str, source: str, payload: str, reliability: str, status: str) -> dict[str, Any]:
    return {
        "schema_version": "v2.1.0",
        "source_type": source_type,
        "source": source,
        "reliability": reliability,
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "raw_response_sha256": sha256_text(payload),
        "credential_workflow": "none",
        "broker_trading_workflow": "none",
    }


def write_manifest(manifest: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
