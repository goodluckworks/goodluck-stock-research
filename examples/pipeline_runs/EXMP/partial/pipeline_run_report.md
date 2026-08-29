# Review-Gated Pipeline Run Report

## Summary

- Pipeline run ID: `pipeline-fictional_sandbox_partial-exmp-2026-07-01T070057z0000`
- Mode: `fictional_sandbox_partial`
- Ticker: `EXMP`
- Company: `Example Semiconductor Corp.`
- Fixture data status: `fictional_sample`
- No investment conclusion: `true`

## Run Steps

| Step | Status |
|---|---|
| candidate | copied_local_fixture |
| workbench | copied_local_fixture |
| quality | copied_local_fixture |
| review | copied_local_fixture |
| promotion | copied_local_fixture |
| normalized_csv_sandbox | passed |
| v02_ratio_dry_run | passed |
| end_to_end_audit | passed |

## Blocked Steps

| Step | Reason |
|---|---|
| None | None |

## Warnings

- Fictional sandbox only; partial fields may make ratios unavailable.

## Boundary

- Offline / fixture-first pipeline.
- Not investment data.
- Not production research.
- No target price, buy/sell/hold, position size, research status or trading action.
- Real-company-shaped runs are review-only and not approved.
