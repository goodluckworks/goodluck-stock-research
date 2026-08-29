#!/usr/bin/env python3
"""Tests for v2 production architecture and policy docs."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PROD = ROOT / "goodluck-stock-research" / "production"


def read(name: str) -> str:
    return (PROD / name).read_text(encoding="utf-8").lower()


def main() -> int:
    source = read("source_policy.md")
    approval = read("approval_policy.md")
    conclusion = read("research_conclusion_policy.md")
    assert "sec-only" in source
    assert "explicit user-agent" in source
    assert "maximum response size" in source
    for state in ("draft_unreviewed", "reviewed_internal", "approved_internal", "publishable_research_packet", "blocked"):
        assert state in approval
    for forbidden in ("trade instruction", "position sizing", "broker order", "guaranteed return"):
        assert forbidden in conclusion
    assert "constructive" in conclusion and "insufficient_evidence" in conclusion
    print("PASS: production policy tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
