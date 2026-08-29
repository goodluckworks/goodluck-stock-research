#!/usr/bin/env python3
"""Contract and edge-case tests for offline candidate extraction."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from types import ModuleType


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
ROOT = XBRL_DIR.parent
FIXTURES = XBRL_DIR / "fixtures"
MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"
EXTRACTOR = XBRL_DIR / "offline_xbrl_candidate_extractor.py"
sys.path.insert(0, str(XBRL_DIR))

CASES = {
    "EXMP": (
        "Example Semiconductor Corp.",
        "0000000000",
        "fictional-exmp-001",
        "FY2025",
        "exmp_fictional_inline_xbrl.html",
    ),
    "MRVL": (
        "Marvell Technology, Inc.",
        "1835632",
        "0001835632-26-000011",
        "FY2026",
        "mrvl_candidate_fixture.html",
    ),
    "NVDA": (
        "NVIDIA Corporation",
        "1045810",
        "fictional-nvda-candidate",
        "FY2026",
        "nvda_candidate_fixture.html",
    ),
    "AVGO": (
        "Broadcom Inc.",
        "1730168",
        "fictional-avgo-candidate",
        "FY2025",
        "avgo_candidate_fixture.html",
    ),
}
REQUIRED_OUTPUTS = {
    "extraction_run_manifest.json",
    "extraction_candidates.json",
    "field_provenance.json",
    "unresolved_fields.json",
    "extraction_run_report.md",
}


def load_module() -> ModuleType:
    """Load extractor module."""
    spec = importlib.util.spec_from_file_location("offline_xbrl", EXTRACTOR)
    if spec is None or spec.loader is None:
        raise AssertionError("Could not load extractor.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def config_for(
    module: ModuleType, ticker: str, input_file: Path, output_dir: Path
) -> object:
    """Create test config."""
    company, cik, accession, period, _ = CASES[ticker]
    return module.Config(
        input_file=input_file,
        mapping_file=MAPPING,
        company=company,
        ticker=ticker,
        cik=cik,
        accession=accession,
        form_type="10-K",
        reporting_period=period,
        fiscal_year=period.replace("FY", ""),
        fiscal_quarter="FY",
        currency="USD",
        amount_unit="USD millions",
        per_share_unit="USD/share",
        fixture_format="auto",
        output_dir=output_dir,
    )


def run_case(module: ModuleType, ticker: str, root: Path) -> Path:
    """Run one named fixture."""
    filename = CASES[ticker][4]
    output = root / ticker
    module.run(config_for(module, ticker, FIXTURES / filename, output))
    files = {path.name for path in output.iterdir() if path.is_file()}
    assert REQUIRED_OUTPUTS <= files
    assert all((output / name).stat().st_size > 0 for name in REQUIRED_OUTPUTS)
    assert not (output / "approved_normalized_draft.json").exists()
    manifest = read_json(output / "extraction_run_manifest.json")
    candidates = read_json(output / "extraction_candidates.json")
    provenance = read_json(output / "field_provenance.json")
    assert manifest["mode"] == "offline_fixture_only"
    assert manifest["review_status"] == "draft_extracted_unreviewed"
    assert manifest["fixture_data_status"] == (
        "fictional_sample"
        if ticker == "EXMP"
        else "synthetic_unverified_real_company_shape"
    )
    assert all(
        item["review_status"] == "draft_extracted_unreviewed"
        for item in candidates["candidates"]
    )
    assert {
        item["candidate_id"] for item in candidates["candidates"]
    } == {
        item["candidate_id"] for item in provenance["records"]
    }
    return output


def artificial_fact(
    concept: str,
    period: str = "FY2025",
    unit: str = "USD",
    dimensions: str = "",
    value: str = "100",
    locator: str = "temporary fact",
) -> str:
    """Return one artificial fixture fact."""
    return (
        f'<span data-xbrl-concept="{concept}" '
        'data-xbrl-context="TEMP-CONTEXT" '
        'data-xbrl-period-type="duration" '
        f'data-xbrl-period="{period}" data-xbrl-unit="{unit}" '
        f'data-xbrl-dimensions="{dimensions}" '
        'data-xbrl-statement="income_statement" '
        f'data-xbrl-locator="{locator}">{value}</span>'
    )


def run_temporary_fixture(
    module: ModuleType, root: Path, name: str, body: str
) -> tuple[dict[str, object], dict[str, object]]:
    """Run a temporary EXMP fixture."""
    fixture = root / f"{name}.html"
    fixture.write_text(f"<!doctype html><html><body>{body}</body></html>")
    output = root / f"{name}-output"
    module.run(config_for(module, "EXMP", fixture, output))
    return (
        read_json(output / "extraction_candidates.json"),
        read_json(output / "unresolved_fields.json"),
    )


def main() -> int:
    """Run all candidate tests."""
    module = load_module()
    with tempfile.TemporaryDirectory(prefix="xbrl-candidate-tests-") as temp:
        root = Path(temp)
        outputs = {
            ticker: run_case(module, ticker, root) for ticker in CASES
        }

        exmp_candidates = read_json(
            outputs["EXMP"] / "extraction_candidates.json"
        )["candidates"]
        assert len(exmp_candidates) == 9
        assert {item["normalized_field"] for item in exmp_candidates} == set(
            module.SCOPED_FIELDS
        )
        capex = next(
            item
            for item in exmp_candidates
            if item["normalized_field"] == "capital_expenditure"
        )
        assert capex["source_value"] == "-90"
        assert capex["extracted_value"] == 90
        assert capex["transformation"] == "absolute_value_to_positive_outflow"

        mrvl_unresolved = read_json(
            outputs["MRVL"] / "unresolved_fields.json"
        )["unresolved_fields"]
        assert ("gross_profit", "missing_field") in {
            (item["normalized_field"], item["reason_code"])
            for item in mrvl_unresolved
        }
        assert ("revenue", "multiple_candidates") in {
            (item["normalized_field"], item["reason_code"])
            for item in mrvl_unresolved
        }

        nvda_candidates = read_json(
            outputs["NVDA"] / "extraction_candidates.json"
        )["candidates"]
        shares = next(
            item
            for item in nvda_candidates
            if item["normalized_field"] == "diluted_shares"
        )
        assert shares["context_id"] == "NVDA-FY2026"
        nvda_rejected = read_json(
            outputs["NVDA"] / "unresolved_fields.json"
        )["rejected_facts"]
        reasons = {reason for item in nvda_rejected for reason in item["reasons"]}
        assert {"dimension_conflict", "wrong_period", "split_basis_unverified"} <= reasons

        avgo_unresolved = read_json(
            outputs["AVGO"] / "unresolved_fields.json"
        )["unresolved_fields"]
        assert any(
            item["normalized_field"] == "total_debt"
            and item["reason_code"] == "debt_double_count_risk"
            for item in avgo_unresolved
        )
        avgo_rejected = read_json(
            outputs["AVGO"] / "unresolved_fields.json"
        )["rejected_facts"]
        assert any("dimension_conflict" in item["reasons"] for item in avgo_rejected)

        concept = "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
        _, wrong_period = run_temporary_fixture(
            module, root, "wrong-period", artificial_fact(concept, period="FY2024")
        )
        assert any(
            item["normalized_field"] == "revenue"
            and item["reason_code"] == "no_eligible_fact"
            for item in wrong_period["unresolved_fields"]
        )
        assert any(
            "wrong_period" in item["reasons"]
            for item in wrong_period["rejected_facts"]
        )

        _, wrong_unit = run_temporary_fixture(
            module, root, "wrong-unit", artificial_fact(concept, unit="EUR")
        )
        assert any(
            "wrong_unit" in item["reasons"]
            for item in wrong_unit["rejected_facts"]
        )

        _, dimension = run_temporary_fixture(
            module,
            root,
            "dimension",
            artificial_fact(concept, dimensions="SegmentAxis=ExampleMember"),
        )
        assert any(
            "dimension_conflict" in item["reasons"]
            for item in dimension["rejected_facts"]
        )

        _, multiple = run_temporary_fixture(
            module,
            root,
            "multiple",
            artificial_fact(concept, locator="candidate one")
            + artificial_fact(
                "us-gaap:SalesRevenueNet", value="101", locator="candidate two"
            ),
        )
        assert any(
            item["normalized_field"] == "revenue"
            and item["reason_code"] == "multiple_candidates"
            for item in multiple["unresolved_fields"]
        )

    print("PASS: candidate extraction fixtures, provenance, ambiguity, period, unit, dimension, capex, debt, and shares tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
