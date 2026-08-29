# Adapter Contract Schema

## 1. Purpose

定义 future data adapter 的统一输入、输出、错误和安全契约。本文件是设计规范，不包含 adapter 实现。

Adapter 的唯一产物是 evidence package 和 normalized input path。Adapter 不得输出投资结论、研究状态、估值判断、thesis、bear case、仓位或交易动作。

## 2. Adapter Metadata

| Field | Required | Allowed / Meaning |
|---|---:|---|
| `adapter_name` | Yes | Stable adapter identifier |
| `adapter_type` | Yes | `official_filing_adapter`, `company_ir_adapter`, `earnings_release_adapter`, `transcript_adapter`, `market_snapshot_adapter`, `user_manual_input_adapter` |
| `adapter_version` | Yes | Semantic or immutable version |
| `mode` | Yes | `no_key`, `optional_key_read_only`, `local_manual` |
| `requires_key` | Yes | Boolean; default false |
| `allowed_sources` | Yes | Explicit allowlist of source types/domains or local inputs |
| `prohibited_actions` | Yes | Must include trading, broker, order execution, portfolio action, investment conclusion, credential persistence and source mutation |

Metadata invariants:

- `mode=no_key` implies `requires_key=false`.
- `optional_key_read_only` requires separate approval before implementation.
- No mode permits broker or trading behavior.

## 3. Input Contract

| Field | Required | Meaning |
|---|---:|---|
| `ticker` | Conditional | Security ticker; may be unresolved initially |
| `company_name` | Yes | Legal or requested company name |
| `cik` | Conditional | SEC CIK for U.S. filing requests |
| `exchange` | Conditional | Listing exchange |
| `fiscal_period` | Yes | Requested period or `latest_as_of_date` |
| `data_request_type` | Yes | `financials`, `market_snapshot`, `filing`, `transcript`, `peer_comps`, `identity`, `mixed_evidence` |
| `source_preference` | Yes | Ordered source-type preference |
| `as_of_date` | Yes | ISO 8601 date/time boundary |

Optional design fields:

- `share_class`
- `reporting_currency`
- `requested_fields`
- `allow_stale_cache`
- `maximum_staleness`
- `request_id`

Input behavior:

- Ambiguous identity stops company-specific normalization.
- Missing ticker may be resolved only from authoritative identity evidence.
- `as_of_date` prevents future evidence from leaking into historical research.

## 4. Output Contract

Allowed top-level output:

| Field | Required | Meaning |
|---|---:|---|
| `request_id` | Yes | Links request and evidence package |
| `adapter_metadata` | Yes | Frozen metadata used for the run |
| `raw_snapshot_manifest` | Yes | Path or object conforming to raw snapshot schema |
| `source_manifest` | Yes | Path or object conforming to source manifest schema |
| `field_provenance` | Yes | Path or object conforming to field provenance schema |
| `normalized_input_paths` | Yes | Zero or more local CSV / JSON paths |
| `unresolved_fields` | Yes | Explicit list; empty array if none |
| `warnings` | Yes | Explicit list; empty array if none |
| `errors` | Yes | Explicit list; empty array if none |
| `completed_at` | Yes | ISO 8601 timestamp |

Prohibited output fields include:

- `investment_conclusion`
- `recommendation`
- `buy`, `sell`, `hold`
- `target_price`
- `portfolio_action`
- `position_size`
- `research_status`
- `thesis_score`

Normalized paths may target:

- `financials_input_schema.md`
- `valuation_input_schema.md`
- `peer_comps_input_schema.md`
- `assumptions_schema.md`

An adapter may produce no normalized path when evidence is insufficient. That is a valid evidence result, not a reason to fabricate fields.

## 5. Error Contract

Each error record:

| Field | Meaning |
|---|---|
| `code` | Stable machine-readable code |
| `severity` | `warning`, `recoverable`, `blocking` |
| `stage` | identity / retrieval / snapshot / normalization / validation |
| `message` | Human-readable description |
| `source_id` | Related source or `not_applicable` |
| `affected_fields` | List of fields |
| `retryable` | Boolean |
| `recommended_action` | Manual refresh, provide source, resolve identity, etc. |

Blocking examples:

- `ticker_ambiguity`
- `company_cik_mismatch`
- `unit_mismatch`
- `currency_mismatch`
- `split_basis_mismatch`
- `unsupported_company_type`
- `provenance_missing`

## 6. Security Contract

- Read-only source access.
- No broker, order, trade or portfolio action.
- No source-system mutation.
- No credential value in output, manifest, warning, error or log.
- No environment-secret persistence.
- No automatic investment conclusion.
- Local output only to an approved workspace/cache root.
- Restricted evidence must not be committed.
- Optional-key implementation requires explicit approval and external credential management.

## 7. Examples

```yaml
request_id: avgo-fy2025-financials-001
adapter_metadata:
  adapter_name: future_official_filing_adapter
  adapter_type: official_filing_adapter
  adapter_version: design-example
  mode: no_key
  requires_key: false
  allowed_sources: [official_filing]
  prohibited_actions:
    - investment_conclusion
    - broker_connection
    - order_execution
raw_snapshot_manifest: manifests/avgo/raw-snapshot-manifest.json
source_manifest: manifests/avgo/source-manifest.json
field_provenance: manifests/avgo/field-provenance.json
normalized_input_paths:
  - normalized/avgo/financials.csv
unresolved_fields:
  - segment_operating_income
warnings:
  - FY2024 comparability affected by VMware acquisition
errors: []
completed_at: 2026-06-25T12:00:00Z
```

