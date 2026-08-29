#!/usr/bin/env python3
"""Reverse-engineer market-implied scale-up requirements from local CSV data."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


REQUIRED_FIELDS = [
    "ticker",
    "company",
    "currency",
    "amount_unit",
    "per_share_unit",
    "reporting_period",
    "basis",
    "current_price",
    "market_cap",
    "enterprise_value",
    "revenue_ttm",
    "revenue_ntm",
    "gross_margin",
    "operating_margin",
    "free_cash_flow_ttm",
    "net_income_ttm",
    "diluted_shares",
    "ev_sales_current",
    "target_ev_sales_mature",
    "pe_current",
    "target_pe_mature",
    "p_fcf_current",
    "target_p_fcf_mature",
    "years_to_maturity",
    "source",
    "timestamp",
    "market_session",
    "source_status",
]

OPTIONAL_FIELDS = [
    "normalized_net_income_ttm",
    "normalized_eps_ttm",
    "earnings_basis",
    "earnings_basis_notes",
]

EARNINGS_BASES = {
    "reported_gaap",
    "normalized",
    "non_gaap",
    "adjusted",
    "unknown",
}

NUMERIC_FIELDS = {
    "current_price",
    "market_cap",
    "enterprise_value",
    "revenue_ttm",
    "revenue_ntm",
    "gross_margin",
    "operating_margin",
    "free_cash_flow_ttm",
    "net_income_ttm",
    "normalized_net_income_ttm",
    "normalized_eps_ttm",
    "diluted_shares",
    "ev_sales_current",
    "target_ev_sales_mature",
    "pe_current",
    "target_pe_mature",
    "p_fcf_current",
    "target_p_fcf_mature",
    "years_to_maturity",
}

DISCLAIMER = (
    "仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。"
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Reverse-engineer market-implied expectations from local CSV data."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input CSV path.")
    parser.add_argument("--output", required=True, type=Path, help="Output Markdown path.")
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, object]]:
    """Read and validate valuation input rows."""
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing = [field for field in REQUIRED_FIELDS if field not in headers]
        if missing:
            raise ValueError(
                "Input CSV is missing required field(s): " + ", ".join(missing)
            )

        rows: list[dict[str, object]] = []
        for line_number, raw in enumerate(reader, start=2):
            for field in (
                "ticker",
                "company",
                "currency",
                "amount_unit",
                "per_share_unit",
                "reporting_period",
                "basis",
                "source",
                "timestamp",
                "market_session",
                "source_status",
            ):
                if not (raw.get(field) or "").strip():
                    raise ValueError(
                        f"Line {line_number}: required field '{field}' is blank."
                    )

            parsed: dict[str, object] = {
                field: (raw.get(field) or "").strip()
                for field in REQUIRED_FIELDS + OPTIONAL_FIELDS
            }
            if not parsed["earnings_basis"]:
                parsed["earnings_basis"] = "reported_gaap"
            if str(parsed["earnings_basis"]).casefold() not in EARNINGS_BASES:
                raise ValueError(
                    f"Line {line_number}: unsupported earnings_basis "
                    f"{parsed['earnings_basis']!r}."
                )
            for field in NUMERIC_FIELDS:
                value = (raw.get(field) or "").strip()
                if value == "":
                    parsed[field] = None
                    continue
                try:
                    number = float(value.replace(",", ""))
                except ValueError as exc:
                    raise ValueError(
                        f"Line {line_number}: field '{field}' must be numeric; got {value!r}."
                    ) from exc
                if not math.isfinite(number):
                    raise ValueError(
                        f"Line {line_number}: field '{field}' must be finite; got {value!r}."
                    )
                parsed[field] = number

            years = parsed["years_to_maturity"]
            if not isinstance(years, float) or years <= 0:
                raise ValueError(
                    f"Line {line_number}: 'years_to_maturity' must be greater than zero."
                )
            rows.append(parsed)

    if not rows:
        raise ValueError("Input CSV contains no data rows.")
    return rows


def safe_multiple(
    numerator: Optional[float], denominator: Optional[float]
) -> Optional[float]:
    """Return a positive multiple when inputs permit."""
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def scale_up(
    current_value: Optional[float],
    value_base: Optional[float],
    mature_multiple: Optional[float],
    years: float,
) -> tuple[Optional[float], Optional[float], Optional[float]]:
    """Return required mature value, scale-up multiple, and CAGR."""
    if (
        current_value is None
        or current_value <= 0
        or value_base is None
        or value_base <= 0
        or mature_multiple is None
        or mature_multiple <= 0
    ):
        return None, None, None
    required_value = value_base / mature_multiple
    scale = required_value / current_value
    if scale <= 0:
        return required_value, scale, None
    cagr = scale ** (1 / years) - 1
    return required_value, scale, cagr


def format_number(value: object) -> str:
    """Format a numeric value."""
    if not isinstance(value, float):
        return "未验证 / 无法计算"
    return f"{value:,.2f}"


def format_multiple(value: object) -> str:
    """Format a valuation multiple."""
    if not isinstance(value, float) or value <= 0:
        return "未验证 / 无法计算"
    return f"{value:.2f}x"


def format_percent(value: object) -> str:
    """Format a decimal percentage."""
    if not isinstance(value, float):
        return "未验证 / 无法计算"
    return f"{value:.2%}"


def md_escape(value: object) -> str:
    """Escape Markdown table separators."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_company_section(row: dict[str, object]) -> tuple[str, list[str]]:
    """Build one company's implied-expectations section and list missing evidence."""
    missing: list[str] = []
    years = float(row["years_to_maturity"])
    amount_unit = str(row["amount_unit"])
    per_share_unit = str(row["per_share_unit"])
    normalized_net_income = row["normalized_net_income_ttm"]
    normalized_eps = row["normalized_eps_ttm"]
    input_earnings_basis = str(row["earnings_basis"]).casefold()
    earnings_basis_notes = str(row["earnings_basis_notes"]).strip()
    if isinstance(normalized_net_income, float):
        earnings_base = normalized_net_income
        earnings_basis_used = "normalized"
    else:
        earnings_base = row["net_income_ttm"]
        earnings_basis_used = "reported_gaap"

    current_ev_sales = row["ev_sales_current"]
    if not isinstance(current_ev_sales, float):
        current_ev_sales = safe_multiple(
            row["enterprise_value"], row["revenue_ttm"]
        )
    current_pe = row["pe_current"]
    if not isinstance(current_pe, float):
        current_pe = safe_multiple(row["market_cap"], row["net_income_ttm"])
    pe_on_earnings_basis = safe_multiple(row["market_cap"], earnings_base)
    current_p_fcf = row["p_fcf_current"]
    if not isinstance(current_p_fcf, float):
        current_p_fcf = safe_multiple(
            row["market_cap"], row["free_cash_flow_ttm"]
        )

    revenue_required, revenue_scale, revenue_cagr = scale_up(
        row["revenue_ttm"],
        row["enterprise_value"],
        row["target_ev_sales_mature"],
        years,
    )
    income_required, income_scale, income_cagr = scale_up(
        earnings_base,
        row["market_cap"],
        row["target_pe_mature"],
        years,
    )
    fcf_required, fcf_scale, fcf_cagr = scale_up(
        row["free_cash_flow_ttm"],
        row["market_cap"],
        row["target_p_fcf_mature"],
        years,
    )

    checks = {
        "EV/Sales": (
            ["enterprise_value", "revenue_ttm", "target_ev_sales_mature"],
            revenue_required,
        ),
        "P/E": (
            ["market_cap", "net_income_ttm", "target_pe_mature"],
            income_required,
        ),
        "P/FCF": (
            ["market_cap", "free_cash_flow_ttm", "target_p_fcf_mature"],
            fcf_required,
        ),
    }
    for label, (fields, result) in checks.items():
        if result is None:
            absent = [field for field in fields if row[field] is None]
            missing.append(
                f"{label}: 缺少或无效字段 {', '.join(absent) if absent else ', '.join(fields)}。"
            )

    required_fcf_margin = (
        fcf_required / revenue_required
        if fcf_required is not None
        and revenue_required is not None
        and revenue_required != 0
        else None
    )
    current_fcf_margin = (
        row["free_cash_flow_ttm"] / row["revenue_ttm"]
        if isinstance(row["free_cash_flow_ttm"], float)
        and isinstance(row["revenue_ttm"], float)
        and row["revenue_ttm"] != 0
        else None
    )
    required_net_margin = (
        income_required / revenue_required
        if income_required is not None
        and revenue_required is not None
        and revenue_required != 0
        else None
    )
    earnings_cautions: list[str] = []
    if earnings_basis_used == "reported_gaap" and earnings_basis_notes:
        earnings_cautions.append(
            "Reported GAAP earnings may require normalization; P/E implied "
            "expectations should be interpreted with caution."
        )
    if (
        not isinstance(normalized_net_income, float)
        and input_earnings_basis != "reported_gaap"
    ):
        earnings_cautions.append(
            "Normalized earnings were not provided; reported GAAP is used as fallback."
        )
    pe_bridge_statement = (
        "P/E bridge using normalized earnings."
        if earnings_basis_used == "normalized"
        else "P/E bridge uses reported GAAP earnings."
    )
    earnings_caution_md = "\n".join(
        f"- {item}" for item in earnings_cautions
    ) or "- No additional earnings-basis caution was triggered by the input."

    section = f"""### {md_escape(row["ticker"])} - {md_escape(row["company"])}

#### Input snapshot

| Item | Value |
| --- | ---: |
| Current price | {format_number(row["current_price"])} {per_share_unit} |
| Market cap | {format_number(row["market_cap"])} {amount_unit} |
| Enterprise value | {format_number(row["enterprise_value"])} {amount_unit} |
| Revenue TTM | {format_number(row["revenue_ttm"])} {amount_unit} |
| Revenue NTM | {format_number(row["revenue_ntm"])} {amount_unit} |
| Gross margin | {format_percent(row["gross_margin"])} |
| Operating margin | {format_percent(row["operating_margin"])} |
| Current EV/Sales | {format_multiple(current_ev_sales)} |
| Current P/E (input / reported market basis) | {format_multiple(current_pe)} |
| P/E on earnings basis used | {format_multiple(pe_on_earnings_basis)} |
| Current P/FCF | {format_multiple(current_p_fcf)} |
| Years to maturity | {years:g} |

#### Earnings basis

- Earnings basis requested: {md_escape(row["earnings_basis"])}
- Earnings basis used: {earnings_basis_used}
- Reported GAAP net income: {format_number(row["net_income_ttm"])} {amount_unit}
- Normalized net income: {format_number(normalized_net_income)} {amount_unit}
- Normalized EPS context: {format_number(normalized_eps)} {per_share_unit}
- Earnings basis notes: {md_escape(earnings_basis_notes or "未提供")}
- {pe_bridge_statement}
{earnings_caution_md}

#### Static scale-up requirements

| Framework | Mature multiple assumption | Required mature operating value ({amount_unit}) | Scale-up vs TTM | Required CAGR |
| --- | ---: | ---: | ---: | ---: |
| EV/Sales -> revenue | {format_multiple(row["target_ev_sales_mature"])} | {format_number(revenue_required)} | {format_multiple(revenue_scale)} | {format_percent(revenue_cagr)} |
| P/E -> net income / EPS | {format_multiple(row["target_pe_mature"])} | {format_number(income_required)} | {format_multiple(income_scale)} | {format_percent(income_cagr)} |
| P/FCF -> free cash flow | {format_multiple(row["target_p_fcf_mature"])} | {format_number(fcf_required)} | {format_multiple(fcf_scale)} | {format_percent(fcf_cagr)} |

#### Margin implications

- Current FCF margin: {format_percent(current_fcf_margin)}
- Implied mature FCF margin, combining the EV/Sales and P/FCF static requirements: {format_percent(required_fcf_margin)}
- Implied mature net margin, combining the EV/Sales and P/E static requirements: {format_percent(required_net_margin)}
- Current gross margin: {format_percent(row["gross_margin"])}
- Current operating margin: {format_percent(row["operating_margin"])}

#### Interpretation

- The calculation holds current enterprise value or market capitalization constant and asks how much revenue, net income, or FCF would be needed for the supplied mature multiple.
- Required CAGR is a mechanical bridge to the mature value over {years:g} years, not a forecast.
- If the required revenue CAGR, margin conversion, or FCF growth is materially above sourced operating evidence, valuation compression risk is higher.
- Share count is treated as constant for the EPS scale-up interpretation; dilution or buybacks would change the result.
- The P/E scale-up uses the displayed earnings basis; normalized earnings are never generated by the tool.

#### Source record

- Source: {md_escape(row["source"])}
- Input basis: {md_escape(row["basis"])}
- Timestamp: {md_escape(row["timestamp"])}
- Market session: {md_escape(row["market_session"])}
- Source status: {md_escape(row["source_status"])}
- Reporting period: {md_escape(row["reporting_period"])}
"""
    return section, missing


