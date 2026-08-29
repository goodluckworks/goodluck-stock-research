#!/usr/bin/env python3
"""SEC source adapter wrapper."""

from __future__ import annotations

import urllib.request
from typing import Callable, Any

from source_manifest import build_manifest
from source_policy import validate_sec_source


def fetch_sec_metadata(url: str, user_agent: str, opener: Callable[[urllib.request.Request, float], bytes], timeout_seconds: float = 10.0) -> dict[str, Any]:
    validate_sec_source(url)
    if not user_agent or "@" not in user_agent:
        raise ValueError("SEC source requires explicit User-Agent with contact email.")
    request = urllib.request.Request(url, headers={"User-Agent": user_agent}, method="GET")
    data = opener(request, timeout_seconds)
    payload = data.decode("utf-8", errors="replace")
    return {"payload": payload, "manifest": build_manifest("sec", url, payload, "primary_official", "available")}
