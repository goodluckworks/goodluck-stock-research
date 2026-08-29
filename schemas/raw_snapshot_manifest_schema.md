# Raw Snapshot Manifest Schema

## 1. Purpose

定义 raw evidence snapshot 的不可变记录。Snapshot 是 normalization 的唯一允许来源之一；未来 adapter 不得只保存解析结果而丢弃原始证据。

## 2. Manifest Metadata

- `manifest_version`
- `package_id`
- `created_at`
- `snapshots`

## 3. Snapshot Record

| Field | Required | Meaning |
|---|---:|---|
| `raw_snapshot_id` | Yes | Unique snapshot ID |
| `source_id` | Yes | Source manifest link |
| `original_locator` | Yes | URL or local logical path |
| `local_path` | Yes | Versioned local evidence path |
| `retrieved_at` | Yes | ISO 8601 with timezone |
| `content_type` | Yes | HTML, JSON, CSV, PDF, text, etc. |
| `encoding` | Yes | UTF-8, binary, etc. |
| `byte_size` | Yes | Stored size |
| `checksum_algorithm` | Yes | Recommended SHA-256 |
| `checksum` | Yes | Content checksum |
| `http_or_file_status` | Yes | Future HTTP status or local file read status |
| `immutable` | Yes | Must be true |
| `retention_status` | Yes | retained / metadata_only / restricted |
| `license_or_access_notes` | Yes | Public, restricted, unknown |
| `supersedes_snapshot_id` | Yes | Prior snapshot or not_applicable |
| `notes` | Yes | Capture limitations |

## 4. Path Design

Suggested pattern:

```text
raw/<company>/<source_type>/<retrieved_at>-<source_id>-<checksum-prefix>.<ext>
```

Requirements:

- No silent overwrite.
- Filename alone is not authoritative; checksum and manifest are.
- Same source retrieved later creates a new snapshot.
- Identical bytes may be deduplicated physically, but each retrieval event remains auditable.

## 5. Snapshot Integrity

- Calculate checksum before normalization.
- Recheck checksum before regeneration when feasible.
- Checksum mismatch invalidates dependent normalized files.
- Partial or truncated evidence gets `retention_status=restricted` or an error, not verified.
- Parser output is derived evidence and does not replace raw snapshot.

## 6. Restricted Content

If licensing prevents retention:

- Store metadata and permitted locator only.
- Set `retention_status=metadata_only` or `restricted`.
- State that full reproducibility requires renewed source access.
- Do not commit restricted content.
- Do not store credentials, cookies, tokens or authorization metadata.

## 7. Restatement and Refresh

- Corrected filing or release gets a new snapshot ID.
- `supersedes_snapshot_id` links versions.
- Old snapshot remains retained.
- Dependent normalized files are invalidated, not deleted.

## 8. Examples

```yaml
manifest_version: 0.3-design
package_id: avgo-2026-06-24
created_at: 2026-06-25T12:00:00Z
snapshots:
  - raw_snapshot_id: raw-avgo-2025-10k
    source_id: avgo-2025-10k
    original_locator: https://www.sec.gov/example
    local_path: raw/AVGO/official_filing/20260625T100000Z-avgo-2025-10k-ab12cd34.html
    retrieved_at: 2026-06-25T10:00:00Z
    content_type: text/html
    encoding: UTF-8
    byte_size: 1234567
    checksum_algorithm: sha256
    checksum: ab12cd34example
    http_or_file_status: 200
    immutable: true
    retention_status: retained
    license_or_access_notes: public regulatory filing
    supersedes_snapshot_id: not_applicable
    notes: Filing正文 snapshot
```

## 9. Validation Rules

- `immutable` must be true.
- Local path must be inside approved evidence root.
- Byte size and checksum required for retained content.
- Snapshot/source links must resolve.
- A superseded snapshot cannot be silently deleted.
- Manifest must contain no credentials, investment conclusions or trading instructions.

