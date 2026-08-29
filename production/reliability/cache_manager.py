#!/usr/bin/env python3
"""Cache manager for production workflows."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def cache_key(source: str, version: str) -> str:
    return hashlib.sha256(f"{version}:{source}".encode("utf-8")).hexdigest()[:24]


def write_cache_entry(cache_dir: Path, source: str, version: str, payload: str) -> dict[str, Any]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = cache_key(source, version)
    data_path = cache_dir / f"{key}.txt"
    data_path.write_text(payload, encoding="utf-8")
    manifest = {
        "cache_key": key,
        "source": source,
        "version": version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "payload_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "stale_warning": False,
    }
    (cache_dir / f"{key}.manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def mark_stale(manifest: dict[str, Any]) -> dict[str, Any]:
    updated = dict(manifest)
    updated["stale_warning"] = True
    return updated
