# Peer Comps Input Schema

## Purpose

为 `scripts/peer_comps_table.py` 提供本地同业市场与财务数据，生成原始对比、统计区间和目标公司相对位置。

## Required fields

CSV 必须包含：

`ticker`, `company`, `currency`, `amount_unit`, `per_share_unit`, `reporting_period`, `basis`, `market_cap`, `enterprise_value`, `revenue_ttm`, `ebitda_ttm`, `net_income_ttm`, `free_cash_flow_ttm`, `revenue_growth_forward`, `gross_margin`, `operating_margin`, `ev_sales_ttm`, `ev_ebitda_ttm`, `pe_ttm`, `forward_pe`, `p_fcf_ttm`, `source`, `timestamp`, `market_session`, `source_status`

文本身份字段不得为空。数值字段和倍数字段可以为空。

## Optional fields

可选字段：

- `forward_revenue_growth_source`：`consensus`, `company_guidance`, `derived_from_ps_multiple`, `analyst_assumption`, `unknown`。
- `peer_group`：`core_ai_accelerator`, `ai_networking_connectivity`, `diversified_semiconductor`, `semiconductor_equipment`, `foundry`, `ip_licensing`, `handset_mobile`, `optical_connectivity`, `reference_only`, `other`。
- `comparability_status`：`core`, `adjacent`, `reference`, `weak`, `exclude`, `unknown`。
- `comparability_notes`：解释业务模式、规模、margin、地域或会计口径差异。
- `include_in_core_stats`：`true` 或 `false`。

运行时必须通过 `--target-ticker` 指定目标公司。

## Field definitions

| Field group | Fields | Meaning |
| --- | --- | --- |
| Identity | `ticker`, `company` | 公司身份 |
| Basis | `currency`, `amount_unit`, `per_share_unit`, `reporting_period`, `basis` | 币种、单位、期间、会计口径和估算属性 |
| Market value | `market_cap`, `enterprise_value` | 市值和企业价值 |
| Operating data | `revenue_ttm`, `ebitda_ttm`, `net_income_ttm`, `free_cash_flow_ttm` | TTM 基础财务数据 |
| Forward / quality | `revenue_growth_forward`, `gross_margin`, `operating_margin` | 预期增长和利润率 |
| Multiples | `ev_sales_ttm`, `ev_ebitda_ttm`, `pe_ttm`, `forward_pe`, `p_fcf_ttm` | 估值倍数 |
| Provenance | `source`, `timestamp`, `market_session`, `source_status` | 来源和市场数据状态 |
| Growth provenance | `forward_revenue_growth_source` | Forward revenue growth 的来源类型 |
| Comparability | `peer_group`, `comparability_status`, `comparability_notes`, `include_in_core_stats` | 分组、可比性判断、理由和是否纳入核心统计 |

## Units and currency rules

- 同一公司的 market cap、EV、revenue、EBITDA、net income 和 FCF 必须使用相同 `amount_unit`。
- `per_share_unit` 用于保留每股数据单位语境，即使当前工具不展示股价。
- 不同公司可使用不同币种，但脚本不做汇率转换，并会提示可比性风险。
- Margin 和 growth 输入小数，例如 `0.18` 表示 18%。
- 倍数输入纯数字，例如 `24.5`，不带 `x`。

## Timestamp rules

- 市场数据必须使用带时区 ISO 8601，例如 `2026-06-24T16:00:00-04:00`。
- 无法确认更新时间时填写 `timestamp 未验证`。
- `market_session` 使用 `regular close`, `pre-market`, `after-hours`, `intraday` 或明确页面快照。

## Source status rules

二级公开页面应标记 `indicative` 或 `partially_verified`。推荐枚举：`verified`, `partially_verified`, `unverified`, `indicative`, `fictional_sample`。

## Example row

```csv
ticker,company,currency,amount_unit,per_share_unit,reporting_period,basis,market_cap,enterprise_value,revenue_ttm,ebitda_ttm,net_income_ttm,free_cash_flow_ttm,revenue_growth_forward,gross_margin,operating_margin,ev_sales_ttm,ev_ebitda_ttm,pe_ttm,forward_pe,p_fcf_ttm,source,timestamp,market_session,source_status,forward_revenue_growth_source,peer_group,comparability_status,comparability_notes,include_in_core_stats
EXMP,Example Semiconductor Corp.,USD,USD millions,USD/share,FY2025 TTM,TTM GAAP; USD millions; market snapshot,12000,12500,2200,520,250,410,0.18,0.60,0.17,,,,32,,Fictional market snapshot,2026-06-24T16:00:00-04:00,regular close,fictional_sample,analyst_assumption,core_ai_accelerator,core,Target company,false
```

## Validation notes

- 缺失的 EV/Sales、EV/EBITDA、P/E 和 P/FCF 可由基础字段计算。
- Forward P/E 没有 forward earnings 时不能计算。
- 负 EBITDA、净利润或 FCF 不用于对应正倍数统计。
- Mean、Median、Min 和 Max 只基于有效正倍数。
- Blended statistics 使用 target 以外全部有效正倍数；它只是宽泛参考。
- Core statistics 还要求 `include_in_core_stats == true`，并完全依赖用户提供的可比性分类。
- Core comparable 少于 2 家时，输出必须提示样本过小。
- 目标公司即使错误标记为 `include_in_core_stats=true`，统计时仍会被排除。
- `NaN` 和 `Infinity` 会被拒绝。
- 目标公司相对位置是描述性统计，不能直接转化为买卖建议。
- `derived_from_ps_multiple` 必须在输出中标记为机械反推；它不是 sourced consensus growth，也不是公司指引或分析师一致预期。
