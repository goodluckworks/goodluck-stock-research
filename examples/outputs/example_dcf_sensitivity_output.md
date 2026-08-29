# Simplified DCF Sensitivity

## Input file

- `goodluck-stock-research/examples/data/example_assumptions.json`

## Generated at

- 2026-06-25T01:18:00+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2025

## Input basis

- FCFF and net debt in USD millions; diluted shares in millions; FCFF is an unlevered enterprise cash-flow assumption

## Source status

- fictional_sample
- Source: Fictional example assumptions
- Source date: 2026-06-24

## Key assumptions

- FCF type: FCFF
- Base-year FCF: 1,000.00 USD millions
- Projection years: 5
- Net debt input: 500.00 USD millions
- Diluted shares: 100.00 million shares
- Valuation bridge: Projected FCFF/UFCF is discounted to enterprise value; net debt is then subtracted to obtain equity value.
- Net debt treatment: Net debt of 500.00 USD millions was subtracted because FCFF/UFCF is an enterprise cash-flow measure.
- Scenario summary uses median discount rate 10.00% and median terminal growth 2.50%.
- Growth inputs are applied to FCF sequentially; the field name permits revenue-derived assumptions, but the model itself projects FCF.

## Calculation result

### Bear / Base / Bull projected FCF (USD millions)

| Case | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Bear | 1,050.00 | 1,092.00 | 1,124.76 | 1,158.50 | 1,181.67 |
| Base | 1,100.00 | 1,188.00 | 1,271.16 | 1,347.43 | 1,414.80 |
| Bull | 1,150.00 | 1,288.00 | 1,416.80 | 1,530.14 | 1,621.95 |

### Scenario DCF summary

| Case | Discount rate | Terminal growth | Terminal value (USD millions) | Enterprise value (USD millions) | Equity value (USD millions) | Implied value per share (USD/share) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bear | 10.00% | 2.50% | 16,149.53 | 14,254.66 | 13,754.66 | 137.55 |
| Base | 10.00% | 2.50% | 19,335.61 | 16,741.55 | 16,241.55 | 162.42 |
| Bull | 10.00% | 2.50% | 22,166.69 | 18,990.36 | 18,490.36 | 184.90 |

### Base-case sensitivity: implied value per share (USD/share)

| Discount rate \ Terminal growth | 2.00% | 2.50% | 3.00% |
| --- | ---: | ---: | ---: |
| 8.00% | 208.69 | 224.44 | 243.35 |
| 9.00% | 177.64 | 188.65 | 201.50 |
| 10.00% | 154.36 | 162.42 | 171.62 |
| 11.00% | 136.28 | 142.37 | 149.22 |
| 12.00% | 121.82 | 126.55 | 131.81 |

## Data limitations

- 示例输入标记为虚构数据，不可用于任何真实投资判断。
- This is a simplified FCF model and does not separately model revenue, margins, taxes, working capital, capex, SBC, or financing flows.
- FCFF/UFCF requires a WACC-style discount rate; FCFE requires a cost-of-equity-style discount rate. The tool validates arithmetic, not whether the supplied rate matches the FCF type.
- Net debt is held constant for FCFF/UFCF scenarios and is not applied to FCFE scenarios; diluted shares are held constant in all scenarios.
- Terminal value can represent a large share of the discounted enterprise or equity value and is highly sensitive to discount and terminal growth rates.
- The computed implied value per share is a research output, not a promised target price or a buy/sell signal.
- The script validates arithmetic and field structure only; it does not fetch or verify external data.

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
