# Fictional Normalized CSV Sandbox

## Summary

- Company: `Example Semiconductor Corp.`
- Ticker: `EXMP`
- Sandbox status: `fictional_sandbox_not_investment_data`
- Promotion ID: `promotion-exmp-fy2025-05a7dc26d188`
- Review batch ID: `normalized-review-exmp-05a7dc26d188`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Snapshot SHA-256: `05a7dc26d188d1685b905353a68cc0d3102dedf831fa7fb3e50e1a943cf4a0b1`
- Populated fields: `capital_expenditure, cash_and_equivalents, gross_profit, operating_cash_flow, operating_income, revenue`
- Omitted fields: `accounts_receivable, acquisition_accounting_notes, acquisition_related_amortization, acquisition_related_costs, cash_and_short_term_investments, current_assets, current_liabilities, goodwill, intangible_assets, inventory, net_income, normalized_eps, normalized_net_income, normalized_operating_income, restructuring_and_integration_costs, shareholders_equity, shares_diluted, short_term_investments, stock_based_compensation, total_assets`
- Unresolved fields: `total_debt`
- Blocked fields: `none`
- Ratio dry-run allowed: `true`
- Overwrite used: `true`

## Partial-Field and Unresolved-Field UX

### Populated fields

- `capital_expenditure`
- `cash_and_equivalents`
- `gross_profit`
- `operating_cash_flow`
- `operating_income`
- `revenue`

### Omitted fields

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

### Unresolved fields

- `total_debt`

### Blocked fields

- None

### Available ratios

- `gross_margin`
- `operating_margin`
- `operating_cash_flow_margin`
- `free_cash_flow`
- `fcf_margin`

### Unavailable ratios

| Ratio | Missing inputs | Reason |
|---|---|---|
| raw_net_margin | `net_income` | missing_or_unresolved_inputs |
| raw_roe | `net_income`, `shareholders_equity` | missing_or_unresolved_inputs |
| raw_roa | `net_income`, `total_assets` | missing_or_unresolved_inputs |
| net_debt | `total_debt` | missing_or_unresolved_inputs |
| debt_to_equity | `total_debt`, `shareholders_equity` | missing_or_unresolved_inputs |
| current_ratio | `current_assets`, `current_liabilities` | missing_or_unresolved_inputs |
| sbc_to_revenue | `stock_based_compensation` | missing_or_unresolved_inputs |
| ar_to_revenue | `accounts_receivable` | missing_or_unresolved_inputs |
| inventory_to_revenue | `inventory` | missing_or_unresolved_inputs |
| diluted_shares_trend | `shares_diluted` | missing_or_unresolved_inputs |

### Caution

- Missing, unresolved and blocked fields are left blank. They are never auto-filled with zero.
- Unavailable ratios are disclosed instead of inferred.


## Boundary

- Fictional only.
- Sandbox.
- Not investment data.
- Not real company fact.
- Not for trading.
- Not production normalization.
- Promotion did not call v0.2.x scripts.
- Unsupported fields are blank or unresolved; they are not guessed.
