# Financials Input Schema

## Purpose

为 `scripts/ratio_calculator.py` 提供按时间顺序排列的本地财务数据。脚本只计算比率，不验证原始披露。

## Required fields

CSV 必须包含以下列名。文本身份字段不得为空；数值字段允许为空，但对应指标将输出 `无法计算`。

`period`, `currency`, `amount_unit`, `per_share_unit`, `basis`, `revenue`, `gross_profit`, `operating_income`, `net_income`, `operating_cash_flow`, `capital_expenditure`, `cash_and_equivalents`, `total_debt`, `total_assets`, `shareholders_equity`, `shares_diluted`, `stock_based_compensation`, `accounts_receivable`, `inventory`, `current_assets`, `current_liabilities`, `source`, `source_date`, `source_status`

## Optional fields

支持以下可选字段：`short_term_investments`, `cash_and_short_term_investments`, `net_debt_basis`, `special_items_notes`, `normalized_net_income`, `normalized_eps`, `normalized_operating_income`, `goodwill`, `intangible_assets`, `acquisition_related_amortization`, `restructuring_and_integration_costs`, `acquisition_related_costs`, `acquisition_accounting_notes`。

## Field definitions

| Field | Required value | Meaning | Example |
| --- | --- | --- | --- |
| `period` | Yes | 财务期间，按早到晚排列 | `FY2025` |
| `currency` | Yes | ISO 币种或明确报告币种 | `USD` |
| `amount_unit` | Yes | 汇总金额单位 | `USD millions` |
| `per_share_unit` | Yes | 每股数据单位 | `USD/share` |
| `basis` | Yes | 会计口径、金额单位和必要重述说明 | `GAAP; USD millions` |
| `revenue` | No | 收入 | `2200` |
| `gross_profit` | No | 毛利润 | `1320` |
| `operating_income` | No | 营业利润 | `374` |
| `net_income` | No | 归属所选口径的净利润 | `250` |
| `operating_cash_flow` | No | 经营现金流 | `410` |
| `capital_expenditure` | No | 资本开支现金流出绝对值 | `110` |
| `cash_and_equivalents` | No | 现金及现金等价物 | `540` |
| `short_term_investments` | No | 可纳入净债务口径的短期投资或 marketable securities | `60` |
| `cash_and_short_term_investments` | No | 用户已核实并合并的现金及短期投资；优先于前两项 | `600` |
| `net_debt_basis` | No | 净债务现金口径说明 | `cash_plus_short_term_investments` |
| `total_debt` | No | 有息债务总额 | `590` |
| `total_assets` | No | 总资产 | `3800` |
| `shareholders_equity` | No | 股东权益 | `2070` |
| `shares_diluted` | No | 稀释后加权平均股数 | `105` |
| `stock_based_compensation` | No | 股权激励费用 | `75` |
| `accounts_receivable` | No | 应收账款 | `360` |
| `inventory` | No | 存货 | `230` |
| `current_assets` | No | 流动资产 | `1260` |
| `current_liabilities` | No | 流动负债 | `610` |
| `source` | Yes | 数据来源名称或文件 | `FY2025 10-K` |
| `source_date` | Yes | 来源发布日期或获取日期 | `2026-03-01` |
| `source_status` | Yes | 来源核实状态 | `verified` |
| `special_items_notes` | No | 重大一次性、非经营或会计特殊项目说明 | `Gain on divestiture affects GAAP net income` |
| `normalized_net_income` | No | 有来源、可复核的标准化净利润 | `275` |
| `normalized_eps` | No | 有来源、可复核的标准化 EPS | `2.62` |
| `normalized_operating_income` | No | 有来源、可复核的标准化营业利润 | `410` |
| `goodwill` | No | 期末 goodwill | `900` |
| `intangible_assets` | No | 期末 acquired and other intangible assets | `420` |
| `acquisition_related_amortization` | No | 当期 acquisition-related intangible amortization | `85` |
| `restructuring_and_integration_costs` | No | 当期 restructuring / integration costs | `24` |
| `acquisition_related_costs` | No | 当期 acquisition transaction-related costs | `8` |
| `acquisition_accounting_notes` | No | 并购范围、口径、减值风险与有机增长可比性说明 | `Goodwill includes prior acquisitions; no impairment recognized` |

