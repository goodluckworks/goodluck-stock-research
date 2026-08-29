# Goodluck Stock Research Skill

这是一个面向 Agent / Codex / Claude 的结构化股票研究 Skill。v0.2 在既有研究流程、来源规范、财务质量检查、估值纪律、反方观点、thesis kill criteria 和可复用模板之外，增加了读取本地 CSV / JSON 的基础计算工具层。默认输出仍是完整 Markdown 研究报告；Obsidian 公司卡片只是可选归档功能。

默认输出为中文，必要的金融术语保留英文。适用市场以美股为主，同时兼容 A 股、港股和其他上市公司。

## 适用场景

- 快速了解一家公司或 ticker。
- 生成 company deep dive 研究框架。
- 更新财报后判断 thesis 是否增强或削弱。
- 做 valuation review、market-implied expectation 或情景估值。
- 跟踪观察池、持仓、候选公司或行业主题。
- 对 AI infrastructure / AI supply chain 股票做额外 overlay。
- 在用户明确要求时，额外生成 Obsidian-ready 公司卡片和研究记录。

## v0.2.4 工具增强

- Ratio tool 显式记录 cash / short-term investments 的 net debt basis。
- Ratio tool 结构化记录 goodwill、intangibles、acquisition amortization、restructuring / integration costs 和 acquisition-related costs。
- Peer comps 同时输出 blended peer statistics 与 core comparable statistics。
- Implied expectations 支持有来源的 normalized earnings basis，并在回退到 reported GAAP 时提示风险。
- AVGO 回归覆盖并购驱动、半导体加基础设施软件双主业，以及 AI infrastructure narrative 与 consolidated financials 的分离。
- 所有增强仍只读取本地 CSV / JSON；不联网、不接 API、不执行交易。

## v0.3 Architecture 状态

v0.2.x 本地工具层已完成。v0.3 architecture design 已完成；v0.3.1 实现
local-file evidence packaging，v0.3.2 新增极窄范围的 SEC official filing
evidence adapter。v0.3.3 scope release 只定义未来 XBRL extraction 的字段范围、
mapping schema 和人工 review gate。v0.3.4 在此基础上实现 offline fixture-only
candidate extractor、review validator 和 fictional EXMP promotion draft。v0.3.5
进一步增加 machine-readable schemas、标准库 schema validator、offline inline-XBRL-like /
minimal instance XML fixture subset，以及 package-level audit。v0.3.6 增加 mapping
review workflow、reviewer workbench、review decision collector、promotion isolation
hardening 和 expanded synthetic edge cases。v0.3.7 增加 reviewer checklist、review
quality scoring、taxonomy relationship metadata、mapping relationship review hardening
和短小 real-filing-excerpt offline review drill。v0.3.8 增加 fictional-only normalized
CSV sandbox、EXMP-only v0.2.x ratio dry-run 和 end-to-end offline pipeline audit。
v0.3.9 增加 partial-field handling 和 unresolved-field UX，让 EXMP sandbox 在部分字段
获批时仍能 dry-run，同时清楚披露 unavailable ratios 和 missing inputs。
v0.3.10 增加 offline review-gated pipeline orchestrator，把本地 example packages 串成
EXMP fictional sandbox full/partial flow 和 MRVL/NVDA/AVGO review-only flow。
v0.3.11 增加 sandbox/review-only research packet builder，用于把 pipeline output 整理成
可读 packet，但不是投资报告。
v0.3.12 增加 pipeline audit dashboard 和 blocked real-company matrix，用于集中检查
pipeline runs、packet status 和真实公司 block 状态。
v0.4.0 将这些能力稳定整合为 review-gated offline research pipeline，但默认研究输出
仍是完整 Markdown 报告，pipeline 是可选本地工具链。

