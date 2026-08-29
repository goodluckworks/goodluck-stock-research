# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `xbrl-avgo-fy2025-7dc8a9c4d00a`
- Company: `Broadcom Inc.`
- Ticker: `AVGO`
- Mode: `offline_fixture_only`
- Fixture format: `data_attr`
- Input: `goodluck-stock-research/xbrl/fixtures/avgo_candidate_fixture.html`
- Input SHA-256: `7dc8a9c4d00afce413507447e50bf457f5ece27e71a8c15a2afb18f27daf2df3`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Mapping status: `prototype_fixture_only`
- Candidate count: `8`
- Unresolved field count: `1`
- Rejected fixture fact count: `1`
- Review status: `draft_extracted_unreviewed`
- Fixture data status: `synthetic_unverified_real_company_shape`
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
