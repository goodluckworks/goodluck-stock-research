# Peer Comps Table

## Input file

- `goodluck-stock-research/examples/real_tests/AVGO/inputs/avgo_peer_comps.csv`

## Generated at

- 2026-06-25T06:34:41+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- TTM / market close 2026-06-24

## Input basis

- StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; semiconductor plus infrastructure software and acquisition-driven profile

## Source status

- indicative

## Key assumptions

- Target ticker: AVGO (Broadcom Inc.)
- Missing EV/Sales, EV/EBITDA, P/E, and P/FCF may be calculated from supplied base fields.
- Forward P/E cannot be derived without forward earnings and remains unavailable when not supplied.
- Forward revenue growth provenance is retained from `forward_revenue_growth_source`.
- Blended peer statistics exclude the target company and exclude missing, zero, and negative valuation multiples.
- Core comparable statistics additionally require `include_in_core_stats == true`.
- Currency conversion is not performed; cross-currency absolute values are not directly comparable.

## Calculation result

### Raw peer comps

| Ticker | Company | Currency | Amount unit | Peer group | Comparability | Comparability notes | Core stats | Market cap | EV | Forward revenue growth (derived where noted) | Growth source | Gross margin | Operating margin | EV/Sales TTM | EV/EBITDA TTM | P/E TTM | Forward P/E | P/FCF TTM |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AVGO | Broadcom Inc. | USD | USD millions | diversified_semiconductor | core | Target company; semiconductor, AI networking/custom silicon and infrastructure software mix | false | 1,817,728.67 | 1,863,007.67 | 87.67% (derived) | derived_from_ps_multiple | 76.28% | 44.17% | 24.69x | 44.27x | 63.59x | 24.26x | 55.48x |
| NVDA | NVIDIA Corporation | USD | USD millions | core_ai_accelerator | adjacent | Strong AI accelerator reference but no infrastructure software mix and materially different margins | true | 4,819,884.52 | 4,779,526.52 | 71.62% (derived) | derived_from_ps_multiple | 74.15% | 64.02% | 18.85x | 28.88x | 30.48x | 20.02x | 40.48x |
| MRVL | Marvell Technology, Inc. | USD | USD millions | ai_networking_connectivity | adjacent | AI networking and custom-silicon reference; much smaller scale and no software segment | true | 242,057.16 | 243,490.76 | 45.50% (derived) | derived_from_ps_multiple | 51.50% | 16.41% | 27.93x | 89.78x | 95.58x | 61.06x | 145.35x |
| AMD | Advanced Micro Devices Inc. | USD | USD millions | core_ai_accelerator | adjacent | Accelerator and CPU exposure but different business mix, scale and profitability | false | 847,488.38 | 839,012.38 | 48.41% (derived) | derived_from_ps_multiple | 53.06% | 11.78% | 22.40x | 112.92x | 173.32x | 59.61x | 98.84x |
| QCOM | QUALCOMM Incorporated | USD | USD millions | handset_mobile | weak | Handset and licensing exposure materially limit comparability | false | 208,070.14 | 213,541.14 | -8.49% (derived) | derived_from_ps_multiple | 54.80% | 25.68% | 4.80x | 16.43x | 21.57x | 20.27x | 16.64x |
| TXN | Texas Instruments Incorporated | USD | USD millions | diversified_semiconductor | reference | Analog-focused semiconductor reference with different cycle and capital intensity | false | 275,858.23 | 284,805.23 | 17.10% (derived) | derived_from_ps_multiple | 57.32% | 35.96% | 15.45x | 32.87x | 51.81x | 36.72x | 74.14x |
| ADI | Analog Devices Inc. | USD | USD millions | diversified_semiconductor | reference | Analog-focused semiconductor reference; different growth duration and end markets | false | 201,244.88 | 206,514.30 | 26.33% (derived) | derived_from_ps_multiple | 64.49% | 32.85% | 16.21x | 33.58x | 61.51x | 29.84x | 44.08x |
| CSCO | Cisco Systems Inc. | USD | USD millions | reference_only | reference | Networking systems and software reference; business model and AI silicon exposure differ | false | 471,907.97 | 488,268.97 | 11.56% (derived) | derived_from_ps_multiple | 64.30% | 23.71% | 8.04x | 28.71x | 39.91x | 25.52x | 40.03x |
| CRM | Salesforce Inc. | USD | USD millions | reference_only | weak | Infrastructure software reference only; SaaS economics and capital structure are not comparable | false | 125,110.44 | 155,821.44 | 9.94% (derived) | derived_from_ps_multiple | 77.64% | 21.87% | 3.64x | 12.08x | 17.73x | 10.97x | 8.53x |

