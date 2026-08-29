# XBRL Reviewer Workbench

> NOT APPROVED. This workbench is a human review aid, not a normalized financial output.

## Summary

- Company: `Broadcom Inc.`
- Ticker: `AVGO`
- Fixture data status: `real_filing_excerpt_drill`
- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Extraction run ID: `xbrl-avgo-fy2025-1f3d337d3708`
- Snapshot SHA-256: `1f3d337d3708945b3aed545de6b3f180ba2bffa9c5c9173c652c992f46dfe350`
- Generated at: `2026-06-29T09:23:05+00:00`

## Executive Review Summary

- Candidate count: `1`
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
| `revenue` | `avgo-revenue-candidate-001` | `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax` | `high` | `high` | `synthetic_real_company_fixture_unverified` |

## Candidates

### revenue / `avgo-revenue-candidate-001`

> NOT APPROVED. This candidate is a draft review item only.

| Field | Value |
|---|---|
| candidate_id | `avgo-revenue-candidate-001` |
| normalized_field | `revenue` |
| extracted_value | `51000` |
| source_value | `51000` |
| unit | `USD millions` |
| period | `FY2025` |
| concept_qname | `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax` |
| concept_label | `Revenue from contracts with customers, excluding assessed tax` |
| concept_type | `standard` |
| context_id | `AVGO-FY2025` |
| period_type | `duration` |
| dimensions | `[]` |
| source_locator | `excerpt consolidated revenue line` |
| transformation | `identity` |
| confidence | `high` |
| confidence explanation | `Extraction confidence reflects fixture matching strength only; approval also requires provenance, taxonomy relationship evidence, checklist completion and quality score readiness.` |
| relationship_confidence | `high` |
| warning_flags | `['synthetic_real_company_fixture_unverified']` |
| competing_candidate_ids | `none` |
| review_status | `draft_extracted_unreviewed` |
| provenance link | `provenance-avgo-revenue-candidate-001` |

#### Relationship Metadata

| Field | Value |
|---|---|
| taxonomy_namespace | `us-gaap` |
| taxonomy_version | `fixture-v0.3.7` |
| closest_standard_concept | `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax` |
| presentation_parent | `income_statement_revenue` |
| presentation_children | `[]` |
| calculation_parent | `not_applicable` |
| calculation_children | `[]` |
| anchor_concept | `us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax` |
| relationship_basis | `standard tag; fixture fallback fixture:ConsolidatedRevenue requires reviewed revenue relationship` |
| relationship_evidence_notes | `standard tag; fixture fallback fixture:ConsolidatedRevenue requires reviewed revenue relationship` |
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

