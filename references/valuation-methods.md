# Valuation Methods

估值用于判断当前价格隐含了什么预期，以及风险收益是否合理。估值不是确定性目标价，必须以区间和情景表达。

## 基本输出要求

每次估值分析至少包含：

- 当前估值。
- 历史估值区间。
- 同业估值。
- 市场隐含预期。
- 关键敏感性。
- 安全边际。
- 估值失效条件。

若缺少股价、市值、净现金/净债务、利润或现金流数据，应明确写入缺口，不能强行计算。

## v0.2 本地计算工具

当用户或 Agent 提供符合 `schemas/` 的本地 CSV / JSON 时，可以运行：

- `scripts/dcf_sensitivity.py`：简化 FCF DCF 与 discount rate / terminal growth 敏感性。
- `scripts/peer_comps_table.py`：同业倍数、统计区间和目标公司相对位置。
- `scripts/implied_expectations.py`：EV/Sales、P/E、P/FCF 的成熟期 scale-up 反推。
- `scripts/ratio_calculator.py`：为估值使用的财务质量与现金流比率提供计算辅助。

使用规则：

- 脚本不自动获取、更新或验证数据。
- 运行前检查 source、basis、reporting period、currency、timestamp / source date、market session（适用时）、source status 和金额单位。
- 在报告中将结果标记为 `基于所列输入的计算结果`，并引用输入文件。
- 脚本结果与公司披露冲突时，以核对后的原始披露为准。
- DCF、同业估值和隐含预期结果只能作为研究辅助，不能单独决定最终状态。
- Net debt 必须记录 cash base：cash only、cash plus short-term investments，或用户已核实的合并口径。
- Peer comps 必须区分 blended statistics 与用户分类的 core comparable statistics。
- P/E implied expectations 必须显示 reported GAAP 或 normalized earnings basis；工具不得自行生成 normalized earnings。
- 对并购驱动公司，估值必须同时检查 goodwill / assets、intangibles / assets、acquisition amortization、integration costs、organic growth 与 debt bridge；相关 ratio 输出不能自动证明 management-adjusted earnings 更接近经济利润。
- 对半导体加软件等复杂分部公司，consolidated peer median 只能作为宽泛参考；segment mix、资本强度与会计口径差异仍需在报告层人工拆解，必要时使用 SOTP。

## 相对估值

### P/E

适用于盈利相对稳定、会计利润质量较高的公司。

注意：

- 检查 EPS 是 GAAP 还是 Non-GAAP。
- 检查是否受一次性税率、减值、汇兑或资产出售影响。
- 对周期股不能使用周期顶部 EPS 外推。

### Forward P/E

适用于市场对未来盈利有较稳定预期的公司。

注意：

- 必须注明 consensus 来源和时间戳。
- 分析预期是否已经包含乐观增长和 margin 扩张。
- 如果 forward EPS 的假设不可见，应降低结论置信度。
- Reported GAAP earnings 如受重大非经营或一次性项目影响，应补充 normalized bridge；没有可靠 bridge 时保留 GAAP 并明确 caution。

### EV/Sales

适用于高增长、利润尚未成熟、或短期利润被投资阶段压低的公司。

注意：

- 高增长公司不能只看 P/E。
- EV/Sales 必须结合 gross margin、retention、operating leverage 和 FCF path。
- 低毛利、低留存或高资本强度公司不应享受高 SaaS 式 sales multiple。

### EV/EBITDA

适用于资本结构差异较大、折旧摊销影响较明显的公司。

注意：

- EBITDA 不能替代现金流。
- 对高维护性 capex 公司，应结合 FCF。
- 对租赁负债较重的公司，应注意 EV 和 EBITDA 的口径一致。

### P/FCF

适用于现金流稳定且 capex 需求可解释的公司。

注意：

- 判断 FCF 是否由 working capital timing 拉动。
- 检查 capex 是否被短期压低。
- 对高速扩张公司，FCF margin 可能暂时失真。

### PEG

用于粗略比较成长与估值，但不能单独使用。

注意：

- 增长率必须有来源。
- EPS growth 可能来自回购、税率、成本削减，而非收入增长。
- 高周期性行业的 PEG 容易误导。

## 绝对估值

### DCF

适用于可对现金流做合理区间预测的公司。

必须列明：

- Revenue growth。
- Operating margin。
- Tax rate。
- Reinvestment / capex。
- Working capital。
- Terminal growth。
- Discount rate。
- Share count。
- Net cash / net debt。

敏感性至少覆盖：

- Revenue CAGR。
- Terminal margin。
- Discount rate。
- Terminal growth。

DCF 输出应为区间，不应给单点确定目标价。

本地简化 DCF 工具使用逐年 FCF 增长路径。它不单独建模 revenue、margin、tax、working capital、capex 或 SBC，因此只有在这些经营假设已在研究报告中解释时，输出才具有分析意义。

#### FCFF / UFCF 与 FCFE 口径

- `FCFF` / `UFCF` 是企业自由现金流 / unlevered free cash flow。使用与企业风险匹配的 WACC-style discount rate，折现结果先形成 enterprise value，再扣减 net debt 得到 equity value。
- `FCFE` 是股权自由现金流 / levered free cash flow。使用 cost-of-equity-style discount rate，折现结果直接形成 equity value，不得再次扣减 net debt。
- `OCF - capex` 通常已经受利息现金流影响，可近似视作 FCFE，但不必然是严格 FCFE。必须检查利息分类、税、租赁、净借款、优先股和少数股权，并标记为 `research approximation`。
- 任何 DCF 输出必须显示 FCF type、amount unit、per-share unit、valuation bridge 和 net debt treatment。
- 如果 FCF type 无法确认，不应输出高置信度 DCF 结论。

### SOTP

