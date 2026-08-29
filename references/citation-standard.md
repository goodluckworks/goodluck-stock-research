# Citation Standard

股票研究必须让读者知道每个关键结论来自哪里、覆盖什么期间、使用什么口径，以及哪些内容只是推断或假设。

在 future adapter workflow 中，引用必须能从报告回到 normalized input、field provenance、source manifest 和 raw snapshot。Adapter-generated citation 只证明 lineage，不自动证明研究结论正确。

## 基本标注规则

每个关键财务数字和关键事实至少包含：

- 来源。
- 日期或期间。
- 币种。
- 会计口径。
- 披露性质：公司披露、市场预期、第三方估算、个人推断。
- 验证状态：已验证、部分验证、未验证。
- `source_id` 和 field provenance record（使用 adapter evidence package 时）。

## 财务数据引用格式

推荐格式：

```text
[指标]：[数值]，[期间]，[币种]，[口径]，[披露性质]，来源：[文件/页面/数据终端]。
```

示例：

```text
Revenue：USD 10.2bn，FY2025，GAAP，公司披露，来源：FY2025 Form 10-K，Consolidated Statements。
```

```text
Gross margin：42.5%，Q2 FY2026，Non-GAAP，公司披露，来源：Q2 FY2026 earnings release，Non-GAAP reconciliation。
```

```text
Forward P/E：约 28x，NTM，USD，市场预期，来源：数据终端 consensus estimate；该数字需与最新股价时间戳一起使用。
```

## 市场数据引用格式

当前股价、市值、EV、估值倍数、股息率和汇率都属于时间敏感数据。引用时必须注明：

- 数据来源。
- 获取时间。
- 市场时区。
- Market session：regular close、pre-market、after-hours、intraday、delayed close 等。
- 币种。
- 是否为实时、延迟或估算数据。
- Forward / trailing / TTM / NTM / FY1 / FY2 等口径。

适用指标包括：

- 当前股价。
- 市值。
- Enterprise value / EV。
- P/E。
- Forward P/E。
- EV/Sales。
- EV/EBITDA。
- P/FCF。
- 股息率。
- 汇率。

推荐格式：

```text
[市场指标]：[数值]，[币种]，[口径]，来源：[数据源]，获取时间：[YYYY-MM-DD HH:MM]，[市场时区]，market session：[regular close / pre-market / after-hours / intraday]，数据性质：[实时 / 延迟 / 估算]。
```

示例：

```text
当前股价：USD 125.40，来源：NASDAQ official quote，获取时间：2026-06-23 16:05，America/New_York，market session：regular close，数据性质：延迟数据。
```

```text
市值：USD 245bn，来源：数据终端，获取时间：2026-06-23 16:10，America/New_York，market session：regular close，数据性质：估算；计算口径基于最新股价和 diluted shares outstanding。
```

```text
EV/Sales：8.5x，NTM，USD，来源：数据终端，获取时间：2026-06-23 16:15，America/New_York，market session：regular close，数据性质：估算；EV 使用市值 + 总债务 - 现金及短期投资。
```

```text
Forward P/E：32x，FY1，USD，来源：数据终端 consensus，获取时间：2026-06-23 16:15，America/New_York，market session：regular close，数据性质：估算；EPS 为市场预期，未查看底层分析师模型。
```

```text
汇率：USD/CNY 7.25，来源：央行或数据终端，获取时间：2026-06-23 16:00，Asia/Shanghai，market session：intraday，数据性质：延迟数据。
```

如果缺少时间戳或 market session，应写：

```text
该市场数据缺少获取时间或 market session，暂不用于精确估值判断。
```

## 二级市场数据 fallback 规则

当市场数据来自 StockAnalysis、Yahoo Finance、CompaniesMarketCap、Macrotrends、Macroaxis、Koyfin 免费页面、财经门户或其他二级公开页面时，必须标注为 `indicative` 或 `待交叉验证`。

必须记录：

- Source：页面名称和 URL。
- Timestamp：页面显示时间、抓取时间或 `timestamp 未验证`。
- Market session：regular close、pre-market、after-hours、intraday、delayed close 或 `session 未验证`。
- Currency。
- Basis：trailing / forward / TTM / NTM / FY1 / FY2 / snapshot。
- Data nature：实时、延迟、估算、页面快照或 `性质未验证`。
- Cross-check status：已交叉验证 / 待交叉验证 / 无法交叉验证。

禁止：

- 不允许把二级页面数据当作公司官方披露。
- 不允许用没有 timestamp 的二级市场数据支撑精确估值结论。
- 不允许混用不同页面的市值、EV、shares、debt、cash 而不说明口径差异。

示例：

```text
EV/Sales：31.1x，TTM，USD，来源：StockAnalysis MRVL statistics，获取时间：2026-06-23 09:30，America/New_York，market session：regular close snapshot，数据性质：二级页面快照 / indicative，cross-check status：待交叉验证。该数据不属于公司官方披露。
```

