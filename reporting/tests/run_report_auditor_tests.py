#!/usr/bin/env python3
"""Tests for report auditor."""

from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "reporting"))

import report_auditor
import research_report_builder


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "MRVL"
        research_report_builder.write_report(ROOT, "MRVL", out)
        assert not report_auditor.audit_report(out)
        poisoned = out / "report_packet.md"
        poisoned.write_text(poisoned.read_text(encoding="utf-8") + "\ntarget price: bad\n", encoding="utf-8")
        assert report_auditor.audit_report(out)
    print("PASS: report auditor tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
