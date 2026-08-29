#!/usr/bin/env python3
"""Generate an auditable simplified DCF sensitivity report from local JSON."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


REQUIRED_FIELDS = [
    "company",
    "ticker",
    "currency",
    "amount_unit",
    "per_share_unit",
    "reporting_period",
    "basis",
    "fcf_type",
    "base_year_fcf",
    "projection_years",
    "revenue_or_fcf_growth_cases",
    "discount_rates",
    "terminal_growth_rates",
    "net_debt",
    "diluted_shares",
    "source",
    "source_date",
    "source_status",
]

CASE_NAMES = ("bear", "base", "bull")
FCF_TYPES = ("FCFF", "UFCF", "FCFE")
DISCLAIMER = (
    "仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。"
)


def is_finite_number(value: object) -> bool:
    """Return True for finite int/float values, excluding booleans."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a simplified DCF sensitivity report from local JSON."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input JSON path.")
    parser.add_argument("--output", required=True, type=Path, help="Output Markdown path.")
    return parser.parse_args()


def load_assumptions(path: Path) -> dict[str, Any]:
    """Load and validate DCF assumptions."""
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Input JSON must contain one object.")

    missing = [field for field in REQUIRED_FIELDS if field not in data]
    if missing:
        raise ValueError(
            "Input JSON is missing required field(s): " + ", ".join(missing)
        )

    text_fields = [
        "company",
        "ticker",
        "currency",
        "amount_unit",
        "per_share_unit",
        "reporting_period",
        "basis",
        "fcf_type",
        "source",
        "source_date",
        "source_status",
    ]
    for field in text_fields:
        if not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"Field '{field}' must be a non-empty string.")
    data["fcf_type"] = data["fcf_type"].upper()
    if data["fcf_type"] not in FCF_TYPES:
        raise ValueError(
            "Field 'fcf_type' must be one of: " + ", ".join(FCF_TYPES) + "."
        )

    numeric_fields = ["base_year_fcf", "net_debt", "diluted_shares"]
    for field in numeric_fields:
        if not is_finite_number(data[field]):
            raise ValueError(f"Field '{field}' must be a finite number.")

    years = data["projection_years"]
    if not isinstance(years, int) or isinstance(years, bool) or years <= 0:
        raise ValueError("Field 'projection_years' must be a positive integer.")
    if data["diluted_shares"] <= 0:
        raise ValueError("Field 'diluted_shares' must be greater than zero.")

    cases = data["revenue_or_fcf_growth_cases"]
    if not isinstance(cases, dict):
        raise ValueError("Field 'revenue_or_fcf_growth_cases' must be an object.")
    for case in CASE_NAMES:
        rates = cases.get(case)
        if not isinstance(rates, list):
            raise ValueError(f"Growth case '{case}' must be a list.")
        if len(rates) != years:
            raise ValueError(
                f"Growth case '{case}' must contain {years} annual rates."
            )
        if not all(is_finite_number(rate) for rate in rates):
            raise ValueError(f"Growth case '{case}' contains a non-finite rate.")
        if any(rate < -1 for rate in rates):
            raise ValueError(
                f"Growth case '{case}' cannot contain a rate below -100%."
            )

    for field in ("discount_rates", "terminal_growth_rates"):
        rates = data[field]
        if not isinstance(rates, list) or not rates:
            raise ValueError(f"Field '{field}' must be a non-empty list.")
        if not all(is_finite_number(rate) for rate in rates):
            raise ValueError(f"Field '{field}' contains a non-finite rate.")

    if any(rate <= -1 for rate in data["discount_rates"]):
        raise ValueError("Every discount rate must be greater than -100%.")
    if any(rate <= -1 for rate in data["terminal_growth_rates"]):
        raise ValueError("Every terminal growth rate must be greater than -100%.")

    for discount_rate in data["discount_rates"]:
        for terminal_growth in data["terminal_growth_rates"]:
            if discount_rate <= terminal_growth:
                raise ValueError(
                    "Every discount rate must be greater than every terminal growth rate."
                )
    return data


