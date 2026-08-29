#!/usr/bin/env python3
"""Tests for report builder."""

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "reporting"))

import research_report_builder


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        for ticker in ("EXMP", "MRVL", "NVDA", "AVGO"):
            research_report_builder.write_report(ROOT, ticker, out / ticker)
            text = (out / ticker / "report_packet.md").read_text(encoding="utf-8")
            assert "target price:" not in text.lower()
            assert "position size:" not in text.lower()
            assert "research status:" not in text.lower()
    print("PASS: research report builder tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
