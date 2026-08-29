#!/usr/bin/env python3
"""Extract draft candidates from a local, artificial XBRL-like HTML fixture."""

from __future__ import annotations

import argparse
import math
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Sequence
import xml.etree.ElementTree as ET

from xbrl_common import (
    ensure_distinct_paths,
    load_json,
    prepare_output_dir,
    relative_or_absolute,
    require_text,
    sha256_file,
    utc_now,
    write_json,
)


PROTOTYPE_VERSION = "v0.3.5"
REVIEW_STATUS = "draft_extracted_unreviewed"
FIXTURE_FORMATS = {"data_attr", "inline_like", "instance_xml", "auto"}
SCOPED_FIELDS = (
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "total_debt",
    "diluted_shares",
)
REQUIRED_OUTPUTS = (
    "extraction_run_manifest.json",
    "extraction_candidates.json",
    "field_provenance.json",
    "unresolved_fields.json",
    "extraction_run_report.md",
)


@dataclass(frozen=True)
class Fact:
    """One artificial fixture fact."""

    fact_id: str
    concept_qname: str
    source_value: str
    numeric_value: float | int
    context_id: str
    period_type: str
    period: str
    unit: str
    dimensions: tuple[str, ...]
    statement: str
    source_locator: str
    split_adjusted: str
    decimals: str
    scale: str


@dataclass(frozen=True)
class Config:
    """Validated extractor inputs."""

    input_file: Path
    mapping_file: Path
    company: str
    ticker: str
    cik: str
    accession: str
    form_type: str
    reporting_period: str
    fiscal_year: str
    fiscal_quarter: str
    currency: str
    amount_unit: str
    per_share_unit: str
    fixture_format: str
    output_dir: Path
    overwrite: bool = False


class FixtureParser(HTMLParser):
    """Parse the documented data-xbrl-* fixture subset."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._active: dict[str, str] | None = None
        self._parts: list[str] = []
        self.raw_facts: list[tuple[dict[str, str], str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        values = {name: value or "" for name, value in attrs}
        if values.get("data-xbrl-concept"):
            if self._active is not None:
                raise ValueError("Nested fixture facts are not supported.")
            self._active = values
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._active is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._active is not None:
            self.raw_facts.append((self._active, "".join(self._parts).strip()))
            self._active = None
            self._parts = []


class InlineLikeParser(HTMLParser):
    """Parse the documented offline inline-XBRL-like fixture subset."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.contexts: dict[str, dict[str, str]] = {}
        self.units: dict[str, str] = {}
        self._active: dict[str, str] | None = None
        self._parts: list[str] = []
        self.raw_facts: list[tuple[dict[str, str], str]] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        tag_name = tag.lower()
        values = {name.lower(): value or "" for name, value in attrs}
        if tag_name in {"xbrli-context", "context"}:
            context_id = values.get("id")
            if context_id:
                self.contexts[context_id] = {
                    "period_type": values.get("data-xbrl-period-type", ""),
                    "period": values.get("data-xbrl-period", ""),
                    "dimensions": values.get("data-xbrl-dimensions", ""),
                }
        elif tag_name in {"xbrli-unit", "unit"}:
            unit_id = values.get("id")
            if unit_id:
                self.units[unit_id] = values.get("measure", "") or values.get(
                    "data-xbrl-measure", ""
                ) or unit_id
        elif tag_name in {"ix-nonfraction", "ix:nonfraction"}:
            if self._active is not None:
                raise ValueError("Nested inline-like facts are not supported.")
            self._active = values
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._active is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self._active is not None and tag.lower() in {
            "ix-nonfraction",
            "ix:nonfraction",
        }:
            self.raw_facts.append((self._active, "".join(self._parts).strip()))
            self._active = None
            self._parts = []


def parse_number(value: str, locator: str) -> float | int:
    """Parse a finite fixture number."""
    cleaned = value.replace(",", "").strip()
    if not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)", cleaned):
        raise ValueError(f"Non-numeric fixture value at {locator}: {value!r}")
    number = float(cleaned)
    if not math.isfinite(number):
        raise ValueError(f"Non-finite fixture value at {locator}.")
    return int(number) if number.is_integer() else number


