# Adapter Failure Modes

本文规定 adapter 遇到异常时的最小行为。

v0.3.1 已实现 local-file subset。v0.3.2 新增 SEC-only network subset：invalid
domain、missing User-Agent、timeout、HTTP failure、response-size limit 和 bounded retry
都会明确失败或生成 structured error；不会切换到其他来源。

## 1. Ticker Ambiguity

场景：同一 ticker 在不同市场复用、ADR 与普通股混淆、share class 不明确。

行为：

- Blocking error。
- 返回候选 company/exchange/share class。
- 不生成 company-specific normalized input。
- 不猜测 exchange 或默认使用美股。

## 2. Company Name / CIK Mismatch

场景：ticker 指向的法律实体与 CIK、公司名或 filing entity 不一致。

行为：

- Blocking error `company_cik_mismatch`。
- 保存 identity evidence。
- 要求人工选择正确实体。
- 不拼接不同实体的 financials。

## 3. Missing Filing

场景：目标期间没有 filing、foreign issuer filing type 不同或 filing 尚未发布。

行为：

- 记录 requested period、searched source 和 as-of date。
- 可返回上一期 evidence，但必须标记 stale/history-only。
- 关键字段进入 unresolved list。
- 不使用未来日期 filing 回填历史 as-of request。

## 4. Filing Restatement

场景：10-K/A、10-Q/A、corrected release 或 restated comparatives。

行为：

- 保存新旧 snapshot。
- 链接 `supersedes_source_id`。
- 新版本成为 active candidate。
- 失效 dependent normalized inputs 和 reports。
- 列出受影响字段，禁止静默覆盖。

## 5. Unit Mismatch

场景：USD、USD thousands、USD millions 或 shares 与 million shares 混用。

行为：

- Blocking for affected fields。
- 只有显式 `unit_scale` transformation 才可转换。
- 记录原值、转换因子和目标单位。
- 无法确认时写 `待核实`，不能按经验猜单位。

## 6. Currency Mismatch

场景：财报币种与市场币种不同，或 peer comps 跨币种。

行为：

- 不自动转换。
- 若未来允许转换，必须有 FX source、timestamp、session 和 formula。
- 未转换的绝对金额不得直接比较或相加。
- Multiples 仍需确认 numerator/denominator 同币种。

## 7. Share Split / Share Count Mismatch

场景：历史 EPS 已重述但 shares 未重述、market cap 使用当前股数、ADR ratio 改变。

行为：

- Blocking for per-share calculations。
- 记录 split date、ratio、company restatement status。
- 优先使用 company-restated historical values。
- 不自行混合 pre-split 与 post-split data。

## 8. Market Snapshot Staleness

场景：当前估值使用旧收盘价、无 timestamp 或 session。

行为：

- 标记 `stale_blocking` 或 `indicative`。
- 不用于精确 current valuation。
- 保留历史 snapshot 供重现。
- 要求手工 refresh 或批准的 future source refresh。

## 9. Source Conflict

场景：filing、release、vendor 或 secondary page 数值不一致。

行为：

- 保留所有 source records。
- 检查 period、basis、unit、currency、restatement 和 delay。
- 根据 hierarchy 选择 active candidate并记录理由。
- 无法解决时不标 verified，并阻止精确结论。

## 10. Segment Reporting Change

场景：公司重组 segment、recast historical periods 或停止披露旧 KPI。

行为：

- 记录旧/新 segment taxonomy。
- 优先使用 company-recast comparatives。
- 不把不兼容 period 机械计算增长。
- 报告层必须说明 comparability break。

## 11. Acquisition / Divestiture Break

场景：大额收购、剥离或 discontinued operations 破坏期间可比性。

行为：

- 记录 transaction date、included periods、pro forma status。
- 分开 reported growth 与 organic/pro forma claims。
- 不自动构造 organic growth。
- 要求 goodwill、intangibles、amortization、debt 和 integration notes（适用时）。

## 12. Missing Normalized Reconciliation

场景：公司强调 adjusted result，但没有完整 GAAP reconciliation，或用户只提供 adjusted number。

行为：

- 不生成 normalized earnings。
- 使用 reported GAAP fallback（若可用）并显示 caution。
- 将 reconciliation 列入 unresolved fields。
- 不把 vendor adjusted EPS 当公司披露。

## 13. Vendor Estimate Conflict

场景：不同 vendor 的 consensus、forward revenue、EPS 或 EV 不一致。

行为：

- 分别记录 vendor、timestamp、period 和 methodology。
- 不求平均掩盖冲突。
- 选择依据必须可解释；否则标 indicative。
- Mechanical derived growth 不得称为 consensus。

## 14. Network or Source Unavailable

v0.3.2 SEC adapter behavior：

- 结构化 error，不伪造成功。
- 不自动回退到 cache 或其他 URL。
- 不在失败后偷偷切换低优先级来源。
- Retry policy 必须有限、可观察且不影响本地工具边界。

## 15. Authentication Failure

当前实现不支持认证：

- 不记录 secret、header、cookie 或 token。
- 返回 `authentication_required` 或 `authentication_failed`。
- 不回退到 broker/account credentials。
- Optional-key adapter 必须经单独审批且只读。

## 16. Rate Limit

v0.3.2 SEC adapter behavior：

- 对 timeout、network error 和指定 transient HTTP status 返回 retryable structured error。
- 不无限重试。
- 不绕过限制或切换未批准来源。
- 不自动使用 cache；调用者可在独立人工流程中选择已有 evidence。

## 17. Unsupported Company Type

场景：银行、保险、基金、SPAC、pre-revenue biotech 或复杂 partnership 不适配现有 financial/valuation schema。

行为：

- 返回 `unsupported_company_type` 或 partial support。
- 明确哪些字段和工具不适用。
- 不强套工业公司比率。
- 要求专用 schema/design review 后再支持。

## 18. Required Behavior Summary

| Failure class | May use cached evidence | May normalize | May calculate | May issue research conclusion |
|---|---:|---:|---:|---:|
| Identity ambiguity | No | No | No | No |
| Stale historical evidence | Yes, labeled | Historical only | Historical only | Report layer with warning |
| Source conflict | Yes, all versions | Only resolved fields | Partial | Report layer only |
| Missing fields | Yes | Partial | Partial if schema permits | Report layer only |
| Unit/currency/split mismatch | No for affected fields | No | No | No |
| Authentication/network/rate limit | Cache if policy permits | Based on cache status | Based on normalized cache | No adapter conclusion |
| Unsupported company type | Partial | Supported fields only | Supported tools only | Report layer only |

Universal rules:

- Never fabricate data.
- Never silently overwrite evidence.
- Never drop provenance.
- Never output investment conclusion from adapter.
- Never connect to broker or execute trades.
