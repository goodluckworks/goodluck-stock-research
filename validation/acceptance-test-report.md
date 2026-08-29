# Stock Research Skill v0.1 Acceptance Test Report

## 1. Scope

This report validates the current `goodluck-stock-research/` v0.1 as a document-only equity research Skill. The validation did not use network access, real company financial data, EDGAR/yfinance/OpenBB scripts, API keys, brokerage credentials, automatic trading, or order execution.

The goal is to verify that the Skill is usable, stable, internally consistent, and resistant to data fabrication or over-direct investment advice.

## 2. Static Checks

| Check Item | Result | Notes |
|---|---:|---|
| `SKILL.md` YAML front matter is valid | Pass | Parsed with local Ruby YAML parser. `name` is `stock-research`; `description` is present. |
| `SKILL.md` description includes English and Chinese triggers | Pass | Includes `analyze a stock`, `public company`, `earnings result`, `valuation`, `investment thesis`, plus `股票分析`, `公司研究`, `财报更新`, `估值分析`, `投资逻辑`, `观察池`, `持仓复核`, `AI 产业链公司分析`. |
| No default-only Obsidian behavior | Pass | `SKILL.md`, `README.md`, `research-workflow.md`, and `obsidian-company-card.md` state that default output is a full research report and Obsidian is optional. |
| `status-taxonomy.md` defines all 8 statuses | Pass | Defines `排除`, `观察池`, `候选`, `深入研究`, `小仓位跟踪`, `持仓复核`, `等待更好价格`, `数据不足，暂不判断`. |
| Template status labels match `status-taxonomy.md` | Pass | Quick tearsheet, company deep dive, earnings update, thesis tracker, and scoring template use the same status labels. |
| All templates include no-empty-field rule | Pass | All six templates and scoring output template include `不允许留空字段`. |
| Market data fields require source, timestamp, market session, currency, and trailing/forward basis | Pass after fix | Strengthened top rules across templates and scoring output; tightened quick tearsheet and valuation note fields. |
| Empty files | Pass | No zero-byte files found. |
| Files with only headings and no content | Pass | No file is only headings; templates contain fillable fields plus rules and sections. |
| Obvious unresolved placeholders | Pass | No unresolved placeholder markers found. Fillable template blanks are intentional and governed by no-empty-output rules. |
| API keys, secrets, brokerage login, auto-trading, order execution | Pass | Mentions are prohibitive only; no API key, credential, broker login, script, or trading execution feature exists. |
| Disclaimer behavior | Pass | Rules require one concise disclaimer at the beginning or end of formal research output and explicitly forbid repeating it in every section. |

## 3. Test Cases

### Test Case 1: 中文快速股票分析请求

- Simulated user request:
  - “帮我快速分析一下 MRVL 这家公司，看看是否值得进入观察池。”
- Expected behavior:
  - Trigger `stock-research`.
  - Default to a complete quick tearsheet or short research report.
  - Do not default to an Obsidian card.
  - Do not fabricate revenue, profit, market cap, valuation multiples, or news.
  - Mark missing inputs as `未验证`, `待核实`, or `暂无可靠来源`.
  - Include bear case, next checks, and three-veto check before final status.
  - If data is insufficient, final status should lean `数据不足，暂不判断` or `观察池` with explicit verification items.
- Actual observed behavior from skill files:
  - `SKILL.md` Chinese trigger terms include `股票分析` and `观察池`.
  - `SKILL.md` default workflow requires source planning, unknown-field labels, bear case, thesis kill criteria, three-veto check, and full Markdown report output by default.
  - `templates/quick-tearsheet.md` requires no blank fields, market data source/timestamp/session/currency, bear and bull sections, thesis kill criteria, next checks, and full status labels.
  - Anti-hallucination rules prohibit fabricated price, market cap, revenue, margins, valuation multiples, estimates, guidance, and news.
- Pass / Fail:
  - Pass.
- Issues found:
  - Quick tearsheet market data fields initially did not explicitly include all required currency/session/basis details in every field.
- Fixes applied:
  - Strengthened quick tearsheet market data fields to require source, timestamp, market session, currency, calculation basis, and trailing/forward/TTM/NTM basis where applicable.

### Test Case 2: Explicit Obsidian Output

- Simulated user request:
  - “请把这家公司输出成 Obsidian 公司卡片格式。”
- Expected behavior:
  - Allow direct Obsidian YAML + Markdown card output.
  - YAML includes `ticker`, `company`, `exchange`, `sector`, `industry`, `currency`, `latest_reporting_period`, `data_date`, `source_status`, `status`, `research_stage`, `confidence`, `score_total`, `veto_triggered`, `watchlist_reason`, `last_updated`, `next_check`, `thesis_review_due`, `aliases`, `related`, and `tags`.
  - `tags`, `aliases`, and `related` use array format.
  - `status` comes from `status-taxonomy.md`.
  - Unknown fields are not blank and use `未验证`, `未披露`, `不适用`, or `待核实`.
