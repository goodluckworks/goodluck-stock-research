# Valuation Note

## 使用规则

- 不允许留空字段。
- 未知内容必须明确写：`未披露`、`未验证`、`暂无可靠来源`、`不适用` 或 `待核实`。
- 所有关键未知项必须进入 `来源附录` 的待核实问题。
- 最终状态如有输出，必须使用 `references/status-taxonomy.md` 定义的枚举。
- 当前股价、市值、EV 和估值倍数必须包含 source + timestamp + market session + currency；估值倍数还必须注明 trailing / forward / TTM / NTM 口径。
- 当市场数据来自 StockAnalysis、Yahoo Finance、CompaniesMarketCap、Macrotrends 等二级公开页面时，必须标注 `indicative` 或 `待交叉验证`，记录实时/延迟/估算/页面快照性质；若无法确认更新时间，写 `timestamp 未验证`。
- 不允许把二级市场数据当作公司官方披露；估值结论必须说明是否依赖未交叉验证的市场数据。
- 高增长公司必须做市场隐含预期反推；周期股必须区分 peak earnings 和 normalized earnings。
- 使用 v0.2 本地脚本时，必须引用 input file、generated at、source、basis、source status、reporting period、currency、timestamp / market session（适用时）、关键假设和 data limitations。
- DCF 必须注明 `FCFF / UFCF / FCFE`、discount rate 类型、valuation bridge、net debt 是否扣减及原因。
- 汇总金额必须注明 `amount_unit`，每股价值必须注明 `per_share_unit`。
- Net debt 必须记录 cash base used、net debt basis，以及短期投资是否适合纳入。
- Peer comps 必须区分 blended peer statistics 与 core comparable statistics，并记录 comparability notes。
- P/E implied expectations 必须记录 earnings basis used、reported GAAP net income、normalized net income（如有）和特殊项目 caution。
- 并购驱动公司必须记录 goodwill / assets、intangibles / assets、acquisition amortization、integration costs、organic growth 与 debt bridge；不能仅凭 adjusted earnings 忽略长期重复的并购费用。
- 多分部公司必须说明 consolidated multiples 是否被 segment mix 扭曲；软件与半导体等明显不同业务应考虑 SOTP 或分部参考，不能机械使用 blended peer median。
- 脚本输出必须标记为 `基于所列输入的计算结果`，不能替代原始来源核验或最终研究判断。
- 正式报告开头或结尾只保留一次：`本文仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。`

## 研究对象与范围

- Ticker：
- Exchange：
- Company：
- Reporting currency：
- Latest reporting period：
- Research objective：
- Investment horizon：
- Data date：

## 当前市场数据

- 当前股价：数值 + 来源 + 时间戳 + market session + 币种 + 实时/延迟/估算
- 市值：数值 + 来源 + 时间戳 + market session + 币种 + 计算口径
- 现金及短期投资：
- Cash base used：
- Net debt basis：cash_only / cash_plus_short_term_investments / user_provided_cash_and_investments / unknown
- 总债务：
- 净现金 / 净债务：
- 企业价值 / EV：数值 + 来源 + 时间戳 + market session + 币种 + 计算口径
- 股本数量：
- 数据时间戳：
- 市场时区：
- Market session：regular close / pre-market / after-hours / intraday
- 数据性质：实时 / 延迟 / 估算 / 页面快照 / timestamp 未验证
- 交叉验证状态：已交叉验证 / indicative / 待交叉验证
- 来源：

## 当前估值倍数

| 指标 | 当前 | 期间 | 币种 | 口径 | 来源 | 时间戳 | Market session | 数据性质 | 交叉验证状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P/E |  |  |  | trailing / TTM |  |  |  | 实时 / 延迟 / 估算 / 页面快照 | 已交叉验证 / indicative / 待交叉验证 |
| Forward P/E |  |  |  | forward / FY1 / NTM |  |  |  | 实时 / 延迟 / 估算 / 页面快照 | 已交叉验证 / indicative / 待交叉验证 |
| EV/Sales |  |  |  | TTM / NTM / FY1 |  |  |  | 实时 / 延迟 / 估算 / 页面快照 | 已交叉验证 / indicative / 待交叉验证 |
| EV/EBITDA |  |  |  | TTM / NTM / FY1 |  |  |  | 实时 / 延迟 / 估算 / 页面快照 | 已交叉验证 / indicative / 待交叉验证 |
| P/FCF |  |  |  | TTM / NTM / normalized |  |  |  | 实时 / 延迟 / 估算 / 页面快照 | 已交叉验证 / indicative / 待交叉验证 |
| PEG |  |  |  | growth source required |  |  |  | 实时 / 延迟 / 估算 / 页面快照 | 已交叉验证 / indicative / 待交叉验证 |