def fact_from_parts(
    index: int,
    concept_qname: str,
    source_value: str,
    context_id: str,
    period_type: str,
    period: str,
    unit: str,
    dimensions_text: str,
    statement: str,
    locator: str,
    split_adjusted: str = "not_applicable",
    decimals: str = "not_provided",
    scale: str = "not_provided",
) -> Fact:
    """Create one validated fact from parsed fixture fields."""
    dimensions = tuple(
        item.strip() for item in dimensions_text.split("|") if item.strip()
    )
    return Fact(
        fact_id=f"fact-{index:03d}",
        concept_qname=require_text("concept_qname", concept_qname),
        source_value=source_value,
        numeric_value=parse_number(source_value, locator),
        context_id=require_text("context_id", context_id),
        period_type=require_text("period_type", period_type),
        period=require_text("period", period),
        unit=require_text("unit", unit),
        dimensions=dimensions,
        statement=require_text("statement", statement),
        source_locator=require_text("source_locator", locator),
        split_adjusted=split_adjusted.lower(),
        decimals=decimals,
        scale=scale,
    )


def parse_data_attr_facts(path: Path) -> list[Fact]:
    """Parse and validate all local data-xbrl-* fixture facts."""
    parser = FixtureParser()
    parser.feed(path.read_text(encoding="utf-8"))
    facts: list[Fact] = []
    required = (
        "data-xbrl-concept",
        "data-xbrl-context",
        "data-xbrl-period-type",
        "data-xbrl-period",
        "data-xbrl-unit",
        "data-xbrl-dimensions",
        "data-xbrl-statement",
        "data-xbrl-locator",
    )
    for index, (attrs, text) in enumerate(parser.raw_facts, start=1):
        missing = [name for name in required if name not in attrs]
        if missing:
            raise ValueError(f"Fixture fact {index} missing attributes: {missing}")
        facts.append(
            fact_from_parts(
                index=index,
                concept_qname=attrs["data-xbrl-concept"],
                source_value=text,
                context_id=attrs["data-xbrl-context"],
                period_type=attrs["data-xbrl-period-type"],
                period=attrs["data-xbrl-period"],
                unit=attrs["data-xbrl-unit"],
                dimensions_text=attrs["data-xbrl-dimensions"],
                statement=attrs["data-xbrl-statement"],
                locator=attrs["data-xbrl-locator"],
                split_adjusted=attrs.get("data-xbrl-split-adjusted", "not_applicable"),
                decimals=attrs.get("data-xbrl-decimals", "not_provided"),
                scale=attrs.get("data-xbrl-scale", "not_provided"),
            )
        )
    if not facts:
        raise ValueError("No data-xbrl-* facts found in local fixture.")
    return facts


def parse_inline_like_facts(path: Path) -> list[Fact]:
    """Parse the narrow offline inline-like fixture subset."""
    parser = InlineLikeParser()
    text = path.read_text(encoding="utf-8")
    if "http://" in text or "https://" in text:
        raise ValueError("Inline-like fixtures may not contain external URLs.")
    parser.feed(text)
    facts: list[Fact] = []
    for index, (attrs, source_value) in enumerate(parser.raw_facts, start=1):
        required = ("name", "contextref", "unitref", "data-xbrl-statement", "data-xbrl-locator")
        missing = [name for name in required if name not in attrs]
        if missing:
            raise ValueError(f"Inline-like fact {index} missing attributes: {missing}")
        context_id = attrs["contextref"]
        context = parser.contexts.get(context_id)
        if context is None:
            raise ValueError(f"Inline-like fact {index} references missing context: {context_id}")
        unit_ref = attrs["unitref"]
        unit = parser.units.get(unit_ref)
        if unit is None:
            raise ValueError(f"Inline-like fact {index} references missing unit: {unit_ref}")
        facts.append(
            fact_from_parts(
                index=index,
                concept_qname=attrs["name"],
                source_value=source_value,
                context_id=context_id,
                period_type=context["period_type"],
                period=context["period"],
                unit=unit,
                dimensions_text=context["dimensions"],
                statement=attrs["data-xbrl-statement"],
                locator=attrs["data-xbrl-locator"],
                split_adjusted=attrs.get("data-xbrl-split-adjusted", "not_applicable"),
                decimals=attrs.get("decimals", "not_provided"),
                scale=attrs.get("scale", "not_provided"),
            )
        )
    if not facts:
        raise ValueError("No inline-like ix-nonFraction facts found in local fixture.")
    return facts


