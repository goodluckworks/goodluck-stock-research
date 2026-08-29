# XBRL Reviewer Workbench

> NOT APPROVED. This workbench is a human review aid, not a normalized financial output.

## Summary

- Company: `Marvell Technology, Inc.`
- Ticker: `MRVL`
- Fixture data status: `synthetic_unverified_real_company_shape`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Extraction run ID: `xbrl-mrvl-fy2026-a1aaa9bfaf36`
- Snapshot SHA-256: `a1aaa9bfaf3605ceb1dbce7ae810c87044f6e651b96e94c60c27043205bedd6a`
- Generated at: `2026-06-29T09:22:19+00:00`

## Executive Review Summary

- Candidate count: `7`
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
- Complete filing storage and production parsing are out of scope.
- Reviewer decision file is separate.
- Review quality scores are advisory and cannot approve fields.
- No target price, recommendation, buy/sell/hold, position size or research status is produced.

## Candidate Table by Normalized Field

| Field | Candidate ID | Concept | Confidence | Relationship Confidence | Warnings |
|---|---|---|---|---|---|
| `operating_income` | `mrvl-operating_income-candidate-001` | `us-gaap:OperatingIncomeLoss` | `high` | `high` | `synthetic_real_company_fixture_unverified` |
| `net_income` | `mrvl-net_income-candidate-001` | `us-gaap:NetIncomeLoss` | `high` | `medium` | `synthetic_real_company_fixture_unverified` |
| `operating_cash_flow` | `mrvl-operating_cash_flow-candidate-001` | `us-gaap:NetCashProvidedByUsedInOperatingActivities` | `high` | `high` | `synthetic_real_company_fixture_unverified` |
| `capital_expenditure` | `mrvl-capital_expenditure-candidate-001` | `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` | `high` | `medium` | `source_sign_preserved_in_source_value, synthetic_real_company_fixture_unverified` |
| `cash_and_equivalents` | `mrvl-cash_and_equivalents-candidate-001` | `us-gaap:CashAndCashEquivalentsAtCarryingValue` | `high` | `high` | `synthetic_real_company_fixture_unverified` |
| `total_debt` | `mrvl-total_debt-candidate-001` | `fixture:TotalDebt` | `high` | `medium` | `synthetic_real_company_fixture_unverified` |
| `diluted_shares` | `mrvl-diluted_shares-candidate-001` | `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding` | `high` | `high` | `synthetic_real_company_fixture_unverified` |

## Candidates

### operating_income / `mrvl-operating_income-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-operating_income-candidate-001` |
| normalized_field | `operating_income` |
| extracted_value | `12` |
| source_value | `12` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:OperatingIncomeLoss` |
| concept_label | `Operating income or loss` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `synthetic MRVL operating income` |
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

### net_income / `mrvl-net_income-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-net_income-candidate-001` |
| normalized_field | `net_income` |
| extracted_value | `8` |
| source_value | `8` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:NetIncomeLoss` |
| concept_label | `Net income or loss` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `synthetic MRVL net income` |
| transformation | `identity` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `medium` |
| warning_flags | `['synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-mrvl-net_income-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `us-gaap` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:NetIncomeLoss` |
| presentation_parent | `income_statement_bottom_line` |
| presentation_children | `[]` |
| calculation_parent | `not_applicable` |
| calculation_children | `[]` |
| anchor_concept | `us-gaap:NetIncomeLoss` |
| relationship_basis | `standard net income concept; attribution basis still requires review notes` |
| relationship_evidence_notes | `standard net income concept; attribution basis still requires review notes` |
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
| extracted_value | `20` |
| source_value | `20` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:NetCashProvidedByUsedInOperatingActivities` |
| concept_label | `Net cash provided by used in operating activities` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `synthetic MRVL operating cash flow` |
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
| extracted_value | `6` |
| source_value | `-6` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` |
| concept_label | `Payments to acquire property plant and equipment` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `synthetic MRVL capex` |
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

