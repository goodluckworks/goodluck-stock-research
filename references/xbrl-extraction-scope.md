# XBRL Extraction Scope

## 1. Purpose

本文定义 XBRL extraction prototype 的最小范围、候选值规则和人工复核 gate。
v0.3.4 已实现一个严格受限的 offline fixture subset：它只解析人工
`data-xbrl-*` fixtures、输出 draft candidates，并对 fictional EXMP 测试人工 review
与 promotion。v0.3.5 增加 machine-readable schemas、标准库 schema validation、
inline-XBRL-like / minimal instance XML 人工 fixture subset 和 package audit。
v0.3.6 增加 mapping review workflow、reviewer workbench、review decision collector、
promotion isolation hardening 和 expanded synthetic edge cases。它仍然不是 production
iXBRL parser，不解析真实完整 filing，也不执行 live extraction。v0.3.7 增加 review
checklist、taxonomy relationship metadata、review quality scoring 和短小 real-filing-excerpt
offline drill；这些 drill 仍不等于完整 filing 或真实公司 approved data。v0.3.8 增加
fictional-only normalized CSV sandbox 和 EXMP-only ratio dry-run；真实公司仍不允许
promotion、normalized CSV generation 或 v0.2.x calculation dry-run。

目标不是“一键生成财务数据”，而是把一个已保存、checksum 可验证的 official filing
raw snapshot 转换为少量、可审计、尚未批准的候选字段。任何候选值只有通过人工复核后，
才可能进入 v0.2.x 的本地 CSV / JSON。

## 2. Non-Goals

- No full automated investment report。
- No target price、recommendation、buy/sell/hold、position size 或 research status。
- No broker connection、trading、order execution 或 portfolio action。
- No ticker、CIK、accession 或 filing discovery。
- No new live source、yfinance、OpenBB、paid market data 或 credential workflow。
- No silent field population。
- No extraction without raw snapshot、source manifest 和 field provenance。
- No normalized output without a completed human review gate。
- No automatic Non-GAAP、normalized earnings、segment、AI-only revenue 或 valuation
  extraction。
- No automatic use of a candidate value by v0.2.x calculation scripts。
- No production parser claim from fixture-only parser tests。
- No real-company promotion or approved normalized input。
- No real-company normalized CSV generation or v0.2.x calculation dry-run。

## 3. First Extraction Scope

初始 prototype 只考虑 consolidated GAAP statements 中以下九个字段：

| Normalized field | Expected statement | Initial treatment |
|---|---|---|
| `revenue` | Income statement | Duration concept; consolidated total only |
| `gross_profit` | Income statement | Duration concept; unresolved if not explicitly reported |
| `operating_income` | Income statement | Duration concept; GAAP operating result |
| `net_income` | Income statement | Duration concept; attributable basis must be recorded |
| `operating_cash_flow` | Cash flow statement | Duration concept; net cash from operating activities |
| `capital_expenditure` | Cash flow / investing disclosure | Duration concept; normalized as positive cash-outflow magnitude |
| `cash_and_equivalents` | Balance sheet | Instant concept at period end |
| `total_debt` | Balance sheet / debt note | Instant concept; components require explicit anti-double-counting rule |
| `diluted_shares` | EPS statement/note | Duration concept; weighted-average diluted shares, not ending shares |

Out of scope for the first prototype:

- Segment revenue or segment profit.
- Gross margin reconstructed from cost components when gross profit is absent.
- Free cash flow or normalized earnings.
- Stock-based compensation, goodwill, intangibles and acquisition accounting fields.
- Marketable securities and net debt calculation.
- Per-share values other than source context for diluted weighted-average shares.
- TTM bridges, quarterly-to-annual reconstruction or cross-filing arithmetic.

Missing an in-scope field is a valid outcome. The extractor must emit an unresolved record rather
than derive an unsupported value.

## 4. XBRL Tag Mapping Strategy

### US-GAAP tags

- Maintain a reviewed mapping record for each normalized field.
- Prefer standard US-GAAP concepts that match statement, period type, unit and economic meaning.
- A preferred tag is not sufficient by itself; context selection and reconciliation are mandatory.
- Tag labels are supporting metadata, not a substitute for concept identity.

### Company-specific extension tags

- Extension tags may produce candidates only when `extension_tag_allowed=true`.
- Require an explicit anchor or presentation/calculation relationship to a supported US-GAAP
  concept, plus matching statement location and context.
