# Valuation Input Schema

## Purpose

为 `scripts/implied_expectations.py` 提供本地市场价值、经营数据和成熟期倍数假设，反推当前估值要求的收入、净利润和 FCF scale-up。

## Required fields

CSV 必须包含：

`ticker`, `company`, `currency`, `amount_unit`, `per_share_unit`, `reporting_period`, `basis`, `current_price`, `market_cap`, `enterprise_value`, `revenue_ttm`, `revenue_ntm`, `gross_margin`, `operating_margin`, `free_cash_flow_ttm`, `net_income_ttm`, `diluted_shares`, `ev_sales_current`, `target_ev_sales_mature`, `pe_current`, `target_pe_mature`, `p_fcf_current`, `target_p_fcf_mature`, `years_to_maturity`, `source`, `timestamp`, `market_session`, `source_status`

文本身份字段和 `years_to_maturity` 不得为空；其他数值字段允许为空，但对应框架会输出无法计算与缺失字段。

## Optional fields

- `normalized_net_income_ttm`：有来源、可复核的 TTM normalized net income。
- `normalized_eps_ttm`：用于展示的 normalized EPS context，不直接替代 net-income scale-up。
- `earnings_basis`：`reported_gaap`, `normalized`, `non_gaap`, `adjusted`, `unknown`。
- `earnings_basis_notes`：特殊项目、reconciliation 缺口或口径说明。

可用多行分析多家公司或多组假设。

## Field definitions

| Field | Meaning |
| --- | --- |
| `current_price` | 当前股价快照 |
| `amount_unit`, `per_share_unit` | 汇总金额与每股数据的显式单位 |
| `basis` | TTM/NTM、GAAP/Non-GAAP、金额单位和静态反推口径 |
| `market_cap` | 当前市值 |
| `enterprise_value` | 当前企业价值 |
| `revenue_ttm`, `revenue_ntm` | TTM 与 NTM 收入 |
| `gross_margin`, `operating_margin` | 当前利润率 |
| `free_cash_flow_ttm`, `net_income_ttm` | TTM FCF 与净利润 |
| `normalized_net_income_ttm`, `normalized_eps_ttm` | 有来源的 normalized earnings context |
| `earnings_basis`, `earnings_basis_notes` | 请求口径与可比性说明 |
| `diluted_shares` | 稀释股数 |
| `ev_sales_current`, `pe_current`, `p_fcf_current` | 当前倍数，可留空后由基础字段计算 |
| `target_ev_sales_mature`, `target_pe_mature`, `target_p_fcf_mature` | 用户假设的成熟期倍数 |
| `years_to_maturity` | 达到成熟期的年数 |
| `source`, `timestamp`, `market_session`, `source_status` | 来源记录 |

## Units and currency rules

- 市值、EV、收入、净利润和 FCF 必须使用相同 `amount_unit`。
- 当前股价使用 `per_share_unit`。
- Margin 使用小数。
- 倍数输入纯数字，不带 `x`。
- `current_price` 和 `diluted_shares` 仅用于保留输入语境；v0.2 的 scale-up 主要基于市值或 EV。
- 脚本不做币种换算。

## Timestamp rules

- 使用带时区 ISO 8601 时间，并记录对应 `market_session`。
- 无法确认数据更新时间时填写 `timestamp 未验证`，`source_status` 不得标记为 verified。

## Source status rules

推荐枚举：`verified`, `partially_verified`, `unverified`, `indicative`, `fictional_sample`。

## Example row

```csv
ticker,company,currency,amount_unit,per_share_unit,reporting_period,basis,current_price,market_cap,enterprise_value,revenue_ttm,revenue_ntm,gross_margin,operating_margin,free_cash_flow_ttm,net_income_ttm,diluted_shares,ev_sales_current,target_ev_sales_mature,pe_current,target_pe_mature,p_fcf_current,target_p_fcf_mature,years_to_maturity,source,timestamp,market_session,source_status,normalized_net_income_ttm,normalized_eps_ttm,earnings_basis,earnings_basis_notes
EXMP,Example Semiconductor Corp.,USD,USD millions,USD/share,FY2025 TTM / FY2026 NTM,TTM GAAP; NTM estimate; USD millions; static mature-multiple bridge,120,12000,12500,2000,2500,0.62,0.20,400,300,100,6.25,3.5,40,20,30,18,5,Fictional market and financial snapshot,2026-06-24T16:00:00-04:00,regular close,fictional_sample,330,3.30,normalized,Fictional sourced normalization bridge
```

## Validation notes

- 静态反推保持当前 EV 或 market cap 不变。
- Revenue requirement = EV / mature EV/Sales。
- Net income requirement = market cap / mature P/E。
- P/E scale-up 优先使用 `normalized_net_income_ttm`；未提供时回退到 reported GAAP net income。
- `normalized_eps_ttm` 只提供每股语境，主要 scale-up 仍使用 net income，避免股数口径不一致。
- 如果请求 normalized / non-GAAP / adjusted 口径却未提供 normalized net income，输出会明确提示回退到 reported GAAP。
- 工具不会自动生成 normalized earnings。
- FCF requirement = market cap / mature P/FCF。
- CAGR 是从 TTM 基础值到静态成熟值的机械桥接，不是预测。
- `NaN` 和 `Infinity` 会被拒绝。
- 成熟倍数必须由研究者结合行业、利率、竞争和利润质量解释。
