# DCF Assumptions Schema

## Purpose

为 `scripts/dcf_sensitivity.py` 提供本地 JSON 假设，生成简化 Bear/Base/Bull DCF 与敏感性表。

## Required fields

`company`, `ticker`, `currency`, `amount_unit`, `per_share_unit`, `reporting_period`, `basis`, `fcf_type`, `base_year_fcf`, `projection_years`, `revenue_or_fcf_growth_cases`, `discount_rates`, `terminal_growth_rates`, `net_debt`, `diluted_shares`, `source`, `source_date`, `source_status`

## Optional fields

v0.2 不读取额外字段。复杂收入、利润率、税率、营运资本和 capex 模型应在外部完成，再把得到的 FCF 路径作为假设输入。

## Field definitions

| Field | Type | Meaning |
| --- | --- | --- |
| `company` | string | 公司名称 |
| `ticker` | string | 股票代码 |
| `currency` | string | 报告币种 |
| `amount_unit` | string | 汇总金额单位，例如 `USD millions` |
| `per_share_unit` | string | 每股价值单位，例如 `USD/share` |
| `reporting_period` | string | Base-year FCF 对应期间 |
| `basis` | string | FCF、净债务和股数的口径及单位 |
| `fcf_type` | string | 仅允许 `FCFF`、`UFCF`、`FCFE` |
| `base_year_fcf` | number | 基准年度 FCF |
| `projection_years` | integer | 显式预测年数，必须大于 0 |
| `revenue_or_fcf_growth_cases` | object | `bear`, `base`, `bull` 三组逐年增长率 |
| `discount_rates` | array[number] | 敏感性折现率 |
| `terminal_growth_rates` | array[number] | 永续增长率 |
| `net_debt` | number | 净债务；净现金可用负数 |
| `diluted_shares` | number | 稀释股数，必须大于 0 |
| `source` | string | 假设或数据来源 |
| `source_date` | string | 来源日期或获取日期 |
| `source_status` | string | 核实状态 |

## Units and currency rules

- `base_year_fcf`、`net_debt` 和由模型产生的企业价值或股权价值必须使用 `amount_unit`。
- `diluted_shares` 使用与金额单位匹配的股数单位，例如金额为 millions 时股数也使用 millions。
- Implied value per share 使用 `per_share_unit`。
- 增长率、折现率、永续增长率使用小数，例如 `0.10` 表示 10%。
- 脚本不做币种换算。

## Timestamp rules

`source_date` 使用 `YYYY-MM-DD` 或 ISO 8601。无法验证时填写 `timestamp 未验证`。

## Source status rules

推荐枚举：`verified`, `partially_verified`, `unverified`, `indicative`, `fictional_sample`。

## JSON example

```json
{
  "company": "Example Semiconductor Corp.",
  "ticker": "EXMP",
  "currency": "USD",
  "amount_unit": "USD millions",
  "per_share_unit": "USD/share",
  "reporting_period": "FY2025",
  "basis": "FCFF and net debt in USD millions; diluted shares in millions",
  "fcf_type": "FCFF",
  "base_year_fcf": 1000,
  "projection_years": 5,
  "revenue_or_fcf_growth_cases": {
    "bear": [0.05, 0.04, 0.03, 0.03, 0.02],
    "base": [0.10, 0.08, 0.07, 0.06, 0.05],
    "bull": [0.15, 0.12, 0.10, 0.08, 0.06]
  },
  "discount_rates": [0.08, 0.09, 0.10, 0.11, 0.12],
  "terminal_growth_rates": [0.02, 0.025, 0.03],
  "net_debt": 500,
  "diluted_shares": 100,
  "source": "Fictional example assumptions",
  "source_date": "2026-06-24",
  "source_status": "fictional_sample"
}
```

## Validation notes

- 每个情景的增长率数量必须等于 `projection_years`。
- 每个 discount rate 必须大于每个 terminal growth rate。
- `FCFF` / `UFCF` 折现得到 enterprise value，再扣减 net debt 得到 equity value。
- `FCFE` 折现直接得到 equity value，不再扣减 net debt；enterprise value 输出为不适用。
- `OCF - capex` 通常更接近 levered FCF / FCFE，但只能作为 research approximation；研究者仍需检查利息、税、租赁和融资现金流口径。
- FCFF/UFCF 通常应匹配 WACC-style discount rate；FCFE 通常应匹配 cost-of-equity-style discount rate。
- 所有数值必须有限；JSON 布尔值不视为数字。
- Discount rate 和 terminal growth rate 必须大于 `-1`，避免无效折现或终值计算。
- DCF 将增长率直接应用于 FCF；字段名保留 `revenue_or_fcf` 是为了兼容由收入路径间接推导的 FCF 假设。
- 输出的 implied value per share 是敏感性计算结果，不是确定性目标价。
