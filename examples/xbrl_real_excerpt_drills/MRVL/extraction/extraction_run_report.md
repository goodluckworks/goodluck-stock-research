# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `xbrl-mrvl-fy2026-29b488050b1b`
- Company: `Marvell Technology, Inc.`
- Ticker: `MRVL`
- Mode: `offline_fixture_only`
- Fixture format: `data_attr`
- Input: `goodluck-stock-research/xbrl/fixtures/real_excerpt_drills/mrvl_10k_excerpt_inline_like.html`
- Input SHA-256: `29b488050b1b47b4734ba9723aa03a53e5b3163e4c73fbd97a0f0128be18491e`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Mapping status: `prototype_fixture_only`
- Candidate count: `3`
- Unresolved field count: `6`
- Rejected fixture fact count: `0`
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
