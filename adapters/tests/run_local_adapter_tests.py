#!/usr/bin/env python3
"""Run local-only contract tests for the filing evidence adapter."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path
from types import ModuleType


TEST_DIR = Path(__file__).resolve().parent
ADAPTER_PATH = TEST_DIR.parent / "local_official_filing_adapter.py"
FIXTURE_DIR = TEST_DIR / "fixtures"
EXPECTED_DIR = TEST_DIR / "expected"
REQUIRED_OUTPUTS = {
    "raw_snapshot_manifest.json",
    "source_manifest.json",
    "field_provenance.json",
    "unresolved_fields.json",
    "normalized_input_draft.json",
    "adapter_run_report.md",
}
REQUIRED_SOURCE_FIELDS = {
    "source_id",
    "source_name",
    "source_type",
    "source_url",
    "retrieved_at",
    "source_date",
    "filing_date",
    "form_type",
    "reporting_period",
    "fiscal_year",
    "fiscal_quarter",
    "currency",
    "amount_unit",
    "per_share_unit",
    "source_status",
    "data_status",
    "confidence",
    "transformation_notes",
    "notes",
}
REQUIRED_UNRESOLVED = {
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "total_debt",
    "diluted_shares",
}
PROHIBITED_OUTPUT_KEYS = {
    "investment_conclusion",
    "recommendation",
    "target_price",
    "position_size",
    "research_status",
    "portfolio_action",
}
PROHIBITED_IMPORT_ROOTS = {
    "requests",
    "urllib",
    "http",
    "socket",
    "aiohttp",
    "yfinance",
    "openbb",
    "subprocess",
    "selenium",
    "playwright",
}


def load_adapter() -> ModuleType:
    """Import the adapter from its filesystem path."""
    spec = importlib.util.spec_from_file_location(
        "local_official_filing_adapter", ADAPTER_PATH
    )
    if spec is None or spec.loader is None:
        raise AssertionError("Could not load adapter module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, object]:
    """Read a JSON object."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AssertionError(f"Expected JSON object: {path}")
    return payload


