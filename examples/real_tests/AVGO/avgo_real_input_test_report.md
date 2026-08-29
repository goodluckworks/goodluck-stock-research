# AVGO Real Input Test Report

## 1. Test Purpose

本测试验证本地 CSV / JSON 工具能否处理 Broadcom Inc. 这种并购驱动、半导体与基础设施软件并存、GAAP 与 management-defined Non-GAAP 差异显著的公司。测试不构成完整投资报告，不输出买卖建议。

## 2. Source Log

| Source | Type | Date / Period | Used For | Reliability | Notes |
|---|---|---|---|---|---|
| [Broadcom FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000121/avgo-20251102.htm) | Official filing | Filed 2025-12-18; FY ended 2025-11-02 | FY2024/FY2025 financials, segments, VMware, goodwill, intangibles, debt | Primary / verified | Filing正文优先于摘要页面。 |
| [Broadcom FY2025 earnings release](https://www.sec.gov/Archives/edgar/data/1730168/000173016825000116/avgo-11022025x8kxex99.htm) | Official 8-K exhibit | 2025-12-11 | Non-GAAP reconciliation, OCF, capex, FCF | Primary / company-disclosed | Non-GAAP 为管理层定义，不与 GAAP 混同。 |
| [Broadcom Q2 FY2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000054/avgo-20260503.htm) | Official filing | Filed 2026-06-09; quarter ended 2026-05-03 | Latest balance sheet, segment revenue, TTM bridge | Primary / verified | 用于最新 cash、debt、goodwill、intangibles 和 H1 数据。 |
| [Broadcom Q2 FY2026 earnings release](https://www.sec.gov/Archives/edgar/data/1730168/000173016826000051/avgo-05032026x8kxex99.htm) | Official 8-K exhibit | 2026-06-03 | Q2 AI semiconductor commentary, FCF and guidance | Primary / company-disclosed | AI revenue 与 guidance 均按管理层披露标注。 |
| StockAnalysis company statistics pages | Secondary market-data pages | Snapshot 2026-06-24 regular close | Price, market cap, EV, multiples and peer snapshots | Indicative / pending cross-check | 页面快照，不是公司官方披露；所有市场值均待交叉验证。 |

## 3. Input Files Created

| File | Purpose | Source Status | Notes |
|---|---|---|---|
| `inputs/avgo_financials.csv` | Ratio and acquisition-accounting review | verified | FY2024-FY2025 GAAP plus sourced company Non-GAAP reconciliation. |
| `inputs/avgo_assumptions.json` | FCFE DCF pressure test | verified inputs / analyst assumptions | TTM FCF derived from official releases; scenarios are analyst test assumptions. |
| `inputs/avgo_peer_comps.csv` | Blended and core peer comparison | indicative | Market snapshots are secondary data and classifications are analyst judgment. |
| `inputs/avgo_valuation_inputs.csv` | Market-implied expectations | indicative | Official operating evidence combined with indicative market values. |

## 4. Script Runs

| Script | Command | Result | Output File | Notes |
|---|---|---|---|---|
| Ratio calculator | `ratio_calculator.py --input .../avgo_financials.csv` | Pass | `outputs/avgo_ratio_output.md` | v0.2.4 acquisition-accounting section generated. |
| DCF sensitivity | `dcf_sensitivity.py --input .../avgo_assumptions.json` | Pass | `outputs/avgo_dcf_sensitivity_output.md` | FCFE bridge; net debt not subtracted. |
| Peer comps | `peer_comps_table.py --target-ticker AVGO` | Pass | `outputs/avgo_peer_comps_output.md` | Blended and two-company core statistics retained separately. |
| Implied expectations | `implied_expectations.py --input .../avgo_valuation_inputs.csv` | Pass | `outputs/avgo_implied_expectations_output.md` | Normalized earnings bridge and static mature-multiple requirements displayed. |

## 5. Key Outputs Summary

### Ratio Calculator

- Verified FY2025 revenue growth versus FY2024: `23.87%`.
- FY2025 GAAP gross margin: `67.77%`; operating margin: `39.89%`; FCF margin: `42.13%`.
- Net debt declined from `USD 58,218 million` to `USD 48,958 million` on a cash-only year-end basis.
- FY2025 goodwill / assets: `57.16%`; intangible assets / assets: `18.86%`.
- FY2025 acquisition-related amortization / revenue: `12.62%`.
- Company-defined normalized metrics are shown beside, not substituted for, GAAP metrics.

### DCF Sensitivity

- Base FCF is `USD 32,762 million`, derived from official-release TTM OCF less capex.
- It is treated as `FCFE research approximation`; therefore net debt is not subtracted again.
- Median-case implied values of `USD 91.27 / 112.17 / 132.81 per share` for bear/base/bull are pressure-test outputs. They are highly assumption-dependent and are not target-price commitments.

### Peer Comps Table

- Blended medians combine semiconductor, networking and software references and therefore are broad reference points only.
- Core statistics use NVDA and MRVL; the two-company sample is usable for orientation but remains narrow and heterogeneous.
- AVGO's infrastructure-software and acquisition-driven mix makes single-multiple comparison fragile.

### Implied Expectations

- Indicative market snapshot: `USD 382.07/share`, market cap `USD 1,817,728.67 million`, EV `USD 1,863,007.67 million`, regular close on 2026-06-24.
- A static bridge from `24.69x` EV/Sales to `10.0x` over five years requires about `19.81%` revenue CAGR if EV is unchanged.
- A normalized-earnings P/E bridge to `25.0x` requires about `12.48%` net-income CAGR.
- A P/FCF bridge to `30.0x` requires about `13.09%` FCF CAGR.
- These are reverse-engineered requirements, not forecasts.

## 6. Acquisition / VMware / Accounting Treatment

- **Verified fact:** VMware was acquired on 2023-11-22; FY2024 therefore includes a near-full year of VMware operations and is not cleanly comparable with a pre-acquisition base.
- **Verified fact:** FY2025 goodwill was `USD 97,801 million` and intangible assets were `USD 32,272 million`.
- **Verified fact:** Broadcom's reconciliation identifies FY2025 acquisition-related amortization of `USD 8,062 million`, restructuring and other charges of `USD 667 million`, and acquisition-related costs of `USD 216 million`.
- **Verified fact:** Company-defined Non-GAAP excludes amortization, SBC, restructuring, acquisition costs, selected financing items and tax adjustments. Broadcom cautions that exclusion does not mean the items are non-recurring.
- **Analyst judgment:** GAAP understates management's preferred operating view, but management-adjusted metrics may overstate economic recurrence if repeated acquisitions, SBC and integration costs are treated as permanently excludable.
- **Analyst judgment:** Debt and deleveraging remain key tracking items because acquisition debt is material even though cash generation is strong.

## 7. Segment and AI Infrastructure Treatment

- **Verified fact:** Broadcom separately reports semiconductor solutions and infrastructure software revenue.
- **Management disclosure:** Q2 FY2026 AI semiconductor revenue was stated as `USD 10.8 billion`, up `143%`, with Q3 AI semiconductor revenue guidance of about `USD 16 billion`.
- This is company-disclosed AI semiconductor revenue, but it is not the same as consolidated `AI-only revenue`; infrastructure software and non-AI semiconductor revenue remain separate.
- AI networking, custom silicon and hyperscaler programs are supported by management commentary, but design wins and forward programs are not realized revenue until recognized.
- Software and semiconductor economics should be discussed separately. Consolidated ratios are useful for financial quality, while valuation may require SOTP or at least segment-aware reference multiples.

## 8. Peer Comparability and Valuation Checks

- Blended peer statistics are not reliable final anchors because the set mixes accelerator, analog, handset, networking and SaaS economics.
- Core statistics contain two companies. This satisfies the tool's minimum threshold but remains indicative rather than robust.
- Semiconductor and software references should be grouped separately in interpretation even though the tool preserves a blended table.
- AVGO's acquisition-driven profile, leverage and amortization can distort P/E and EV/EBITDA comparisons.
- EV/Sales is useful for testing the growth burden but ignores mix and margin. P/FCF is closer to cash economics but can be affected by working-capital timing. P/E is most sensitive to GAAP/Non-GAAP acquisition adjustments.

## 9. Research Usefulness

- Directly usable with source context: reported ratio calculations, cash/debt bridge, acquisition-accounting ratios, segment facts and company-disclosed AI semiconductor revenue.
- Indicative only: price, market cap, EV, market multiples, peer distribution and mechanically derived forward revenue.
- Assumption-heavy: DCF outcomes, mature-multiple choices and five-year implied-growth bridges.
- Important gaps: sourced organic-growth bridge, detailed hyperscaler/customer concentration, segment-level profitability, acquisition ROIC, debt maturity/refinancing schedule and consensus estimates independently cross-checked from another market source.

## 10. Issues Found

| Issue | Severity | Category | Suggested Fix | Needs v0.2.4? |
|---|---|---|---|---:|
| v0.2.3 ratio schema could not structurally express goodwill, acquired intangibles or acquisition-related expenses | Medium | Schema / implementation | Add optional acquisition-accounting fields and ratio output section | Yes; fixed |
| Segment revenue and segment profitability are not modeled by the four local tools | Method limitation | Report-layer analysis | Keep segment analysis explicit in the research report; consider SOTP manually | No |
| Core peer classification remains subjective and the sample is small | Method limitation | Valuation judgment | Preserve notes, sample count and blended/core separation | No |
| Market data relies on one secondary-page snapshot | Low | Evidence | Cross-check before a production investment report | No |

## 11. Phase 3 Acceptance Review

| Acceptance Criterion | Result | Evidence |
|---|---:|---|
| Four AVGO inputs and outputs exist | Pass | `inputs/` and `outputs/` contain all required files. |
| Four scripts run successfully | Pass | All commands completed with non-empty Markdown outputs. |
| Source, period, currency and units retained | Pass | Each input records the relevant source fields and basis. |
| Market timestamp and session retained | Pass | 2026-06-24 regular-close snapshot is explicit. |
| Acquisition accounting quantified | Pass after v0.2.4 fix | Ratio output includes goodwill/assets, intangibles/assets and expense ratios. |
| GAAP and Non-GAAP remain distinct | Pass | Both are labeled and reconciliation limitations are stated. |
| Segment and AI narrative remain distinct | Pass | Segment facts, AI semiconductor disclosure and consolidated limits are separated. |
| Peer grouping used without mechanical conclusion | Pass | Peer metadata, blended/core tables and caveats are visible. |
| DCF FCF type is explicit | Pass | FCFE approximation with no net-debt subtraction. |
| No source-free number or direct trading advice | Pass | Sources and evidence status are attached; outputs are research tools only. |
| Safety boundary preserved | Pass | No API, network client, broker, credential or trading code added. |

## 12. Recommendation

- Phase 3 passed: Yes
- v0.2.3 是否足够支持 AVGO：No; acquisition accounting required a Medium schema fix.
- 是否建议进入 v0.2.4 小修：Yes; implemented and validated.
- 是否建议进入 Phase 4 三案例综合审查：Yes
- 是否建议进入 v0.3 design：Yes, after Phase 4 review
- 是否建议继续保持 private：Yes

