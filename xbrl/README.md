# Offline XBRL Candidate Prototype

v0.4 keeps the XBRL layer as an offline, fixture-first candidate extraction prototype with
machine-readable package schemas, standard-library validation, and package
audit. It adds mapping review workflow, reviewer workbench generation, review
quality scoring, checklist-aware decision collection, taxonomy relationship
metadata, stricter promotion isolation, a fictional-only normalized CSV sandbox,
an EXMP-only v0.2.x ratio dry-run wrapper, an end-to-end offline pipeline
auditor and a higher-level review-gated pipeline under `pipeline/`. It parses only the documented local fixture subsets in `fixtures/README.md`:
`data_attr`, `inline_like`, and minimal `instance_xml`. It is not a production
iXBRL parser and does not read live SEC URLs.

v0.6 adds a controlled real-company sandbox gate outside the XBRL extraction layer. It consumes local review/candidate/quality artifacts and can generate one quarantined MRVL sandbox drill. It is not production extraction and does not change the XBRL parser boundary.

Workflow:

```text
local fixture
  -> draft extraction candidates
  -> schema validation
  -> mapping review
  -> reviewer workbench
  -> review quality score
  -> review decision collection
  -> human review validation
  -> package audit
  -> fictional-only approved normalized draft
  -> EXMP-only normalized CSV sandbox
  -> EXMP-only ratio_calculator dry-run
  -> end-to-end offline audit
  -> optional v0.6 MRVL quarantined sandbox gate
```

## Commands

Candidate extraction:

```bash
python3 goodluck-stock-research/xbrl/offline_xbrl_candidate_extractor.py \
  --input-file goodluck-stock-research/xbrl/fixtures/mrvl_candidate_fixture.html \
  --mapping-file goodluck-stock-research/xbrl/mappings/us_gaap_core_v0_3_7.json \
  --company "Marvell Technology, Inc." \
  --ticker MRVL \
  --cik 1835632 \
  --accession 0001835632-26-000011 \
  --form-type 10-K \
  --reporting-period FY2026 \
  --fiscal-year 2026 \
  --fiscal-quarter FY \
  --currency USD \
  --amount-unit "USD millions" \
  --per-share-unit "USD/share" \
  --fixture-format auto \
  --output-dir /private/tmp/xbrl-candidates/MRVL
```

Schema validation:

```bash
python3 goodluck-stock-research/xbrl/schema_validator.py \
  --schema-dir goodluck-stock-research/xbrl/schemas \
  --input-dir goodluck-stock-research/examples/xbrl_extraction_runs/EXMP \
  --output-report /private/tmp/exmp-package-schema.md
```

Review validation:

```bash
python3 goodluck-stock-research/xbrl/extraction_review_validator.py \
  --review-file goodluck-stock-research/xbrl/review_fixtures/exmp_review_approved.json \
  --candidate-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_candidates.json \
  --manifest-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_run_manifest.json \
  --output-report /private/tmp/exmp-review-validation.md
```

Mapping review:

```bash
python3 goodluck-stock-research/xbrl/mapping_review.py \
  --mapping-file goodluck-stock-research/xbrl/mappings/us_gaap_core_v0_3_7.json \
  --review-file goodluck-stock-research/xbrl/mapping_review_fixtures/mapping_review_approved_v0_3_7.json \
  --output-dir /private/tmp/exmp-mapping-review \
  --overwrite
```

Reviewer workbench:

```bash
python3 goodluck-stock-research/xbrl/reviewer_workbench.py \
  --candidate-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_candidates.json \
  --manifest-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_run_manifest.json \
  --provenance-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/field_provenance.json \
  --output-workbench /private/tmp/exmp-workbench/review_workbench.md \
  --output-decision-template /private/tmp/exmp-workbench/review_decision_template.json
```

Review quality scoring:

```bash
python3 goodluck-stock-research/xbrl/review_quality_scorer.py \
  --candidate-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_candidates.json \
  --manifest-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_run_manifest.json \
  --provenance-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/field_provenance.json \
  --output-dir /private/tmp/exmp-review-quality \
  --overwrite
```

Review decision collection:

```bash
python3 goodluck-stock-research/xbrl/review_decision_collector.py \
  --decision-file /private/tmp/exmp-workbench/review_decision_template.json \
  --candidate-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_candidates.json \
  --manifest-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_run_manifest.json \
  --quality-score-file /private/tmp/exmp-review-quality/review_quality_score.json \
  --output-dir /private/tmp/exmp-review-decisions \
  --overwrite
```

Fictional promotion:

