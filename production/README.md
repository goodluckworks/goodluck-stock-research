# Production Research System

`production/` contains the v2 production research system layer.

The system supports controlled official SEC ingestion, scoped production XBRL parsing, normalized financial statements, data quality gates, valuation scenarios, evidence-backed research conclusions, report drafts and human approval gates.

It does not connect to brokers, place orders, execute trades, read credential secrets, provide personalized financial advice or generate position sizing.

## Publication States

- `draft_unreviewed`
- `reviewed_internal`
- `approved_internal`
- `publishable_research_packet`
- `blocked`

## v2.0 Stable Scope

v2.0 supports controlled live SEC ingestion, scoped production XBRL parser MVP, normalized financial statements, data quality gate, valuation scenarios, evidence-backed research conclusion, approval-gated report packets and MRVL production pilot.

It remains a research system. It does not connect to brokers, execute trades, route orders, read secrets, provide personalized financial advice, output position sizing or create trade instructions.

## v3.0 Live Production Scope

v3.0 adds the usable production workflow layer:

- `sources/`: live source registry, SEC source, company IR source, market data CSV / controlled source fallback, source cache and manifests.
- `history/`: multi-filing annual and quarterly financial history, period alignment and historical metrics.
- `xbrl_parser/parser_hardening.py`: real-filing hardening checks for dimensions, contexts, units, capex sign, debt, cash, shares, extensions and amendments.
- `comps/`: user-provided peer set, market multiples and comps auditor.
- `valuation/`: DCF, multiples valuation, implied expectations, sensitivity and valuation auditor.
- `workflows/`: real-company research workflow, manifest and workflow auditor.
- `cli.py`: user-facing `research` and `validate` commands.
- `reliability/`: cache, retry, error taxonomy, source monitor and run recovery.
- `audit/`: accuracy audit, source quality audit and final red-team.

Typical commands:

```bash
python3 goodluck-stock-research/production/cli.py research --ticker MRVL --mode fixture
python3 goodluck-stock-research/production/cli.py validate --run-dir goodluck-stock-research/examples/production_research/MRVL
```

Inspect `source_manifest.json`, `data_quality_report.md`, `valuation_scenarios.json`, `research_conclusion.json` and `workflow_audit_report.md` before relying on any draft.

v3.0 still does not connect to brokers, place orders, execute trades, route orders, read or store secrets, provide personalized financial advice, output position sizing or create trade instructions.

## v3.0.1 Usability Smoke

v3.0.1 adds production usability smoke checks for daily internal use. The goal is to verify that a user can run the CLI, understand the output paths, inspect caveats, use a market-data CSV fallback and confirm safety boundaries before relying on a draft.

Example smoke commands:

```bash
python3 goodluck-stock-research/production/cli.py --help
python3 goodluck-stock-research/production/cli.py research --ticker MRVL --mode fixture --output-dir /private/tmp/stock-research-v301-fixture/MRVL
python3 goodluck-stock-research/production/cli.py validate --run-dir goodluck-stock-research/examples/production_research/MRVL
python3 goodluck-stock-research/production/usability/tests/run_cli_usability_tests.py
```

Controlled live SEC smoke remains explicit and bounded:

```bash
python3 goodluck-stock-research/production/ingestion/sec_live_ingestor.py \
  --mode live_mode_explicit_url \
  --source-url "https://www.sec.gov/cgi-bin/browse-edgar?CIK=MRVL&owner=exclude&action=getcompany" \
  --user-agent "goodluck-stock-research smoke-test research@example.com" \
  --output-dir /private/tmp/stock-research-v301-live/MRVL
```

Raw live output should stay in `/private/tmp` or another non-repo scratch path unless a human explicitly reviews and decides otherwise.
