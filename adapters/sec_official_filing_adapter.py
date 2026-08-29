#!/usr/bin/env python3
"""Package one explicit SEC official filing URL or local fixture as evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence


ADAPTER_NAME = "sec_official_filing_adapter"
ADAPTER_VERSION = "v0.3.2"
ALLOWED_HOSTS = {"sec.gov", "www.sec.gov", "data.sec.gov"}
SOURCE_STATUSES = {
    "verified",
    "partially_verified",
    "indicative",
    "unverified",
    "fictional_sample",
}
DATA_STATUSES = {
    "available",
    "partial",
    "stale",
    "conflicting",
    "superseded",
    "missing",
    "not_applicable",
}
RETRYABLE_HTTP_STATUSES = {429, 500, 502, 503, 504}
UNRESOLVED_FINANCIAL_FIELDS = (
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "total_debt",
    "diluted_shares",
)


@dataclass(frozen=True)
class AdapterConfig:
    """SEC adapter inputs."""

    mode: str
    company: str
    ticker: str
    cik: str
    form_type: str
    accession: str
    filing_date: str
    reporting_period: str
    fiscal_year: str
    fiscal_quarter: str
    source_url: str
    currency: str
    amount_unit: str
    per_share_unit: str
    user_agent: str
    output_dir: Path
    input_file: Path | None = None
    source_status: str = "verified"
    data_status: str = "available"
    retrieved_at: str = ""
    notes: str = "none"
    timeout: float = 15.0
    min_request_interval: float = 0.5
    max_requests: int = 3
    max_bytes: int = 25_000_000
    overwrite: bool = False


@dataclass(frozen=True)
class FetchResponse:
    """One bounded HTTP response."""

    body: bytes
    status: int
    final_url: str
    content_type: str
    retrieved_at: str


class FetchFailure(Exception):
    """Structured fetch failure."""

    def __init__(
        self,
        code: str,
        message: str,
        request_count: int,
        http_status: int | str = "",
        retrieved_at: str = "",
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.request_count = request_count
        self.http_status = http_status
        self.retrieved_at = retrieved_at or utc_now()


Fetcher = Callable[[str, str, float, int], FetchResponse]
Sleeper = Callable[[float], None]


def utc_now() -> str:
    """Return an ISO 8601 UTC timestamp."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def require_text(name: str, value: str) -> str:
    """Require nonblank text."""
    stripped = value.strip()
    if not stripped:
        raise ValueError(f"{name} must not be blank.")
    return stripped


