# Source Manifest Schema

## 1. Purpose

定义一个 evidence package 中所有来源的 manifest。Manifest 记录来源身份、可靠性、期间、单位、freshness、冲突和 supersession，不保存投资观点。

## 2. Manifest Metadata

| Field | Required | Meaning |
|---|---:|---|
| `manifest_version` | Yes | Schema version |
| `package_id` | Yes | Evidence package ID |
| `company_name` | Yes | Company identity |
| `ticker` | Yes | Ticker or `unresolved` |
| `exchange` | Yes | Exchange or `unresolved` |
| `cik` | Yes | CIK or `not_applicable/unresolved` |
| `as_of_date` | Yes | Evidence cutoff |
| `created_at` | Yes | Manifest creation timestamp |
| `sources` | Yes | Array of source records |
| `conflicts` | Yes | Array, empty if none |
| `active_source_ids` | Yes | Selected active sources by purpose |

## 3. Source Record

Required fields:

- `source_id`
- `source_name`
- `source_url`
- `source_type`
- `retrieved_at`
- `source_date`
- `filing_date`
- `reporting_period`
- `fiscal_period`
- `fiscal_year`
- `fiscal_quarter`
- `currency`
- `amount_unit`
- `per_share_unit`
- `market_session`
- `data_nature`
- `source_status`
- `data_status`
- `confidence`
- `freshness_class`
- `freshness_status`
- `raw_snapshot_id`
- `checksum`
- `notes`
- `transformation_notes`

Optional fields:

- `access_restrictions`
- `supersedes_source_id`
- `amends_source_id`
- `restatement_status`
- `license_notes`
- `timezone`
- `content_type`

## 4. Enumerations

### Source type

Use the taxonomy from `references/source-provenance-policy.md`.

### Source status

- `verified`
- `partially_verified`
- `indicative`
- `unverified`
- `fictional_sample`

### Data status

- `available`
- `partial`
- `stale`
- `conflicting`
- `superseded`
- `missing`
- `not_applicable`

### Confidence

- `high`
- `medium`
- `low`

### Freshness status

- `fresh`
- `stale_usable_for_history`
- `stale_blocking`
- `superseded`
- `unknown`

### Data nature

- `company_disclosed`
- `regulatory_filing`
- `management_commentary`
- `guidance`
- `real_time`
- `delayed`
- `estimated`
- `page_snapshot`
- `manual_input`
- `analyst_assumption`

## 5. Conflict Record

| Field | Meaning |
|---|---|
| `conflict_id` | Unique ID |
| `source_ids` | Conflicting sources |
| `affected_fields` | Fields affected |
| `conflict_type` | period / unit / currency / basis / value / identity / restatement |
| `resolution_status` | resolved / unresolved / manual_review_required |
| `selected_source_id` | Selected source or `none` |
| `resolution_notes` | Evidence-based reason |

Unresolved conflicts prevent affected fields from being marked verified.

## 6. Active Source Selection

`active_source_ids` maps purpose to source:

```yaml
active_source_ids:
  annual_financials: avgo-2025-10k
  latest_quarter: avgo-q2fy2026-10q
  normalized_reconciliation: avgo-q2fy2026-release
  market_snapshot: avgo-market-20260624-close
```

Selection must respect `as_of_date` and restatement status.

## 7. Example

```yaml
manifest_version: 0.3-design
package_id: avgo-2026-06-24
company_name: Broadcom Inc.
ticker: AVGO
exchange: NASDAQ
cik: "0001730168"
as_of_date: 2026-06-24T23:59:59-04:00
created_at: 2026-06-25T12:00:00Z
sources:
  - source_id: avgo-2025-10k
    source_name: Broadcom FY2025 Form 10-K
    source_url: https://www.sec.gov/example
    source_type: official_filing
    retrieved_at: 2026-06-25T10:00:00Z
    source_date: 2025-12-18
    filing_date: 2025-12-18
    reporting_period: FY2025
    fiscal_period: FY2025
    fiscal_year: FY2025
    fiscal_quarter: not_applicable
    currency: USD
    amount_unit: USD millions
    per_share_unit: USD/share
    market_session: not_applicable
    data_nature: regulatory_filing
    source_status: verified
    data_status: available
    confidence: high
    freshness_class: annual_filing
    freshness_status: fresh
    raw_snapshot_id: raw-avgo-2025-10k
    checksum: sha256:example
    notes: Filing正文
    transformation_notes: identity / none at source level
conflicts: []
active_source_ids:
  annual_financials: avgo-2025-10k
```

## 8. Validation Rules

- All required fields must be nonblank.
- `source_id` and `raw_snapshot_id` must be unique within a package.
- `retrieved_at` must include timezone.
- Market sources require session and data nature.
- Filing sources require filing date.
- Secondary pages cannot default to verified.
- `source_status` and `data_status` must both be present and must not be treated as synonyms.
- Superseded source cannot remain active.
- Manifest must not contain credentials, research conclusions or trading instructions.
