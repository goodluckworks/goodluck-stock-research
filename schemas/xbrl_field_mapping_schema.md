# XBRL Field Mapping Schema

## 1. Purpose

This schema defines versioned records for mapping XBRL concepts to the first nine supported
normalized financial fields. v0.3.4 implements a `prototype_fixture_only` registry using this
shape, and v0.3.5 adds machine-readable validation under `xbrl/schemas/`. The registry does not
authorize production extraction, select a value by first match or populate a v0.2.x CSV / JSON.
v0.3.6 adds a separate mapping review workflow: promotion may use a mapping version only when a
matching mapping review batch is `approved` and not `superseded` or `rejected`.
v0.3.7 adds required taxonomy relationship metadata to every mapping record and requires mapping
review to explicitly assess relationship evidence.

## 2. Mapping Record Fields

Document-level fields:

| Field | Required | Meaning |
|---|---:|---|
| `mapping_version` | Yes | Immutable mapping release |
| `taxonomy_family` | Yes | Initial value: `us-gaap` |
| `taxonomy_versions` | Yes | Explicit supported taxonomy years |
| `supported_forms` | Yes | Initial values: `10-K`, `10-Q` |
| `created_at` | Yes | Timezone-aware timestamp |
| `review_status` | Yes | `draft`, `reviewed`, `approved`, `superseded` |
| `records` | Yes | Array of mapping records |

Each mapping record:

| Field | Required | Meaning |
|---|---:|---|
| `mapping_id` | Yes | Stable unique ID |
| `normalized_field` | Yes | One supported v0.2.x field |
| `statement` | Yes | `income_statement`, `balance_sheet`, `cash_flow`, `eps_note` |
| `preferred_tags` | Yes | Ordered standard concept QNames; may be empty only with rationale |
| `fallback_tags` | Yes | Reviewed alternatives; empty array allowed |
| `extension_tag_allowed` | Yes | Boolean |
| `extension_requirements` | Yes | Required relationships/context evidence or `not_allowed` |
| `period_type` | Yes | `duration` or `instant` |
| `balance_type` | Yes | `debit`, `credit`, or `not_applicable` |
| `expected_unit` | Yes | Currency, shares or other exact unit rule |
| `allowed_dimensions` | Yes | Usually empty for consolidated fields |
| `sign_convention` | Yes | Source and normalized sign rule |
| `scale` | Yes | Target amount/share unit and conversion rule |
| `aggregation_rule` | Yes | `identity`, reviewed non-overlapping sum, or explicit prohibition |
| `required` | Yes | Boolean for prototype completeness |
| `candidate_selection_rules` | Yes | Ordered context and reconciliation rules |
| `confidence_rules` | Yes | High/medium/low criteria |
| `ambiguity_behavior` | Yes | Must resolve to `unresolved` when material ambiguity remains |
| `review_required` | Yes | Must be true |
| `relationship_metadata` | Yes | Concept label/type, taxonomy namespace/version, closest standard concept, presentation/calculation relationship, anchor, confidence, review status and evidence notes |
| `notes` | Yes | Field-specific limitations |

Mapping records may name candidate concepts, but implementation must validate them against the
filing taxonomy version and context. A tag list is never a promise that the first available fact is
correct.

`relationship_metadata` is review evidence, not a production taxonomy parser. Unsupported or
unreviewed relationships must block mapping approval and downstream promotion. Real-company
relationship approval requires a separate future taxonomy-year review.

v0.3.5 validation is still fixture-oriented. Passing `mapping_registry_schema.json` means the local
registry has the expected audit shape; it does not mean the mapping is approved for arbitrary SEC
filings or production iXBRL extraction.

## 3. Example Mapping Records

The following are design examples. Exact QNames and taxonomy versions require mapping review before
prototype use.

### Revenue

