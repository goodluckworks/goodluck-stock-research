# Field Provenance Schema

## 1. Purpose

定义 normalized input 中每个关键字段如何追溯到一个或多个 raw source。Field provenance 是 evidence layer 与 v0.2.x input schema 之间的审计桥。

## 2. Document Metadata

- `provenance_version`
- `package_id`
- `normalized_schema`
- `normalized_input_path`
- `created_at`
- `records`

## 3. Provenance Record

| Field | Required | Meaning |
|---|---:|---|
| `record_id` | Yes | Unique record ID |
| `normalized_field` | Yes | Existing v0.2.x schema field |
| `value` | Yes | Value or explicit unknown marker |
| `value_type` | Yes | number / string / date / boolean / array / unknown |
| `currency` | Yes | Currency or not_applicable |
| `unit` | Yes | Amount/per-share/ratio unit |
| `period` | Yes | Reporting or market period |
| `source_ids` | Yes | One or more source IDs |
| `source_field_names` | Yes | Original tags/labels |
| `source_locators` | Yes | Table/page/section/path/cell |
| `transformation` | Yes | Transformation type |
| `transformation_expression` | Yes | Reproducible formula or `identity` |
| `confidence` | Yes | high / medium / low |
| `source_status` | Yes | verified / partially_verified / indicative / unverified |
| `data_status` | Yes | available / partial / stale / conflicting / superseded / missing |
| `notes` | Yes | Basis, conflict or assumption notes |
| `transformation_notes` | Yes | Human-readable explanation complementing the reproducible expression |

## 4. Transformation Types

- `identity`
- `rename`
- `unit_scale`
- `currency_conversion`
- `sum`
- `difference`
- `ratio`
- `ttm_bridge`
- `split_adjustment`
- `manual_mapping`
- `analyst_assumption`
- `unresolved`

Currency conversion and split adjustment require their own source records and formulas.

## 5. Multiple Sources

For a derived field:

- List every source ID.
- Preserve each original value in `components`.
- State arithmetic order and rounding.
- Mark confidence no higher than the weakest material component.

Suggested `components`:

```yaml
components:
  - source_id: fy2025-release
    field: operating_cash_flow
    value: 27537
  - source_id: h1fy2026-release
    field: operating_cash_flow
    value: 19423
  - source_id: h1fy2025-release
    field: operating_cash_flow
    value: 9445
```

## 6. Missing and Unresolved Fields

Missing values are records, not blanks:

```yaml
value: 待核实
value_type: unknown
transformation: unresolved
source_ids: []
confidence: low
source_status: unverified
notes: Company does not separately disclose AI-only consolidated revenue
```

Zero is a numeric value and must never be used as a missing marker.

## 7. Mapping to v0.2.x Schemas

Each normalized file declares one target:

- `financials_input_schema`
- `valuation_input_schema`
- `peer_comps_input_schema`
- `assumptions_schema`

Every required text field and every populated numeric field must have a provenance record. Analyst assumptions in DCF inputs use `transformation=analyst_assumption`.

## 8. Examples

### Direct filing value

```yaml
record_id: avgo-fy2025-revenue
normalized_field: revenue
value: 63887
value_type: number
currency: USD
unit: USD millions
period: FY2025
source_ids: [avgo-2025-10k]
source_field_names: [Revenue]
source_locators: [Consolidated Statements of Operations]
transformation: identity
transformation_expression: identity
confidence: high
source_status: verified
data_status: available
notes: GAAP
transformation_notes: Direct extraction; no transformation
```

### Split-adjusted shares

```yaml
record_id: nvda-fy2026-diluted-shares
normalized_field: shares_diluted
value: 24514
value_type: number
currency: not_applicable
unit: million shares
period: FY2026
source_ids: [nvda-2026-10k]
source_field_names: [Weighted average diluted shares]
source_locators: [EPS note]
transformation: split_adjustment
transformation_expression: company-restated historical share basis after 10-for-1 split
confidence: high
source_status: verified
data_status: available
notes: Do not mix with pre-split share values
transformation_notes: Company-restated historical share basis
```

### Analyst assumption

```yaml
record_id: avgo-dcf-terminal-growth
normalized_field: terminal_growth_rates
value: [0.02, 0.025, 0.03]
value_type: array
currency: not_applicable
unit: decimal
period: projection
source_ids: [assumption-set-avgo-001]
source_field_names: [terminal_growth_rates]
source_locators: [local assumptions file]
transformation: analyst_assumption
transformation_expression: identity
confidence: low
source_status: unverified
data_status: available
notes: Scenario input, not company guidance
transformation_notes: Manually supplied scenario assumption
```

## 9. Validation Rules

- No populated field without provenance.
- No source ID absent from source manifest.
- No currency/unit conversion without formula and source.
- No `verified` status for analyst assumptions or secondary-only values.
- No transformation called `consensus` unless the source actually supplies consensus.
- No investment conclusion, status, recommendation or trading instruction.