v0.5.0 增加 offline packet QA、artifact hygiene checker 和 public-readiness audit。该阶段
只审查本地 tracked artifacts、research packets、dashboard 和发布准备度；它不公开仓库，不改变
MRVL/NVDA/AVGO review-only 边界，也不允许真实公司 promotion。
v0.5.1 增强 dashboard quality checker 和 synthetic edge-case coverage，用于确认 blocked
matrix、blocked reasons、audit completeness、partial-field downstream impact 和 forbidden
conclusion-field checks。
v0.5.2 增强 MRVL/NVDA/AVGO review-only packet QA，明确候选字段、unresolved explanations、
quality/workbench references、reviewer evidence checks 和 `Suitable for promotion: No`。
v0.6.0 增加 controlled real-company sandbox gate。该 gate 默认关闭，必须显式传入
`--allow-real-company-sandbox`、`--quarantine-output`、`approved_for_quarantine` review batch、
`ready_for_quarantine` quality score 和 quarantine output path。v0.6 tracked example 只允许
MRVL quarantined sandbox drill；NVDA/AVGO 仍默认 blocked。
v0.7.0 增加 parser-readiness、evidence reconciliation 和 taxonomy drift 审计层，用于确认
fixture-first parser prototype 的候选值、source locator、mapping lineage、review decision、
quality score 和 quarantine manifest 是否可追溯。默认结论仍是 `production_parser_ready: No`；
它不实现 production parser，不做 live extraction。
v0.7.1 增加 quarantine QA、filing identity checker 和 amendment/restatement drill，要求
ticker、CIK、accession、form、filing date 和 snapshot hash 在 review / quality / quarantine
链条中一致；amendment 触发 supersession warning，restatement conflict 阻断 production readiness。
v0.8.0 增加 controlled multi-company quarantine dashboard。MRVL tracked quarantine drill
保持通过；NVDA/AVGO 若没有完整显式 gate data，则保持 blocked，并且不创建 tracked quarantine output。
v0.8.1 增加 calculation guardrails 和 quarantined ratio runner policy。真实公司 quarantine
下只允许 ratio-only dry-run；DCF、peer comps、implied expectations、target price、recommendation、
position size 和 research status 均被阻断。
v0.9.0 增加 review-gated research report builder。EXMP、MRVL、NVDA、AVGO 均可生成对应
report packet，但真实公司 packet 只汇总 quarantine/review evidence、unresolved fields 和 audit
references，不输出投资结论。
v0.9.1 增加 report red-team audit，确保 report builder 不能绕过 target price / buy-sell-hold /
position size / production claim / candidate-as-fact / missing-audit-reference 等边界。
v0.9.5-rc 增加 release-candidate audit、security boundary audit 和 copyright/artifact audit，
检查 README/SKILL/CHANGELOG 准确性、无完整 filing 文本、无本地路径泄漏、无密钥、无 cache、
无 production parser / live extraction / investment advice claim。Public readiness 需要用户单独决策。

v1.0.0 是 stable review-gated stock research Skill。它整合本地 evidence workflow、
parser-readiness audit、evidence reconciliation、controlled quarantine sandbox、quarantined
calculation guardrails、review-gated report packets、red-team audit 和 release-candidate audit。
Public readiness 状态为 `Needs user decision`，仓库默认继续保持 private。

