#!/usr/bin/env python3
"""Tests for controlled SEC ingestion."""

from pathlib import Path
import tempfile
import urllib.error
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "goodluck-stock-research" / "production" / "ingestion"))

import sec_live_ingestor


def main() -> int:
    fixture = ROOT / "goodluck-stock-research" / "xbrl" / "fixtures" / "real_excerpt_drills" / "mrvl_10k_excerpt_inline_like.html"
    with tempfile.TemporaryDirectory() as tmp:
        manifest = sec_live_ingestor.ingest_fixture(fixture, Path(tmp))
        assert manifest["financial_extraction_performed"] == "false"
        config = sec_live_ingestor.IngestionConfig(
            mode="live_mode_explicit_url",
            source_url="https://www.sec.gov/Archives/edgar/data/1835632/0001835632-26-000011.txt",
            user_agent="Research Test contact@example.com",
            max_response_bytes=20,
        )
        live = sec_live_ingestor.ingest_live(config, Path(tmp) / "live", opener=lambda req, timeout: b"fixture")
        assert live["mode"] == "live_mode_explicit_url"
        for bad in ("https://example.com/file.txt", "http://www.sec.gov/file.txt"):
            try:
                sec_live_ingestor.validate_sec_url(bad)
                raise AssertionError("bad URL accepted")
            except ValueError:
                pass
        try:
            sec_live_ingestor.fetch_live(sec_live_ingestor.IngestionConfig("live_mode_explicit_url", config.source_url, ""))
            raise AssertionError("missing User-Agent accepted")
        except ValueError:
            pass
        try:
            sec_live_ingestor.fetch_live(config, opener=lambda req, timeout: b"x" * 25)
            raise AssertionError("oversized response accepted")
        except ValueError:
            pass
        try:
            sec_live_ingestor.fetch_live(config, opener=lambda req, timeout: (_ for _ in ()).throw(urllib.error.HTTPError(req.full_url, 404, "not found", {}, None)))
            raise AssertionError("404 accepted")
        except ValueError:
            pass
    print("PASS: live SEC ingestion tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
