# Review Fixtures

These JSON files validate the human-review gate against the fictional EXMP
candidate run.

- `exmp_review_approved.json` is the full fictional promotion batch and
  includes approve, adjust, reject and unresolved decisions.
- The smaller adjusted/rejected/unresolved files isolate decision rules.
- `invalid_review_missing_approval.json` is intentionally invalid.

Review fixtures contain no real-company approval. They are regenerated or
updated only when the tracked EXMP candidate manifest changes.