v1.1.0 启动 v2 production research system 路线，新增 `production/` 架构、source policy、
research conclusion policy 和 approval policy。该阶段只定义 production system 边界，不实现 live parser。
v1.2.0 增加 controlled SEC live ingestion、filing identity resolver 和 amendment discovery。
它支持 fixture mode 与 explicit SEC URL live mode，后者必须使用 SEC-only HTTPS、explicit User-Agent、
bounded timeout/request count/response size。该阶段不解析财务字段。
v1.3.0 增加 scoped production XBRL parser MVP。Parser 只读本地 filing package，不联网；范围限制为
10-K / 10-Q 和九个基础字段。Ambiguous、wrong period、wrong unit、dimensional fact 均保持 unresolved。
v1.4.0 增加 normalized financial statement builder。它从 parsed facts 生成 normalized income
statement、balance sheet、cash flow、metrics input、manifest、unresolved fields 和 audit report，
并保留 provenance / confidence / review status。
v1.5.0 增加 data quality scoring、reconciliation engine 和 quality gate。Restatement conflict、
missing provenance、low parser confidence 和 unit mismatch 会阻断 production；unresolved fields 会要求复核。
v1.6.0 增加 valuation and scenario engine。估值只在 quality gate 通过后运行，输出 scenarios、
sensitivity、assumptions 和 confidence；fair value range 不是 recommendation。
v1.7.0 增加 evidence-backed research conclusion engine。它可以输出 constructive / neutral /
cautious / negative / insufficient_evidence 等研究观点，但必须解释 evidence basis、valuation basis、
data quality caveats 和 missing evidence。
v1.8.0 增加 production report builder 和 approval gate。生产报告 draft 需要质量、结论、报告审计
均通过，并且有 human approval record，才能标记为 publishable research packet。
v1.9.0 增加 MRVL production pilot，使用 fixture/local inputs 串联 production pipeline，并生成
internal research packet、publication manifest 和 pilot audit。输出不是个性化建议，不是交易指令。
v1.9.5-rc 增加 production red-team 和 release-candidate audit，覆盖 parser guessing、missing
provenance、low quality data usage、approval bypass、trade instruction、position size、credential /
broker / trading code 等失败模式。

v2.0.0 是 production research system stable release。它支持 controlled live SEC ingestion、
scoped production XBRL parser MVP、normalized financial statements、data quality gate、valuation
scenarios、evidence-backed research conclusion engine、approval-gated report packets 和 MRVL production
pilot。v2.0 仍不接 broker、不交易、不下单、不读取 secrets、不输出 personalized advice 或 position sizing。

v3.0.0 是 final usable live production research system release。它在 v2.0 之上增加 live source
registry、company IR source、market data CSV / controlled source fallback、multi-filing historical financials、
parser hardening、comps and market multiples、full valuation suite、real-company workflow、production CLI、
reliability/cache/error recovery、source monitoring、accuracy audit 和 final red-team。v3.0 可以生成完整
research report draft、valuation scenarios、research conclusion、source manifests、data-quality report 和 audit trail。

运行示例：

```bash
python3 goodluck-stock-research/production/cli.py research --ticker MRVL --mode fixture
python3 goodluck-stock-research/production/cli.py research --ticker NVDA --mode fixture
python3 goodluck-stock-research/production/cli.py validate --run-dir goodluck-stock-research/examples/production_research/MRVL
```

使用 live SEC 或 market data 时，必须检查 source manifest、data quality、valuation assumptions、
research conclusion 和 workflow audit。Market data 优先使用 user-provided CSV；如果 source 不可靠或不可得，
系统必须输出 `insufficient_market_data` caveat，而不是编造数据。

v3.0 仍不支持 broker integration、trading execution、order routing、portfolio allocation、position sizing、
personalized financial advice、guaranteed return 或 hidden credential / secret workflow。

设计规定：

- Future adapter 只读、source-backed。
- Adapter 先保存 raw evidence、source manifest 和 field provenance。
- Adapter 只生成本地 normalized CSV / JSON，再交给 v0.2.x scripts。
- Adapter 不输出投资结论、研究状态、交易动作或仓位建议。
- Optional-key adapter 需要单独审批；credentials 不存储在本 Skill。

## v0.3.2 SEC Filing Adapter

`adapters/sec_official_filing_adapter.py` 支持离线 fixture mode 和显式 SEC URL 的
live mode：

- 默认测试不联网，使用本地 fixture。
- Live mode 必须由用户明确提供 `source_url` 和带身份/联系信息的 User-Agent。
- 网络范围只允许 SEC 官方 HTTPS 域名，GET only，并受 timeout、限速、请求数和
  响应大小限制。
