# Parser Readiness

This folder contains local-only parser-readiness and evidence-reconciliation audits.

The tools do not fetch data, call live APIs, read credentials, use browser automation, or claim production XBRL parsing. They inspect tracked fixtures and manifests to decide whether the repository is ready for a separate production parser effort.

Default result: `production_parser_ready: No`.
