#!/usr/bin/env python3
"""Build review-gated report packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Sequence

from report_policy import forbidden_hits, packet_type_for


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def review_manifest(repo_root: Path, ticker: str) -> dict[str, Any]:
    return load_json(repo_root / "goodluck-stock-research" / "examples" / "research_packets" / ticker / "review_only_packet.manifest.json")


def build_report(repo_root: Path, ticker: str) -> tuple[str, dict[str, Any]]:
    ticker = ticker.upper()
    packet_type = packet_type_for(ticker)
    manifest = {
        "report_manifest_schema_version": "v0.9.0",
        "ticker": ticker,
        "packet_type": packet_type,
        "no_investment_conclusion": True,
        "no_target_price": True,
        "no_position_size": True,
    }
    if ticker == "EXMP":
        text = """# EXMP Fictional Review-Gated Report Packet

## Boundary

Fictional sandbox only. Not investment advice. Not for trading.

## Evidence Summary

- Uses fictional approved fields.
- Includes ratio dry-run summary by reference.
- Discloses partial-field caveats and sandbox audit references.

## Audit References

- Pipeline dashboard.
- Sandbox packet manifest.
- v0.2.x ratio dry-run manifest.
"""
        manifest["source_type"] = "fictional_sandbox"
    elif ticker == "MRVL":
        q = load_json(repo_root / "goodluck-stock-research" / "examples" / "real_company_quarantine" / "MRVL" / "quarantine_manifest.json")
        text = f"""# MRVL Quarantined Review-Gated Report Packet

## Boundary

Quarantined real-company sandbox only. Not production data. Not investment data. Not for trading. Manual review required.

## Quarantined Field Status

- Approved quarantined fields: {', '.join(q.get('approved_fields', []))}
- Quarantined CSV: {q.get('outputs', {}).get('quarantined_csv')}
- Ratio-only dry-run: {q.get('outputs', {}).get('ratio_output')}

## Evidence Reconciliation

- Review batch: {q.get('review_batch')}
- Quality score: {q.get('quality_score')}
- Candidate package: {q.get('candidate_package')}
- Quarantine manifest: goodluck-stock-research/examples/real_company_quarantine/MRVL/quarantine_manifest.json

## Missing Evidence

- Production approval is absent.
- Public release approval is absent.
- Full research conclusion is intentionally omitted.
"""
        manifest["quarantine_manifest"] = "goodluck-stock-research/examples/real_company_quarantine/MRVL/quarantine_manifest.json"
    else:
        m = review_manifest(repo_root, ticker)
        text = f"""# {ticker} Review-Only Report Packet

## Boundary

Review-only packet. Draft candidates are not facts. Not investment advice. Not for trading. No CSV and no dry-run.

## Candidate Fields

{', '.join(m.get('candidate_fields', []))}

## Unresolved Fields

{', '.join(m.get('unresolved_fields', []))}

## Evidence Gaps

- Promotion suitability: {m.get('suitable_for_promotion')}
- Workbench: {m.get('workbench_reference')}
- Quality: {m.get('quality_reference')}
- Source manifest: {m.get('source_pipeline_manifest')}
"""
        manifest["source_review_packet"] = f"goodluck-stock-research/examples/research_packets/{ticker}/review_only_packet.manifest.json"
    hits = forbidden_hits(text)
    if hits:
        raise ValueError(f"report contains forbidden conclusion terms: {hits}")
    return text, manifest


def write_report(repo_root: Path, ticker: str, output_dir: Path) -> None:
    text, manifest = build_report(repo_root, ticker)
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "report_packet.md").write_text(text, encoding="utf-8")
    (output_dir / "report_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build review-gated report packet.")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    write_report(args.repo_root, args.ticker, args.output_dir)
    print(f"PASS: built report packet for {args.ticker.upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
