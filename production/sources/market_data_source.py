#!/usr/bin/env python3
"""Controlled market data source adapter."""

from __future__ import annotations

import csv
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any

from source_manifest import build_manifest
from source_policy import validate_market_data_source


@dataclass
class MarketDataConfig:
    mode: str
    source: str
    timeout_seconds: float = 10.0
    max_response_bytes: int = 500_000


def load_user_csv(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Market data CSV not found: {path}")
    rows = list(csv.DictReader(path.read_text(encoding="utf-8").splitlines()))
    required = {"ticker", "price", "currency", "timestamp", "market_session", "source_status"}
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise ValueError(f"Market data CSV missing fields: {sorted(missing)}")
    payload = path.read_text(encoding="utf-8")
    return {"rows": rows, "manifest": build_manifest("market_data_csv", str(path), payload, "user_provided", "available")}


def fetch_mockable_market_data(config: MarketDataConfig, opener: Callable[[urllib.request.Request, float], bytes]) -> dict[str, Any]:
    if config.mode != "mocked_live":
        raise ValueError("Only mocked_live is supported for no-key public source tests.")
    validate_market_data_source(config.source)
    request = urllib.request.Request(config.source, headers={"User-Agent": "goodluck-stock-research/3.0 research@example.com"}, method="GET")
    data = opener(request, config.timeout_seconds)
    if len(data) > config.max_response_bytes:
        raise ValueError("Market data response exceeds max_response_bytes.")
    payload = data.decode("utf-8", errors="replace")
    return {"rows": [], "manifest": build_manifest("market_data_mocked_live", config.source, payload, "indicative", "available")}


def insufficient_market_data(reason: str) -> dict[str, Any]:
    return {
        "rows": [],
        "manifest": build_manifest("market_data", "none", reason, "unavailable", "insufficient_market_data"),
        "caveat": reason,
    }