```text
Market cap：USD 269.3bn，来源：Yahoo Finance quote page，timestamp 未验证，market session：regular close，currency：USD，数据性质：页面快照 / 待交叉验证。由于缺少明确更新时间，本报告仅用于估值方向判断，不用于精确区间。
```

估值结论若依赖未交叉验证的市场数据，必须说明：

```text
本估值结论依赖二级市场数据，尚未与交易所、公司 share count、债务和现金数据交叉验证；结论置信度应下调。
```

## 公司公告引用格式

推荐格式：

```text
公司在 [公告名称]（[发布日期]）中披露/表示：[简要事实]。
```

示例：

```text
公司在 FY2025 Form 10-K（2026-02-20）中披露，最大客户贡献收入比例超过 10%；具体客户名称未在摘要中披露。
```

## 新闻/媒体引用格式

媒体信息只能用于事实背景或线索，除非它引用并链接到原始文件。

推荐格式：

```text
[媒体名称] 于 [发布日期] 报道 [事实/事件]；该信息尚需公司公告或监管文件交叉验证。
```

示例：

```text
某权威财经媒体于 2026-03-05 报道公司可能扩大 AI data center 订单；由于公司未单独披露订单金额，该信息仅作为需求线索，不用于收入预测。
```

## 管理层发言引用格式

管理层发言必须标注场景和日期，并区分事实披露、指引和观点性表述。

推荐格式：

```text
管理层在 [会议/电话会]（[日期]）表示：[原意摘要]。性质：[事实披露/指引/管理层观点]。
```

示例：

```text
管理层在 Q3 FY2026 earnings call（2026-11-02）表示，AI-related demand remained strong。性质：管理层观点；仍需订单、收入或 backlog 数据验证。
```

## 数据不可得时的表述方式

不要用模糊语言掩盖缺口。使用以下表达：

- `公司未单独披露该指标。`
- `当前资料不足以判断。`
- `缺少可复核来源，暂不用于核心结论。`
- `该数字来自第三方估算，未与公司披露交叉验证。`
- `需要下一步查阅原始 filing / transcript / 数据终端。`

## 未验证信息标注

格式：

```text
未验证信息：[内容]。当前仅作为线索，不作为投资结论依据。待验证来源：[需要查找的文件或数据]。
```

示例：

```text
未验证信息：市场讨论称公司可能获得新 hyperscaler 客户订单。当前仅作为线索，不作为收入预测依据。待验证来源：公司公告、earnings call transcript、客户披露或可信数据终端。
```

## 区分披露性质

### 公司披露

公司在 filings、公告、IR 材料或 transcript 中直接披露的信息。

示例：

```text
公司披露：FY2025 revenue 为 USD X.Xbn，GAAP，来源：FY2025 Form 10-K。
```

### 市场预期

来自 consensus estimate、sell-side aggregation 或数据终端的预期。必须注明数据源和时间戳。

示例：

```text
市场预期：FY2026 revenue growth 约 X%，来源：某数据终端 consensus，数据时间：2026-06-23。未查看底层分析师模型。
```

### 第三方估算

来自行业机构、媒体、专家访谈、供应链数据或非公司披露模型。

示例：

```text
第三方估算：某行业机构估算 AI accelerator 市场规模为 USD Xbn，期间：2026E，来源：[机构报告名]。该数据不是公司披露。
```

### 个人推断

研究者基于已知事实做出的逻辑推导。必须明确假设。

示例：

```text
个人推断：如果公司 AI segment revenue 占比继续提升，gross margin 可能受益于产品 mix 改善。关键假设：AI 产品毛利率高于公司平均水平；该假设需公司分部披露验证。
```

## 事实 / 推断 / 假设 / 观点格式

推荐在结论中使用：

```markdown
### 事实
- 公司披露 ...

### 推断
- 基于 ... 可以推断 ...

### 假设
- Base case 假设 ...

### 观点
- 当前更适合归入观察池，而不是候选。
```

## Adapter Evidence Citation

当数据来自 future adapter evidence package，推荐附：

```text
Source ID: avgo-2025-10k
Field provenance: avgo-fy2025-revenue
Raw snapshot: raw-avgo-2025-10k
Transformation: identity
Source status: verified
```

Derived fields 必须列 transformation，例如 `FY2025 + H1 FY2026 - H1 FY2025`。Market snapshot 仍必须记录 timestamp、timezone、market session 和 indicative/cross-check status。

禁止：

- 只引用 adapter 名称，不引用 source。
- 把 adapter extraction 当作 company disclosure。
- 隐藏 unit scale、currency conversion、split adjustment 或 TTM bridge。
- 由 adapter citation 自动推出投资结论。
