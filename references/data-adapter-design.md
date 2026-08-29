# Data Adapter Design

## 1. Purpose

本文定义 `goodluck-stock-research` v0.3 的数据适配器架构。`stock-research-v0.3-design`
是 design-only release；v0.3.1 实现 local-file evidence packaging；v0.3.2 实现
显式 SEC URL 的极窄、no-key、evidence-only live adapter。

v0.3.1 已实现一个严格受限的 design subset：`local_official_filing_adapter`。它只读取本地文件并生成 evidence package，不执行 live source access 或财务抽取。

核心原则：

- Adapter 负责获取或接收证据，不负责投资判断。
- Raw evidence 必须先落地，不能直接把网络响应送入计算脚本。
- Normalization 必须保留字段级来源、变换和单位。
- v0.2.x scripts 继续只读取本地 CSV / JSON。
- Research report 必须由 Agent 或研究者审查来源、假设、冲突和缺口后形成。

## 2. Non-Goals

本架构及当前实现不包含：

- Trading、broker connection、order execution 或 portfolio action。
- 自动买入、卖出、调仓、仓位或交易信号。
- 隐藏 credentials、API key、token、password 或 secret。
- 自动投资结论、最终研究状态、thesis、bear case 或 target price。
- 非 SEC live source、yfinance、OpenBB、market vendor 或通用网页抓取 adapter。
- SEC ticker/CIK/accession discovery、bulk crawl、XBRL extraction 或财务字段 population。
- 网络认证、browser automation 或第三方依赖。
- 替代人工判断 source reliability、peer comparability、normalized earnings 或估值假设。

## 3. Architecture Overview

```text
Source
  -> Raw Evidence Snapshot
  -> Source Manifest
  -> Field-Level Provenance
  -> Normalized Input CSV / JSON
  -> v0.2.x Calculation Tools
  -> Research Report
```

数据流必须是单向、可审计的。任何层都不得绕过 raw evidence、source manifest 或 field provenance 直接生成研究结论。

## 4. Layer Boundaries

### Source Adapter Layer

职责：

- 接收明确的 identity、period、request type 和 source preference。
- 在未来实现中，以只读方式访问获准来源或读取用户提供文件。
- 保存原始响应或原始文件，不做投资解释。
- 报告 unresolved fields、warnings 和 errors。

禁止：

- 计算估值结论。
- 生成 buy/sell、研究状态、thesis 或 portfolio action。
- 修改来源系统。
- 静默使用其他 ticker、期间、币种或估算值填补缺口。

### Evidence Layer

职责：

- 保存 immutable raw snapshot。
- 为 snapshot 生成 checksum、retrieved_at、content type、source identity 和文件路径。
- 创建 source manifest，记录可靠性、期间、状态和冲突。
- 保留 restatement、修订和替代版本，而不是覆盖旧文件。

### Normalization Layer

职责：

- 从 raw snapshot 提取字段。
- 统一字段名称、日期格式和显式单位。
- 生成 field-level provenance。
- 输出符合现有 schema 的本地 CSV / JSON。
- 将缺失、冲突、推断和人工假设明确标注。

禁止：

- 在没有 source 或 transformation note 时生成数字。
- 把 `data center revenue` 自动映射为 `AI-only revenue`。
- 把 management-defined Non-GAAP 自动当作 normalized earnings。

### Calculation Layer

职责：

- 继续使用 v0.2.x 的四个标准库脚本。
- 只读取本地 CSV / JSON。
- 输出可复现 Markdown 计算结果。

Adapter 不得调用计算结果形成投资结论；计算层也不负责验证来源真实性。

### Research Report Layer

职责：

- 核对 source manifest、field provenance、warnings 和 unresolved fields。
- 区分事实、推断、假设、观点。
- 执行 bear case、kill criteria、三否决和适用时的九项评分。
- 形成研究流程状态，而不是交易建议。

## 5. Source Hierarchy

优先级从高到低：

1. Official filings：监管 filing 正文及修订文件。
2. Company IR：公司 IR 页面和可下载材料。
3. Earnings releases：公司正式业绩公告及 reconciliation。
4. Earnings call transcripts / prepared remarks。
5. Investor presentations。
6. Exchange、government、industry regulator 或其他官方数据。
7. Market data vendors。
8. Secondary market pages。
9. User-provided data。
10. Analyst assumptions。

高优先级不代表自动正确。必须比较 filing date、reporting period、GAAP/Non-GAAP、restatement、currency 和单位。

## 6. Adapter Types

以下类型说明架构状态：

| Adapter type | Intended evidence | Default mode | Important boundary |
|---|---|---|---|
| `official_filing_adapter` | Filing 正文、metadata、amendment chain | no-key | Filing index 不能替代正文 |
| `company_ir_adapter` | IR release、presentation、fact sheet | no-key | 必须区分摘要、GAAP 和 Non-GAAP |
| `earnings_release_adapter` | Results、guidance、reconciliation | no-key | Guidance 不能当作 realized result |
| `transcript_adapter` | Prepared remarks、Q&A、management commentary | no-key or approved optional-key | 发言需标注 speaker、date 和 statement type |
| `market_snapshot_adapter` | Price、market cap、EV、multiples、FX | approved source dependent | 必须记录 timestamp、timezone、session 和 indicative status |
| `user_manual_input_adapter` | 用户上传或手工整理的文件 | local | 用户输入不能自动升级为 verified |

Implementation status:

- `local_official_filing_adapter`: implemented in v0.3.1 for local-file evidence packaging only.
- `sec_official_filing_adapter`: implemented in v0.3.2 for one explicit SEC URL,
  GET-only evidence packaging; fixture tests remain offline.
- All other live/no-key network adapters: not implemented.
- Optional-key adapters: not approved or implemented.

