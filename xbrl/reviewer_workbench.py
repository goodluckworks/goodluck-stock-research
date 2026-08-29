#!/usr/bin/env python3
"""Generate local reviewer workbench Markdown and decision templates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import ensure_distinct_paths, load_json, relative_or_absolute, utc_now, write_json


def candidate_rows(candidates: list[dict[str, Any]], provenance_by_candidate: dict[str, dict[str, Any]]) -> str:
    """Render candidate sections."""
    sections: list[str] = []
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        provenance = provenance_by_candidate.get(candidate_id, {})
        relationship = candidate.get("taxonomy_relationship", {})
        checklist = candidate.get("review_checklist", {})
        warnings = list(candidate.get("warning_flags", []))
        warning_lines = "\n".join(
            f"- Severity `review_required` / flag `{warning}`: inspect source context, relationship evidence and competing candidates before approval."
            for warning in warnings
        ) or "- None"
        competing = candidate.get("competing_candidate_ids", [])
        competing_text = ", ".join(f"`{item}`" for item in competing) if competing else "`none`"
        checklist_rows = "\n".join(
            f"| {field.replace('_', ' ')} | `{checklist.get(field, False)}` | Review and mark true only with evidence. |"
            for field in (
                "period_checked",
                "unit_checked",
                "context_checked",
                "dimensions_checked",
                "sign_checked",
                "scale_checked",
                "relationship_checked",
                "competing_candidates_checked",
                "prior_period_checked",
                "materiality_checked",
                "reviewer_notes_present",
            )
        )
        sections.append(
            f"""### {candidate['normalized_field']} / `{candidate_id}`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `{candidate_id}` |
| normalized_field | `{candidate['normalized_field']}` |
| extracted_value | `{candidate['extracted_value']}` |
| source_value | `{candidate['source_value']}` |
| unit | `{candidate['unit']}` |
| period | `{candidate['period']}` |
| concept_qname | `{candidate['concept_qname']}` |
| concept_label | `{relationship.get('concept_label', 'missing')}` |
| concept_type | `{relationship.get('concept_type', 'missing')}` |
| context_id | `{candidate['context_id']}` |
| period_type | `{candidate['period_type']}` |
| dimensions | `{candidate.get('dimensions', [])}` |
| source_locator | `{candidate['source_locator']}` |
| transformation | `{candidate['transformation']}` |
| confidence | `{candidate['confidence']}` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `{relationship.get('relationship_confidence', 'missing')}` |
| warning_flags | `{candidate.get('warning_flags', [])}` |
| competing_candidate_ids | {competing_text} |
| review_status | `{candidate['review_status']}` |
| provenance link | `{provenance.get('record_id', 'missing')}` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `{relationship.get('taxonomy_namespace', 'missing')}` |
| taxonomy_version | `{relationship.get('taxonomy_version', 'missing')}` |
| closest_standard_concept | `{relationship.get('closest_standard_concept', 'missing')}` |
| presentation_parent | `{relationship.get('presentation_parent', 'missing')}` |
| presentation_children | `{relationship.get('presentation_children', [])}` |
| calculation_parent | `{relationship.get('calculation_parent', 'missing')}` |
| calculation_children | `{relationship.get('calculation_children', [])}` |
| anchor_concept | `{relationship.get('anchor_concept', 'missing')}` |
| relationship_basis | `{relationship.get('relationship_basis', 'missing')}` |
| relationship_evidence_notes | `{relationship.get('relationship_evidence_notes', 'missing')}` |
| relationship_review_status | `{relationship.get('relationship_review_status', 'missing')}` |

#### Warning Flags by Severity

{warning_lines}

#### Competing Candidates Comparison

- Competing candidate IDs: {competing_text}
- If competing candidates exist, compare concept label, context, period, unit, dimensions, source locator and relationship evidence before approval.
- If no competing candidates exist, still confirm the field is not duplicated in unresolved or rejected facts.

#### Review Checklist

| Checklist Item | Current Value | Reviewer Instruction |
|---|---:|---|
{checklist_rows}

#### Reviewer Questions

