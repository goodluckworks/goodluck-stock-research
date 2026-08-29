#!/usr/bin/env python3
"""Tests for real-company research workflow."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WF = ROOT / "goodluck-stock-research" / "production" / "workflows"
sys.path.insert(0, str(WF))

from real_company_research_workflow import run_research_workflow  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "MRVL"
        manifest = run_research_workflow("MRVL", out)
        assert manifest["status"] == "completed_internal_draft"
        assert (out / "research_report_draft.md").is_file()
        nvda = run_research_workflow("NVDA", Path(tmp) / "NVDA")
        assert nvda["status"] == "completed_internal_draft"
        avgo = run_research_workflow("AVGO", Path(tmp) / "AVGO")
        assert avgo["status"] == "blocked"
    print("PASS: real-company research workflow tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
