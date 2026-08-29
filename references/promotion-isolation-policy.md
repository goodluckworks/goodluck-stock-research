# Promotion Isolation Policy

## 1. Purpose

Promotion converts reviewed candidate records into an auditable fictional normalized draft. It is a separate gate after extraction, schema validation, mapping review and reviewer decision collection.
v0.3.7 also requires a ready review quality score and completed reviewer checklist for every
promoted record.
v0.3.8 adds a second, optional EXMP-only sandbox step that can convert the fictional promotion
package into a v0.2.x-compatible CSV draft. That CSV step is not part of promotion itself and
does not apply to real companies.

## 2. Default Deny Rules

- Deny promotion unless the review batch is normalized by `review_decision_collector.py`.
- Deny promotion unless the mapping review batch status is `approved`.
- Deny promotion if the mapping review status is `draft`, `reviewed`, `superseded` or `rejected`.
- Deny promotion unless a matching review quality score package is provided.
- Deny promotion if any promoted record lacks `approval_readiness=ready`, has blocking quality
  issues, or lacks a completed relationship checklist.
- Deny promotion for MRVL, NVDA, AVGO and other real-company-shaped fixtures by default.
- Deny normalized CSV sandbox generation unless the ticker is fictional EXMP.
- Deny v0.2.x dry-run unless the input is the EXMP normalized CSV sandbox with sandbox flags.

## 3. Fictional EXMP Allow Rule

Fictional EXMP may be promoted in tracked tests only when:

- `fictional_company=true`.
- Mapping review is approved.
- Review batch is normalized and approved.
- Review decision log is present.
- Review quality score is present and ready for every promoted record.
- Reviewer checklist is complete for every promoted record.
- Promotion manifest includes mapping review, decision log and package audit references.

## 4. Real-Company Promotion Future Gate

Real-company promotion is out of scope for v0.3.8. A future release would need an explicit policy, separate test plan, human approval path and additional source verification. No current flag or test authorizes real-company promotion, real-company normalized CSV generation or real-company v0.2.x dry-run.

## 5. Mapping Approval Requirement

Promotion must verify:

- Mapping version matches extraction and review packages.
- Mapping review file references the same mapping version.
- Mapping review batch status is `approved`.
- No reviewed mapping record is `superseded` or `rejected`.

## 6. Review Batch Requirement

Promotion must verify:

- Review batch was produced by `review_decision_collector.py`.
- Review batch status is `approved`.
- Every promoted record is `approve` or `adjust`.
- Every promoted record has completed checklist evidence, including `relationship_checked=true`.
- Every promoted record has ready quality score evidence and no blocking issues.
- Rejected, unresolved and needs-more-evidence records are excluded.

## 7. Audit Trail Requirement

Promotion manifest must include:

- `mapping_review_reference`
- `review_decision_log_reference`
- `quality_score_reference`
- `package_audit_reference`

These references do not make the output investment-ready; they only make the local promotion path auditable.

v0.3.8 normalized CSV sandbox must also preserve:

- `review_batch_id`
- `promotion_id`
- `mapping_version`
- `snapshot_sha256`
- candidate and review record references for every populated field
- fictional/sandbox/not-investment-data labels

## 8. Prohibited Outputs

Promotion must not directly generate:

- investment conclusion
- research status
- target price
- buy / sell / hold
- position size
- broker, order or trading output

The separate v0.3.8 CSV sandbox generator may generate a populated v0.2.x-compatible CSV only
for fictional EXMP. It must not generate such files for MRVL, NVDA, AVGO or any real company.

## 9. Failure Behavior

Failures must be explicit and blocking. The tool should return an error rather than silently downgrading a missing mapping review, missing decision log, raw workbench template or real-company ticker.

## 10. Examples

- Allowed: fictional EXMP normalized review batch with approved mapping review and decision log.
- Allowed: fictional EXMP promotion package converted to a sandbox CSV, then run through an explicit ratio dry-run.
- Blocked: MRVL / NVDA / AVGO even if a reviewer decision file exists.
- Blocked: MRVL / NVDA / AVGO normalized CSV generation or v0.2.x calculation dry-run.
- Blocked: any package using a superseded mapping review.
- Blocked: raw workbench decision template used directly as a review batch.