- Actual observed behavior from skill files:
  - `templates/obsidian-company-card.md` includes all required YAML fields.
  - `aliases`, `related`, and `tags` are initialized as arrays.
  - Template rules require `status` from `references/status-taxonomy.md`.
  - Template rules forbid blank fields and require unknown values to be explicit.
  - `SKILL.md` says Obsidian is direct output only when explicitly requested.
- Pass / Fail:
  - Pass.
- Issues found:
  - None after prior v0.1 iteration.
- Fixes applied:
  - None in this pass.

### Test Case 3: AI Infrastructure Stock Overlay

- Simulated user request:
  - “帮我分析一家 AI 光互联公司，重点看它是真实受益还是只是 AI 叙事受益。”
- Expected behavior:
  - Use or cite `ai-infrastructure-stock-framework.md`.
  - Distinguish real revenue benefit, order/backlog support, customer concentration, hyperscaler capex sustainability, narrative benefit, and valuation-implied expectations.
  - Require market-implied expectation reverse-engineering.
  - Include technology substitution risk, competition risk, and gross margin compression risk.
  - Do not give a positive conclusion just because the company has an AI narrative.
- Actual observed behavior from skill files:
  - `SKILL.md` defines `ai_supply_chain_overlay` and requires distinguishing real AI revenue exposure from narrative-driven multiple expansion.
  - `references/ai-infrastructure-stock-framework.md` includes AI revenue verification levels, demand-source decomposition, customer concentration, hyperscaler capex sustainability, competition/substitution risk, gross margin pressure, inventory rebuild risk, and valuation overlay.
  - Anti-hallucination rules require market-implied expectation reverse-engineering for high-valuation growth stocks and prohibit using unverified narratives as core conclusions.
- Pass / Fail:
  - Pass.
- Issues found:
  - None.
- Fixes applied:
  - None.

### Test Case 4: Portfolio Review

- Simulated user request:
  - “我已经持有这只股票，请帮我做一次持仓复核。”
- Expected behavior:
  - Output a complete holding-review research report, not buy/sell advice.
  - Force three-veto check.
  - Force nine-score framework.
  - Include original thesis validity, thesis pillars, bear case, kill criteria, early warning indicators, next 1-2 quarter checks, and final research workflow status.
  - If using `小仓位跟踪` or `持仓复核`, clearly state these are research workflow states, not position-size or trading advice.
- Actual observed behavior from skill files:
  - `SKILL.md` makes holding reviews (`持仓复核`) a mandatory nine-score scenario and requires three-veto check before final status.
  - `references/status-taxonomy.md` defines `持仓复核` as a research review state, not a hold/buy/sell recommendation.
  - `references/status-taxonomy.md` defines `小仓位跟踪` as a research workflow state and explicitly says it is not a position-size recommendation.
  - `templates/thesis-tracker.md` requires three-veto check, nine-score if holding review, thesis pillars, bear case, kill criteria, early warning indicators, and next checks.
  - `references/risk-and-kill-criteria.md` requires thesis pillars, bear case, top risks, kill criteria, early warning indicators, and next 1-2 quarter checks.
- Pass / Fail:
  - Pass.
- Issues found:
  - None.
- Fixes applied:
  - None.

## 4. Issues Fixed

- Tightened `templates/quick-tearsheet.md` market data fields so current price, market cap, EV, and valuation multiples explicitly require source, timestamp, market session, currency, calculation basis, and trailing/forward/TTM/NTM basis where applicable.
- Tightened market-data rules across all templates and scoring output template to include currency and trailing/forward/TTM/NTM basis, not only source/timestamp/session.
- Added missing currency requirement to the `Enterprise value / EV` field in `templates/valuation-note.md`.

## 5. Remaining Risks

- The Skill is document-only and cannot verify live market data without user-provided sources or a future data integration.
- Fillable template cells remain blank by design; output rules require the agent to fill unknowns with explicit markers rather than leave final outputs blank.
- The Skill can guide research discipline, but final quality still depends on whether the user or agent supplies reliable filings, transcripts, market data, and timestamps.
- Official `quick_validate.py` may require an environment with `PyYAML`; local YAML validation was performed with Ruby instead.

## 6. Recommendation

- Ready for v0.1 use: Yes
- Suggested next step: Commit this v0.1 document-only Skill after review. Do not add API, EDGAR/yfinance/OpenBB scripts, or trading features in the v0.1 commit.
