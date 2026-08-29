# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `xbrl-nvda-fy2026-c08153438a7f`
- Company: `NVIDIA Corporation`
- Ticker: `NVDA`
- Mode: `offline_fixture_only`
- Fixture format: `data_attr`
- Input: `goodluck-stock-research/xbrl/fixtures/nvda_candidate_fixture.html`
- Input SHA-256: `c08153438a7f3a97d4f34b0f6fa3136d8fd7be0fc1fbf84ddd0f3173e96c5834`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Mapping status: `prototype_fixture_only`
- Candidate count: `9`
- Unresolved field count: `0`
- Rejected fixture fact count: `2`
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
