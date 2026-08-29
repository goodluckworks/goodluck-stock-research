#!/usr/bin/env python3
"""Run v3 module tests from production subdirectories."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

TESTS = [
    "goodluck-stock-research/production/sources/tests/run_source_registry_tests.py",
    "goodluck-stock-research/production/sources/tests/run_company_ir_source_tests.py",
    "goodluck-stock-research/production/sources/tests/run_market_data_source_tests.py",
    "goodluck-stock-research/production/history/tests/run_filing_history_tests.py",
    "goodluck-stock-research/production/history/tests/run_period_aligner_tests.py",
    "goodluck-stock-research/production/history/tests/run_historical_statement_tests.py",
    "goodluck-stock-research/production/comps/tests/run_peer_set_tests.py",
    "goodluck-stock-research/production/comps/tests/run_market_multiples_tests.py",
    "goodluck-stock-research/production/comps/tests/run_comps_auditor_tests.py",
    "goodluck-stock-research/production/valuation/tests/run_dcf_engine_tests.py",
    "goodluck-stock-research/production/valuation/tests/run_multiples_valuation_tests.py",
    "goodluck-stock-research/production/valuation/tests/run_implied_expectations_tests.py",
    "goodluck-stock-research/production/valuation/tests/run_sensitivity_tests.py",
    "goodluck-stock-research/production/valuation/tests/run_valuation_auditor_tests.py",
    "goodluck-stock-research/production/reliability/tests/run_cache_tests.py",
    "goodluck-stock-research/production/reliability/tests/run_error_recovery_tests.py",
    "goodluck-stock-research/production/reliability/tests/run_source_monitor_tests.py",
]


def main() -> int:
    for test in TESTS:
        try:
            runpy.run_path(str(ROOT / test), run_name="__main__")
        except SystemExit as exc:
            if exc.code not in {0, None}:
                raise
    print("PASS: v3 module tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
