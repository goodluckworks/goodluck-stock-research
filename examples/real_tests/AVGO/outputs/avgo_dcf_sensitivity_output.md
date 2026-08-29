# Simplified DCF Sensitivity

## Input file

- `goodluck-stock-research/examples/real_tests/AVGO/inputs/avgo_assumptions.json`

## Generated at

- 2026-06-25T06:34:41+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- TTM ended 2026-05-03

## Input basis

- Base FCF is official-release-derived TTM operating cash flow less purchases of property, plant and equipment: FY2025 plus H1 FY2026 less H1 FY2025. It is treated as FCFE / levered FCF as a research approximation; no net debt subtraction is applied. AVGO has material acquisition debt, interest, amortization, restructuring and integration effects, so this simplified DCF is a pressure test rather than a formal target-price model. Growth, discount-rate and terminal-growth paths are analyst test assumptions, not company guidance.

## Source status

- verified
- Source: Broadcom FY2025 earnings release and Q2 FY2026 earnings release / Form 10-Q
- Source date: 2026-06-09

## Key assumptions

- FCF type: FCFE
- Base-year FCF: 32,762.00 USD millions
- Projection years: 5
- Net debt input: 45,279.00 USD millions
- Diluted shares: 4,876.00 million shares
- Valuation bridge: Projected FCFE is discounted directly to equity value; enterprise value is not calculated by this simplified bridge.
- Net debt treatment: Net debt was not subtracted because FCFE is a levered equity cash-flow measure and financing effects are already reflected in the cash-flow basis.
- Scenario summary uses median discount rate 11.00% and median terminal growth 2.50%.
- Growth inputs are applied to FCF sequentially; the field name permits revenue-derived assumptions, but the model itself projects FCF.

## Calculation result

### Bear / Base / Bull projected FCF (USD millions)

| Case | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Bear | 35,382.96 | 37,505.94 | 39,381.23 | 40,956.48 | 42,185.18 |
| Base | 37,676.30 | 42,197.46 | 46,417.20 | 50,130.58 | 53,138.41 |
| Bull | 39,969.64 | 47,164.18 | 53,767.16 | 59,143.88 | 63,875.39 |

### Scenario DCF summary

| Case | Discount rate | Terminal growth | Terminal value (USD millions) | Enterprise value (USD millions) | Equity value (USD millions) | Implied value per share (USD/share) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bear | 11.00% | 2.50% | 508,703.62 | 不适用 / N/A | 445,017.41 | 91.27 |
| Base | 11.00% | 2.50% | 640,786.74 | 不适用 / N/A | 546,964.24 | 112.17 |
| Bull | 11.00% | 2.50% | 770,262.00 | 不适用 / N/A | 647,582.12 | 132.81 |

### Base-case sensitivity: implied value per share (USD/share)

| Discount rate \ Terminal growth | 2.00% | 2.50% | 3.00% |
| --- | ---: | ---: | ---: |
| 9.00% | 139.30 | 147.78 | 157.68 |
| 10.00% | 121.39 | 127.60 | 134.69 |
| 11.00% | 107.48 | 112.17 | 117.45 |
| 12.00% | 96.37 | 100.01 | 104.06 |
| 13.00% | 87.28 | 90.17 | 93.36 |

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
