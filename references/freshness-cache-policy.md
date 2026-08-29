# Freshness and Cache Policy

## 1. Purpose

本政策定义 adapter 如何判断数据是否新鲜、何时可使用缓存、如何保留 raw evidence，
以及何时必须失败或要求人工刷新。

v0.3.1 只实现本地 checksum-addressed snapshot。它不判断 live source 是否最新，也不实现自动 cache refresh。Filing date、retrieved-at 和 source status 由用户显式提供并进入 manifest。

v0.3.2 可从一个用户明确指定的 SEC URL 下载 filing evidence，并记录真实
`retrieved_at`、HTTP status 和 checksum。它不执行 filing discovery、amendment chain
搜索或 latest-effective 判断，因此下载成功不等于已确认是最新有效 filing。

## 2. Freshness Classes

| Freshness class | Typical evidence | Required check |
|---|---|---|
| `real_time_or_intraday` | Intraday quote / FX | Timestamp、timezone、session、delay |
| `daily_market_snapshot` | Regular close price、market cap、EV | Trading date、session、corporate actions |
| `latest_filing` | Latest effective filing | Filing date、period、amendment chain |
| `latest_quarter` | Latest quarterly financials | Fiscal quarter、release date、later filing |
| `annual_filing` | Annual statements | Fiscal year、restatement、latest annual filing |
| `transcript` | Earnings call transcript | Event date、quarter、version/license |
| `static_company_profile` | Identity、sector、exchange | Identity change、listing status |
| `analyst_assumption` | DCF / mature multiple / classification | Owner、created_at、review_due |

## 3. Stale Data Rules

- Freshness is evaluated against `as_of_date` and request type.
- Stale market data cannot support a current price or precise valuation claim.
- A stale filing may still support historical facts but cannot be labeled latest.
- Stale data must set `source_status=partially_verified` or `indicative` as appropriate and generate a warning.
- If a required time-sensitive field is stale beyond the approved threshold, normalization must omit it or fail; it may not silently reuse an old value.
- Analyst assumptions require explicit `review_due`; expired assumptions remain visible but cannot be treated as current.

Recommended design thresholds, subject to implementation approval:

- Intraday: valid only for the documented session and delay window.
- Daily close: valid for the stated completed trading day.
- Latest filing/quarter: valid until a newer effective filing or corrected release exists.
- Transcript: valid for its event; never a current market snapshot.

## 4. Market Session Rules

Every market snapshot records:

- Timestamp with timezone.
- Trading date.
- `regular close`, `pre-market`, `after-hours`, `intraday`, `delayed close`, or `session_unverified`.
- Real-time / delayed / estimated / page snapshot.
- Currency and per-share unit.

Do not combine pre-market price with regular-close market cap or stale share count without transformation notes.

## 5. Cache Directory Design

Suggested future layout, not created or implemented in v0.3 design:

```text
evidence-cache/
├── raw/
│   └── <company>/<source_type>/<retrieved_at>-<source_id>.<ext>
├── normalized/
│   └── <company>/<as_of_date>/<schema>/<version>.<csv|json>
├── manifests/
│   └── <company>/<as_of_date>/
│       ├── raw-snapshot-manifest.json
│       ├── source-manifest.json
│       └── field-provenance.json
└── reports/
    └── <company>/<as_of_date>/<tool>-<generated_at>.md
```

## 6. No Silent Overwrite

- Existing raw snapshot is immutable.
- Same path or source ID collision causes failure unless content checksum is identical.
- Refresh creates a new retrieved timestamp and version.
- Normalized and report files use versioned paths.
- Manual replacement requires an explicit supersession record.

v0.3.1 behavior:

- 默认拒绝非空输出目录。
- `--overwrite` 只允许更新已知 manifests/reports，并在 raw manifest 和 report 中记录。
- Raw snapshot 以 checksum 命名；不同内容保留为不同文件，不静默覆盖。
- 完整 supersession lineage 与 automatic invalidation 仍属于 future implementation。

v0.3.2 延续同样的 no-silent-overwrite 规则。Live output 应写入新的空目录；显式
`--overwrite` 会记录审计标记，但不会把“已下载”提升为“latest effective”。

## 7. Reproducibility

Each calculation must be reproducible from:

- Raw snapshot checksum.
- Source manifest version.
- Field provenance version.
- Normalized input checksum.
- Script version or Git commit.
- Generated-at timestamp.
- Assumption set.

## 8. Raw Snapshot Retention

- Keep the exact bytes or faithful local representation used for extraction where licensing permits.
- Record content type, encoding, checksum and byte size.
- If content cannot legally be retained, store metadata, permitted excerpt/location and access restriction; mark reproducibility limited.
- Never commit restricted or credential-bearing content.

## 9. Derived Output Retention

- Derived outputs may be regenerated but should retain lineage.
- A changed normalized input invalidates dependent outputs.
- Do not delete prior outputs when a source is restated; mark them superseded.
- Research reports must state the evidence and calculation generation dates.

## 10. Cache Invalidation

Invalidate active normalized/derived status when:

- New filing, amendment or corrected release appears.
- Corporate action changes share basis.
- Currency or unit mapping is corrected.
- Source conflict resolution changes the selected value.
- Market snapshot exceeds freshness threshold.
- Adapter or normalization logic version changes materially.
- Input checksum changes.

Invalidation does not delete artifacts; it changes status and requires regeneration.

## 11. Failure and Fallback

| Condition | Required behavior |
|---|---|
| Live source unavailable | Use cache only if policy permits; label stale and preserve original retrieved_at |
| Cache missing | Return structured error; no fabricated fallback |
| Cache stale | Warning or hard failure depending on request |
| Source conflict | Preserve all versions; do not silently choose lower-priority source |
| Restatement found | Supersede active source, invalidate dependents |
| Timestamp/session absent | Mark unverified; exclude from precise current valuation |
| Unit/currency mismatch | Stop affected normalization unless explicit conversion exists |

## 12. Examples

### Daily market snapshot

```yaml
freshness_class: daily_market_snapshot
retrieved_at: 2026-06-24T16:10:00-04:00
market_session: regular close
source_status: indicative
stale_after: next completed regular session
fallback: retain snapshot for historical reproduction only
```

### Restated filing

```yaml
freshness_class: latest_filing
source_id: company-2025-10ka
supersedes_source_id: company-2025-10k
invalidate:
  - normalized/financials-v1.csv
  - reports/ratio-v1.md
behavior: retain old lineage and generate a new normalized version
```

### Analyst assumption

```yaml
freshness_class: analyst_assumption
created_at: 2026-06-25T10:00:00+08:00
review_due: 2026-09-30
source_status: unverified
behavior: display as assumption; never promote to company-disclosed fact
```
