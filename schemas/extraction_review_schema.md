# Extraction Review Schema

## 1. Purpose

This schema defines the human review record between draft XBRL extraction candidates and any
future approved normalized CSV / JSON. v0.3.4 implements validation for this gate and a
fictional-only promotion draft. v0.3.5 adds machine-readable review and promotion schemas plus
package-level audit. v0.3.6 adds reviewer workbench generation and review decision collection:
raw workbench templates are not promotion-ready; only collector-normalized review batches may pass
the promotion gate. It still does not generate a v0.2.x financial input.
v0.3.7 adds review checklist records and advisory review quality scores. Approve / adjust decisions
require completed checklist evidence and `approval_readiness=ready` with no blocking issues.
v0.3.8 adds a fictional-only normalized CSV sandbox after promotion. Only EXMP fictional
promotion output may be converted into a populated v0.2.x-compatible CSV draft, and only that
sandbox CSV may be used for an EXMP ratio dry-run.

## 2. Review Record Fields

Document-level fields:

| Field | Required | Meaning |
|---|---:|---|
| `review_schema_version` | Yes | Immutable schema version |
| `review_batch_id` | Yes | Groups records for one extraction run |
| `extraction_run_id` | Yes | Links candidate output and mapping version |
| `raw_snapshot_id` | Yes | Links immutable source evidence |
| `snapshot_sha256` | Yes | Integrity check before review |
| `mapping_version` | Yes | Exact field-mapping version |
| `created_at` | Yes | Timezone-aware timestamp |
| `batch_status` | Yes | `pending`, `partially_reviewed`, `approved`, `rejected`, `superseded` |
| `records` | Yes | Array of review records |

Each review record includes at least:

| Field | Required | Meaning |
|---|---:|---|
| `review_record_id` | Yes | Stable unique ID |
| `run_id` | Yes | Extraction run identifier |
| `company` | Yes | Legal company name |
| `ticker` | Yes | Ticker or explicit unresolved marker |
| `cik` | Yes | SEC CIK |
| `accession` | Yes | Filing accession |
| `form_type` | Yes | Initially 10-K or 10-Q |
| `normalized_field` | Yes | Supported target field |
| `candidate_id` | Yes | Candidate provenance link |
| `extracted_value` | Yes | Source-precision value or explicit unknown |
| `unit` | Yes | Source unit |
| `period` | Yes | Exact instant or duration |
| `source_tag` | Yes | Concept QName |
| `source_context` | Yes | Context ID, entity, dimensions and dates |
| `source_locator` | Yes | Statement/note plus raw evidence locator |
| `transformation` | Yes | Identity, unit scale, sign normalization, sum, etc. |
| `confidence` | Yes | `high`, `medium`, `low` |
| `warning_flags` | Yes | Array; empty if none |
| `competing_candidate_ids` | Yes | Array; empty if none |
| `reviewer_decision` | Yes | Decision enumeration |
| `reviewer_id` | Yes | Non-sensitive reviewer identifier |
| `reviewer_notes` | Yes | Evidence and rationale; `none` only when permitted |
| `approved_value` | Yes | Number or explicit `not_approved` |
| `approved_unit` | Yes | Unit or `not_approved` |
| `approval_timestamp` | Yes | Timezone-aware timestamp or `not_approved` |
| `prior_review_record_id` | Yes | Prior version or `not_applicable` |
| `review_checklist` | Yes | Period, unit, context, dimension, sign, scale, relationship, competing candidates, prior/materiality and reviewer-notes checks |
| `review_quality` | Yes | Advisory quality record with completeness, provenance, relationship, ambiguity, readiness and blocking issues |
| `quality_score_reference` | Yes | Quality score package ID used by review decision collection |

No field may be blank. Unknowns use explicit markers such as `unresolved`, `not_applicable` or
`not_approved`.

## 3. Reviewer Decisions

- `approve`: extracted value and transformation are accepted as the approved value.
- `adjust`: reviewer supplies a different `approved_value`, unit and explanation while preserving
  the original extracted value.
- `reject`: candidate is invalid and must not populate normalized output.
- `unresolved`: evidence is insufficient or materially ambiguous.
- `needs_more_evidence`: review pauses pending another filing context, note or mapping decision.

Rules:

- `approve` requires high or medium confidence, resolved warnings and a nonblank rationale.
- `adjust` requires the adjustment formula/rationale and supporting evidence IDs.
- `reject`, `unresolved` and `needs_more_evidence` require `approved_value=not_approved`.
- Low-confidence candidates cannot be approved without additional evidence and a new reviewed
  candidate or explicit escalation policy.

## 4. Approval Gate

A future normalized output may be generated only when:

