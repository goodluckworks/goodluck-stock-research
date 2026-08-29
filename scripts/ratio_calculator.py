#!/usr/bin/env python3
"""Calculate auditable financial ratios from a local CSV file."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


REQUIRED_FIELDS = [
    "period",
    "currency",
    "amount_unit",
    "per_share_unit",
    "basis",
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "total_debt",
    "total_assets",
    "shareholders_equity",
    "shares_diluted",
    "stock_based_compensation",
    "accounts_receivable",
    "inventory",
    "current_assets",
    "current_liabilities",
    "source",
    "source_date",
    "source_status",
]

OPTIONAL_FIELDS = [
    "short_term_investments",
    "cash_and_short_term_investments",
    "net_debt_basis",
    "special_items_notes",
    "normalized_net_income",
    "normalized_eps",
    "normalized_operating_income",
    "goodwill",
    "intangible_assets",
    "acquisition_related_amortization",
    "restructuring_and_integration_costs",
    "acquisition_related_costs",
    "acquisition_accounting_notes",
]

NUMERIC_FIELDS = {
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income",
    "operating_cash_flow",
    "capital_expenditure",
    "cash_and_equivalents",
    "short_term_investments",
    "cash_and_short_term_investments",
    "total_debt",
    "total_assets",
    "shareholders_equity",
    "shares_diluted",
    "stock_based_compensation",
    "accounts_receivable",
    "inventory",
    "current_assets",
    "current_liabilities",
    "normalized_net_income",
    "normalized_eps",
    "normalized_operating_income",
    "goodwill",
    "intangible_assets",
    "acquisition_related_amortization",
    "restructuring_and_integration_costs",
    "acquisition_related_costs",
}

NET_DEBT_BASES = {
    "cash_only",
    "cash_plus_short_term_investments",
    "user_provided_cash_and_investments",
    "unknown",
}

DISCLAIMER = (
    "仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。"
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Calculate financial ratios from a local CSV file."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input CSV path.")
    parser.add_argument("--output", required=True, type=Path, help="Output Markdown path.")
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, object]]:
    """Read and validate financial rows from CSV."""
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
                "period",
                "currency",
                "amount_unit",
                "per_share_unit",
                "basis",
                "source",
                "source_date",
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
            for field in NUMERIC_FIELDS:
                if field not in headers:
                    parsed[field] = None
                    continue
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
            net_debt_basis = str(parsed["net_debt_basis"]).casefold()
            if net_debt_basis and net_debt_basis not in NET_DEBT_BASES:
                raise ValueError(
                    f"Line {line_number}: unsupported net_debt_basis "
                    f"{parsed['net_debt_basis']!r}."
                )
            rows.append(parsed)

    if not rows:
        raise ValueError("Input CSV contains no data rows.")
    return rows


def safe_divide(
    numerator: Optional[float], denominator: Optional[float]
) -> Optional[float]:
    """Return numerator divided by denominator, or None when unavailable."""
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def growth(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    """Return period-over-period growth, or None when unavailable."""
    if current is None or previous is None or previous == 0:
        return None
    return current / previous - 1


def format_number(value: Optional[float]) -> str:
    """Format a numeric value for Markdown."""
    if value is None:
        return "无法计算"
    return f"{value:,.2f}"


def format_percent(value: Optional[float]) -> str:
    """Format a decimal ratio as a percentage."""
    if value is None:
        return "无法计算"
    return f"{value:.2%}"


def format_multiple(value: Optional[float]) -> str:
    """Format a ratio as a multiple."""
    if value is None:
        return "无法计算"
    return f"{value:.2f}x"


def format_net_debt(value: Optional[float]) -> str:
    """Format net debt and make a net-cash position explicit."""
    if value is None:
        return "无法计算"
    if value < 0:
        return f"Net cash {abs(value):,.2f}"
    return f"Net debt {value:,.2f}"


def md_escape(value: object) -> str:
    """Escape Markdown table separators."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def build_report(input_path: Path, rows: list[dict[str, object]]) -> str:
    """Build the Markdown ratio report."""
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    currencies = sorted({str(row["currency"]) for row in rows})
    amount_units = sorted({str(row["amount_unit"]) for row in rows})
    per_share_units = sorted({str(row["per_share_unit"]) for row in rows})
    bases = sorted({str(row["basis"]) for row in rows})
    periods = [str(row["period"]) for row in rows]
    source_statuses = sorted({str(row["source_status"]) for row in rows})
    limitations: list[str] = []

    if len(currencies) > 1:
        limitations.append(
            "输入包含多种币种；跨期比率可能不可比，除非输入已按一致汇率重述。"
        )
    if len(rows) < 2:
        limitations.append(
            "只有一期数据；Revenue growth 和 Diluted shares trend 无法计算。"
        )

    table_rows: list[str] = []
    prior_revenue: Optional[float] = None
    prior_shares: Optional[float] = None
    missing_cells = 0
    normalization_rows: list[str] = []
    acquisition_rows: list[str] = []

    for index, row in enumerate(rows):
        revenue = row["revenue"]
        gross_profit = row["gross_profit"]
        operating_income = row["operating_income"]
        net_income = row["net_income"]
        operating_cash_flow = row["operating_cash_flow"]
        capex = row["capital_expenditure"]
        cash = row["cash_and_equivalents"]
        short_term_investments = row["short_term_investments"]
        cash_and_investments = row["cash_and_short_term_investments"]
        input_net_debt_basis = str(row["net_debt_basis"]).strip()
        debt = row["total_debt"]
        assets = row["total_assets"]
        equity = row["shareholders_equity"]
        shares = row["shares_diluted"]
        sbc = row["stock_based_compensation"]
        ar = row["accounts_receivable"]
        inventory = row["inventory"]
        current_assets = row["current_assets"]
        current_liabilities = row["current_liabilities"]
        normalized_net_income = row["normalized_net_income"]
        normalized_eps = row["normalized_eps"]
        normalized_operating_income = row["normalized_operating_income"]
        special_items_notes = str(row["special_items_notes"]).strip()
        goodwill = row["goodwill"]
        intangible_assets = row["intangible_assets"]
        acquisition_amortization = row["acquisition_related_amortization"]
        restructuring_costs = row["restructuring_and_integration_costs"]
        acquisition_costs = row["acquisition_related_costs"]
        acquisition_accounting_notes = str(
            row["acquisition_accounting_notes"]
        ).strip()

        numeric_values = [
            revenue,
            gross_profit,
            operating_income,
            net_income,
            operating_cash_flow,
            capex,
            cash,
            debt,
            assets,
            equity,
            shares,
            sbc,
            ar,
            inventory,
            current_assets,
            current_liabilities,
        ]
        missing_cells += sum(value is None for value in numeric_values)

        normalized_capex = abs(capex) if isinstance(capex, float) else None
        fcf = (
            operating_cash_flow - normalized_capex
            if isinstance(operating_cash_flow, float)
            and normalized_capex is not None
            else None
        )
        if isinstance(cash_and_investments, float):
            cash_base = cash_and_investments
            selected_net_debt_basis = "user_provided_cash_and_investments"
        elif isinstance(short_term_investments, float):
            cash_base = (
                cash + short_term_investments
                if isinstance(cash, float)
                else None
            )
            selected_net_debt_basis = "cash_plus_short_term_investments"
        else:
            cash_base = cash if isinstance(cash, float) else None
            selected_net_debt_basis = "cash_only"
        if (
            input_net_debt_basis
            and input_net_debt_basis != "unknown"
            and input_net_debt_basis != selected_net_debt_basis
        ):
            raise ValueError(
                f"{row['period']}: net_debt_basis {input_net_debt_basis!r} "
                f"conflicts with selected fields; expected "
                f"{selected_net_debt_basis!r}."
            )
        net_debt_basis = input_net_debt_basis or selected_net_debt_basis
        net_debt = (
            debt - cash_base
            if isinstance(debt, float) and isinstance(cash_base, float)
            else None
        )
        revenue_growth = (
            growth(revenue, prior_revenue)
            if index > 0
            else None
        )
        shares_growth = (
            growth(shares, prior_shares)
            if index > 0
            else None
        )

        revenue_growth_display = (
            "无法计算：需要至少两期数据"
            if len(rows) == 1
            else format_percent(revenue_growth)
        )
        shares_growth_display = (
            "无法计算：需要至少两期数据"
            if len(rows) == 1
            else format_percent(shares_growth)
        )

        table_rows.append(
            "| "
            + " | ".join(
                [
                    md_escape(row["period"]),
                    revenue_growth_display,
                    format_percent(safe_divide(gross_profit, revenue)),
                    format_percent(safe_divide(operating_income, revenue)),
                    format_percent(safe_divide(net_income, revenue)),
                    format_percent(safe_divide(operating_cash_flow, revenue)),
                    format_number(fcf),
                    format_percent(safe_divide(fcf, revenue)),
                    format_percent(safe_divide(net_income, equity)),
                    format_percent(safe_divide(net_income, assets)),
                    format_percent(safe_divide(normalized_net_income, revenue)),
                    format_percent(safe_divide(normalized_net_income, equity)),
                    format_percent(safe_divide(normalized_net_income, assets)),
                    format_number(cash_base),
                    md_escape(net_debt_basis),
                    format_number(net_debt),
                    format_net_debt(net_debt),
                    format_multiple(safe_divide(debt, equity)),
                    format_multiple(safe_divide(current_assets, current_liabilities)),
                    format_percent(safe_divide(sbc, revenue)),
                    format_percent(safe_divide(ar, revenue)),
                    format_percent(safe_divide(inventory, revenue)),
                    shares_growth_display,
                ]
            )
            + " |"
        )

        prior_revenue = revenue if isinstance(revenue, float) else None
        prior_shares = shares if isinstance(shares, float) else None

        if special_items_notes:
            normalization_rows.append(
                f"| {md_escape(row['period'])} | {md_escape(special_items_notes)} | "
                f"{format_number(normalized_operating_income)} | "
                f"{format_number(normalized_net_income)} | "
                f"{format_number(normalized_eps)} |"
            )
            limitations.append(
                f"{row['period']}: raw GAAP profitability may require normalization; "
                f"special items notes: {special_items_notes}"
            )
            if not isinstance(normalized_net_income, float):
                limitations.append(
                    f"{row['period']}: normalized metrics not provided; raw GAAP "
                    "profitability should not be over-interpreted."
                )

        acquisition_values = [
            goodwill,
            intangible_assets,
            acquisition_amortization,
            restructuring_costs,
            acquisition_costs,
        ]
        if any(isinstance(value, float) for value in acquisition_values) or acquisition_accounting_notes:
            acquisition_rows.append(
                "| "
                + " | ".join(
                    [
                        md_escape(row["period"]),
                        format_number(goodwill),
                        format_percent(safe_divide(goodwill, assets)),
                        format_number(intangible_assets),
                        format_percent(safe_divide(intangible_assets, assets)),
                        format_number(acquisition_amortization),
                        format_percent(safe_divide(acquisition_amortization, revenue)),
                        format_number(restructuring_costs),
                        format_percent(safe_divide(restructuring_costs, revenue)),
                        format_number(acquisition_costs),
                        format_percent(safe_divide(acquisition_costs, revenue)),
                        md_escape(acquisition_accounting_notes or "未提供"),
                    ]
                )
                + " |"
            )
            limitations.append(
                f"{row['period']}: acquisition accounting ratios depend on "
                "user-supplied classifications and do not determine whether an "
                "expense is economically recurring."
            )

    if missing_cells:
        limitations.append(
            f"输入共有 {missing_cells} 个空白数值单元格；相关指标标记为“无法计算”。"
        )
    limitations.append(
        "ROE 和 ROA 使用期末 shareholders' equity 与 total assets，未使用期初期末平均值。"
    )
    limitations.append(
        "Capital expenditure 按现金流出绝对值处理，FCF = operating cash flow - |capital expenditure|。"
    )
    limitations.append(
        "Net debt depends on the cash/investments field selected by the input. "
        "Users must confirm whether short-term investments are liquid and appropriate to include."
    )
    limitations.append(
        "本工具只校验字段和算术逻辑，不验证输入数据是否与原始披露一致。"
    )

    sources = "\n".join(
        f"- {md_escape(row['period'])}: basis {md_escape(row['basis'])}; "
        f"source {md_escape(row['source'])}; "
        f"source date {md_escape(row['source_date'])}; "
        f"status {md_escape(row['source_status'])}."
        for row in rows
    )
    limitations_md = "\n".join(f"- {item}" for item in limitations)
    normalization_section = (
        "\n".join(
            [
                "## Special items and normalization",
                "",
                "Raw GAAP profitability may require normalization where notes are present.",
                "",
                f"| Period | Special items notes | Normalized operating income ({', '.join(amount_units)}) | Normalized net income ({', '.join(amount_units)}) | Normalized EPS ({', '.join(per_share_units)}) |",
                "| --- | --- | ---: | ---: | ---: |",
                *normalization_rows,
            ]
        )
        if normalization_rows
        else "## Special items and normalization\n\n- No special items notes were provided."
    )
    acquisition_section = (
        "\n".join(
            [
                "## Acquisition accounting",
                "",
                f"| Period | Goodwill ({', '.join(amount_units)}) | Goodwill / assets | Intangible assets ({', '.join(amount_units)}) | Intangibles / assets | Acquisition-related amortization ({', '.join(amount_units)}) | Amortization / revenue | Restructuring and integration costs ({', '.join(amount_units)}) | Restructuring / revenue | Acquisition-related costs ({', '.join(amount_units)}) | Acquisition costs / revenue | Acquisition accounting notes |",
                "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
                *acquisition_rows,
                "",
                "These fields preserve reported acquisition-accounting evidence. "
                "They do not automatically convert GAAP results into normalized results.",
            ]
        )
        if acquisition_rows
        else (
            "## Acquisition accounting\n\n"
            "- No acquisition-accounting fields were provided; acquisition-related "
            "balance-sheet and expense ratios were not calculated."
        )
    )

    return f"""# Financial Ratio Calculation

## Input file

- `{input_path}`

## Generated at

- {generated_at} UTC

## Currency

- {", ".join(currencies)}
- Amount unit: {", ".join(amount_units)}
- Per-share unit: {", ".join(per_share_units)}

## Reporting period

- {periods[0]} to {periods[-1]}

## Input basis

- {"; ".join(bases)}

## Source status

- {", ".join(source_statuses)}

## Key assumptions

- 输入行按时间从早到晚排列；growth 与 share trend 使用相邻行计算。
- 金额单位使用 amount_unit；每股数据单位使用 per_share_unit，不进行币种换算或单位缩放。
- 所有比率使用同一行的财务数据，除非另有说明。

## Calculation result

| Period | Revenue growth | Gross margin | Operating margin | Raw net margin | OCF margin | Free cash flow ({", ".join(amount_units)}) | FCF margin | Raw ROE | Raw ROA | Normalized net margin | Normalized ROE | Normalized ROA | Cash base used ({", ".join(amount_units)}) | Net debt basis | Net debt numeric ({", ".join(amount_units)}) | Net debt / (net cash) | Debt / equity | Current ratio | SBC / revenue | AR / revenue | Inventory / revenue | Diluted shares trend |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(table_rows)}

## Input sources

{sources}

{normalization_section}

{acquisition_section}

## Data limitations

{limitations_md}

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

    print(f"Wrote ratio report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
