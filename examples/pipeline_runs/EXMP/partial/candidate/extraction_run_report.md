# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `xbrl-exmp-fy2025-05a7dc26d188`
- Company: `Example Semiconductor Corp.`
- Ticker: `EXMP`
- Mode: `offline_fixture_only`
- Fixture format: `data_attr`
- Input: `goodluck-stock-research/xbrl/fixtures/exmp_fictional_inline_xbrl.html`
- Input SHA-256: `05a7dc26d188d1685b905353a68cc0d3102dedf831fa7fb3e50e1a943cf4a0b1`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Mapping status: `prototype_fixture_only`
- Candidate count: `9`
- Unresolved field count: `0`
- Rejected fixture fact count: `0`
- Review status: `draft_extracted_unreviewed`
- Fixture data status: `fictional_sample`
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
