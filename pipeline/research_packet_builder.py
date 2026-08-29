#!/usr/bin/env python3
"""Build sandbox/review-only research packets from pipeline runs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence


PIPELINE_DIR = Path(__file__).resolve().parent
SKILL_DIR = PIPELINE_DIR.parent
XBRL_DIR = SKILL_DIR / "xbrl"
sys.path.insert(0, str(XBRL_DIR))

from xbrl_common import ensure_distinct_paths, relative_or_absolute, utc_now, write_json  # noqa: E402


FORBIDDEN_TERMS = ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:")


def load_json(path: Path) -> dict[str, Any]:
    """Load JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def bullets(values: list[str]) -> str:
    """Render bullets."""
    return "\n".join(f"- `{value}`" for value in values) if values else "- None"


def blocked_rows(blocked: list[dict[str, str]]) -> str:
    """Render blocked rows."""
    if not blocked:
        return "| None | None |"
    return "\n".join(f"| {item['step']} | {item['reason']} |" for item in blocked)


def candidate_rows(candidates: list[dict[str, Any]]) -> str:
    """Render real-company candidate rows."""
    if not candidates:
        return "| None | None | None | None | None |"
    return "\n".join(
        "| {field} | {candidate_id} | {concept} | {confidence} | {warnings} |".format(
            field=item.get("normalized_field", "unknown"),
            candidate_id=item.get("candidate_id", "unknown"),
            concept=item.get("concept_qname", "unknown"),
            confidence=item.get("confidence", "unknown"),
            warnings=", ".join(item.get("warning_flags", [])) or "none",
        )
        for item in candidates
    )


def unresolved_rows(unresolved_items: list[dict[str, Any]]) -> str:
    """Render unresolved field explanation rows."""
    if not unresolved_items:
        return "| None | None | None | None |"
    return "\n".join(
        "| {field} | {reason_code} | {reason} | {action} |".format(
            field=item.get("normalized_field", "unknown"),
            reason_code=item.get("reason_code", "unknown"),
            reason=item.get("reason", "unknown"),
            action=item.get("suggested_action", "Manual review required."),
        )
        for item in unresolved_items
    )


