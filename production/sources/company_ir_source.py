#!/usr/bin/env python3
"""Controlled company investor-relations source adapter."""

from __future__ import annotations

import urllib.request
from typing import Callable, Any

from source_manifest import build_manifest
from source_policy import validate_company_ir_source


def fetch_company_ir(url: str, opener: Callable[[urllib.request.Request, float], bytes], timeout_seconds: float = 10.0, max_response_bytes: int = 750_000) -> dict[str, Any]:
    validate_company_ir_source(url)
    request = urllib.request.Request(url, headers={"User-Agent": "goodluck-stock-research/3.0 research@example.com"}, method="GET")
    data = opener(request, timeout_seconds)
    if len(data) > max_response_bytes:
        raise ValueError("Company IR response exceeds max_response_bytes.")
    payload = data.decode("utf-8", errors="replace")
    return {"payload": payload, "manifest": build_manifest("company_ir", url, payload, "company_official", "available")}