```yaml
mapping_id: revenue-us-gaap-draft
normalized_field: revenue
statement: income_statement
preferred_tags:
  - us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax
fallback_tags:
  - us-gaap:SalesRevenueNet
extension_tag_allowed: true
extension_requirements:
  - reviewed presentation or calculation relationship to a revenue concept
  - consolidated no-dimension context
period_type: duration
balance_type: credit
expected_unit: reporting_currency
allowed_dimensions: []
sign_convention: preserve source sign; normalized revenue expected nonnegative
scale: convert explicitly to amount_unit
aggregation_rule: identity
required: true
candidate_selection_rules:
  - exact requested duration
  - consolidated legal entity
  - no segment/customer/geography dimension
confidence_rules:
  high: standard tag, exact context and rendered-statement reconciliation
  medium: reviewed extension or fallback with exact context
  low: competing concepts or incomplete reconciliation
ambiguity_behavior: unresolved
review_required: true
notes: Do not substitute segment or AI-related revenue.
```

### Net income

```yaml
mapping_id: net-income-us-gaap-draft
normalized_field: net_income
statement: income_statement
preferred_tags:
  - us-gaap:NetIncomeLoss
fallback_tags:
  - us-gaap:ProfitLoss
extension_tag_allowed: true
extension_requirements:
  - attributable-basis review
period_type: duration
balance_type: credit
expected_unit: reporting_currency
allowed_dimensions: []
sign_convention: preserve profit/loss sign
scale: convert explicitly to amount_unit
aggregation_rule: identity
required: true
candidate_selection_rules:
  - exact duration
  - determine parent versus consolidated attribution
confidence_rules:
  high: exact basis and no competing attributable concept
  medium: exact context but attribution requires note confirmation
  low: attribution or noncontrolling-interest ambiguity
ambiguity_behavior: unresolved
review_required: true
notes: Losses remain negative; never normalize special items automatically.
```

### Operating cash flow

```yaml
mapping_id: operating-cash-flow-us-gaap-draft
normalized_field: operating_cash_flow
statement: cash_flow
preferred_tags:
  - us-gaap:NetCashProvidedByUsedInOperatingActivities
fallback_tags: []
extension_tag_allowed: false
extension_requirements: not_allowed
period_type: duration
balance_type: not_applicable
expected_unit: reporting_currency
allowed_dimensions: []
sign_convention: preserve source sign
scale: convert explicitly to amount_unit
aggregation_rule: identity
required: true
candidate_selection_rules:
  - exact duration
  - cash flow statement total
confidence_rules:
  high: standard concept and exact statement reconciliation
  medium: exact context with presentation review pending
  low: competing duration or dimensional fact
ambiguity_behavior: unresolved
review_required: true
notes: Do not substitute individual working-capital components.
```

### Capital expenditure

```yaml
mapping_id: capital-expenditure-us-gaap-draft
normalized_field: capital_expenditure
statement: cash_flow
preferred_tags:
  - us-gaap:PaymentsToAcquirePropertyPlantAndEquipment
fallback_tags: []
extension_tag_allowed: true
extension_requirements:
  - reviewed PP&E acquisition/payment meaning
  - exclude business combinations and unrelated investing cash flows
period_type: duration
balance_type: not_applicable
expected_unit: reporting_currency
allowed_dimensions: []
sign_convention: preserve extracted sign; normalized value is positive outflow magnitude
scale: explicit amount_unit conversion followed by recorded absolute_value transformation
aggregation_rule: identity; no automatic sum of unrelated investing concepts
required: true
candidate_selection_rules:
  - exact duration
  - reviewed investing cash flow or PP&E note location
confidence_rules:
  high: standard concept and rendered cash-flow reconciliation
  medium: reviewed extension with exact context
  low: capitalized software or acquisition-scope ambiguity
ambiguity_behavior: unresolved
review_required: true
notes: Current v0.2.x FCF subtracts positive capex.
```

### Cash and equivalents

```yaml
mapping_id: cash-and-equivalents-us-gaap-draft
normalized_field: cash_and_equivalents
statement: balance_sheet
preferred_tags:
  - us-gaap:CashAndCashEquivalentsAtCarryingValue
fallback_tags: []
extension_tag_allowed: true
extension_requirements:
  - explicit cash-only basis
period_type: instant
balance_type: debit
expected_unit: reporting_currency
allowed_dimensions: []
sign_convention: preserve source sign
scale: convert explicitly to amount_unit
aggregation_rule: identity
required: true
candidate_selection_rules:
  - exact period end
  - consolidated context
confidence_rules:
  high: standard cash-only concept and balance-sheet reconciliation
  medium: reviewed extension with confirmed basis
  low: includes restricted cash or investments
ambiguity_behavior: unresolved
review_required: true
notes: Do not silently include short-term investments or restricted cash.
```

