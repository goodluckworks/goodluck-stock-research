# Production Source Policy

## Supported Sources

- SEC official filing URLs and company submission metadata.
- Company official investor relations documents when manually provided.
- Local filing packages and fixtures.

## Unsupported Sources

- Broker data.
- Paid market-data vendors unless separately approved.
- Social media as a primary financial source.
- Unsourced numeric data.

## SEC Request Policy

- SEC-only HTTPS domains.
- GET only.
- Explicit User-Agent required.
- Timeout required.
- Maximum request count required.
- Minimum request interval required.
- Maximum response size required.
- Bounded retry behavior only.
- No bulk crawl.

## Retention

Raw live filings should be written to `/private/tmp` unless explicitly approved for tracked fixture use. Tracked repository artifacts must store manifests, checksums, provenance and short fixtures, not full raw filings.
