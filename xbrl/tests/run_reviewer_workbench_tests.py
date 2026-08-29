#!/usr/bin/env python3
"""Reviewer workbench generation tests."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
ROOT = XBRL_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from reviewer_workbench import run_workbench  # noqa: E402


EXAMPLES = ROOT / "examples" / "xbrl_extraction_runs"
TICKERS = ("EXMP", "MRVL", "NVDA", "AVGO")
REQUIRED_TEXT = (
    "company",
    "ticker",
    "fixture data status",
    "mapping version",
    "extraction run id",
    "snapshot sha-256",
    "candidate_id",
    "normalized_field",
    "extracted_value",
    "source_value",
    "unit",
    "period",
    "concept_qname",
    "context_id",
    "period_type",
    "dimensions",
    "source_locator",
    "transformation",
    "confidence",
    "confidence explanation",
    "relationship metadata",
    "taxonomy_namespace",
    "closest_standard_concept",
    "anchor_concept",
    "relationship_evidence_notes",
    "approval readiness",
    "blocking issues",
    "warning flags by severity",
    "competing candidates comparison",
    "review checklist",
    "reviewer questions",
    "required evidence",
    "warning_flags",
    "competing_candidate_ids",
    "review_status",
    "provenance link",
    "this is not approval",
    "this is not investment advice",
)


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def main() -> int:
    """Run reviewer workbench tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-workbench-tests-") as temp_name:
        temp = Path(temp_name)
        for ticker in TICKERS:
            source = EXAMPLES / ticker
            out = temp / ticker
            run_workbench(
                source / "extraction_candidates.json",
                source / "extraction_run_manifest.json",
                source / "field_provenance.json",
                out / "review_workbench.md",
                out / "review_decision_template.json",
            )
            workbench = (out / "review_workbench.md").read_text(encoding="utf-8").lower()
            for text in REQUIRED_TEXT:
                assert text in workbench, (ticker, text)
            for forbidden in ("target price:", "position size:", "research status:", "buy:", "sell:", "hold:"):
                assert forbidden not in workbench
            template = read(out / "review_decision_template.json")
            candidates = read(source / "extraction_candidates.json")
            assert template["decision_source"] == "reviewer_workbench_template"
            assert template["decision_template_schema_version"] == "v0.3.7"
            assert template["mapping_version"] == read(source / "extraction_run_manifest.json")["mapping_version"]
            assert {record["candidate_id"] for record in template["records"]} == {
                candidate["candidate_id"] for candidate in candidates["candidates"]
            }
            assert all("review_checklist" in record for record in template["records"])
            if ticker == "EXMP":
                assert {"approve", "adjust", "reject", "unresolved", "needs_more_evidence"} <= {
                    record["reviewer_decision"] for record in template["records"]
                }
            else:
                assert {record["reviewer_decision"] for record in template["records"]} == {"unresolved"}

    print("PASS: EXMP/MRVL/NVDA/AVGO reviewer workbenches, required fields, boundaries and decision templates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
