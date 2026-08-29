# Financial Ratio Calculation

## Input file

- `goodluck-stock-research/examples/data/example_financials.csv`

## Generated at

- 2026-06-25T06:40:49+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2023 to FY2025

## Input basis

- GAAP; USD millions

## Source status

- fictional_sample

## Key assumptions

- 输入行按时间从早到晚排列；growth 与 share trend 使用相邻行计算。
- 金额单位使用 amount_unit；每股数据单位使用 per_share_unit，不进行币种换算或单位缩放。
- 所有比率使用同一行的财务数据，除非另有说明。

## Calculation result

| Period | Revenue growth | Gross margin | Operating margin | Raw net margin | OCF margin | Free cash flow (USD millions) | FCF margin | Raw ROE | Raw ROA | Normalized net margin | Normalized ROE | Normalized ROA | Cash base used (USD millions) | Net debt basis | Net debt numeric (USD millions) | Net debt / (net cash) | Debt / equity | Current ratio | SBC / revenue | AR / revenue | Inventory / revenue | Diluted shares trend |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FY2023 | 无法计算 | 55.00% | 12.00% | 8.00% | 14.00% | 140.00 | 9.33% | 7.06% | 3.75% | 无法计算 | 无法计算 | 无法计算 | 400.00 | cash_only | 250.00 | Net debt 250.00 | 0.38x | 1.83x | 3.00% | 17.33% | 12.67% | 无法计算 |
| FY2024 | 20.00% | 57.00% | 14.00% | 9.17% | 16.11% | 205.00 | 11.39% | 8.92% | 4.78% | 无法计算 | 无法计算 | 无法计算 | 500.00 | cash_plus_short_term_investments | 120.00 | Net debt 120.00 | 0.34x | 1.93x | 3.22% | 17.22% | 11.94% | 2.00% |
| FY2025 | 22.22% | 60.00% | 17.00% | 11.36% | 18.64% | 300.00 | 13.64% | 12.08% | 6.58% | 12.50% | 13.29% | 7.24% | 600.00 | user_provided_cash_and_investments | -10.00 | Net cash 10.00 | 0.29x | 2.07x | 3.41% | 16.36% | 10.45% | 2.94% |

## Input sources

- FY2023: basis GAAP; USD millions; source Fictional example filing; source date 2024-03-01; status fictional_sample.
- FY2024: basis GAAP; USD millions; source Fictional example filing; source date 2025-03-01; status fictional_sample.
- FY2025: basis GAAP; USD millions; source Fictional example filing; source date 2026-03-01; status fictional_sample.

## Special items and normalization

Raw GAAP profitability may require normalization where notes are present.

| Period | Special items notes | Normalized operating income (USD millions) | Normalized net income (USD millions) | Normalized EPS (USD/share) |
| --- | --- | ---: | ---: | ---: |
| FY2025 | Fictional restructuring charge affects GAAP profitability | 410.00 | 275.00 | 2.62 |

## Acquisition accounting

| Period | Goodwill (USD millions) | Goodwill / assets | Intangible assets (USD millions) | Intangibles / assets | Acquisition-related amortization (USD millions) | Amortization / revenue | Restructuring and integration costs (USD millions) | Restructuring / revenue | Acquisition-related costs (USD millions) | Acquisition costs / revenue | Acquisition accounting notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| FY2023 | 500.00 | 15.62% | 220.00 | 6.88% | 35.00 | 2.33% | 12.00 | 0.80% | 4.00 | 0.27% | Fictional acquisition-accounting values |
| FY2024 | 620.00 | 17.97% | 280.00 | 8.12% | 42.00 | 2.33% | 15.00 | 0.83% | 5.00 | 0.28% | Fictional acquisition-accounting values |
| FY2025 | 900.00 | 23.68% | 420.00 | 11.05% | 85.00 | 3.86% | 24.00 | 1.09% | 8.00 | 0.36% | Fictional acquisition-accounting values |

These fields preserve reported acquisition-accounting evidence. They do not automatically convert GAAP results into normalized results.

## Data limitations

- FY2023: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- FY2024: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- FY2025: raw GAAP profitability may require normalization; special items notes: Fictional restructuring charge affects GAAP profitability
- FY2025: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- ROE 和 ROA 使用期末 shareholders' equity 与 total assets，未使用期初期末平均值。
- Capital expenditure 按现金流出绝对值处理，FCF = operating cash flow - |capital expenditure|。
- Net debt depends on the cash/investments field selected by the input. Users must confirm whether short-term investments are liquid and appropriate to include.
- 本工具只校验字段和算术逻辑，不验证输入数据是否与原始披露一致。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
