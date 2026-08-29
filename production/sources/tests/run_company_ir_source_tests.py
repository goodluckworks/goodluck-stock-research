#!/usr/bin/env python3
"""Tests for company IR source adapter."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "goodluck-stock-research" / "production" / "sources"
sys.path.insert(0, str(SRC))

from company_ir_source import fetch_company_ir  # noqa: E402


def main() -> int:
    result = fetch_company_ir("https://investor.example.com/news", lambda request, timeout: b"IR payload")
    assert result["manifest"]["reliability"] == "company_official"
    try:
        fetch_company_ir("http://investor.example.com/news", lambda request, timeout: b"bad")
        raise AssertionError("non-HTTPS should fail")
    except ValueError:
        pass
    try:
        fetch_company_ir("https://investor.example.com/news", lambda request, timeout: b"x" * 800_001)
        raise AssertionError("oversized response should fail")
    except ValueError:
        pass
    print("PASS: company IR source tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
