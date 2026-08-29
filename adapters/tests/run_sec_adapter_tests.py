#!/usr/bin/env python3
"""Fixture and mocked-live tests for the SEC official filing adapter."""

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
ADAPTER_PATH = TEST_DIR.parent / "sec_official_filing_adapter.py"
FIXTURE = TEST_DIR / "fixtures" / "sec_filing_document_sample.html"
REQUIRED_OUTPUTS = {
    "raw_snapshot_manifest.json",
    "source_manifest.json",
    "field_provenance.json",
    "unresolved_fields.json",
    "normalized_input_draft.json",
    "adapter_run_report.md",
}
CASES = {
    "MRVL": {
        "company": "Marvell Technology, Inc.",
        "cik": "1835632",
        "accession": "0001835632-26-000011",
        "filing_date": "2026-03-11",
        "period": "FY2026",
        "year": "2026",
        "url": (
            "https://www.sec.gov/Archives/edgar/data/1835632/"
            "000183563226000011/mrvl-20260131.htm"
        ),
    },
    "NVDA": {
        "company": "NVIDIA Corporation",
        "cik": "1045810",
        "accession": "0001045810-26-000021",
        "filing_date": "2026-02-25",
        "period": "FY2026",
        "year": "2026",
        "url": (
            "https://www.sec.gov/Archives/edgar/data/1045810/"
            "000104581026000021/nvda-20260125.htm"
        ),
    },
    "AVGO": {
        "company": "Broadcom Inc.",
        "cik": "1730168",
        "accession": "0001730168-25-000121",
        "filing_date": "2025-12-18",
        "period": "FY2025",
        "year": "2025",
        "url": (
            "https://www.sec.gov/Archives/edgar/data/1730168/"
            "000173016825000121/avgo-20251102.htm"
        ),
    },
}


