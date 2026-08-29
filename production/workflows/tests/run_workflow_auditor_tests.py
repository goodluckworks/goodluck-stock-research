#!/usr/bin/env python3
"""Tests for workflow auditor."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
WF = ROOT / "goodluck-stock-research" / "production" / "workflows"
sys.path.insert(0, str(WF))

from real_company_research_workflow import run_research_workflow  # noqa: E402
from workflow_auditor import audit_workflow  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "MRVL"
        run_research_workflow("MRVL", out)
        assert not audit_workflow(out)
        (out / "research_report_draft.md").write_text("buy now\n", encoding="utf-8")
        assert any("forbidden" in issue for issue in audit_workflow(out))
    print("PASS: workflow auditor tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