### Total debt

```yaml
mapping_id: total-debt-us-gaap-draft
normalized_field: total_debt
statement: balance_sheet
preferred_tags:
  - us-gaap:LongTermDebtAndFinanceLeaseObligationsCurrent
  - us-gaap:LongTermDebtAndFinanceLeaseObligationsNoncurrent
fallback_tags:
  - us-gaap:LongTermDebtCurrent
  - us-gaap:LongTermDebtNoncurrent
extension_tag_allowed: true
extension_requirements:
  - reviewed debt note relationship
  - component overlap analysis
period_type: instant
balance_type: credit
expected_unit: reporting_currency
allowed_dimensions: []
sign_convention: preserve source sign; normalized debt expected nonnegative
scale: convert each reviewed component explicitly before sum
aggregation_rule: prefer reviewed total; otherwise sum non-overlapping current and noncurrent components only
required: true
candidate_selection_rules:
  - prefer one reviewed total when available
  - otherwise sum non-overlapping current and noncurrent components
  - never combine a total with its components
confidence_rules:
  high: reconciled total or complete non-overlapping components
  medium: debt-note components with minor classification uncertainty
  low: overlap, lease or commercial-paper ambiguity
ambiguity_behavior: unresolved
review_required: true
notes: Exact debt scope is an open design decision.
```

### Diluted shares

```yaml
mapping_id: diluted-shares-us-gaap-draft
normalized_field: diluted_shares
statement: eps_note
preferred_tags:
  - us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding
fallback_tags: []
extension_tag_allowed: false
extension_requirements: not_allowed
period_type: duration
balance_type: not_applicable
expected_unit: shares
allowed_dimensions: []
sign_convention: preserve source sign
scale: convert explicitly to million shares when required
aggregation_rule: identity
required: true
candidate_selection_rules:
  - exact requested duration
  - company-restated split basis
  - diluted weighted-average, not ending shares
confidence_rules:
  high: standard tag, exact duration and EPS reconciliation
  medium: exact context with split review pending
  low: pre/post-split or duration ambiguity
ambiguity_behavior: unresolved
review_required: true
notes: Do not use common shares outstanding at period end.
```

`gross_profit` and `operating_income` follow the same record structure. A prototype mapping review
must approve their exact preferred/fallback concepts before implementation; if gross profit is not
explicitly reported, it remains unresolved.

## 4. Ambiguity Rules

- Do not select a candidate by document order.
- Reject facts with wrong entity, period type, dates or unit.
- Treat dimensions as material unless explicitly allowed.
- Preserve all competing candidate IDs.
- A component is not interchangeable with a statement total.
- A calculated candidate cannot be labeled directly extracted.
- Material ambiguity forces `confidence=low`, `reviewer_decision=unresolved` and no normalized
  population.

## 5. Extension Tags

For every extension candidate, retain:

- Extension QName and label.
- Taxonomy namespace and version.
- XBRL anchoring relationship, if present.
- Presentation and calculation parents/children.
- Rendered statement location.
- Closest supported standard concept.
- Reviewer rationale.

Extension mapping is versioned by company and taxonomy. Approval for one company or filing does not
generalize automatically to another issuer.

## 6. Review Status

Mapping lifecycle:

- `draft`: design or candidate mapping; extraction use prohibited.
- `reviewed`: concept/context review completed; fixture testing still required.
- `approved`: may be used by an explicitly approved prototype.
- `superseded`: retained for audit but not active.
- `rejected`: retained for audit but not active.

Every change to preferred tags, period/unit rules, sign, scale or extension behavior creates a new
mapping version. The extraction run records the exact mapping version used.

v0.3.4 uses `review_status=prototype_fixture_only`, which is below `approved`
and valid only for artificial local fixtures.

v0.3.6 stores mapping-review decisions separately from the mapping registry. The review batch must
record `approve_mapping`, `reject_mapping`, `request_more_evidence` or `supersede_mapping` for
each reviewed mapping record, with nonblank evidence notes. Superseded or rejected mapping review
status blocks promotion even when old extraction candidates still exist.
