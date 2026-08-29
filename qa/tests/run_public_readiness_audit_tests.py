#!/usr/bin/env python3
"""Tests for public-readiness audit."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
QA_DIR = ROOT / "goodluck-stock-research" / "qa"
sys.path.insert(0, str(QA_DIR))

from public_readiness_audit import audit_public_readiness  # noqa: E402


def write_minimal_repo(tmp_root: Path) -> None:
    """Create enough repository structure for focused public-readiness tests."""
    (tmp_root / "goodluck-stock-research" / "examples").mkdir(parents=True)
    (tmp_root / "goodluck-stock-research" / "pipeline").mkdir(parents=True)
    (tmp_root / "goodluck-stock-research" / "production" / "ingestion").mkdir(parents=True)
    (tmp_root / "goodluck-stock-research" / "production" / "audit").mkdir(parents=True)
    (tmp_root / "README.md").write_text("This repo does not provide investment advice or live extraction.\n", encoding="utf-8")
    (tmp_root / "goodluck-stock-research" / "README.md").write_text("No production parser.\n", encoding="utf-8")
    (tmp_root / "CHANGELOG.md").write_text("v2.0\n", encoding="utf-8")


def assert_private_repo_not_public_ready() -> None:
    """Current repo should pass checks but remain not public-ready by policy."""
    results, ready, reason = audit_public_readiness(ROOT, "PRIVATE")
    failed = [item for item in results if not item.passed]
    assert not ready
    assert reason == "requires separate public-readiness approval"
    assert not failed, "\n".join(f"{item.check}: {item.notes}" for item in failed[:20])


def assert_public_visibility_fails() -> None:
    """Public visibility should fail the private-boundary check."""
    results, ready, _ = audit_public_readiness(ROOT, "PUBLIC")
    assert not ready
    assert any(not item.passed and "visibility" in item.check for item in results)


def assert_detects_risky_example_data() -> None:
    """User-local path in examples should be detected as personal data risk."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        write_minimal_repo(tmp_root)
        (tmp_root / "goodluck-stock-research" / "examples" / "leak.md").write_text("/Users/example/private\n", encoding="utf-8")
        results, ready, _ = audit_public_readiness(tmp_root, "PRIVATE")
        assert not ready
        assert any(not item.passed and "personal data" in item.check for item in results)


def assert_red_team_payload_strings_are_not_implementation_risk() -> None:
    """Risk strings in scanner/red-team payload files should not fail implementation checks."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        write_minimal_repo(tmp_root)
        (tmp_root / "goodluck-stock-research" / "production" / "audit" / "production_red_team.py").write_text(
            "PAYLOADS = ['api_key =', 'password =', 'secret =', 'broker.connect', 'place_order']\n",
            encoding="utf-8",
        )
        results, _, _ = audit_public_readiness(tmp_root, "PRIVATE")
        failures = [item for item in results if not item.passed and item.check == "no credentials / secrets implementation"]
        assert not failures, failures
        excluded = [item for item in results if item.check == "scanner/test/red-team payload files excluded from implementation risk"]
        assert excluded and "production_red_team.py" in excluded[0].notes


def assert_real_implementation_risks_fail() -> None:
    """Credential, environment-secret and broker/order code in implementation files should fail."""
    risk_cases = {
        "api_key assignment": "api_key = 'abc'\n",
        "environment secret read": "import os\nvalue = os.environ.get('SECRET')\n",
        "broker order execution": "broker.connect()\nplace_order('MRVL')\nexecute_trade()\n",
    }
    for label, body in risk_cases.items():
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            write_minimal_repo(tmp_root)
            (tmp_root / "goodluck-stock-research" / "production" / "ingestion" / "risky_source.py").write_text(body, encoding="utf-8")
            results, ready, _ = audit_public_readiness(tmp_root, "PRIVATE")
            assert not ready, label
            failures = [item for item in results if not item.passed and item.check == "no credentials / secrets implementation"]
            assert failures and "risky_source.py" in failures[0].notes, label


def main() -> int:
    """Run tests."""
    assert_private_repo_not_public_ready()
    assert_public_visibility_fails()
    assert_detects_risky_example_data()
    assert_red_team_payload_strings_are_not_implementation_risk()
    assert_real_implementation_risks_fail()
    print("PASS: public-readiness audit policy and negative tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