- 输出 raw snapshot metadata、source manifest、field provenance、unresolved fields、
  structured errors 和 run report。
- 不做 ticker discovery、CIK resolution、accession discovery、submission crawl、
  XBRL extraction 或财务字段 population。
- 不生成投资结论、研究状态、target price、交易或仓位动作。

## v0.3.3 Extraction Scope Design

`references/xbrl-extraction-scope.md`、`schemas/xbrl_field_mapping_schema.md` 和
`schemas/extraction_review_schema.md` 定义未来 prototype 的边界：

- 初始只考虑 revenue、gross profit、operating income、net income、operating cash
  flow、capital expenditure、cash and equivalents、total debt 和 diluted shares。
- 每个候选值必须保留 XBRL tag、context、period、unit、scale、sign、snapshot hash 和
  field provenance。
- Company extension tags、多个候选、dimensions、amendment/restatement 和 taxonomy
  drift 必须显式处理。
- Extraction 产物只能是 `draft_extracted_unreviewed` 候选。
- 只有人工 `approve` 或 `adjust` 后，独立 promotion gate 才能生成本地 normalized
  input。
- `stock-research-v0.3.3-scope` 本身不含 extraction code、populated normalized
  output 或自动投资结论；v0.3.4 只实现下述 offline fixture subset。

## v0.3.4 Offline Candidate Prototype

`xbrl/` 提供三个本地标准库工具：

- `offline_xbrl_candidate_extractor.py`：读取人工 fixture 与 versioned mapping，输出
  draft candidates、provenance 和 unresolved fields。
- `extraction_review_validator.py`：验证 review decision、approval value、confidence、
  snapshot checksum 和 mapping version。
- `promote_reviewed_fields.py`：只把通过 review 的 fictional records 写入 auditable
  approved normalized draft。

边界：

- 不联网，不读取真实 SEC live snapshot，不解析任意完整 filing。
- 只支持 `fixtures/README.md` 描述的本地人工 fixture subset。
- MRVL、NVDA、AVGO examples 永远是 synthetic draft/unreviewed candidates。
- 只有 fictional EXMP example 包含 promotion output。
- Promotion 不生成或替换 v0.2.x CSV，也不调用 calculation scripts。
- Human review gate 必须先通过；真实 ticker 默认被 promotion 阻断。

## v0.3.5 Machine-Validated Offline Package

v0.3.5 在 v0.3.4 之上增加：

- `xbrl/schemas/*.json`：manifest、candidate、mapping、review、promotion 等
  machine-readable schemas。
- `xbrl/schema_validator.py`：标准库 validator，支持单文件和 package 目录验证。
- `xbrl/package_auditor.py`：跨 extraction/review/promotion 的一致性 audit。
- `fixtures/*_inline_xbrl_like.html`：更接近 inline XBRL 结构的短人工 fixtures。
- `fixtures/exmp_instance_document.xml`：minimal instance-document XML fixture subset。

边界不变：

- 不做 live extraction。
- 不宣称 production iXBRL parser。
- 不读取完整真实 filing 或外部 taxonomy URL。
- MRVL、NVDA、AVGO 保持 draft-only。
- 不对真实公司 promotion，不生成 approved normalized input。
- 不生成 v0.2.x populated CSV，也不调用 calculation scripts。

## v0.3.8 Fictional Normalized Sandbox

v0.3.8 在 review-gated prototype 后增加一个严格隔离的端到端 sandbox：

```text
EXMP fictional fixture
  -> candidate extraction
  -> reviewer workbench
  -> quality score
  -> normalized review decision batch
  -> approved-field promotion
  -> sandbox normalized v0.2.x CSV draft
  -> ratio_calculator dry-run
  -> end-to-end audit report
```

新增工具：

