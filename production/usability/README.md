# Production Usability Smoke

v3.0.1 usability tools validate whether the production research workflow is understandable and runnable.

They check CLI help, example commands, fixture workflow output, market-data CSV fallback, report readability, evidence chain, caveats and safety boundaries.

They do not connect to brokers, execute trades, route orders, read secrets or produce personalized financial advice.

## Commands

Run the CLI usability checks:

```bash
python3 goodluck-stock-research/production/usability/tests/run_cli_usability_tests.py
python3 goodluck-stock-research/production/usability/tests/run_command_examples_tests.py
python3 goodluck-stock-research/production/usability/tests/run_report_usability_tests.py
```

Run a fixture research smoke:

```bash
python3 goodluck-stock-research/production/cli.py research \
  --ticker MRVL \
  --mode fixture \
  --output-dir /private/tmp/stock-research-v301-fixture/MRVL
```

Run a controlled SEC live smoke only with an explicit SEC URL and User-Agent:

```bash
python3 goodluck-stock-research/production/ingestion/sec_live_ingestor.py \
  --mode live_mode_explicit_url \
  --source-url "https://www.sec.gov/cgi-bin/browse-edgar?CIK=MRVL&owner=exclude&action=getcompany" \
  --user-agent "goodluck-stock-research smoke-test research@example.com" \
  --output-dir /private/tmp/stock-research-v301-live/MRVL
```

## Expected Output

Fixture and live smoke output should make these fields easy to find:

- report path
- audit path
- data quality status
- conclusion label
- caveats
- source manifest
- no broker action / no trade instruction / no position sizing boundary

Live raw SEC output belongs in `/private/tmp` or another scratch location, not in the repository.
