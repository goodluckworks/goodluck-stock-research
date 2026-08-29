# Pipeline Audit Dashboard

Generated at: `2026-07-01T07:06:07+00:00`

| Ticker | Mode | Fixture status | Promotion | Normalized CSV | Dry-run | Packet | Audit | Safety | Unresolved fields | Missing fields | Approval readiness |
|---|---|---|---|---|---|---|---|---|---:|---:|---|
| AVGO | real_company_review_only | synthetic_or_excerpt_review_only | blocked_or_not_applicable | blocked_or_not_applicable | blocked_or_not_applicable | present | complete | pass | 0 | 0 | review_only_or_not_applicable |
| EXMP | fictional_sandbox_full | fictional_sample | present | present | present | present | complete | pass | 1 | 20 | review_only_or_not_applicable |
| EXMP | fictional_sandbox_partial | fictional_sample | present | present | present | present | complete | pass | 1 | 20 | review_only_or_not_applicable |
| MRVL | real_company_review_only | synthetic_or_excerpt_review_only | blocked_or_not_applicable | blocked_or_not_applicable | blocked_or_not_applicable | present | complete | pass | 0 | 0 | review_only_or_not_applicable |
| NVDA | real_company_review_only | synthetic_or_excerpt_review_only | blocked_or_not_applicable | blocked_or_not_applicable | blocked_or_not_applicable | present | complete | pass | 0 | 0 | review_only_or_not_applicable |

## Boundary

- EXMP may have fictional sandbox promotion, normalized CSV and ratio dry-run.
- MRVL / NVDA / AVGO must remain review-only.
- No real-company promotion, normalized CSV or v0.2.x dry-run should be present.
- No target price, buy/sell/hold, position size, research status or trading action.
