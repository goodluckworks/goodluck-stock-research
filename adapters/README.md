# Official Filing Evidence Adapters

本目录包含两个边界不同、互不替代的 official filing evidence adapter：

- `local_official_filing_adapter.py`：v0.3.1，本地文件模式，完全不联网。
- `sec_official_filing_adapter.py`：v0.3.2，默认使用离线 fixture；只有显式选择
  `--mode live`、提供单个 SEC `source_url` 和合规 `--user-agent` 时才执行受限
  SEC 官方 GET。

两者都只生成 evidence package，不做财务字段抽取、XBRL 解析、normalized financial
population、估值结论或交易动作。

## SEC Official Filing Adapter

`sec_official_filing_adapter.py` 是 live-capable but narrow 的 SEC 官方 filing
evidence adapter。

### 允许范围

- Fixture mode 从本地短 fixture 生成 evidence package，不联网。
- Live mode 只访问用户明确提供的 `https://sec.gov`、`https://www.sec.gov` 或
  `https://data.sec.gov` URL。
- 只使用 GET；关闭环境代理继承，不使用 cookie、login、authentication 或 credential。
- Live mode 强制提供包含身份和联系信息的 User-Agent。
- 请求有 timeout、最小间隔、最大请求次数和最大响应大小。
- 保存 status code、retrieved_at、source URL、SHA-256、manifest、provenance 和
  structured errors。

### 明确不做

- 不做 ticker discovery、CIK resolution 或 accession discovery。
- 不扫描 company submissions，不批量下载。
- 不做 XBRL 或财务字段抽取。
- 不生成 populated normalized input；只生成 `draft_unpopulated`。
- 不生成 target price、buy/sell/hold、position size 或 research status。
- 不访问非 SEC 网络来源，不使用 API key，不连接券商，不交易。

### Fixture 示例

```bash
python3 goodluck-stock-research/adapters/sec_official_filing_adapter.py \
  --mode fixture \
  --input-file goodluck-stock-research/adapters/tests/fixtures/sec_filing_document_sample.html \
  --company "Marvell Technology, Inc." \
  --ticker MRVL \
  --cik 1835632 \
  --form-type 10-K \
  --accession 0001835632-26-000011 \
  --filing-date 2026-03-11 \
  --reporting-period FY2026 \
  --fiscal-year 2026 \
  --fiscal-quarter FY \
  --source-url "https://www.sec.gov/Archives/edgar/data/1835632/000183563226000011/mrvl-20260131.htm" \
  --currency USD \
  --amount-unit "USD millions" \
  --per-share-unit "USD/share" \
  --output-dir goodluck-stock-research/examples/adapter_runs_sec/MRVL
```

Fixture mode 中 `source_url` 只作为 metadata 保存，不会打开。Live mode 还必须添加
`--user-agent "Organization contact@example.com"`，并应把输出写到新的空目录。

SEC 访问规则见 `references/sec-access-policy.md`。

## Local Official Filing Adapter

`local_official_filing_adapter.py` 是 v0.3.1 的 local-file-only evidence packaging adapter。

它读取用户已经下载到本地的官方 filing 文件或测试 fixture，生成可审计 evidence package。它不是 live EDGAR adapter，不下载 filing，不打开 URL，不调用 SEC API，也不做完整 XBRL/财务字段抽取。

## 能做什么

- 读取一个本地文件。
- 计算 SHA-256。
- 保存 checksum-addressed raw snapshot。
- 生成 raw snapshot manifest、source manifest 和 field provenance。
- 生成结构化 unresolved fields、warnings 和 errors。
- 生成未填充的 normalized input draft。
- 生成 Markdown run report。

## 不做什么

- 不联网，不抓取网页，不调用 `data.sec.gov`。
- 不读取 API key、token、password、secret 或环境变量。
- 不调用 subprocess 或浏览器。
- 不连接券商，不交易，不下单。
- 不解析完整 filing/XBRL。
- 不生成 target price、buy/sell、position size、research status 或投资结论。

## 示例

```bash
python3 goodluck-stock-research/adapters/local_official_filing_adapter.py \
  --input-file goodluck-stock-research/adapters/tests/fixtures/sample_mrvl_filing_excerpt.html \
  --company "Marvell Technology, Inc." \
  --ticker MRVL \
  --source-type official_filing \
  --form-type 10-K \
  --filing-date 2026-03-11 \
  --reporting-period "FY2026" \
  --fiscal-year 2026 \
  --fiscal-quarter FY \
  --source-url "local-fixture://sample_mrvl_filing_excerpt.html" \
  --currency USD \
  --amount-unit "USD millions" \
  --per-share-unit "USD/share" \
  --output-dir goodluck-stock-research/examples/adapter_runs/MRVL
```

`--source-url` 仅保存为 citation string，即使值为 `https://...` 也不会被打开。

`source_status` 和 `data_status` 是用户提供的 metadata。Adapter 只验证本地文件可读性和 checksum，不验证 filing 真伪、完整性或是否为最新有效版本。

## Overwrite policy

- 输出目录为空时正常生成。
- 输出目录非空时默认失败。
- `--overwrite` 允许更新已知 manifest/report。
- Raw snapshot 使用 checksum 文件名；不同内容创建新 snapshot，旧 snapshot 不删除。
- Run report 和 raw manifest 会记录 `overwrite_used`。

## 输出

- `raw_snapshot_manifest.json`
- `source_manifest.json`
- `field_provenance.json`
- `unresolved_fields.json`
- `normalized_input_draft.json`
- `adapter_run_report.md`
- `raw/<checksum-addressed snapshot>`

## 与 v0.2.x 的关系

本 adapter 只打包 evidence。财务字段仍需人工 normalization 或未来单独批准的 extraction adapter，然后才能形成符合以下 schema 的本地文件：

- `financials_input_schema`
- `valuation_input_schema`
- `peer_comps_input_schema`
- `assumptions_schema`

现有 v0.2.x scripts 继续只读取本地 CSV / JSON。

## 与 v0.4 pipeline 的关系

v0.4 pipeline 不改变 adapter 边界。Adapter 仍只生成 evidence package；pipeline 只读取本地
fixture/example packages 和 approved fictional sandbox outputs，不会让 adapter 自动抽取财务字段、
不会把 draft candidates 当事实，也不会对真实公司生成 promotion、normalized CSV 或 dry-run。
