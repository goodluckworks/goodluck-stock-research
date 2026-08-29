---
name: goodluck-stock-research
description: Use this skill for structured equity research on listed companies, including business analysis, financial quality review, valuation, catalysts, risks, thesis tracking, portfolio watchlists, optional Obsidian-ready output, and auditable local CSV/JSON calculations for financial ratios, DCF sensitivity, peer comps, and market-implied expectations. Use when the user asks to analyze a stock, public company, earnings result, valuation, investment thesis, sector-related equity idea, portfolio watchlist item, local valuation data, 股票分析, 公司研究, 财报更新, 估值分析, 投资逻辑, 财务比率计算, DCF 敏感性, 同业估值, 市场隐含预期, 观察池, 持仓复核, or AI 产业链公司分析.
---

# Goodluck Stock Research

## Purpose

Use this skill to produce structured, source-aware equity research for listed companies. The skill is designed for investment research, not trading execution. It emphasizes research process, evidence quality, financial data hygiene, valuation discipline, bear-case thinking, thesis tracking, and clear full-report output. Obsidian output is optional and should be generated only when requested or offered as a follow-up.

Default output language is Chinese, while keeping standard English financial terms such as revenue, gross margin, free cash flow, EBITDA, DCF, bear case, base case, bull case, thesis, catalyst, and kill criteria.

## When To Use This Skill

Use this skill when the user asks for:

- A stock or listed-company analysis.
- A quick tearsheet for a ticker or public company.
- A company deep dive or investment thesis.
- An earnings result review or update.
- A valuation review, including multiples, DCF, SOTP, or market-implied expectations.
- A sector-related public-equity idea or watchlist candidate.
- A thesis tracker, portfolio review note, or optional Obsidian company card.
- An AI infrastructure or AI supply chain equity overlay.

Before starting any research, identify and state:

- `ticker`
- `exchange`
- `reporting currency`
- `latest reporting period`
- `research objective`
- `investment horizon`

If any of these are unknown, mark them as unknown and add them to `next checks`.

## When Not To Use This Skill

Do not use this skill for:

- Private-company diligence unless the user explicitly wants a public-equity-style framework.
- Automated trading, signal execution, order routing, position sizing automation, or brokerage integration.
- Claims that require real-time market data when no current source is available.
- Tax, legal, accounting, or personalized financial advice.
- High-confidence conclusions based on incomplete, stale, unsourced, or unverifiable data.

If the user asks for a buy/sell recommendation, reframe the output as evidence, scenarios, risks, valuation range, and a research status. Do not provide unsupported buy/sell instructions.

## Default Workflow

1. Confirm the research object and scope: ticker, exchange, reporting currency, latest reporting period, research objective, and investment horizon.
2. Build a source plan using `references/source-registry.md` and `references/citation-standard.md`.
3. Mark unknown fields explicitly as `未披露`, `未验证`, `暂无可靠来源`, `不适用`, or `待核实`; add key gaps to `Next Checks`.
4. Select the research mode and read the relevant template/reference files.
5. Separate all claims into facts, inferences, assumptions, and opinions.
6. If the user provides suitable local CSV / JSON, optionally run the relevant tool in `scripts/` after validating its schema; preserve the input provenance in the report.
7. If the user explicitly asks for local pipeline tooling, use the v0.4 review-gated pipeline only on local files / fixtures / approved EXMP sandbox outputs; never treat draft candidates as facts.
8. Review business model, industry position, competition, financial quality, valuation, catalysts, and risks.
9. Include bear case and thesis kill criteria.
10. Check the three vetoes before any final status decision.
11. Run the nine-score framework only when required by mode or user request.
12. Output a full Markdown research report by default, then sources and next checks, then final research status, then ask whether to add an Obsidian card when useful.

## Research Modes

### 1. `quick_tearsheet`

Use for a fast first-pass view of a company or ticker. Read `templates/quick-tearsheet.md`. Include business summary, revenue structure, recent financial performance, valuation snapshot, bull case, bear case, risks, and next checks.

### 2. `company_deep_dive`

Use for a full research note. Read `references/research-workflow.md`, `references/financial-quality-checklist.md`, `references/valuation-methods.md`, `references/risk-and-kill-criteria.md`, `scoring/three-veto-nine-score.md`, and `templates/company-deep-dive.md`.

### 3. `earnings_update`

Use after quarterly or annual results. Read `templates/earnings-update.md`, `references/citation-standard.md`, and the financial quality checklist. Compare results against prior thesis, management guidance, and market expectations only when those expectations are sourced.

### 4. `valuation_review`

