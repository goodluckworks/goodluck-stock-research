# Local Official Filing Adapter Run

## Run Summary

- Adapter: `local_official_filing_adapter`
- Version: `v0.3.1`
- Input file: `goodluck-stock-research/adapters/tests/fixtures/sample_avgo_filing_excerpt.html`
- Output directory: `goodluck-stock-research/examples/adapter_runs/AVGO`
- Raw snapshot: `goodluck-stock-research/examples/adapter_runs/AVGO/raw/raw-avgo-10-k-2025-12-18-282eb9790d7d.html`
- SHA-256: `282eb9790d7da2785a482bb0c864db1944f93bac2234a76a83adb93a4acb44a5`
- Source ID: `avgo-10-k-2025-12-18-282eb9790d7d`
- Snapshot ID: `raw-avgo-10-k-2025-12-18-282eb9790d7d`
- Retrieved at: `2026-06-25T12:00:00Z`
- Overwrite used: `false`

## Source Metadata

- Company: Broadcom Inc.
- Ticker: AVGO
- Source type: official_filing
- Form type: 10-K
- Filing date: 2025-12-18
- Reporting period: FY2025
- Fiscal year / quarter: 2025 / FY
- Source URL string: `local-fixture://sample_avgo_filing_excerpt.html`
- Currency: USD
- Amount unit: USD millions
- Per-share unit: USD/share
- Source status: verified
- Data status: available
- Verification basis: user-supplied metadata plus local file checksum only
- Notes: Short artificial fixture for local evidence packaging validation.

The source URL is retained only as citation metadata. This adapter does not open
URLs or perform network access. The adapter does not independently verify that
the local file is authentic, complete, or the latest effective filing.

## Generated Files

- `raw_snapshot_manifest.json`
- `source_manifest.json`
- `field_provenance.json`
- `unresolved_fields.json`
- `normalized_input_draft.json`
- `adapter_run_report.md`

## Safety Boundary

- Local input only.
- No network request, SEC API, live EDGAR fetch, browser automation, or web scraping.
- No credential, API key, token, password, secret, or environment-variable read.
- No subprocess, broker connection, order routing, or trading execution.
- This evidence package does not contain an investment conclusion, target price, portfolio action, or trading instruction.

## Unresolved Fields

- `revenue`: requires manual normalization.
- `gross_profit`: requires manual normalization.
- `operating_income`: requires manual normalization.
- `net_income`: requires manual normalization.
- `operating_cash_flow`: requires manual normalization.
- `capital_expenditure`: requires manual normalization.
- `cash_and_equivalents`: requires manual normalization.
- `total_debt`: requires manual normalization.
- `diluted_shares`: requires manual normalization.

## Next Manual Step

Review the raw snapshot and source manifest, then manually map supported values
into the appropriate v0.2.x input schema. A future extraction adapter would
require separate approval and its own field-level tests.

## Mapping to v0.2.x

- `financials_input_schema`: financial fields remain unresolved.
- `valuation_input_schema`: requires separate market and financial evidence.
- `peer_comps_input_schema`: requires separate market snapshots and comparability judgment.
- `assumptions_schema`: analyst assumptions must be supplied separately.
- `normalized_input_draft.json` records this evidence-only status and contains no financial values.
