# Financial Ratio Calculation

## Input file

- `goodluck-stock-research/examples/real_tests/MRVL/inputs/mrvl_financials.csv`

## Generated at

- 2026-06-25T06:40:49+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2025 to FY2026

## Input basis

- GAAP; USD millions; fiscal year ended 2025-02-01; capex entered as positive cash outflow; GAAP; USD millions; fiscal year ended 2026-01-31; capex entered as positive cash outflow

## Source status

- verified

## Key assumptions

- 输入行按时间从早到晚排列；growth 与 share trend 使用相邻行计算。
- 金额单位使用 amount_unit；每股数据单位使用 per_share_unit，不进行币种换算或单位缩放。
- 所有比率使用同一行的财务数据，除非另有说明。

## Calculation result

| Period | Revenue growth | Gross margin | Operating margin | Raw net margin | OCF margin | Free cash flow (USD millions) | FCF margin | Raw ROE | Raw ROA | Normalized net margin | Normalized ROE | Normalized ROA | Cash base used (USD millions) | Net debt basis | Net debt numeric (USD millions) | Net debt / (net cash) | Debt / equity | Current ratio | SBC / revenue | AR / revenue | Inventory / revenue | Diluted shares trend |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FY2025 | 无法计算 | 41.31% | -12.49% | -15.35% | 29.15% | 1,396.60 | 24.22% | -6.59% | -4.38% | 无法计算 | 无法计算 | 无法计算 | 948.30 | cash_only | 3,115.50 | Net debt 3,115.50 | 0.30x | 1.54x | 10.36% | 17.83% | 17.85% | 无法计算 |
| FY2026 | 42.09% | 51.02% | 16.14% | 32.58% | 21.36% | 1,396.40 | 17.04% | 18.66% | 11.98% | 无法计算 | 无法计算 | 无法计算 | 2,638.80 | cash_only | 1,831.80 | Net debt 1,831.80 | 0.31x | 2.01x | 7.21% | 26.68% | 16.94% | 0.49% |

## Input sources

- FY2025: basis GAAP; USD millions; fiscal year ended 2025-02-01; capex entered as positive cash outflow; source Marvell FY2026 Form 10-K comparative financial statements; source date 2026-03-11; status verified.
- FY2026: basis GAAP; USD millions; fiscal year ended 2026-01-31; capex entered as positive cash outflow; source Marvell FY2026 Form 10-K; source date 2026-03-11; status verified.

## Special items and normalization

Raw GAAP profitability may require normalization where notes are present.

| Period | Special items notes | Normalized operating income (USD millions) | Normalized net income (USD millions) | Normalized EPS (USD/share) |
| --- | --- | ---: | ---: | ---: |
| FY2026 | FY2026 GAAP net income includes material non-operating or one-time effects; raw net margin and ROE should not be extrapolated without a sourced normalization bridge. | 无法计算 | 无法计算 | 无法计算 |

## Acquisition accounting

| Period | Goodwill (USD millions) | Goodwill / assets | Intangible assets (USD millions) | Intangibles / assets | Acquisition-related amortization (USD millions) | Amortization / revenue | Restructuring and integration costs (USD millions) | Restructuring / revenue | Acquisition-related costs (USD millions) | Acquisition costs / revenue | Acquisition accounting notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| FY2025 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | Optional acquisition-accounting fields were not populated in this regression; verify from filing before use. |
| FY2026 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | Optional acquisition-accounting fields were not populated in this regression; verify from filing before use. |

These fields preserve reported acquisition-accounting evidence. They do not automatically convert GAAP results into normalized results.

## Data limitations

- FY2025: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- FY2026: raw GAAP profitability may require normalization; special items notes: FY2026 GAAP net income includes material non-operating or one-time effects; raw net margin and ROE should not be extrapolated without a sourced normalization bridge.
- FY2026: normalized metrics not provided; raw GAAP profitability should not be over-interpreted.
- FY2026: acquisition accounting ratios depend on user-supplied classifications and do not determine whether an expense is economically recurring.
- ROE 和 ROA 使用期末 shareholders' equity 与 total assets，未使用期初期末平均值。
- Capital expenditure 按现金流出绝对值处理，FCF = operating cash flow - |capital expenditure|。
- Net debt depends on the cash/investments field selected by the input. Users must confirm whether short-term investments are liquid and appropriate to include.
- 本工具只校验字段和算术逻辑，不验证输入数据是否与原始披露一致。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
