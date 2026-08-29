#!/usr/bin/env python3
"""Source monitoring helpers."""

from __future__ import annotations

from typing import Any


def monitor_sources(sources: list[dict[str, Any]]) -> dict[str, Any]:
    unavailable = [item for item in sources if item.get("status") not in {"available", "cached"}]
    return {
        "monitor_schema_version": "v2.8.0",
        "source_count": len(sources),
        "unavailable_count": len(unavailable),
        "unavailable_sources": unavailable,
        "partial_report_allowed": len(unavailable) < len(sources),
        "silent_failure": False,
    }
