#!/usr/bin/env python3
"""Live source registry for production research workflows."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from market_data_source import insufficient_market_data, load_user_csv
from source_manifest import write_manifest
from source_policy import assert_no_forbidden_payload


SUPPORTED_SOURCE_TYPES = {"sec", "company_ir", "market_data", "market_data_csv", "market_data_mocked_live"}


def register_source(source_type: str, source: str, manifest: dict[str, Any]) -> dict[str, Any]:
    if source_type not in SUPPORTED_SOURCE_TYPES:
        raise ValueError(f"Unsupported source type: {source_type}")
    assert_no_forbidden_payload(manifest)
    return {
        "registry_schema_version": "v2.1.0",
        "source_type": source_type,
        "source": source,
        "manifest": manifest,
        "source_reliability_score": reliability_score(manifest),
    }


def reliability_score(manifest: dict[str, Any]) -> float:
    reliability = manifest.get("reliability")
    if reliability == "primary_official":
        return 0.95
    if reliability == "company_official":
        return 0.85
    if reliability == "user_provided":
        return 0.75
    if reliability == "indicative":
        return 0.55
    return 0.0


def resolve_market_data(csv_path: Path | None) -> dict[str, Any]:
    if csv_path:
        result = load_user_csv(csv_path)
    else:
        result = insufficient_market_data("No user CSV or reliable no-key source was provided.")
    return register_source(result["manifest"]["source_type"], result["manifest"]["source"], result["manifest"])


def write_registered_manifest(registry_entry: dict[str, Any], output_path: Path) -> None:
    write_manifest(registry_entry, output_path)
