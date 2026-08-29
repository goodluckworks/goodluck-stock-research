# SEC Access Policy

## 1. Purpose

本政策约束 `sec_official_filing_adapter` 对 SEC 官方公开来源的窄范围、只读访问。v0.3.2 只下载用户明确指定的单个 filing document；不发现 ticker、CIK、accession，不抓取完整 submissions history，不解析 XBRL。

SEC 官方说明：`data.sec.gov` 的公开 JSON API 不要求认证或 API key；自动访问必须遵守 SEC Privacy and Security Policy 与 fair-access guidance。SEC 当前公开 guidance 要求高效下载、只取所需内容，并将总请求率限制在每秒不超过 10 次。v0.3.2 使用更保守默认值。

## 2. Allowed Sources

仅允许 HTTPS 且 host 精确为：

- `sec.gov`
- `www.sec.gov`
- `data.sec.gov`

允许路径范围：

- `https://www.sec.gov/`
- `https://www.sec.gov/Archives/`
- `https://www.sec.gov/ixviewer/`
- `https://data.sec.gov/submissions/`
- `https://data.sec.gov/api/xbrl/companyfacts/`

v0.3.2 默认实现 filing document 的单 URL 下载。`data.sec.gov` 仅保留官方 public JSON compatibility，不使用 API key，也不做 company-wide crawl 或 XBRL extraction。

任何 redirect 必须继续位于上述 SEC host；非 SEC redirect 在跟随前阻断。

## 3. Request Rules

- GET only。
- No authentication、cookies 或 login。
- User-Agent required。
- Timeout required。
- Minimum request interval required。
- Retry count bounded。
- Maximum requests per run bounded。
- Maximum response bytes bounded。
- No parallel or bulk download。
- One explicit source URL per adapter run。
- Respect SEC fair-access guidance。

## 4. User-Agent Policy

Live mode 必须通过 `--user-agent` 提供可识别的组织/个人名称与联系信息。缺少或过短时 adapter 失败。

User-Agent：

- 只进入 HTTP header。
- 不写入 manifests 或 logs。
- Run report 只记录 `provided: Yes/No`，不打印 email 或完整值。

## 5. Rate Limit Policy

v0.3.2 defaults：

- Minimum interval：`0.5` seconds。
- Maximum requests/attempts per run：`3`。
- Timeout：`15` seconds per attempt。
- Maximum response：`25 MB`。

允许配置更保守值。不得将 interval 设置低于 `0.2` 秒，不得将 attempts 设置高于 `3`。

## 6. Cache Policy

- 成功响应保存为 checksum-addressed immutable raw snapshot。
- 默认拒绝非空 output directory。
- `--overwrite` 更新 manifests/reports，但不同 checksum 的 raw snapshots 全部保留。
- Fixture mode 不联网，使用本地文件模拟 evidence flow。
- v0.3.2 不自动刷新、不判断 SEC 上是否存在更新 filing。

## 7. Failure Behavior

- Invalid/non-SEC URL：fetch 前 blocking failure。
- Missing User-Agent：fetch 前 blocking failure。
- HTTP error、timeout、rate-limit 或 oversized response：生成结构化 failure package。
- Failure package 保留 status、request count、retrieved_at、errors 和 unresolved fields；不伪造 raw snapshot。
- 不自动切换其他 URL 或较低优先级来源。

## 8. Prohibited Actions

- POST / PUT / DELETE。
- Ticker discovery、CIK resolution、accession discovery。
- Bulk submissions crawl。
- Full XBRL/financial extraction。
- API key、token、password、secret 或 `os.environ` credential read。
- yfinance、OpenBB、paid vendor、broker 或 trading integration。
- Investment conclusion、target price、buy/sell/hold、position size 或 research status。

## 9. Logging and Provenance

必须记录：

- Source URL 和 validated SEC domain。
- Mode、request count、timeout、minimum interval、HTTP status。
- Retrieved-at timestamp。
- SHA-256、byte size、raw snapshot path。
- CIK、accession、form、filing date 和 reporting period。
- Source/data status、verification basis、amendment awareness。
- Unresolved fields、warnings 和 errors。

不得记录完整 User-Agent、email、cookie、authorization header 或 secret。

## 10. Implementation Gates

- Fixture and mocked-live tests pass。
- Non-SEC URL blocked before fetch。
- User-Agent required for live mode。
- Redirects remain SEC-only。
- Retry、timeout、request count and response size bounded。
- Local adapter remains network-free。
- Existing v0.2.x 16-script regression passes。
- Any populated extraction adapter requires separate user approval。

Official references:

- SEC EDGAR APIs: `https://www.sec.gov/search-filings/edgar-application-programming-interfaces`
- SEC Developer Resources / Fair Access: `https://www.sec.gov/about/developer-resources`
- SEC Privacy and Security: `https://www.sec.gov/about/privacy-information`