- `xbrl/generate_normalized_csv_sandbox.py`：只接受 EXMP fictional promotion package，生成 `normalized_financials_sandbox.csv`、manifest、field audit 和 report。
- `xbrl/run_v02_sandbox_dry_run.py`：只接受 EXMP sandbox CSV，in-process 调用 `ratio_calculator.py` 生成 sandbox dry-run output。
- `xbrl/end_to_end_pipeline_auditor.py`：检查 extraction、quality、review、promotion、CSV 和 dry-run 之间的 ID、mapping、snapshot、field value 和 sandbox label 链路。

边界：

- 只允许 EXMP fictional sandbox CSV generation。
- MRVL、NVDA、AVGO 仍不允许 promotion、normalized CSV generation 或 v0.2.x dry-run。
- Promotion 不自动调用 v0.2.x scripts；ratio dry-run 必须由单独命令显式触发。
- v0.3.8 只 dry-run ratio calculator，不运行 DCF、peer comps 或 implied expectations。
- CSV 和 dry-run 输出必须标记 fictional、sandbox、not investment data、not company fact、not for trading 和 not production research。
- 不做 live extraction，不宣称 production parser，不生成投资结论。

## v0.3.1 Local Filing Adapter

`adapters/local_official_filing_adapter.py` 已实现 design contract 的第一个本地、只读子集：

- 输入是用户已下载的本地 official filing 文件或短 fixture。
- 输出 raw snapshot、source manifest、field provenance、unresolved fields 和 run report。
- 生成 `draft_unpopulated` normalized input draft，但不填财务数字。
- 不打开 `source_url`；该值只作为 citation string。
- 不联网、不调用 SEC API、不抓取网页、不做完整 XBRL extraction。
- 不生成研究状态、投资结论、target price、仓位或交易动作。

使用说明见 `adapters/README.md`。MRVL、NVDA、AVGO 示例位于 `examples/adapter_runs/`。

## 工具与设计边界

- 包含文档、模板、检查清单、输入 schema 和本地 Python 计算脚本。
- 脚本只读取用户或 Agent 提供的本地 CSV / JSON，不自动获取数据。
- v0.3 design 文档不改变 scripts 的本地文件边界。
- v0.3.1 adapter 也不直接调用或绕过计算脚本；人工 normalization 后才进入 v0.2.x 输入。
- v0.3.6 reviewer workbench 和 decision collector 只生成复核 workspace、decision log
  和 normalized review batch；不生成 populated v0.2.x CSV。
- v0.3.7 review quality score 是人工复核辅助，不自动 approve 字段；promotion 仍需
  normalized review batch、ready quality score、approved mapping review 和 package audit。
- v0.3.7 real-filing excerpt drill 只保存短小摘录结构；不是完整 filing，不是权威财务
  数据，不允许 MRVL、NVDA、AVGO promotion。
- v0.3.8 normalized CSV sandbox 只允许 EXMP fictional fixture；真实公司没有 approved
  normalized input、populated v0.2.x CSV 或 calculation dry-run。
- v0.3.8 end-to-end audit 只证明 sandbox audit trail 完整，不证明生产 extraction 能力。
- v0.3.9 partial-field policy 要求缺失字段保持空白，不自动填 0；downstream impact
  必须披露 available / unavailable ratios 和 missing inputs。
- v0.3.10 pipeline orchestrator 是可选本地工具链；真实公司 pipeline 只能 review-only，
  不生成 promotion、normalized CSV 或 v0.2.x dry-run。
- v0.3.11 research packet 只总结 sandbox 或 review-only evidence，不生成 target price、
  buy/sell/hold、position size、research status 或 trading action。
- v0.3.12 dashboard 只审计本地 pipeline outputs，不触发 live extraction、promotion 或
  calculation dry-run。
- v0.4 pipeline 不改变默认研究报告工作流；它只处理 local files / fixtures / approved
  EXMP sandbox，不把 draft candidates 当事实。
