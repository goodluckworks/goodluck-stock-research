#!/usr/bin/env python3
"""Score local XBRL candidate review readiness as reviewer aid only."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from xbrl_common import ensure_distinct_paths, load_json, prepare_output_dir, relative_or_absolute, utc_now, write_json


OUTPUTS = ("review_quality_score.json", "review_quality_report.md")


def score_candidate(candidate: dict[str, Any], provenance_by_candidate: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Return advisory score for one candidate."""
    candidate_id = str(candidate.get("candidate_id", "missing"))
    relationship = candidate.get("taxonomy_relationship", {})
    warnings = list(candidate.get("warning_flags", []))
    competing = list(candidate.get("competing_candidate_ids", []))
    blocking: list[str] = []

    completeness_score = 100.0
    required = (
        "candidate_id",
        "normalized_field",
        "extracted_value",
        "unit",
        "period",
        "concept_qname",
        "context_id",
        "source_locator",
        "transformation",
        "confidence",
    )
    missing = [field for field in required if field not in candidate or candidate.get(field) in {"", None}]
    completeness_score -= 10 * len(missing)
    if missing:
        blocking.append("missing_candidate_fields")

    provenance_score = 100.0 if candidate_id in provenance_by_candidate else 40.0
    if candidate_id not in provenance_by_candidate:
        blocking.append("missing_provenance")

    relationship_status = relationship.get("relationship_review_status", "missing")
    relationship_confidence = relationship.get("relationship_confidence", "missing")
    if relationship_status in {"reviewed", "not_applicable"} and relationship_confidence in {"high", "medium"}:
        relationship_score = 100.0 if relationship_confidence == "high" else 85.0
    elif relationship_confidence == "low":
        relationship_score = 55.0
        blocking.append("weak_relationship_evidence")
    else:
        relationship_score = 35.0
        blocking.append("missing_relationship_evidence")

    ambiguity_score = 100.0
    if competing:
        ambiguity_score -= 35
        blocking.append("competing_candidates")
    if candidate.get("confidence") == "low":
        ambiguity_score -= 50
        blocking.append("low_confidence")
    if any("dimension" in flag for flag in warnings):
        ambiguity_score -= 25
        blocking.append("dimension_warning")
    synthetic_real_fixture = any("synthetic_real_company_fixture_unverified" == flag for flag in warnings)
    if synthetic_real_fixture:
        ambiguity_score -= 15
    if any("material_change_threshold_review_required" == flag for flag in warnings):
        ambiguity_score -= 10

    scores = [completeness_score, provenance_score, relationship_score, ambiguity_score]
    ready = "ready"
    if blocking:
        ready = "not_ready"
    elif synthetic_real_fixture:
        ready = "needs_review"
    elif min(scores) < 80:
        ready = "needs_review"
    return {
        "candidate_id": candidate_id,
        "normalized_field": candidate.get("normalized_field", "missing"),
        "completeness_score": max(0.0, completeness_score),
        "provenance_score": max(0.0, provenance_score),
        "relationship_score": max(0.0, relationship_score),
        "ambiguity_score": max(0.0, ambiguity_score),
        "approval_readiness": ready,
        "blocking_issues": sorted(set(blocking)),
        "warning_flags": warnings,
        "relationship_confidence": relationship_confidence,
        "relationship_review_status": relationship_status,
    }


def run_scorer(
    candidate_file: Path,
    manifest_file: Path,
    provenance_file: Path,
    output_dir: Path,
    overwrite: bool = False,
) -> dict[str, Path]:
    """Run review quality scoring."""
    ensure_distinct_paths(candidate_file, manifest_file, provenance_file, output_dir)
    candidate_doc = load_json(candidate_file)
    manifest = load_json(manifest_file)
    provenance_doc = load_json(provenance_file)
    candidates = candidate_doc.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("Candidate file must contain non-empty candidates array.")
    provenance_by_candidate = {
        item.get("candidate_id"): item
        for item in provenance_doc.get("records", [])
        if isinstance(item, dict)
    }
    records = [score_candidate(candidate, provenance_by_candidate) for candidate in candidates]
    prepare_output_dir(output_dir, overwrite)
    paths = {name: output_dir / name for name in OUTPUTS}
    package = {
        "quality_schema_version": "v0.3.7",
        "quality_package_id": f"review-quality-{str(manifest['ticker']).lower()}-{manifest['snapshot_sha256'][:12]}",
        "extraction_run_id": manifest["run_id"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "mapping_version": manifest["mapping_version"],
        "company": manifest["company"],
        "ticker": manifest["ticker"],
        "fictional_company": manifest["ticker"] == "EXMP",
        "created_at": utc_now(),
        "candidate_file": relative_or_absolute(candidate_file),
        "provenance_file": relative_or_absolute(provenance_file),
        "records": records,
        "boundary": [
            "Scores are advisory only.",
            "Scores do not approve fields.",
            "Real-company-shaped fixtures remain unapproved and unpromoted.",
        ],
    }
    rows = "\n".join(
        f"| `{r['candidate_id']}` | `{r['normalized_field']}` | {r['completeness_score']:.0f} | {r['provenance_score']:.0f} | {r['relationship_score']:.0f} | {r['ambiguity_score']:.0f} | `{r['approval_readiness']}` | `{', '.join(r['blocking_issues']) or 'none'}` |"
        for r in records
    )
    report = f"""# XBRL Review Quality Report

## Summary

- Company: `{manifest['company']}`
- Ticker: `{manifest['ticker']}`
- Extraction run ID: `{manifest['run_id']}`
- Mapping version: `{manifest['mapping_version']}`
- Generated at: `{utc_now()}`

## Scores

| Candidate | Field | Completeness | Provenance | Relationship | Ambiguity | Readiness | Blocking Issues |
|---|---|---:|---:|---:|---:|---|---|
{rows}

## Boundary

- Scores are reviewer aids only.
- Scores cannot approve fields or create normalized output.
- No investment conclusion or v0.2.x populated CSV is generated.
"""
    write_json(paths["review_quality_score.json"], package)
    paths["review_quality_report.md"].write_text(report, encoding="utf-8")
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Score local XBRL review quality.")
    parser.add_argument("--candidate-file", required=True, type=Path)
    parser.add_argument("--manifest-file", required=True, type=Path)
    parser.add_argument("--provenance-file", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run_scorer(args.candidate_file, args.manifest_file, args.provenance_file, args.output_dir, args.overwrite)
    except (FileNotFoundError, FileExistsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote review quality package: {args.output_dir}")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