- Extension candidates default to lower confidence than an unambiguous standard concept.
- An extension tag must never be accepted solely because its label contains a familiar word.

### Fallback behavior

- Try preferred tags, then reviewed fallback tags.
- If no candidate passes context and unit checks, emit unresolved.
- Do not scrape rendered text as an automatic fallback in the first prototype.
- Do not replace a missing GAAP field with management Non-GAAP data.

### Multiple candidate tags

When multiple candidates remain:

1. Filter to the requested legal entity and consolidated context.
2. Match fiscal period, start/end dates and instant/duration type.
3. Exclude dimensional facts unless the mapping explicitly allows the dimension.
4. Prefer the statement concept over note-only or component concepts.
5. Compare amended/restated facts and filing acceptance times.
6. Reconcile candidates to the rendered statement and calculation relationships when available.
7. If material ambiguity remains, keep all candidates and mark the field unresolved.

The prototype must not select by “first tag”, largest value, latest XML order or shortest name.

### Period matching

- Duration fields must match the requested fiscal start and end dates.
- Instant fields must match the requested period end.
- Annual and quarterly durations may not be mixed.
- YTD 10-Q values may not be labeled as standalone quarter values.
- Comparative prior-year facts require their own period identity.
- Facts from a later filing may be used only when the request's as-of policy permits them.

### Unit matching

- Monetary statement fields require the filing reporting currency.
- Share fields require `shares`; EPS or per-share units are not substitutes.
- Pure-number facts are accepted only for concepts whose mapping expects a pure number.
- Unit numerator/denominator and entity identifier must be retained in provenance.

### Sign convention

- Preserve the reported fact sign in extraction evidence.
- Apply a normalized sign only through an explicit transformation record.
- `capital_expenditure` is normalized as a positive cash-outflow magnitude for compatibility with
  current v0.2.x inputs; the source sign and `absolute_value` transformation must both be recorded.
- Debt and cash balances must not be sign-flipped unless the source presentation requires and
  documents that transformation.

### Scale conversion

- Read XBRL decimals/precision and unit metadata; do not infer scale from visual commas alone.
- Convert to the requested `amount_unit` only through a recorded factor.
- Preserve the exact extracted value before conversion.
- Reject non-finite values and ambiguous scale.
- Never round before reconciliation; final display rounding is separate from stored precision.

### Restatement and amendment

- Every candidate links to accession, filing date, acceptance timestamp and amendment status.
- A 10-K/A or 10-Q/A creates a new candidate lineage; it never silently overwrites an earlier fact.
- The prototype may not claim “latest effective” unless amendment discovery is separately
  implemented and reviewed.
- Conflicting original/amended facts require manual selection and dependent-output invalidation.

### Confidence scoring

Suggested candidate confidence:

- `high`: standard tag, exact context/unit, consolidated statement location, no competing fact,
  and rendered-statement reconciliation passed.
- `medium`: reviewed extension or fallback tag with exact context/unit and no material conflict.
- `low`: multiple candidates, uncertain dimensionality, incomplete statement reconciliation,
  unusual unit/scale or amendment uncertainty.

Confidence never replaces reviewer approval. Low-confidence fields remain unresolved.

## 5. Field Reconciliation Rules

Every extraction candidate must retain:

- Extracted value at source precision.
- Source ID, snapshot checksum, accession and source locator.
- XBRL concept QName and label.
- Context ID, legal entity identifier and dimensions.
- Period start/end or instant date.
- Unit ID, numerator/denominator, decimals and scale.
- Expected statement and observed presentation location.
- Transformation and exact expression.
- Confidence and warning flags.
- Competing candidate IDs.
- Taxonomy relationship metadata, including concept label, concept type, namespace, closest
  standard concept, anchor concept, presentation/calculation relationship notes, relationship
  confidence and evidence notes.
- Initial review checklist placeholder for period, unit, context, dimensions, sign, scale,
  relationship, competing candidates, prior period/materiality and reviewer notes.

Field-specific reconciliation:

- `revenue`: reject segment/customer/geography dimensions for consolidated revenue.
- `gross_profit`: do not compute from revenue less cost of revenue in the first prototype.
- `operating_income`: distinguish operating income from income before tax.
- `net_income`: record whether attributable to parent, consolidated entity or noncontrolling
  interests; unresolved if the requested basis is unclear.