- v0.5 QA 工具只审计本地 artifacts、packet completeness、blocked matrix、path hygiene 和
  public-readiness；默认 public-ready 仍为 No。
- v0.5.1 dashboard quality checker 只读取本地 dashboard / pipeline / packet artifacts；
  它不触发 pipeline、不生成新 extraction、不启用真实公司 promotion。
- v0.5.2 real-company review packet QA 只确认 MRVL/NVDA/AVGO review-only packet 可审查；
  它明确 promotion suitability 为 No，不生成 approved normalized input。
- v0.6 controlled sandbox gate 只生成 quarantined MRVL sandbox CSV 和 ratio dry-run；
  输出不是 production data、不是 investment data、不是 company fact until verified、not for trading、
  not for public release。
- v0.6 仍不允许 DCF、peer comps、implied expectations、完整研究报告、target price、
  buy/sell/hold、position size 或 research status。
- v0.5 删除完整 raw filing HTML/HTM tracked examples；adapter reports 和 manifests 保留
  checksum/provenance 记录，但完整 raw filing 不应提交到仓库。
- 除 v0.3.2 明确、受限的 SEC official filing GET 外，不接入其他 live API 或网页来源。
- 不包含 API key、密钥、券商凭证或任何敏感信息。
- 不做自动交易、下单、仓位自动调整或交易信号执行。
- 不编造数据，不生成无依据的买卖建议。
- 所有关键财务和市场数据必须要求注明来源、期间或获取时间、币种、口径和时间戳。
- 计算结果只保证逻辑可审计，不保证输入数据准确，也不能替代最终研究判断。
- 不替代个人投资判断。
- 适合个人研究、小范围分享和朋友之间的研究交流；朋友不需要拥有相同的 Obsidian 结构即可阅读完整报告。

## 目录结构

```text
goodluck-stock-research/
├── SKILL.md
├── README.md
├── adapters/
│   ├── README.md
│   ├── local_official_filing_adapter.py
│   ├── sec_official_filing_adapter.py
│   └── tests/
├── qa/
│   ├── offline_packet_qa.py
│   ├── public_readiness_audit.py
│   ├── artifact_hygiene_checker.py
│   └── tests/
├── xbrl/
│   ├── offline_xbrl_candidate_extractor.py
│   ├── extraction_review_validator.py
│   ├── promote_reviewed_fields.py
│   ├── schema_validator.py
│   ├── package_auditor.py
│   ├── review_quality_scorer.py
│   ├── schemas/
│   ├── mappings/
│   ├── fixtures/
│   ├── review_fixtures/
│   └── tests/
├── scripts/
│   ├── README.md
│   ├── ratio_calculator.py
│   ├── dcf_sensitivity.py
│   ├── peer_comps_table.py
│   └── implied_expectations.py
├── schemas/
│   ├── adapter_contract_schema.md
│   ├── source_manifest_schema.md
│   ├── field_provenance_schema.md
│   ├── raw_snapshot_manifest_schema.md
│   ├── xbrl_field_mapping_schema.md
│   ├── extraction_review_schema.md
│   ├── financials_input_schema.md
│   ├── valuation_input_schema.md
│   ├── peer_comps_input_schema.md
│   └── assumptions_schema.md
├── references/
│   ├── source-registry.md
│   ├── citation-standard.md
│   ├── research-workflow.md
│   ├── financial-quality-checklist.md
│   ├── valuation-methods.md
│   ├── risk-and-kill-criteria.md
│   ├── ai-infrastructure-stock-framework.md
│   ├── status-taxonomy.md
│   ├── xbrl-extraction-scope.md
│   └── red-flags.md
├── templates/
│   ├── quick-tearsheet.md
│   ├── company-deep-dive.md
│   ├── earnings-update.md
│   ├── valuation-note.md
│   ├── thesis-tracker.md
│   └── obsidian-company-card.md
├── scoring/
│   ├── three-veto-nine-score.md
│   └── scoring-output-template.md
├── examples/
│   ├── example-research-brief.md
│   ├── data/
│   └── outputs/
└── validation/
    ├── acceptance-test-report.md
    ├── live-source-test-MRVL.md
    └── v0.2-data-tools-validation.md
```

