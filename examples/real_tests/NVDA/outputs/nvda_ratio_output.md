# Financial Ratio Calculation

## Input file

- `goodluck-stock-research/examples/real_tests/NVDA/inputs/nvda_financials.csv`

## Generated at

- 2026-06-25T06:40:49+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2025 to FY2026

## Input basis

- GAAP; fiscal year ended 2025-01-26; all share and per-share amounts retrospectively adjusted for the June 2024 ten-for-one stock split; capex entered as positive cash outflow; GAAP; fiscal year ended 2026-01-25; all share and per-share amounts retrospectively adjusted for the June 2024 ten-for-one stock split; capex entered as positive cash outflow

## Source status

- verified

## Key assumptions

- 输入行按时间从早到晚排列；growth 与 share trend 使用相邻行计算。
- 金额单位使用 amount_unit；每股数据单位使用 per_share_unit，不进行币种换算或单位缩放。
- 所有比率使用同一行的财务数据，除非另有说明。

## Calculation result

| Period | Revenue growth | Gross margin | Operating margin | Raw net margin | OCF margin | Free cash flow (USD millions) | FCF margin | Raw ROE | Raw ROA | Normalized net margin | Normalized ROE | Normalized ROA | Cash base used (USD millions) | Net debt basis | Net debt numeric (USD millions) | Net debt / (net cash) | Debt / equity | Current ratio | SBC / revenue | AR / revenue | Inventory / revenue | Diluted shares trend |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FY2025 | 无法计算 | 74.99% | 62.42% | 55.85% | 49.11% | 60,853.00 | 46.63% | 91.87% | 65.30% | 无法计算 | 无法计算 | 无法计算 | 43,210.00 | cash_plus_short_term_investments | -34,747.00 | Net cash 34,747.00 | 0.11x | 4.44x | 3.63% | 17.67% | 7.72% | 无法计算 |
| FY2026 | 65.47% | 71.07% | 60.38% | 55.60% | 47.57% | 96,676.00 | 44.77% | 76.33% | 58.06% | 无法计算 | 无法计算 | 无法计算 | 62,556.00 | cash_plus_short_term_investments | -54,088.00 | Net cash 54,088.00 | 0.05x | 3.91x | 2.96% | 17.81% | 9.91% | -1.17% |

## Input sources

- FY2025: basis GAAP; fiscal year ended 2025-01-26; all share and per-share amounts retrospectively adjusted for the June 2024 ten-for-one stock split; capex entered as positive cash outflow; source NVIDIA FY2026 Form 10-K comparative financial statements; source date 2026-02-25; status verified.
- FY2026: basis GAAP; fiscal year ended 2026-01-25; all share and per-share amounts retrospectively adjusted for the June 2024 ten-for-one stock split; capex entered as positive cash outflow; source NVIDIA FY2026 Form 10-K; source date 2026-02-25; status verified.

## Special items and normalization

Raw GAAP profitability may require normalization where notes are present.

| Period | Special items notes | Normalized operating income (USD millions) | Normalized net income (USD millions) | Normalized EPS (USD/share) |
| --- | --- | ---: | ---: | ---: |
| FY2026 | GAAP gross profit and operating income include a USD 4.5 billion H20 excess inventory and purchase-obligation charge; GAAP other income includes material equity-security gains. Normalized metrics are not supplied because this test does not construct a complete sourced GAAP-to-normalized bridge. | 无法计算 | 无法计算 | 无法计算 |

## Acquisition accounting

| Period | Goodwill (USD millions) | Goodwill / assets | Intangible assets (USD millions) | Intangibles / assets | Acquisition-related amortization (USD millions) | Amortization / revenue | Restructuring and integration costs (USD millions) | Restructuring / revenue | Acquisition-related costs (USD millions) | Acquisition costs / revenue | Acquisition accounting notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| FY2025 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | Optional acquisition-accounting fields were not populated because they are not a central stress area for this regression. |
| FY2026 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | Optional acquisition-accounting fields were not populated because they are not a central stress area for this regression. |

These fields preserve reported acquisition-accounting evidence. They do not automatically convert GAAP results into normalized results.

## Data limitations

- FY2025: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- FY2026: raw GAAP profitability may require normalization; special items notes: GAAP gross profit and operating income include a USD 4.5 billion H20 excess inventory and purchase-obligation charge; GAAP other income includes material equity-security gains. Normalized metrics are not supplied because this test does not construct a complete sourced GAAP-to-normalized bridge.
- FY2026: normalized metrics not provided; raw GAAP profitability should not be over-interpreted.
- FY2026: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- ROE 和 ROA 使用期末 shareholders' equity 与 total assets，未使用期初期末平均值。
- Capital expenditure 按现金流出绝对值处理，FCF = operating cash flow - |capital expenditure|。
- Net debt depends on the cash/investments field selected by the input. Users must confirm whether short-term investments are liquid and appropriate to include.
- 本工具只校验字段和算术逻辑，不验证输入数据是否与原始披露一致。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
