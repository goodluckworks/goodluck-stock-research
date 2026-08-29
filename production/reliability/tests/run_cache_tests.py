#!/usr/bin/env python3
"""Tests for cache manager."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REL = ROOT / "goodluck-stock-research" / "production" / "reliability"
sys.path.insert(0, str(REL))

from cache_manager import cache_key, mark_stale, write_cache_entry  # noqa: E402


def main() -> int:
    assert cache_key("source", "v1") == cache_key("source", "v1")
    with tempfile.TemporaryDirectory() as tmp:
        manifest = write_cache_entry(Path(tmp), "source", "v1", "payload")
        assert (Path(tmp) / f"{manifest['cache_key']}.txt").is_file()
        assert mark_stale(manifest)["stale_warning"] is True
    print("PASS: reliability cache tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
