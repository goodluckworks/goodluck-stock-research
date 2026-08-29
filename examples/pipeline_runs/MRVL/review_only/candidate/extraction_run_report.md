# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `xbrl-mrvl-fy2026-a1aaa9bfaf36`
- Company: `Marvell Technology, Inc.`
- Ticker: `MRVL`
- Mode: `offline_fixture_only`
- Fixture format: `data_attr`
- Input: `goodluck-stock-research/xbrl/fixtures/mrvl_candidate_fixture.html`
- Input SHA-256: `a1aaa9bfaf3605ceb1dbce7ae810c87044f6e651b96e94c60c27043205bedd6a`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Mapping status: `prototype_fixture_only`
- Candidate count: `7`
- Unresolved field count: `2`
- Rejected fixture fact count: `0`
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
