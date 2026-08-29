#!/usr/bin/env python3
"""Tests for production CLI."""

from __future__ import annotations

import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "production"))

import cli  # noqa: E402


def capture(argv: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = cli.main(argv)
    return code, buffer.getvalue()


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "MRVL"
        code, text = capture(["research", "--ticker", "MRVL", "--mode", "fixture", "--output-dir", str(out)])
        assert code == 0
        assert "report path:" in text and "audit path:" in text
        assert "no broker action" in text
        assert "position sizing" in text
        code, text = capture(["validate", "--run-dir", str(out)])
        assert code == 0 and "validation status: pass" in text
    print("PASS: CLI tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
