# Peer Comps Table

## Input file

- `goodluck-stock-research/examples/real_tests/NVDA/inputs/nvda_peer_comps.csv`

## Generated at

- 2026-06-25T01:18:01+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- TTM / market close 2026-06-23

## Input basis

- StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; handset and licensing exposure limits comparability; StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; royalty and licensing model is weakly comparable to merchant silicon

## Source status

- indicative

## Key assumptions

- Target ticker: NVDA (NVIDIA Corporation)
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
| NVDA | NVIDIA Corporation | USD | USD millions | core_ai_accelerator | core | Target company | false | 4,850,000.00 | 4,800,000.00 | 71.54% (derived) | derived_from_ps_multiple | 74.15% | 64.02% | 18.95x | 29.03x | 30.64x | 20.13x | 40.69x |
| AMD | Advanced Micro Devices Inc. | USD | USD millions | core_ai_accelerator | core | Direct accelerator competitor but materially different scale and margins | true | 847,670.00 | 839,190.00 | 48.39% (derived) | derived_from_ps_multiple | 53.06% | 11.78% | 22.41x | 112.95x | 173.35x | 59.62x | 98.86x |
| AVGO | Broadcom Inc. | USD | USD millions | diversified_semiconductor | adjacent | Custom silicon and networking exposure but material software and acquisition mix | false | 1,810,000.00 | 1,850,000.00 | 87.71% (derived) | derived_from_ps_multiple | 76.28% | 44.17% | 24.57x | 44.05x | 63.27x | 24.14x | 55.20x |
| MRVL | Marvell Technology, Inc. | USD | USD millions | ai_networking_connectivity | adjacent | AI networking and custom silicon reference with much smaller scale | false | 244,100.00 | 245,540.00 | 45.45% (derived) | derived_from_ps_multiple | 51.50% | 16.41% | 28.17x | 90.54x | 96.39x | 61.58x | 146.57x |
| ARM | Arm Holdings plc | USD | USD millions | ip_licensing | weak | Royalty and licensing economics are weakly comparable | false | 391,330.00 | 388,220.00 | 21.58% (derived) | derived_from_ps_multiple | 97.54% | 18.46% | 78.91x | 364.63x | 432.89x | 168.60x | 399.73x |
| QCOM | QUALCOMM Incorporated | USD | USD millions | handset_mobile | weak | Handset and licensing exposure materially limit comparability | false | 215,150.00 | 220,620.00 | -8.33% (derived) | derived_from_ps_multiple | 54.80% | 25.68% | 4.96x | 16.97x | 22.30x | 20.87x | 17.21x |

`(calc)` 表示脚本使用输入的基础字段计算；未标记项为输入文件直接提供。

- Forward revenue growth is labeled by provenance. `derived_from_ps_multiple` is a mechanical derivation, not sourced consensus growth, company guidance, or analyst consensus.
- Derived rows: NVDA, AMD, AVGO, MRVL, ARM, QCOM.

### Blended peer statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 24.57x | 31.80x | 4.96x | 78.91x | 5 |
| EV/EBITDA TTM | 90.54x | 125.83x | 16.97x | 364.63x | 5 |
| P/E TTM | 96.39x | 157.64x | 22.30x | 432.89x | 5 |
| Forward P/E | 59.62x | 66.96x | 20.87x | 168.60x | 5 |
| P/FCF TTM | 98.86x | 143.51x | 17.21x | 399.73x | 5 |

Blended peer medians are broad reference points, not final valuation anchors.

### Core comparable statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 22.41x | 22.41x | 22.41x | 22.41x | 1 |
| EV/EBITDA TTM | 112.95x | 112.95x | 112.95x | 112.95x | 1 |
| P/E TTM | 173.35x | 173.35x | 173.35x | 173.35x | 1 |
| Forward P/E | 59.62x | 59.62x | 59.62x | 59.62x | 1 |
| P/FCF TTM | 98.86x | 98.86x | 98.86x | 98.86x | 1 |

- Core comparable sample is too small; core stats are indicative only.

Core comparable medians depend on user-provided comparability classification.

### Target relative position versus blended peers

| Metric | Target | Premium / (discount) vs median | Low-to-high percentile |
| --- | ---: | ---: | ---: |
| EV/Sales TTM | 18.95x | -22.87% | 33% |
| EV/EBITDA TTM | 29.03x | -67.94% | 33% |
| P/E TTM | 30.64x | -68.21% | 33% |
| Forward P/E | 20.13x | -66.24% | 17% |
| P/FCF TTM | 40.69x | -58.84% | 33% |

### Target relative position versus core comparable median

| Metric | Target | Premium / (discount) vs core median |
| --- | ---: | ---: |
| EV/Sales TTM | 18.95x | -15.44% |
| EV/EBITDA TTM | 29.03x | -74.30% |
| P/E TTM | 30.64x | -82.32% |
| Forward P/E | 20.13x | -66.24% |
| P/FCF TTM | 40.69x | -58.84% |

相对位置仅描述倍数分布，不代表估值高低一定合理，也不构成买卖判断。

## Data gaps

- 未发现估值倍数数据缺口。

## Potentially incomparable companies

- NVDA: 来源尚未完全核实。
- AMD: 来源尚未完全核实。
- AVGO: 来源尚未完全核实。
- MRVL: 来源尚未完全核实。
- ARM: 来源尚未完全核实, 结构化可比性为 weak。
- QCOM: 来源尚未完全核实, 结构化可比性为 weak。

## Input sources

- NVDA: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis NVDA statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group core_ai_accelerator; comparability core; core stats excluded.
- AMD: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis AMD statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group core_ai_accelerator; comparability core; core stats included.
- AVGO: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis AVGO statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group diversified_semiconductor; comparability adjacent; core stats excluded.
- MRVL: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis MRVL statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group ai_networking_connectivity; comparability adjacent; core stats excluded.
- ARM: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; royalty and licensing model is weakly comparable to merchant silicon; source StockAnalysis ARM statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group ip_licensing; comparability weak; core stats excluded.
- QCOM: basis StockAnalysis standardized TTM; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; handset and licensing exposure limits comparability; source StockAnalysis QCOM statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group handset_mobile; comparability weak; core stats excluded.

## Data limitations

- 本工具不验证公司业务是否真正可比，也不调整会计准则、资本结构、税率或一次性项目。
- Core comparable statistics depend entirely on user-provided peer group and comparability classifications.
- 页面快照、延迟数据或第三方估算必须保留 source status，并在研究报告中标注为 indicative / 待交叉验证。
- 同业均值或中位数不能直接推出目标公司的研究状态或买卖结论。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
