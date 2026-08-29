# Sandbox Ratio Dry-Run Banner

- Sandbox status: `fictional_sandbox_not_investment_data`
- Ticker: `EXMP`
- Fictional only.
- Not investment data.
- Not company fact.
- Not for trading.
- Not production research.
- Partial-field caution: missing, unresolved and blocked fields remain blank and are never filled with zero.
- No target price, buy/sell/hold, position size or research status.

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


# Financial Ratio Calculation

## Input file

- `goodluck-stock-research/examples/pipeline_runs/EXMP/partial/normalized_csv_sandbox/normalized_financials_sandbox.csv`

## Generated at

- 2026-07-01T07:00:57+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2025 to FY2025

## Input basis

- GAAP-like fictional sandbox; populated only from EXMP approved-field promotion; not company fact; not investment data

## Source status

- fictional_sandbox

## Key assumptions

- 输入行按时间从早到晚排列；growth 与 share trend 使用相邻行计算。
- 金额单位使用 amount_unit；每股数据单位使用 per_share_unit，不进行币种换算或单位缩放。
- 所有比率使用同一行的财务数据，除非另有说明。

## Calculation result

| Period | Revenue growth | Gross margin | Operating margin | Raw net margin | OCF margin | Free cash flow (USD millions) | FCF margin | Raw ROE | Raw ROA | Normalized net margin | Normalized ROE | Normalized ROA | Cash base used (USD millions) | Net debt basis | Net debt numeric (USD millions) | Net debt / (net cash) | Debt / equity | Current ratio | SBC / revenue | AR / revenue | Inventory / revenue | Diluted shares trend |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FY2025 | 无法计算：需要至少两期数据 | 60.00% | 25.83% | 无法计算 | 27.50% | 238.00 | 19.83% | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 410.00 | unknown | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算：需要至少两期数据 |

## Input sources

- FY2025: basis GAAP-like fictional sandbox; populated only from EXMP approved-field promotion; not company fact; not investment data; source fictional EXMP XBRL promotion sandbox promotion-exmp-fy2025-05a7dc26d188; source date 2026-06-29T09:22:19+00:00; status fictional_sandbox.

## Special items and normalization

Raw GAAP profitability may require normalization where notes are present.

| Period | Special items notes | Normalized operating income (USD millions) | Normalized net income (USD millions) | Normalized EPS (USD/share) |
| --- | --- | ---: | ---: | ---: |
| FY2025 | fictional sandbox; unsupported fields left blank/unresolved | 无法计算 | 无法计算 | 无法计算 |

## Acquisition accounting

- No acquisition-accounting fields were provided; acquisition-related balance-sheet and expense ratios were not calculated.

## Data limitations

- 只有一期数据；Revenue growth 和 Diluted shares trend 无法计算。
- FY2025: raw GAAP profitability may require normalization; special items notes: fictional sandbox; unsupported fields left blank/unresolved
- FY2025: normalized metrics not provided; raw GAAP profitability should not be over-interpreted.
- 输入共有 10 个空白数值单元格；相关指标标记为“无法计算”。
- ROE 和 ROA 使用期末 shareholders' equity 与 total assets，未使用期初期末平均值。
- Capital expenditure 按现金流出绝对值处理，FCF = operating cash flow - |capital expenditure|。
- Net debt depends on the cash/investments field selected by the input. Users must confirm whether short-term investments are liquid and appropriate to include.
- 本工具只校验字段和算术逻辑，不验证输入数据是否与原始披露一致。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