def parse_instance_xml_facts(path: Path) -> list[Fact]:
    """Parse a minimal artificial instance-document XML subset."""
    text = path.read_text(encoding="utf-8")
    if "http://" in text or "https://" in text:
        raise ValueError("Instance XML fixtures may not contain external URLs.")
    root = ET.fromstring(text)
    contexts: dict[str, dict[str, str]] = {}
    units: dict[str, str] = {}
    for child in root:
        tag = child.tag.split("}")[-1]
        if tag == "context":
            context_id = child.attrib.get("id", "")
            contexts[context_id] = {
                "period_type": child.attrib.get("periodType", ""),
                "period": child.attrib.get("period", ""),
                "dimensions": child.attrib.get("dimensions", ""),
            }
        elif tag == "unit":
            unit_id = child.attrib.get("id", "")
            units[unit_id] = child.attrib.get("measure", "") or unit_id
    facts: list[Fact] = []
    for child in root:
        if child.tag.split("}")[-1] != "fact":
            continue
        index = len(facts) + 1
        context_id = child.attrib.get("contextRef", "")
        unit_ref = child.attrib.get("unitRef", "")
        if context_id not in contexts:
            raise ValueError(f"Instance fact {index} references missing context: {context_id}")
        if unit_ref not in units:
            raise ValueError(f"Instance fact {index} references missing unit: {unit_ref}")
        facts.append(
            fact_from_parts(
                index=index,
                concept_qname=child.attrib.get("concept", ""),
                source_value=(child.text or "").strip(),
                context_id=context_id,
                period_type=contexts[context_id]["period_type"],
                period=contexts[context_id]["period"],
                unit=units[unit_ref],
                dimensions_text=contexts[context_id]["dimensions"],
                statement=child.attrib.get("statement", ""),
                locator=child.attrib.get("locator", ""),
                split_adjusted=child.attrib.get("splitAdjusted", "not_applicable"),
                decimals=child.attrib.get("decimals", "not_provided"),
                scale=child.attrib.get("scale", "not_provided"),
            )
        )
    if not facts:
        raise ValueError("No minimal instance XML facts found in local fixture.")
    return facts


def detect_fixture_format(path: Path) -> str:
    """Detect only documented artificial fixture formats."""
    text = path.read_text(encoding="utf-8")[:4096].lower()
    if "data-xbrl-concept" in text:
        return "data_attr"
    if "ix-nonfraction" in text or "ix:nonfraction" in text:
        return "inline_like"
    if "<xbrl-fixture" in text and "<fact" in text:
        return "instance_xml"
    raise ValueError("Could not auto-detect a documented fixture format.")


def parse_facts(path: Path, fixture_format: str) -> tuple[str, list[Fact]]:
    """Parse local fixture facts by explicit or auto-detected format."""
    selected = detect_fixture_format(path) if fixture_format == "auto" else fixture_format
    if selected == "data_attr":
        return selected, parse_data_attr_facts(path)
    if selected == "inline_like":
        return selected, parse_inline_like_facts(path)
    if selected == "instance_xml":
        return selected, parse_instance_xml_facts(path)
    raise ValueError(f"Unsupported fixture format: {fixture_format}")