Use when the user asks about valuation, upside/downside, multiples, DCF, implied expectations, or margin of safety. Read `references/valuation-methods.md` and `templates/valuation-note.md`. When local input data is available, use `scripts/dcf_sensitivity.py`, `scripts/peer_comps_table.py`, or `scripts/implied_expectations.py` as appropriate.

### 5. `thesis_tracking`

Use for ongoing monitoring of a watchlist or holding. Read `templates/thesis-tracker.md` and `references/risk-and-kill-criteria.md`. Focus on thesis pillars, support evidence, bear case, kill criteria, early warning indicators, and next one to two quarter checks.

### 6. `ai_supply_chain_overlay`

Use for AI infrastructure companies or AI narrative stocks. Read `references/ai-infrastructure-stock-framework.md`. Distinguish real revenue benefit from narrative benefit, and identify whether demand comes from training, inference, data center upgrade, inventory replenishment, or speculative ordering.

For AI infrastructure companies, do not treat `data center revenue` as equal to `AI-only revenue`. If the company only discloses data center revenue, state `AI-only revenue 未单独披露 / 需间接验证` and separate disclosed AI revenue, AI-related revenue, data center revenue, management commentary, design wins / backlog / customer programs, and market narrative.

## Local Data Tools

Use the v0.2 tools only when the user or Agent supplies local structured data. Read `scripts/README.md` and the matching file in `schemas/` before execution.

- `scripts/ratio_calculator.py`: calculate financial ratios from local financials CSV.
- `scripts/dcf_sensitivity.py`: calculate simplified DCF scenarios and sensitivity from local assumptions JSON.
- `scripts/peer_comps_table.py`: calculate and summarize peer valuation multiples from local CSV.
- `scripts/implied_expectations.py`: reverse-engineer revenue, earnings, and FCF scale-up requirements from local valuation CSV.

Rules:

- Do not use these scripts to fetch data, read API keys, log in to websites, connect to brokers, or execute trades.
- Validate required fields and units before running a script.
- Cite the input file, source, basis, reporting period, currency, timestamp or source date, market session when applicable, and source status when using script results.
- Treat script output as a reproducible calculation layer, not as verified source data or a final investment conclusion.
- Reconcile calculated results with primary sources and explain any conflicting basis.
- Do not let a script output replace business analysis, bear case, thesis kill criteria, three-veto review, or final research status.

## v0.4 Review-Gated Local Pipeline

Use `pipeline/` only when the user explicitly asks to run or inspect the offline pipeline, sandbox, packet, or audit dashboard. Read `references/v0.4-review-gated-pipeline.md` and `pipeline/README.md` first.

Rules:

- The default user-facing research output remains a complete Markdown equity research report, not a pipeline packet.
- The v0.4 pipeline is an optional local toolchain for local files, fixtures and approved fictional sandbox outputs.
- The pipeline does not automatically fetch data, extract live filings, connect to brokers, trade, or produce buy/sell advice.
- EXMP fictional sandbox may produce normalized CSV and ratio dry-run outputs.
- MRVL, NVDA and AVGO are review-only: no promotion, no normalized CSV, no v0.2.x dry-run and no approved normalized input.
- Draft candidates, review workbenches, quality scores and review-only packets are evidence workflow artifacts, not company facts.
- Pipeline packets are sandbox/review-only summaries, not final investment reports.
- Use the audit dashboard to verify blocked real-company steps before citing any pipeline output.

## v0.5 QA And Public-Readiness Audit

Use `qa/` only when the user asks to validate the local pipeline artifacts, audit public-readiness, or check artifact hygiene.

Rules:

- QA tools only read local repository files and emit local reports.
- `offline_packet_qa.py` checks pipeline manifests, research packets, dashboard references, EXMP sandbox disclaimers, and MRVL/NVDA/AVGO blocked outputs.
- `public_readiness_audit.py` checks whether the repository is suitable for public sharing; default readiness is `No` unless a separate public-readiness approval is performed.
- `artifact_hygiene_checker.py` checks for `.DS_Store`, cache artifacts, raw full filings, local path leaks, and accidental temporary evidence.
- QA output is not a research report and must not include investment conclusions.
- QA does not enable live extraction, production parser claims, real-company promotion, normalized CSV generation, v0.2.x dry-run, broker/trading, or public release.

## v0.6 Controlled Real-Company Sandbox Gate

Use `pipeline/controlled_real_company_sandbox_gate.py` only when the user explicitly asks to inspect or run the controlled real-company sandbox gate. Read `references/v0.6-controlled-real-company-sandbox.md` first.

Rules:

