# Simplified DCF Sensitivity

## Input file

- `goodluck-stock-research/examples/real_tests/NVDA/inputs/nvda_assumptions.json`

## Generated at

- 2026-06-25T01:18:01+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- TTM ended 2026-04-26

## Input basis

- Base FCF is filing-derived TTM operating cash flow less purchases of productive assets and is treated as FCFE / levered FCF as a research approximation; no net debt subtraction is applied. TTM equals FY2026 plus Q1 FY2027 less Q1 FY2026. Diluted shares use Q1 FY2027 weighted-average diluted shares in millions. Growth, discount-rate, and terminal-growth paths are analyst test assumptions, not company guidance.

## Source status

- partially_verified
- Source: NVIDIA FY2026 Form 10-K and Q1 FY2027 Form 10-Q for base inputs; scenario assumptions prepared solely for Phase 2 regression testing
- Source date: 2026-06-24

## Key assumptions

- FCF type: FCFE
- Base-year FCF: 119,076.00 USD millions
- Projection years: 5
- Net debt input: -4,767.00 USD millions
- Diluted shares: 24,391.00 million shares
- Valuation bridge: Projected FCFE is discounted directly to equity value; enterprise value is not calculated by this simplified bridge.
- Net debt treatment: Net debt was not subtracted because FCFE is a levered equity cash-flow measure and financing effects are already reflected in the cash-flow basis.
- Scenario summary uses median discount rate 13.00% and median terminal growth 2.50%.
- Growth inputs are applied to FCF sequentially; the field name permits revenue-derived assumptions, but the model itself projects FCF.

## Calculation result

### Bear / Base / Bull projected FCF (USD millions)

| Case | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Bear | 130,983.60 | 141,462.29 | 149,950.03 | 157,447.53 | 163,745.43 |
| Base | 142,891.20 | 164,324.88 | 184,043.87 | 202,448.25 | 218,644.11 |
| Bull | 154,798.80 | 193,498.50 | 232,198.20 | 267,027.93 | 293,730.72 |

### Scenario DCF summary

| Case | Discount rate | Terminal growth | Terminal value (USD millions) | Enterprise value (USD millions) | Equity value (USD millions) | Implied value per share (USD/share) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Bear | 13.00% | 2.50% | 1,598,467.27 | 不适用 / N/A | 1,383,647.27 | 56.73 |
| Base | 13.00% | 2.50% | 2,134,383.00 | 不适用 / N/A | 1,783,988.66 | 73.14 |
| Bull | 13.00% | 2.50% | 2,867,371.34 | 不适用 / N/A | 2,328,945.58 | 95.48 |

### Base-case sensitivity: implied value per share (USD/share)

| Discount rate \ Terminal growth | 2.00% | 2.50% | 3.00% |
| --- | ---: | ---: | ---: |
| 10.00% | 98.76 | 103.87 | 109.70 |
| 12.00% | 78.22 | 81.21 | 84.55 |
| 14.00% | 64.56 | 66.48 | 68.58 |
| 16.00% | 54.84 | 56.15 | 57.56 |

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