- Why might this candidate be suspicious?
- Why might this candidate be acceptable?
- Which source evidence, statement line, note, context, unit and relationship supports approval?
- Are there competing candidates or material prior-period changes?

#### Required Evidence

- Source locator and source fact IDs.
- Period, unit, context and dimension evidence.
- Relationship metadata and anchor / closest standard concept evidence.
- Transformation and sign/scale evidence.
- Reviewer notes explaining any approval or adjustment.
"""
        )
    return "\n".join(sections)


def exmp_decision(candidate: dict[str, Any]) -> tuple[str, Any, str, str, str]:
    """Return deterministic fictional EXMP decisions."""
    field = candidate["normalized_field"]
    if field == "capital_expenditure":
        return (
            "adjust",
            float(candidate["extracted_value"]) + 2,
            candidate["unit"],
            "Fictional adjustment example for review workflow; preserves extracted value in source fields.",
            "2026-06-29T01:14:00Z",
        )
    if field in {"net_income"}:
        return ("reject", "not_approved", "not_approved", "Fictional rejection example.", "not_approved")
    if field in {"total_debt"}:
        return ("unresolved", "not_approved", "not_approved", "Fictional unresolved debt review example.", "not_approved")
    if field in {"diluted_shares"}:
        return ("needs_more_evidence", "not_approved", "not_approved", "Fictional needs-more-evidence share basis example.", "not_approved")
    return (
        "approve",
        candidate["extracted_value"],
        candidate["unit"],
        "Fictional approval example for offline EXMP fixture only.",
        "2026-06-29T01:10:00Z",
    )


def decision_template_records(
    manifest: dict[str, Any], candidates: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Create decision template records."""
    records: list[dict[str, Any]] = []
    ticker = str(manifest["ticker"]).upper()
    for index, candidate in enumerate(candidates, start=1):
        if ticker == "EXMP":
            decision, approved_value, approved_unit, notes, approval_timestamp = exmp_decision(candidate)
        else:
            decision = "unresolved"
            approved_value = "not_approved"
            approved_unit = "not_approved"
            notes = "Synthetic real-company-shaped fixture remains unapproved."
            approval_timestamp = "not_approved"
        records.append(
            {
                "decision_record_id": f"decision-{ticker.lower()}-{index:03d}",
                "candidate_id": candidate["candidate_id"],
                "reviewer_decision": decision,
                "reviewer_id": "fixture-reviewer",
                "reviewer_notes": notes,
                "approved_value": approved_value,
                "approved_unit": approved_unit,
                "approval_timestamp": approval_timestamp,
                "prior_review_record_id": "not_applicable",
                "review_checklist": {
                    "checklist_schema_version": "v0.3.7",
                    "candidate_id": candidate["candidate_id"],
                    "period_checked": decision in {"approve", "adjust"},
                    "unit_checked": decision in {"approve", "adjust"},
                    "context_checked": decision in {"approve", "adjust"},
                    "dimensions_checked": decision in {"approve", "adjust"},
                    "sign_checked": decision in {"approve", "adjust"},
                    "scale_checked": decision in {"approve", "adjust"},
                    "relationship_checked": decision in {"approve", "adjust"},
                    "competing_candidates_checked": decision in {"approve", "adjust"},
                    "prior_period_checked": decision in {"approve", "adjust"},
                    "materiality_checked": decision in {"approve", "adjust"},
                    "reviewer_notes_present": bool(notes and notes != "not_approved"),
                },
            }
        )
    return records