`(calc)` 表示脚本使用输入的基础字段计算；未标记项为输入文件直接提供。

- Forward revenue growth is labeled by provenance. `derived_from_ps_multiple` is a mechanical derivation, not sourced consensus growth, company guidance, or analyst consensus.
- Derived rows: AVGO, NVDA, MRVL, AMD, QCOM, TXN, ADI, CSCO, CRM.

### Blended peer statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 15.83x | 14.66x | 3.64x | 27.93x | 8 |
| EV/EBITDA TTM | 30.88x | 44.41x | 12.08x | 112.92x | 8 |
| P/E TTM | 45.86x | 61.49x | 17.73x | 173.32x | 8 |
| Forward P/E | 27.68x | 33.00x | 10.97x | 61.06x | 8 |
| P/FCF TTM | 42.28x | 58.51x | 8.53x | 145.35x | 8 |

Blended peer medians are broad reference points, not final valuation anchors.

### Core comparable statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 23.39x | 23.39x | 18.85x | 27.93x | 2 |
| EV/EBITDA TTM | 59.33x | 59.33x | 28.88x | 89.78x | 2 |
| P/E TTM | 63.03x | 63.03x | 30.48x | 95.58x | 2 |
| Forward P/E | 40.54x | 40.54x | 20.02x | 61.06x | 2 |
| P/FCF TTM | 92.91x | 92.91x | 40.48x | 145.35x | 2 |

- Core comparable sample contains 2 companies.

Core comparable medians depend on user-provided comparability classification.

### Target relative position versus blended peers

| Metric | Target | Premium / (discount) vs median | Low-to-high percentile |
| --- | ---: | ---: | ---: |
| EV/Sales TTM | 24.69x | 55.97% | 89% |
| EV/EBITDA TTM | 44.27x | 43.38% | 78% |
| P/E TTM | 63.59x | 38.66% | 78% |
| Forward P/E | 24.26x | -12.36% | 44% |
| P/FCF TTM | 55.48x | 31.22% | 67% |

### Target relative position versus core comparable median

| Metric | Target | Premium / (discount) vs core median |
| --- | ---: | ---: |
| EV/Sales TTM | 24.69x | 5.56% |
| EV/EBITDA TTM | 44.27x | -25.38% |
| P/E TTM | 63.59x | 0.89% |
| Forward P/E | 24.26x | -40.16% |
| P/FCF TTM | 55.48x | -40.29% |

相对位置仅描述倍数分布，不代表估值高低一定合理，也不构成买卖判断。

## Data gaps

- 未发现估值倍数数据缺口。

## Potentially incomparable companies

- AVGO: 来源尚未完全核实。
- NVDA: 来源尚未完全核实。
- MRVL: 来源尚未完全核实。
- AMD: 来源尚未完全核实。
- QCOM: 来源尚未完全核实, 结构化可比性为 weak。
- TXN: 来源尚未完全核实, 结构化可比性为 reference。
- ADI: 来源尚未完全核实, 结构化可比性为 reference。
- CSCO: 来源尚未完全核实, 结构化可比性为 reference。
- CRM: 来源尚未完全核实, 结构化可比性为 weak。

## Input sources

- AVGO: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; semiconductor plus infrastructure software and acquisition-driven profile; source StockAnalysis AVGO statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group diversified_semiconductor; comparability core; core stats excluded.
- NVDA: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis NVDA statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group core_ai_accelerator; comparability adjacent; core stats included.
- MRVL: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis MRVL statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group ai_networking_connectivity; comparability adjacent; core stats included.
- AMD: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis AMD statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group core_ai_accelerator; comparability adjacent; core stats excluded.
- QCOM: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis QCOM statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group handset_mobile; comparability weak; core stats excluded.
- TXN: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis TXN statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group diversified_semiconductor; comparability reference; core stats excluded.
- ADI: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis ADI statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group diversified_semiconductor; comparability reference; core stats excluded.
- CSCO: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis CSCO statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group reference_only; comparability reference; core stats excluded.
- CRM: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis CRM statistics page; 2026-06-24T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group reference_only; comparability weak; core stats excluded.

## Data limitations

- 本工具不验证公司业务是否真正可比，也不调整会计准则、资本结构、税率或一次性项目。
- Core comparable statistics depend entirely on user-provided peer group and comparability classifications.
- 页面快照、延迟数据或第三方估算必须保留 source status，并在研究报告中标注为 indicative / 待交叉验证。
- 同业均值或中位数不能直接推出目标公司的研究状态或买卖结论。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
