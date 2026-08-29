#!/usr/bin/env python3
"""Build an auditable peer-comps Markdown table from a local CSV file."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
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
    "market_cap",
    "enterprise_value",
    "revenue_ttm",
    "ebitda_ttm",
    "net_income_ttm",
    "free_cash_flow_ttm",
    "revenue_growth_forward",
    "gross_margin",
    "operating_margin",
    "ev_sales_ttm",
    "ev_ebitda_ttm",
    "pe_ttm",
    "forward_pe",
    "p_fcf_ttm",
    "source",
    "timestamp",
    "market_session",
    "source_status",
]

OPTIONAL_FIELDS = [
    "forward_revenue_growth_source",
    "peer_group",
    "comparability_status",
    "comparability_notes",
    "include_in_core_stats",
]

PEER_GROUPS = {
    "core_ai_accelerator",
    "ai_networking_connectivity",
    "diversified_semiconductor",
    "semiconductor_equipment",
    "foundry",
    "ip_licensing",
    "handset_mobile",
    "optical_connectivity",
    "reference_only",
    "other",
}

COMPARABILITY_STATUSES = {
    "core",
    "adjacent",
    "reference",
    "weak",
    "exclude",
    "unknown",
}

NUMERIC_FIELDS = {
    "market_cap",
    "enterprise_value",
    "revenue_ttm",
    "ebitda_ttm",
    "net_income_ttm",
    "free_cash_flow_ttm",
    "revenue_growth_forward",
    "gross_margin",
    "operating_margin",
    "ev_sales_ttm",
    "ev_ebitda_ttm",
    "pe_ttm",
    "forward_pe",
    "p_fcf_ttm",
}

MULTIPLE_FIELDS = (
    "ev_sales_ttm",
    "ev_ebitda_ttm",
    "pe_ttm",
    "forward_pe",
    "p_fcf_ttm",
)

MULTIPLE_LABELS = {
    "ev_sales_ttm": "EV/Sales TTM",
    "ev_ebitda_ttm": "EV/EBITDA TTM",
    "pe_ttm": "P/E TTM",
    "forward_pe": "Forward P/E",
    "p_fcf_ttm": "P/FCF TTM",
}

DISCLAIMER = (
    "仅用于研究分析和学习交流，不构成投资建议、买卖建议或个性化资产配置建议。"
)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a peer-comps table from a local CSV file."
    )
    parser.add_argument("--input", required=True, type=Path, help="Input CSV path.")
    parser.add_argument("--output", required=True, type=Path, help="Output Markdown path.")
    parser.add_argument(
        "--target-ticker",
        required=True,
        help="Ticker to identify as the target company.",
    )
    return parser.parse_args()


def read_rows(path: Path) -> list[dict[str, object]]:
    """Read and validate peer-comps rows."""
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
            if not parsed["forward_revenue_growth_source"]:
                parsed["forward_revenue_growth_source"] = "unknown"
            if not parsed["peer_group"]:
                parsed["peer_group"] = "other"
            if str(parsed["peer_group"]).casefold() not in PEER_GROUPS:
                raise ValueError(
                    f"Line {line_number}: unsupported peer_group "
                    f"{parsed['peer_group']!r}."
                )
            if not parsed["comparability_status"]:
                parsed["comparability_status"] = "unknown"
            if (
                str(parsed["comparability_status"]).casefold()
                not in COMPARABILITY_STATUSES
            ):
                raise ValueError(
                    f"Line {line_number}: unsupported comparability_status "
                    f"{parsed['comparability_status']!r}."
                )
            include_value = str(parsed["include_in_core_stats"]).casefold()
            if include_value in {"true", "1", "yes"}:
                parsed["include_in_core_stats"] = True
            elif include_value in {"false", "0", "no", ""}:
                parsed["include_in_core_stats"] = False
            else:
                raise ValueError(
                    f"Line {line_number}: include_in_core_stats must be true or false."
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
            rows.append(parsed)

    if not rows:
        raise ValueError("Input CSV contains no data rows.")
    tickers = [str(row["ticker"]).casefold() for row in rows]
    if len(tickers) != len(set(tickers)):
        raise ValueError("Input CSV contains duplicate ticker values.")
    return rows


def safe_multiple(
    numerator: Optional[float], denominator: Optional[float]
) -> Optional[float]:
    """Return a positive valuation multiple when inputs permit."""
    if numerator is None or denominator is None or denominator <= 0:
        return None
    return numerator / denominator


def fill_calculated_multiples(row: dict[str, object]) -> dict[str, str]:
    """Calculate missing valuation multiples and return calculation labels."""
    origins: dict[str, str] = {}
    calculations = {
        "ev_sales_ttm": safe_multiple(
            row["enterprise_value"], row["revenue_ttm"]
        ),
        "ev_ebitda_ttm": safe_multiple(
            row["enterprise_value"], row["ebitda_ttm"]
        ),
        "pe_ttm": safe_multiple(row["market_cap"], row["net_income_ttm"]),
        "p_fcf_ttm": safe_multiple(
            row["market_cap"], row["free_cash_flow_ttm"]
        ),
    }
    for field, calculated in calculations.items():
        if row[field] is None and calculated is not None:
            row[field] = calculated
            origins[field] = "calculated"
        elif row[field] is not None:
            origins[field] = "provided"
        else:
            origins[field] = "unavailable"

    origins["forward_pe"] = (
        "provided" if row["forward_pe"] is not None else "unavailable"
    )
    return origins


def format_number(value: object) -> str:
    """Format a numeric value or mark it unavailable."""
    if not isinstance(value, float):
        return "未提供 / 无法计算"
    return f"{value:,.2f}"


def format_multiple(value: object, origin: str) -> str:
    """Format a valuation multiple and indicate calculated values."""
    if not isinstance(value, float) or value <= 0:
        return "未提供 / 无法计算"
    suffix = " (calc)" if origin == "calculated" else ""
    return f"{value:.2f}x{suffix}"


def format_percent(value: object) -> str:
    """Format a decimal percentage."""
    if not isinstance(value, float):
        return "未提供"
    return f"{value:.2%}"


def format_forward_growth(value: object, source: object) -> str:
    """Format forward growth and visibly mark mechanical derivations."""
    formatted = format_percent(value)
    if str(source).casefold() == "derived_from_ps_multiple":
        return f"{formatted} (derived)"
    return formatted


def md_escape(value: object) -> str:
    """Escape Markdown table separators."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def valid_values(rows: list[dict[str, object]], field: str) -> list[float]:
    """Return positive comparable values for a multiple."""
    return [
        value
        for row in rows
        if isinstance((value := row[field]), float) and value > 0
    ]


