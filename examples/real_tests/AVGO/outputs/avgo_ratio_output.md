# Financial Ratio Calculation

## Input file

- `goodluck-stock-research/examples/real_tests/AVGO/inputs/avgo_financials.csv`

## Generated at

- 2026-06-25T06:39:36+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2024 to FY2025

## Input basis

- GAAP; fiscal year ended 2024-11-03; VMware acquisition closed 2023-11-22 and materially affects period comparability; capex entered as positive cash outflow; GAAP; fiscal year ended 2025-11-02; VMware integrated into infrastructure software; capex entered as positive cash outflow

## Source status

- verified

## Key assumptions

- 输入行按时间从早到晚排列；growth 与 share trend 使用相邻行计算。
- 金额单位使用 amount_unit；每股数据单位使用 per_share_unit，不进行币种换算或单位缩放。
- 所有比率使用同一行的财务数据，除非另有说明。

## Calculation result

| Period | Revenue growth | Gross margin | Operating margin | Raw net margin | OCF margin | Free cash flow (USD millions) | FCF margin | Raw ROE | Raw ROA | Normalized net margin | Normalized ROE | Normalized ROA | Cash base used (USD millions) | Net debt basis | Net debt numeric (USD millions) | Net debt / (net cash) | Debt / equity | Current ratio | SBC / revenue | AR / revenue | Inventory / revenue | Diluted shares trend |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FY2024 | 无法计算 | 63.03% | 26.10% | 11.43% | 38.71% | 19,414.00 | 37.64% | 8.71% | 3.56% | 46.02% | 35.07% | 14.33% | 9,348.00 | cash_only | 58,218.00 | Net debt 58,218.00 | 1.00x | 1.17x | 11.13% | 8.56% | 3.41% | 无法计算 |
| FY2025 | 23.87% | 67.77% | 39.89% | 36.20% | 43.10% | 26,914.00 | 42.13% | 28.45% | 13.52% | 52.79% | 41.49% | 19.71% | 16,178.00 | cash_only | 48,958.00 | Net debt 48,958.00 | 0.80x | 1.71x | 11.85% | 11.18% | 3.55% | 1.57% |

## Input sources

- FY2024: basis GAAP; fiscal year ended 2024-11-03; VMware acquisition closed 2023-11-22 and materially affects period comparability; capex entered as positive cash outflow; source Broadcom FY2025 Form 10-K comparative financial statements and FY2025 earnings release reconciliation; source date 2025-12-18; status verified.
- FY2025: basis GAAP; fiscal year ended 2025-11-02; VMware integrated into infrastructure software; capex entered as positive cash outflow; source Broadcom FY2025 Form 10-K and FY2025 earnings release reconciliation; source date 2025-12-18; status verified.

## Special items and normalization

Raw GAAP profitability may require normalization where notes are present.

| Period | Special items notes | Normalized operating income (USD millions) | Normalized net income (USD millions) | Normalized EPS (USD/share) |
| --- | --- | ---: | ---: | ---: |
| FY2024 | FY2024 includes a near-full year of VMware operations after the 2023-11-22 acquisition. GAAP profitability includes USD 9,267 million acquisition-related intangible amortization, USD 1,787 million restructuring and other charges, USD 549 million acquisition-related costs, VMware financing interest, and discontinued operations. Company-defined non-GAAP metrics exclude amortization, SBC, restructuring, acquisition costs and tax adjustments; these exclusions are management-adjusted and should not be treated as GAAP. | 30,736.00 | 23,733.00 | 4.87 |
| FY2025 | FY2025 GAAP profitability includes USD 8,062 million acquisition-related intangible amortization, USD 667 million restructuring and other charges, USD 216 million acquisition-related costs, debt-extinguishment losses and unusual tax effects. Company-defined non-GAAP metrics exclude amortization, SBC, restructuring, acquisition costs and tax adjustments; management states these exclusions should not imply the items are non-recurring. | 41,997.00 | 33,728.00 | 6.82 |

## Acquisition accounting

| Period | Goodwill (USD millions) | Goodwill / assets | Intangible assets (USD millions) | Intangibles / assets | Acquisition-related amortization (USD millions) | Amortization / revenue | Restructuring and integration costs (USD millions) | Restructuring / revenue | Acquisition-related costs (USD millions) | Acquisition costs / revenue | Acquisition accounting notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| FY2024 | 97,784.00 | 59.03% | 38,122.00 | 23.01% | 9,267.00 | 17.97% | 1,787.00 | 3.46% | 549.00 | 1.06% | VMware acquisition closed 2023-11-22. Goodwill and intangible balances are reported year-end balances; expense classifications follow Broadcom's FY2025 non-GAAP reconciliation. |
| FY2025 | 97,801.00 | 57.16% | 32,272.00 | 18.86% | 8,062.00 | 12.62% | 667.00 | 1.04% | 216.00 | 0.34% | Goodwill and intangible balances are reported year-end balances. Expense classifications follow Broadcom's FY2025 non-GAAP reconciliation and remain economically relevant even when excluded from management-adjusted metrics. |

These fields preserve reported acquisition-accounting evidence. They do not automatically convert GAAP results into normalized results.

## Data limitations

- FY2024: raw GAAP profitability may require normalization; special items notes: FY2024 includes a near-full year of VMware operations after the 2023-11-22 acquisition. GAAP profitability includes USD 9,267 million acquisition-related intangible amortization, USD 1,787 million restructuring and other charges, USD 549 million acquisition-related costs, VMware financing interest, and discontinued operations. Company-defined non-GAAP metrics exclude amortization, SBC, restructuring, acquisition costs and tax adjustments; these exclusions are management-adjusted and should not be treated as GAAP.
- FY2024: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- FY2025: raw GAAP profitability may require normalization; special items notes: FY2025 GAAP profitability includes USD 8,062 million acquisition-related intangible amortization, USD 667 million restructuring and other charges, USD 216 million acquisition-related costs, debt-extinguishment losses and unusual tax effects. Company-defined non-GAAP metrics exclude amortization, SBC, restructuring, acquisition costs and tax adjustments; management states these exclusions should not imply the items are non-recurring.
- FY2025: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- ROE 和 ROA 使用期末 shareholders' equity 与 total assets，未使用期初期末平均值。
- Capital expenditure 按现金流出绝对值处理，FCF = operating cash flow - |capital expenditure|。
- Net debt depends on the cash/investments field selected by the input. Users must confirm whether short-term investments are liquid and appropriate to include.
- 本工具只校验字段和算术逻辑，不验证输入数据是否与原始披露一致。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
