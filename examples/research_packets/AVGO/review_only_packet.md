# Review-Only Research Packet: AVGO

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

- Pipeline run ID: `pipeline-real_company_review_only-avgo-2026-07-01T070058z0000`
- Mode: `real_company_review_only`
- Company: `Broadcom Inc.`
- Ticker: `AVGO`
- Fixture data status: `synthetic_or_excerpt_review_only`

## Candidate Summary

- Candidate count: `8`
- Candidate fields: `revenue, gross_profit, operating_income, net_income, operating_cash_flow, capital_expenditure, cash_and_equivalents, diluted_shares`
- Review batch: `normalized-review-avgo-7dc8a9c4d00a`
- Quality package: `review-quality-avgo-7dc8a9c4d00a`
- Quality score status: `review_only`
- Quality records: `8`
- Workbench reference: `goodluck-stock-research/examples/pipeline_runs/AVGO/review_only/workbench/review_workbench.md`
- Quality reference: `goodluck-stock-research/examples/pipeline_runs/AVGO/review_only/quality/review_quality_score.json`

## Candidate Fields

| Field | Candidate ID | Concept | Confidence | Warnings |
|---|---|---|---|---|
| revenue | avgo-revenue-candidate-001 | us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax | high | synthetic_real_company_fixture_unverified |
| gross_profit | avgo-gross_profit-candidate-001 | us-gaap:GrossProfit | high | synthetic_real_company_fixture_unverified |
| operating_income | avgo-operating_income-candidate-001 | us-gaap:OperatingIncomeLoss | high | synthetic_real_company_fixture_unverified |
| net_income | avgo-net_income-candidate-001 | us-gaap:NetIncomeLoss | high | synthetic_real_company_fixture_unverified |
| operating_cash_flow | avgo-operating_cash_flow-candidate-001 | us-gaap:NetCashProvidedByUsedInOperatingActivities | high | synthetic_real_company_fixture_unverified |
| capital_expenditure | avgo-capital_expenditure-candidate-001 | us-gaap:PaymentsToAcquirePropertyPlantAndEquipment | high | source_sign_preserved_in_source_value, synthetic_real_company_fixture_unverified |
| cash_and_equivalents | avgo-cash_and_equivalents-candidate-001 | us-gaap:CashAndCashEquivalentsAtCarryingValue | high | synthetic_real_company_fixture_unverified |
| diluted_shares | avgo-diluted_shares-candidate-001 | us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding | high | synthetic_real_company_fixture_unverified |

## Unresolved / Blocked Fields

- `revenue`
- `gross_profit`
- `operating_income`
- `net_income`
- `operating_cash_flow`
- `capital_expenditure`
- `cash_and_equivalents`
- `diluted_shares`

## Unresolved Field Explanations

| Field | Reason code | Reason | Reviewer next check |
|---|---|---|---|
| total_debt | debt_double_count_risk | A total-debt fact and debt components coexist; the prototype will not combine or choose between them. | Review fixture facts, mapping and context manually. |

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
- Snapshot SHA-256: `7dc8a9c4d00afce413507447e50bf457f5ece27e71a8c15a2afb18f27daf2df3`
- Review batch: `normalized-review-avgo-7dc8a9c4d00a`
- Candidate package: `goodluck-stock-research/examples/pipeline_runs/AVGO/review_only/candidate/extraction_candidates.json`
- Unresolved fields: `goodluck-stock-research/examples/pipeline_runs/AVGO/review_only/candidate/unresolved_fields.json`
- Workbench: `goodluck-stock-research/examples/pipeline_runs/AVGO/review_only/workbench/review_workbench.md`
- Quality score: `goodluck-stock-research/examples/pipeline_runs/AVGO/review_only/quality/review_quality_score.json`
