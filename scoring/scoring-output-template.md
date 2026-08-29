# Scoring Output Template

## 使用规则

- 不允许留空字段。
- 未知内容必须明确写：`未披露`、`未验证`、`暂无可靠来源`、`不适用` 或 `待核实`。
- 所有关键未知项必须进入 `下一步动作` 或 `来源附录` 的待核实问题。
- 所有市场数据和估值倍数必须注明 source + timestamp + market session + currency；估值倍数还必须注明 trailing / forward / TTM / NTM 口径。
- 最终状态必须使用 `references/status-taxonomy.md` 定义的枚举。
- 输出最终状态前必须先检查三项否决。
- 所有状态都是研究流程状态，不是交易建议；`小仓位跟踪` 不是仓位建议。
- 九项评分每项都必须包含 `Score 1-5`、`Evidence`、`Confidence: High / Medium / Low` 和 `Missing evidence`。
- 如果证据不足，不允许给高置信度高分；如果某项无法判断，写 `无法可靠评分`，不要强行给分。

## 研究对象

- Ticker：
- Exchange：
- Company：
- Reporting currency：
- Latest reporting period：
- Research objective：
- Investment horizon：
- Data date：

## 是否触发否决项

| 否决项 | 是否触发 | 证据 | 处理 |
| --- | --- | --- | --- |
| 商业模式不可理解或收入真实性无法验证 |  |  |  |
| 财务质量明显恶化且无法解释 |  |  |  |
| 估值严重依赖不可验证的远期叙事 |  |  |  |

结论：

```text
若任一否决项触发，最终状态只能是排除、数据不足，暂不判断，或观察池；使用观察池时必须说明重大风险和待核实事项。
```

## 九项评分表

| 项目 | Score 1-5 | 权重 | 加权分 | Evidence | Confidence | Missing evidence | 主要风险 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 行业空间 |  |  |  |  | High / Medium / Low |  |  |
| 竞争格局 |  |  |  |  | High / Medium / Low |  |  |
| 商业模式 |  |  |  |  | High / Medium / Low |  |  |
| 护城河 |  |  |  |  | High / Medium / Low |  |  |
| 管理层 |  |  |  |  | High / Medium / Low |  |  |
| 财务质量 |  |  |  |  | High / Medium / Low |  |  |
| 增长确定性 |  |  |  |  | High / Medium / Low |  |  |
| 估值安全边际 |  |  |  |  | High / Medium / Low |  |  |
| 催化剂与风险收益比 |  |  |  |  | High / Medium / Low |  |  |

无法判断示例：

```text
Score：无法可靠评分；Evidence：暂无可靠来源；Confidence：Low；Missing evidence：需要公司披露 backlog、customer concentration 或 segment margin。
```

## 总分

- 原始总分：
- 加权总分：
- 分数区间解释：
- 评分置信度：

## 权重说明

默认等权。若调整权重，必须说明原因。

示例：

```text
本次提高估值安全边际和财务质量权重，因为公司处于周期高位，peak earnings 风险较高。
```

## 强项

1.
2.
3.

## 弱项

1.
2.
3.

## 最大不确定性

-

## 结论状态

只能选择：

- 排除
- 观察池
- 候选
- 深入研究
- 小仓位跟踪
- 持仓复核
- 等待更好价格
- 数据不足，暂不判断

状态：

理由：

## 下一步动作

- 需要补充的来源：
- 需要验证的指标：
- 下次复核触发条件：
- 需要建立的估值或同业表：

## 来源附录

-
