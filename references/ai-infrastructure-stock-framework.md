# AI Infrastructure Stock Framework

本 overlay 用于 AI 产业链和 AI narrative 股票。目标是区分真实收入受益、订单受益、margin 受益、估值受益和纯叙事受益。

## 覆盖范围

- GPU。
- ASIC。
- CPU。
- HBM。
- 封装。
- 光模块。
- SerDes。
- 交换芯片。
- 网络设备。
- 数据中心电力。
- 液冷。
- 云厂商。
- 软件平台。

## 核心判断

先回答：

```text
公司是否真实受益于 AI capex？
AI 收入是否已经单独披露？
是否只是叙事受益？
需求来自训练、推理、数据中心升级，还是库存补库？
客户集中度如何？
Hyperscaler capex 是否可持续？
毛利率是否会受定制项目压缩？
竞争者是谁？
技术替代风险是什么？
当前估值隐含了多高增长？
```

## 收入口径拆分

AI 产业链研究必须先拆清楚收入证据层级：

- `disclosed AI revenue`：公司明确披露的 AI revenue、AI product revenue、AI segment revenue 或 AI ARR。
- `AI-related revenue`：公司披露与 AI demand、AI customer program、AI data center deployment 相关，但未单独给出 AI-only 金额的收入。
- `data center revenue`：公司 data center end market / segment revenue。它可以作为 AI 暴露线索，但不等于 AI-only revenue。
- `management commentary`：管理层对 AI demand、orders、design wins、customer ramps 的文字表述。
- `design wins / backlog / customer programs`：订单、backlog、RPO、客户项目、量产节点、认证进度。
- `market narrative`：媒体、分析师或市场把公司归入 AI 受益链条的说法。

硬规则：

- `data center revenue` 不等于 `AI-only revenue`。
- 如果公司只披露 data center revenue，不能直接全部视为 AI revenue。
- 如果 AI-only revenue 未单独披露，必须写：`AI-only revenue 未单独披露 / 需间接验证`。
- 不允许仅凭 `data center 增长` 直接得出 `AI 真实受益充分验证` 的结论。
- 若只有 management commentary 或 market narrative，而没有收入、订单、backlog 或客户项目验证，应标记为 `叙事受益，待验证` 或 `AI-related exposure，证据不足`。

## AI 收入验证层级

### Level 1：公司单独披露 AI 收入

证据：

- AI segment revenue。
- AI product revenue。
- AI customer revenue。
- AI backlog / RPO。
- 管理层披露可复核数据。

可信度最高，但仍需确认口径是否变化。

### Level 2：公司披露 AI 相关订单或客户

证据：

- Design win。
- 客户项目。
- AI data center deployment。
- 产品进入 AI server / cluster / networking architecture。

需要验证订单是否转化为收入、毛利率和现金流。

### Level 3：供应链或同业间接验证

证据：

- 客户 capex。
- 同业订单。
- 行业出货量。
- 供应链交叉验证。

只能作为支持性证据，不可替代公司披露。

### Level 4：叙事受益

特征：

- 公司经常提 AI，但没有 AI revenue 或订单披露。
- 股价和估值扩张快于可验证财务改善。
- 管理层措辞偏概念，缺少量化指标。

应标记为 `叙事受益，待验证`。

## 需求来源拆解

### 训练

观察：

- Large-scale GPU / accelerator clusters。
- HBM、networking、power、cooling 需求。
- Hyperscaler 和 AI lab capex。

风险：

- 训练 scaling law 放缓。
- Capex ROI 被质疑。
- 客户预算集中度过高。

### 推理

观察：

- Inference accelerator。
- Edge / cloud inference workloads。
- Unit economics and latency needs。

风险：

- 推理成本快速下降导致 ASP 压力。
- 自研 ASIC 替代通用 GPU。
- 软件优化减少硬件需求。

### 数据中心升级

观察：

- Power capacity。
- Liquid cooling。
- High-speed networking。
- Optical interconnect。
- Rack-scale architecture。

风险：