def project_fcf(base_fcf: float, growth_rates: list[float]) -> list[float]:
    """Project FCF by applying each annual growth rate sequentially."""
    values: list[float] = []
    current = base_fcf
    for rate in growth_rates:
        current *= 1 + rate
        values.append(current)
    return values


def dcf_value(
    projected_fcf: list[float],
    discount_rate: float,
    terminal_growth_rate: float,
    net_debt: float,
    diluted_shares: float,
    fcf_type: str,
) -> dict[str, Optional[float]]:
    """Calculate value using the bridge appropriate for the supplied FCF type."""
    terminal_value = (
        projected_fcf[-1]
        * (1 + terminal_growth_rate)
        / (discount_rate - terminal_growth_rate)
    )
    pv_explicit = sum(
        fcf / ((1 + discount_rate) ** year)
        for year, fcf in enumerate(projected_fcf, start=1)
    )
    pv_terminal = terminal_value / ((1 + discount_rate) ** len(projected_fcf))
    discounted_value = pv_explicit + pv_terminal
    if fcf_type in {"FCFF", "UFCF"}:
        enterprise_value: Optional[float] = discounted_value
        equity_value = discounted_value - net_debt
        net_debt_adjustment: Optional[float] = net_debt
    else:
        enterprise_value = None
        equity_value = discounted_value
        net_debt_adjustment = None
    return {
        "terminal_value": terminal_value,
        "pv_explicit": pv_explicit,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "net_debt_adjustment": net_debt_adjustment,
        "implied_value_per_share": equity_value / diluted_shares,
    }


def money(value: float) -> str:
    """Format a monetary value."""
    return f"{value:,.2f}"


def optional_money(value: Optional[float]) -> str:
    """Format an optional monetary value."""
    if value is None:
        return "不适用 / N/A"
    return money(value)


def percent(value: float) -> str:
    """Format a decimal percentage."""
    return f"{value:.2%}"


