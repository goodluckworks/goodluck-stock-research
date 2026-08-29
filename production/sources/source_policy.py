#!/usr/bin/env python3
"""Source policy for live production research sources."""

from __future__ import annotations

from urllib.parse import urlparse


ALLOWED_SEC_HOSTS = {"www.sec.gov", "sec.gov", "data.sec.gov"}
ALLOWED_IR_HOST_SUFFIXES = (".com", ".net", ".org")
ALLOWED_MARKET_HOSTS = {"query1.finance.yahoo.com", "finance.yahoo.com", "companiesmarketcap.com"}


def validate_https_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Only HTTPS URLs with a hostname are allowed.")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URLs are not allowed.")


def validate_sec_source(url: str) -> None:
    validate_https_url(url)
    if urlparse(url).hostname not in ALLOWED_SEC_HOSTS:
        raise ValueError("SEC source must be an allowlisted SEC host.")


def validate_company_ir_source(url: str) -> None:
    validate_https_url(url)
    host = urlparse(url).hostname or ""
    if host in ALLOWED_SEC_HOSTS or not host.endswith(ALLOWED_IR_HOST_SUFFIXES):
        raise ValueError("Company IR source must be an explicit company HTTPS source.")


def validate_market_data_source(url: str) -> None:
    validate_https_url(url)
    if urlparse(url).hostname not in ALLOWED_MARKET_HOSTS:
        raise ValueError("Market data source is not allowlisted.")


def assert_no_forbidden_payload(payload: dict[str, object]) -> None:
    text = str(payload).lower()
    for term in ("api_key", "password", "secret", "broker.connect", "place_order", "execute_trade"):
        if term in text:
            raise ValueError(f"Forbidden source payload term: {term}")
