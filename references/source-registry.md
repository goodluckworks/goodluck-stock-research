# Source Registry

本文件定义股票研究的数据源优先级和财务数字引用要求。默认原则是：一级来源优先，二级来源交叉验证，三级来源只能作为线索。

v0.3 design 中，future adapter 必须把来源注册为 source manifest，并为每个 normalized field 保留 field-level provenance。来源等级不能因 adapter 自动访问而提升。

## 一级来源

一级来源应作为关键事实和关键财务数字的首选依据。

- 公司年报、季报、10-K、10-Q、20-F、8-K。
- 公司 Investor Relations 页面、presentation、fact sheet、press release。
- Earnings call transcript。
- 交易所公告。
- 监管文件。
- 通过 SEC EDGAR 获取的 10-K、10-Q、8-K、20-F、6-K 等 filing 正文。

适用用途：

- 收入、利润、现金流、资产负债表、分部数据。
- 管理层指引和口径解释。
- 风险因素、法律诉讼、重大合同、资本配置。
- 会计政策、Non-GAAP reconciliation、一次性项目解释。

## SEC EDGAR 说明

SEC EDGAR 是获取美国上市公司监管文件的官方渠道。通过 EDGAR 获取的 10-K、10-Q、8-K、20-F、6-K 等 filing 本身按一级来源处理。

EDGAR 搜索页、索引页或 metadata 只是访问入口，不应替代 filing 正文。引用 EDGAR filing 时，应引用具体 filing、报告期、提交日期和相关表格或段落。

公司 Investor Relations 与 EDGAR filing 若有差异，应优先核对 filing 原文、发布时间、是否存在修订 filing，以及 IR 材料是否为摘要、Non-GAAP 或 presentation 口径。

## 二级来源

二级来源用于交叉验证、补充历史数据、查找市场预期或媒体事实背景。

- SEC EDGAR 搜索页、索引页或 metadata。
- 公司官网。
- 交易所官网。
- 年报数据库。
- 财经数据终端。
- 权威财经媒体。
- 审计师、评级机构、行业协会或政府统计机构公开资料。
- StockAnalysis、Yahoo Finance、CompaniesMarketCap、Macrotrends 等公开市场数据页面。

适用用途：

- 校验 filings 与媒体报道是否一致。
- 查找历史估值、同业估值、市场预期。
- 补充行业规模、份额、监管背景。
- 发现需要回到一级来源验证的线索。

### 二级市场数据页面使用规则

公开市场数据页面可用于快速获取股价、市值、EV、P/E、Forward P/E、EV/Sales、EV/EBITDA、P/FCF、股息率和汇率等时间敏感数据，但默认只能视为 `indicative` 或 `待交叉验证`。

使用时必须记录：

- Source。
- Timestamp；如果页面未显示更新时间，写 `timestamp 未验证`。
- Market session。
- Currency。
- Trailing / forward / TTM / NTM / FY1 / FY2 口径。
- 数据性质：实时、延迟、估算或页面快照。
- 是否已与交易所、公司 filing、数据终端或其他来源交叉验证。

不允许把二级市场数据页面当作公司官方披露。估值结论若依赖未交叉验证的二级市场数据，必须降低置信度并写入 `Next Checks`。

## 三级来源

三级来源只能作为线索，不得作为关键结论依据。

- 博客。
- 社交媒体。
- 论坛。
- 二级解读文章。
- 未经验证的 newsletter、播客摘要、短视频内容。

适用用途：

- 发现市场关注点。
- 收集潜在 bear case 或争议点。
- 形成待验证问题清单。

不适用用途：

- 直接证明收入、利润、订单、客户、毛利率或现金流。
- 直接支持投资结论。
- 代替公司披露或监管文件。

## 财务数字引用要求

所有关键财务数字必须注明：

- 来源：文件名、公告名、transcript 名称或数据终端名称。
- 期间：例如 FY2025、Q1 FY2026、TTM、LTM、calendar 2025。
- 币种：例如 USD、CNY、HKD、EUR。
- 口径：GAAP、Non-GAAP、IFRS、Adjusted、segment reporting。
- 性质：公司披露、市场预期、第三方估算、个人推断。
- 是否可复核：能否通过原始文件定位到表格、页码或段落。

推荐格式：

```text
Revenue: USD X.Xbn, FY2025, GAAP, company-disclosed, source: FY2025 Form 10-K, consolidated statements.
```

如果缺少任何要素，应写明：

```text
该数字缺少可复核来源 / 期间 / 币种 / 口径，暂不用于核心结论。
```

## 冲突处理

当来源之间存在冲突：

1. 优先使用公司 filings 和监管文件。
2. 检查期间、币种、会计口径是否不同。
3. 检查是否为 restatement、pro forma、constant currency 或 Non-GAAP。
4. 如果无法解释冲突，将其列入 `next checks`，不要强行合并。

Future adapter 还必须：

- 保留冲突来源的 raw snapshots。
- 创建结构化 conflict record。
- 记录 active source 的选择理由。
- 在 restatement 或 correction 后保留旧 lineage，并 invalidates dependent normalized/derived outputs。

完整规范见 `source-provenance-policy.md` 和 `freshness-cache-policy.md`。

## 不可接受的来源行为

- 用二级或三级来源替代公司披露的核心财务数据。
- 把社交媒体传言写成事实。
- 使用没有日期的数字作为当前数据。
- 使用未经说明的 consensus estimate。
- 混用 GAAP 与 Non-GAAP 而不说明差异。
- 把盘前、盘后或短期股价波动当作基本面证据。
- Adapter 在没有 raw snapshot、source manifest 或 field provenance 时直接生成 normalized 数字。
- Adapter 直接输出投资结论、研究状态或交易动作。