def load_adapter() -> ModuleType:
    """Load adapter module."""
    spec = importlib.util.spec_from_file_location(
        "sec_official_filing_adapter", ADAPTER_PATH
    )
    if spec is None or spec.loader is None:
        raise AssertionError("Could not load SEC adapter.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, object]:
    """Read a JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def fixture_config(
    module: ModuleType,
    ticker: str,
    output_dir: Path,
    mode: str = "fixture",
    overwrite: bool = False,
) -> object:
    """Build fixture/live config."""
    case = CASES[ticker]
    return module.AdapterConfig(
        mode=mode,
        input_file=FIXTURE if mode == "fixture" else None,
        company=case["company"],
        ticker=ticker,
        cik=case["cik"],
        form_type="10-K",
        accession=case["accession"],
        filing_date=case["filing_date"],
        reporting_period=case["period"],
        fiscal_year=case["year"],
        fiscal_quarter="FY",
        source_url=case["url"],
        currency="USD",
        amount_unit="USD millions",
        per_share_unit="USD/share",
        user_agent="Research Tester test@example.com",
        output_dir=output_dir,
        source_status="verified",
        data_status="available",
        retrieved_at="2026-06-25T12:00:00Z",
        notes="Artificial SEC fixture.",
        timeout=5.0,
        min_request_interval=0.2,
        max_requests=3,
        max_bytes=1_000_000,
        overwrite=overwrite,
    )


def assert_outputs(output_dir: Path, expected_mode: str) -> None:
    """Validate common output contract."""
    files = {path.name for path in output_dir.iterdir() if path.is_file()}
    assert REQUIRED_OUTPUTS <= files
    for name in REQUIRED_OUTPUTS:
        assert (output_dir / name).stat().st_size > 0
    raw = read_json(output_dir / "raw_snapshot_manifest.json")
    source = read_json(output_dir / "source_manifest.json")
    provenance = read_json(output_dir / "field_provenance.json")
    unresolved = read_json(output_dir / "unresolved_fields.json")
    draft = read_json(output_dir / "normalized_input_draft.json")
    report = (output_dir / "adapter_run_report.md").read_text(encoding="utf-8")
    assert raw["mode"] == expected_mode
    assert raw["sec_domain_validated"] is True
    assert source["source_status"] != source["data_status"]
    assert draft["status"] == "draft_unpopulated"
    assert "revenue" in {
        record["field_name"] for record in unresolved["unresolved_fields"]
    }
    assert provenance["records"]
    assert "User-Agent provided: `Yes`" in report
    for forbidden in (
        "Target price:",
        "Buy:",
        "Sell:",
        "Position size:",
        "Research status:",
    ):
        assert forbidden not in report


def assert_fixture_cases(module: ModuleType, root: Path) -> None:
    """Run three offline fixtures and overwrite checks."""
    expected_sha = hashlib.sha256(FIXTURE.read_bytes()).hexdigest()
    for ticker in CASES:
        output_dir = root / f"fixture-{ticker}"
        config = fixture_config(module, ticker, output_dir)
        module.run_adapter(config)
        assert_outputs(output_dir, "fixture")
        raw = read_json(output_dir / "raw_snapshot_manifest.json")
        assert raw["sha256"] == expected_sha
        assert raw["http_status"] == "fixture"
        assert raw["request_count"] == 0
        assert raw["overwrite_used"] is False
        assert raw["source_url"] == CASES[ticker]["url"]
        try:
            module.run_adapter(config)
        except FileExistsError:
            pass
        else:
            raise AssertionError("Default overwrite protection failed.")
        overwrite = fixture_config(module, ticker, output_dir, overwrite=True)
        module.run_adapter(overwrite)
        assert read_json(output_dir / "raw_snapshot_manifest.json")[
            "overwrite_used"
        ] is True
        print(f"PASS fixture: {ticker}")


def assert_mocked_live(module: ModuleType, root: Path) -> None:
    """Test successful and failed live paths without real network."""
    calls: list[str] = []

    def success_fetch(url: str, user_agent: str, timeout: float, max_bytes: int):
        calls.append(url)
        assert user_agent and timeout == 5.0 and max_bytes == 1_000_000
        return module.FetchResponse(
            body=b"<html>mocked SEC response</html>",
            status=200,
            final_url=url,
            content_type="text/html",
            retrieved_at="2026-06-25T12:01:00Z",
        )

    output_dir = root / "live-success"
    config = fixture_config(module, "MRVL", output_dir, mode="live")
    module.run_adapter(config, fetcher=success_fetch, sleeper=lambda _: None)
    assert calls == [CASES["MRVL"]["url"]]
    assert_outputs(output_dir, "live")
    raw = read_json(output_dir / "raw_snapshot_manifest.json")
    assert raw["http_status"] == 200 and raw["request_count"] == 1
    assert raw["retrieved_at"] == "2026-06-25T12:01:00Z"

    attempts = {"count": 0}

    def failed_fetch(url: str, user_agent: str, timeout: float, max_bytes: int):
        attempts["count"] += 1
        return module.FetchResponse(
            body=b"",
            status=503,
            final_url=url,
            content_type="text/html",
            retrieved_at="2026-06-25T12:02:00Z",
        )

    failed_dir = root / "live-http-failure"
    failed_config = fixture_config(module, "MRVL", failed_dir, mode="live")
    module.run_adapter(
        failed_config, fetcher=failed_fetch, sleeper=lambda _: None
    )
    assert attempts["count"] == 3
    failure = read_json(failed_dir / "unresolved_fields.json")
    assert failure["errors"][0]["code"] == "http_error"
    assert not read_json(failed_dir / "field_provenance.json")["records"]

    def timeout_fetch(url: str, user_agent: str, timeout: float, max_bytes: int):
        raise TimeoutError("mock timeout")

    timeout_dir = root / "live-timeout"
    timeout_config = fixture_config(module, "NVDA", timeout_dir, mode="live")
    module.run_adapter(
        timeout_config, fetcher=timeout_fetch, sleeper=lambda _: None
    )
    timeout_payload = read_json(timeout_dir / "unresolved_fields.json")
    assert timeout_payload["errors"][0]["code"] == "network_error"
    print("PASS mocked live: success, HTTP failure, timeout")


def assert_validation_failures(module: ModuleType, root: Path) -> None:
    """Confirm failures occur before any fetch."""
    called = {"value": False}

    def forbidden_fetch(url: str, user_agent: str, timeout: float, max_bytes: int):
        called["value"] = True
        raise AssertionError("Fetcher should not be called.")

    base = fixture_config(module, "MRVL", root / "invalid", mode="live")
    for changes in (
        {"source_url": "https://example.com/not-sec"},
        {"source_url": "https://www.sec.gov.example.com/not-sec"},
        {"user_agent": ""},
        {"user_agent": "anonymous-agent"},
        {"user_agent": "Researcher http-contact-without-url"},
        {"mode": "invalid"},
    ):
        invalid = module.AdapterConfig(**{**base.__dict__, **changes})
        try:
            module.run_adapter(invalid, fetcher=forbidden_fetch)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected validation failure: {changes}")
    assert called["value"] is False

    redirect_handler = module.SECOnlyRedirectHandler()
    try:
        redirect_handler.redirect_request(
            None, None, 302, "Found", {}, "https://example.com/redirect"
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Non-SEC redirect should be blocked.")

    attempts = {"count": 0}

    def not_found_fetch(url: str, user_agent: str, timeout: float, max_bytes: int):
        attempts["count"] += 1
        return module.FetchResponse(
            body=b"",
            status=404,
            final_url=url,
            content_type="text/html",
            retrieved_at="2026-06-25T12:03:00Z",
        )

    not_found_dir = root / "live-404"
    not_found = fixture_config(module, "MRVL", not_found_dir, mode="live")
    module.run_adapter(
        not_found, fetcher=not_found_fetch, sleeper=lambda _: None
    )
    assert attempts["count"] == 1
    error = read_json(not_found_dir / "unresolved_fields.json")["errors"][0]
    assert error["code"] == "http_error" and error["retryable"] is False

    fixture = fixture_config(module, "MRVL", root / "unused")
    same_path = module.AdapterConfig(
        **{**fixture.__dict__, "output_dir": FIXTURE}
    )
    try:
        module.run_adapter(same_path)
    except ValueError:
        pass
    else:
        raise AssertionError("output_dir == input_file should fail.")
    print("PASS validation: URL, redirect, User-Agent, mode, path")


def assert_network_scope() -> None:
    """Ensure urllib network imports stay in the SEC adapter."""
    sec_tree = ast.parse(ADAPTER_PATH.read_text(encoding="utf-8"))
    assert any(
        isinstance(node, ast.Import) and any(alias.name == "urllib.request" for alias in node.names)
        for node in ast.walk(sec_tree)
    )
    for path in (
        TEST_DIR.parent / "local_official_filing_adapter.py",
        TEST_DIR.parent.parent / "scripts" / "ratio_calculator.py",
        TEST_DIR.parent.parent / "scripts" / "dcf_sensitivity.py",
        TEST_DIR.parent.parent / "scripts" / "peer_comps_table.py",
        TEST_DIR.parent.parent / "scripts" / "implied_expectations.py",
    ):
        text = path.read_text(encoding="utf-8")
        assert "urllib.request" not in text and "urlopen(" not in text


def main() -> int:
    """Run all fixture and mocked-live tests."""
    module = load_adapter()
    assert_network_scope()
    with tempfile.TemporaryDirectory(prefix="sec-adapter-tests-") as temp:
        root = Path(temp)
        assert_fixture_cases(module, root)
        assert_mocked_live(module, root)
        assert_validation_failures(module, root)
    print("PASS: SEC adapter fixture/mocked-live contract and scope tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
