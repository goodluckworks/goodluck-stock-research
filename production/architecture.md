# v2 Production Architecture

## Pipeline

```text
official filing live ingestion
  -> filing identity and amendment discovery
  -> production XBRL parsing
  -> normalized financial statement generation
  -> data quality and reconciliation checks
  -> valuation and scenario analysis
  -> research conclusion
  -> report generation
  -> human approval gate
  -> publishable research packet
```

## Boundaries

- SEC official sources only for live filing ingestion.
- Live ingestion must use explicit URL, explicit User-Agent, bounded timeout, request count, interval and response size.
- Parser reads local filing packages only.
- Research conclusions are evidence-backed views, not trading instructions.
- Publication requires human approval.
