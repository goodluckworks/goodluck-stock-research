#!/usr/bin/env python3
"""Fixture-format tests for data_attr, inline_like and instance_xml subsets."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from offline_xbrl_candidate_extractor import Config, run as run_extraction  # noqa: E402


FIXTURES = XBRL_DIR / "fixtures"
MAPPING = XBRL_DIR / "mappings" / "us_gaap_core_v0_3_7.json"


def base_config(input_file: Path, output_dir: Path, fixture_format: str) -> Config:
    """Return EXMP config."""
    return Config(
        input_file=input_file,
        mapping_file=MAPPING,
        company="Example Semiconductor Corp.",
        ticker="EXMP",
        cik="0000000000",
        accession="fictional-exmp-001",
        form_type="10-K",
        reporting_period="FY2025",
        fiscal_year="2025",
        fiscal_quarter="FY",
        currency="USD",
        amount_unit="USD millions",
        per_share_unit="USD/share",
        fixture_format=fixture_format,
        output_dir=output_dir,
    )


def run_case(input_file: Path, output_dir: Path, fixture_format: str) -> str:
    """Run extraction and return report text."""
    run_extraction(base_config(input_file, output_dir, fixture_format))
    report = (output_dir / "extraction_run_report.md").read_text(encoding="utf-8")
    assert "not production iXBRL parsing" in report
    return report


def main() -> int:
    """Run fixture-format tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-fixture-format-tests-") as temp_name:
        temp = Path(temp_name)
        run_case(FIXTURES / "exmp_fictional_inline_xbrl.html", temp / "data_attr", "data_attr")
        run_case(FIXTURES / "exmp_inline_xbrl_like.html", temp / "inline_like", "inline_like")
        run_case(FIXTURES / "exmp_instance_document.xml", temp / "instance_xml", "instance_xml")
        run_case(FIXTURES / "exmp_inline_xbrl_like.html", temp / "auto", "auto")

        wrong = temp / "wrong-unit.html"
        wrong.write_text(
            '<html><body><xbrli-context id="C1" data-xbrl-period-type="duration" data-xbrl-period="FY2025" data-xbrl-dimensions=""></xbrli-context>'
            '<xbrli-unit id="EUR" measure="EUR"></xbrli-unit>'
            '<ix-nonFraction name="us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax" contextRef="C1" unitRef="EUR" data-xbrl-statement="income_statement" data-xbrl-locator="wrong unit">100</ix-nonFraction>'
            '</body></html>',
            encoding="utf-8",
        )
        run_extraction(base_config(wrong, temp / "wrong-unit-output", "inline_like"))
        unresolved = (temp / "wrong-unit-output" / "unresolved_fields.json").read_text(encoding="utf-8")
        assert "wrong_unit" in unresolved

        wrong_period = temp / "wrong-period.xml"
        wrong_period.write_text(
            '<xbrl-fixture><context id="C1" periodType="duration" period="FY2024" dimensions="" />'
            '<unit id="USD" measure="USD" />'
            '<fact concept="us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax" contextRef="C1" unitRef="USD" statement="income_statement" locator="wrong period">100</fact>'
            '</xbrl-fixture>',
            encoding="utf-8",
        )
        run_extraction(base_config(wrong_period, temp / "wrong-period-output", "instance_xml"))
        assert "wrong_period" in (temp / "wrong-period-output" / "unresolved_fields.json").read_text(encoding="utf-8")

        dimension = temp / "dimension.html"
        dimension.write_text(
            '<html><body><xbrli-context id="C1" data-xbrl-period-type="duration" data-xbrl-period="FY2025" data-xbrl-dimensions="SegmentAxis=One"></xbrli-context>'
            '<xbrli-unit id="USD" measure="USD"></xbrli-unit>'
            '<ix-nonFraction name="us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax" contextRef="C1" unitRef="USD" data-xbrl-statement="income_statement" data-xbrl-locator="dimension">100</ix-nonFraction>'
            '</body></html>',
            encoding="utf-8",
        )
        run_extraction(base_config(dimension, temp / "dimension-output", "inline_like"))
        assert "dimension_conflict" in (temp / "dimension-output" / "unresolved_fields.json").read_text(encoding="utf-8")

        external = temp / "external.html"
        external.write_text(
            '<html><body>https://example.com/taxonomy.xsd<ix-nonFraction name="us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax" contextRef="C" unitRef="USD">100</ix-nonFraction></body></html>',
            encoding="utf-8",
        )
        try:
            run_extraction(base_config(external, temp / "external-output", "inline_like"))
        except ValueError as exc:
            assert "external URLs" in str(exc)
        else:
            raise AssertionError("External URL fixture should fail.")

    print("PASS: fixture formats data_attr, inline_like, instance_xml, auto, wrong unit, wrong period, dimension rejection, external URL block and production-claim absence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