def validate_mapping(mapping: dict[str, Any]) -> list[dict[str, Any]]:
    """Validate the fixture-only mapping registry."""
    if mapping.get("review_status") != "prototype_fixture_only":
        raise ValueError("Mapping review_status must be prototype_fixture_only.")
    require_text("mapping_version", mapping.get("mapping_version"))
    records = mapping.get("records")
    if not isinstance(records, list):
        raise ValueError("Mapping records must be an array.")
    fields = [record.get("normalized_field") for record in records]
    if tuple(fields) != SCOPED_FIELDS:
        raise ValueError("Mapping registry must contain the exact nine-field scope.")
    required = {
        "mapping_id",
        "normalized_field",
        "statement",
        "preferred_tags",
        "fallback_tags",
        "extension_tag_allowed",
        "period_type",
        "expected_unit",
        "sign_convention",
        "scale",
        "aggregation_rule",
        "required",
        "candidate_selection_rules",
        "confidence_rules",
        "ambiguity_behavior",
        "review_required",
        "notes",
        "relationship_metadata",
    }
    for record in records:
        if not isinstance(record, dict) or not required <= record.keys():
            raise ValueError("Mapping record is incomplete.")
        if record["ambiguity_behavior"] != "unresolved":
            raise ValueError("Mapping ambiguity behavior must be unresolved.")
        if record["review_required"] is not True:
            raise ValueError("Every mapping must require review.")
    return records


def validate_config(config: Config) -> Config:
    """Validate local-only CLI inputs."""
    input_file = config.input_file.expanduser().resolve()
    mapping_file = config.mapping_file.expanduser().resolve()
    output_dir = config.output_dir.expanduser().resolve()
    if not input_file.is_file():
        raise FileNotFoundError(f"Input fixture does not exist: {input_file}")
    if not mapping_file.is_file():
        raise FileNotFoundError(f"Mapping file does not exist: {mapping_file}")
    ensure_distinct_paths(input_file, mapping_file, output_dir)
    cik = require_text("cik", config.cik)
    if not cik.isdigit():
        raise ValueError("cik must contain digits only.")
    accession = require_text("accession", config.accession)
    return Config(
        input_file=input_file,
        mapping_file=mapping_file,
        company=require_text("company", config.company),
        ticker=require_text("ticker", config.ticker).upper(),
        cik=cik.zfill(10),
        accession=accession,
        form_type=require_text("form_type", config.form_type).upper(),
        reporting_period=require_text(
            "reporting_period", config.reporting_period
        ),
        fiscal_year=require_text("fiscal_year", config.fiscal_year),
        fiscal_quarter=require_text("fiscal_quarter", config.fiscal_quarter),
        currency=require_text("currency", config.currency),
        amount_unit=require_text("amount_unit", config.amount_unit),
        per_share_unit=require_text("per_share_unit", config.per_share_unit),
        fixture_format=require_text("fixture_format", config.fixture_format),
        output_dir=output_dir,
        overwrite=config.overwrite,
    )


def expected_unit(mapping: dict[str, Any], currency: str) -> str:
    """Resolve mapping unit aliases."""
    return currency if mapping["expected_unit"] == "currency" else mapping["expected_unit"]


def default_review_checklist(candidate_id: str, has_competing: bool = False) -> dict[str, Any]:
    """Return a default reviewer checklist placeholder."""
    return {
        "checklist_schema_version": "v0.3.7",
        "candidate_id": candidate_id,
        "period_checked": False,
        "unit_checked": False,
        "context_checked": False,
        "dimensions_checked": False,
        "sign_checked": False,
        "scale_checked": False,
        "relationship_checked": False,
        "competing_candidates_checked": not has_competing,
        "prior_period_checked": False,
        "materiality_checked": False,
        "reviewer_notes_present": False,
    }