### cash_and_equivalents / `mrvl-cash_and_equivalents-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-cash_and_equivalents-candidate-001` |
| normalized_field | `cash_and_equivalents` |
| extracted_value | `15` |
| source_value | `15` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `us-gaap:CashAndCashEquivalentsAtCarryingValue` |
| concept_label | `Cash and cash equivalents at carrying value` |
| concept_type | `standard` |
| context_id | `MRVL-2026` |
| period_type | `instant` |
| dimensions | `[]` |
| source_locator | `synthetic MRVL cash` |
| transformation | `identity` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `high` |
| warning_flags | `['synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-mrvl-cash_and_equivalents-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `us-gaap` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:CashAndCashEquivalentsAtCarryingValue` |
| presentation_parent | `balance_sheet_current_assets` |
| presentation_children | `[]` |
| calculation_parent | `not_applicable` |
| calculation_children | `[]` |
| anchor_concept | `us-gaap:CashAndCashEquivalentsAtCarryingValue` |
| relationship_basis | `cash-only concept; restricted cash, short-term investments and marketable securities are excluded from this field` |
| relationship_evidence_notes | `cash-only concept; restricted cash, short-term investments and marketable securities are excluded from this field` |
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

### total_debt / `mrvl-total_debt-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-total_debt-candidate-001` |
| normalized_field | `total_debt` |
| extracted_value | `30` |
| source_value | `30` |
| unit | `USD millions` |
| period | `FY2026` |
| concept_qname | `fixture:TotalDebt` |
| concept_label | `Total debt fixture concept or reviewed current/noncurrent debt components` |
| concept_type | `fixture_local` |
| context_id | `MRVL-2026` |
| period_type | `instant` |
| dimensions | `[]` |
| source_locator | `synthetic MRVL debt` |
| transformation | `identity` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `medium` |
| warning_flags | `['synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-mrvl-total_debt-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `fixture` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:LongTermDebtAndFinanceLeaseObligations` |
| presentation_parent | `balance_sheet_liabilities_or_debt_note` |
| presentation_children | `['us-gaap:LongTermDebtAndFinanceLeaseObligationsCurrent', 'us-gaap:LongTermDebtAndFinanceLeaseObligationsNoncurrent']` |
| calculation_parent | `fixture:TotalDebt` |
| calculation_children | `['us-gaap:LongTermDebtAndFinanceLeaseObligationsCurrent', 'us-gaap:LongTermDebtAndFinanceLeaseObligationsNoncurrent']` |
| anchor_concept | `us-gaap:LongTermDebtAndFinanceLeaseObligations` |
| relationship_basis | `use a reviewed total or non-overlapping current plus noncurrent components; never combine total with components` |
| relationship_evidence_notes | `use a reviewed total or non-overlapping current plus noncurrent components; never combine total with components` |
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

### diluted_shares / `mrvl-diluted_shares-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `mrvl-diluted_shares-candidate-001` |
| normalized_field | `diluted_shares` |
| extracted_value | `50` |
| source_value | `50` |
| unit | `million shares` |
| period | `FY2026` |
| concept_qname | `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding` |
| concept_label | `Weighted average number of diluted shares outstanding` |
| concept_type | `standard` |
| context_id | `MRVL-FY2026` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `synthetic MRVL diluted shares` |
| transformation | `identity` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `high` |
| warning_flags | `['synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-mrvl-diluted_shares-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `us-gaap` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding` |
| presentation_parent | `eps_note` |
| presentation_children | `[]` |
| calculation_parent | `not_applicable` |
| calculation_children | `[]` |
| anchor_concept | `us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding` |
| relationship_basis | `weighted-average diluted shares for exact duration; not ending shares or basic shares` |
| relationship_evidence_notes | `weighted-average diluted shares for exact duration; not ending shares or basic shares` |
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

