#!/usr/bin/env python3
"""Audit review-gated report packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from report_policy import forbidden_hits


def audit_report(packet_dir: Path) -> list[str]:
    issues: list[str] = []
    report = packet_dir / "report_packet.md"
    manifest = packet_dir / "report_manifest.json"
    if not report.exists():
        issues.append("missing report_packet.md")
        return issues
    text = report.read_text(encoding="utf-8")
    hits = forbidden_hits(text)
    if hits:
        issues.append("forbidden terms: " + ", ".join(hits))
    if "Not investment" not in text and "Not for trading" not in text:
        issues.append("missing no-investment/no-trading boundary")
    if not manifest.exists():
        issues.append("missing report_manifest.json")
    else:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("no_investment_conclusion") is not True:
            issues.append("manifest missing no_investment_conclusion")
    return issues


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit report packet.")
    parser.add_argument("packet_dir", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    issues = audit_report(args.packet_dir)
    if issues:
        print("\n".join(issues))
        return 1
    print("PASS: report packet audit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
