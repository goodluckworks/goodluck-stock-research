#!/usr/bin/env python3
"""Tests for artifact hygiene checker."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
QA_DIR = ROOT / "goodluck-stock-research" / "qa"
sys.path.insert(0, str(QA_DIR))

from artifact_hygiene_checker import check_hygiene  # noqa: E402


def assert_current_repo_clean() -> None:
    """Current tracked artifacts should be hygiene-clean."""
    results = check_hygiene(ROOT)
    failed = [item for item in results if not item.passed]
    assert not failed, "\n".join(f"{item.check}: {item.notes}" for item in failed[:20])


def assert_detects_path_and_cache_leaks() -> None:
    """Path leaks, cache files and .DS_Store should fail."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / "goodluck-stock-research" / "examples").mkdir(parents=True)
        (tmp_root / "goodluck-stock-research" / "examples" / "artifact.md").write_text("/Users/example/leak\n", encoding="utf-8")
        (tmp_root / ".DS_Store").write_text("cache", encoding="utf-8")
        (tmp_root / "module.pyc").write_text("cache", encoding="utf-8")
        results = check_hygiene(tmp_root)
        failed_names = {item.check for item in results if not item.passed}
        assert "no /Users path leaks" in failed_names
        assert "no .DS_Store tracked" in failed_names
        assert "no generated cache files tracked" in failed_names


def main() -> int:
    """Run tests."""
    assert_current_repo_clean()
    assert_detects_path_and_cache_leaks()
    print("PASS: artifact hygiene current repo and negative tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