def sha256(path: Path) -> str:
    """Return SHA-256 for a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def assert_no_prohibited_code() -> None:
    """Check imports and obvious prohibited runtime calls statically."""
    source = ADAPTER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots = {alias.name.split(".", 1)[0] for alias in node.names}
            assert not roots & PROHIBITED_IMPORT_ROOTS, roots
        if isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".", 1)[0]
            assert root not in PROHIBITED_IMPORT_ROOTS, root
        if isinstance(node, ast.Attribute):
            assert not (
                isinstance(node.value, ast.Name)
                and node.value.id == "os"
                and node.attr == "environ"
            ), "os.environ is prohibited"
    for token in ("data.sec.gov", "broker.connect(", "place_order(", "execute_trade("):
        assert token not in source, f"Prohibited implementation token: {token}"


def config_from_expected(
    module: ModuleType, expected: dict[str, object], output_dir: Path, overwrite: bool
) -> object:
    """Build AdapterConfig from one expected fixture definition."""
    fixture = FIXTURE_DIR / str(expected["fixture"])
    return module.AdapterConfig(
        input_file=fixture,
        company=str(expected["company"]),
        ticker=str(expected["ticker"]),
        source_type="official_filing",
        form_type=str(expected["form_type"]),
        filing_date=str(expected["filing_date"]),
        reporting_period=str(expected["reporting_period"]),
        fiscal_year=str(expected["fiscal_year"]),
        fiscal_quarter=str(expected["fiscal_quarter"]),
        source_url=str(expected["source_url"]),
        currency="USD",
        amount_unit="USD millions",
        per_share_unit="USD/share",
        output_dir=output_dir,
        source_status="verified",
        data_status="available",
        retrieved_at="2026-06-25T12:00:00Z",
        notes="Local test fixture; evidence packaging only.",
        overwrite=overwrite,
    )


def assert_fixture_run(
    module: ModuleType, expected_path: Path, temp_root: Path
) -> None:
    """Run and validate one fixture."""
    expected = read_json(expected_path)
    ticker = str(expected["ticker"])
    output_dir = temp_root / ticker
    config = config_from_expected(module, expected, output_dir, overwrite=False)
    outputs = module.run_adapter(config)

    assert set(outputs) == REQUIRED_OUTPUTS
    for path in outputs.values():
        assert path.is_file() and path.stat().st_size > 0, path

    raw_manifest = read_json(output_dir / "raw_snapshot_manifest.json")
    source_manifest = read_json(output_dir / "source_manifest.json")
    provenance = read_json(output_dir / "field_provenance.json")
    unresolved = read_json(output_dir / "unresolved_fields.json")
    draft = read_json(output_dir / "normalized_input_draft.json")
    report = (output_dir / "adapter_run_report.md").read_text(encoding="utf-8")

    fixture_path = FIXTURE_DIR / str(expected["fixture"])
    assert raw_manifest["sha256"] == sha256(fixture_path)
    assert raw_manifest["sha256"] == expected["sha256"]
    snapshot_path = Path(str(raw_manifest["raw_snapshot_path"]))
    assert snapshot_path.is_file()
    assert sha256(snapshot_path) == expected["sha256"]
    assert raw_manifest["immutable"] is True
    assert raw_manifest["overwrite_used"] is False

    assert REQUIRED_SOURCE_FIELDS <= set(source_manifest)
    assert source_manifest["source_status"] == "verified"
    assert source_manifest["data_status"] == "available"
    assert source_manifest["source_status"] != source_manifest["data_status"]
    assert source_manifest["verification_basis"] == (
        "user_supplied_metadata_and_local_file_checksum_only"
    )
    assert source_manifest["source_url"] == expected["source_url"]
    assert source_manifest["reporting_period"] == expected["reporting_period"]

    records = provenance.get("records")
    assert isinstance(records, list) and records
    assert records[0]["field_name"] == "raw_filing_text"
    assert records[0]["source_id"] == source_manifest["source_id"]

    unresolved_records = unresolved.get("unresolved_fields")
    assert isinstance(unresolved_records, list) and unresolved_records
    unresolved_names = {record["field_name"] for record in unresolved_records}
    assert REQUIRED_UNRESOLVED <= unresolved_names
    assert unresolved.get("errors") == []
    assert len(unresolved.get("warnings", [])) >= 2

    assert draft["status"] == "draft_unpopulated"
    assert set(draft) == {"status", "reason", "target_schemas"}
    serialized_outputs = json.dumps(
        [raw_manifest, source_manifest, provenance, unresolved, draft],
        ensure_ascii=False,
    )
    for key in PROHIBITED_OUTPUT_KEYS:
        assert f'"{key}"' not in serialized_outputs
    for heading in (
        "## Investment Conclusion",
        "## Recommendation",
        "Target price:",
        "Position size:",
        "Research status:",
    ):
        assert heading not in report
    assert "No network request" in report
    assert "requires manual normalization" in report

    try:
        module.run_adapter(config)
    except FileExistsError:
        pass
    else:
        raise AssertionError("Non-empty output directory should fail by default.")

    overwrite_config = config_from_expected(
        module, expected, output_dir, overwrite=True
    )
    module.run_adapter(overwrite_config)
    overwritten_manifest = read_json(output_dir / "raw_snapshot_manifest.json")
    assert overwritten_manifest["overwrite_used"] is True
    assert sha256(Path(str(overwritten_manifest["raw_snapshot_path"]))) == expected[
        "sha256"
    ]

    modified_fixture = temp_root / f"{ticker.lower()}-modified.html"
    modified_fixture.write_bytes(
        fixture_path.read_bytes() + b"\n<!-- modified fixture version -->\n"
    )
    changed_config = module.AdapterConfig(
        **{
            **overwrite_config.__dict__,
            "input_file": modified_fixture,
        }
    )
    module.run_adapter(changed_config)
    raw_files = list((output_dir / "raw").iterdir())
    assert len(raw_files) == 2, "Changed content must retain the prior raw snapshot."
    changed_manifest = read_json(output_dir / "raw_snapshot_manifest.json")
    assert changed_manifest["sha256"] == sha256(modified_fixture)
    assert changed_manifest["sha256"] != expected["sha256"]


def assert_scope_restrictions(module: ModuleType, temp_root: Path) -> None:
    """Confirm the implementation remains an official-filing-only adapter."""
    expected = read_json(
        EXPECTED_DIR / "sample_mrvl_expected_manifest.json"
    )
    config = config_from_expected(
        module, expected, temp_root / "invalid-source", overwrite=False
    )
    invalid = module.AdapterConfig(
        **{
            **config.__dict__,
            "source_type": "secondary_market_page",
        }
    )
    try:
        module.run_adapter(invalid)
    except ValueError as exc:
        assert "official_filing" in str(exc)
    else:
        raise AssertionError("Non-official source type should be rejected.")

    same_path_config = module.AdapterConfig(
        **{
            **config.__dict__,
            "output_dir": config.input_file,
        }
    )
    try:
        module.run_adapter(same_path_config)
    except ValueError as exc:
        assert "cannot equal input_file" in str(exc)
    else:
        raise AssertionError("output_dir equal to input_file should be rejected.")


def main() -> int:
    """Run all local adapter tests."""
    assert_no_prohibited_code()
    module = load_adapter()
    expected_paths = sorted(EXPECTED_DIR.glob("sample_*_expected_manifest.json"))
    if len(expected_paths) != 3:
        raise AssertionError("Expected exactly three fixture expectation files.")
    with tempfile.TemporaryDirectory(prefix="local-filing-adapter-tests-") as temp:
        temp_root = Path(temp)
        for expected_path in expected_paths:
            assert_fixture_run(module, expected_path, temp_root)
            print(f"PASS: {expected_path.name}")
        assert_scope_restrictions(module, temp_root)
    print("PASS: local adapter contract, overwrite, URL-string, and safety tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
