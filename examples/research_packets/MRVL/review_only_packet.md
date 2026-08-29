# Review-Only Research Packet: MRVL

## Boundary

- Review-only packet, not a final investment report.
- Draft / unapproved.
- Synthetic or excerpt fixture, not authoritative company data.
- Not investment advice.
- Not production research.
- No target price.
- No buy/sell/hold instruction.
- No position size.
- No trading action.

## Pipeline Summary

- Pipeline run ID: `pipeline-real_company_review_only-mrvl-2026-07-01T070057z0000`
- Mode: `real_company_review_only`
- Company: `Marvell Technology, Inc.`
- Ticker: `MRVL`
- Fixture data status: `synthetic_or_excerpt_review_only`

## Candidate Summary

- Candidate count: `7`
- Candidate fields: `operating_income, net_income, operating_cash_flow, capital_expenditure, cash_and_equivalents, total_debt, diluted_shares`
- Review batch: `normalized-review-mrvl-a1aaa9bfaf36`
- Quality package: `review-quality-mrvl-a1aaa9bfaf36`
- Quality score status: `review_only`
- Quality records: `7`
- Workbench reference: `goodluck-stock-research/examples/pipeline_runs/MRVL/review_only/workbench/review_workbench.md`
- Quality reference: `goodluck-stock-research/examples/pipeline_runs/MRVL/review_only/quality/review_quality_score.json`

## Candidate Fields

| Field | Candidate ID | Concept | Confidence | Warnings |
|---|---|---|---|---|
| operating_income | mrvl-operating_income-candidate-001 | us-gaap:OperatingIncomeLoss | high | synthetic_real_company_fixture_unverified |
| net_income | mrvl-net_income-candidate-001 | us-gaap:NetIncomeLoss | high | synthetic_real_company_fixture_unverified |
| operating_cash_flow | mrvl-operating_cash_flow-candidate-001 | us-gaap:NetCashProvidedByUsedInOperatingActivities | high | synthetic_real_company_fixture_unverified |
| capital_expenditure | mrvl-capital_expenditure-candidate-001 | us-gaap:PaymentsToAcquirePropertyPlantAndEquipment | high | source_sign_preserved_in_source_value, synthetic_real_company_fixture_unverified |
| cash_and_equivalents | mrvl-cash_and_equivalents-candidate-001 | us-gaap:CashAndCashEquivalentsAtCarryingValue | high | synthetic_real_company_fixture_unverified |
| total_debt | mrvl-total_debt-candidate-001 | fixture:TotalDebt | high | synthetic_real_company_fixture_unverified |
| diluted_shares | mrvl-diluted_shares-candidate-001 | us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding | high | synthetic_real_company_fixture_unverified |

## Unresolved / Blocked Fields

- `operating_income`
- `net_income`
- `operating_cash_flow`
- `capital_expenditure`
- `cash_and_equivalents`
- `total_debt`
- `diluted_shares`

## Unresolved Field Explanations

| Field | Reason code | Reason | Reviewer next check |
|---|---|---|---|
| revenue | multiple_candidates | Multiple eligible facts remain; first-match selection is prohibited. | Review fixture facts, mapping and context manually. |
| gross_profit | missing_field | No mapped fact was present. | Review fixture facts, mapping and context manually. |

## Reviewer Evidence Checks

- Confirm source period, unit, scale, sign and context for every candidate.
- Reconcile candidate fields against the workbench and quality score before any approval decision.
- Resolve every unresolved field from the table above; do not infer or zero-fill.
- Document source evidence before any future quarantine gate.

## Blocked Steps

| Step | Reason |
|---|---|
| promotion | real_company_promotion_blocked |
| normalized_csv | real_company_csv_generation_blocked |
| v02_ratio_dry_run | real_company_dry_run_blocked |

## Explicit Non-Outputs

- No approval.
- No promotion.
- No normalized CSV.
- No v0.2.x dry-run.
- No approved normalized input.
- Suitable for promotion: `No`.
- Reason: real-company review packet is synthetic/excerpt-only and lacks explicit controlled sandbox approval.

## Audit References

- Mapping version: `us-gaap-core-v0.3.7-fixture-1`
- Snapshot SHA-256: `a1aaa9bfaf3605ceb1dbce7ae810c87044f6e651b96e94c60c27043205bedd6a`
- Review batch: `normalized-review-mrvl-a1aaa9bfaf36`
- Candidate package: `goodluck-stock-research/examples/pipeline_runs/MRVL/review_only/candidate/extraction_candidates.json`
- Unresolved fields: `goodluck-stock-research/examples/pipeline_runs/MRVL/review_only/candidate/unresolved_fields.json`
- Workbench: `goodluck-stock-research/examples/pipeline_runs/MRVL/review_only/workbench/review_workbench.md`
- Quality score: `goodluck-stock-research/examples/pipeline_runs/MRVL/review_only/quality/review_quality_score.json`
