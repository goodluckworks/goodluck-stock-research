# NVDA Real Input Test Report

## 1. Test Purpose

本测试使用 `stock-research-v0.2.3` 的四个本地数据工具处理 NVIDIA 的真实、手工整理 CSV/JSON 输入，并回归验证 cash/investments net debt basis、peer comparability 和 normalized earnings fallback。

财务事实优先使用 NVIDIA 10-K、10-Q、earnings release 与 CFO commentary。市场和 peer 数据来自二级公开页面，仅标记为 `indicative / 待交叉验证`。脚本只读取本地文件，不联网、不交易。

## 2. Source Log

| Source | Type | Date / Period | Used For | Reliability | Notes |
|---|---|---|---|---|---|
| [NVIDIA FY2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm) | Official filing | Filed 2026-02-25; FY ended 2026-01-25 | FY2025/FY2026 financials, Data Center revenue, H20 charge, stock split, customer and risk context | Primary / verified | All share and per-share figures are retrospectively adjusted for the June 2024 ten-for-one split. |
| [NVIDIA Q1 FY2027 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm) | Official filing | Filed 2026-05-20; quarter ended 2026-04-26 | Latest quarter, TTM bridge, Data Center/Hyperscale/ACIE, customer concentration, SBC, balance sheet | Primary / verified | Filing changed revenue market-platform presentation and recast comparable periods. |
| [NVIDIA Q1 FY2027 earnings release](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000051/q1fy27pr.htm) | Official 8-K exhibit | 2026-05-20 | Revenue highlights and management statements | Primary / company-disclosed | Revenue facts are cross-checked to the 10-Q. |
| [NVIDIA Q1 FY2027 CFO commentary](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000051/q1fy27cfocommentary.htm) | Official 8-K exhibit | 2026-05-20 | Data Center details, GAAP/Non-GAAP changes, market-platform definitions, management outlook | Primary / company-disclosed | Management claims and guidance are not treated as realized facts. |
| [SEC NVIDIA company facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0001045810.json) | Official XBRL data | Retrieved 2026-06-24 | Machine-readable cross-check and TTM bridge | Primary / verified | Used only to cross-check filing values and periods. |
| [StockAnalysis NVDA statistics](https://stockanalysis.com/stocks/nvda/statistics/) | Secondary market page | Regular close 2026-06-23; page updated 2026-06-24 | Price, market cap, EV, standardized TTM metrics and multiples | Secondary / indicative | Not company disclosure; must be cross-checked before formal valuation use. |
| [StockAnalysis AMD statistics](https://stockanalysis.com/stocks/amd/statistics/) | Secondary market page | Regular close 2026-06-23 | Peer comps | Secondary / indicative | Merchant CPU/GPU competitor, but profitability and product mix differ. |
| [StockAnalysis AVGO statistics](https://stockanalysis.com/stocks/avgo/statistics/) | Secondary market page | Regular close 2026-06-23 | Peer comps | Secondary / indicative | Diversified semiconductor/software and acquisition profile reduce comparability. |
| [StockAnalysis MRVL statistics](https://stockanalysis.com/stocks/mrvl/statistics/) | Secondary market page | Regular close 2026-06-23 | Peer comps | Secondary / indicative | AI connectivity/custom silicon reference; smaller scale. |
| [StockAnalysis ARM statistics](https://stockanalysis.com/stocks/arm/statistics/) | Secondary market page | Regular close 2026-06-23 | Peer comps | Secondary / indicative | Royalty/licensing model is weakly comparable to merchant silicon. |
| [StockAnalysis QCOM statistics](https://stockanalysis.com/stocks/qcom/statistics/) | Secondary market page | Regular close 2026-06-23 | Peer comps | Secondary / indicative | Handset and licensing exposure limit comparability. |

## 3. Input Files Created

| File | Purpose | Source Status | Notes |
|---|---|---|---|
| `inputs/nvda_financials.csv` | FY2025-FY2026 ratio calculation | `verified` | GAAP filing data; marketable securities included as short-term investments; normalized metrics not invented. |
| `inputs/nvda_assumptions.json` | Simplified DCF sensitivity | `partially_verified` | Base FCF is filing-derived; scenario paths are analyst test assumptions. |
| `inputs/nvda_peer_comps.csv` | NVDA versus AMD, AVGO, MRVL, ARM and QCOM | `indicative` | AMD is the only user-classified core comparable; other companies are adjacent or weak references. |
| `inputs/nvda_valuation_inputs.csv` | Market-implied expectations bridge | `indicative` | Reported GAAP earnings are retained with an explicit equity-gain caution; no normalized earnings are invented. |

## 4. Script Runs

| Script | Command | Result | Output File | Notes |
|---|---|---|---|---|
| `ratio_calculator.py` | `python3 goodluck-stock-research/scripts/ratio_calculator.py --input goodluck-stock-research/examples/real_tests/NVDA/inputs/nvda_financials.csv --output goodluck-stock-research/examples/real_tests/NVDA/outputs/nvda_ratio_output.md` | Pass | `outputs/nvda_ratio_output.md` | Used cash plus marketable securities and displayed net cash explicitly. |
| `dcf_sensitivity.py` | `python3 goodluck-stock-research/scripts/dcf_sensitivity.py --input goodluck-stock-research/examples/real_tests/NVDA/inputs/nvda_assumptions.json --output goodluck-stock-research/examples/real_tests/NVDA/outputs/nvda_dcf_sensitivity_output.md` | Pass | `outputs/nvda_dcf_sensitivity_output.md` | FCFE bridge correctly avoids net debt subtraction. |
| `peer_comps_table.py` | `python3 goodluck-stock-research/scripts/peer_comps_table.py --input goodluck-stock-research/examples/real_tests/NVDA/inputs/nvda_peer_comps.csv --output goodluck-stock-research/examples/real_tests/NVDA/outputs/nvda_peer_comps_output.md --target-ticker NVDA` | Pass | `outputs/nvda_peer_comps_output.md` | Shows structured group/status/notes, blended stats and a one-company core sample warning. |
| `implied_expectations.py` | `python3 goodluck-stock-research/scripts/implied_expectations.py --input goodluck-stock-research/examples/real_tests/NVDA/inputs/nvda_valuation_inputs.csv --output goodluck-stock-research/examples/real_tests/NVDA/outputs/nvda_implied_expectations_output.md` | Pass | `outputs/nvda_implied_expectations_output.md` | Uses reported GAAP fallback and displays the equity-gain normalization caution. |

## 5. Key Outputs Summary

### Ratio Calculator

- FY2026 revenue increased `65.47%` to `USD 215,938 million`.
- Gross margin declined from `74.99%` to `71.07%`; the filing attributes pressure partly to the `USD 4.5 billion` H20 inventory and purchase-obligation charge and the transition toward full-scale Blackwell data-center solutions.
- Operating margin declined from `62.42%` to `60.38%`, while FY2026 FCF increased to `USD 96,676 million`.
- SBC increased in absolute terms to `USD 6,386 million`, while SBC/revenue declined from `3.63%` to `2.96%`.
- Inventory/revenue increased from `7.72%` to `9.91%`; this is a follow-up item given rapid product transitions and supply commitments.
- Diluted weighted-average shares declined `1.17%`; all periods are already retrospectively adjusted for the ten-for-one split.
- Cash plus marketable securities produced net cash of `USD 34,747 million` in FY2025 and `USD 54,088 million` in FY2026, correcting the prior cash-only understatement.
- FY2026 marketable securities included investments subject to short-term lock-up restrictions; the cash base is therefore a research liquidity measure, not a claim that every security is immediately fungible with cash.
- Raw GAAP net margin, ROE and ROA should not be over-interpreted because FY2026 includes the H20 charge and material investment-related other income; no normalized bridge was supplied.

### DCF Sensitivity

- TTM FCF is `USD 119,076 million`, derived as FY2026 plus Q1 FY2027 less Q1 FY2026.
- `OCF - capex` is treated as FCFE / levered FCF research approximation; enterprise value is `N/A` and net debt is not subtracted.
- At the median `13.0%` discount rate and `2.5%` terminal growth, Bear/Base/Bull implied values per share are `USD 56.73 / 73.14 / 95.48`.
- This large gap versus the `USD 200.04` market snapshot does not establish mispricing. It shows that this simplified DCF is highly sensitive to the chosen FCFE growth path, discount rate, terminal assumptions and the inability to model revenue, margins and reinvestment explicitly.
- For NVDA, this DCF is a pressure test rather than a standalone target-price model.

### Peer Comps Table

- NVDA EV/Sales TTM is `18.95x`, below the blended peer median of `24.57x`.
- NVDA Forward P/E is `20.13x`, below the blended peer median of `59.62x`.
- AMD is the only row classified as core, so the core sample is explicitly flagged as too small and remains indicative.
- These apparent discounts are not directly decision-useful because the peer set contains radically different business models, growth rates, margins and accounting profiles.
- ARM's licensing economics, AVGO's software/acquisition mix, QCOM's handset/licensing exposure, and MRVL's smaller-scale connectivity exposure make a single blended median potentially misleading.
- All forward growth values are mechanically `derived_from_ps_multiple`; they are not sourced consensus growth or company guidance.

### Implied Expectations

Under the supplied five-year mature-multiple assumptions:

- An `8x` mature EV/Sales requires revenue to reach `USD 600,000 million`, a `2.37x` scale-up and about `18.81%` CAGR from TTM.
- A `25x` mature P/E requires net income of `USD 194,000 million`, about `3.98%` CAGR.
- A `30x` mature P/FCF requires FCF of `USD 161,667 million`, about `6.31%` CAGR.
- The mechanically derived `revenue_ntm` of `USD 435,368 million` comes from market cap divided by forward P/S. It is not a sourced consensus revenue estimate.
- Current FCF margin is `46.97%`, above the static mature FCF margin requirement of `26.94%`. This means valuation support in this bridge depends more on sustaining exceptional profitability and scaling revenue than on further margin expansion.
- The P/E bridge uses reported GAAP net income and visibly warns that material equity-security gains may require normalization. No normalized value is generated without a sourced reconciliation.

## 6. AI / Data Center Revenue Treatment

### Verified facts

- FY2026 Data Center revenue was `USD 193,737 million`, up `68%`, according to the FY2026 10-K.
- Q1 FY2027 Data Center revenue was `USD 75,246 million`, up `92%` year over year.
- Q1 FY2027 Data Center was split into `USD 37,869 million` Hyperscale and `USD 37,377 million` AI Clouds, Industrial & Enterprise (`ACIE`).
- Management stated that Data Center growth was driven by Blackwell 300 and demand for InfiniBand, Spectrum-X Ethernet and NVLink.
- Three direct customers represented `21%`, `17%` and `16%` of Q1 FY2027 total revenue, all primarily attributable to Compute & Networking.

### Required distinction

**AI-only revenue 未单独披露；data center revenue 可作为 AI-related exposure 的重要线索，但不能直接等同于 AI-only revenue。**

- `disclosed AI revenue`: 未单独披露。
- `AI-related revenue`: Data Center, Hyperscale and ACIE provide strong company-disclosed evidence of AI-related exposure.
- `data center revenue`: Fully disclosed as a market platform, but includes accelerated computing, networking, software and services; it is not an AI-only accounting segment.
- `management commentary`: Strongly attributes demand to AI factories, accelerated computing, Blackwell and networking.
- `market narrative`: NVIDIA is widely treated as the leading AI accelerator company, but market narrative is not used as a substitute for revenue disclosure.
- `unverified assumptions`: The exact percentage of Data Center revenue attributable exclusively to AI workloads, training versus inference, or individual end customers is not disclosed.

### Further verification

- Track Hyperscale versus ACIE mix under the new presentation framework.
- Monitor whether management introduces a separate AI revenue or software/services disclosure.
- Track customer concentration, China restrictions, Blackwell/Rubin transition costs, networking attach rates and inventory provisions.

## 7. High-Valuation Growth Stock Checks

- The static implied-expectations bridge requires about `18.81%` five-year revenue CAGR to reach an `8x` mature EV/Sales at unchanged EV.
- Current GAAP gross margin (`74.15%` TTM) and operating margin (`64.02%` TTM) are exceptionally high. A research conclusion must test margin normalization rather than assume these levels indefinitely.
- Current FCF margin (`46.97%`) is also unusually high; working-capital timing, supply commitments, investment spending and product transitions can change cash conversion.
- The June 2024 ten-for-one split changes nominal share price and share count but not enterprise value. All historical filing share and per-share figures used here are retrospectively adjusted.
- Q1 FY2027 diluted weighted-average shares were `24,391 million`, while StockAnalysis reported approximately `24,220 million` current shares outstanding. The difference reflects period-average versus point-in-time concepts and must not be silently mixed.
- FY2026 SBC was `USD 6,386 million`; share count nevertheless declined, supported by buybacks. Per-share analysis should track whether repurchases continue to exceed dilution and at what valuation.
- If revenue growth falls below the implied path while margins normalize, valuation compression can occur through both lower operating estimates and a lower terminal multiple.

## 8. Research Usefulness

### Results that can be directly cited

- Filing-derived FY2025/FY2026 revenue, margins, cash flow, balance-sheet ratios, SBC and split-adjusted share trend.
- Filing-derived TTM revenue, net income, OCF, capex and FCF bridge, provided the calculation formula is shown.
- Company-disclosed Data Center, Hyperscale, ACIE and customer-concentration facts.

### Results that are only indicative

- Current price, market cap, EV, standardized market multiples and peer values from StockAnalysis.
- Forward growth mechanically derived from P/S versus forward P/S.
- Peer medians and relative valuation positions.

### Results that depend heavily on assumptions

- Every DCF scenario and implied value per share.
- Mature EV/Sales, P/E and P/FCF assumptions.
- The five-year maturity period and mechanically derived NTM revenue.

### Data gaps affecting conclusions

- AI-only revenue is not separately disclosed.
- Some marketable securities have lock-up or market-value risk, so the reported cash base still requires liquidity judgment.
- The core peer sample contains only AMD and is too small for a robust valuation anchor.
- Normalized earnings were not supplied because no complete sourced reconciliation was prepared; the tool therefore uses reported GAAP with a visible caution.

## 9. Issues Found

| Issue | Severity | Category | v0.2.3 treatment | Needs v0.2.4? |
|---|---|---|---|---:|
| Cash-only net debt understated NVDA liquidity. | Medium, fixed | Schema / methodology | Added short-term investments, cash base, net-debt basis and net-cash display. | No |
| Blended peer median obscured weak comparability. | Medium, fixed | Peer methodology | Added peer group, status, notes, inclusion flag, blended stats and core stats. | No |
| P/E bridge lacked a normalized earnings basis. | Medium, fixed | Valuation basis | Added optional normalized net income/EPS and explicit GAAP fallback caution. | No |
| `OCF - capex` remains an FCFE research approximation rather than a complete levered cash-flow model. | Method limitation | DCF methodology | Preserve the existing warning and require manual review of financing, leases, taxes and working capital. | No |
| Forward revenue growth is derived from P/S ratios rather than a sourced consensus estimate. | Low | Market-data limitation | Keep `derived_from_ps_multiple` label and do not treat it as guidance or consensus. | No |
| Marketable securities may include lock-up or valuation risk. | Method limitation | Liquidity | Review security composition before treating the full amount as immediately available cash. | No |

The three Phase 2 Medium implementation gaps are fixed. Remaining items are disclosed method or data limitations and do not block another regression case.

## 10. Phase 2 Acceptance Review

| Acceptance Criterion | Result | Evidence |
|---|---:|---|
| Four NVDA input files created | Pass | All four files exist under `inputs/`. |
| Four scripts ran successfully | Pass | Each CLI returned success and generated Markdown. |
| Four outputs are non-empty | Pass | All output files contain calculation tables and limitations. |
| Inputs preserve source and source status | Pass | Financials are verified; assumptions partially verified; market inputs indicative. |
| Market data preserve timestamp/session/currency/units | Pass | `2026-06-23T16:00:00-04:00`, regular close, USD, USD millions, USD/share. |
| Data Center and AI-only revenue are not mixed | Pass | Report explicitly states AI-only revenue is not separately disclosed. |
| DCF FCF type is explicit | Pass | FCFE; net debt not subtracted. |
| Implied expectations are not presented as forecast | Pass | Output and report identify static bridge and analyst assumptions. |
| Peer comparability is disclosed | Pass | Structured groups, notes, inclusion flags, blended stats and core stats are visible. |
| No unsourced number used as fact | Pass | Filing values, derived calculations and assumptions are separately labeled. |
| No direct buy/sell advice | Pass | Outputs remain research calculations and method review. |
| No API/network/trading/credential code added | Pass | Only local CSV/JSON/Markdown files were added. |
| High/Medium implementation issues handled | Pass | All three Phase 2 Medium implementation gaps are fixed and regression-tested. |

## 11. Recommendation

- Phase 2 passed: **Yes**
- v0.2.3 是否足够支持 NVDA：**Yes for research-grade local calculations with disclosed manual judgments**
- 是否建议进入 v0.2.4 小修：**No**
- 是否建议进入 Phase 3 AVGO：**Yes, after user review and merge of v0.2.3**
- 是否建议继续保持 private：**Yes**

本文仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