def parse_timestamp(value: str) -> str:
    """Validate a timezone-aware ISO timestamp."""
    candidate = value or utc_now()
    try:
        parsed = datetime.fromisoformat(candidate.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Invalid retrieved_at: {candidate!r}.") from exc
    if parsed.tzinfo is None:
        raise ValueError("retrieved_at must include timezone information.")
    return candidate


def safe_id(value: str) -> str:
    """Create a stable identifier component."""
    cleaned = "".join(
        character.lower() if character.isalnum() else "-"
        for character in value.strip()
    )
    return "-".join(part for part in cleaned.split("-") if part) or "unknown"


def display_path(path: Path | None) -> str:
    """Prefer a cwd-relative path."""
    if path is None:
        return "not_applicable"
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(resolved)


def write_json(path: Path, payload: object) -> None:
    """Write deterministic JSON."""
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def validate_sec_url(url: str) -> urllib.parse.ParseResult:
    """Validate an HTTPS SEC official URL."""
    parsed = urllib.parse.urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or host not in ALLOWED_HOSTS:
        raise ValueError(
            "source_url must use HTTPS and an exact SEC host: "
            "sec.gov, www.sec.gov, or data.sec.gov."
        )
    if parsed.username or parsed.password or parsed.port not in {None, 443}:
        raise ValueError("source_url must not contain credentials or a custom port.")
    return parsed


def validate_archive_identity(
    parsed: urllib.parse.ParseResult, cik: str, accession: str
) -> None:
    """Check archive URLs against user-supplied CIK/accession where applicable."""
    if "/Archives/edgar/data/" not in parsed.path:
        return
    expected = f"/Archives/edgar/data/{int(cik)}/{accession.replace('-', '')}/"
    if expected not in parsed.path:
        raise ValueError(
            "SEC Archives URL does not match the supplied CIK/accession path."
        )


def validate_config(config: AdapterConfig) -> AdapterConfig:
    """Validate fixture/live boundaries."""
    mode = require_text("mode", config.mode).lower()
    if mode not in {"fixture", "live"}:
        raise ValueError("mode must be 'fixture' or 'live'.")
    required = {
        "company": config.company,
        "ticker": config.ticker,
        "cik": config.cik,
        "form_type": config.form_type,
        "accession": config.accession,
        "filing_date": config.filing_date,
        "reporting_period": config.reporting_period,
        "fiscal_year": config.fiscal_year,
        "fiscal_quarter": config.fiscal_quarter,
        "source_url": config.source_url,
        "currency": config.currency,
        "amount_unit": config.amount_unit,
        "per_share_unit": config.per_share_unit,
        "source_status": config.source_status,
        "data_status": config.data_status,
    }
    cleaned = {name: require_text(name, value) for name, value in required.items()}
    if not cleaned["cik"].isdigit():
        raise ValueError("cik must contain digits only.")
    if not re.fullmatch(r"\d{10}-\d{2}-\d{6}", cleaned["accession"]):
        raise ValueError("accession must match ##########-##-######.")
    parsed = validate_sec_url(cleaned["source_url"])
    validate_archive_identity(parsed, cleaned["cik"], cleaned["accession"])
    if cleaned["source_status"] not in SOURCE_STATUSES:
        raise ValueError(f"Unsupported source_status: {cleaned['source_status']!r}.")
    if cleaned["data_status"] not in DATA_STATUSES:
        raise ValueError(f"Unsupported data_status: {cleaned['data_status']!r}.")
    if not 1 <= config.max_requests <= 3:
        raise ValueError("max_requests must be between 1 and 3.")
    if config.min_request_interval < 0.2:
        raise ValueError("min_request_interval must be at least 0.2 seconds.")
    if not 1 <= config.timeout <= 60:
        raise ValueError("timeout must be between 1 and 60 seconds.")
    if not 1 <= config.max_bytes <= 100_000_000:
        raise ValueError("max_bytes must be between 1 and 100,000,000.")

    input_file = (
        config.input_file.expanduser().resolve()
        if config.input_file is not None
        else None
    )
    output_dir = config.output_dir.expanduser().resolve()
    if mode == "fixture":
        if input_file is None or not input_file.is_file():
            raise FileNotFoundError("fixture mode requires an existing --input-file.")
        if output_dir == input_file:
            raise ValueError("output_dir cannot equal input_file.")
    elif input_file is not None:
        raise ValueError("live mode does not accept --input-file.")

    user_agent = config.user_agent.strip()
    has_contact = bool(
        re.search(r"[^@\s]+@[^@\s]+\.[^@\s]+", user_agent)
        or re.search(r"https?://\S+", user_agent, flags=re.IGNORECASE)
    )
    if mode == "live" and (
        len(user_agent) < 8
        or " " not in user_agent
        or not has_contact
    ):
        raise ValueError(
            "live mode requires a clear --user-agent with identity and contact "
            "information."
        )

    return AdapterConfig(
        mode=mode,
        company=cleaned["company"],
        ticker=cleaned["ticker"].upper(),
        cik=cleaned["cik"].zfill(10),
        form_type=cleaned["form_type"].upper(),
        accession=cleaned["accession"],
        filing_date=cleaned["filing_date"],
        reporting_period=cleaned["reporting_period"],
        fiscal_year=cleaned["fiscal_year"],
        fiscal_quarter=cleaned["fiscal_quarter"],
        source_url=cleaned["source_url"],
        currency=cleaned["currency"],
        amount_unit=cleaned["amount_unit"],
        per_share_unit=cleaned["per_share_unit"],
        user_agent=user_agent,
        output_dir=output_dir,
        input_file=input_file,
        source_status=cleaned["source_status"],
        data_status=cleaned["data_status"],
        retrieved_at=parse_timestamp(config.retrieved_at),
        notes=config.notes.strip() or "none",
        timeout=config.timeout,
        min_request_interval=config.min_request_interval,
        max_requests=config.max_requests,
        max_bytes=config.max_bytes,
        overwrite=config.overwrite,
    )


def prepare_output_dir(config: AdapterConfig) -> bool:
    """Enforce no-silent-overwrite."""
    existing = list(config.output_dir.iterdir()) if config.output_dir.is_dir() else []
    if existing and not config.overwrite:
        raise FileExistsError(
            f"Output directory is not empty: {config.output_dir}. Use --overwrite."
        )
    config.output_dir.mkdir(parents=True, exist_ok=True)
    return bool(existing and config.overwrite)


class SECOnlyRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Block redirects away from SEC official hosts."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        validate_sec_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def default_fetch(url: str, user_agent: str, timeout: float, max_bytes: int) -> FetchResponse:
    """Perform one bounded SEC-only GET."""
    validate_sec_url(url)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/json",
        },
        method="GET",
    )
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}),
        SECOnlyRedirectHandler(),
    )
    with opener.open(request, timeout=timeout) as response:
        final_url = response.geturl()
        validate_sec_url(final_url)
        status = int(getattr(response, "status", response.getcode()))
        body = response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise FetchFailure(
                "response_too_large",
                f"SEC response exceeded max_bytes={max_bytes}.",
                request_count=1,
                http_status=status,
            )
        return FetchResponse(
            body=body,
            status=status,
            final_url=final_url,
            content_type=response.headers.get_content_type(),
            retrieved_at=utc_now(),
        )


