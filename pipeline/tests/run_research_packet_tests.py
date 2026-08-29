#!/usr/bin/env python3
"""Research packet builder tests."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


PIPELINE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PIPELINE_DIR))

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


def assert_packet(path: Path, expected: list[str], forbidden_dry_run: bool = False) -> None:
    """Assert packet content."""
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    for item in expected:
        assert item in text, item
    for term in ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:"):
        assert term not in lowered
    if forbidden_dry_run:
        assert "Ratio Dry-Run Summary" not in text
        assert "No v0.2.x dry-run" in text


def main() -> int:
    """Run packet tests."""
    with tempfile.TemporaryDirectory(prefix="research-packet-tests-") as temp_name:
        temp = Path(temp_name)
        for mode, dirname in (
            ("fictional_sandbox_full", "full"),
            ("fictional_sandbox_partial", "partial"),
        ):
            run_dir = temp / "EXMP" / dirname
            run_pipeline(mode, "EXMP", COMPANIES["EXMP"], run_dir)
            paths = build_packet(run_dir, temp / "packets" / "EXMP" / f"{dirname}_packet.md")
            assert paths["packet_markdown"].is_file()
            assert paths["packet_manifest"].is_file()
            manifest = read(paths["packet_manifest"])
            assert manifest["packet_type"] == "fictional_sandbox"
            assert manifest["no_investment_conclusion"] is True
            assert_packet(
                paths["packet_markdown"],
                ["Sandbox Research Packet", "Approved / Populated Fields", "Ratio Dry-Run Summary", "Audit References"],
            )

        for ticker in ("MRVL", "NVDA", "AVGO"):
            run_dir = temp / ticker / "review_only"
            run_pipeline("real_company_review_only", ticker, COMPANIES[ticker], run_dir)
            paths = build_packet(run_dir, temp / "packets" / ticker / "review_only_packet.md")
            manifest = read(paths["packet_manifest"])
            assert manifest["packet_type"] == "real_company_review_only"
            assert manifest["no_investment_conclusion"] is True
            assert_packet(
                paths["packet_markdown"],
                ["Review-Only Research Packet", "No promotion.", "No normalized CSV.", "No v0.2.x dry-run."],
                forbidden_dry_run=True,
            )

    print("PASS: EXMP sandbox packets, MRVL/NVDA/AVGO review-only packets, manifests and conclusion-field checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
