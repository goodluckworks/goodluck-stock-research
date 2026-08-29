# Peer Comps Table

## Input file

- `goodluck-stock-research/examples/real_tests/MRVL/inputs/mrvl_peer_comps.csv`

## Generated at

- 2026-06-25T01:18:00+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- TTM / market close 2026-06-23

## Input basis

- StockAnalysis standardized TTM; USD millions; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1

## Source status

- indicative

## Key assumptions

- Target ticker: MRVL (Marvell Technology, Inc.)
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
| MRVL | Marvell Technology, Inc. | USD | USD millions | ai_networking_connectivity | core | Target company | false | 244,100.00 | 245,540.00 | 45.45% (derived) | derived_from_ps_multiple | 51.50% | 16.41% | 28.17x | 90.54x | 96.39x | 61.58x | 146.57x |
| AVGO | Broadcom Inc. | USD | USD millions | diversified_semiconductor | adjacent | Custom silicon and networking exposure but material software and acquisition mix | false | 1,810,000.00 | 1,850,000.00 | 87.71% (derived) | derived_from_ps_multiple | 76.28% | 44.17% | 24.57x | 44.05x | 63.27x | 24.14x | 55.20x |
| CRDO | Credo Technology Group Holding Ltd. | USD | USD millions | ai_networking_connectivity | core | AI connectivity exposure with smaller scale | true | 50,720.00 | 49,310.00 | 82.64% (derived) | derived_from_ps_multiple | 68.04% | 33.33% | 36.93x | 102.80x | 108.37x | 44.44x | 124.63x |
| ALAB | Astera Labs, Inc. | USD | USD millions | ai_networking_connectivity | core | AI connectivity exposure with higher growth and smaller scale | true | 68,050.00 | 66,910.00 | 74.45% (derived) | derived_from_ps_multiple | 75.99% | 22.36% | 66.81x | 286.69x | 268.42x | 118.04x | 198.51x |
| COHR | Coherent Corp. | USD | USD millions | optical_connectivity | reference | Different product mix and negative TTM FCF | false | 74,580.00 | 75,580.00 | 33.57% (derived) | derived_from_ps_multiple | 36.99% | 12.08% | 11.45x | 57.53x | 159.14x | 51.21x | 未提供 / 无法计算 |

`(calc)` 表示脚本使用输入的基础字段计算；未标记项为输入文件直接提供。

- Forward revenue growth is labeled by provenance. `derived_from_ps_multiple` is a mechanical derivation, not sourced consensus growth, company guidance, or analyst consensus.
- Derived rows: MRVL, AVGO, CRDO, ALAB, COHR.

### Blended peer statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 30.75x | 34.94x | 11.45x | 66.81x | 4 |
| EV/EBITDA TTM | 80.16x | 122.77x | 44.05x | 286.69x | 4 |
| P/E TTM | 133.75x | 149.80x | 63.27x | 268.42x | 4 |
| Forward P/E | 47.83x | 59.46x | 24.14x | 118.04x | 4 |
| P/FCF TTM | 124.63x | 126.11x | 55.20x | 198.51x | 3 |

Blended peer medians are broad reference points, not final valuation anchors.

### Core comparable statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 51.87x | 51.87x | 36.93x | 66.81x | 2 |
| EV/EBITDA TTM | 194.75x | 194.75x | 102.80x | 286.69x | 2 |
| P/E TTM | 188.40x | 188.40x | 108.37x | 268.42x | 2 |
| Forward P/E | 81.24x | 81.24x | 44.44x | 118.04x | 2 |
| P/FCF TTM | 161.57x | 161.57x | 124.63x | 198.51x | 2 |

- Core comparable sample contains 2 companies.

Core comparable medians depend on user-provided comparability classification.

### Target relative position versus blended peers

| Metric | Target | Premium / (discount) vs median | Low-to-high percentile |
| --- | ---: | ---: | ---: |
| EV/Sales TTM | 28.17x | -8.39% | 60% |
| EV/EBITDA TTM | 90.54x | 12.94% | 60% |
| P/E TTM | 96.39x | -27.94% | 40% |
| Forward P/E | 61.58x | 28.76% | 80% |
| P/FCF TTM | 146.57x | 17.60% | 75% |

### Target relative position versus core comparable median

| Metric | Target | Premium / (discount) vs core median |
| --- | ---: | ---: |
| EV/Sales TTM | 28.17x | -45.69% |
| EV/EBITDA TTM | 90.54x | -53.51% |
| P/E TTM | 96.39x | -48.84% |
| Forward P/E | 61.58x | -24.20% |
| P/FCF TTM | 146.57x | -9.28% |

相对位置仅描述倍数分布，不代表估值高低一定合理，也不构成买卖判断。

## Data gaps

- COHR: 缺少或无法计算 P/FCF TTM。

## Potentially incomparable companies

- MRVL: 来源尚未完全核实。
- AVGO: 来源尚未完全核实。
- CRDO: 来源尚未完全核实。
- ALAB: 来源尚未完全核实。
- COHR: 来源尚未完全核实, 结构化可比性为 reference。

## Input sources

- MRVL: basis StockAnalysis standardized TTM; USD millions; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis MRVL statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group ai_networking_connectivity; comparability core; core stats excluded.
- AVGO: basis StockAnalysis standardized TTM; USD millions; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis AVGO statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group diversified_semiconductor; comparability adjacent; core stats excluded.
- CRDO: basis StockAnalysis standardized TTM; USD millions; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis CRDO statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group ai_networking_connectivity; comparability core; core stats included.
- ALAB: basis StockAnalysis standardized TTM; USD millions; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis ALAB statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group ai_networking_connectivity; comparability core; core stats included.
- COHR: basis StockAnalysis standardized TTM; USD millions; forward revenue growth mechanically derived from P/S divided by forward P/S minus 1; source StockAnalysis COHR statistics page; 2026-06-23T16:00:00-04:00; regular close; indicative; forward growth source derived_from_ps_multiple; peer group optical_connectivity; comparability reference; core stats excluded.

## Data limitations

- 本工具不验证公司业务是否真正可比，也不调整会计准则、资本结构、税率或一次性项目。
- Core comparable statistics depend entirely on user-provided peer group and comparability classifications.
- 页面快照、延迟数据或第三方估算必须保留 source status，并在研究报告中标注为 indicative / 待交叉验证。
- 同业均值或中位数不能直接推出目标公司的研究状态或买卖结论。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
