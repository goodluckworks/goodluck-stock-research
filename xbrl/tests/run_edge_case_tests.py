#!/usr/bin/env python3
"""Expanded synthetic edge-case fixture tests."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from offline_xbrl_candidate_extractor import Config, run as run_extraction  # noqa: E402


EDGE = XBRL_DIR / "fixtures" / "edge_cases"
MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"
FIELD_BY_FIXTURE = {
    "debt_double_count_complex.html": "total_debt",
    "capex_scope_ambiguity.html": "capital_expenditure",
    "restricted_cash_confusion.html": "cash_and_equivalents",
    "diluted_shares_wrong_duration.html": "diluted_shares",
    "duration_vs_instant_mismatch.html": "cash_and_equivalents",
}


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def run_fixture(fixture: Path, output: Path) -> tuple[dict[str, object], dict[str, object]]:
    """Run one edge fixture."""
    run_extraction(
        Config(
            input_file=fixture,
            mapping_file=MAPPING,
            company="Example Semiconductor Corp.",
            ticker="EXMP",
            cik="0000000000",
            accession=f"edge-{fixture.stem}",
            form_type="10-K",
            reporting_period="FY2025",
            fiscal_year="2025",
            fiscal_quarter="FY",
            currency="USD",
            amount_unit="USD millions",
            per_share_unit="USD/share",
            fixture_format="data_attr",
            output_dir=output,
        )
    )
    return read(output / "extraction_candidates.json"), read(output / "unresolved_fields.json")


def by_field(items: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    """Filter package records by normalized field."""
    return [item for item in items if item.get("normalized_field") == field]


def main() -> int:
    """Run edge-case tests."""
    expected = read(EDGE / "expected_results.json")
    assert set(expected) <= {path.name for path in EDGE.glob("*.html")}
    with tempfile.TemporaryDirectory(prefix="xbrl-edge-case-tests-") as temp_name:
        temp = Path(temp_name)
        for fixture_name, spec_obj in expected.items():
            spec = dict(spec_obj)
            candidates_doc, unresolved_doc = run_fixture(EDGE / fixture_name, temp / fixture_name.replace(".html", ""))
            candidates = candidates_doc["candidates"]
            unresolved = unresolved_doc["unresolved_fields"]
            rejected = unresolved_doc["rejected_facts"]
            target_field = FIELD_BY_FIXTURE.get(fixture_name, "revenue")
            target_candidates = by_field(candidates, target_field)
            target_unresolved = by_field(unresolved, target_field)

            if spec["expected"] == "candidate":
                assert target_candidates, fixture_name
                assert target_candidates[0]["confidence"] == spec["confidence"]
                assert spec["warning"] in target_candidates[0]["warning_flags"]
            elif spec["expected"] == "candidate_with_rejected_peer":
                assert target_candidates, fixture_name
                assert any(spec["rejected_reason"] in item["reasons"] for item in rejected)
            elif spec["expected"] == "warning":
                assert target_candidates, fixture_name
                assert spec["warning"] in target_candidates[0]["warning_flags"]
            else:
                assert target_unresolved, fixture_name
                assert target_unresolved[0]["reason_code"] == spec["reason_code"], fixture_name
                if "rejected_reason" in spec:
                    assert any(spec["rejected_reason"] in item["reasons"] for item in rejected), fixture_name

    print("PASS: synthetic edge cases for extension, restatement, debt, capex, cash, shares, units, materiality, dimensions and period type")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
