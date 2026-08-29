# Research Workflow

这是完整股票研究流程。根据任务深度可压缩，但不得跳过来源质量、反方观点、kill criteria 和 next checks。

## Step 1：识别研究对象

先确认并记录：

- ticker。
- exchange。
- 公司全名。
- reporting currency。
- latest reporting period。
- 当前研究使用的数据日期。
- 是否存在 ADR、双重上市、不同 share class 或 VIE 结构。

若无法确认，应列入 `next checks`。

## Step 2：确定研究目的

明确研究输出的用途：

- 快速过滤。
- 观察池加入。
- 候选公司深挖。
- 财报后复核。
- 持仓复核。
- 估值复核。
- 行业主题筛选。
- AI supply chain overlay。

同时明确 investment horizon：

- 1-2 个季度。
- 1 年。
- 3-5 年。
- 周期底部到周期中段。
- 事件驱动。

## Step 3：收集核心资料

优先收集：

- 最新 annual report / 10-K / 20-F。
- 最新 quarterly report / 10-Q / interim report。
- 最新 earnings release。
- 最新 earnings call transcript。
- Investor presentation。
- 最近重大公告或 8-K。
- 交易所公告和监管文件。

记录资料覆盖范围和缺口：

```text
已覆盖：FY2025 10-K、Q1 FY2026 10-Q、Q1 earnings call。
未覆盖：最新 consensus estimate、同业估值表、客户订单验证。
```

### 可选：本地数据计算工具层

如果用户或 Agent 已提供本地 CSV / JSON，可读取 `scripts/README.md` 和对应 `schemas/`，选择：

- `ratio_calculator.py`：财务比率。
- `dcf_sensitivity.py`：简化 DCF 敏感性。
- `peer_comps_table.py`：同业估值表。
- `implied_expectations.py`：市场隐含预期反推。

脚本不自动获取数据。运行前必须检查输入文件的 source、basis、reporting period、currency、timestamp / source date、market session（适用时）、source status 和金额单位。报告引用脚本结果时，应同时引用输入文件及其来源，并标记为 `基于所列输入的计算结果`。

脚本输出不能替代原始 filing、业务分析、bear case、kill criteria、三否决或最终研究状态。

### v0.3 design：future evidence adapter layer

v0.3 当前只有设计文档，不包含 live adapter。未来 adapter 若经批准实现，必须遵循：

```text
Source
-> Raw Evidence Snapshot
-> Source Manifest
-> Field Provenance
-> Normalized Input CSV / JSON
-> v0.2.x Calculation Tools
-> Research Report
```

- Adapter 只负责只读 evidence collection / receipt 和 normalization。
- Adapter 不输出 investment conclusion、研究状态、thesis、bear case 或 portfolio action。
- Raw evidence、source manifest 和 field provenance 必须先落地。
- Normalized input 必须映射到现有四类 schema。
- v0.2.x scripts 仍只读取本地文件。
- 报告层必须人工审查 warnings、unresolved fields、freshness、source conflicts 和 assumptions。

设计规范见：

- `references/data-adapter-design.md`
- `references/source-provenance-policy.md`
- `references/freshness-cache-policy.md`
- `references/adapter-failure-modes.md`

## Step 4：业务拆解

回答：

- 公司卖什么产品或服务？
- 客户是谁？
- 收入如何确认？
- 收入来自哪些 segment、region、product line、customer type？
- 毛利率和资本强度由什么决定？
- 增长来自价格、销量、并购、汇率、产品 mix、会计口径，还是周期反弹？
- 是否存在客户集中、供应商集中或渠道依赖？

输出时区分：

- 已披露的 revenue mix。
- 未披露但可合理推断的业务结构。
- 仍需验证的业务假设。

## Step 5：行业与竞争格局

分析：

- 行业空间和增长驱动。
- 周期性、渗透率、替代技术和监管变量。
- 主要竞争对手。
- 客户议价能力和供应商议价能力。
- 新进入者威胁。
- 公司相对份额、产品差异化和成本位置。

避免只写行业故事。必须连接到公司收入、利润、现金流或估值。

## Step 6：财务质量分析

使用 `financial-quality-checklist.md`。至少覆盖：

- 收入质量。
- 利润质量。
- 现金流质量。
- 资产负债表。
- 股本稀释和回购质量。
- GAAP 与 Non-GAAP 差异。
- 红旗和需要解释的异常变化。

