#!/usr/bin/env python3
"""Review quality scoring tests."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path


TEST_DIR = Path(__file__).resolve().parent
XBRL_DIR = TEST_DIR.parent
ROOT = XBRL_DIR.parent
sys.path.insert(0, str(XBRL_DIR))

from review_quality_scorer import run_scorer  # noqa: E402


EXAMPLES = ROOT / "examples" / "xbrl_extraction_runs"


def read(path: Path) -> dict[str, object]:
    """Read JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def write(path: Path, value: object) -> None:
    """Write JSON."""
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def score(temp: Path, extraction_dir: Path, label: str) -> dict[str, object]:
    """Run scorer and return score package."""
    out = temp / label
    run_scorer(
        extraction_dir / "extraction_candidates.json",
        extraction_dir / "extraction_run_manifest.json",
        extraction_dir / "field_provenance.json",
        out,
    )
    report = (out / "review_quality_report.md").read_text(encoding="utf-8").lower()
    assert "scores are reviewer aids only" in report
    assert "no investment conclusion" in report
    return read(out / "review_quality_score.json")


def main() -> int:
    """Run review quality tests."""
    with tempfile.TemporaryDirectory(prefix="xbrl-review-quality-tests-") as temp_name:
        temp = Path(temp_name)
        exmp_quality = score(temp, EXAMPLES / "EXMP", "exmp-quality")
        assert {record["approval_readiness"] for record in exmp_quality["records"]} == {"ready"}
        assert all(not record["blocking_issues"] for record in exmp_quality["records"])

        mrvl_quality = score(temp, EXAMPLES / "MRVL", "mrvl-quality")
        assert "needs_review" in {record["approval_readiness"] for record in mrvl_quality["records"]}
        assert mrvl_quality["fictional_company"] is False

        candidates = read(EXAMPLES / "EXMP" / "extraction_candidates.json")
        missing_relationship = copy.deepcopy(candidates)
        del missing_relationship["candidates"][0]["taxonomy_relationship"]
        missing_path = temp / "missing-relationship.json"
        write(missing_path, missing_relationship)
        missing_out = temp / "missing-relationship-quality"
        run_scorer(
            missing_path,
            EXAMPLES / "EXMP" / "extraction_run_manifest.json",
            EXAMPLES / "EXMP" / "field_provenance.json",
            missing_out,
        )
        missing_quality = read(missing_out / "review_quality_score.json")
        assert missing_quality["records"][0]["approval_readiness"] == "not_ready"
        assert "missing_relationship_evidence" in missing_quality["records"][0]["blocking_issues"]

        provenance = read(EXAMPLES / "EXMP" / "field_provenance.json")
        provenance["records"] = provenance["records"][1:]
        bad_provenance = temp / "bad-provenance.json"
        write(bad_provenance, provenance)
        missing_prov_out = temp / "missing-provenance-quality"
        run_scorer(
            EXAMPLES / "EXMP" / "extraction_candidates.json",
            EXAMPLES / "EXMP" / "extraction_run_manifest.json",
            bad_provenance,
            missing_prov_out,
        )
        missing_prov = read(missing_prov_out / "review_quality_score.json")
        assert missing_prov["records"][0]["approval_readiness"] == "not_ready"
        assert "missing_provenance" in missing_prov["records"][0]["blocking_issues"]

    print("PASS: review quality ready, real-fixture needs_review, missing relationship and missing provenance cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