## 7. No-Key vs Optional-Key Mode

- `no-key` 是默认模式，也是任何 implementation 的第一优先级。
- Optional-key mode 只能用于只读数据访问。
- Optional-key mode 永远不得连接 broker、交易、订单或 portfolio action。
- Credentials 不在本 Skill、evidence package、manifest、日志或 Git 仓库中存储。
- 未来实现如需 credentials，必须由外部运行环境管理，并经过单独用户审批和安全设计。
- Optional-key adapter 必须独立审查、独立测试、独立文档化；不能因已有 no-key adapter 而自动获准。

## 8. Data Flow

1. Resolve identity：ticker、company、exchange、CIK/LEI（适用时）。
2. Freeze request：as-of date、fiscal period、data request type、source preference。
3. Collect or receive source in read-only mode。
4. Persist raw snapshot using a unique, immutable path。
5. Write raw snapshot manifest and checksum。
6. Write source manifest with reliability and freshness assessment。
7. Extract candidate fields with field-level provenance。
8. Validate units, currency, period and share basis。
9. Write normalized v0.2.x inputs to new versioned paths。
10. Run calculation scripts only after normalization validation passes。
11. Present warnings and unresolved fields to the report layer。

## 9. Provenance Requirements

每个 evidence package 至少包含：

- `source_url`
- `source_name`
- `source_type`
- `retrieved_at`
- `source_date`
- `filing_date`
- `reporting_period`
- `fiscal_period`
- `currency`
- `amount_unit`
- `per_share_unit`
- `market_session`
- `data_status`
- `field_provenance`
- `transformation_notes`

每个关键 normalized field 必须追溯到 `source_id`、原始字段或文本位置、变换过程和 confidence。

## 10. Freshness Requirements

- Filing：检查是否为截至 `as_of_date` 的最新有效 filing，是否有 amendment/restatement。
- Market snapshot：必须有带时区 timestamp、market session 和数据性质。
- Transcript：必须与对应 earnings period 和 event date 匹配。
- Stale evidence 不得静默使用；必须产生 warning，并可阻止 time-sensitive output。
- Freshness 是相对于 request 的属性，不是来源的永久属性。

## 11. Cache and Raw Snapshot Policy

- Raw snapshot immutable，采用唯一版本路径和 checksum。
- Normalized input 必须引用 raw snapshot 与 manifest。
- Derived output 必须引用 normalized input。
- 不允许 silent overwrite；同一路径存在时必须创建新版本或明确失败。
- Source correction、restatement 或 refresh 创建新 lineage，不删除旧 lineage。
- Cache 只提升可复现性，不能把 stale cache 伪装成 fresh source。

## 12. Failure Behavior

所有失败必须结构化进入 `warnings`、`errors` 或 `unresolved_fields`：

- Source unavailable：不生成伪数据；可使用符合 policy 的旧 snapshot，并明确 stale。
- Conflicting sources：保留双方，按优先级和口径分析，无法解决则阻止字段进入 verified 状态。
- Missing field：输出缺失原因与建议来源，不留空冒充零。
- Unit/currency mismatch：停止相关 normalization，除非转换规则和汇率来源明确。
- Restatement：新旧版本并存，最新有效版本成为 active candidate。
- Ticker ambiguity：停止 company-specific normalization。
- Split mismatch：停止 per-share 和 share-count bridge。
- Unsupported company type：输出不支持原因，不强套现有 schema。

详细规则见 `adapter-failure-modes.md`。

## 13. Security Boundary

- 只读 source access。
- 不写入来源系统。
- 不保存 credentials。
- 不记录 authorization header、cookie、session token 或用户账户信息。
- 禁止 broker、order、trade、portfolio action 和交易信号。
- Evidence path 必须位于用户指定本地工作区或缓存根目录。
- Raw evidence 可包含公开材料，但不得把受限内容提交到仓库；manifest 应记录访问和许可限制。

## 14. Testing Strategy

未来 implementation 必须使用 fixture-first：

- MRVL：AI networking、GAAP special items、FCFE approximation。
- NVDA：marketable securities、split-adjusted shares、AI/data-center distinctions。
- AVGO：acquisition accounting、segment mix、debt 和 Non-GAAP reconciliation。
- Stale、conflict、missing field、restatement、split mismatch fixtures。
- Contract tests 确认 adapter 不输出研究结论。
- Regression tests 确认 normalized files可被 v0.2.x scripts 读取。
- Security tests 确认无 broker/trading 路径和无 secret persistence。

## 15. Implementation Gates

进入 v0.3 implementation 前必须满足：

1. Design review 通过且无 High/Medium design issue。
2. 用户明确批准 implementation scope。
3. 首个 adapter 必须是 no-key、official-source、read-only。
4. Fixture、manifest 和 contract tests 先于 live implementation。
5. Optional-key adapter 需要单独审批。
6. 任何 broker 或交易接口永久排除在本项目外。
7. Live adapter 不能改变 v0.2.x 本地 CSV / JSON 工具边界。

v0.3.2 满足单个显式 SEC filing URL 的 evidence-packaging gate。任何 discovery、
XBRL extraction、financial population、其他 live source 或 optional-key implementation
仍需新的用户确认和独立安全审查。

## 16. Open Questions

- SEC filing extraction/normalization 的字段范围与人工复核 gate。
- Raw snapshot 的默认 retention period 和用户删除策略。
- 公共 transcript 的许可与可存储范围。
- Market vendor 的数据许可、延迟属性和再分发限制。
- Restatement lineage 的 active-version 选择是否需要人工确认。
- CIK、ticker、exchange 和 share-class identity 的权威映射来源。
- Optional-key credentials 由何种外部 runtime 管理；本 Skill 不承担存储。
