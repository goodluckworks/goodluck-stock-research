# Sandbox Research Packet: EXMP

## Boundary

- Sandbox / review-gated packet, not a final investment report.
- Fictional only.
- Not investment advice.
- Not production research.
- No target price.
- No buy/sell/hold instruction.
- No position size.
- No trading action.

## Pipeline Summary

- Pipeline run ID: `pipeline-fictional_sandbox_partial-exmp-2026-07-01T070057z0000`
- Mode: `fictional_sandbox_partial`
- Company: `Example Semiconductor Corp.`
- Ticker: `EXMP`
- Fixture data status: `fictional_sample`

## Approved / Populated Fields

- `capital_expenditure`
- `cash_and_equivalents`
- `gross_profit`
- `operating_cash_flow`
- `operating_income`
- `revenue`

## Omitted / Unresolved / Blocked Fields

### Omitted

- `accounts_receivable`
- `acquisition_accounting_notes`
- `acquisition_related_amortization`
- `acquisition_related_costs`
- `cash_and_short_term_investments`
- `current_assets`
- `current_liabilities`
- `goodwill`
- `intangible_assets`
- `inventory`
- `net_income`
- `normalized_eps`
- `normalized_net_income`
- `normalized_operating_income`
- `restructuring_and_integration_costs`
- `shareholders_equity`
- `shares_diluted`
- `short_term_investments`
- `stock_based_compensation`
- `total_assets`

### Unresolved

- `total_debt`

### Blocked

- None

## Ratio Dry-Run Summary

- Dry-run ID: `v02-ratio-sandbox-exmp-05a7dc26d188`
- Script: `ratio_calculator.py`
- Run status: `passed`
- Available ratios: `5`
- Unavailable ratios: `10`

| Unavailable ratio | Missing inputs |
|---|---|
| raw_net_margin | net_income |
| raw_roe | net_income, shareholders_equity |
| raw_roa | net_income, total_assets |
| net_debt | total_debt |
| debt_to_equity | total_debt, shareholders_equity |
| current_ratio | current_assets, current_liabilities |
| sbc_to_revenue | stock_based_compensation |
| ar_to_revenue | accounts_receivable |
| inventory_to_revenue | inventory |
| diluted_shares_trend | shares_diluted |

## Audit References

- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Snapshot SHA-256: `05a7dc26d188d1685b905353a68cc0d3102dedf831fa7fb3e50e1a943cf4a0b1`
- Review batch: `normalized-review-exmp-05a7dc26d188`
- Promotion ID: `promotion-exmp-fy2025-05a7dc26d188`
- Normalized CSV manifest: `goodluck-stock-research/examples/pipeline_runs/EXMP/partial/normalized_csv_sandbox/normalized_csv_manifest.json`
- v0.2 dry-run manifest: `goodluck-stock-research/examples/pipeline_runs/EXMP/partial/v02_ratio_dry_run/v02_dry_run_manifest.json`

## Caveats

- Missing fields remain blank and are not filled with zero.
- Ratio output is a sandbox calculation check, not company fact.