核心问题：

```text
利润是否转化为现金？
增长是否依赖一次性因素？
Non-GAAP 是否越来越远离 GAAP？
资产负债表能否支撑当前战略？
```

## Step 7：估值分析

使用 `valuation-methods.md`。选择适合公司的框架：

- 稳定盈利公司：P/E、Forward P/E、P/FCF、DCF。
- 高增长公司：EV/Sales、gross profit multiple、unit economics、market-implied expectations。
- 周期股：normalized earnings、mid-cycle multiple、asset value。
- 银行保险：P/B、ROE、资本充足率、承保质量。
- REITs：FFO/AFFO、NAV、cap rate、负债期限。
- 资源股：commodity cycle、reserve life、unit cost、NAV。
- SaaS：ARR growth、NRR、gross margin、Rule of 40、FCF margin。
- 半导体：cycle position、gross margin, inventory, design wins, capex exposure。

估值结论必须使用区间，不给单点确定目标价。

若使用 v0.2 本地工具：

- DCF 敏感性读取用户提供的假设，不将 implied value per share 写成确定性目标价。
- Peer comps 的均值、中位数和相对位置只作为描述性证据，不直接形成买卖判断。
- Market-implied expectations 是静态反推框架，不是预测模型。
- 在估值章节列出 input file、generated at、source status、关键假设和 data limitations。

## Step 8：风险与反方观点

必须输出：

- Bear case。
- Top 5 risks。
- Thesis kill criteria。
- Early warning indicators。
- Next 1-2 quarter checks。

Bear case 要足够强，不能只是轻描淡写的“宏观不好”。

## Step 9：催化剂与跟踪指标

催化剂可能包括：

- 财报。
- 管理层指引变化。
- 新产品发布。
- 客户订单或 design win。
- 监管变化。
- 行业价格拐点。
- 资本回报。
- 资产剥离或并购。

跟踪指标应可验证：

- Revenue growth。
- Segment margin。
- Backlog / RPO。
- Inventory days。
- FCF margin。
- Customer concentration。
- Capex intensity。
- Guidance revision。
- Valuation multiple relative to history and peers。

## Step 10：三否决硬门槛与九项评分

任何最终状态判断前，都必须先使用 `scoring/three-veto-nine-score.md` 检查三项否决。

先检查三项否决：

1. 商业模式不可理解或收入真实性无法验证。
2. 财务质量明显恶化且无法解释。
3. 估值严重依赖不可验证的远期叙事。

若触发任一否决项，最终状态只能是：

- 排除。
- 数据不足，暂不判断。
- 观察池，但必须明确说明重大风险和待核实事项。

未触发否决后，再判断是否需要九项评分。九项评分只在以下场景强制执行：

- Company deep dive。
- 候选判断。
- 持仓复核。
- 多公司对比。
- 用户明确要求评分。

评分是研究辅助工具，不可替代来源验证和逻辑判断。

## Step 11：形成结论

最终状态必须先查 `references/status-taxonomy.md`，并且只能使用：

- 排除。
- 观察池。
- 候选。
- 深入研究。
- 小仓位跟踪。
- 持仓复核。
- 等待更好价格。
- 数据不足，暂不判断。

结论必须说明：

- 关键事实。
- 支持 thesis 的证据。
- 反方观点。
- 最大不确定性。
- 估值是否已经反映乐观预期。
- 何时应该改变判断。

## Step 12：输出研究报告与可选归档

默认输出顺序：

1. 完整研究报告。
2. 数据来源与待核实问题。
3. 最终研究状态。
4. 是否需要追加 Obsidian 卡片。

除非用户明确要求，否则不要只输出 Obsidian 格式。Obsidian 是归档格式，不是唯一报告格式。

根据用途选择模板：

- 快速卡片：`templates/quick-tearsheet.md`。
- 深度报告：`templates/company-deep-dive.md`。
- 财报更新：`templates/earnings-update.md`。
- 估值备忘录：`templates/valuation-note.md`。
- Thesis 跟踪：`templates/thesis-tracker.md`。
- Obsidian 公司卡片：`templates/obsidian-company-card.md`，仅在用户明确要求 Obsidian 输出时直接使用。

输出应保留来源附录和 next checks，方便未来复核。如果完整报告适合归档，但用户没有要求 Obsidian，可在报告末尾询问是否需要追加生成 Obsidian 公司卡片。