- The gate is off by default.
- A run must explicitly provide `--mode controlled_real_company_sandbox`, `--allow-real-company-sandbox`, `--quarantine-output`, `--review-batch`, `--quality-score`, `--candidate-package`, `--approval-policy`, and a quarantine output path.
- v0.6 tracked example allows only MRVL quarantined sandbox output.
- NVDA and AVGO remain blocked from tracked quarantine output by default.
- Quarantine output must be marked `quarantined`, `not_production_data`, `not_investment_data`, `not_company_fact_until_verified`, `manual_review_required`, `not_for_trading`, `not_for_public_release`, and `no_recommendation`.
- Quarantined ratio dry-run is a calculation smoke test only. Do not use it as company fact, investment data or a final research conclusion.
- Do not run DCF, peer comps or implied expectations from real-company quarantine output.
- Do not produce a full research report, target price, buy/sell/hold, position size or research status from quarantine output.
- Public-readiness remains `No` unless a separate public-readiness approval is performed.

## v1.0 Stable Review-Gated Workflow

Use the v1.0 local workflow only when the user explicitly asks to inspect or run local evidence, parser-readiness, quarantine, report-packet, QA or release-candidate tooling.

Rules:

- v1.0 is a stable review-gated stock research Skill, not a production extraction system.
- Parser-readiness audit defaults to `production_parser_ready: No`.
- Evidence reconciliation must keep draft candidates, reviewed decisions, quarantine outputs, dry-runs and report packets traceable.
- Controlled quarantine output is non-production, non-investment data, not for trading and not for public release.
- Report packets are evidence/review work products, not investment recommendations.
- Do not use report packets to output target price, buy/sell/hold, position size, portfolio action or research status.
- Public-readiness status is `Needs user decision` unless the user separately approves public release after audit.
- The repository should remain private by default.

## v2.0 Production Research System

Use the v2 production system only when the user explicitly asks for production ingestion, production parser, normalized statements, data quality gate, valuation scenarios, evidence-backed research conclusion, production report packet, approval gate, or production pilot.

Rules:

- Controlled live SEC ingestion must use SEC-only HTTPS, GET only, explicit User-Agent, timeout, request count, interval and response-size caps.
- Production XBRL parser reads local filing packages; it must not silently guess values.
- Normalized statements must preserve field-level provenance, units, period, confidence, review status and unresolved fields.
- Data quality failures must be visible and can block valuation, conclusion and publication.
- Research conclusions may use `constructive`, `neutral`, `cautious`, `negative` or `insufficient_evidence`, with evidence basis and confidence.
- Report packets require approval gate before `publishable_research_packet`.
- Do not output personalized financial advice, position sizing, trade instruction, broker order, auto-buy, auto-sell, or guaranteed return.
- Do not read or save API keys, tokens, passwords, secrets or broker credentials.

## Default Output Rules

- Output a complete Markdown equity research report by default.
- Do not default to only an Obsidian company card.
- Treat Obsidian as an optional archive format.
- Directly output `templates/obsidian-company-card.md` only when the user explicitly asks for Obsidian format, an Obsidian card, or an Obsidian-ready company note.
- If the user did not ask for Obsidian but the report is suitable for archiving, end the report by asking whether they want an additional Obsidian company card.
- Each formal research output should include this disclaimer once, at the beginning or end: `本文仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。`
- Do not repeat the disclaimer in every section.
- Do not use the disclaimer as a reason to avoid clear research judgment; make clear judgments while separating facts, inferences, assumptions, and opinions.

## Required Source Hierarchy

Use `references/source-registry.md` as the source hierarchy.

- Prefer primary sources: company filings, annual reports, quarterly reports, 10-K, 10-Q, 20-F, 8-K, investor relations materials, earnings call transcripts, exchange announcements, and regulatory filings.
- Use secondary sources for cross-checking: SEC EDGAR, company website, exchange websites, annual report databases, financial data terminals, and authoritative financial media.
- Treat tertiary sources as leads only: blogs, social media, forums, and secondary commentary articles.

All key financial numbers and market data must include source, period or retrieval time, currency, accounting basis or market-data basis, timestamp when applicable, market session when applicable, and whether the number is company-disclosed, estimated, real-time, delayed, or unverified.

## Anti-Hallucination Rules