def fetch_with_retries(
    config: AdapterConfig,
    fetcher: Fetcher,
    sleeper: Sleeper,
) -> tuple[FetchResponse, int]:
    """Fetch with bounded retries and conservative spacing."""
    last_failure: FetchFailure | None = None
    for attempt in range(1, config.max_requests + 1):
        if attempt > 1:
            sleeper(config.min_request_interval)
        try:
            response = fetcher(
                config.source_url,
                config.user_agent,
                config.timeout,
                config.max_bytes,
            )
            if 200 <= response.status < 300:
                return response, attempt
            failure = FetchFailure(
                "http_error",
                f"SEC returned HTTP {response.status}.",
                attempt,
                response.status,
                response.retrieved_at,
            )
        except FetchFailure as exc:
            failure = FetchFailure(
                exc.code,
                exc.message,
                attempt,
                exc.http_status,
                exc.retrieved_at,
            )
        except urllib.error.HTTPError as exc:
            failure = FetchFailure(
                "http_error",
                f"SEC returned HTTP {exc.code}.",
                attempt,
                exc.code,
            )
        except (TimeoutError, urllib.error.URLError) as exc:
            failure = FetchFailure("network_error", str(exc), attempt)

        last_failure = failure
        retryable = (
            failure.code == "network_error"
            or failure.http_status in RETRYABLE_HTTP_STATUSES
        )
        if not retryable:
            break
    assert last_failure is not None
    raise last_failure


def sha256_bytes(value: bytes) -> str:
    """Hash bytes."""
    return hashlib.sha256(value).hexdigest()


def build_unresolved_fields() -> list[dict[str, str]]:
    """Return intentionally unresolved financial fields."""
    return [
        {
            "field_name": field,
            "reason": (
                "v0.3.2 packages official evidence only and does not perform "
                "financial extraction"
            ),
            "required_for": "financials_input_schema and downstream research",
            "severity": "blocking_for_normalized_financials",
            "suggested_manual_action": (
                "Manually normalize the field or use a separately approved "
                "extraction adapter."
            ),
        }
        for field in UNRESOLVED_FINANCIAL_FIELDS
    ]


def output_paths(output_dir: Path) -> dict[str, Path]:
    """Return required output paths."""
    return {
        name: output_dir / name
        for name in (
            "raw_snapshot_manifest.json",
            "source_manifest.json",
            "field_provenance.json",
            "unresolved_fields.json",
            "normalized_input_draft.json",
            "adapter_run_report.md",
        )
    }


def masked_user_agent_status(config: AdapterConfig) -> str:
    """Report only whether a User-Agent was supplied."""
    return "Yes" if bool(config.user_agent) else "No"


