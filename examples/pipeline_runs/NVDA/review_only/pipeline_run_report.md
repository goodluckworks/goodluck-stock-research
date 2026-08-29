# Review-Gated Pipeline Run Report

## Summary

- Pipeline run ID: `pipeline-real_company_review_only-nvda-2026-07-01T070058z0000`
- Mode: `real_company_review_only`
- Ticker: `NVDA`
- Company: `NVIDIA Corporation`
- Fixture data status: `synthetic_or_excerpt_review_only`
- No investment conclusion: `true`

## Run Steps

| Step | Status |
|---|---|
| candidate | review_only_copied_local_fixture |
| workbench | review_only_copied_local_fixture |
| quality | review_only_copied_local_fixture |
| review | review_only_copied_local_fixture |
| blocked_steps_report | passed |

## Blocked Steps

| Step | Reason |
|---|---|
| promotion | real_company_promotion_blocked |
| normalized_csv | real_company_csv_generation_blocked |
| v02_ratio_dry_run | real_company_dry_run_blocked |

## Warnings

- Real-company-shaped fixture remains draft/review-only.
- No promotion, no normalized CSV and no v0.2.x dry-run were generated.

## Boundary

- Offline / fixture-first pipeline.
- Not investment data.
- Not production research.
- No target price, buy/sell/hold, position size, research status or trading action.
- Real-company-shaped runs are review-only and not approved.
