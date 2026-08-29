# Simplified DCF Sensitivity

## Input file

- `goodluck-stock-research/examples/real_tests/MRVL/inputs/mrvl_assumptions.json`

## Generated at

- 2026-06-25T01:18:00+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- TTM ended 2026-05-02

## Input basis

- Base FCF is OCF - capex and is treated as FCFE / levered FCF as a research approximation for this tool test; no net debt subtraction should be applied in the DCF bridge; amounts in USD millions and diluted shares in millions; growth, discount-rate, and terminal-growth paths are analyst test assumptions rather than company guidance

## Source status

- partially_verified
- Source: Marvell FY2026 10-K and Q1 FY2027 10-Q for base inputs; scenario assumptions prepared solely for v0.2.2 methodology validation
- Source date: 2026-06-24

## Key assumptions

- FCF type: FCFE
- Base-year FCF: 1,665.40 USD millions
- Projection years: 5
- Net debt input: 1,117.70 USD millions
- Diluted shares: 893.30 million shares
- Valuation bridge: Projected FCFE is discounted directly to equity value; enterprise value is not calculated by this simplified bridge.
- Net debt treatment: Net debt was not subtracted because FCFE is a levered equity cash-flow measure and financing effects are already reflected in the cash-flow basis.
- Scenario summary uses median discount rate 15.00% and median terminal growth 2.50%.
- Growth inputs are applied to FCF sequentially; the field name permits revenue-derived assumptions, but the model itself projects FCF.

## Calculation result

### Bear / Base / Bull projected FCF (USD millions)

| Case | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Bear | 1,748.67 | 1,818.62 | 1,873.18 | 1,929.37 | 1,967.96 |
| Base | 1,915.21 | 2,145.04 | 2,359.54 | 2,548.30 | 2,701.20 |
| Bull | 2,081.75 | 2,498.10 | 2,872.81 | 3,160.10 | 3,412.90 |

### Scenario DCF summary

| Case | Discount rate | Terminal growth | Terminal value (USD millions) | Enterprise value (USD millions) | Equity value (USD millions) | Implied value per share (USD/share) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bear | 15.00% | 2.50% | 16,137.26 | 不适用 / N/A | 14,231.98 | 15.93 |
| Base | 15.00% | 2.50% | 22,149.84 | 不适用 / N/A | 18,651.15 | 20.88 |
| Bull | 15.00% | 2.50% | 27,985.81 | 不适用 / N/A | 23,005.57 | 25.75 |

### Base-case sensitivity: implied value per share (USD/share)

| Discount rate \ Terminal growth | 2.00% | 2.50% | 3.00% |
| --- | ---: | ---: | ---: |
| 12.00% | 26.74 | 27.75 | 28.87 |
| 14.00% | 22.12 | 22.77 | 23.48 |
| 16.00% | 18.83 | 19.27 | 19.75 |
| 18.00% | 16.37 | 16.68 | 17.02 |

## Data limitations

- 输入数据由用户提供；本工具未独立验证其真实性。
- This is a simplified FCF model and does not separately model revenue, margins, taxes, working capital, capex, SBC, or financing flows.
- FCFF/UFCF requires a WACC-style discount rate; FCFE requires a cost-of-equity-style discount rate. The tool validates arithmetic, not whether the supplied rate matches the FCF type.
- Net debt is held constant for FCFF/UFCF scenarios and is not applied to FCFE scenarios; diluted shares are held constant in all scenarios.
- Terminal value can represent a large share of the discounted enterprise or equity value and is highly sensitive to discount and terminal growth rates.
- The computed implied value per share is a research output, not a promised target price or a buy/sell signal.
- The script validates arithmetic and field structure only; it does not fetch or verify external data.

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
