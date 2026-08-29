# XBRL-like Fixtures

These short HTML files are artificial test fixtures. Values in files named
MRVL, NVDA or AVGO are synthetic and must not be treated as company disclosure.

Supported fixture shapes:

## 1. `data_attr`

```html
<span
  data-xbrl-concept="us-gaap:ExampleConcept"
  data-xbrl-context="FY2026"
  data-xbrl-period-type="duration"
  data-xbrl-period="FY2026"
  data-xbrl-unit="USD"
  data-xbrl-dimensions=""
  data-xbrl-statement="income_statement"
  data-xbrl-locator="fixture line identifier"
>-100</span>
```

Optional `data-xbrl-split-adjusted="true"` is used by the diluted-shares
fixture. Dimensions are pipe-separated.

## 2. `inline_like`

The inline-like subset is still artificial and local-only. It uses short
`ix-nonFraction` elements plus local context/unit declarations:

```html
<xbrli-context id="FY2026" data-xbrl-period-type="duration"
  data-xbrl-period="FY2026" data-xbrl-dimensions=""></xbrli-context>
<xbrli-unit id="USD" measure="USD"></xbrli-unit>
<ix-nonFraction name="us-gaap:ExampleConcept" contextRef="FY2026"
  unitRef="USD" decimals="-6" scale="6"
  data-xbrl-statement="income_statement"
  data-xbrl-locator="fixture line identifier">100</ix-nonFraction>
```

## 3. `instance_xml`

The minimal instance XML subset supports only artificial `<context>`, `<unit>`
and `<fact>` elements in `exmp_instance_document.xml`. It does not load
taxonomy URLs, schemas, linkbases, labels, continuations or footnotes.

## Boundary

- Fixture-only.
- Not production iXBRL.
- Not real filing extraction.
- Not authoritative financial data.
- External URLs inside inline-like or instance XML fixtures are rejected.

## v0.3.6 Edge Cases

`fixtures/edge_cases/` contains short synthetic fixtures and `expected_results.json` for:

- taxonomy drift
- extension tag without anchor
- extension tag with weak relationship
- restatement conflict
- complex debt double count
- capex scope ambiguity
- restricted cash confusion
- diluted shares wrong duration
- duration versus instant mismatch
- mixed units
- material change threshold warning
- dimension-only revenue

These fixtures are intentionally tiny and artificial. They exist to test unresolved behavior,
warning flags, provenance preservation and review-gate safety; they are not excerpts of complete
real filings.

## v0.3.7 Real-Filing-Excerpt Drills

`fixtures/real_excerpt_drills/` contains short, manually reduced excerpt-like local fixtures for
MRVL, NVDA and AVGO review drills. They are intended to test reviewer ergonomics, taxonomy
relationship metadata, quality scoring and draft-only promotion isolation against real-company-shaped
filing snippets.

Boundaries:

- Excerpt only; not complete filings.
- Not authoritative company or SEC data.
- No live extraction and no production parser claim.
- No approved normalized input or v0.2.x populated CSV.
- MRVL, NVDA and AVGO remain draft-only and cannot be promoted.
