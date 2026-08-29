# Stock Research Skill QA Tools

This directory contains local-only QA tools for the review-gated offline research pipeline.

The tools read tracked repository artifacts and emit structured Markdown/JSON review results. They do not fetch data, call live APIs, read credentials, access broker systems, or produce investment conclusions.

## Tools

- `offline_packet_qa.py`: checks pipeline run manifests, research packet manifests, packet Markdown boundaries, dashboard coverage, and real-company blocked paths.
- `public_readiness_audit.py`: checks whether the repository is suitable for public sharing. The default v0.5/v0.6 result is `ready_for_public_release: No` unless explicit approval is provided separately.
- `artifact_hygiene_checker.py`: checks tracked artifacts for local path leaks, raw filing files, cache files, `.DS_Store`, and accidental generated artifacts.

## Example Commands

```bash
python3 goodluck-stock-research/qa/offline_packet_qa.py \
  --repo-root . \
  --output goodluck-stock-research/validation/offline_packet_qa_report.md
```

```bash
python3 goodluck-stock-research/qa/public_readiness_audit.py \
  --repo-root . \
  --repository-visibility PRIVATE \
  --output goodluck-stock-research/validation/public_readiness_audit_report.md
```

```bash
python3 goodluck-stock-research/qa/artifact_hygiene_checker.py \
  --repo-root . \
  --output goodluck-stock-research/validation/artifact_hygiene_report.md
```

## Boundaries

- Local files only.
- No live extraction.
- No production parser claims.
- No investment advice, target price, buy/sell/hold, position size, broker, order, or trading output.
- `/private/tmp` is allowed in validation command logs and intentionally temporary paths.
- `/Users/...` paths are not allowed in tracked generated artifacts.
