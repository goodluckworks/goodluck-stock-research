#!/usr/bin/env python3
"""Amendment and restatement status discovery from local metadata lists."""

from __future__ import annotations

from typing import Any


def discover(identity: dict[str, Any], filings: list[dict[str, Any]]) -> dict[str, Any]:
    """Return amendment status from provided metadata.

    This function does not crawl SEC. It only evaluates supplied metadata.
    """
    accession = identity.get("accession")
    amendments = [item for item in filings if item.get("amends_accession") == accession or str(item.get("form", "")).endswith("/A")]
    restatements = [item for item in filings if item.get("restatement") is True]
    return {
        "amendment_schema_version": "v1.2.0",
        "accession": accession,
        "amendment_found": bool(amendments),
        "restatement_found": bool(restatements),
        "latest_effective_established": not amendments,
        "requires_review": bool(amendments or restatements),
    }
