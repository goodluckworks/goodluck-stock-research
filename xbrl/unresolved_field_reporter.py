#!/usr/bin/env python3
"""Render unresolved-field UX for sandbox manifests and reports."""

from __future__ import annotations

from typing import Any


def bullet_list(values: list[str]) -> str:
    """Render a Markdown bullet list."""
    return "\n".join(f"- `{value}`" for value in values) if values else "- None"


def render_unresolved_section(manifest: dict[str, Any]) -> str:
    """Render a concise unresolved-field section."""
    impact = manifest.get("downstream_impact", {})
    available = impact.get("available_ratios", [])
    unavailable = impact.get("unavailable_ratios", [])
    unavailable_rows = "\n".join(
        "| {ratio} | {missing} | {reason} |".format(
            ratio=item.get("ratio", "unknown"),
            missing=", ".join(f"`{field}`" for field in item.get("missing_inputs", [])),
            reason=item.get("reason", "missing_or_unresolved_inputs"),
        )
        for item in unavailable
    )
    if not unavailable_rows:
        unavailable_rows = "| None | None | None |"
    return f"""## Partial-Field and Unresolved-Field UX

### Populated fields

{bullet_list(list(manifest.get("populated_fields", [])))}

### Omitted fields

{bullet_list(list(manifest.get("omitted_fields", [])))}

### Unresolved fields

{bullet_list(list(manifest.get("unresolved_fields", [])))}

### Blocked fields

{bullet_list(list(manifest.get("blocked_fields", [])))}

### Available ratios

{bullet_list(list(available))}

### Unavailable ratios

| Ratio | Missing inputs | Reason |
|---|---|---|
{unavailable_rows}

### Caution

- Missing, unresolved and blocked fields are left blank. They are never auto-filled with zero.
- Unavailable ratios are disclosed instead of inferred.
"""