def relationship_metadata(mapping: dict[str, Any], fact: Fact | None = None) -> dict[str, Any]:
    """Return fixture-level relationship metadata for a mapping/fact pair."""
    base = dict(mapping.get("relationship_metadata", {}))
    if not base:
        base = {
            "relationship_id": f"relationship-{mapping['mapping_id']}",
            "concept_qname": fact.concept_qname if fact else "unresolved",
            "concept_label": mapping["normalized_field"],
            "concept_type": "fixture_local",
            "taxonomy_namespace": "fixture",
            "taxonomy_version": "unreviewed_fixture",
            "closest_standard_concept": "unresolved",
            "presentation_parent": "unresolved",
            "presentation_children": [],
            "calculation_parent": "unresolved",
            "calculation_children": [],
            "anchor_concept": "unresolved",
            "relationship_basis": "No relationship metadata supplied by mapping registry.",
            "relationship_confidence": "missing",
            "relationship_evidence_notes": "Missing relationship metadata blocks approval readiness.",
            "relationship_review_status": "needs_more_evidence",
        }
    if fact is not None:
        base["concept_qname"] = fact.concept_qname
        if not fact.concept_qname.startswith("us-gaap:"):
            base["concept_type"] = "extension" if not fact.concept_qname.startswith("fixture:") else "fixture_local"
            if base.get("anchor_concept") in {"unresolved", "not_applicable", ""}:
                base["relationship_confidence"] = "missing"
                base["relationship_review_status"] = "needs_more_evidence"
    return base


def classify_fact(
    fact: Fact, mapping: dict[str, Any], config: Config
) -> list[str]:
    """Return reasons a fact cannot be a candidate."""
    reasons: list[str] = []
    allowed_tags = mapping["preferred_tags"] + mapping["fallback_tags"]
    if fact.concept_qname not in allowed_tags:
        reasons.append("tag_not_mapped")
    if (
        not fact.concept_qname.startswith("us-gaap:")
        and fact.concept_qname in allowed_tags
        and not mapping["extension_tag_allowed"]
    ):
        reasons.append("extension_tag_not_allowed")
    if fact.statement != mapping["statement"]:
        reasons.append("wrong_statement")
    if fact.period_type != mapping["period_type"]:
        reasons.append("wrong_period_type")
    if fact.period != config.reporting_period:
        reasons.append("wrong_period")
    if fact.unit != expected_unit(mapping, config.currency):
        reasons.append("wrong_unit")
    if fact.dimensions:
        reasons.append("dimension_conflict")
    if (
        mapping["normalized_field"] == "diluted_shares"
        and fact.split_adjusted != "true"
    ):
        reasons.append("split_basis_unverified")
    return reasons


def candidate_from_fact(
    fact: Fact,
    mapping: dict[str, Any],
    config: Config,
    candidate_id: str,
) -> dict[str, Any]:
    """Create one draft candidate."""
    preferred = fact.concept_qname in mapping["preferred_tags"]
    extracted: float | int = fact.numeric_value
    transformation = "identity"
    warnings: list[str] = []
    if mapping["normalized_field"] == "capital_expenditure":
        extracted = abs(fact.numeric_value)
        transformation = "absolute_value_to_positive_outflow"
        warnings.append("source_sign_preserved_in_source_value")
    if not preferred:
        warnings.append("fallback_or_extension_tag_requires_review")
    if "material change" in fact.source_locator.lower() or "material_change" in fact.source_locator.lower():
        warnings.append("material_change_threshold_review_required")
    if config.ticker in {"MRVL", "NVDA", "AVGO"}:
        warnings.append("synthetic_real_company_fixture_unverified")
    has_competing = False
    return {
        "candidate_id": candidate_id,
        "normalized_field": mapping["normalized_field"],
        "extracted_value": extracted,
        "source_value": fact.source_value,
        "unit": (
            config.amount_unit
            if mapping["expected_unit"] == "currency"
            else "million shares"
        ),
        "source_unit": fact.unit,
        "period": fact.period,
        "concept_qname": fact.concept_qname,
        "context_id": fact.context_id,
        "period_type": fact.period_type,
        "dimensions": list(fact.dimensions),
        "source_locator": fact.source_locator,
        "source_fact_ids": [fact.fact_id],
        "xbrl_decimals": fact.decimals,
        "xbrl_scale": fact.scale,
        "transformation": transformation,
        "confidence": "high" if preferred else "medium",
        "warning_flags": warnings,
        "competing_candidate_ids": [],
        "review_status": REVIEW_STATUS,
        "taxonomy_relationship": relationship_metadata(mapping, fact),
        "review_checklist": default_review_checklist(candidate_id, has_competing),
    }


