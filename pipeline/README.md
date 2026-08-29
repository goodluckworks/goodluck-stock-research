# Review-Gated Offline Pipeline

`pipeline/` contains the v0.4 review-gated offline pipeline for the stock research skill. It is offline, fixture-first and review-gated.

## Modes

- `fictional_sandbox_full`: EXMP fictional end-to-end sandbox path.
- `fictional_sandbox_partial`: EXMP fictional partial-field sandbox path.
- `real_company_review_only`: MRVL / NVDA / AVGO review-only path; no promotion, no CSV, no dry-run.
- `blocked_real_company_promotion_attempt`: records blocked promotion / CSV / dry-run attempts for MRVL / NVDA / AVGO.
- `controlled_real_company_sandbox`: v0.6 explicit, allowlisted and quarantined MRVL-only sandbox drill.

## Boundary

- Local files only.
- No live extraction.
- No production parser claim.
- No default real-company promotion.
- No default real-company normalized CSV.
- No default real-company v0.2.x dry-run.
- v0.6 MRVL controlled sandbox output is quarantined only, not production data, not investment data, not company fact until verified, and not for trading.
- No target price, buy/sell/hold, position size, research status or trading action.

## Example

```bash
python3 goodluck-stock-research/pipeline/pipeline_orchestrator.py \
  --mode fictional_sandbox_full \
  --ticker EXMP \
  --company "Example Semiconductor Corp." \
  --output-dir goodluck-stock-research/examples/pipeline_runs/EXMP/full \
  --overwrite
```

## Packet Builder

```bash
python3 goodluck-stock-research/pipeline/research_packet_builder.py \
  --run-dir goodluck-stock-research/examples/pipeline_runs/EXMP/full \
  --output-md goodluck-stock-research/examples/research_packets/EXMP/full_sandbox_packet.md \
  --overwrite
```

## Audit Dashboard

```bash
python3 goodluck-stock-research/pipeline/pipeline_audit_dashboard.py \
  --pipeline-root goodluck-stock-research/examples/pipeline_runs \
  --packet-root goodluck-stock-research/examples/research_packets \
  --output-dir goodluck-stock-research/examples/pipeline_audit_dashboard \
  --overwrite
```

See `references/v0.4-review-gated-pipeline.md` for the full policy.

## Controlled Real-Company Sandbox

```bash
python3 goodluck-stock-research/pipeline/controlled_real_company_sandbox_gate.py \
  --mode controlled_real_company_sandbox \
  --allow-real-company-sandbox \
  --ticker MRVL \
  --quarantine-output \
  --review-batch goodluck-stock-research/examples/real_company_quarantine/MRVL/approval_inputs/review_batch_approved_for_quarantine.json \
  --quality-score goodluck-stock-research/examples/real_company_quarantine/MRVL/approval_inputs/quality_score_ready_for_quarantine.json \
  --candidate-package goodluck-stock-research/examples/pipeline_runs/MRVL/review_only/candidate/extraction_candidates.json \
  --approval-policy goodluck-stock-research/examples/real_company_quarantine/MRVL/approval_inputs/approval_policy.json \
  --output-dir goodluck-stock-research/examples/real_company_quarantine/MRVL
```

This generates quarantined MRVL sandbox artifacts only. It does not permit NVDA/AVGO tracked quarantine output and does not run DCF, peer comps, implied expectations or full research reports.

See `references/v0.6-controlled-real-company-sandbox.md` for the v0.6 policy.
