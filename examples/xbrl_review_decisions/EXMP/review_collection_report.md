# Review Decision Collection Report

## Summary

- Collection passed: `true`
- Ticker: `EXMP`
- Review batch ID: `normalized-review-exmp-05a7dc26d188`
- Extraction run ID: `xbrl-exmp-fy2025-05a7dc26d188`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Quality score reference: `review-quality-exmp-05a7dc26d188`
- Snapshot SHA-256: `05a7dc26d188d1685b905353a68cc0d3102dedf831fa7fb3e50e1a943cf4a0b1`
- Generated at: `2026-06-29T09:22:19+00:00`

## Decisions

- `adjust`: 1
- `approve`: 5
- `needs_more_evidence`: 1
- `reject`: 1
- `unresolved`: 1

## Boundary

- Collector validates reviewer decisions but does not promote fields.
- Real-company decision batches remain blocked by promotion isolation.
- No investment conclusion or v0.2.x populated CSV is generated.