适用于多业务、多资产、控股平台或分部估值差异大的公司。

必须列明：

- 各业务分部。
- 分部收入、利润或资产指标。
- 适用倍数或估值方法。
- 控股折价、少数股权、净债务和税务影响。

## 情景估值

至少设置：

- Bear case。
- Base case。
- Bull case。

每个情景必须包含：

- 关键经营假设。
- 估值倍数或 DCF 假设。
- 对应估值区间。
- 触发条件。
- 失效条件。

示例结构：

```markdown
### Bear Case
- 假设：Revenue CAGR 降至 X%，margin 无法扩张。
- 估值：使用较低历史分位 EV/Sales 或 normalized P/E。
- 结果：估值区间为 ...
- 触发条件：订单放缓、客户流失、库存增加。
```

## 市场隐含预期

高估值成长股必须反推市场隐含预期。可回答：

- 当前 EV/Sales 或 P/E 隐含多长时间的高增长？
- 当前估值要求收入、margin、FCF margin 达到什么水平？
- 需要多大 TAM、份额和定价权才能支撑当前价格？
- 如果增长下降一个档位，估值区间如何变化？

P/E bridge 的 earnings basis 优先级：

1. 使用有来源、可复核的 `normalized_net_income_ttm`。
2. 没有 normalized bridge 时，使用 reported GAAP net income，但必须披露特殊项目和谨慎解释。
3. normalized EPS 可以补充 per-share context，但不得与不一致的 share count 混算。
4. 不得因为估值模型需要而自行发明 adjusted / normalized earnings。

Peer statistics 必须同时说明：

- Blended peer median 是宽泛参考，不是最终 valuation anchor。
- Core comparable median 取决于用户提供的 peer group、comparability status 和 inclusion flag。
- Core comparable 少于两家时，只能作为 indicative reference。

### 简明反推框架

不要求自动计算，但必须做定性或半定量反推：

1. `EV/Sales` 反推收入要求：
   - 当前 EV 是多少？
   - 若成熟期合理 EV/Sales 为 X-Y 倍，收入需要达到多少？
   - 从当前 revenue 到隐含 revenue，需要未来几年多少 revenue CAGR？
2. `P/E` 或 `Forward P/E` 反推 EPS 要求：
   - 当前价格或市值隐含多少 EPS / net income？
   - EPS growth 来自 revenue growth、gross margin、operating margin、税率、回购，还是 Non-GAAP 调整？
   - Forward EPS 是否来自可验证 consensus，还是未验证市场预期？
3. `P/FCF` 反推 FCF 要求：
   - 当前市值对应多少 normalized FCF 才能回到合理 P/FCF？
   - 需要多高 FCF margin 和 FCF conversion？
   - 当前 FCF 是否受 working capital timing、capex 周期或 SBC 影响？
4. 成熟期路径：
   - 需要多长时间达到合理成熟期估值倍数？
   - 期间是否要求 gross margin、operating margin、FCF margin 同时改善？
   - 如果 growth 或 margin 低于预期，估值下修风险是多少？

输出示例：

```text
当前 EV/Sales 为 X 倍。若成熟期 EV/Sales 回落到 Y-Z 倍，在 EV 不变的静态假设下，收入需要达到约 A-B，是当前收入的 C-D 倍。该反推不是预测，而是说明当前估值对 revenue CAGR、margin expansion 和 terminal multiple 的要求。
```

如果数据不足：

```text
当前缺少股价、市值、净现金/净债务或 consensus 数据，无法可靠反推市场隐含预期。
```

## 安全边际

安全边际来自：

- 当前价格显著低于保守估值区间。
- 资产负债表强。
- 现金流稳定。
- 下行情景可承受。
- 关键 thesis 有可验证证据。
- 估值没有依赖过多远期叙事。

不应把“股价跌了很多”自动视为安全边际。

## 行业估值框架差异

### 银行

常用：

- P/B。
- P/TBV。
- ROE / ROTCE。
- NIM。
- 资本充足率。
- 信用成本。

### 保险

常用：

- P/B。
- Embedded value。
- Combined ratio。
- Investment yield。
- Reserve adequacy。

### REITs

常用：

- FFO / AFFO。
- NAV。
- Cap rate。
- Occupancy。
- Lease maturity。
- Debt maturity and interest cost。

### 资源股

常用：

- Mid-cycle EBITDA。
- NAV。
- Reserve life。
- Unit cost。
- Commodity price sensitivity。

### SaaS

常用：

- EV/Sales。
- ARR growth。
- NRR / GRR。
- Gross margin。
- CAC payback。
- Rule of 40。
- FCF margin。

### 半导体

常用：

- Cycle-normalized earnings。
- EV/Sales。
- P/E on normalized EPS。
- Gross margin through cycle。
- Inventory days。
- Design win conversion。
- Capex exposure。

### 消费股

常用：

- P/E。
- EV/EBITDA。
- Same-store sales。
- Pricing power。
- Gross margin。
- Inventory and markdown risk。

## 估值失效条件

估值结论应列出何时失效：

- 增长显著低于 base case。
- 毛利率或 FCF margin 无法达到隐含水平。
- 同业估值中枢下移。
- 利率或 discount rate 变化。
- 技术替代或监管导致 terminal value 假设失效。
- 周期股盈利被证明是 peak earnings。
- 公司改变会计口径导致可比性下降。

## 禁止做法

- 给单点确定目标价。
- 用未经验证的远期叙事支撑高估值。
- 用周期顶部利润计算“便宜”。
- 对高增长公司只看 P/E。
- 把 consensus 当作事实。
- 混用 GAAP、Non-GAAP、TTM、NTM 而不说明口径。
- 用 FCFE 推导 enterprise value后再次扣减 net debt，或用 FCFF 直接当作 equity value。
