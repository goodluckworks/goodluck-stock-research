# SEC Official Filing Adapter Run

## Run Summary

- Adapter: `sec_official_filing_adapter`
- Version: `v0.3.2`
- Mode: `fixture`
- Source URL: `https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm`
- Final URL: `https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm`
- SEC domain validated: `true`
- User-Agent provided: `No`
- Request count: `0`
- Timeout: `15.0` seconds
- Minimum request interval: `0.5` seconds
- HTTP status: `fixture`
- Retrieved at: `2026-06-25T12:00:00Z`
- Output directory: `goodluck-stock-research/examples/adapter_runs_sec/MRVL`
- Raw snapshot: `goodluck-stock-research/examples/adapter_runs_sec/MRVL/raw/raw-mrvl-10-k-0001835632-26-000011-af8af9321049.htm`
- SHA-256: `af8af93210492293be69631aa1df5d1799a1ed1392246fcb9b2803185a7457cb`
- Overwrite used: `false`

## Generated Files

- `raw_snapshot_manifest.json`
- `source_manifest.json`
- `field_provenance.json`
- `unresolved_fields.json`
- `normalized_input_draft.json`
- `adapter_run_report.md`

## Boundaries

- SEC-only explicit URL; GET only.
- No authentication, cookies, API key, token, password, or secret.
- No ticker/CIK/accession discovery and no bulk crawl.
- No XBRL or financial extraction.
- No populated normalized input.
- No broker, trading, order execution, investment conclusion, or portfolio instruction.

## Retrieval Result

- Errors: `0`
- Raw evidence available: `Yes`
- Latest-effective status: `user_specified_not_independently_discovered`

## Next Manual Step

Review the evidence package and manually normalize supported fields into v0.2.x
schemas. A populated extraction adapter requires separate approval.
