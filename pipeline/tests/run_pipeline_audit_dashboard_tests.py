#!/usr/bin/env python3
"""Pipeline audit dashboard tests."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR))

from pipeline_audit_dashboard import build_dashboard  # noqa: E402
from pipeline_orchestrator import run_pipeline  # noqa: E402
from research_packet_builder import build_packet  # noqa: E402


COMPANIES = {
    "EXMP": "Example Semiconductor Corp.",
    "MRVL": "Marvell Technology, Inc.",
    "NVDA": "NVIDIA Corporation",
    "AVGO": "Broadcom Inc.",
}


def read(path: Path) -> dict[str, object]:
    """Read JSON."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def main() -> int:
    """Run dashboard tests."""
    with tempfile.TemporaryDirectory(prefix="pipeline-dashboard-tests-") as temp_name:
        temp = Path(temp_name)
        pipeline_root = temp / "pipeline_runs"
        packet_root = temp / "research_packets"
        for mode, dirname, packet_name in (
            ("fictional_sandbox_full", "full", "full_sandbox_packet.md"),
            ("fictional_sandbox_partial", "partial", "partial_sandbox_packet.md"),
        ):
            run_dir = pipeline_root / "EXMP" / dirname
            run_pipeline(mode, "EXMP", COMPANIES["EXMP"], run_dir)
            build_packet(run_dir, packet_root / "EXMP" / packet_name)
        for ticker in ("MRVL", "NVDA", "AVGO"):
            run_dir = pipeline_root / ticker / "review_only"
            run_pipeline("real_company_review_only", ticker, COMPANIES[ticker], run_dir)
            build_packet(run_dir, packet_root / ticker / "review_only_packet.md")
        paths = build_dashboard(pipeline_root, packet_root, temp / "dashboard")
        assert all(path.is_file() for path in paths.values())
        summary = read(paths["summary"])
        runs = summary["runs"]
        assert len(runs) == 5
        assert {row["ticker"] for row in runs} == {"EXMP", "MRVL", "NVDA", "AVGO"}
        matrix = summary["blocked_real_company_matrix"]
        assert len(matrix) == 9
        assert all(row["result"] == "pass" for row in matrix)
        for ticker in ("MRVL", "NVDA", "AVGO"):
            run_dir = pipeline_root / ticker / "review_only"
            assert not (run_dir / "promotion").exists()
            assert not (run_dir / "normalized_csv_sandbox").exists()
            assert not (run_dir / "v02_ratio_dry_run").exists()
        text = paths["dashboard"].read_text(encoding="utf-8").lower()
        for term in ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:"):
            assert term not in text

    print("PASS: dashboard generation, expected runs, blocked matrix, no real-company outputs and conclusion-field scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