## Units and currency rules

- 同一行所有汇总金额必须使用 `amount_unit`，例如全部为 `USD millions`。
- `currency` 只记录币种；`per_share_unit` 单独记录每股单位。
- 脚本不做汇率转换或单位缩放。
- `capital_expenditure` 推荐填正数现金流出；脚本会取绝对值。
- Net debt 的 cash base 优先使用 `cash_and_short_term_investments`，其次为 `cash_and_equivalents + short_term_investments`，最后才是 `cash_and_equivalents`。
- `net_debt_basis` 推荐枚举：`cash_only`, `cash_plus_short_term_investments`, `user_provided_cash_and_investments`, `unknown`。
- 除 `unknown` 外，`net_debt_basis` 必须与实际触发的字段优先级一致；冲突时脚本会报错。
- 纳入 short-term investments 前，必须确认其流动性、期限、限制出售条款和与债务口径的匹配性。
- 比率字段使用小数计算，不输入百分号。
- 并购会计金额使用同一 `amount_unit`。脚本计算 goodwill / assets、intangibles / assets、acquisition amortization / revenue、restructuring and integration costs / revenue，以及 acquisition-related costs / revenue。
- `acquisition_related_amortization`、`restructuring_and_integration_costs` 和 `acquisition_related_costs` 必须来自可核实披露或清楚标注的手工分类；工具不会自动判定其是否为非经常性项目。

## Timestamp rules

- `source_date` 使用 `YYYY-MM-DD` 或包含时区的 ISO 8601 时间。
- 若日期无法验证，不应留空；使用 `timestamp 未验证`，并将该问题带入研究报告。

## Source status rules

推荐枚举：`verified`, `partially_verified`, `unverified`, `indicative`, `fictional_sample`。

## Example row

```csv
period,currency,amount_unit,per_share_unit,basis,revenue,gross_profit,operating_income,net_income,operating_cash_flow,capital_expenditure,cash_and_equivalents,total_debt,total_assets,shareholders_equity,shares_diluted,stock_based_compensation,accounts_receivable,inventory,current_assets,current_liabilities,source,source_date,source_status,short_term_investments,cash_and_short_term_investments,net_debt_basis,special_items_notes,normalized_net_income,normalized_eps,normalized_operating_income,goodwill,intangible_assets,acquisition_related_amortization,restructuring_and_integration_costs,acquisition_related_costs,acquisition_accounting_notes
FY2025,USD,USD millions,USD/share,GAAP; USD millions,2200,1320,374,250,410,110,540,590,3800,2070,105,75,360,230,1260,610,Fictional example filing,2026-03-01,fictional_sample,,600,user_provided_cash_and_investments,Fictional restructuring charge,275,2.62,410,900,420,85,24,8,Fictional acquisition-accounting sample
```

## Validation notes

- 缺少列名时脚本终止并列出缺失字段。
- 文本身份字段为空时脚本终止。
- 非法数字会报告行号和字段名。
- `NaN` 和 `Infinity` 会被拒绝。
- 只有一期数据时，Revenue growth 和 Diluted shares trend 输出 `无法计算`。
- ROE 与 ROA 使用期末余额，不等同于使用平均资产或平均权益的标准化口径。
- `special_items_notes` 非空时，输出会警告 raw GAAP profitability may require normalization。
- 只有提供 `normalized_net_income` 时才计算 normalized net margin、ROE 和 ROA；工具不会自行发明 normalized values。
- 并购会计字段均为可选；缺失时脚本明确写未计算，不会从资产负债表差额反推。
- 并购会计比率保留 reported evidence，不自动把相关费用视为非经常性，也不替代 organic growth、impairment trigger 或 ROIC 分析。
- 负数 net debt 表示 net cash，不是输入错误；输出会同时显示数值和 `Net cash` 解释。
- 如果可选投资字段均缺失，脚本仍可运行，并使用 `cash_only` 口径。
