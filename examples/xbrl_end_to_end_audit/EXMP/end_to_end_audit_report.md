# EXMP End-to-End XBRL Sandbox Audit

## Summary

- Audit passed: `true`
- Generated at: `2026-07-01T06:56:49+00:00`
- Candidate dir: `goodluck-stock-research/examples/xbrl_extraction_runs/EXMP`
- Quality dir: `goodluck-stock-research/examples/xbrl_review_quality/EXMP`
- Review dir: `goodluck-stock-research/examples/xbrl_review_decisions/EXMP`
- Promotion dir: `goodluck-stock-research/examples/xbrl_promotion_runs/EXMP`
- Normalized dir: `goodluck-stock-research/examples/xbrl_normalized_sandbox/EXMP`
- Dry-run dir: `goodluck-stock-research/examples/xbrl_v02_dry_runs/EXMP`

## Checks

| Check | Result | Evidence |
|---|---:|---|
| EXMP fictional only | Pass | EXMP |
| mapping_version chain | Pass | us-gaap-core-v0.3.7-fixture-1 |
| snapshot_sha256 chain | Pass | 05a7dc26d188d1685b905353a68cc0d3102dedf831fa7fb3e50e1a943cf4a0b1 |
| ID chain | Pass | run/review/promotion/csv/dry-run IDs checked |
| sandbox labels | Pass | CSV and dry-run labels checked |
| CSV values and audit records | Pass | approved values and audit references checked |
| dry-run output | Pass | goodluck-stock-research/examples/xbrl_v02_dry_runs/EXMP/ratio_output_sandbox.md |

## Errors

- None

## Boundary

- EXMP fictional sandbox only.
- No real-company normalized CSV.
- No real-company v0.2.x dry-run.
- No live extraction or production parser claim.
- No investment conclusion, target price, buy/sell/hold, position size or research status.