def build_report(
    input_path: Path,
    rows: list[dict[str, object]],
    target_ticker: str,
) -> str:
    """Build the Markdown peer-comps report."""
    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    origins = {str(row["ticker"]): fill_calculated_multiples(row) for row in rows}
    target = next(
        (
            row
            for row in rows
            if str(row["ticker"]).casefold() == target_ticker.casefold()
        ),
        None,
    )
    if target is None:
        raise ValueError(f"Target ticker '{target_ticker}' was not found in the input.")

    currencies = sorted({str(row["currency"]) for row in rows})
    amount_units = sorted({str(row["amount_unit"]) for row in rows})
    per_share_units = sorted({str(row["per_share_unit"]) for row in rows})
    periods = sorted({str(row["reporting_period"]) for row in rows})
    bases = sorted({str(row["basis"]) for row in rows})
    statuses = sorted({str(row["source_status"]) for row in rows})

    raw_rows: list[str] = []
    for row in rows:
        origin = origins[str(row["ticker"])]
        raw_rows.append(
            "| "
            + " | ".join(
                [
                    md_escape(row["ticker"]),
                    md_escape(row["company"]),
                    md_escape(row["currency"]),
                    md_escape(row["amount_unit"]),
                    md_escape(row["peer_group"]),
                    md_escape(row["comparability_status"]),
                    md_escape(row["comparability_notes"] or "未提供"),
                    "true" if row["include_in_core_stats"] else "false",
                    format_number(row["market_cap"]),
                    format_number(row["enterprise_value"]),
                    format_forward_growth(
                        row["revenue_growth_forward"],
                        row["forward_revenue_growth_source"],
                    ),
                    md_escape(row["forward_revenue_growth_source"]),
                    format_percent(row["gross_margin"]),
                    format_percent(row["operating_margin"]),
                    format_multiple(row["ev_sales_ttm"], origin["ev_sales_ttm"]),
                    format_multiple(
                        row["ev_ebitda_ttm"], origin["ev_ebitda_ttm"]
                    ),
                    format_multiple(row["pe_ttm"], origin["pe_ttm"]),
                    format_multiple(row["forward_pe"], origin["forward_pe"]),
                    format_multiple(row["p_fcf_ttm"], origin["p_fcf_ttm"]),
                ]
            )
            + " |"
        )

    peer_rows = [
        row
        for row in rows
        if str(row["ticker"]).casefold() != target_ticker.casefold()
    ]
    if not peer_rows:
        raise ValueError("At least one peer row other than the target ticker is required.")
    core_peer_rows = [
        row for row in peer_rows if row["include_in_core_stats"] is True
    ]

    blended_stats_rows: list[str] = []
    core_stats_rows: list[str] = []
    blended_position_rows: list[str] = []
    core_position_rows: list[str] = []
    for field in MULTIPLE_FIELDS:
        peer_values = valid_values(peer_rows, field)
        core_peer_values = valid_values(core_peer_rows, field)
        all_values = valid_values(rows, field)
        if peer_values:
            blended_stats_rows.append(
                "| "
                + " | ".join(
                    [
                        MULTIPLE_LABELS[field],
                        f"{statistics.median(peer_values):.2f}x",
                        f"{statistics.mean(peer_values):.2f}x",
                        f"{min(peer_values):.2f}x",
                        f"{max(peer_values):.2f}x",
                        str(len(peer_values)),
                    ]
                )
                + " |"
            )
        else:
            blended_stats_rows.append(
                f"| {MULTIPLE_LABELS[field]} | 无法计算 | 无法计算 | "
                "无法计算 | 无法计算 | 0 |"
            )

        target_value = target[field]
        if (
            not isinstance(target_value, float)
            or target_value <= 0
            or not peer_values
        ):
            blended_position_rows.append(
                f"| {MULTIPLE_LABELS[field]} | 未提供 / 无法计算 | "
                "无法比较 | 无法比较 |"
            )
        else:
            median = statistics.median(peer_values)
            premium = target_value / median - 1 if median != 0 else None
            rank = sum(value <= target_value for value in all_values)
            percentile = rank / len(all_values)
            blended_position_rows.append(
                f"| {MULTIPLE_LABELS[field]} | {target_value:.2f}x | "
                f"{premium:.2%} | {percentile:.0%} |"
            )

        if core_peer_values:
            core_stats_rows.append(
                "| "
                + " | ".join(
                    [
                        MULTIPLE_LABELS[field],
                        f"{statistics.median(core_peer_values):.2f}x",
                        f"{statistics.mean(core_peer_values):.2f}x",
                        f"{min(core_peer_values):.2f}x",
                        f"{max(core_peer_values):.2f}x",
                        str(len(core_peer_values)),
                    ]
                )
                + " |"
            )
        else:
            core_stats_rows.append(
                f"| {MULTIPLE_LABELS[field]} | 无法计算 | 无法计算 | "
                "无法计算 | 无法计算 | 0 |"
            )

        if (
            not isinstance(target_value, float)
            or target_value <= 0
            or not core_peer_values
        ):
            core_position_rows.append(
                f"| {MULTIPLE_LABELS[field]} | 未提供 / 无法计算 | "
                "无法比较 |"
            )
        else:
            core_median = statistics.median(core_peer_values)
            core_premium = (
                target_value / core_median - 1 if core_median != 0 else None
            )
            core_position_rows.append(
                f"| {MULTIPLE_LABELS[field]} | {target_value:.2f}x | "
                f"{core_premium:.2%} |"
            )

    gaps: list[str] = []
    comparability: list[str] = []
    for row in rows:
        ticker = str(row["ticker"])
        missing = [
            MULTIPLE_LABELS[field]
            for field in MULTIPLE_FIELDS
            if not isinstance(row[field], float) or row[field] <= 0
        ]
        if missing:
            gaps.append(f"- {ticker}: 缺少或无法计算 {', '.join(missing)}。")
        reasons: list[str] = []
        if row["currency"] != target["currency"]:
            reasons.append("币种不同")
        if row["reporting_period"] != target["reporting_period"]:
            reasons.append("报告期间不同")
        if row["ebitda_ttm"] is None or (
            isinstance(row["ebitda_ttm"], float) and row["ebitda_ttm"] <= 0
        ):
            reasons.append("EBITDA 非正或缺失")
        if row["net_income_ttm"] is None or (
            isinstance(row["net_income_ttm"], float)
            and row["net_income_ttm"] <= 0
        ):
            reasons.append("净利润非正或缺失")
        if str(row["source_status"]).lower() not in {"verified", "company_filing"}:
            reasons.append("来源尚未完全核实")
        if str(row["comparability_status"]).casefold() in {
            "reference",
            "weak",
            "exclude",
            "unknown",
        }:
            reasons.append(
                f"结构化可比性为 {row['comparability_status']}"
            )
        if reasons:
            comparability.append(f"- {ticker}: {', '.join(reasons)}。")

    if not gaps:
        gaps.append("- 未发现估值倍数数据缺口。")
    if not comparability:
        comparability.append("- 未发现基于输入字段的明显不可比项；仍需人工核对商业模式和会计口径。")
    core_sample_note = (
        "- Core comparable sample is too small; core stats are indicative only."
        if len(core_peer_rows) < 2
        else f"- Core comparable sample contains {len(core_peer_rows)} companies."
    )

    source_rows = "\n".join(
        f"- {md_escape(row['ticker'])}: basis {md_escape(row['basis'])}; "
        f"source {md_escape(row['source'])}; "
        f"{md_escape(row['timestamp'])}; {md_escape(row['market_session'])}; "
        f"{md_escape(row['source_status'])}; forward growth source "
        f"{md_escape(row['forward_revenue_growth_source'])}; peer group "
        f"{md_escape(row['peer_group'])}; comparability "
        f"{md_escape(row['comparability_status'])}; core stats "
        f"{'included' if row['include_in_core_stats'] else 'excluded'}."
        for row in rows
    )
    derived_growth_rows = [
        str(row["ticker"])
        for row in rows
        if str(row["forward_revenue_growth_source"]).casefold()
        == "derived_from_ps_multiple"
    ]
    growth_provenance_note = (
        "- Forward revenue growth is labeled by provenance. "
        "`derived_from_ps_multiple` is a mechanical derivation, not sourced "
        "consensus growth, company guidance, or analyst consensus."
    )
    if derived_growth_rows:
        growth_provenance_note += (
            f"\n- Derived rows: {', '.join(derived_growth_rows)}."
        )

    return f"""# Peer Comps Table

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

- Target ticker: {target["ticker"]} ({target["company"]})
- Missing EV/Sales, EV/EBITDA, P/E, and P/FCF may be calculated from supplied base fields.
- Forward P/E cannot be derived without forward earnings and remains unavailable when not supplied.
- Forward revenue growth provenance is retained from `forward_revenue_growth_source`.
- Blended peer statistics exclude the target company and exclude missing, zero, and negative valuation multiples.
- Core comparable statistics additionally require `include_in_core_stats == true`.
- Currency conversion is not performed; cross-currency absolute values are not directly comparable.

## Calculation result

### Raw peer comps

| Ticker | Company | Currency | Amount unit | Peer group | Comparability | Comparability notes | Core stats | Market cap | EV | Forward revenue growth (derived where noted) | Growth source | Gross margin | Operating margin | EV/Sales TTM | EV/EBITDA TTM | P/E TTM | Forward P/E | P/FCF TTM |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(raw_rows)}

`(calc)` 表示脚本使用输入的基础字段计算；未标记项为输入文件直接提供。

{growth_provenance_note}

### Blended peer statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(blended_stats_rows)}

Blended peer medians are broad reference points, not final valuation anchors.

### Core comparable statistics excluding target

| Metric | Median | Mean | Min | Max | Valid count |
| --- | ---: | ---: | ---: | ---: | ---: |
{chr(10).join(core_stats_rows)}

{core_sample_note}

Core comparable medians depend on user-provided comparability classification.

### Target relative position versus blended peers

| Metric | Target | Premium / (discount) vs median | Low-to-high percentile |
| --- | ---: | ---: | ---: |
{chr(10).join(blended_position_rows)}

### Target relative position versus core comparable median

| Metric | Target | Premium / (discount) vs core median |
| --- | ---: | ---: |
{chr(10).join(core_position_rows)}

相对位置仅描述倍数分布，不代表估值高低一定合理，也不构成买卖判断。

## Data gaps

{chr(10).join(gaps)}

## Potentially incomparable companies

{chr(10).join(comparability)}

## Input sources

{source_rows}

## Data limitations

- 本工具不验证公司业务是否真正可比，也不调整会计准则、资本结构、税率或一次性项目。
- Core comparable statistics depend entirely on user-provided peer group and comparability classifications.
- 页面快照、延迟数据或第三方估算必须保留 source status，并在研究报告中标注为 indicative / 待交叉验证。
- 同业均值或中位数不能直接推出目标公司的研究状态或买卖结论。

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
        report = build_report(args.input, rows, args.target_ticker)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote peer comps report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