- 建设周期和电力许可延迟。
- 项目制收入波动。
- 定制化压低毛利率。

### 库存补库

观察：

- 短期订单暴增。
- Channel inventory。
- 客户提前下单。

风险：

- Double ordering。
- 后续需求真空。
- 存货减值。

## 分环节分析问题

### GPU

- AI revenue 是否单独披露？
- Supply constraint 还是 demand constraint？
- Gross margin 是否处于周期高位？
- 客户是否集中在少数 hyperscaler？
- ASIC 替代风险如何？

### ASIC

- 是 merchant silicon 还是 customer-specific ASIC？
- Design win 到量产周期多长？
- 定制项目毛利率是否低于标准产品？
- 客户是否可能转向自研或第二供应商？

### CPU

- AI server CPU attach rate 如何？
- 是否受 GPU cluster 拉动，还是被 accelerator 替代？
- Data center CPU share 是否稳定？

### HBM

- 产能、良率和 pricing 是否可持续？
- HBM 代际转换风险如何？
- 客户认证周期多长？
- Commodity memory cycle 是否掩盖 AI 增长？

### 封装

- Advanced packaging 产能是否稀缺？
- CoWoS / 2.5D / 3D packaging 供需如何？
- Capex 是否能转化为高回报？
- 客户集中度和议价能力如何？

### 光模块

- 速率升级路径是否明确？
- 800G / 1.6T 需求是否真实来自 AI clusters？
- ASP 和毛利率是否受竞争压缩？
- 客户认证和替代风险如何？

### SerDes / 交换芯片 / 网络设备

- AI cluster networking architecture 是否提升内容价值？
- Ethernet vs InfiniBand 格局如何？
- 软件栈和生态是否构成壁垒？
- Hyperscaler 是否倾向自研或白盒化？

### 数据中心电力与液冷

- 需求来自新增机房、改造，还是短期抢装？
- 项目制收入是否导致波动？
- 电力设备交付周期和 backlog 是否可见？
- 液冷技术路线是否确定？

### 云厂商

- AI capex 是否带来可见收入和利润？
- GPU utilization、pricing、depreciation pressure 如何？
- AI revenue 是新增需求还是替代原有 cloud spend？
- Capex intensity 是否压制 FCF？

### 软件平台

- AI 功能是否带来 ARPU、retention 或 seat expansion？
- 是否单独披露 AI attach rate 或 AI ARR？
- Gross margin 是否被模型推理成本压缩？
- 开源模型或平台替代风险如何？

## 估值 overlay

AI 相关公司必须回答：

- 当前估值中有多少来自可验证收入？
- 有多少来自 AI narrative multiple expansion？
- 当前估值隐含多少 revenue CAGR、margin expansion 和 terminal profitability？
- 如果 hyperscaler capex 增速放缓，估值区间如何变化？
- 如果 AI revenue 只是周期性订单，normalized multiple 应该如何调整？

## 红旗

- AI 词频增加，但没有 AI revenue、订单或客户披露。
- 估值倍数大幅扩张，但收入和 FCF 没有同步改善。
- 客户高度集中，且客户 capex 存在削减风险。
- 管理层将所有增长都归因于 AI，但 segment 数据无法验证。
- 定制项目收入增长但毛利率下降。
- Inventory 快速上升，可能反映需求错配。
- 同业披露需求放缓，而公司仍维持过高指引。

## 输出建议

```markdown
### AI Supply Chain Overlay
- AI 暴露环节：
- 收入口径拆分：disclosed AI revenue / AI-related revenue / data center revenue / management commentary / design wins or backlog / market narrative
- AI 收入披露层级：
- AI-only revenue 是否单独披露：是 / 否；若否，写 `未单独披露 / 需间接验证`
- 真实收入受益：
- 叙事受益：
- Data center revenue 是否被误当作 AI revenue：
- 需求来源：训练 / 推理 / 数据中心升级 / 库存补库
- Design wins / backlog / customer programs：
- 客户集中度：
- 竞争与替代风险：
- 毛利率影响：
- 当前估值隐含预期：
- Next checks：
```