def write_package(
    config: AdapterConfig,
    overwrite_used: bool,
    body: bytes | None,
    http_status: int | str,
    request_count: int,
    retrieved_at: str,
    content_type: str,
    final_url: str,
    error: FetchFailure | None = None,
) -> dict[str, Path]:
    """Write a success or structured failure evidence package."""
    paths = output_paths(config.output_dir)
    accession_id = config.accession.replace("-", "")
    source_id = (
        f"{safe_id(config.ticker)}-{safe_id(config.form_type)}-"
        f"{safe_id(config.accession)}"
    )
    checksum = sha256_bytes(body) if body is not None else ""
    snapshot_id = f"raw-{source_id}-{checksum[:12]}" if checksum else ""
    snapshot_path: Path | None = None
    if body is not None:
        raw_dir = config.output_dir / "raw"
        raw_dir.mkdir(exist_ok=True)
        suffix = Path(urllib.parse.urlparse(final_url).path).suffix or ".html"
        snapshot_path = raw_dir / f"{snapshot_id}{suffix}"
        if not snapshot_path.exists():
            snapshot_path.write_bytes(body)
        elif sha256_bytes(snapshot_path.read_bytes()) != checksum:
            raise ValueError(f"Raw snapshot checksum mismatch: {snapshot_path}")

    is_amendment = config.form_type.endswith("/A")
    raw_manifest = {
        "snapshot_id": snapshot_id,
        "adapter_name": ADAPTER_NAME,
        "adapter_version": ADAPTER_VERSION,
        "mode": config.mode,
        "input_file": display_path(config.input_file),
        "source_url": config.source_url,
        "final_url": final_url,
        "raw_snapshot_path": display_path(snapshot_path),
        "sha256": checksum,
        "created_at": utc_now(),
        "retrieved_at": retrieved_at,
        "http_status": http_status,
        "sec_domain_validated": True,
        "immutable": True,
        "overwrite_used": overwrite_used,
        "request_count": request_count,
        "content_type": content_type,
        "byte_size": len(body) if body is not None else 0,
        "notes": config.notes,
    }
    source_manifest = {
        "source_id": source_id,
        "source_name": f"{config.company} {config.form_type} {config.reporting_period}",
        "source_type": "official_filing",
        "source_url": config.source_url,
        "retrieved_at": retrieved_at,
        "source_date": config.filing_date,
        "filing_date": config.filing_date,
        "form_type": config.form_type,
        "accession": config.accession,
        "cik": config.cik,
        "ticker": config.ticker,
        "company": config.company,
        "reporting_period": config.reporting_period,
        "fiscal_year": config.fiscal_year,
        "fiscal_quarter": config.fiscal_quarter,
        "currency": config.currency,
        "amount_unit": config.amount_unit,
        "per_share_unit": config.per_share_unit,
        "source_status": config.source_status if body is not None else "unverified",
        "data_status": config.data_status if body is not None else "missing",
        "confidence": "high" if config.mode == "live" and body is not None else "medium",
        "verification_basis": (
            "sec_https_get_and_sha256"
            if config.mode == "live" and body is not None
            else "local_fixture_and_sha256"
            if body is not None
            else "fetch_failed_no_raw_snapshot"
        ),
        "is_amendment": is_amendment,
        "latest_effective_status": "user_specified_not_independently_discovered",
        "transformation_notes": (
            "Official filing document downloaded or fixture copied; checksum "
            "recorded; no financial extraction performed."
        ),
        "notes": config.notes,
    }
    provenance = {
        "records": (
            [
                {
                    "field_name": "raw_filing_text",
                    "value_status": "raw_snapshot_available",
                    "source_id": source_id,
                    "source_field_name": "full filing text / SEC filing document",
                    "source_locator": display_path(snapshot_path),
                    "transformation": (
                        "official filing document downloaded or fixture copied; "
                        "checksum recorded"
                    ),
                    "confidence": "high",
                    "notes": "No financial field was inferred from the filing text.",
                }
            ]
            if body is not None
            else []
        )
    }
    errors = (
        [
            {
                "code": error.code,
                "severity": "blocking",
                "stage": "retrieval",
                "message": error.message,
                "source_id": source_id,
                "affected_fields": list(UNRESOLVED_FINANCIAL_FIELDS),
                "retryable": (
                    error.code == "network_error"
                    or error.http_status in RETRYABLE_HTTP_STATUSES
                ),
                "recommended_action": "Review URL/access and rerun explicitly.",
            }
        ]
        if error is not None
        else []
    )
    unresolved = {
        "unresolved_fields": build_unresolved_fields(),
        "warnings": [
            "No financial or XBRL extraction was performed.",
            (
                "The adapter does not discover newer amendments or determine that "
                "this is the latest effective filing."
            ),
        ],
        "errors": errors,
    }
    draft = {
        "status": "draft_unpopulated",
        "reason": (
            "This adapter packages SEC evidence only; financial fields require "
            "manual normalization or a separately approved extraction adapter."
        ),
        "target_schemas": [
            "financials_input_schema",
            "valuation_input_schema",
            "peer_comps_input_schema",
            "assumptions_schema",
        ],
    }

    generated = "\n".join(f"- `{name}`" for name in paths)
    report = f"""# SEC Official Filing Adapter Run

## Run Summary

- Adapter: `{ADAPTER_NAME}`
- Version: `{ADAPTER_VERSION}`
- Mode: `{config.mode}`
- Source URL: `{config.source_url}`
- Final URL: `{final_url}`
- SEC domain validated: `true`
- User-Agent provided: `{masked_user_agent_status(config)}`
- Request count: `{request_count}`
- Timeout: `{config.timeout}` seconds
- Minimum request interval: `{config.min_request_interval}` seconds
- HTTP status: `{http_status}`
- Retrieved at: `{retrieved_at}`
- Output directory: `{display_path(config.output_dir)}`
- Raw snapshot: `{display_path(snapshot_path)}`
- SHA-256: `{checksum or 'not_available'}`
- Overwrite used: `{str(overwrite_used).lower()}`

## Generated Files

{generated}

## Boundaries

- SEC-only explicit URL; GET only.
- No authentication, cookies, API key, token, password, or secret.
- No ticker/CIK/accession discovery and no bulk crawl.
- No XBRL or financial extraction.
- No populated normalized input.
- No broker, trading, order execution, investment conclusion, or portfolio instruction.

## Retrieval Result

- Errors: `{len(errors)}`
- Raw evidence available: `{'Yes' if body is not None else 'No'}`
- Latest-effective status: `user_specified_not_independently_discovered`

## Next Manual Step

Review the evidence package and manually normalize supported fields into v0.2.x
schemas. A populated extraction adapter requires separate approval.
"""

    write_json(paths["raw_snapshot_manifest.json"], raw_manifest)
    write_json(paths["source_manifest.json"], source_manifest)
    write_json(paths["field_provenance.json"], provenance)
    write_json(paths["unresolved_fields.json"], unresolved)
    write_json(paths["normalized_input_draft.json"], draft)
    paths["adapter_run_report.md"].write_text(report, encoding="utf-8")
    return paths


