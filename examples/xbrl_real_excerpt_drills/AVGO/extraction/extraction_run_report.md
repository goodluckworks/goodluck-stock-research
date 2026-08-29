# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `xbrl-avgo-fy2025-1f3d337d3708`
- Company: `Broadcom Inc.`
- Ticker: `AVGO`
- Mode: `offline_fixture_only`
- Fixture format: `data_attr`
- Input: `goodluck-stock-research/xbrl/fixtures/real_excerpt_drills/avgo_10k_excerpt_inline_like.html`
- Input SHA-256: `1f3d337d3708945b3aed545de6b3f180ba2bffa9c5c9173c652c992f46dfe350`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Mapping status: `prototype_fixture_only`
- Candidate count: `1`
- Unresolved field count: `8`
- Rejected fixture fact count: `1`
- Review status: `draft_extracted_unreviewed`
- Fixture data status: `real_filing_excerpt_drill`
- Overwrite used: `true`

## Output Files

- `extraction_run_manifest.json`
- `extraction_candidates.json`
- `field_provenance.json`
- `unresolved_fields.json`
- `extraction_run_report.md`

## Boundaries

- Local artificial fixture only; no URL access.
- Parser subset is limited to documented local fixtures; this is not production iXBRL parsing.
- Candidate extraction only; no approved normalized output.
- Every candidate requires human review.
- No downstream calculation or investment conclusion is produced.