def build_report(input_path: Path, data: dict[str, Any]) -> str:
    """Build the Markdown DCF report."""
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    discount_rates = sorted(float(rate) for rate in data["discount_rates"])
    terminal_rates = sorted(float(rate) for rate in data["terminal_growth_rates"])
    central_discount = statistics.median(discount_rates)
    central_terminal = statistics.median(terminal_rates)
    fcf_type = str(data["fcf_type"])
    amount_unit = str(data["amount_unit"])
    per_share_unit = str(data["per_share_unit"])
    if fcf_type in {"FCFF", "UFCF"}:
        valuation_bridge = (
            "Projected FCFF/UFCF is discounted to enterprise value; net debt is "
            "then subtracted to obtain equity value."
        )
        debt_treatment = (
            f"Net debt of {money(float(data['net_debt']))} {amount_unit} was "
            "subtracted because FCFF/UFCF is an enterprise cash-flow measure."
        )
    else:
        valuation_bridge = (
            "Projected FCFE is discounted directly to equity value; enterprise "
            "value is not calculated by this simplified bridge."
        )
        debt_treatment = (
            "Net debt was not subtracted because FCFE is a levered equity cash-flow "
            "measure and financing effects are already reflected in the cash-flow basis."
        )

    projections = {
        case: project_fcf(
            float(data["base_year_fcf"]),
            [float(rate) for rate in data["revenue_or_fcf_growth_cases"][case]],
        )
        for case in CASE_NAMES
    }

    projection_header = " | ".join(
        ["Case"] + [f"Year {year}" for year in range(1, data["projection_years"] + 1)]
    )
    projection_separator = " | ".join(
        ["---"] + ["---:" for _ in range(data["projection_years"])]
    )
    projection_rows = "\n".join(
        "| "
        + " | ".join([case.title()] + [money(value) for value in projections[case]])
        + " |"
        for case in CASE_NAMES
    )

    scenario_rows: list[str] = []
    for case in CASE_NAMES:
        result = dcf_value(
            projections[case],
            central_discount,
            central_terminal,
            float(data["net_debt"]),
            float(data["diluted_shares"]),
            fcf_type,
        )
        scenario_rows.append(
            "| "
            + " | ".join(
                [
                    case.title(),
                    percent(central_discount),
                    percent(central_terminal),
                    optional_money(result["terminal_value"]),
                    optional_money(result["enterprise_value"]),
                    optional_money(result["equity_value"]),
                    optional_money(result["implied_value_per_share"]),
                ]
            )
            + " |"
        )

    sensitivity_header = (
        "| Discount rate \\ Terminal growth | "
        + " | ".join(percent(rate) for rate in terminal_rates)
        + " |"
    )
    sensitivity_separator = "| --- | " + " | ".join(
        "---:" for _ in terminal_rates
    ) + " |"
    sensitivity_rows: list[str] = []
    for discount_rate in discount_rates:
        values = []
        for terminal_rate in terminal_rates:
            result = dcf_value(
                projections["base"],
                discount_rate,
                terminal_rate,
                float(data["net_debt"]),
                float(data["diluted_shares"]),
                fcf_type,
            )
            values.append(optional_money(result["implied_value_per_share"]))
        sensitivity_rows.append(
            f"| {percent(discount_rate)} | " + " | ".join(values) + " |"
        )

    fictional_note = (
        "- 示例输入标记为虚构数据，不可用于任何真实投资判断。"
        if data["source_status"] == "fictional_sample"
        else "- 输入数据由用户提供；本工具未独立验证其真实性。"
    )

    return f"""# Simplified DCF Sensitivity

## Input file

- `{input_path}`

## Generated at

- {generated_at} UTC

## Currency

- {data["currency"]}
- Amount unit: {amount_unit}
- Per-share unit: {per_share_unit}

## Reporting period

- {data["reporting_period"]}

## Input basis

- {data["basis"]}

## Source status

- {data["source_status"]}
- Source: {data["source"]}
- Source date: {data["source_date"]}

## Key assumptions

- FCF type: {fcf_type}
- Base-year FCF: {money(float(data["base_year_fcf"]))} {amount_unit}
- Projection years: {data["projection_years"]}
- Net debt input: {money(float(data["net_debt"]))} {amount_unit}
- Diluted shares: {money(float(data["diluted_shares"]))} million shares
- Valuation bridge: {valuation_bridge}
- Net debt treatment: {debt_treatment}
- Scenario summary uses median discount rate {percent(central_discount)} and median terminal growth {percent(central_terminal)}.
- Growth inputs are applied to FCF sequentially; the field name permits revenue-derived assumptions, but the model itself projects FCF.

## Calculation result

### Bear / Base / Bull projected FCF ({amount_unit})

| {projection_header} |
| {projection_separator} |
{projection_rows}

### Scenario DCF summary

| Case | Discount rate | Terminal growth | Terminal value ({amount_unit}) | Enterprise value ({amount_unit}) | Equity value ({amount_unit}) | Implied value per share ({per_share_unit}) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(scenario_rows)}

### Base-case sensitivity: implied value per share ({per_share_unit})

{sensitivity_header}
{sensitivity_separator}
{chr(10).join(sensitivity_rows)}

## Data limitations

{fictional_note}
- This is a simplified FCF model and does not separately model revenue, margins, taxes, working capital, capex, SBC, or financing flows.
- FCFF/UFCF requires a WACC-style discount rate; FCFE requires a cost-of-equity-style discount rate. The tool validates arithmetic, not whether the supplied rate matches the FCF type.
- Net debt is held constant for FCFF/UFCF scenarios and is not applied to FCFE scenarios; diluted shares are held constant in all scenarios.
- Terminal value can represent a large share of the discounted enterprise or equity value and is highly sensitive to discount and terminal growth rates.
- The computed implied value per share is a research output, not a promised target price or a buy/sell signal.
- The script validates arithmetic and field structure only; it does not fetch or verify external data.

## Disclaimer

{DISCLAIMER}
"""


def main() -> int:
    """Run the command-line tool."""
    args = parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Input and output paths must be different.")
        data = load_assumptions(args.input)
        report = build_report(args.input, data)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote DCF sensitivity report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