def select_field(
    facts: list[Fact],
    mapping: dict[str, Any],
    config: Config,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None, list[dict[str, Any]]]:
    """Select one field candidate or return a structured unresolved result."""
    mapped_tags = set(mapping["preferred_tags"] + mapping["fallback_tags"])
    relevant = [fact for fact in facts if fact.concept_qname in mapped_tags]
    rejected: list[dict[str, Any]] = []
    valid: list[Fact] = []
    for fact in relevant:
        reasons = classify_fact(fact, mapping, config)
        if reasons:
            rejected.append(
                {
                    "fact_id": fact.fact_id,
                    "concept_qname": fact.concept_qname,
                    "context_id": fact.context_id,
                    "source_locator": fact.source_locator,
                    "reasons": reasons,
                }
            )
        else:
            valid.append(fact)

    field = mapping["normalized_field"]
    if field == "total_debt" and valid:
        preferred = [
            fact for fact in valid if fact.concept_qname in mapping["preferred_tags"]
        ]
        components = [
            fact for fact in valid if fact.concept_qname in mapping["fallback_tags"]
        ]
        if preferred and components:
            return None, unresolved(
                field,
                "debt_double_count_risk",
                "A total-debt fact and debt components coexist; the prototype will not combine or choose between them.",
                valid,
                rejected,
            ), rejected
        if not preferred and components:
            concepts = {fact.concept_qname for fact in components}
            if concepts != set(mapping["fallback_tags"]) or len(components) != 2:
                return None, unresolved(
                    field,
                    "incomplete_or_competing_debt_components",
                    "Debt components are incomplete or duplicated.",
                    valid,
                    rejected,
                ), rejected
            candidate_id = f"{config.ticker.lower()}-{field}-candidate-001"
            value = sum(float(fact.numeric_value) for fact in components)
            if value.is_integer():
                value = int(value)
            candidate = {
                "candidate_id": candidate_id,
                "normalized_field": field,
                "extracted_value": value,
                "source_value": [fact.source_value for fact in components],
                "unit": config.amount_unit,
                "source_unit": config.currency,
                "period": config.reporting_period,
                "concept_qname": "sum:" + "+".join(sorted(concepts)),
                "context_id": "+".join(fact.context_id for fact in components),
                "period_type": "instant",
                "dimensions": [],
                "source_locator": " + ".join(
                    fact.source_locator for fact in components
                ),
                "source_fact_ids": [fact.fact_id for fact in components],
                "xbrl_decimals": "multiple",
                "xbrl_scale": "multiple",
                "transformation": "sum_non_overlapping_debt_components",
                "confidence": "medium",
                "warning_flags": ["component_scope_requires_review"],
                "competing_candidate_ids": [],
                "review_status": REVIEW_STATUS,
                "taxonomy_relationship": relationship_metadata(mapping, components[0]),
                "review_checklist": default_review_checklist(candidate_id),
            }
            return candidate, None, rejected

    if not valid:
        reason_code = "missing_field" if not relevant else "no_eligible_fact"
        reason = (
            "No mapped fact was present."
            if not relevant
            else "Mapped facts failed period, unit, statement, dimension or split-basis checks."
        )
        return None, unresolved(
            field, reason_code, reason, relevant, rejected
        ), rejected
    if len(valid) > 1:
        ids = [
            f"{config.ticker.lower()}-{field}-competing-{index:03d}"
            for index, _ in enumerate(valid, start=1)
        ]
        item = unresolved(
            field,
            "multiple_candidates",
            "Multiple eligible facts remain; first-match selection is prohibited.",
            valid,
            rejected,
        )
        item["competing_candidate_ids"] = ids
        return None, item, rejected

    candidate_id = f"{config.ticker.lower()}-{field}-candidate-001"
    return (
        candidate_from_fact(valid[0], mapping, config, candidate_id),
        None,
        rejected,
    )


def unresolved(
    field: str,
    code: str,
    reason: str,
    facts: list[Fact],
    rejected: list[dict[str, Any]],
) -> dict[str, Any]:
    """Create a structured unresolved record."""
    return {
        "normalized_field": field,
        "reason_code": code,
        "reason": reason,
        "source_fact_ids": [fact.fact_id for fact in facts],
        "rejected_facts": rejected,
        "competing_candidate_ids": [],
        "review_required": True,
        "suggested_action": "Review fixture facts, mapping and context manually.",
    }


