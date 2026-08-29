# XBRL Reviewer Workbench

> NOT APPROVED. This workbench is a human review aid, not a normalized financial output.

## Summary

- Company: `Marvell Technology, Inc.`
- Ticker: `MRVL`
- Fixture data status: `real_filing_excerpt_drill`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Extraction run ID: `xbrl-mrvl-fy2026-29b488050b1b`
- Snapshot SHA-256: `29b488050b1b47b4734ba9723aa03a53e5b3163e4c73fbd97a0f0128be18491e`
- Generated at: `2026-06-29T09:23:05+00:00`

## Executive Review Summary

- Candidate count: `3`
- Workbench status: `draft_review_workspace`
- Approval readiness: `requires reviewer checklist, quality score and normalized decision collection`
- Real-company boundary: `synthetic/unverified real-company-shaped fixture`

## Approval Readiness

- Current state: `not_approved`
- Required gates: `completed review checklist`, `ready review quality score`, `normalized review decision`, `approved mapping relationship review`, `package audit`
- This workbench cannot approve fields by itself.

## Blocking Issues

- Candidate warning flags must be resolved or documented.
- Missing provenance, missing taxonomy relationship evidence, weak relationship evidence, low confidence or unresolved competing candidates block approve / adjust decisions.
- Real-company excerpt drills remain draft-only and cannot be promoted.

## Boundary

- This is not approval.
- This is not investment advice.
- Real-company-shaped fixtures are synthetic/unverified unless explicitly stated.
- Real filing excerpt drill: excerpt only, not a complete filing, not authoritative financial data, no approved values.
- Complete filing storage and production parsing are out of scope.
- Reviewer decision file is separate.
- Review quality scores are advisory and cannot approve fields.
- No target price, recommendation, buy/sell/hold, position size or research status is produced.

## Candidate Table by Normalized Field

| Field | Candidate ID | Concept | Confidence | Relationship Confidence | Warnings |
|---|---|---|---|---|---|
| `operating_income` | `mrvl-operating_income-candidate-001` | `us-gaap:OperatingIncomeLoss` | `high` | `high` | `synthetic_real_company_fixture_unverified` |
| `operating_cash_flow` | `mrvl-operating_cash_flow-candidate-001` | `us-gaap:NetCashProvidedByUsedInOperatingActivities` | `high` | `high` | `synthetic_real_company_fixture_unverified` |
| `capital_expenditure` | `mrvl-capital_expenditure-candidate-001` | `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` | `high` | `medium` | `source_sign_preserved_in_source_value, synthetic_real_company_fixture_unverified` |

## Candidates