def run_workbench(
    candidate_file: Path,
    manifest_file: Path,
    provenance_file: Path,
    output_workbench: Path,
    output_decision_template: Path,
) -> None:
    """Generate Markdown workbench and decision template."""
    ensure_distinct_paths(
        candidate_file, manifest_file, provenance_file, output_workbench, output_decision_template
    )
    candidate_doc = load_json(candidate_file)
    manifest = load_json(manifest_file)
    provenance_doc = load_json(provenance_file)
    candidates = candidate_doc.get("candidates", [])
    provenance_by_candidate = {
        item.get("candidate_id"): item
        for item in provenance_doc.get("records", [])
        if isinstance(item, dict)
    }
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Candidate file must contain non-empty candidates array.")
    missing_provenance = [
        item["candidate_id"] for item in candidates if item["candidate_id"] not in provenance_by_candidate
    ]
    if missing_provenance:
        raise ValueError(f"Candidate provenance missing: {missing_provenance}")
    output_workbench.parent.mkdir(parents=True, exist_ok=True)
    output_decision_template.parent.mkdir(parents=True, exist_ok=True)

    input_file = str(manifest.get("input_file", ""))
    excerpt_warning = (
        "- Real filing excerpt drill: excerpt only, not a complete filing, not authoritative financial data, no approved values.\n"
        if "real_excerpt_drills" in input_file
        else ""
    )
    workbench = f"""# XBRL Reviewer Workbench

> NOT APPROVED. This workbench is a human review aid, not a normalized financial output.

## Summary

- Company: `{manifest['company']}`
- Ticker: `{manifest['ticker']}`
- Fixture data status: `{manifest['fixture_data_status']}`
- Mapping version: `{manifest['mapping_version']}`
- Extraction run ID: `{manifest['run_id']}`
- Snapshot SHA-256: `{manifest['snapshot_sha256']}`
- Generated at: `{utc_now()}`

## Executive Review Summary

- Candidate count: `{len(candidates)}`
- Workbench status: `draft_review_workspace`
- Approval readiness: `requires reviewer checklist, quality score and normalized decision collection`
- Real-company boundary: `{'fictional EXMP fixture' if manifest['ticker'] == 'EXMP' else 'synthetic/unverified real-company-shaped fixture'}`

## Approval Readiness

- Current state: `not_approved`
- Required gates: `completed review checklist`, `ready review quality score`, `normalized review decision`, `approved mapping relationship review`, `package audit`
- This workbench cannot approve fields by itself.

## Blocking Issues

- Candidate warning flags must be resolved or documented.
- Missing provenance, missing taxonomy relationship evidence, weak relationship evidence, low confidence or unresolved competing candidates block approve / adjust decisions.
- Real-company excerpt drills remain draft-only and cannot be promoted.

## Boundary

- This is not approval.
- This is not investment advice.
- Real-company-shaped fixtures are synthetic/unverified unless explicitly stated.
{excerpt_warning}- Complete filing storage and production parsing are out of scope.
- Reviewer decision file is separate.
- Review quality scores are advisory and cannot approve fields.
- No target price, recommendation, buy/sell/hold, position size or research status is produced.

## Candidate Table by Normalized Field

| Field | Candidate ID | Concept | Confidence | Relationship Confidence | Warnings |
|---|---|---|---|---|---|
{chr(10).join(f"| `{c['normalized_field']}` | `{c['candidate_id']}` | `{c['concept_qname']}` | `{c['confidence']}` | `{c.get('taxonomy_relationship', {}).get('relationship_confidence', 'missing')}` | `{', '.join(c.get('warning_flags', [])) or 'none'}` |" for c in candidates)}

## Candidates

{candidate_rows(candidates, provenance_by_candidate)}
"""
    template = {
        "decision_template_schema_version": "v0.3.7",
        "decision_source": "reviewer_workbench_template",
        "company": manifest["company"],
        "ticker": manifest["ticker"],
        "fictional_company": manifest["ticker"] == "EXMP",
        "fixture_data_status": manifest["fixture_data_status"],
        "extraction_run_id": manifest["run_id"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "mapping_version": manifest["mapping_version"],
        "created_at": utc_now(),
        "records": decision_template_records(manifest, candidates),
    }
    output_workbench.write_text(workbench, encoding="utf-8")
    write_json(output_decision_template, template)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Generate local XBRL reviewer workbench.")
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--manifest-file", required=True, type=Path)
    parser.add_argument("--provenance-file", required=True, type=Path)
    parser.add_argument("--output-workbench", required=True, type=Path)
    parser.add_argument("--output-decision-template", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        run_workbench(
            args.candidate_file,
            args.manifest_file,
            args.provenance_file,
            args.output_workbench,
            args.output_decision_template,
        )
    except (FileNotFoundError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote reviewer workbench: {args.output_workbench}")
    print(f"Wrote decision template: {args.output_decision_template}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
