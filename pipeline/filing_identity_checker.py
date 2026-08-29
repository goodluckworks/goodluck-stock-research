#!/usr/bin/env python3
"""Filing identity consistency checks for quarantined real-company drills."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence


IDENTITY_FIELDS = ("ticker", "cik", "accession", "form", "filing_date", "snapshot_sha256")


@dataclass
class IdentityResult:
    status: str
    issues: list[str]
    warnings: list[str]


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return value


def check_identity(payload: dict[str, Any]) -> IdentityResult:
    expected = payload.get("expected_identity") or {}
    artifacts = payload.get("artifacts") or {}
    issues: list[str] = []
    warnings: list[str] = []
    for name, identity in artifacts.items():
        if not isinstance(identity, dict):
            issues.append(f"{name}: identity must be object")
            continue
        for field in IDENTITY_FIELDS:
            if not identity.get(field):
                issues.append(f"{name}: missing {field}")
            elif expected.get(field) and identity.get(field) != expected.get(field):
                issues.append(f"{name}: {field} mismatch")
    if payload.get("claims_latest_effective") is True and payload.get("latest_effective_established") is not True:
        issues.append("latest-effective claim is not established")
    if payload.get("amendment_present") is True:
        warnings.append("amendment present; supersession review required")
    if payload.get("restatement_conflict") is True:
        issues.append("restatement conflict blocks production readiness")
    return IdentityResult("fail" if issues else "pass", issues, warnings)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check filing identity fixture.")
    parser.add_argument("--input", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    result = check_identity(load_json(args.input))
    print(json.dumps({"status": result.status, "issues": result.issues, "warnings": result.warnings}, indent=2))
    return 0 if result.status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
