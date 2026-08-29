#!/usr/bin/env python3
"""v0.2 ratio dry-run wrapper tests for fictional sandbox CSV only."""

from __future__ import annotations

import csv
import json
import shutil
import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
ROOT = XBRL_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from generate_normalized_csv_sandbox import run_generator  # noqa: E402
from run_v02_sandbox_dry_run import run_dry_run  # noqa: E402


EXMP_PROMOTION = ROOT / "examples" / "xbrl_promotion_runs" / "EXMP"
EXMP_REVIEW = ROOT / "examples" / "xbrl_review_decisions" / "EXMP" / "normalized_review_batch.json"
EXMP_CANDIDATES = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP" / "extraction_candidates.json"
EXMP_MANIFEST = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP" / "extraction_run_manifest.json"


def read_json(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write_json(path: Path, value: object) -> None:
    """Write JSON object."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    """Write CSV rows preserving existing field names."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        fieldnames = list(csv.DictReader(handle).fieldnames or [])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read CSV rows."""
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def copy_inputs(root: Path) -> tuple[Path, Path, Path, Path]:
    """Copy EXMP source packages to a temporary root."""
    promotion = root / "promotion"
    shutil.copytree(EXMP_PROMOTION, promotion)
    review = root / "review.json"
    candidates = root / "candidates.json"
    manifest = root / "manifest.json"
    shutil.copy2(EXMP_REVIEW, review)
    shutil.copy2(EXMP_CANDIDATES, candidates)
    shutil.copy2(EXMP_MANIFEST, manifest)
    return promotion, review, candidates, manifest


def expect_failure(input_csv: Path, output_dir: Path, expected: str) -> None:
    """Assert dry-run failure includes expected text."""
    try:
        run_dry_run(input_csv, output_dir)
    except (ValueError, FileNotFoundError, FileExistsError) as exc:
        assert expected in str(exc), str(exc)
    else:
        raise AssertionError(f"Expected dry-run failure containing {expected!r}")


def main() -> int:
    """Run v0.2 dry-run wrapper tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-v02-dry-run-tests-") as temp_name:
        temp = Path(temp_name)
        promotion, review, candidates, manifest = copy_inputs(temp)
        normalized = temp / "normalized"
        run_generator(promotion, review, candidates, manifest, normalized)
        input_csv = normalized / "normalized_financials_sandbox.csv"
        output = temp / "dry-run"
        paths = run_dry_run(input_csv, output)

        assert set(paths) == {
            "ratio_output_sandbox.md",
            "v02_dry_run_manifest.json",
            "v02_dry_run_report.md",
        }
        assert all(path.is_file() and path.stat().st_size > 0 for path in paths.values())
        dry_manifest = read_json(output / "v02_dry_run_manifest.json")
        assert dry_manifest["script"] == "ratio_calculator.py"
        assert dry_manifest["sandbox_status"] == "fictional_sandbox_not_investment_data"
        assert dry_manifest["no_investment_conclusion"] is True
        report = (output / "ratio_output_sandbox.md").read_text(encoding="utf-8")
        assert "Sandbox Ratio Dry-Run Banner" in report
        assert "# Financial Ratio Calculation" in report
        lowered = report.lower()
        for forbidden in ("target price:", "buy:", "sell:", "hold:", "position size:", "research status:"):
            assert forbidden not in lowered

        source = (XBRL_DIR / "run_v02_sandbox_dry_run.py").read_text(encoding="utf-8")
        assert "subprocess" not in source
        for script_name in ("dcf_sensitivity", "peer_comps_table", "implied_expectations"):
            assert script_name not in source

        for ticker in ("MRVL", "NVDA", "AVGO"):
            real_dir = temp / f"{ticker}-blocked"
            shutil.copytree(normalized, real_dir)
            manifest_doc = read_json(real_dir / "normalized_csv_manifest.json")
            manifest_doc["ticker"] = ticker
            write_json(real_dir / "normalized_csv_manifest.json", manifest_doc)
            expect_failure(real_dir / "normalized_financials_sandbox.csv", temp / f"{ticker}-out", "allows only EXMP")

        nonsandbox = temp / "nonsandbox"
        shutil.copytree(normalized, nonsandbox)
        rows = read_csv_rows(nonsandbox / "normalized_financials_sandbox.csv")
        rows[0]["sandbox_status"] = "ordinary_csv"
        write_csv(nonsandbox / "normalized_financials_sandbox.csv", rows)
        expect_failure(nonsandbox / "normalized_financials_sandbox.csv", temp / "nonsandbox-out", "sandbox_status")

        no_manifest = temp / "missing-manifest"
        shutil.copytree(normalized, no_manifest)
        (no_manifest / "normalized_csv_manifest.json").unlink()
        expect_failure(no_manifest / "normalized_financials_sandbox.csv", temp / "missing-out", "Input file does not exist")

    print("PASS: EXMP sandbox ratio dry-run, banner, manifest, real-ticker and non-sandbox blocks, no DCF/peer/implied calls")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
