# Prototype Mapping Registry

`us_gaap_core_v0_3_7.json` is the current versioned, fixture-oriented registry for the
initial nine fields. It is intentionally marked `prototype_fixture_only` and is
validated by machine-readable schema checks.

The registry:

- Does not claim complete US-GAAP taxonomy coverage.
- Does not authorize first-match selection.
- Requires exact period type, unit and consolidated/no-dimension context.
- Allows only explicitly listed extension tags.
- Treats missing gross profit as unresolved.
- Requires explicit capex sign transformation.
- Blocks total-debt plus component double counting.
- Requires all extracted candidates to remain draft until review.

v0.3.6 adds a separate mapping review workflow. A mapping registry may be used for fictional
promotion only when a matching mapping review batch is `approved` and not `superseded` or
`rejected`. The reviewed artifacts live in `mapping_review_fixtures/` and tracked example output
is generated under `examples/xbrl_mapping_review/`.

v0.3.7 adds relationship metadata to every mapping record:

- concept label and concept type
- taxonomy namespace and fixture taxonomy version
- closest standard concept and anchor concept
- presentation and calculation relationship notes
- relationship confidence, review status and evidence notes

Approved mapping review records must explicitly review relationship evidence. Unsupported or
insufficient relationship metadata blocks mapping approval and downstream promotion.

Any production mapping requires a separate taxonomy-year review and approval. The v0.3.7 approval
fixtures authorize only the offline artificial EXMP promotion path; they do not authorize arbitrary
SEC filing extraction or real-company promotion.
