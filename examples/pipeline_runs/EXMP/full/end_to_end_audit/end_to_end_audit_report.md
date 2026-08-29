# EXMP End-to-End XBRL Sandbox Audit

## Summary

- Audit passed: `true`
- Generated at: `2026-07-01T07:00:57+00:00`
- Candidate dir: `goodluck-stock-research/examples/pipeline_runs/EXMP/full/candidate`
- Quality dir: `goodluck-stock-research/examples/pipeline_runs/EXMP/full/quality`
- Review dir: `goodluck-stock-research/examples/pipeline_runs/EXMP/full/review`
- Promotion dir: `goodluck-stock-research/examples/pipeline_runs/EXMP/full/promotion`
- Normalized dir: `goodluck-stock-research/examples/pipeline_runs/EXMP/full/normalized_csv_sandbox`
- Dry-run dir: `goodluck-stock-research/examples/pipeline_runs/EXMP/full/v02_ratio_dry_run`

## Checks

| Check | Result | Evidence |
|---|---:|---|
| EXMP fictional only | Pass | EXMP |
| mapping_version chain | Pass | us-gaap-core-v0.3.7-fixture-1 |
| snapshot_sha256 chain | Pass | 05a7dc26d188d1685b905353a68cc0d3102dedf831fa7fb3e50e1a943cf4a0b1 |
| ID chain | Pass | run/review/promotion/csv/dry-run IDs checked |
| sandbox labels | Pass | CSV and dry-run labels checked |
| CSV values and audit records | Pass | approved values and audit references checked |
| dry-run output | Pass | goodluck-stock-research/examples/pipeline_runs/EXMP/full/v02_ratio_dry_run/ratio_output_sandbox.md |

## Errors

- None

## Boundary

- EXMP fictional sandbox only.
- No real-company normalized CSV.
- No real-company v0.2.x dry-run.
- No live extraction or production parser claim.
- No investment conclusion, target price, buy/sell/hold, position size or research status.
