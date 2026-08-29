#!/usr/bin/env python3
"""Quarantined ratio-only runner policy wrapper."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from calculation_guardrails import evaluate_calculation


def can_run_ratio(input_csv: Path) -> dict[str, str]:
    """Check whether ratio-only run is allowed."""
    return evaluate_calculation("ratio", quarantined_csv_exists=input_csv.exists(), quarantined=True)


def render_policy(input_csv: Path) -> str:
    decision = can_run_ratio(input_csv)
    return f"""# Quarantined Ratio Runner Policy

- Decision: {decision['decision']}
- Reason: {decision['reason']}
- Input CSV: {input_csv}

## Boundary

- Ratio only.
- No DCF.
- No peer comps.
- No implied expectations.
- No target price, recommendation, position size or research status.
- Missing fields must be disclosed; no zero-fill.
"""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render quarantined ratio runner policy.")
    parser.add_argument("--input-csv", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    text = render_policy(args.input_csv)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print("PASS: quarantined ratio runner policy" if can_run_ratio(args.input_csv)["decision"] == "allow" else text)
    return 0 if can_run_ratio(args.input_csv)["decision"] == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
