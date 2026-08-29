#!/usr/bin/env python3
"""Unresolved-field UX report tests."""

from __future__ import annotations

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
from unresolved_field_reporter import render_unresolved_section  # noqa: E402


EXMP_PROMOTION = ROOT / "examples" / "xbrl_promotion_runs" / "EXMP"
EXMP_REVIEW = ROOT / "examples" / "xbrl_review_decisions" / "EXMP" / "normalized_review_batch.json"
EXMP_CANDIDATES = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP" / "extraction_candidates.json"
EXMP_MANIFEST = ROOT / "examples" / "xbrl_extraction_runs" / "EXMP" / "extraction_run_manifest.json"


def read_json(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def main() -> int:
    """Run unresolved UX tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-unresolved-ux-tests-") as temp_name:
        temp = Path(temp_name)
        promotion = temp / "promotion"
        shutil.copytree(EXMP_PROMOTION, promotion)
        review = temp / "review.json"
        candidates = temp / "candidates.json"
        manifest = temp / "manifest.json"
        shutil.copy2(EXMP_REVIEW, review)
        shutil.copy2(EXMP_CANDIDATES, candidates)
        shutil.copy2(EXMP_MANIFEST, manifest)
        run_generator(promotion, review, candidates, manifest, temp / "normalized")
        manifest_doc = read_json(temp / "normalized" / "normalized_csv_manifest.json")
        rendered = render_unresolved_section(manifest_doc)
        assert "Partial-Field and Unresolved-Field UX" in rendered
        assert "Populated fields" in rendered
        assert "Omitted fields" in rendered
        assert "Unresolved fields" in rendered
        assert "Available ratios" in rendered
        assert "Unavailable ratios" in rendered
        assert "never auto-filled with zero" in rendered
        assert "`total_debt`" in rendered
        report = (temp / "normalized" / "normalized_csv_report.md").read_text(encoding="utf-8")
        assert "Partial-Field and Unresolved-Field UX" in report
        assert "Unavailable ratios" in report

    print("PASS: unresolved-field UX renders populated, omitted, unresolved, downstream impact and no-zero-fill caution")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