1. Raw snapshot checksum still matches.
2. Source manifest and candidate provenance resolve.
3. Mapping version is approved and not superseded.
4. Filing identity, form, accession and period match the requested output.
5. Every populated field has one final `approve` or `adjust` record.
6. No blocking warning or unresolved competing candidate remains.
7. Currency, amount unit, share unit, sign and scale are approved.
8. The review batch is immutable after approval; corrections create a new batch.

The promotion step must be separate and explicit. Extraction alone cannot call v0.2.x scripts or
write an approved normalized file.

v0.3.4 promotion additionally requires `fictional_company=true` unless an
explicit real-company override is supplied. The override is not used in tests
or examples; MRVL, NVDA and AVGO remain draft/unreviewed.

v0.3.5 package audit checks review batch identity, snapshot checksum, mapping version, candidate
references and promotion decisions across files. Audit passing does not approve real-company data;
it only confirms consistency of the local package.

v0.3.6 promotion additionally requires:

- `normalized_review_batch=true`
- `decision_source=normalized_review_batch`
- `batch_status=approved`
- approved mapping review reference
- review decision log reference
- package audit reference

The raw reviewer workbench decision template must never be used directly for promotion.

v0.3.7 promotion additionally requires:

- ready review quality score file matching extraction run, snapshot and mapping version
- no blocking quality issues for promoted records
- completed reviewer checklist for every approve / adjust record
- `relationship_checked=true` and reviewed taxonomy relationship evidence

Review quality scores are advisory gates only. They cannot approve fields, produce normalized output
or create investment conclusions by themselves.

v0.3.8 CSV sandbox additionally requires:

- ticker `EXMP`
- `fictional_company=true`
- source review batch and promotion manifest IDs
- mapping version and snapshot checksum matching extraction, review and promotion packages
- field-level audit records for every populated CSV value
- explicit fictional/sandbox/not-investment-data labels

MRVL, NVDA, AVGO and any real-company-shaped package remain blocked from normalized CSV
generation and v0.2.x dry-run.

If only some fields pass, a partial normalized file is allowed only when the target v0.2.x schema
and downstream script explicitly support those omissions. All omitted fields remain unresolved.

## 5. Audit Trail

- Preserve extraction candidate, original review and every revised review record.
- Never overwrite an approved value silently.
- `adjust` retains both extracted and approved values.
- Reviewer identity should be a local alias or role, not sensitive personal data.
- Record timestamps with timezone.
- Link every approved field to snapshot hash, mapping version and provenance.
- Amendment/restatement creates a new review batch and marks affected prior approvals superseded.
- A changed mapping version invalidates dependent approvals until re-reviewed.
- Audit records contain no investment conclusion, recommendation or trading action.

## 6. Examples

### Approved direct fact

```yaml
review_record_id: mrvl-fy2026-revenue-review-001
run_id: mrvl-10k-extraction-draft-001
company: Marvell Technology, Inc.
ticker: MRVL
cik: "0001835632"
accession: 0001835632-26-000011
form_type: 10-K
normalized_field: revenue
candidate_id: mrvl-fy2026-revenue-candidate-001
extracted_value: unresolved
unit: USD
period: 2025-02-02/2026-01-31
source_tag: us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax
source_context: entity and exact annual duration; no dimensions
source_locator: consolidated statement locator placeholder
transformation: unit_scale_pending
confidence: high
warning_flags:
  - design_example_no_value_extracted
competing_candidate_ids: []
reviewer_decision: unresolved
reviewer_id: design-reviewer
reviewer_notes: Schema example only; no company value is present or approved.
approved_value: not_approved
approved_unit: not_approved
approval_timestamp: not_approved
prior_review_record_id: not_applicable
```

The example deliberately does not approve a financial value. It demonstrates record shape only.

### Adjusted capex sign

```yaml
review_record_id: example-capex-review-001
run_id: fictional-extraction-draft-001
company: Example Semiconductor Corp.
ticker: EXMP
cik: "0000000000"
accession: fictional
form_type: 10-K
normalized_field: capital_expenditure
candidate_id: example-capex-candidate-001
extracted_value: -125
unit: USD millions
period: FY2025
source_tag: example:PaymentsToAcquirePropertyPlantAndEquipment
source_context: fictional exact annual duration
source_locator: fictional cash flow statement
transformation: absolute_value
confidence: medium
warning_flags: []
competing_candidate_ids: []
reviewer_decision: adjust
reviewer_id: example-reviewer
reviewer_notes: Fictional example; normalize cash outflow magnitude as positive for v0.2.x.
approved_value: 125
approved_unit: USD millions
approval_timestamp: 2026-06-25T12:00:00Z
prior_review_record_id: not_applicable
```

All values in the second example are fictional and cannot be used for investment analysis.