### operating_income / `mrvl-operating_income-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-operating_income-candidate-001` |
| normalized_field | `operating_income` |
| extracted_value | `-120` |
| source_value | `-120` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:OperatingIncomeLoss` |
| concept_label | `Operating income or loss` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `excerpt operating loss line` |
| transformation | `identity` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `high` |
| warning_flags | `['synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-mrvl-operating_income-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `us-gaap` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:OperatingIncomeLoss` |
| presentation_parent | `income_statement_operating_result` |
| presentation_children | `[]` |
| calculation_parent | `not_applicable` |
| calculation_children | `[]` |
| anchor_concept | `us-gaap:OperatingIncomeLoss` |
| relationship_basis | `standard operating result concept; not income before tax` |
| relationship_evidence_notes | `standard operating result concept; not income before tax` |
| relationship_review_status | `reviewed` |

#### Warning Flags by Severity

- Severity `review_required` / flag `synthetic_real_company_fixture_unverified`: inspect source context, relationship evidence and competing candidates before approval.

#### Competing Candidates Comparison

- Competing candidate IDs: `none`
- If competing candidates exist, compare concept label, context, period, unit, dimensions, source locator and relationship evidence before approval.
- If no competing candidates exist, still confirm the field is not duplicated in unresolved or rejected facts.

#### Review Checklist

| Checklist Item | Current Value | Reviewer Instruction |
|---|---:|---|
| period checked | `False` | Review and mark true only with evidence. |
| unit checked | `False` | Review and mark true only with evidence. |
| context checked | `False` | Review and mark true only with evidence. |
| dimensions checked | `False` | Review and mark true only with evidence. |
| sign checked | `False` | Review and mark true only with evidence. |
| scale checked | `False` | Review and mark true only with evidence. |
| relationship checked | `False` | Review and mark true only with evidence. |
| competing candidates checked | `True` | Review and mark true only with evidence. |
| prior period checked | `False` | Review and mark true only with evidence. |
| materiality checked | `False` | Review and mark true only with evidence. |
| reviewer notes present | `False` | Review and mark true only with evidence. |

#### Reviewer Questions

- Why might this candidate be suspicious?
- Why might this candidate be acceptable?
- Which source evidence, statement line, note, context, unit and relationship supports approval?
- Are there competing candidates or material prior-period changes?

#### Required Evidence

- Source locator and source fact IDs.
- Period, unit, context and dimension evidence.
- Relationship metadata and anchor / closest standard concept evidence.
- Transformation and sign/scale evidence.
- Reviewer notes explaining any approval or adjustment.

### operating_cash_flow / `mrvl-operating_cash_flow-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-operating_cash_flow-candidate-001` |
| normalized_field | `operating_cash_flow` |
| extracted_value | `1700` |
| source_value | `1700` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:NetCashProvidedByUsedInOperatingActivities` |
| concept_label | `Net cash provided by used in operating activities` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `excerpt operating cash flow line` |
| transformation | `identity` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `high` |
| warning_flags | `['synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-mrvl-operating_cash_flow-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `us-gaap` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:NetCashProvidedByUsedInOperatingActivities` |
| presentation_parent | `cash_flow_operating_activities` |
| presentation_children | `[]` |
| calculation_parent | `not_applicable` |
| calculation_children | `[]` |
| anchor_concept | `us-gaap:NetCashProvidedByUsedInOperatingActivities` |
| relationship_basis | `standard operating activities total only` |
| relationship_evidence_notes | `standard operating activities total only` |
| relationship_review_status | `reviewed` |

#### Warning Flags by Severity

- Severity `review_required` / flag `synthetic_real_company_fixture_unverified`: inspect source context, relationship evidence and competing candidates before approval.

#### Competing Candidates Comparison

- Competing candidate IDs: `none`
- If competing candidates exist, compare concept label, context, period, unit, dimensions, source locator and relationship evidence before approval.
- If no competing candidates exist, still confirm the field is not duplicated in unresolved or rejected facts.

#### Review Checklist

| Checklist Item | Current Value | Reviewer Instruction |
|---|---:|---|
| period checked | `False` | Review and mark true only with evidence. |
| unit checked | `False` | Review and mark true only with evidence. |
| context checked | `False` | Review and mark true only with evidence. |
| dimensions checked | `False` | Review and mark true only with evidence. |
| sign checked | `False` | Review and mark true only with evidence. |
| scale checked | `False` | Review and mark true only with evidence. |
| relationship checked | `False` | Review and mark true only with evidence. |
| competing candidates checked | `True` | Review and mark true only with evidence. |
| prior period checked | `False` | Review and mark true only with evidence. |
| materiality checked | `False` | Review and mark true only with evidence. |
| reviewer notes present | `False` | Review and mark true only with evidence. |

#### Reviewer Questions

- Why might this candidate be suspicious?
- Why might this candidate be acceptable?
- Which source evidence, statement line, note, context, unit and relationship supports approval?
- Are there competing candidates or material prior-period changes?

#### Required Evidence

- Source locator and source fact IDs.
- Period, unit, context and dimension evidence.
- Relationship metadata and anchor / closest standard concept evidence.
- Transformation and sign/scale evidence.
- Reviewer notes explaining any approval or adjustment.

### capital_expenditure / `mrvl-capital_expenditure-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-capital_expenditure-candidate-001` |
| normalized_field | `capital_expenditure` |
| extracted_value | `420` |
| source_value | `-420` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` |
| concept_label | `Payments to acquire property plant and equipment` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `excerpt capex line` |
| transformation | `absolute_value_to_positive_outflow` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `medium` |
| warning_flags | `['source_sign_preserved_in_source_value', 'synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-mrvl-capital_expenditure-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `us-gaap` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` |
| presentation_parent | `cash_flow_investing_activities` |
| presentation_children | `[]` |
| calculation_parent | `not_applicable` |
| calculation_children | `[]` |
| anchor_concept | `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` |
| relationship_basis | `PP&E acquisition/payment concept; excludes business combinations, capitalized software and unrelated investing cash flows unless separately reviewed` |
| relationship_evidence_notes | `PP&E acquisition/payment concept; excludes business combinations, capitalized software and unrelated investing cash flows unless separately reviewed` |
| relationship_review_status | `reviewed` |

#### Warning Flags by Severity

- Severity `review_required` / flag `source_sign_preserved_in_source_value`: inspect source context, relationship evidence and competing candidates before approval.
- Severity `review_required` / flag `synthetic_real_company_fixture_unverified`: inspect source context, relationship evidence and competing candidates before approval.

#### Competing Candidates Comparison

- Competing candidate IDs: `none`
- If competing candidates exist, compare concept label, context, period, unit, dimensions, source locator and relationship evidence before approval.
- If no competing candidates exist, still confirm the field is not duplicated in unresolved or rejected facts.

#### Review Checklist

| Checklist Item | Current Value | Reviewer Instruction |
|---|---:|---|
| period checked | `False` | Review and mark true only with evidence. |
| unit checked | `False` | Review and mark true only with evidence. |
| context checked | `False` | Review and mark true only with evidence. |
| dimensions checked | `False` | Review and mark true only with evidence. |
| sign checked | `False` | Review and mark true only with evidence. |
| scale checked | `False` | Review and mark true only with evidence. |
| relationship checked | `False` | Review and mark true only with evidence. |
| competing candidates checked | `True` | Review and mark true only with evidence. |
| prior period checked | `False` | Review and mark true only with evidence. |
| materiality checked | `False` | Review and mark true only with evidence. |
| reviewer notes present | `False` | Review and mark true only with evidence. |

#### Reviewer Questions

- Why might this candidate be suspicious?
- Why might this candidate be acceptable?
- Which source evidence, statement line, note, context, unit and relationship supports approval?
- Are there competing candidates or material prior-period changes?

#### Required Evidence

- Source locator and source fact IDs.
- Period, unit, context and dimension evidence.
- Relationship metadata and anchor / closest standard concept evidence.
- Transformation and sign/scale evidence.
- Reviewer notes explaining any approval or adjustment.