def build_exmp_packet(run_dir: Path, manifest: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Build EXMP fictional sandbox packet."""
    csv_manifest_path = run_dir / "normalized_csv_sandbox" / "normalized_csv_manifest.json"
    dry_manifest_path = run_dir / "v02_ratio_dry_run" / "v02_dry_run_manifest.json"
    csv_manifest = load_json(csv_manifest_path)
    dry_manifest = load_json(dry_manifest_path)
    impact = csv_manifest.get("downstream_impact", {})
    unavailable_rows = "\n".join(
        f"| {item['ratio']} | {', '.join(item['missing_inputs'])} |"
        for item in impact.get("unavailable_ratios", [])
    ) or "| None | None |"
    body = f"""# Sandbox Research Packet: {manifest['ticker']}

## Boundary

- Sandbox / review-gated packet, not a final investment report.
- Fictional only.
- Not investment advice.
- Not production research.
- No target price.
- No buy/sell/hold instruction.
- No position size.
- No trading action.

## Pipeline Summary

- Pipeline run ID: `{manifest['pipeline_run_id']}`
- Mode: `{manifest['mode']}`
- Company: `{manifest['company']}`
- Ticker: `{manifest['ticker']}`
- Fixture data status: `{manifest['fixture_data_status']}`

## Approved / Populated Fields

{bullets(list(csv_manifest.get('populated_fields', [])))}

## Omitted / Unresolved / Blocked Fields

### Omitted

{bullets(list(csv_manifest.get('omitted_fields', [])))}

### Unresolved

{bullets(list(csv_manifest.get('unresolved_fields', [])))}

### Blocked

{bullets(list(csv_manifest.get('blocked_fields', [])))}

## Ratio Dry-Run Summary

- Dry-run ID: `{dry_manifest['dry_run_id']}`
- Script: `{dry_manifest['script']}`
- Run status: `{dry_manifest['run_status']}`
- Available ratios: `{len(impact.get('available_ratios', []))}`
- Unavailable ratios: `{len(impact.get('unavailable_ratios', []))}`

| Unavailable ratio | Missing inputs |
|---|---|
{unavailable_rows}

## Audit References

- Mapping version: `{manifest['audit_references'].get('mapping_version')}`
- Snapshot SHA-256: `{manifest['audit_references'].get('snapshot_sha256')}`
- Review batch: `{manifest['audit_references'].get('review_batch_id')}`
- Promotion ID: `{manifest['audit_references'].get('promotion_id')}`
- Normalized CSV manifest: `{manifest['audit_references'].get('normalized_csv_manifest')}`
- v0.2 dry-run manifest: `{manifest['audit_references'].get('v02_dry_run_manifest')}`

## Caveats

- Missing fields remain blank and are not filled with zero.
- Ratio output is a sandbox calculation check, not company fact.
"""
    packet_manifest = {
        "packet_schema_version": "v0.3.11",
        "packet_type": "fictional_sandbox",
        "pipeline_run_id": manifest["pipeline_run_id"],
        "ticker": manifest["ticker"],
        "mode": manifest["mode"],
        "source_pipeline_manifest": relative_or_absolute(run_dir / "pipeline_run_manifest.json"),
        "audit_references": manifest["audit_references"],
        "no_investment_conclusion": True,
        "created_at": utc_now(),
    }
    return body, packet_manifest


def build_review_only_packet(run_dir: Path, manifest: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Build real-company-shaped review-only packet."""
    quality = load_json(run_dir / "quality" / "review_quality_score.json")
    review = load_json(run_dir / "review" / "normalized_review_batch.json")
    candidate = load_json(run_dir / "candidate" / "extraction_candidates.json")
    unresolved_payload = load_json(run_dir / "candidate" / "unresolved_fields.json")
    unresolved = [
        item.get("normalized_field", "unknown")
        for item in review.get("records", [])
        if item.get("reviewer_decision") not in {"approve", "adjust"}
    ]
    candidate_fields = [item.get("normalized_field", "unknown") for item in candidate.get("candidates", [])]
    unresolved_items = unresolved_payload.get("unresolved_fields", [])
    quality_records = quality.get("records", [])
    quality_ready = quality.get("overall_status", quality.get("approval_readiness", "review_only"))
    body = f"""# Review-Only Research Packet: {manifest['ticker']}

## Boundary

- Review-only packet, not a final investment report.
- Draft / unapproved.
- Synthetic or excerpt fixture, not authoritative company data.
- Not investment advice.
- Not production research.
- No target price.
- No buy/sell/hold instruction.
- No position size.
- No trading action.

## Pipeline Summary

- Pipeline run ID: `{manifest['pipeline_run_id']}`
- Mode: `{manifest['mode']}`
- Company: `{manifest['company']}`
- Ticker: `{manifest['ticker']}`
- Fixture data status: `{manifest['fixture_data_status']}`

## Candidate Summary

- Candidate count: `{len(candidate.get('candidates', []))}`
- Candidate fields: `{', '.join(candidate_fields) if candidate_fields else 'none'}`
- Review batch: `{review.get('review_batch_id')}`
- Quality package: `{quality.get('quality_package_id')}`
- Quality score status: `{quality_ready}`
- Quality records: `{len(quality_records)}`
- Workbench reference: `{relative_or_absolute(run_dir / 'workbench' / 'review_workbench.md')}`
- Quality reference: `{relative_or_absolute(run_dir / 'quality' / 'review_quality_score.json')}`

## Candidate Fields

| Field | Candidate ID | Concept | Confidence | Warnings |
|---|---|---|---|---|
{candidate_rows(candidate.get('candidates', []))}

## Unresolved / Blocked Fields

{bullets(unresolved)}

## Unresolved Field Explanations

| Field | Reason code | Reason | Reviewer next check |
|---|---|---|---|
{unresolved_rows(unresolved_items)}

## Reviewer Evidence Checks

- Confirm source period, unit, scale, sign and context for every candidate.
- Reconcile candidate fields against the workbench and quality score before any approval decision.
- Resolve every unresolved field from the table above; do not infer or zero-fill.
- Document source evidence before any future quarantine gate.

## Blocked Steps

| Step | Reason |
|---|---|
{blocked_rows(manifest.get('blocked_steps', []))}

## Explicit Non-Outputs

- No approval.
- No promotion.
- No normalized CSV.
- No v0.2.x dry-run.
- No approved normalized input.
- Suitable for promotion: `No`.
- Reason: real-company review packet is synthetic/excerpt-only and lacks explicit controlled sandbox approval.

## Audit References

- Mapping version: `{manifest['audit_references'].get('mapping_version')}`
- Snapshot SHA-256: `{manifest['audit_references'].get('snapshot_sha256')}`
- Review batch: `{manifest['audit_references'].get('review_batch_id')}`
- Candidate package: `{relative_or_absolute(run_dir / 'candidate' / 'extraction_candidates.json')}`
- Unresolved fields: `{relative_or_absolute(run_dir / 'candidate' / 'unresolved_fields.json')}`
- Workbench: `{relative_or_absolute(run_dir / 'workbench' / 'review_workbench.md')}`
- Quality score: `{relative_or_absolute(run_dir / 'quality' / 'review_quality_score.json')}`
"""
    packet_manifest = {
        "packet_schema_version": "v0.3.11",
        "packet_type": "real_company_review_only",
        "pipeline_run_id": manifest["pipeline_run_id"],
        "ticker": manifest["ticker"],
        "mode": manifest["mode"],
        "source_pipeline_manifest": relative_or_absolute(run_dir / "pipeline_run_manifest.json"),
        "audit_references": manifest["audit_references"],
        "blocked_steps": manifest.get("blocked_steps", []),
        "candidate_fields": candidate_fields,
        "unresolved_fields": [item.get("normalized_field", "unknown") for item in unresolved_items],
        "workbench_reference": relative_or_absolute(run_dir / "workbench" / "review_workbench.md"),
        "quality_reference": relative_or_absolute(run_dir / "quality" / "review_quality_score.json"),
        "suitable_for_promotion": False,
        "no_investment_conclusion": True,
        "created_at": utc_now(),
    }
    return body, packet_manifest


def build_packet(run_dir: Path, output_md: Path, overwrite: bool = False) -> dict[str, Path]:
    """Build a research packet from a pipeline run directory."""
    run_dir = run_dir.expanduser().resolve()
    output_md = output_md.expanduser().resolve()
    ensure_distinct_paths(run_dir, output_md)
    if output_md.exists() and not overwrite:
        raise FileExistsError(f"Output packet already exists: {output_md}. Use --overwrite.")
    manifest = load_json(run_dir / "pipeline_run_manifest.json")
    if manifest["ticker"] == "EXMP":
        body, packet_manifest = build_exmp_packet(run_dir, manifest)
    else:
        body, packet_manifest = build_review_only_packet(run_dir, manifest)
    lowered = body.lower()
    for term in FORBIDDEN_TERMS:
        if term in lowered:
            raise ValueError(f"Packet contains forbidden conclusion term: {term}")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(body, encoding="utf-8")
    manifest_path = output_md.with_suffix(".manifest.json")
    write_json(manifest_path, packet_manifest)
    return {"packet_markdown": output_md, "packet_manifest": manifest_path}


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Build sandbox/review-only research packet.")
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--output-md", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = build_packet(args.run_dir, args.output_md, args.overwrite)
    except (FileNotFoundError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print("Wrote research packet:")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