def build_report(input_path: Path, rows: list[dict[str, object]]) -> str:
    """Build the Markdown implied-expectations report."""
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    currencies = sorted({str(row["currency"]) for row in rows})
    amount_units = sorted({str(row["amount_unit"]) for row in rows})
    per_share_units = sorted({str(row["per_share_unit"]) for row in rows})
    periods = sorted({str(row["reporting_period"]) for row in rows})
    bases = sorted({str(row["basis"]) for row in rows})
    statuses = sorted({str(row["source_status"]) for row in rows})

    sections: list[str] = []
    gaps: list[str] = []
    for row in rows:
        section, company_gaps = build_company_section(row)
        sections.append(section)
        gaps.extend(f"- {row['ticker']}: {gap}" for gap in company_gaps)
    if not gaps:
        gaps.append("- 未发现阻止三种反推框架运行的关键字段缺口。")

    return f"""# Market-Implied Expectations

## Input file

- `{input_path}`

## Generated at

- {generated_at} UTC

## Currency

- {", ".join(currencies)}
- Amount unit: {", ".join(amount_units)}
- Per-share unit: {", ".join(per_share_units)}

## Reporting period

- {", ".join(periods)}

## Input basis

- {"; ".join(bases)}

## Source status

- {", ".join(statuses)}

## Key assumptions

- This is a reverse-engineering framework, not a forecasting model.
- Enterprise value and market capitalization are held constant in the static mature-multiple bridge.
- Mature multiples and years to maturity are user-provided assumptions and require independent justification.
- TTM, NTM, source timestamp, market session, currency, amount unit, per-share unit, and source status are retained from the input.

## Calculation result

{chr(10).join(sections)}

## Data gaps

{chr(10).join(gaps)}

## Data limitations

- The tool does not model changes in net debt, share count, acquisitions, divestitures, taxes, or capital intensity.
- Current multiples may be calculated from supplied base fields when the multiple itself is blank.
- Required growth rates can be mathematically negative when current operating values already exceed the static mature-multiple requirement; this is not a positive or negative investment conclusion by itself.
- A research report must compare these implied requirements with sourced TAM, market share, margin, competitive, and cash-conversion evidence.
- No deterministic target price or buy/sell instruction is produced.

## Disclaimer

{DISCLAIMER}
"""


def main() -> int:
    """Run the command-line tool."""
    args = parse_args()
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("Input and output paths must be different.")
        rows = read_rows(args.input)
        report = build_report(args.input, rows)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote implied-expectations report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
