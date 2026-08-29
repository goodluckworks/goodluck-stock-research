# Dashboard Quality Report

## Summary

- Passed: Yes
- Failed checks: 0

## Checks

| Check | Result | Notes |
|---|---:|---|
| all pipeline modes represented | Pass | modes: ['fictional_sandbox_full', 'fictional_sandbox_partial', 'real_company_review_only'] |
| MRVL review-only run represented | Pass | present |
| MRVL blocked promotion has reason | Pass | real_company_promotion_blocked |
| MRVL blocked normalized_csv has reason | Pass | real_company_csv_generation_blocked |
| MRVL blocked v02_dry_run has reason | Pass | real_company_dry_run_blocked |
| MRVL review-only packet has no dry-run | Pass | blocked_or_not_applicable |
| MRVL review-only has no promotion | Pass | blocked_or_not_applicable |
| MRVL review-only has no normalized CSV | Pass | blocked_or_not_applicable |
| NVDA review-only run represented | Pass | present |
| NVDA blocked promotion has reason | Pass | real_company_promotion_blocked |
| NVDA blocked normalized_csv has reason | Pass | real_company_csv_generation_blocked |
| NVDA blocked v02_dry_run has reason | Pass | real_company_dry_run_blocked |
| NVDA review-only packet has no dry-run | Pass | blocked_or_not_applicable |
| NVDA review-only has no promotion | Pass | blocked_or_not_applicable |
| NVDA review-only has no normalized CSV | Pass | blocked_or_not_applicable |
| AVGO review-only run represented | Pass | present |
| AVGO blocked promotion has reason | Pass | real_company_promotion_blocked |
| AVGO blocked normalized_csv has reason | Pass | real_company_csv_generation_blocked |
| AVGO blocked v02_dry_run has reason | Pass | real_company_dry_run_blocked |
| AVGO review-only packet has no dry-run | Pass | blocked_or_not_applicable |
| AVGO review-only has no promotion | Pass | blocked_or_not_applicable |
| AVGO review-only has no normalized CSV | Pass | blocked_or_not_applicable |
| AVGO real_company_review_only audit completeness | Pass | complete |
| AVGO real_company_review_only packet status | Pass | present |
| AVGO real_company_review_only packet no conclusion fields | Pass | goodluck-stock-research/examples/research_packets/AVGO/review_only_packet.md |
| EXMP fictional_sandbox_full audit completeness | Pass | complete |
| EXMP fictional_sandbox_full packet status | Pass | present |
| EXMP fictional_sandbox_full packet no conclusion fields | Pass | goodluck-stock-research/examples/research_packets/EXMP/full_sandbox_packet.md |
| EXMP fictional_sandbox_partial audit completeness | Pass | complete |
| EXMP fictional_sandbox_partial packet status | Pass | present |
| EXMP fictional_sandbox_partial packet no conclusion fields | Pass | goodluck-stock-research/examples/research_packets/EXMP/partial_sandbox_packet.md |
| MRVL real_company_review_only audit completeness | Pass | complete |
| MRVL real_company_review_only packet status | Pass | present |
| MRVL real_company_review_only packet no conclusion fields | Pass | goodluck-stock-research/examples/research_packets/MRVL/review_only_packet.md |
| NVDA real_company_review_only audit completeness | Pass | complete |
| NVDA real_company_review_only packet status | Pass | present |
| NVDA real_company_review_only packet no conclusion fields | Pass | goodluck-stock-research/examples/research_packets/NVDA/review_only_packet.md |
| EXMP full promotion preserved | Pass | present |
| EXMP partial promotion preserved | Pass | present |
| partial-field run displays downstream impact | Pass | unavailable ratios: 10 |
| partial unresolved count matches dashboard | Pass | dashboard vs manifest |
| partial omitted count matches dashboard | Pass | dashboard vs manifest |
| dashboard has no conclusion fields | Pass | markdown scan |
| blocked matrix covers every real-company forbidden path | Pass | 9/9 pass rows |
