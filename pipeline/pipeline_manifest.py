#!/usr/bin/env python3
"""Pipeline run manifest helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    """Write deterministic manifest JSON."""
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