## 文件分工

- `SKILL.md`：Skill 入口，定义触发场景、默认流程、研究模式、反幻觉规则和输出要求。
- `references/`：研究规则、来源优先级、引用规范、财务检查清单、估值方法、风险框架和 AI 产业链 overlay。
- `references/status-taxonomy.md`：集中定义最终研究状态，避免模板漂移。
- `templates/`：可直接复制使用的研究输出模板。
- `scoring/`：三否决九计分框架和评分输出模板。
- `scripts/`：标准库 Python 本地计算工具，不联网、不取数、不交易。
- `adapters/`：official filing evidence packaging 工具；包括完全离线的 local adapter
  和仅支持显式 SEC URL 的受限 live-capable adapter。
- `xbrl/`：offline artificial-fixture candidate extraction、human review validation
  和 fictional-only promotion prototype；v0.3.5 增加 machine-readable schemas、
  schema validation、fixture-format tests 和 package audit；v0.3.6 增加 mapping
  review、reviewer workbench、decision collector、promotion isolation tests 和
  expanded synthetic edge-case fixtures；v0.3.7 增加 review quality score、taxonomy
  relationship metadata、checklist schema 和 real-excerpt drill tests。
- `schemas/`：四类输入文件的字段、单位、时间戳和来源状态约束。
- `schemas/xbrl_field_mapping_schema.md` 与 `schemas/extraction_review_schema.md`：
  future extraction candidate mapping 和人工 approval gate 的设计契约，不是实现。
- `examples/`：虚构输入和脚本生成输出，不能用于投资判断。
- `validation/`：版本验收、真实来源测试和本地工具验证记录。

## 使用方式

当用户要求分析某只股票、上市公司、财报、估值或投资 thesis 时，Agent 应先读取 `SKILL.md`，再根据研究模式选择对应 reference 和 template。

默认输出完整研究报告。只有在用户明确要求 Obsidian、Obsidian card 或 Obsidian-ready note 时，才直接输出 Obsidian 公司卡片。如果完整报告适合归档，可以在报告结尾询问是否需要额外生成 Obsidian 公司卡片。

每次研究都必须先识别：

- ticker
- exchange
- reporting currency
- latest reporting period
- research objective
- investment horizon

如果关键字段缺失，应明确写入 `next checks`，不能用猜测补齐。

当用户提供符合 schema 的本地数据时，Agent 可以调用 `scripts/` 生成财务比率、DCF 敏感性、同业估值和市场隐含预期反推。使用结果时必须同时引用输入文件、来源和口径，并说明这是 `基于所列输入的计算结果`。

## 输出原则

- 区分事实、推断、假设、观点。
- 包含 bear case 和 thesis kill criteria。
- 对高估值成长股反推市场隐含预期。
- 对周期股区分 peak earnings 与 normalized earnings。
- 对 AI 产业链公司区分真实收入受益与叙事受益。
- 最终状态只能使用 Skill 规定的状态标签。

每份正式研究输出只需要在开头或结尾保留一句简洁提示：`本文仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。`

## 未来升级方向

- 经单独批准、fixture-first 且人工 review-gated 的 filing/XBRL extraction prototype；
  当前 SEC adapter 仍只保存证据。
- yfinance 或其他市场数据接口。
- 更完整的三表联动模型。
- 可配置的多阶段 DCF 和 SOTP。
- 行业专用同业筛选与可比性调整。
- Obsidian 自动归档。
- 持仓/观察池定期跟踪。
- 财报 transcript 摘要和管理层措辞变化跟踪。
- 行业 watchlist 自动化更新。
- 数据质量审计和来源覆盖率评分。
