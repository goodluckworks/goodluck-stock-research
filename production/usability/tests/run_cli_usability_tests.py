#!/usr/bin/env python3
"""Tests for CLI usability audit."""

from __future__ import annotations

import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PROD = ROOT / "goodluck-stock-research" / "production"
USABILITY = PROD / "usability"
sys.path.insert(0, str(PROD))
sys.path.insert(0, str(USABILITY))

import cli  # noqa: E402
from cli_usability_audit import audit_command_output, audit_error_message, audit_help_text  # noqa: E402


def capture(argv: list[str]) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        try:
            cli.main(argv)
        except SystemExit as exc:
            if exc.code not in {0, None}:
                raise
    return buffer.getvalue()


def main() -> int:
    help_text = capture(["--help"]) + "\n" + capture(["research", "--help"])
    assert not audit_help_text(help_text), audit_help_text(help_text)
    with tempfile.TemporaryDirectory() as tmp:
        output = capture(["research", "--ticker", "MRVL", "--mode", "fixture", "--output-dir", str(Path(tmp) / "MRVL")])
        assert not audit_command_output(output), audit_command_output(output)
        live = capture(["research", "--ticker", "MRVL", "--mode", "live", "--sec-only", "--output-dir", str(Path(tmp) / "LIVE")])
        assert not audit_error_message(live), audit_error_message(live)
    print("PASS: CLI usability tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
