# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `xbrl-nvda-fy2026-09f187116c7a`
- Company: `NVIDIA Corporation`
- Ticker: `NVDA`
- Mode: `offline_fixture_only`
- Fixture format: `data_attr`
- Input: `goodluck-stock-research/xbrl/fixtures/real_excerpt_drills/nvda_10q_excerpt_inline_like.html`
- Input SHA-256: `09f187116c7a742b38f608ca454016a3d9ac33bd1aac8a69095248c6539bcb4f`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Mapping status: `prototype_fixture_only`
- Candidate count: `3`
- Unresolved field count: `6`
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