## 历史估值

- 历史区间：
- 当前分位：
- 与自身历史相比：
- 历史区间是否受异常周期影响：

## 同业估值

| 公司 | Ticker | Peer group | Comparability | Core stats | 估值指标 | 增长 | Margin | 说明 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |

- Blended peer median：
- Core comparable median：
- Core comparable 样本数量：
- Core comparable sample 是否过小：

## Bear / Base / Bull Case

### Bear Case

- 关键假设：
- 估值方法：
- 估值区间：
- 触发条件：
- 失效条件：

### Base Case

- 关键假设：
- 估值方法：
- 估值区间：
- 触发条件：
- 失效条件：

### Bull Case

- 关键假设：
- 估值方法：
- 估值区间：
- 触发条件：
- 失效条件：

## 市场隐含预期

- 当前估值隐含的 revenue growth：
- EV/Sales 反推：若 EV 不变，收入需要达到多少才能回落到合理成熟期 EV/Sales？
- P/E / Forward P/E 反推：当前价格需要 EPS 未来几年达到什么水平，EPS growth 来源是收入、margin、税率、回购还是 Non-GAAP 调整？
- Earnings basis used：reported_gaap / normalized / non_gaap / adjusted / unknown
- Reported GAAP net income：
- Normalized net income / EPS（如有可靠来源）：
- Earnings basis notes / caution：
- P/FCF 反推：当前市值需要多高 FCF、FCF margin 和 FCF growth 才能支撑？
- 当前估值隐含的 margin：
- 当前估值隐含的 FCF conversion：
- 当前估值隐含的 terminal multiple：
- 需要几年达到成熟期估值倍数：
- 如果增长低于预期，估值下修风险：
- 需要满足的关键经营条件：
- 哪些假设最脆弱：

## 敏感性分析

| 变量 | Bear | Base | Bull |
| --- | --- | --- | --- |
| Revenue CAGR |  |  |  |
| Gross margin |  |  |  |
| Operating margin |  |  |  |
| FCF margin |  |  |  |
| Discount rate / multiple |  |  |  |

## 本地计算工具记录（如使用）

- Tool：`ratio_calculator.py` / `dcf_sensitivity.py` / `peer_comps_table.py` / `implied_expectations.py` / `不适用`
- Input file：
- Generated at：
- Reporting period：
- Currency：
- Amount unit：
- Per-share unit：
- FCF type：
- Valuation bridge：
- Net debt treatment：
- Cash base used：
- Net debt basis：
- Input basis：
- Source：
- Source status：
- Timestamp：
- Market session：
- 关键输入假设：
- 计算结果引用：
- 与原始披露的交叉验证：
- Data limitations：
- 是否依赖未验证或 indicative 数据：
- GAAP 特殊项目与 normalized metrics：
- Acquisition accounting fields / ratios：
- Segment mix / SOTP treatment：
- Earnings basis used：
- Peer group / comparability / core stats：
- Forward growth provenance：consensus / company guidance / derived / analyst assumption / unknown

说明：以上结果是基于所列输入的可复现计算，不是独立验证的数据，也不是最终投资结论。

## 安全边际

- 下行情景保护：
- 资产负债表保护：
- 现金流保护：
- 估值折价：
- 不足之处：

## 估值结论

估值应以研究语境下的区间表达，并说明关键假设与失效条件：

```text
在当前资料下，研究估值区间更接近 [区间]；Base Case 估值区间为 [区间]。关键假设包括 [增长 / margin / FCF / multiple / discount rate]。若 [失效条件] 出现，该估值结论应下修或重新评估。
```

## 估值失效条件

-
-
-

## 来源附录

-
