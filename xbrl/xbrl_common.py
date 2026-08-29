#!/usr/bin/env python3
"""Shared local-file helpers for the v0.3.4 XBRL prototype."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REAL_TICKERS = {"MRVL", "NVDA", "AVGO"}


def utc_now() -> str:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    """Return the SHA-256 checksum of a local file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from a local file."""
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, payload: object) -> None:
    """Write deterministic UTF-8 JSON."""
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def require_text(name: str, value: object) -> str:
    """Return nonblank string input."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a nonblank string.")
    return value.strip()


def require_finite_number(name: str, value: object) -> float | int:
    """Validate a finite numeric value, excluding booleans."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a number.")
    if not math.isfinite(float(value)):
        raise ValueError(f"{name} must be finite.")
    return value


def prepare_output_dir(output_dir: Path, overwrite: bool) -> bool:
    """Create an output directory with explicit overwrite behavior."""
    existing = list(output_dir.iterdir()) if output_dir.is_dir() else []
    if existing and not overwrite:
        raise FileExistsError(
            f"Output directory is not empty: {output_dir}. Use --overwrite."
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    return bool(existing and overwrite)


def relative_or_absolute(path: Path) -> str:
    """Prefer a current-working-directory-relative path."""
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(resolved)


def ensure_distinct_paths(*paths: Path) -> None:
    """Reject identical resolved paths."""
    resolved = [path.expanduser().resolve() for path in paths]
    if len(set(resolved)) != len(resolved):
        raise ValueError("Input, mapping, report and output paths must be distinct.")