- `operating_cash_flow`: require the operating activities total, not a component.
- `capital_expenditure`: require a reviewed PP&E acquisition/payment concept; do not mix
  acquisitions, capitalized software or business combinations without mapping approval.
- `cash_and_equivalents`: distinguish cash-only from cash plus restricted cash or short-term
  investments.
- `total_debt`: either use a reviewed total-debt concept or sum reviewed non-overlapping current
  and noncurrent components; never combine a total with its components.
- `diluted_shares`: require weighted-average diluted shares for the matching duration and
  company-restated split basis.

If any required identity, context, unit, transformation or reconciliation element is ambiguous,
the candidate remains unresolved.

## 6. Human Review Gate

Extraction output status must begin as `draft_extracted_unreviewed`.

Before any normalized CSV / JSON is written or used:

1. A reviewer inspects raw evidence, filing identity and checksum.
2. The reviewer compares the candidate to the rendered consolidated statement or note.
3. The reviewer confirms period, currency, amount unit, share basis and sign.
4. The reviewer resolves competing tags and extension-tag rationale.
5. The reviewer checks material differences from prior periods and prior approved values.
6. The reviewer selects `approve`, `adjust`, `reject`, `unresolved` or
   `needs_more_evidence`.
7. Only `approve` or `adjust` with an explicit approved value may pass the gate.

Low-confidence values cannot be approved without additional evidence and reviewer notes.
Differences exceeding a configured absolute or percentage threshold require explicit review; the
threshold must be policy input, not hard-coded silently.

v0.3.6 将复核拆成四个明确层次：

1. `mapping_review.py` 校验 mapping version 是否 approved 且未 superseded/rejected。
2. `reviewer_workbench.py` 将 draft candidates 和 provenance 渲染为人工复核 Markdown。
3. `review_decision_collector.py` 校验 reviewer decision template 并输出 normalized review batch。
4. `promote_reviewed_fields.py` 只接受 normalized review batch，不接受 raw workbench template。

v0.3.8 在 promotion 之后增加一个独立 sandbox 层：

1. `generate_normalized_csv_sandbox.py` 只接受 EXMP fictional promotion package。
2. 生成的 CSV 必须保留 review batch、promotion ID、mapping version、snapshot SHA 和 field-level audit references。
3. 生成的 CSV 必须标记 fictional、sandbox、not investment data、not company fact、not for trading 和 not production research。
4. `run_v02_sandbox_dry_run.py` 只能对 EXMP sandbox CSV 运行 `ratio_calculator.py` dry-run。
5. `end_to_end_pipeline_auditor.py` 检查 extraction、quality、review、promotion、CSV 和 dry-run 之间的链路。

v0.3.7 在 approve / adjust 之前增加两项硬门槛：

1. `review_quality_scorer.py` 必须为被批准 candidate 输出 `approval_readiness=ready`
   且没有 blocking issues。
2. Reviewer checklist 必须确认 period、unit、context、dimensions、sign、scale、
   relationship、competing candidates、prior-period/materiality 和 reviewer notes。

Relationship metadata 不足、unsupported relationship、缺失 provenance、low confidence 或
未解决 competing candidates 都会阻断 approve / adjust。

Normalized output must include the review record ID and approval timestamp. Draft extraction files
must be stored separately from approved normalized inputs.

## 7. Supported Forms

Initial supported forms:

- Form 10-K.
- Form 10-Q.

Initial unsupported forms and entities:

- 8-K earnings release extraction.
- Proxy statements.
- S-1 and other registration statements.
- 20-F, 40-F, 6-K and foreign private issuers.
- Funds, ETFs, BDCs and investment companies.
- Banks, insurers and other entities requiring specialized statements.
- SPACs, partnerships and variable-interest structures requiring custom mappings.

Unsupported input must return a structured blocking result, not a partial field population
presented as complete.

## 8. Test Fixture Plan

Use local, short, license-safe fixtures and mocked manifests before any live extraction:

- MRVL: standard/extension revenue candidates, special-item context and PP&E capex sign.
- NVDA: split-adjusted diluted shares, cash versus marketable securities and dimensional revenue
  facts.