def fixture_data_status(config: Config) -> str:
    """Return explicit fixture data status for manifest and report."""
    if "real_excerpt_drills" in str(config.input_file):
        return "real_filing_excerpt_drill"
    if config.ticker == "EXMP":
        return "fictional_sample"
    return "synthetic_unverified_real_company_shape"


def run(config: Config) -> dict[str, Path]:
    """Run offline extraction and write the evidence contract."""
    config = validate_config(config)
    if config.fixture_format not in FIXTURE_FORMATS:
        raise ValueError(f"fixture_format must be one of {sorted(FIXTURE_FORMATS)}.")
    overwrite_used = prepare_output_dir(config.output_dir, config.overwrite)
    mapping_doc = load_json(config.mapping_file)
    records = validate_mapping(mapping_doc)
    resolved_fixture_format, facts = parse_facts(config.input_file, config.fixture_format)
    input_sha = sha256_file(config.input_file)
    mapping_sha = sha256_file(config.mapping_file)
    run_id = (
        f"xbrl-{config.ticker.lower()}-{config.reporting_period.lower()}-"
        f"{input_sha[:12]}"
    )

    candidates: list[dict[str, Any]] = []
    unresolved_fields: list[dict[str, Any]] = []
    rejected_facts: list[dict[str, Any]] = []
    for mapping in records:
        candidate, unresolved_item, rejected = select_field(
            facts, mapping, config
        )
        rejected_facts.extend(
            {"normalized_field": mapping["normalized_field"], **item}
            for item in rejected
        )
        if candidate is not None:
            candidates.append(candidate)
        if unresolved_item is not None:
            unresolved_fields.append(unresolved_item)

    candidate_ids = {item["candidate_id"] for item in candidates}
    provenance_records = [
        {
            "record_id": f"provenance-{candidate['candidate_id']}",
            "candidate_id": candidate["candidate_id"],
            "normalized_field": candidate["normalized_field"],
            "snapshot_sha256": input_sha,
            "mapping_version": mapping_doc["mapping_version"],
            "source_fact_ids": candidate["source_fact_ids"],
            "source_locator": candidate["source_locator"],
            "concept_qname": candidate["concept_qname"],
            "context_id": candidate["context_id"],
            "period": candidate["period"],
            "unit": candidate["unit"],
            "transformation": candidate["transformation"],
            "confidence": candidate["confidence"],
            "review_status": REVIEW_STATUS,
        }
        for candidate in candidates
    ]
    assert candidate_ids == {
        item["candidate_id"] for item in provenance_records
    }

    paths = {name: config.output_dir / name for name in REQUIRED_OUTPUTS}
    data_status = fixture_data_status(config)
    manifest = {
        "run_id": run_id,
        "prototype_version": PROTOTYPE_VERSION,
        "mode": "offline_fixture_only",
        "fixture_format": resolved_fixture_format,
        "company": config.company,
        "ticker": config.ticker,
        "cik": config.cik,
        "accession": config.accession,
        "form_type": config.form_type,
        "reporting_period": config.reporting_period,
        "fiscal_year": config.fiscal_year,
        "fiscal_quarter": config.fiscal_quarter,
        "currency": config.currency,
        "amount_unit": config.amount_unit,
        "per_share_unit": config.per_share_unit,
        "input_file": relative_or_absolute(config.input_file),
        "snapshot_sha256": input_sha,
        "mapping_file": relative_or_absolute(config.mapping_file),
        "mapping_sha256": mapping_sha,
        "mapping_version": mapping_doc["mapping_version"],
        "mapping_review_status": mapping_doc["review_status"],
        "generated_at": utc_now(),
        "candidate_count": len(candidates),
        "unresolved_count": len(unresolved_fields),
        "review_status": REVIEW_STATUS,
        "fixture_data_status": data_status,
        "overwrite_used": overwrite_used,
        "output_files": list(REQUIRED_OUTPUTS),
        "boundaries": [
            "local fixture only",
            "fixture parser subset only",
            "no network",
            "draft candidates only",
            "no normalized financial output",
            "no investment conclusion",
        ],
    }
    candidate_doc = {
        "run_id": run_id,
        "mapping_version": mapping_doc["mapping_version"],
        "snapshot_sha256": input_sha,
        "review_status": REVIEW_STATUS,
        "candidates": candidates,
    }
    provenance_doc = {
        "run_id": run_id,
        "snapshot_sha256": input_sha,
        "mapping_version": mapping_doc["mapping_version"],
        "records": provenance_records,
    }
    unresolved_doc = {
        "run_id": run_id,
        "unresolved_fields": unresolved_fields,
        "rejected_facts": rejected_facts,
        "warnings": [
            "Fixture-oriented prototype; not production iXBRL coverage.",
            "All candidates require human review.",
        ],
    }
    report = f"""# Offline XBRL Candidate Extraction Run

## Summary

- Run ID: `{run_id}`
- Company: `{config.company}`
- Ticker: `{config.ticker}`
- Mode: `offline_fixture_only`
- Fixture format: `{resolved_fixture_format}`
- Input: `{relative_or_absolute(config.input_file)}`
- Input SHA-256: `{input_sha}`
- Mapping version: `{mapping_doc['mapping_version']}`
- Mapping status: `{mapping_doc['review_status']}`
- Candidate count: `{len(candidates)}`
- Unresolved field count: `{len(unresolved_fields)}`
- Rejected fixture fact count: `{len(rejected_facts)}`
- Review status: `{REVIEW_STATUS}`
- Fixture data status: `{data_status}`
- Overwrite used: `{str(overwrite_used).lower()}`

## Output Files

{chr(10).join(f"- `{name}`" for name in REQUIRED_OUTPUTS)}

## Boundaries

- Local artificial fixture only; no URL access.
- Parser subset is limited to documented local fixtures; this is not production iXBRL parsing.
- Candidate extraction only; no approved normalized output.
- Every candidate requires human review.
- No downstream calculation or investment conclusion is produced.
"""
    write_json(paths["extraction_run_manifest.json"], manifest)
    write_json(paths["extraction_candidates.json"], candidate_doc)
    write_json(paths["field_provenance.json"], provenance_doc)
    write_json(paths["unresolved_fields.json"], unresolved_doc)
    paths["extraction_run_report.md"].write_text(report, encoding="utf-8")
    return paths


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Extract draft candidates from one local artificial XBRL-like fixture."
    )
    parser.add_argument("--input-file", required=True, type=Path)
    parser.add_argument("--mapping-file", required=True, type=Path)
    parser.add_argument("--company", required=True)
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--cik", required=True)
    parser.add_argument("--accession", required=True)
    parser.add_argument("--form-type", required=True)
    parser.add_argument("--reporting-period", required=True)
    parser.add_argument("--fiscal-year", required=True)
    parser.add_argument("--fiscal-quarter", required=True)
    parser.add_argument("--currency", required=True)
    parser.add_argument("--amount-unit", required=True)
    parser.add_argument("--per-share-unit", required=True)
    parser.add_argument(
        "--fixture-format",
        choices=sorted(FIXTURE_FORMATS),
        default="auto",
        help="Documented local fixture format; auto only detects artificial fixtures.",
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run CLI."""
    args = parse_args(argv)
    try:
        paths = run(
            Config(
                input_file=args.input_file,
                mapping_file=args.mapping_file,
                company=args.company,
                ticker=args.ticker,
                cik=args.cik,
                accession=args.accession,
                form_type=args.form_type,
                reporting_period=args.reporting_period,
                fiscal_year=args.fiscal_year,
                fiscal_quarter=args.fiscal_quarter,
                currency=args.currency,
                amount_unit=args.amount_unit,
                per_share_unit=args.per_share_unit,
                fixture_format=args.fixture_format,
                output_dir=args.output_dir,
                overwrite=args.overwrite,
            )
        )
    except (FileNotFoundError, FileExistsError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"Wrote offline XBRL candidate package: {args.output_dir}")
    for path in paths.values():
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
