#!/usr/bin/env python3
"""Resolve filing identity from source metadata."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ACCESSION_RE = re.compile(r"(\d{10}-\d{2}-\d{6})")


def resolve_identity(source_manifest: dict[str, Any], *, ticker: str, cik: str, form: str, filing_date: str) -> dict[str, Any]:
    url = str(source_manifest.get("source_url", ""))
    match = ACCESSION_RE.search(url)
    accession = match.group(1) if match else "unknown"
    identity = {
        "identity_schema_version": "v1.2.0",
        "ticker": ticker.upper(),
        "cik": cik,
        "accession": accession,
        "form": form,
        "filing_date": filing_date,
        "source_url": url,
        "snapshot_sha256": source_manifest.get("sha256"),
        "latest_effective_claim": False,
        "financial_extraction_performed": False,
    }
    return identity


def write_identity(path: Path, identity: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(identity, indent=2) + "\n", encoding="utf-8")
