#!/usr/bin/env python3
"""Deterministic source cache helpers."""

from __future__ import annotations

import hashlib
from pathlib import Path


def cache_key(source_type: str, source: str) -> str:
    return hashlib.sha256(f"{source_type}:{source}".encode("utf-8")).hexdigest()[:24]


def write_cache(cache_dir: Path, source_type: str, source: str, payload: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = cache_dir / f"{cache_key(source_type, source)}.txt"
    path.write_text(payload, encoding="utf-8")
    return path


def read_cache(cache_dir: Path, source_type: str, source: str) -> str | None:
    path = cache_dir / f"{cache_key(source_type, source)}.txt"
    return path.read_text(encoding="utf-8") if path.is_file() else None
