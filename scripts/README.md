# Local Data Tools

v0.2 工具层读取用户或 Agent 准备的本地 CSV / JSON，输出可审计 Markdown。脚本不联网、不接 API、不读取 API key、不连接券商，也不执行交易或下单。

v0.2.x 本地工具层已经完成。v0.3.1 提供 local-file evidence packaging；v0.3.2
提供一个显式 SEC URL、GET-only、evidence-only 的窄范围 adapter。任何 adapter 都必须先
把 raw evidence、manifests 和经审查的 normalized CSV / JSON 写入本地，再调用这些脚本。
脚本本身不会改成 live data client。

所有示例数据均为虚构数据，不可用于真实投资判断。

## 运行环境

- Python 3
- 仅使用标准库
- 从仓库根目录运行以下命令
- `--input` 与 `--output` 必须是不同文件，避免覆盖原始输入。

## 1. Financial ratio calculator

读取 `schemas/financials_input_schema.md` 定义的 CSV，计算增长、利润率、现金流、资产负债表和稀释指标。v0.2.3 支持 cash only、cash plus short-term investments 和用户合并 cash/investments 三种 net debt basis。v0.2.4 增加 goodwill、intangible assets、acquisition amortization、restructuring / integration costs 和 acquisition-related costs 的结构化检查。

```bash
python3 goodluck-stock-research/scripts/ratio_calculator.py \
  --input goodluck-stock-research/examples/data/example_financials.csv \
  --output goodluck-stock-research/examples/outputs/example_ratio_output.md
```

## 2. DCF sensitivity

读取 `schemas/assumptions_schema.md` 定义的 JSON，生成 Bear/Base/Bull FCF 路径和折现率/永续增长率敏感性表。必须显式指定 `fcf_type`：

- `FCFF` / `UFCF`：折现得到 enterprise value，再扣减 net debt 得到 equity value。
- `FCFE`：折现直接得到 equity value，不再扣减 net debt。

```bash
python3 goodluck-stock-research/scripts/dcf_sensitivity.py \
  --input goodluck-stock-research/examples/data/example_assumptions.json \
  --output goodluck-stock-research/examples/outputs/example_dcf_sensitivity_output.md
```

## 3. Peer comps table

读取 `schemas/peer_comps_input_schema.md` 定义的 CSV。必须用 `--target-ticker` 指定目标公司。输出同时保留 blended statistics 和由 `include_in_core_stats` 控制的 core comparable statistics。

```bash
python3 goodluck-stock-research/scripts/peer_comps_table.py \
  --input goodluck-stock-research/examples/data/example_peer_comps.csv \
  --output goodluck-stock-research/examples/outputs/example_peer_comps_output.md \
  --target-ticker EXMP
```

## 4. Implied expectations

读取 `schemas/valuation_input_schema.md` 定义的 CSV，静态反推成熟期倍数要求的 revenue、net income / EPS 和 FCF scale-up。P/E bridge 优先使用显式提供的 normalized net income，否则回退到 reported GAAP 并显示 earnings-basis caution。

```bash
python3 goodluck-stock-research/scripts/implied_expectations.py \
  --input goodluck-stock-research/examples/data/example_valuation_inputs.csv \
  --output goodluck-stock-research/examples/outputs/example_implied_expectations_output.md
```

## 输出位置

示例命令将结果写入 `goodluck-stock-research/examples/outputs/`。也可以通过 `--output` 指定其他本地 Markdown 路径；脚本会创建不存在的父目录。

## Future adapter boundary

- Adapter output 只能是 evidence package、normalized input paths、warnings、errors 和 unresolved fields。
- Adapter 不得输出 investment conclusion、research status、target price 或 portfolio action。
- Scripts 继续只读取显式 `--input` 本地文件，并写入显式 `--output` Markdown。
- Adapter provenance 不能替代脚本 input source fields；normalized files 仍必须保留 source、period、currency、units 和 timestamps。
- v0.3.2 SEC adapter 只保存官方 filing evidence，不会直接调用 scripts 或填充
  normalized financial inputs。

## 数据限制

- 脚本只保证字段校验和计算逻辑可审计，不保证输入数据准确。
- 数值必须是有限数字；`NaN`、`Infinity` 和 JSON 布尔值不能作为数值输入。
- 输入必须保留 source、basis、reporting period、currency、timestamp 或 source date、market session（适用时）和 source status。
- 输入必须显式记录 `amount_unit` 和 `per_share_unit`，例如 `USD millions` 与 `USD/share`。
- DCF 输入必须使 `fcf_type`、discount rate 和估值桥一致；`OCF - capex` 只能作为 FCFE / levered FCF 的 research approximation，不能自动视为严格定义。
- Ratio 输入如存在重大特殊项目，应填写 `special_items_notes`；normalized metrics 只能使用有来源的输入值。
- 并购驱动公司应填写可核实的 acquisition-accounting fields；工具计算相关资产和费用比率，但不会自动把这些项目认定为非经常性，也不会替代 organic growth、impairment risk 或 ROIC 判断。
- Ratio net debt 必须说明 cash base；纳入短期投资前需确认流动性和限制条件。
- Peer forward revenue growth 如由 P/S 与 forward P/S 反推，必须标记 `derived_from_ps_multiple`，不得称为 consensus。
- Peer core statistics 完全依赖用户提供的分组和可比性判断，不能替代人工筛选。
- Implied expectations 不会生成 normalized earnings；缺少 sourced normalization 时继续使用 GAAP 并提示 caution。
- 页面快照或二级数据应标记 `indicative` / `待交叉验证`。
- 计算结果只能作为研究报告辅助证据，不能替代原始 filing、研究判断、bear case、kill criteria 或三否决检查。
- DCF implied value per share、同业倍数和市场隐含预期不是目标价承诺或买卖信号。
