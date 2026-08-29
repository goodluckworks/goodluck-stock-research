# Source Provenance Policy

## 1. Purpose

本政策规定 future adapter evidence package 的来源分类、可靠性、manifest 字段和字段级溯源要求。目标是让每个关键值都能从 normalized input 回到原始 snapshot。

v0.3.1 `local_official_filing_adapter` 实现本地 source manifest 的 evidence-only
子集。v0.3.2 `sec_official_filing_adapter` 对用户明确指定的 SEC URL 记录 status、
retrieved_at、checksum 和 raw text provenance，但仍不生成财务字段 provenance。

## 2. Source Type Taxonomy

| Source type | Definition | Default treatment |
|---|---|---|
| `official_filing` | 监管 filing 正文及 amendment | Primary |
| `company_ir` | 公司 IR 页面、fact sheet 或公告 | Primary, subject to basis review |
| `earnings_release` | 公司正式 earnings release 和 reconciliation | Primary |
| `earnings_call_transcript` | Prepared remarks、Q&A 或授权 transcript | Primary for statements, not audited facts |
| `investor_presentation` | 公司 presentation | Primary for company claims; reconcile to filings |
| `market_data_vendor` | 交易所或专业数据供应商 | Source-dependent |
| `secondary_market_page` | 公开财经页面或聚合页面 | Indicative / pending cross-check |
| `user_provided` | 用户上传或手工输入 | Unverified until source evidence is attached |
| `analyst_assumption` | 研究者假设或情景输入 | Assumption, never fact |

## 3. Source Reliability Ranking

1. Effective official filing正文。
2. Company earnings release / IR disclosure with matching period。
3. Exchange、government 或 regulator data。
4. Authorized transcript / prepared remarks。
5. Investor presentation。
6. Market data vendor with timestamp and methodology。
7. Secondary market page。
8. User-provided data without attached primary evidence。
9. Analyst assumption。

Ranking is a starting point. A newer restatement outranks an older filing; an official filing does not make management guidance a realized fact.

## 4. Required Source Fields

| Field | Required | Meaning |
|---|---:|---|
| `source_id` | Yes | Evidence package 内稳定唯一 ID |
| `source_name` | Yes | 可读名称 |
| `source_url` | Conditional | 原始 URL；本地文件可写 `local://` logical reference |
| `source_type` | Yes | Taxonomy 枚举 |
| `retrieved_at` | Yes | 带时区 ISO 8601 获取时间 |
| `source_date` | Yes | 来源发布日期或 `date_unverified` |
| `filing_date` | Conditional | Filing 提交日期；非 filing 写 `not_applicable` |
| `reporting_period` | Yes | 覆盖期间 |
| `fiscal_period` | Yes | 标准化期间，例如 `FY2025`, `Q2 FY2026`, `TTM`; 不适用时明确标注 |
| `fiscal_year` | Yes | 财年或 `not_applicable` |
| `fiscal_quarter` | Yes | 财季或 `not_applicable` |
| `currency` | Yes | ISO currency 或 `not_applicable` |
| `amount_unit` | Yes | 例如 `USD millions` 或 `not_applicable` |
| `per_share_unit` | Yes | 例如 `USD/share` 或 `not_applicable` |
| `market_session` | Yes | regular close / intraday / not_applicable / unverified |
| `source_status` | Yes | verified / partially_verified / indicative / unverified / fictional_sample |
| `data_status` | Yes | available / partial / stale / conflicting / superseded / missing / not_applicable |
| `confidence` | Yes | high / medium / low |
| `notes` | Yes | Basis、限制、许可或冲突说明；无则写 `none` |
| `transformation_notes` | Yes | Source-level extraction/normalization note；无变换写 `identity / none` |

不允许空字段。未知值使用明确枚举或 `unverified`。

`source_status` 描述来源可靠性；`data_status` 描述该 source 中目标数据的可用性、freshness 和冲突状态。两者不得合并为一个模糊字段。

## 5. Field-Level Provenance

每个关键字段使用：

| Field | Meaning |
|---|---|
| `normalized_field` | v0.2.x 输入字段名 |
| `value` | 保留原始精度的值 |
| `source_id` | 对应 source manifest |
| `source_field_name` | 原表格字段、XBRL tag 或文本标签 |
| `source_locator` | Page、table、section、line、JSON path 或 cell |
| `transformation` | `identity`, `unit_scale`, `sum`, `difference`, `ttm_bridge`, `manual_mapping`, `assumption` |
| `confidence` | high / medium / low |
| `notes` | 口径、冲突、估算或缺失说明 |

一个字段可引用多个 source records，例如 TTM bridge。所有组成部分都必须列出。

## 6. Derived Fields

Derived field 必须记录：

- 公式或 transformation。
- 输入字段和对应 provenance IDs。
- 单位与 currency。
- rounding policy。
- 是否可逆或可复算。
- 是否来自 analyst assumption。

示例：

```text
free_cash_flow = operating_cash_flow - abs(capital_expenditure)
transformation = difference
source inputs = fp_ocf_fy2025, fp_capex_fy2025
```

机械反推不得改名为 consensus 或 company guidance。

## 7. Conflicting Sources

遇到冲突：

1. 保留每个 source 和 field record。
2. 检查 period、currency、unit、GAAP/Non-GAAP、split basis 和发布日期。
3. 根据 hierarchy 选择 active candidate，并记录选择理由。
4. 无法解决时，字段 `source_status` 不得为 verified。
5. 将冲突写入 `warnings` 和 `unresolved_fields`。

## 8. Restatements and Corrections

- Amendment、restatement 或 corrected release 创建新 `source_id`。
- 旧 snapshot 不删除、不覆盖。
- Manifest 记录 `supersedes_source_id`、effective date 和 changed fields。
- Active normalized input 应基于截至 `as_of_date` 的最新有效版本。
- v0.3.2 不自动发现 amendment 或判断 latest-effective；manifest 必须写
  `latest_effective_status=user_specified_not_independently_discovered`。
- 如果 restatement 影响历史期间，所有 dependent derived outputs 标记 invalidated，等待重算。

## 9. Manual Assumptions

Analyst assumption 必须：

- `source_type=analyst_assumption`
- 有 owner、created_at、purpose 和 scenario。
- 与 company disclosure 和 consensus 分开。
- 不得标记 verified。
- 在 DCF、mature multiple、peer classification 等输出中显式展示。

## 10. Citation Standard Integration

- Source manifest 提供 citation appendices 的基础字段。
- Field provenance 提供数字级引用。
- Market data 必须附 timestamp、timezone、session 和 data nature。
- Secondary pages 必须标记 indicative / pending cross-check。
- Management commentary 必须区分事实披露、guidance 和观点。
- Adapter citation 不能替代研究报告对事实、推断、假设和观点的分类。

## 11. Examples

### Official filing field

```yaml
normalized_field: revenue
value: 63887
source_id: avgo-2025-10k
source_field_name: Revenue
source_locator: Consolidated Statements of Operations, FY2025
transformation: identity
confidence: high
notes: GAAP, USD millions
```

### Market snapshot

```yaml
normalized_field: current_price
value: 382.07
source_id: avgo-market-20260624-close
source_field_name: Close
source_locator: quote snapshot
transformation: identity
confidence: medium
notes: secondary_market_page; regular close; indicative / pending cross-check
```

### TTM bridge

```yaml
normalized_field: free_cash_flow_ttm
value: 32762
source_id:
  - avgo-fy2025-release
  - avgo-q2fy2026-release
transformation: FY2025 + H1FY2026 - H1FY2025
confidence: medium
notes: OCF less capex; FCFE research approximation
```
