#!/usr/bin/env python3
"""Tests for offline packet QA."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
QA_DIR = ROOT / "goodluck-stock-research" / "qa"
sys.path.insert(0, str(QA_DIR))

from offline_packet_qa import run_qa  # noqa: E402


def assert_passes_current_repo() -> None:
    """Current tracked v0.4 artifacts should pass packet QA."""
    results = run_qa(ROOT)
    failed = [item for item in results if not item.passed]
    assert not failed, "\n".join(f"{item.check}: {item.notes}" for item in failed[:20])


def assert_detects_missing_manifest_field() -> None:
    """A tampered copied repo fragment should fail on missing manifest fields."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        minimal = tmp_root / "goodluck-stock-research" / "examples" / "pipeline_runs" / "MRVL" / "review_only"
        minimal.mkdir(parents=True)
        (minimal / "pipeline_run_manifest.json").write_text('{"ticker":"MRVL","mode":"real_company_review_only"}\n', encoding="utf-8")
        packet = tmp_root / "goodluck-stock-research" / "examples" / "research_packets" / "MRVL"
        packet.mkdir(parents=True)
        (packet / "review_only_packet.md").write_text("# Review-Only Research Packet: MRVL\n\nDraft / unapproved\nNo promotion.\nNo normalized CSV.\nNo v0.2.x dry-run.\n", encoding="utf-8")
        (packet / "review_only_packet.manifest.json").write_text('{"ticker":"MRVL"}\n', encoding="utf-8")
        dash = tmp_root / "goodluck-stock-research" / "examples" / "pipeline_audit_dashboard"
        dash.mkdir(parents=True)
        (dash / "pipeline_audit_summary.json").write_text('{"runs":[],"blocked_real_company_matrix":[]}\n', encoding="utf-8")
        (dash / "pipeline_audit_dashboard.md").write_text("# Dashboard\n", encoding="utf-8")
        (dash / "blocked_real_company_matrix.md").write_text("# Matrix\n", encoding="utf-8")
        results = run_qa(tmp_root)
        assert any(not item.passed and "complete" in item.check for item in results)


def main() -> int:
    """Run tests."""
    assert_passes_current_repo()
    assert_detects_missing_manifest_field()
    print("PASS: offline packet QA current repo and negative manifest tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
