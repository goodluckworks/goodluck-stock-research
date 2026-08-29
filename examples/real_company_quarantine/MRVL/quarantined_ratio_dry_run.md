# QUARANTINED REAL-COMPANY SANDBOX DRY-RUN

Not production data.
Not investment advice.
Not for trading.
Manual review required.

## Boundary

- Quarantined MRVL ratio dry-run only.
- No DCF, peer comps or implied expectations.
- No full research report.
- No investment conclusion.
- No target price, buy/sell/hold, position size or research status.

# Financial Ratio Calculation

## Input file

- `goodluck-stock-research/examples/real_company_quarantine/MRVL/quarantined_normalized_sandbox.csv`

## Generated at

- 2026-07-03T02:42:39+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2026 to FY2026

## Input basis

- controlled_real_company_quarantine_sandbox

## Source status

- quarantined_review_fixture

## Key assumptions

- 输入行按时间从早到晚排列；growth 与 share trend 使用相邻行计算。
- 金额单位使用 amount_unit；每股数据单位使用 per_share_unit，不进行币种换算或单位缩放。
- 所有比率使用同一行的财务数据，除非另有说明。

## Calculation result

| Period | Revenue growth | Gross margin | Operating margin | Raw net margin | OCF margin | Free cash flow (USD millions) | FCF margin | Raw ROE | Raw ROA | Normalized net margin | Normalized ROE | Normalized ROA | Cash base used (USD millions) | Net debt basis | Net debt numeric (USD millions) | Net debt / (net cash) | Debt / equity | Current ratio | SBC / revenue | AR / revenue | Inventory / revenue | Diluted shares trend |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| FY2026 | 无法计算：需要至少两期数据 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 14.00 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 15.00 | cash_only | 25.00 | Net debt 25.00 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算 | 无法计算：需要至少两期数据 |

## Input sources

- FY2026: basis controlled_real_company_quarantine_sandbox; source synthetic real-company-shaped review packet; not company fact until verified; source date 2026-07-03; status quarantined_review_fixture.

## Special items and normalization

Raw GAAP profitability may require normalization where notes are present.

| Period | Special items notes | Normalized operating income (USD millions) | Normalized net income (USD millions) | Normalized EPS (USD/share) |
| --- | --- | ---: | ---: | ---: |
| FY2026 | quarantined sandbox; not production data; raw profitability must not be interpreted as company fact | 无法计算 | 无法计算 | 无法计算 |

## Acquisition accounting

- No acquisition-accounting fields were provided; acquisition-related balance-sheet and expense ratios were not calculated.

## Data limitations

- 只有一期数据；Revenue growth 和 Diluted shares trend 无法计算。
- FY2026: raw GAAP profitability may require normalization; special items notes: quarantined sandbox; not production data; raw profitability must not be interpreted as company fact
- FY2026: normalized metrics not provided; raw GAAP profitability should not be over-interpreted.
- 输入共有 9 个空白数值单元格；相关指标标记为“无法计算”。
- ROE 和 ROA 使用期末 shareholders' equity 与 total assets，未使用期初期末平均值。
- Capital expenditure 按现金流出绝对值处理，FCF = operating cash flow - |capital expenditure|。
- Net debt depends on the cash/investments field selected by the input. Users must confirm whether short-term investments are liquid and appropriate to include.
- 本工具只校验字段和算术逻辑，不验证输入数据是否与原始披露一致。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