- AVGO: acquisition-driven presentation, software/semiconductor dimensions and debt components.
- Standard tag with exact context.
- Extension tag with reviewed anchor.
- Multiple candidate tags.
- Wrong period, wrong unit and wrong entity.
- Annual versus YTD/quarter mismatch.
- Consolidated versus segment dimension.
- Amended/restated fact.
- Debt total plus components double-count trap.
- Missing gross profit.
- Capex negative presentation transformed to positive magnitude.
- Low-confidence candidate blocked by review gate.
- Approved, adjusted, rejected and unresolved review records.
- Machine-readable schema validation for extraction, review and promotion files.
- Package audit for extraction_run_id, snapshot_sha256, mapping_version and candidate_id links.
- Mapping review lifecycle cases: approved, superseded, rejected and missing evidence.
- Reviewer workbench and decision collector packages for EXMP, MRVL, NVDA and AVGO.
- Promotion isolation cases proving real-company-shaped packages remain blocked.
- Expanded synthetic edge cases for taxonomy drift, extension tags, restatements, debt, capex,
  restricted cash, diluted share duration, duration/instant mismatch, mixed units, materiality and
  dimension-only facts.

Fixtures must not contain real full filings or credentials. Expected records should test provenance
and gate behavior, not only numeric equality.

## 9. Failure Behavior

| Condition | Required result |
|---|---|
| Unsupported form/entity | Blocking error; no candidates promoted |
| Snapshot checksum mismatch | Stop extraction |
| Missing source manifest/provenance | Stop extraction |
| No mapped tag | Unresolved field |
| Multiple material candidates | Preserve candidates; manual review required |
| Period/unit/entity mismatch | Reject affected candidate |
| Extension tag without reviewed relationship | Low confidence and unresolved |
| Amendment uncertainty | Warning; no latest-effective claim |
| Scale/sign ambiguity | Unresolved; no guessed conversion |
| Review not completed | No normalized output |
| Reviewer rejects value | Preserve audit record; do not populate field |

Errors and unresolved fields must be structured. Missing values are never converted to zero.

## 10. Implementation Gates

v0.3.6 offline fixture prototype 满足本节的 draft-only 子集。任何真实 filing、
instance document、production iXBRL 或 real-company promotion 扩展仍需要单独批准：

1. Freeze the nine-field scope and supported forms.
2. Approve versioned mapping records and field-specific reconciliation rules.
3. Define candidate and review JSON schemas with validation.
4. Implement fixture-first using Python standard library unless a dependency is separately
   approved. v0.3.6 only supports the documented artificial fixture syntax and local review packages.
5. Keep source access separate from extraction; prototype reads an existing raw snapshot.
6. Preserve snapshot checksum, source manifest and field-level provenance.
7. Produce draft candidates only; normalized output remains disabled by default.
8. Require explicit human review before any local normalized file is emitted.
9. Test amendment, extension, context, unit, sign, scale and debt double-count failure cases.
10. Confirm no investment conclusion, broker, trading, credential or non-SEC network path.
11. Re-run v0.2.x regressions and adapter safety scans.
12. Complete independent review on MRVL, NVDA and AVGO synthetic fixtures.

v0.3.6 implementation status:

- Local candidate extractor: implemented.
- Versioned fixture mapping registry: implemented.
- Review validator: implemented.
- Mapping review workflow: implemented for fixture-only review batches.
- Reviewer workbench and review decision collector: implemented for local candidate packages.
- Promotion isolation hardening: implemented for fictional EXMP only.
- Fictional EXMP promotion draft: implemented.
- Real-company approval/promotion: not implemented by default and not tested.
- Live extraction and production iXBRL parsing: not implemented.

## 11. Open Questions

- Should the first prototype parse inline XBRL embedded in filing HTML, SEC filing XBRL instance
  files, or both?
- Which exact standard and fallback QNames are approved for each field and taxonomy year?
- Must extension tags have an XBRL anchoring relationship, a calculation relationship, a
  presentation relationship, or a combination?
- What numerical/materiality thresholds trigger mandatory prior-period review?
- Should `total_debt` be optional until a dedicated debt-component mapping is approved?
- How should restricted cash be handled in `cash_and_equivalents`?
- Which PP&E and capitalized-software concepts count toward `capital_expenditure`?
- What reviewer identity and signature mechanism is sufficient without collecting sensitive
  personal information?
- Should approved normalized output be generated by the extractor or by a separate promotion
  command with its own audit log?
- How are taxonomy-version changes reviewed and versioned?
