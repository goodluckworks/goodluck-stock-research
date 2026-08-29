# Peer Comps Table

## Input file

- `goodluck-stock-research/examples/data/example_peer_comps.csv`

## Generated at

- 2026-06-25T01:18:00+00:00 UTC

## Currency

- USD
- Amount unit: USD millions
- Per-share unit: USD/share

## Reporting period

- FY2025 TTM

## Input basis

- TTM GAAP; USD millions; market snapshot

## Source status

- fictional_sample

## Key assumptions

- Target ticker: EXMP (Example Semiconductor Corp.)
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
| EXMP | Example Semiconductor Corp. | USD | USD millions | core_ai_accelerator | core | Target company | false | 12,000.00 | 12,500.00 | 18.00% | analyst_assumption | 60.00% | 17.00% | 5.68x (calc) | 24.04x (calc) | 48.00x (calc) | 32.00x | 29.27x (calc) |
| PEER1 | Peer Logic Systems | USD | USD millions | core_ai_accelerator | core | Similar accelerator economics | true | 9,800.00 | 10,200.00 | 14.00% | consensus | 57.00% | 16.00% | 4.98x | 21.70x | 31.61x | 27.50x | 27.22x |
| PEER2 | Peer Network Devices | USD | USD millions | ai_networking_connectivity | core | Similar growth and margin profile | true | 14,500.00 | 15,100.00 | 21.00% | company_guidance | 63.00% | 19.00% | 5.39x | 22.21x | 34.52x | 29.00x | 28.43x |
| PEER3 | Peer Analog Holdings | USD | USD millions | diversified_semiconductor | weak | Negative earnings and different end-market mix | false | 7,600.00 | 8,000.00 | 6.00% | unknown | 49.00% | -2.00% | 4.21x | 未提供 / 无法计算 | 未提供 / 无法计算 | 未提供 / 无法计算 | 63.33x |

`(calc)` 表示脚本使用输入的基础字段计算；未标记项为输入文件直接提供。

- Forward revenue growth is labeled by provenance. `derived_from_ps_multiple` is a mechanical derivation, not sourced consensus growth, company guidance, or analyst consensus.

### Blended peer statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 4.98x | 4.86x | 4.21x | 5.39x | 3 |
| EV/EBITDA TTM | 21.95x | 21.95x | 21.70x | 22.21x | 2 |
| P/E TTM | 33.06x | 33.06x | 31.61x | 34.52x | 2 |
| Forward P/E | 28.25x | 28.25x | 27.50x | 29.00x | 2 |
| P/FCF TTM | 28.43x | 39.66x | 27.22x | 63.33x | 3 |

Blended peer medians are broad reference points, not final valuation anchors.

### Core comparable statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
| EV/Sales TTM | 5.19x | 5.19x | 4.98x | 5.39x | 2 |
| EV/EBITDA TTM | 21.95x | 21.95x | 21.70x | 22.21x | 2 |
| P/E TTM | 33.06x | 33.06x | 31.61x | 34.52x | 2 |
| Forward P/E | 28.25x | 28.25x | 27.50x | 29.00x | 2 |
| P/FCF TTM | 27.82x | 27.82x | 27.22x | 28.43x | 2 |

- Core comparable sample contains 2 companies.

Core comparable medians depend on user-provided comparability classification.

### Target relative position versus blended peers

| Metric | Target | Premium / (discount) vs median | Low-to-high percentile |
| --- | ---: | ---: | ---: |
| EV/Sales TTM | 5.68x | 14.09% | 100% |
| EV/EBITDA TTM | 24.04x | 9.49% | 100% |
| P/E TTM | 48.00x | 45.17% | 100% |
| Forward P/E | 32.00x | 13.27% | 100% |
| P/FCF TTM | 29.27x | 2.95% | 75% |

### Target relative position versus core comparable median

| Metric | Target | Premium / (discount) vs core median |
| --- | ---: | ---: |
| EV/Sales TTM | 5.68x | 9.58% |
| EV/EBITDA TTM | 24.04x | 9.49% |
| P/E TTM | 48.00x | 45.17% |
| Forward P/E | 32.00x | 13.27% |
| P/FCF TTM | 29.27x | 5.19% |

相对位置仅描述倍数分布，不代表估值高低一定合理，也不构成买卖判断。

## Data gaps

- PEER3: 缺少或无法计算 EV/EBITDA TTM, P/E TTM, Forward P/E。

## Potentially incomparable companies

- EXMP: 来源尚未完全核实。
- PEER1: 来源尚未完全核实。
- PEER2: 来源尚未完全核实。
- PEER3: EBITDA 非正或缺失, 净利润非正或缺失, 来源尚未完全核实, 结构化可比性为 weak。

## Input sources

- EXMP: basis TTM GAAP; USD millions; market snapshot; source Fictional market snapshot; 2026-06-24T16:00:00-04:00; regular close; fictional_sample; forward growth source analyst_assumption; peer group core_ai_accelerator; comparability core; core stats excluded.
- PEER1: basis TTM GAAP; USD millions; market snapshot; source Fictional market snapshot; 2026-06-24T16:00:00-04:00; regular close; fictional_sample; forward growth source consensus; peer group core_ai_accelerator; comparability core; core stats included.
- PEER2: basis TTM GAAP; USD millions; market snapshot; source Fictional market snapshot; 2026-06-24T16:00:00-04:00; regular close; fictional_sample; forward growth source company_guidance; peer group ai_networking_connectivity; comparability core; core stats included.
- PEER3: basis TTM GAAP; USD millions; market snapshot; source Fictional market snapshot; 2026-06-24T16:00:00-04:00; regular close; fictional_sample; forward growth source unknown; peer group diversified_semiconductor; comparability weak; core stats excluded.

## Data limitations

- 本工具不验证公司业务是否真正可比，也不调整会计准则、资本结构、税率或一次性项目。
- Core comparable statistics depend entirely on user-provided peer group and comparability classifications.
- 页面快照、延迟数据或第三方估算必须保留 source status，并在研究报告中标注为 indicative / 待交叉验证。
- 同业均值或中位数不能直接推出目标公司的研究状态或买卖结论。

## Disclaimer

仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
