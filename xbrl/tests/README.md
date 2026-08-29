# v0.3.7 XBRL Prototype Tests

Run from the repository root:

```bash
for test in goodluck-stock-research/xbrl/tests/run_*_tests.py; do
  python3 "$test"
done
```

The tests use only local artificial fixtures and temporary directories. They do
not access SEC URLs, approve real-company fields or invoke v0.2.x scripts.

Coverage includes candidate extraction, schema validation, mapping relationship review,
reviewer workbench ergonomics, review checklist validation, review quality scoring, real-excerpt
drills and promotion isolation.
