#!/usr/bin/env python3
"""Tests for final red-team audit."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "goodluck-stock-research" / "production" / "audit"
sys.path.insert(0, str(AUDIT))

from final_red_team import audit_artifact_paths, audit_report_text  # noqa: E402


def main() -> int:
    assert audit_report_text("buy now\n")
    assert audit_report_text("Low confidence conclusion.\nCaveats: none\n")
    assert not audit_report_text("Research view: Neutral\nCaveats: source limited\n")
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "leak.txt").write_text("api_key = bad\n", encoding="utf-8")
        (root / "path.txt").write_text("/Users/example/private\n", encoding="utf-8")
        issues = audit_artifact_paths(root)
        assert any("secret leakage" in issue for issue in issues)
        assert any("local path leakage" in issue for issue in issues)
    print("PASS: final red-team tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
