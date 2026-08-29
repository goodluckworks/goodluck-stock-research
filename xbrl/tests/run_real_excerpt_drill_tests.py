#!/usr/bin/env python3
"""Real-filing-excerpt offline drill tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
XBRL_DIR = ROOT / "xbrl"
DRILL_FIXTURES = XBRL_DIR / "fixtures" / "real_excerpt_drills"
DRILL_EXAMPLES = ROOT / "examples" / "xbrl_real_excerpt_drills"
TICKERS = ("MRVL", "NVDA", "AVGO")


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def main() -> int:
    """Run real excerpt drill tests."""
    expected = read(DRILL_FIXTURES / "expected_drill_behavior.json")

    for ticker in TICKERS:
        assert expected[ticker]["promotion_allowed"] is False
        fixture_matches = list(DRILL_FIXTURES.glob(f"{ticker.lower()}_*_excerpt_inline_like.html"))
        assert fixture_matches, ticker
        fixture_text = fixture_matches[0].read_text(encoding="utf-8").lower()
        assert "excerpt only" in fixture_text
        assert "not complete filing" in fixture_text or "not a complete filing" in fixture_text
        assert fixture_matches[0].stat().st_size < 20000

        root = DRILL_EXAMPLES / ticker
        extraction = root / "extraction"
        workbench = root / "workbench" / "review_workbench.md"
        quality = root / "quality" / "review_quality_score.json"
        for required in (
            extraction / "extraction_candidates.json",
            extraction / "extraction_run_manifest.json",
            extraction / "field_provenance.json",
            extraction / "unresolved_fields.json",
            workbench,
            quality,
        ):
            assert required.is_file() and required.stat().st_size > 0, required

        manifest = read(extraction / "extraction_run_manifest.json")
        candidates = read(extraction / "extraction_candidates.json")
        quality_doc = read(quality)
        workbench_text = workbench.read_text(encoding="utf-8").lower()
        assert manifest["ticker"] == ticker
        assert manifest["fixture_data_status"] == "real_filing_excerpt_drill"
        assert "real filing excerpt drill" in workbench_text
        assert "not a complete filing" in workbench_text
        assert "no approved values" in workbench_text
        assert all(candidate["review_status"] == "draft_extracted_unreviewed" for candidate in candidates["candidates"])
        assert quality_doc["ticker"] == ticker
        assert not (root / "promotion").exists()
        assert not (root / "approved_normalized_draft.json").exists()

    print("PASS: MRVL/NVDA/AVGO real excerpt drills stay short, offline, draft-only and unpromoted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
