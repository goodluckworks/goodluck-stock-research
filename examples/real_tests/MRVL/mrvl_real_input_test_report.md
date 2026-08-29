# MRVL Real Input Test Report

## 1. Test Purpose

本报告最初用于 `stock-research-v0.2.1` 真实输入测试，并在 v0.2.2 与 v0.2.3 方法修复后完成回归。当前结果验证 FCFF/FCFE 估值桥、显式单位、cash basis、GAAP 特殊项目提示、peer comparability 和 earnings basis。

测试不调用 live API，不抓取实时行情，不执行交易。财务数据优先取自公司 filing；市场与同业数据来自二级公开页面，只按 `indicative / 待交叉验证` 使用。

## 2. Source Log

| Source | Type | Date / Period | Used For | Reliability | Notes |
|---|---|---|---|---|---|
| [Marvell FY2026 Form 10-K](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000011/mrvl-20260131.htm) | Official filing | Filed 2026-03-11; FY ended 2026-01-31 | FY2025/FY2026 statements, cash flow, balance sheet, shares and SBC | Primary / verified | Amounts entered in USD millions; GAAP. |
| [Marvell Q1 FY2027 Form 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000019/mrvl-20260502.htm) | Official filing | Filed 2026-05-28; quarter ended 2026-05-02 | TTM bridge, latest cash/debt, data-center context | Primary / verified | Data-center revenue is not treated as AI-only revenue. |
| [StockAnalysis MRVL overview](https://stockanalysis.com/stocks/mrvl/) | Secondary market page | Regular close 2026-06-23 | Current price | Secondary / indicative | Price snapshot: USD 279.04; page data must be cross-checked before formal use. |
| [StockAnalysis MRVL statistics](https://stockanalysis.com/stocks/mrvl/statistics/) | Secondary market page | Page updated 2026-06-24; market snapshot 2026-06-23 | Market cap, EV, standardized TTM metrics and multiples | Secondary / indicative | Market data timestamp recorded as 2026-06-23 16:00 EDT; some values are rounded or vendor-standardized. |
| [StockAnalysis AVGO statistics](https://stockanalysis.com/stocks/avgo/statistics/) | Secondary market page | Market snapshot 2026-06-23 | Peer comps | Secondary / indicative | Not company disclosure. |
| [StockAnalysis CRDO statistics](https://stockanalysis.com/stocks/crdo/statistics/) | Secondary market page | Market snapshot 2026-06-23 | Peer comps | Secondary / indicative | Not company disclosure. |
| [StockAnalysis ALAB statistics](https://stockanalysis.com/stocks/alab/statistics/) | Secondary market page | Market snapshot 2026-06-23 | Peer comps | Secondary / indicative | Not company disclosure. |
| [StockAnalysis COHR statistics](https://stockanalysis.com/stocks/cohr/statistics/) | Secondary market page | Market snapshot 2026-06-23 | Peer comps | Secondary / indicative | Negative vendor-reported TTM FCF makes P/FCF unavailable. |

## 3. Input Files Created

| File | Purpose | Source Status | Notes |
|---|---|---|---|
| `inputs/mrvl_financials.csv` | FY2025-FY2026 ratio calculation | `verified` | Filing-derived GAAP data; capex entered as positive cash outflow; net debt basis remains `cash_only` because no separate short-term-investment input was supplied. |
| `inputs/mrvl_assumptions.json` | Simplified DCF sensitivity | `partially_verified` | Base FCF uses `OCF - capex` and is treated as FCFE research approximation; growth and discount assumptions are analyst test assumptions, not guidance. |
| `inputs/mrvl_peer_comps.csv` | MRVL versus AVGO, CRDO, ALAB and COHR | `indicative` | CRDO and ALAB are user-classified core comparables; AVGO and COHR remain adjacent/reference observations. |
| `inputs/mrvl_valuation_inputs.csv` | Market-implied expectations bridge | `indicative` | Uses reported GAAP earnings with an explicit normalization caution; normalized earnings were not invented. |

## 4. Script Runs

| Script | Command | Result | Output File | Notes |
|---|---|---|---|---|
| `ratio_calculator.py` | `python3 goodluck-stock-research/scripts/ratio_calculator.py --input goodluck-stock-research/examples/real_tests/MRVL/inputs/mrvl_financials.csv --output goodluck-stock-research/examples/real_tests/MRVL/outputs/mrvl_ratio_output.md` | Pass | `outputs/mrvl_ratio_output.md` | Correctly calculated ratios and displayed `cash_only` as the net-debt basis. |
| `dcf_sensitivity.py` | `python3 goodluck-stock-research/scripts/dcf_sensitivity.py --input goodluck-stock-research/examples/real_tests/MRVL/inputs/mrvl_assumptions.json --output goodluck-stock-research/examples/real_tests/MRVL/outputs/mrvl_dcf_sensitivity_output.md` | Pass | `outputs/mrvl_dcf_sensitivity_output.md` | Uses FCFE; discounted cash flow goes directly to equity value and net debt is not subtracted. |
| `peer_comps_table.py` | `python3 goodluck-stock-research/scripts/peer_comps_table.py --input goodluck-stock-research/examples/real_tests/MRVL/inputs/mrvl_peer_comps.csv --output goodluck-stock-research/examples/real_tests/MRVL/outputs/mrvl_peer_comps_output.md --target-ticker MRVL` | Pass | `outputs/mrvl_peer_comps_output.md` | Preserved blended stats and produced core stats from CRDO and ALAB. |
| `implied_expectations.py` | `python3 goodluck-stock-research/scripts/implied_expectations.py --input goodluck-stock-research/examples/real_tests/MRVL/inputs/mrvl_valuation_inputs.csv --output goodluck-stock-research/examples/real_tests/MRVL/outputs/mrvl_implied_expectations_output.md` | Pass | `outputs/mrvl_implied_expectations_output.md` | Used reported GAAP fallback and displayed the required normalization caution. |

## 5. Key Outputs Summary

### Ratio Calculator

- FY2026 revenue growth: `42.09%`.
- Gross margin improved from `41.31%` to `51.02%`.
- Operating margin improved from `-12.49%` to `16.14%`.
- FY2026 FCF: `USD 1,396.4 million`; FCF margin `17.04%`.
- Net debt declined from `USD 3,115.5 million` to `USD 1,831.8 million`.
- Cash base equals cash and equivalents, and the output explicitly records `cash_only`; no unverified short-term investments were added.
- AR/revenue increased from `17.83%` to `26.68%`, a follow-up item rather than an automatic red flag.
- FY2026 net margin and ROE are not directly normalizable because net income includes material non-operating effects; the raw ratio output should not be quoted without this caveat.
- The v0.2.2 output now displays this warning and states that normalized metrics were not provided.

### DCF Sensitivity

- With the supplied test assumptions, the script produced Bear/Base/Bull FCF paths and a discount-rate/terminal-growth table.
- MRVL base FCF is `OCF - capex`, treated as `FCFE / levered FCF` as a research approximation.
- The DCF now discounts FCFE directly to equity value; enterprise value is `N/A` and net debt is not subtracted.
- At the median `15.0%` discount rate and `2.5%` terminal growth, calculated values per share were `USD/share 15.93 / 20.88 / 25.75`.
- These figures are highly assumption-dependent and are not reliable target prices.
- Output now distinguishes `USD millions` from `USD/share`.

### Peer Comps Table

- MRVL EV/Sales TTM is `28.17x`, versus the blended peer median of `30.75x` and user-classified core median of `51.87x`.
- MRVL Forward P/E is `61.58x`, versus the blended peer median of `47.83x` and core median of `81.24x`.
- MRVL P/FCF TTM is `146.57x`, versus the blended peer median of `124.63x` and core median of `161.57x`.
- The peer set spans diversified semiconductors, connectivity specialists and optical exposure; it is useful as a valuation range, not a mechanically comparable group.
- Every peer market metric remains `indicative / 待交叉验证`.
- Forward revenue growth is explicitly labeled `derived_from_ps_multiple`; it is not consensus or company guidance.

### Implied Expectations

Using static five-year mature-multiple assumptions:

- `10x` mature EV/Sales requires revenue to scale to `USD 24,554 million`, or about `23.01%` CAGR from TTM.
- `30x` mature P/E requires net income to scale to `USD 8,136.7 million`, or about `26.35%` CAGR.
- `40x` mature P/FCF requires FCF to scale to `USD 6,102.5 million`, or about `29.66%` CAGR.
- The combined bridge implies a mature FCF margin of `24.85%` and net margin of `33.14%`.
- The P/E bridge uses reported GAAP net income because no sourced normalized reconciliation was supplied; the output displays a caution rather than inventing normalized earnings.
- This is a reverse-engineering exercise: it shows what current valuation appears to require under stated assumptions, not what MRVL will achieve.

## 6. Research Usefulness

### Results that can be directly cited

- Filing-derived FY2025/FY2026 revenue, gross margin, operating margin, OCF, FCF, balance-sheet ratios and share trend, with period, currency, basis and source attached.
- The arithmetic of each output, provided the report preserves the exact input basis.
- The fact that the four tools accept real local inputs and produce auditable Markdown without network access.

### Results that are only indicative

- Current price, market cap, EV and valuation multiples from StockAnalysis.
- Peer means, medians and relative positions.
- Forward revenue growth mechanically inferred from current and forward P/S.
- Any comparison involving vendor-standardized EBITDA, FCF or forward estimates.

### Results that depend heavily on assumptions

- All DCF values, because the growth paths, discount rates and terminal rates are test assumptions.
- Market-implied scale-up values, because mature multiples and the five-year horizon are analyst assumptions.
- NTM revenue, which was mechanically derived from market cap and forward P/S rather than sourced from a consensus dataset.

### Data gaps affecting conclusions

- AI-only revenue is not separately disclosed. Q1 FY2027 data-center revenue supports AI-related exposure, but data-center revenue cannot be treated as AI-only revenue.
- Design-win conversion, customer-program timing, customer concentration and AI program gross margins require further company evidence.
- Core peer classification is a user judgment and does not make CRDO or ALAB fully comparable by scale, product mix or growth duration.
- FY2026 GAAP net income contains material non-operating effects. The tool now flags the earnings basis, but a sourced normalized bridge remains a data gap.
- Market metrics have not been cross-checked against a second market-data source.

## 7. Issues Found

| Issue | Severity | Category | Treatment | Needs v0.2.4? |
|---|---|---|---|---:|
| `OCF - capex` remains a research approximation for FCFE and may not capture all financing, lease, tax or preferred-equity effects. | Medium | Methodology | Require analyst review of the FCFE bridge before formal valuation use. | No; documented limitation |
| MRVL normalized operating income, net income and EPS were not supplied because no complete sourced reconciliation was prepared for this test. | Medium | Data gap | Add sourced normalized inputs only after reconciling filing adjustments. | No |
| Market data cannot be independently cross-checked inside the tool layer. | Low | Data limitation | Preserve current manual workflow; do not add live APIs solely to solve this in v0.2.2. | No |
| Peer core classification remains judgmental. | Method limitation | Comparability | Preserve notes and review the selected core subset before using its median. | No |

## 8. Recommendation

- **v0.2.3 是否足够稳定？** 是，cash basis、peer grouping 和 earnings basis 均通过 MRVL 回归。
- **是否仍存在限制？** 是。`OCF - capex` 只是 FCFE research approximation；normalized earnings、peer classification 和二级市场数据仍需要人工核验。
- **是否建议进入下一真实公司回归？** 是，前提是先检查并合并 v0.2.3 分支。
- **是否建议继续保持 private？** 建议继续保持 private，至少等真实样例和公开数据转载边界进一步复核后再考虑公开。

本文仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。