- Do not fabricate prices, market cap, revenue, margins, valuation multiples, consensus estimates, guidance, or news.
- Do not infer the latest reporting period without a source. If unavailable, say so.
- Do not give a high-confidence conclusion when the evidence base is incomplete.
- Mark unverifiable information as `未验证信息`.
- Distinguish `公司披露`, `市场预期`, `第三方估算`, and `个人推断`.
- Separate `事实`, `推断`, `假设`, and `观点` in conclusions.
- Do not leave unknown fields blank. Use `未披露`, `未验证`, `暂无可靠来源`, `不适用`, or `待核实`.
- Add every key unknown or unverified issue to `Next Checks`.
- For high-valuation growth stocks, reverse-engineer market-implied expectations when sufficient valuation and operating data are available; if not available, state what data is missing.
- For cyclical stocks, separate peak earnings from normalized earnings and avoid extrapolating cycle-top profitability.
- For AI supply chain companies, distinguish real AI revenue exposure from narrative-driven multiple expansion. Data center growth alone is not sufficient to conclude that AI benefit is fully verified; verify whether AI-only revenue, AI-related revenue, orders, backlog, design wins, customer programs, or management commentary support the claim.
- If evidence conflicts, show the conflict and prioritize primary sources.
- Do not treat a calculated output as an independently verified fact. Label it as `基于所列输入的计算结果` and preserve the input limitations.

## Three-Veto Rules

Before outputting any final status, check the three vetoes in `scoring/three-veto-nine-score.md`:

1. 商业模式不可理解或收入真实性无法验证。
2. 财务质量明显恶化且无法解释。
3. 估值严重依赖不可验证的远期叙事。

If any veto is triggered, the final status can only be:

- 排除
- 数据不足，暂不判断
- 观察池，但必须明确说明重大风险和待核实事项。

The nine-score framework is not mandatory for every output. It is mandatory only for:

- `company_deep_dive`
- Candidate decisions (`候选` or promotion into candidate review)
- Holding reviews (`持仓复核`)
- Multi-company comparisons
- Explicit user requests for scoring

## Output Requirements

Every research output must include:

- Research identity block: ticker, exchange, reporting currency, latest reporting period, objective, and horizon.
- Source quality note: what was sourced, what was estimated, and what remains unverified.
- Business model and revenue structure.
- Financial quality review appropriate to the requested depth.
- Valuation review appropriate to the requested depth.
- Bull case and bear case.
- Thesis kill criteria.
- Key risks and early warning indicators.
- Next checks.
- Final status using only the allowed labels below.

Allowed final status labels are defined in `references/status-taxonomy.md`:

- 排除
- 观察池
- 候选
- 深入研究
- 小仓位跟踪
- 持仓复核
- 等待更好价格
- 数据不足，暂不判断

All final statuses are research workflow states, not trading instructions, buy/sell recommendations, or position-size advice. `小仓位跟踪` means the name has continuing observation and small-scale research validation value; it does not recommend that any user buy, initiate, or allocate a specific position size.

## v3.0 Production Research System

Use `production/` when the user explicitly asks for the live production research workflow, source registry, market data adapter, production CLI, audit trail, or a full production research packet.

Primary entrypoints:

- `production/cli.py research --ticker <TICKER> --mode fixture`
- `production/cli.py research --ticker <TICKER> --mode live --sec-only`
- `production/cli.py validate --run-dir <RUN_DIR>`

Production workflow rules:

- Live SEC ingestion must remain controlled, bounded, allowlisted, and source-manifested.
- Market data should prefer user-provided CSV; unavailable or unreliable market data must produce an `insufficient_market_data` caveat.
- Every production report draft must preserve source manifest, data-quality report, valuation assumptions, research conclusion, and workflow audit.
- Research conclusions may use `Constructive`, `Neutral`, `Cautious`, `Negative`, or `Insufficient evidence` with `High / Medium / Low` confidence.
- Fair value ranges are scenario outputs, not trading instructions.
- Approval and audit gates are required before anything is treated as a publishable research packet.
- Do not connect to brokers, route orders, execute trades, read credentials, store secrets, output personalized advice, or recommend position sizing.

## Risk And Compliance Boundaries

- Use one concise disclaimer per formal output: `本文仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。`
- Do not claim certainty about future returns.
- Do not generate automatic trading, order-execution instructions, API-key workflows, brokerage integrations, or credential storage.
- Do not present a valuation range as a guaranteed target price.
- When data is stale or missing, explicitly state the limitation and avoid overconfident language.

## Final Answer Format

For normal research tasks, use this structure:

1. `研究对象与范围`
2. `一句话结论`
3. `事实 / 推断 / 假设 / 观点`
4. `业务与行业`
5. `财务质量`
6. `估值与隐含预期`
7. `Bull Case / Bear Case`
8. `Thesis Kill Criteria`
9. `关键风险与早期信号`
10. `Next Checks`
11. `来源与缺口`
12. `最终研究状态`
13. `是否需要追加 Obsidian 卡片`

For file-generation tasks, use the relevant template in `templates/` and keep the final chat response short: changed files, validation performed, and any missing inputs.
