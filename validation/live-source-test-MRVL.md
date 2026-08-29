# Live Source Test: MRVL

本文仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。

## 1. Test Purpose

本次测试使用 `goodluck-stock-research` v0.1 对 Marvell Technology, Inc. (`MRVL`) 做一次真实公开资料验证，目标不是形成最终投资报告，而是检查 Skill 在真实资料下是否能稳定输出完整研究结构。

研究对象识别：

- Ticker: MRVL
- Exchange: Nasdaq Global Select Market
- Reporting currency: USD
- Latest reporting period: Q1 FY2027, three months ended May 2, 2026
- Research objective: 判断 MRVL 是否适合作为 AI 产业链相关股票进入观察池或候选池
- Investment horizon: 中期观察，重点跟踪未来 1-2 个季度 AI/data center 收入质量、客户需求和估值消化

核心验收重点：

- AI 产业链真实受益 vs 叙事受益
- 数据中心 / AI 相关收入是否有公司披露或管理层表述支撑
- 财务质量
- 当前估值与市场隐含预期
- Bear case
- Thesis kill criteria
- 三否决检查
- 最终研究流程状态

## 2. Source Log

| Source | Type | Date / Period | Used For | Reliability |
|---|---|---|---|---|
| [Marvell FY2027 Q1 Form 10-Q](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000019/mrvl-20260502.htm) | Company filing / SEC filing via Marvell IR | Filed May 28, 2026; quarter ended May 2, 2026 | 公司身份、交易所、收入、分业务收入、AI-related demand 表述、现金流、资产负债表、风险因素 | 一级来源 |
| [Marvell FY2026 Form 10-K](https://investor.marvell.com/sec-filings/all-sec-filings/content/0001835632-26-000011/mrvl-20260131.htm) | Company filing / SEC filing via Marvell IR | Filed March 11, 2026; fiscal year ended Jan 31, 2026 | FY2026 收入、利润、现金流、SBC、一次性出售收益、历史财务质量 | 一级来源 |
| [StockAnalysis MRVL overview](https://stockanalysis.com/stocks/mrvl/) | Public market data page | Last checked Jun 23, 2026; price shown at Jun 22, 2026 regular close and Jun 23, 2026 pre-market | 股价、市值、TTM revenue、P/E、Forward P/E、股息率、market session | 二级来源；indicative，需交叉验证 |
| [StockAnalysis MRVL statistics](https://stockanalysis.com/stocks/mrvl/statistics/) | Public market data / valuation page | Last updated Jun 23, 2026; price-based ratios updated through trading day | Market cap、EV、P/E、Forward P/E、EV/Sales、EV/EBITDA、P/FCF、financial ratios | 二级来源；indicative，需交叉验证 |
| [StockAnalysis MRVL financials](https://stockanalysis.com/stocks/mrvl/financials/) | Public standardized financial page | TTM period ended May 2, 2026 | TTM revenue、net income、EPS、FCF cross-check | 二级来源；用于交叉验证，不替代 filing |

未使用或未充分验证的来源：

- Earnings call transcript: 本次未完整验证逐字稿，管理层观点主要来自 10-Q 中的 MD&A 与风险因素。
- Investor presentation: 未能在本次测试中稳定打开官方 PDF，因此未作为关键结论来源。
- 媒体报道: 未作为关键数据依据，仅作为可选背景线索。

## 3. Company Identity

- Company: Marvell Technology, Inc.
- Ticker: MRVL
- Exchange: The Nasdaq Global Select Market
- Reporting currency: USD
- Latest fiscal year: FY2026, fiscal year ended Jan 31, 2026
- Latest quarter: Q1 FY2027, three months ended May 2, 2026
- Source: Marvell FY2027 Q1 Form 10-Q, filed May 28, 2026; Marvell FY2026 Form 10-K, filed March 11, 2026

## 4. Executive Summary

事实：

- MRVL 是一家 data infrastructure semiconductor 公司，10-Q 披露其解决方案覆盖 data center core 到 network edge，属于 fabless supplier。
- Q1 FY2027 net revenue 为 USD 2,417.8 million，较 Q1 FY2026 的 USD 1,895.3 million 增长 28%。来源：10-Q，期间 Q1 FY2027，币种 USD，GAAP/company disclosed。
- Q1 FY2027 data center revenue 为 USD 1,832.7 million，占总收入 76%。来源：10-Q，期间 Q1 FY2027，币种 USD，company disclosed。
- 公司在 10-Q 中说明 data center 增长受 AI-related demand 推动，产品包括 electro-optics、custom、storage、switching。该表述来自公司 filing，但公司未在该处单独披露 AI-only revenue。
- Q1 FY2027 operating cash flow 为 USD 638.8 million；purchases of property and equipment 为 USD 155.7 million；derived FCF 为 USD 483.1 million。来源：10-Q cash flow statement，期间 Q1 FY2027，币种 USD，company disclosed + derived calculation。
- StockAnalysis 显示 MRVL 在 Jun 22, 2026 regular close 为 USD 307.86，market cap USD 269.32 billion，EV USD 270.75 billion，P/E 106.34x，Forward P/E 67.93x，EV/Sales 31.06x，EV/EBITDA 99.83x，P/FCF 161.71x。来源为二级市场数据页，timestamp: Jun 22, 2026 4:00 PM EDT regular close / last updated Jun 23, 2026，currency USD，indicative。

推断：

- MRVL 的 AI 产业链受益不是纯叙事。data center 已经占收入大头，且 filing 将其增长与 AI-related demand 关联。
- 但“AI-specific revenue”没有在本次检索到的 filing 中单独披露，因此不能把全部 data center revenue 等同于 AI revenue。
- 当前估值隐含了非常高的持续增长和利润率改善预期，MRVL 需要在未来几个季度证明 data center 增长、FCF 转化和客户需求可持续。

假设：

- 本报告以 StockAnalysis 的 market data 作为 indicative valuation snapshot，尚需用 Nasdaq、Yahoo Finance、FactSet、Bloomberg 或券商终端交叉验证。
- 本报告将 FY2027 Q1 作为最新财报期，未纳入之后可能发生的未检索事件。

观点：

- 最终研究流程状态：观察池。
- 理由：真实 data center/AI 受益有官方 filing 支撑，但 AI-only revenue、backlog、design-win 细节和当前估值交叉验证仍不足，不建议升级为“候选”。

## 5. Business Overview

事实：

- 公司自述为 data infrastructure semiconductor solutions 供应商，覆盖 data center 和 communications and other end markets。
- MRVL 是 fabless 模式，主要能力包括 System-on-Chip architecture、analog / mixed-signal / digital signal processing，以及 security firmware。
- Q1 FY2027 收入按 end market:
  - Data center: USD 1,832.7 million，76% of total revenue。
  - Communications and other: USD 585.1 million，24% of total revenue。
- Q1 FY2027 收入按客户类型:
  - Direct customers: USD 1,188.9 million，49%。
  - Distributors: USD 1,228.9 million，51%。
- Q1 FY2027 地理发货口径:
  - China: USD 1,057.9 million，44%。
  - Taiwan: USD 519.7 million，21%。
  - United States: USD 170.5 million，7%。
  - Other: USD 669.7 million，28%。

推断：

- 公司当前收入集中在 data center，业务弹性和风险都更依赖 hyperscaler / AI infrastructure capex cycle。
- 发货目的地并不等于终端客户所在地，公司也在 10-Q 中提醒中国发货多数与非中国客户的制造地点有关。

待核实问题：

- Top customer concentration by named customer 未在本次 Q1 关键表格中逐一列示，需要进一步查 10-K customer concentration 章节。
- AI-specific revenue、custom ASIC / optics / switching 的单独收入拆分未披露。

## 6. AI Infrastructure Exposure

### 真实收入受益

事实：

- Q1 FY2027 data center revenue 已达到 USD 1,832.7 million，占总收入 76%。来源：10-Q，Q1 FY2027，USD，company disclosed。
- 公司在 10-Q 中说明 strong revenue growth from data center was driven by AI-related demand，涉及 electro-optics、custom、storage、switching。来源：10-Q MD&A，company disclosed management discussion。
- Q1 FY2027 data center revenue 同比增长约 27.2%，计算口径：USD 1,832.7 million / USD 1,440.6 million - 1，基于 10-Q 披露数据。

推断：

- MRVL 至少在 data center 维度已经有实质收入，而不是只有 AI 概念叙事。
- 但由于公司未在本次使用的 filing 中单独披露 AI-only revenue，不能确认 AI 相关收入占 data center revenue 的具体比例。

### 管理层表述

事实：

- 10-Q MD&A 将 data center 增长归因于 AI-related demand，并列出 electro-optics、custom、storage、switching 等产品类别。
- 10-Q 中也披露 Celestial AI acquisition 预期加速 next-generation AI and cloud data center connectivity strategy；XConn acquisition 扩展 PCIe / CXL switching portfolio 并增强 UALink scale-up switch team。

限制：

- Earnings call transcript 未在本次测试中完整验证，因此未引用逐字稿观点。
- Investor presentation 未能稳定打开，不作为关键结论依据。

### 已披露数据

- Data center revenue: USD 1,832.7 million，Q1 FY2027，company disclosed，USD。
- Data center share of total revenue: 76%，Q1 FY2027，company disclosed。
- Total net revenue: USD 2,417.8 million，Q1 FY2027，GAAP，company disclosed。
- AI-only revenue: 未披露。
- AI backlog / remaining performance obligations: 未披露或本次未检索到可靠披露。
- Named hyperscaler customer revenue: 未披露或本次未检索到可靠披露。

### backlog / design wins / customer programs

事实：

- 10-Q 风险因素明确提及 key customers、design wins 以及 data center end market concentration 的风险。

未验证：

- 具体 design wins、客户项目名称、订单规模、backlog 周期、可取消条款均未在本次可靠来源中确认。
- 媒体或分析师关于 Amazon、Microsoft、Google、Nvidia 等客户或合作的信息，本报告未作为关键事实使用，后续需要用公司公告、filing 或客户方公告交叉验证。

### 叙事受益

推断：

- MRVL 同时具备真实收入受益与叙事溢价。真实受益体现在 data center revenue 的规模与增长；叙事溢价体现在估值倍数极高，对未来 AI capex 和设计胜率的依赖很强。

### 未验证信息

- AI-only revenue 占比：未披露。
- AI backlog：未披露 / 待核实。
- 主要 hyperscaler 客户收入占比：待核实。
- 单个 custom ASIC program 的生命周期和利润率：待核实。
- 光互联、CXL、UALink 相关产品的独立商业化节奏：待核实。

## 7. Financial Quality Review

### Revenue growth

事实：

- Q1 FY2027 net revenue: USD 2,417.8 million，+28% YoY，source: 10-Q，GAAP/company disclosed。
- FY2026 net revenue: USD 8,194.6 million，FY2025 为 USD 5,767.3 million，source: 10-K，GAAP/company disclosed。
- Q1 FY2027 data center revenue: USD 1,832.7 million，占 76%，source: 10-Q。

质量判断：

- 收入增长有官方 filing 支撑，且 data center 占比高。
- 但增长来源中 AI-only、价格、销量、客户集中度、并购贡献拆分不足，仍需深挖。

### Gross margin

事实：

- Q1 FY2027 gross profit: USD 1,260.8 million，gross margin 52.1%。来源：10-Q，GAAP/company disclosed。
- Q1 FY2026 gross margin 为 50.3%，公司称改善主要来自 higher revenues 带来的 cost absorption，部分被 product mix 抵消。
- FY2026 gross profit: USD 4,180.7 million，gross margin 约 51.0%。来源：10-K，GAAP/company disclosed。

质量判断：

- 毛利率在最近季度有所改善，但 custom ASIC、光互联、定制项目和供应链成本可能带来未来毛利率波动。

### Operating margin

事实：

- Q1 FY2027 operating income: USD 339.4 million，operating margin 约 14.0%。来源：10-Q，GAAP/company disclosed。
- R&D expense: USD 652.3 million，占收入 27.0%。来源：10-Q。
- SG&A expense: USD 258.4 million，占收入 10.7%。来源：10-Q。

质量判断：

- R&D 投入较重，符合 advanced semiconductor / design-win 模式。
- Q1 SG&A 上升部分受 acquisition-related costs 影响，需要观察并购整合后费用率是否回落。

### Net income / EPS

事实：

- Q1 FY2027 net income: USD 34.5 million，diluted EPS USD 0.04。来源：10-Q，GAAP/company disclosed。
- FY2026 net income: USD 2,670.1 million，diluted EPS USD 3.07。来源：10-K，GAAP/company disclosed。
- FY2026 净利润包含 automotive ethernet business sale 的 pre-tax gain USD 1.8 billion。来源：10-K，company disclosed。

质量判断：

- FY2026 GAAP net income 受一次性出售收益影响，不宜简单外推。
- Q1 FY2027 GAAP 净利率很低，主要受 non-operating / acquisition-related 项目影响，需要用 operating income、FCF、Non-GAAP reconciliation 做进一步复核。

### Operating cash flow

事实：

- Q1 FY2027 operating cash flow: USD 638.8 million。来源：10-Q，company disclosed。
- FY2026 operating cash flow: USD 1,750.5 million。来源：10-K，company disclosed。

质量判断：

- 经营现金流为正且 Q1 明显高于 GAAP net income，但 Q1 working capital cash outflow 为 USD 211.6 million，需要继续跟踪。

### Free cash flow

事实：

- Q1 FY2027 operating cash flow: USD 638.8 million；purchases of property and equipment: USD 155.7 million；derived FCF = USD 483.1 million。来源：10-Q cash flow statement，company disclosed + derived calculation，USD。
- FY2026 CapEx: USD 354.1 million，derived FCF = USD 1,750.5 million CFO - USD 354.1 million CapEx = USD 1,396.4 million。来源：10-K，derived calculation，USD。
- StockAnalysis 显示 TTM FCF 为 USD 1.67 billion，period ended May 2, 2026，source: StockAnalysis financials / S&P Global, indicative。

待核实：

- FCF 的后续跟踪应统一使用同一口径：operating cash flow - purchases of property and equipment；若使用公司 Non-GAAP FCF，必须引用官方 reconciliation。

### Balance sheet

事实：

- Cash and cash equivalents: USD 3,843.6 million as of May 2, 2026。来源：10-Q，company disclosed。
- Accounts receivable, net: USD 1,871.7 million as of May 2, 2026。来源：10-Q。
- Inventories: USD 1,400.9 million as of May 2, 2026。来源：10-Q。
- Long-term debt: USD 4,961.3 million as of May 2, 2026。来源：10-Q。
- Short-term debt: USD 0 as of May 2, 2026。来源：10-Q。
- StockAnalysis 显示 total debt USD 5.28 billion，cash USD 3.84 billion，net cash USD -1.43 billion，last updated Jun 23, 2026；该 total debt 口径与 filing 的 debt line items 存在口径差异，需交叉验证。

质量判断：

- 流动性看起来较强，但 long-term debt 与并购支付增加使资产负债表复杂度提高。
- Goodwill 为 USD 13,883.5 million as of May 2, 2026，占 total assets USD 26,944.5 million 的约 51.5%，需要纳入红旗跟踪。

### Debt / cash

事实：

- Cash and cash equivalents: USD 3.84 billion。
- Long-term debt: USD 4.96 billion；short-term debt: USD 0。
- StockAnalysis enterprise value 使用的 debt/cash 口径显示 net debt 约 USD 1.43 billion，indicative。

判断：

- 债务压力目前不是第一层风险，但若 AI capex cycle 放缓、并购整合拖累利润，杠杆和 goodwill impairment 风险会抬升。

### SBC

事实：

- Q1 FY2027 stock-based compensation expense: USD 207.6 million。来源：10-Q cash flow discussion，company disclosed。
- FY2026 total stock-based compensation: USD 590.8 million。来源：10-K，company disclosed。

判断：

- Q1 SBC 占 revenue 约 8.6%，不低，尤其在高估值成长股中需要跟踪稀释和真实 FCF 质量。

### GAAP vs Non-GAAP

事实：

- 本报告可靠使用的数据主要为 GAAP/company disclosed filing 数据。
- Q1 adjusted EPS、Non-GAAP margin 等未从官方 release 或 presentation 稳定核验，本报告标记为待核实。

判断：

- 由于 acquisition-related costs、contingent consideration fair value、amortization、SBC 较大，MRVL 的 GAAP 与 Non-GAAP 差异可能很重要。候选判断前必须补齐官方 reconciliation。

### AR / inventory / working capital red flags

事实：

- AR 从 Jan 31, 2026 的 USD 2,186.6 million 降至 May 2, 2026 的 USD 1,871.7 million。
- Inventory 从 Jan 31, 2026 的 USD 1,388.0 million 升至 May 2, 2026 的 USD 1,400.9 million。
- Q1 FY2027 working capital cash outflow 为 USD 211.6 million，公司解释主要由 accounts payable、accrued employee compensation 和 accrued liabilities 下降推动，部分由 AR 下降抵消。

判断：

- 本季度未见“AR 增速明显快于收入”的直接红旗。
- Inventory 绝对规模高，需要跟踪 AI 需求若放缓是否出现库存跌价或订单取消风险。

## 8. Valuation Review

市场数据状态：部分核实。所有市场数据来自二级来源 StockAnalysis，需用 Nasdaq / Yahoo Finance / Bloomberg / FactSet 等交叉验证。以下 valuation snapshot 以 regular close 为主，不代表实时交易价格。

| Metric | Value | Source + timestamp + session + currency + basis |
|---|---:|---|
| Current price | USD 307.86 | StockAnalysis overview, Jun 22, 2026 4:00 PM EDT, regular close, USD, real-time/market data page |
| Pre-market reference | USD 280.93 | StockAnalysis overview, Jun 23, 2026 4:18 AM EDT, pre-market, USD, indicative; not used for valuation multiples below |
| Market cap | USD 269.32 billion | StockAnalysis overview/statistics, last checked Jun 23, 2026, based on regular close snapshot, USD, indicative |
| Enterprise value | USD 270.75 billion | StockAnalysis statistics, last updated Jun 23, 2026, USD, indicative; provider EV口径 |
| P/E | 106.34x | StockAnalysis overview/statistics, last updated Jun 23, 2026, trailing/TTM, USD price basis, indicative |
| Forward P/E | 67.93x | StockAnalysis statistics, last updated Jun 23, 2026, forward, USD price basis, indicative |
| EV/Sales | 31.06x | StockAnalysis statistics, last updated Jun 23, 2026, TTM sales basis, USD, indicative |
| EV/EBITDA | 99.83x | StockAnalysis statistics, last updated Jun 23, 2026, TTM EBITDA basis, USD, indicative |
| P/FCF | 161.71x | StockAnalysis statistics, last updated Jun 23, 2026, TTM FCF basis, USD, indicative |
| Dividend yield | 0.08% | StockAnalysis overview/statistics, last updated Jun 23, 2026, USD, indicative |

### Peer context if available

未验证。需要后续纳入 Broadcom、Astera Labs、Coherent、Lumentum、Nvidia、AMD、Monolithic Power、Credo 等可比公司，但应按业务线拆分，避免简单用单一 peer group。

### Historical context if available

部分未验证。StockAnalysis 显示 MRVL 52-week price change +318.80%，52-week range USD 61.44 - USD 329.88，source: StockAnalysis statistics, last updated Jun 23, 2026，USD，indicative。历史 valuation range 需后续用同一口径数据补齐。

### Market-implied expectations

事实基础：

- EV: USD 270.75 billion，source: StockAnalysis statistics，Jun 23, 2026，USD，indicative。
- TTM revenue: USD 8.72 billion，source: StockAnalysis statistics / financials，period ended May 2, 2026，USD，indicative and cross-checked against company filings。
- TTM FCF: USD 1.67 billion，source: StockAnalysis statistics / financials，period ended May 2, 2026，USD，indicative。

推断与情景反推：

- EV/Sales 约 31x 意味着市场不仅在定价当前 revenue，而是在定价多年高增长、margin expansion 和 AI design-win 成功。
- 若长期 EV/Sales 回落到 15x 这种仍偏高的成长股倍数，在 EV 不变的静态假设下，收入需达到约 USD 18.1 billion，约为当前 TTM revenue 的 2.1 倍。该计算为估值反推，不是预测。
- 若长期 P/FCF 回落到 60x，维持当前 market cap 需要约 USD 4.5 billion FCF，约为当前 TTM FCF 的 2.7 倍；若回落到 40x，则需要约 USD 6.7 billion FCF，约为当前 TTM FCF 的 4.0 倍。该计算为情景假设，不是目标价。
- Forward P/E 67.93x 对应市场已预期 EPS 显著增长。候选判断前必须核实 forward EPS 来源、时间戳和 analyst estimate 分布。

估值判断：

- 估值不是“数据不足”，而是“估值要求极高”。在没有 AI-only revenue、backlog、design-win economics 和客户集中度细节前，估值安全边际偏弱。

## 9. Bull Case

事实支撑：

- Data center 已是公司最大收入来源，Q1 FY2027 占 76%。
- 公司 filing 将 data center 增长与 AI-related demand 关联，涉及 electro-optics、custom、storage、switching。
- Q1 FY2027 gross margin 52.1%，同比提升 1.8 percentage points。
- Operating cash flow 为正，FY2026 和 TTM FCF 均为正。
- Celestial AI 与 XConn acquisition 与 AI/cloud data center connectivity、PCIe/CXL switching、scale-up networking 方向一致。

推断：

- 如果 hyperscaler AI capex 持续、custom silicon 与 optical interconnect 需求继续扩张，MRVL 可能受益于 data center architecture 从计算芯片向互联、光、电、存储和交换整体升级。
- 若新并购资产转化为可规模化收入，且 data center growth 不以明显毛利率牺牲为代价，当前高估值有部分基本面支撑。

观点：

- MRVL 是一个值得进入 AI infrastructure watchlist 的标的，但需要持续验证估值与增长兑现。

## 10. Bear Case

事实支撑：

- 当前 valuation snapshot 显示 EV/Sales 31.06x、EV/EBITDA 99.83x、P/FCF 161.71x，估值极高。
- Q1 FY2027 GAAP net income 仅 USD 34.5 million，GAAP diluted EPS USD 0.04，明显低于 market cap 所隐含的长期盈利要求。
- Goodwill 占资产比例高，Q1 FY2027 goodwill USD 13.88 billion，占 total assets 约 51.5%。
- 公司披露 data center end market、key customers、AI capex sustainability、export restrictions、manufacturing partner concentration 等风险。
- Q1 SBC USD 207.6 million，占收入约 8.6%。

推断：

- 若 AI capex 放缓、custom ASIC design wins 延迟或客户自研/替代方案推进，MRVL 的增长叙事可能迅速被重估。
- 如果 data center 增长更多来自补库存或短期项目 ramp，而不是长期高可见度订单，当前估值可能缺乏支撑。
- 若定制项目压缩毛利率，或并购整合导致费用、摊销和 SBC 持续偏高，FCF 质量会低于市场预期。

观点：

- Bear case 的核心不是业务不存在，而是当前价格对未来成功的容错率低。

## 11. Thesis Kill Criteria

以下 kill criteria 用于研究流程跟踪，不是交易指令：

1. Data center revenue 连续两个季度明显低于管理层或市场预期，且公司无法给出可验证解释。
2. 公司仍无法披露或解释 AI-related revenue 与非 AI data center revenue 的区分，且市场继续按纯 AI 高增长资产定价。
3. Gross margin 或 FCF margin 因 custom projects、供应链成本、价格竞争持续恶化，且未见改善路径。
4. Top customer / design-win 发生重大流失，或 hyperscaler capex 明确转向替代技术路线。
5. AI infrastructure capex 明显放缓，客户库存调整导致订单或收入下修。
6. Inventory 或 AR 出现异常增长，明显快于 revenue，并且管理层解释不足。
7. SBC、并购对价、摊销或重组项目导致 GAAP 与 Non-GAAP 差异持续扩大。
8. Goodwill 或 acquired intangibles 出现 impairment 信号。
9. Export restrictions、China exposure 或供应链地缘风险实质性影响 data center / communications 收入。

## 12. Three Veto Check

| Veto Item | Result | Evidence | Notes |
|---|---|---|---|
| 商业模式不可理解或收入真实性无法验证 | 未触发 | 10-Q 和 10-K 可验证 revenue、end-market split、company identity；Q1 FY2027 data center revenue USD 1,832.7 million | AI-only revenue 未披露，但不等于总收入真实性不可验证 |
| 财务质量明显恶化且无法解释 | 未触发，但需跟踪 | Q1 OCF USD 638.8 million；gross margin 52.1%；但 GAAP net income 低、SBC 高、working capital cash outflow 存在 | 需要补充 official Non-GAAP reconciliation、应收/库存周转、并购影响 |
| 估值严重依赖不可验证的远期叙事 | 未硬触发，但接近候选门槛 | EV/Sales 31.06x、P/FCF 161.71x；AI-only revenue、backlog、design-win economics 未披露 | 不足以进入“候选”，但可进入“观察池”；若要升级候选，必须补齐估值与订单验证 |

三否决结论：

- 未触发必须“排除”的硬否决。
- 第三项存在高风险，需要阻止直接升为“候选”。
- 允许最终状态为“观察池”，并明确重大风险与待核实事项。

## 13. Nine-Score Framework

九项评分本次用于验收测试。评分是研究流程工具，不是投资建议。总分满分 45。

| Dimension | Score 1-5 | Evidence | Confidence |
|---|---:|---|---|
| 行业空间 | 4 | AI data center、光互联、custom silicon、switching 需求方向有 filing 支撑 | 中 |
| 竞争格局 | 3 | 受益方向明确，但竞争对手、客户自研、替代互联技术和 pricing power 未充分验证 | 中低 |
| 商业模式 | 3 | Fabless semiconductor，收入真实可查；但项目制、客户集中与周期性较强 | 中 |
| 护城河 | 3 | SoC、electro-optics、custom、switching、CXL/UALink 资产有战略价值；design-win 持续性未核实 | 中低 |
| 管理层 | 3 | 并购与资本配置积极，FY2026 回购与分红存在；但并购整合、SBC 和估值沟通需跟踪 | 中 |
| 财务质量 | 3 | Revenue、gross margin、OCF/FCF 较好；GAAP net income、SBC、goodwill、working capital 需跟踪 | 中 |
| 增长确定性 | 3 | Q1 data center 增长和 AI-related demand 有公司披露；backlog、AI-only revenue 未披露 | 中 |
| 估值安全边际 | 1 | EV/Sales 31.06x、P/FCF 161.71x，安全边际弱 | 中 |
| 催化剂与风险收益比 | 3 | AI data center demand、Celestial/XConn 整合、后续季度指引可能是催化剂；估值回撤风险大 | 中 |

Total score: 26 / 45

评分解读：

- 强项：行业空间、真实 data center revenue、AI demand filing 支撑。
- 弱项：估值安全边际、AI-only revenue 与 backlog 缺失、客户集中和技术替代风险。
- 最大不确定性：市场当前是否已经把 FY2027-FY2028 高增长和利润率改善充分甚至过度定价。

## 14. Final Research Status

最终研究流程状态：观察池

理由：

- 事实层面：MRVL 真实 data center revenue 已经占收入 76%，并且公司 filing 将 data center 增长与 AI-related demand 关联。
- 推断层面：MRVL 不只是 AI 概念叙事，但目前不能把 data center revenue 全部视作 AI-only revenue。
- 假设层面：若 AI capex 和 custom/optical design wins 延续，MRVL 仍有观察价值。
- 观点层面：估值过高、AI-only revenue 未披露、backlog/design-win economics 未验证，因此不升级为“候选”。

状态说明：

- “观察池”是研究流程状态，不是买入、卖出或仓位建议。
- 若后续补齐客户项目、订单可见度、Non-GAAP reconciliation、同业估值和历史估值区间，可重新评估是否进入“候选”或“等待更好价格”。

Next Checks:

1. 获取并核对官方 Q1 FY2027 earnings release 与 earnings call transcript。
2. 核实 management guidance 中 FY2027 / FY2028 data center 或 total revenue outlook 的官方原文。
3. 查找是否披露 AI-only revenue、AI-related bookings、backlog、remaining performance obligations 或 design-win economics。
4. 对比 AVGO、ALAB、CRDO、COHR、LITE、NVDA、AMD 等 peer valuation，按业务线而非单一行业标签比较。
5. 用 Nasdaq / Yahoo Finance / Bloomberg / FactSet 交叉验证 current price、market cap、EV、Forward P/E、EV/Sales、EV/EBITDA、P/FCF。
6. 建立季度跟踪表：data center revenue growth、gross margin、OCF/FCF、SBC、AR、inventory、customer concentration、China/export exposure。
7. 分析 Celestial AI 与 XConn acquisitions 对 revenue、gross margin、SBC、goodwill 和 intangibles 的影响。
8. 复核 10-K risk factors 中 key customer concentration 与 manufacturing partner concentration。

## 15. Skill Behavior Review

- 是否默认输出完整研究报告？是。本次输出为完整 live-source research test report，没有默认降级为 Obsidian 卡片。
- 是否正确使用 AI overlay？是。报告区分了真实 revenue exposure、管理层 filing 表述、AI-only revenue 未披露、叙事溢价、hyperscaler capex、技术替代、客户集中、毛利率压缩风险。
- 是否正确执行三否决？是。最终状态前执行了三否决，并把估值叙事风险作为候选门槛前的限制。
- 是否正确使用九计分？是。虽然本次不是正式 deep dive，但作为验收测试运行九项评分，并标注 confidence。
- 是否避免了无来源数据？基本是。公司财务数字来自 filing；市场数据来自二级来源并标注 indicative / 待交叉验证。
- 是否没有默认输出 Obsidian？是。未输出 Obsidian 卡片。
- 是否有过度保守或过度宽松的问题？整体没有。结论清晰为“观察池”，但没有给出买卖建议；同时没有因为数据缺口直接“排除”。
- 哪些模板或规则需要 v0.1.1 小修？见 Issues Found。

## 16. Issues Found

| Issue | Severity | Suggested Fix | File to Modify Later |
|---|---|---|---|
| AI overlay 可以更明确要求区分 “data center revenue” 与 “AI-only revenue”，避免把 data center 全部当 AI 收入 | Medium | 在 AI framework 中加入强制字段：AI-only disclosed? data center proxy? attribution confidence? | `references/ai-infrastructure-stock-framework.md` |
| 市场数据不可得或来自二级页面时，Skill 需要更明确的 stale/indicative snapshot fallback 规则 | Medium | 在 citation standard 和 valuation note 中补充：若 current data 无法交叉验证，允许使用带 session/timestamp 的 indicative snapshot，但必须标注待核实 | `references/citation-standard.md`, `templates/valuation-note.md` |
| 估值模板可加强 “market-implied expectations” 的计算示例 | Low | 增加 EV/Sales、P/FCF、Forward EPS implied 的简洁反推方法 | `references/valuation-methods.md`, `templates/valuation-note.md` |
| 财务质量 checklist 可加入 goodwill / acquisition accounting 专项 | Low | 增加 goodwill as % assets、intangibles、contingent consideration、pro forma contribution、impairment risk | `references/financial-quality-checklist.md` |
| 九项评分输出可以要求每项 confidence 与核心 missing evidence | Low | 在 scoring output template 中补充 confidence 和 missing evidence 字段 | `scoring/scoring-output-template.md` |

## 17. Recommendation

- 是否建议保留当前 v0.1？Yes。当前 v0.1 能稳定输出完整研究报告、正确处理来源约束、三否决、bear case、kill criteria 和 AI overlay。
- 是否建议做 v0.1.1 小修？Yes。建议先做小修，重点补充 AI-only revenue vs data center proxy、market data fallback、goodwill/acquisition accounting 和 scoring confidence。
- 是否建议进入 v0.2 数据脚本阶段？暂不建议立即进入。先完成 v0.1.1 文档小修后，再考虑 EDGAR / market data 脚本等 v0.2 功能。