```bash
python3 goodluck-stock-research/xbrl/promote_reviewed_fields.py \
  --review-file /private/tmp/exmp-review-decisions/normalized_review_batch.json \
  --candidate-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_candidates.json \
  --manifest-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_run_manifest.json \
  --mapping-file goodluck-stock-research/xbrl/mappings/us_gaap_core_v0_3_7.json \
  --mapping-review-file goodluck-stock-research/xbrl/mapping_review_fixtures/mapping_review_approved_v0_3_7.json \
  --review-decision-log-file /private/tmp/exmp-review-decisions/review_decision_log.json \
  --quality-score-file /private/tmp/exmp-review-quality/review_quality_score.json \
  --package-audit-reference /private/tmp/exmp-package-audit.md \
  --output-dir /private/tmp/exmp-promotion
```

Package audit:

```bash
python3 goodluck-stock-research/xbrl/package_auditor.py \
  --extraction-dir goodluck-stock-research/examples/xbrl_extraction_runs/EXMP \
  --review-file goodluck-stock-research/examples/xbrl_review_decisions/EXMP/normalized_review_batch.json \
  --promotion-dir goodluck-stock-research/examples/xbrl_promotion_runs/EXMP \
  --mapping-file goodluck-stock-research/xbrl/mappings/us_gaap_core_v0_3_7.json \
  --mapping-review-file goodluck-stock-research/xbrl/mapping_review_fixtures/mapping_review_approved_v0_3_7.json \
  --review-decision-log-file goodluck-stock-research/examples/xbrl_review_decisions/EXMP/review_decision_log.json \
  --quality-score-file goodluck-stock-research/examples/xbrl_review_quality/EXMP/review_quality_score.json \
  --output-report /private/tmp/exmp-package-audit.md
```

Fictional normalized CSV sandbox:

```bash
python3 goodluck-stock-research/xbrl/generate_normalized_csv_sandbox.py \
  --promotion-dir goodluck-stock-research/examples/xbrl_promotion_runs/EXMP \
  --review-file goodluck-stock-research/examples/xbrl_review_decisions/EXMP/normalized_review_batch.json \
  --candidate-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_candidates.json \
  --manifest-file goodluck-stock-research/examples/xbrl_extraction_runs/EXMP/extraction_run_manifest.json \
  --output-dir /private/tmp/exmp-normalized-sandbox
```

EXMP-only v0.2.x ratio dry-run:

```bash
python3 goodluck-stock-research/xbrl/run_v02_sandbox_dry_run.py \
  --input-csv /private/tmp/exmp-normalized-sandbox/normalized_financials_sandbox.csv \
  --output-dir /private/tmp/exmp-v02-dry-run
```

End-to-end pipeline audit:

```bash
python3 goodluck-stock-research/xbrl/end_to_end_pipeline_auditor.py \
  --candidate-dir goodluck-stock-research/examples/xbrl_extraction_runs/EXMP \
  --quality-dir goodluck-stock-research/examples/xbrl_review_quality/EXMP \
  --review-dir goodluck-stock-research/examples/xbrl_review_decisions/EXMP \
  --promotion-dir goodluck-stock-research/examples/xbrl_promotion_runs/EXMP \
  --normalized-dir goodluck-stock-research/examples/xbrl_normalized_sandbox/EXMP \
  --dry-run-dir goodluck-stock-research/examples/xbrl_v02_dry_runs/EXMP \
  --output-report /private/tmp/exmp-end-to-end-audit.md
```

Boundaries:

- Standard library only.
- Local files only; no network or environment credentials.
- Draft candidates only for MRVL, NVDA and AVGO.
- Fictional EXMP is the only promotion example.
- Fictional EXMP is the only normalized CSV sandbox and ratio dry-run example.
- Promotion requires approved mapping review, normalized review batch, ready review quality score, review decision log and package audit reference.
- Real ticker promotion is blocked by default. The override flag exists only
  as an explicit future gate and is not used by v0.3.8 tests or examples.
- Real-filing excerpt drills are short, offline, not complete filings and never promoted.
- No real-company v0.2.x CSV generation or calculation-script invocation.
- Promotion never calls v0.2.x scripts; dry-run is a separate explicit command.
- No DCF, peer comps or implied expectations dry-run in v0.3.8.
- No target price, recommendation, position, broker or trading output.
- No production iXBRL parser claim.
- No real-company approved normalized input or production populated CSV generation.
- v0.4 pipeline orchestration does not change XBRL boundaries; it only links local review-gated outputs.
- v0.6 MRVL quarantine output is explicitly not production data, not investment data, not company fact until verified and not for trading.
- NVDA/AVGO remain blocked from tracked quarantine output by default.

See:

- `mappings/README.md`
- `fixtures/README.md`
- `review_fixtures/README.md`
- `tests/README.md`
- `references/v0.3.4-prototype-decisions.md`
- `references/v0.3.5-prototype-decisions.md`
- `references/v0.3.6-prototype-decisions.md`
- `references/v0.3.7-prototype-decisions.md`
- `references/v0.3.8-prototype-decisions.md`
- `references/v0.3.9-partial-field-decisions.md`
- `references/v0.4-review-gated-pipeline.md`
- `references/v0.6-controlled-real-company-sandbox.md`
- `references/promotion-isolation-policy.md`
