# Synthetic Edge-Case Fixtures

These files are short artificial fixtures for v0.3.6 regression tests. They are not real filings and contain no authoritative company financial data.

Covered cases:

- taxonomy drift
- extension tag without anchor
- extension tag with weak relationship
- debt component overlap
- capex ambiguity
- cash plus restricted cash confusion
- diluted shares wrong period / duration
- duration vs instant mismatch
- mixed units
- restatement / amended filing conflict
- candidate value material change threshold warning
- dimension-only revenue

All edge-case expectations live in `expected_results.json`.
