#!/usr/bin/env python3
"""Controlled SEC live ingestor for production research system."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence


SEC_HOSTS = {"www.sec.gov", "sec.gov", "www.sec.gov"}


@dataclass
class IngestionConfig:
    mode: str
    source_url: str
    user_agent: str
    timeout_seconds: float = 10.0
    max_requests: int = 1
    min_request_interval_seconds: float = 0.2
    max_response_bytes: int = 2_000_000
    retry_count: int = 1


def validate_sec_url(url: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in SEC_HOSTS:
        raise ValueError("Only SEC official HTTPS URLs are allowed.")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URL are not allowed.")
    return parsed


def validate_config(config: IngestionConfig) -> None:
    if config.mode not in {"fixture_mode", "live_mode_explicit_url"}:
        raise ValueError("mode must be fixture_mode or live_mode_explicit_url.")
    if config.mode == "live_mode_explicit_url":
        validate_sec_url(config.source_url)
        if not config.user_agent or "@" not in config.user_agent:
            raise ValueError("Explicit User-Agent with contact email is required.")
    if not 1 <= config.max_requests <= 3:
        raise ValueError("max_requests must be between 1 and 3.")
    if config.timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive.")
    if config.max_response_bytes <= 0:
        raise ValueError("max_response_bytes must be positive.")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_live(config: IngestionConfig, opener: Callable[[urllib.request.Request, float], bytes] | None = None) -> bytes:
    validate_config(config)
    request = urllib.request.Request(config.source_url, headers={"User-Agent": config.user_agent}, method="GET")
    getter = opener or (lambda req, timeout: urllib.request.urlopen(req, timeout=timeout).read(config.max_response_bytes + 1))
    last_error: Exception | None = None
    attempts = min(config.retry_count + 1, config.max_requests)
    for attempt in range(attempts):
        if attempt:
            time.sleep(config.min_request_interval_seconds)
        try:
            data = getter(request, config.timeout_seconds)
            if len(data) > config.max_response_bytes:
                raise ValueError("SEC response exceeds max_response_bytes.")
            return data
        except (TimeoutError, urllib.error.URLError, urllib.error.HTTPError, ValueError) as exc:
            last_error = exc
            if isinstance(exc, urllib.error.HTTPError) and exc.code not in {503, 429}:
                break
    raise ValueError(f"SEC ingestion failed: {last_error}")


def ingest_fixture(input_path: Path, output_dir: Path, source_url: str = "fixture://local") -> dict[str, str]:
    data = input_path.read_bytes()
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / input_path.name
    raw_path.write_bytes(data)
    manifest = {
        "ingestion_schema_version": "v1.2.0",
        "mode": "fixture_mode",
        "source_url": source_url,
        "raw_package": str(raw_path),
        "sha256": sha256_bytes(data),
        "financial_extraction_performed": "false",
    }
    (output_dir / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def ingest_live(config: IngestionConfig, output_dir: Path, opener: Callable[[urllib.request.Request, float], bytes] | None = None) -> dict[str, str]:
    data = fetch_live(config, opener=opener)
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_path = output_dir / "sec_filing_package.raw"
    raw_path.write_bytes(data)
    manifest = {
        "ingestion_schema_version": "v1.2.0",
        "mode": "live_mode_explicit_url",
        "source_url": config.source_url,
        "raw_package": str(raw_path),
        "sha256": sha256_bytes(data),
        "request_policy": "SEC-only GET explicit User-Agent bounded timeout/count/size",
        "financial_extraction_performed": "false",
    }
    (output_dir / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Controlled SEC ingestion.")
    parser.add_argument("--mode", choices=["fixture_mode", "live_mode_explicit_url"], required=True)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--source-url", default="")
    parser.add_argument("--user-agent", default="")
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.mode == "fixture_mode":
        if not args.input:
            raise SystemExit("--input is required for fixture_mode")
        ingest_fixture(args.input, args.output_dir, args.source_url or "fixture://local")
    else:
        config = IngestionConfig(mode=args.mode, source_url=args.source_url, user_agent=args.user_agent)
        ingest_live(config, args.output_dir)
    print("PASS: SEC ingestion")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