def run_adapter(
    config: AdapterConfig,
    fetcher: Fetcher = default_fetch,
    sleeper: Sleeper = time.sleep,
) -> dict[str, Path]:
    """Run fixture or live evidence packaging."""
    config = validate_config(config)
    overwrite_used = prepare_output_dir(config)
    if config.mode == "fixture":
        assert config.input_file is not None
        body = config.input_file.read_bytes()
        content_type = (
            mimetypes.guess_type(config.input_file.name)[0]
            or "application/octet-stream"
        )
        return write_package(
            config,
            overwrite_used,
            body,
            "fixture",
            0,
            config.retrieved_at,
            content_type,
            config.source_url,
        )

    try:
        response, request_count = fetch_with_retries(config, fetcher, sleeper)
    except FetchFailure as exc:
        return write_package(
            config,
            overwrite_used,
            None,
            exc.http_status,
            exc.request_count,
            exc.retrieved_at,
            "not_available",
            config.source_url,
            exc,
        )
    return write_package(
        config,
        overwrite_used,
        response.body,
        response.status,
        request_count,
        response.retrieved_at,
        response.content_type,
        response.final_url,
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Package one explicit SEC official filing URL or local fixture. "
            "No discovery, XBRL extraction, or investment conclusion."
        )
    )
    parser.add_argument("--mode", required=True, choices=("fixture", "live"))
    parser.add_argument("--input-file", type=Path)
    parser.add_argument("--company", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cik", required=True)
    parser.add_argument("--form-type", required=True)
    parser.add_argument("--accession", required=True)
    parser.add_argument("--filing-date", required=True)
    parser.add_argument("--reporting-period", required=True)
    parser.add_argument("--fiscal-year", required=True)
    parser.add_argument("--fiscal-quarter", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--currency", required=True)
    parser.add_argument("--amount-unit", required=True)
    parser.add_argument("--per-share-unit", required=True)
    parser.add_argument("--user-agent", default="")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--source-status", default="verified")
    parser.add_argument("--data-status", default="available")
    parser.add_argument("--retrieved-at", default="")
    parser.add_argument("--notes", default="none")
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--min-request-interval", type=float, default=0.5)
    parser.add_argument("--max-requests", type=int, default=3)
    parser.add_argument("--max-bytes", type=int, default=25_000_000)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    config = AdapterConfig(
        mode=args.mode,
        input_file=args.input_file,
        company=args.company,
        ticker=args.ticker,
        cik=args.cik,
        form_type=args.form_type,
        accession=args.accession,
        filing_date=args.filing_date,
        reporting_period=args.reporting_period,
        fiscal_year=args.fiscal_year,
        fiscal_quarter=args.fiscal_quarter,
        source_url=args.source_url,
        currency=args.currency,
        amount_unit=args.amount_unit,
        per_share_unit=args.per_share_unit,
        user_agent=args.user_agent,
        output_dir=args.output_dir,
        source_status=args.source_status,
        data_status=args.data_status,
        retrieved_at=args.retrieved_at,
        notes=args.notes,
        timeout=args.timeout,
        min_request_interval=args.min_request_interval,
        max_requests=args.max_requests,
        max_bytes=args.max_bytes,
        overwrite=args.overwrite,
    )
    try:
        paths = run_adapter(config)
    except (FileNotFoundError, FileExistsError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote SEC filing evidence package: {args.output_dir}")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
