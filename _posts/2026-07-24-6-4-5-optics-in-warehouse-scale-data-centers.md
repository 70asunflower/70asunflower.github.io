---
title: "6.4.5 Optics in warehouse-scale data centers"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：6.4.5 Optics in warehouse-scale data centers。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.4.5 Optics in warehouse-scale data centers。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.4.5 Optics in warehouse-scale data centers

下面这一节 **6.4.5 Optics in warehouse-scale data centers** 虽然篇幅不长，但它把前面 6.4.3 和 6.4.4 中反复出现的“光互连成本”问题具体化了。

这一节的核心可以概括为：

> **数据中心内部互连不是简单地“越快越好”或“全用光纤”，而是根据距离、速率、成本、功耗、体积、可维护性和故障容忍度，选择最合适的互连介质：铜缆、AOC、并行光纤、可插拔光模块和 WDM。**

---

### 1. 这一节在 6.4 Networking 中的位置

前面几节讲的是：

- 6.4.1：从 tray 到 planet 的网络旅程；
- 6.4.2：主机网络和 SmartNIC/IPU；
- 6.4.3：Clos/fat-tree 集群网络；
- 6.4.4：OCS 和 spine-less networking；
- 6.4.5：数据中心内部互连的物理介质选择。

也就是说，6.4.5 讲的是网络架构最底层的物理基础：

```text
电信号
光信号
铜缆
光纤
光模块
连接器
波分复用
链路距离
端口形态
```

这些看似“硬件细节”，但实际上直接决定：

- 网络成本；
- 功耗；
- 机架布线；
- 故障率；
- 可维护性；
- 升级能力；
- 网络拓扑；
- OCS 可行性；
- TCO。

---

### 2. 数据中心互连介质的基本层次

这一节实际上给出了一个从短距到长距的互连介质层次。

可以整理为：

```text
机架内短距
  ↓
铜缆 copper / DAC

机架内或 row 内稍长距离
  ↓
AOC，Active Optical Cable

短距光链路，约 100m
  ↓
parallel fiber optics

更长距离或 OCS 场景
  ↓
WDM，Wavelength Division Multiplexing
```

核心思想是：

> 能用铜就用铜，铜不够再用 AOC，再不够用并行光纤，更远或更省光纤时用 WDM。

---

### 3. 铜链路：便宜、低功耗，但距离越来越短

原文说：

> Interconnects within a data center use copper links where possible because they’re cheaper and more power efficient.

铜缆的优点非常明确：

1. **便宜**

   - 不需要激光器；
   - 不需要光电转换；
   - 结构简单；
   - 成本低。
2. **功耗低**

   - 无源铜缆几乎不耗电；
   - 有源铜缆功耗也通常低于光模块。
3. **延迟低**

   - 电信号直接传输；
   - 没有光模块 DSP 的额外延迟。
4. **维护简单**

   - 连接器成熟；
   - 不需要清洁光纤端面那么谨慎；
   - 故障排查相对简单。

---

#### 3.1 但高速铜缆距离越来越短

原文：

> However, as link speeds increase, the maximum copper cable length decreases so that today, copper links are only viable inside a rack, for NIC to ToR links and switch-to-switch links within densely packed switch racks.

随着速率提升，例如：

```text
10G → 25G → 50G → 100G → 200G → 400G → 800G
```

铜缆面临：

- 更高插入损耗；
- 更严重信号衰减；
- 更高串扰；
- 更严格均衡；
- 更短线缆长度；
- 更粗线缆；
- 更重；
- 更难布线。

所以在高速网络中，铜缆通常只适合：

```text
机架内
```

例如：

- NIC 到 ToR；
- 机架内 switch-to-switch；
- 高密度交换架内部连接；
- 服务器到机架内 PCIe fabric 或管理网络。

---

#### 3.2 为什么机架内适合铜？

因为机架内距离通常很短：

```text
几十厘米到两三米
```

这个距离内铜缆仍然可以：

- 保持信号完整；
- 成本最低；
- 功耗最低；
- 布线可行。

但如果跨机架、跨 row、跨 aggregation block，铜缆就不太现实了。

---

### 4. AOC：Active Optical Cable，有源光缆

原文说：

> Active optical cables AOC have copper connectors on both ends. Optoelectronic modules in the connector heads convert electrical signals into light.

AOC 是一种介于铜缆和传统光模块之间的互连方式。

---

#### 4.1 AOC 的结构

AOC 的特点是：

```text
两端是铜连接器
连接器内部有光电转换模块
中间是光纤
```

也就是说：

```text
设备电接口
  ↓
AOC 连接器内电转光
  ↓
光纤传输
  ↓
AOC 连接器内光转电
  ↓
设备电接口
```

从设备角度看，它像铜缆一样插入电接口。

从传输介质看，它中间用的是光纤。

---

#### 4.2 AOC 为什么比传统光模块便宜？

原文：

> Since the optical interfaces are fully closed, they are cheaper than optical transceivers.

传统光模块通常需要：

- 可插拔光收发器；
- 光纤连接器；
- 光纤跳线；
- 暴露的光纤端面；
- 清洁和维护；
- 更高测试成本。

AOC 的光学接口通常是：

```text
工厂封闭
整体线缆
不需要用户接触光纤端面
```

因此：

- 成本更低；
- 安装更简单；
- 污染风险更低；
- 维护更简单；
- 可靠性较好。

---

#### 4.3 AOC 的用途

原文：

> AOCs are typically used as alternatives to copper links to extend the reach and reduce the bulk of copper cables. They are used within a row.

AOC 主要用于：

```text
铜缆距离不够
但还不需要复杂光模块
```

的场景。

例如：

- 机架之间短距连接；
- row 内连接；
- ToR 到邻近交换机；
- 服务器到稍远 ToR；
- 高密度交换机之间的短距互连。

AOC 相比铜缆的优势：

- 距离更长；
- 线缆更轻；
- 线缆更细；
- 弯曲半径更好；
- 布线更整洁；
- 适合高密度机架。

---

### 5. 可插拔光模块：QSFP、QSFP-DD、OSFP

原文说：

> Within the data center, optical links use different kinds of optics depending on distance, to optimize cost. Each switch port has a pluggable optic module using formats such as QSFP, QSFP-DD, or OSFP to support the necessary configurations and allow for replacement on failure.

这里讲的是数据中心光模块的标准化形态。

---

#### 5.1 为什么要可插拔光模块？

可插拔光模块的好处是：

1. **按需选择距离和速率**

   - 短距用短距模块；
   - 长距用长距模块；
   - 不同链路不同配置。
2. **故障可替换**

   - 光模块坏了可以单独换；
   - 不必换整根线缆或整个交换机。
3. **多厂商生态**

   - 降低成本；
   - 提高供应弹性；
   - 避免锁定。
4. **升级灵活**

   - 同一交换机端口可以适配不同光模块；
   - 便于速率演进。

---

#### 5.2 QSFP、QSFP-DD、OSFP 的直觉理解

这些是光模块和电接口的外形/通道标准。

可以粗略理解：

|形态|通道数|典型特点|
| ---------| --------: | ------------------------|
|QSFP|4 lanes|较早的高速可插拔形态|
|QSFP-DD|8 lanes|双密度，兼容 QSFP 生态|
|OSFP|8 lanes|更大空间，更好散热|

随着每 lane 速率提升，这些形态支持的总带宽也不断提高。

例如不同代际下可能支持：

```text
40G
100G
200G
400G
800G
```

具体取决于：

- 每 lane 速率；
- 调制方式；
- FEC；
- 光模块类型；
- 交换机 SerDes 能力。

---

### 6. 短距并行光纤：parallel fiber optics

原文说：

> Short reach optics using parallel fiber are used for the next level optics with a reach of around 100 m.

短距光链路通常使用：

```text
parallel fiber
```

也就是并行光纤。

---

#### 6.1 什么是并行光纤？

并行光纤指：

> 每个 lane 使用一根或一对光纤，多个 lane 并行传输。

例如：

```text
4 lanes → 4 对光纤
8 lanes → 8 对光纤
```

典型例子包括：

- 40G-SR4；
- 100G-SR4；
- 200G-SR；
- 400G-SR8；
- 某些 DR 类并行单模方案。

它们通常用于短距离，例如：

```text
约 100m
```

---

#### 6.2 并行光纤的优点

##### 1. 光器件相对简单

每个 lane 一个激光器/探测器。

不需要复杂的波分复用器。

##### 2. 成本适合短距

短距数据中心内部不需要长距激光器件。

可以使用成本较低的光学方案。

##### 3. 适合高密度交换

并行 lane 可以和交换机端口 breakout 配合。

---

#### 6.3 并行光纤的缺点

##### 1. 光纤数量多

lane 越多，光纤越多。

例如 8 lane 可能需要较多光纤芯。

##### 2. 线缆体积大

光纤数量增加会导致：

- 线缆更粗；
- 布线更复杂；
- 配线架更拥挤；
- 安装成本上升。

##### 3. 距离有限

通常适合约 100m 级别。

更长距离需要其他方案。

---

### 7. ToR 到 aggregation blocks 为什么常用短距并行光？

原文说：

> They are often used for ToR to aggregation blocks, where the reach is short and lane breakout/shuffling is needed for better fault tolerance.

ToR 到 aggregation block 的链路通常有几个特点：

1. 距离不长；
2. 带宽需求高；
3. 端口数量多；
4. 需要故障容忍；
5. 需要灵活 breakout；
6. 需要 lane shuffling。

所以短距并行光非常适合。

---

#### 7.1 lane breakout 是什么？

lane breakout 指：

> 把一个高速端口的多个 lane 拆成多个低速端口。

例如：

```text
1 × 100G
→ 4 × 25G
```

或者：

```text
1 × 400G
→ 4 × 100G
```

或者：

```text
1 × 800G
→ 8 × 100G
```

这可以提高端口灵活性。

例如一个 aggregation 端口可以连接多个 ToR。

---

#### 7.2 lane shuffling 是什么？

lane shuffling 可以理解为：

> 重新排列或分配 lane，以提高端口利用率和故障容忍度。

例如某个 lane 或某根光纤故障时，可以通过重新分配 lane：

- 避开故障 lane；
- 使用备用光纤；
- 降低链路速率但保持可用；
- 重新组合端口；
- 减少更换硬件的次数。

这对大规模运维很重要。

因为在数万端口的网络中，不可能一有故障就立即人工更换所有部件。

系统需要能够：

```text
降级运行
重新调度
等待维护窗口
```

---

### 8. WDM：波分复用

原文说：

> For longer reaches, and for cases that involve OCSs, wavelength division multiplexing WDM is used, where each fiber carries multiple colors of light is used to reduce fiber cost and bulk and make more efficient use of OCS switch ports.

WDM 是更长距离和 OCS 场景中的关键技术。

---

#### 8.1 什么是 WDM？

WDM，Wavelength Division Multiplexing，波分复用。

它的核心思想是：

> 在一根光纤中同时传输多个不同波长的光信号。

不同波长可以理解为不同“颜色”的光。

例如：

```text
λ1 → 100G
λ2 → 100G
λ3 → 100G
λ4 → 100G
```

一根光纤就可以承载：

```text
4 × 100G = 400G
```

---

#### 8.2 WDM 的优点

##### 1. 减少光纤数量

不用每个 lane 都单独拉一根光纤。

例如原本需要 8 根光纤，现在可能只需要 1 根或 2 根。

##### 2. 减少线缆体积

光纤数量少，线缆更细，布线更简单。

##### 3. 更适合长距离

长距离光纤成本、安装成本、管道成本都很高。

WDM 可以显著减少光纤需求。

##### 4. 更高效利用 OCS 端口

OCS 端口是稀缺资源。

如果每个 OCS 端口只承载一个 lane，效率有限。

如果每个 OCS 端口通过 WDM 承载多个波长，就可以：

```text
一个光路
多个波长通道
多个高速 lane
```

这大幅提高 OCS 端口利用率。

---

#### 8.3 WDM 的代价

WDM 也不是免费的。

它通常需要：

- 更复杂激光器；
- 更精确波长控制；
- multiplexer/demultiplexer；
- 更高成本光模块；
- 更复杂测试；
- 更高功耗；
- 更严格光功率预算。

所以 WDM 通常用于：

```text
长距离
光纤成本高
OCS 端口稀缺
需要少纤高容量
```

的场景。

---

### 9. 不同互连介质的权衡

可以把这一节整理成一张权衡表。

|互连方式|典型距离|优点|缺点|典型用途|
| -----------------------| -----------: | -----------------------------| ------------------------| ------------------------------|
|copper / DAC|机架内短距|便宜、低功耗、低延迟|高速下距离短、线缆粗重|NIC 到 ToR、机架内交换机互连|
|AOC|row 内短距|比铜更远、更轻、封闭光接口|比铜贵、整体线缆|机架间短距、row 内连接|
|parallel fiber optics|约 100m|适合短距高带宽、可 breakout|光纤数量多、体积大|ToR 到 aggregation|
|WDM optics|更长距离|少光纤、高容量、适合 OCS|光模块复杂、成本高|长距链路、OCS、跨 block|
|pluggable optics|多种距离|可替换、灵活、标准化|模块成本、功耗|交换机端口、网卡端口|

---

### 10. 为什么“根据距离选择 optics”如此重要？

原文反复强调：

> to optimize cost

这是数据中心网络设计的核心原则。

如果所有链路都用长距 WDM 光模块，会出现：

- 成本过高；
- 功耗过高；
- 不必要复杂；
- 短距链路浪费。

如果所有链路都用铜，会出现：

- 距离不够；
- 线缆过重；
- 高速信号不可行；
- 布线困难。

所以必须分层选择：

```text
最短距离：铜
稍长距离：AOC
短距光：parallel fiber
长距/少纤：WDM
```

这就是 TCO 优化。

---

### 11. 与 6.4.3 和 6.4.4 的联系

---

#### 11.1 与 6.4.3 cluster networking 的联系

6.4.3 提到：

> optics represent the largest single cost item.

6.4.5 具体解释了：

- 为什么光模块贵；
- 为什么不同距离用不同 optics；
- 为什么短距优化能降低成本；
- 为什么并行光纤和 WDM 有不同用途。

---

#### 11.2 与 6.4.4 spine-less networking 的联系

6.4.4 讲 OCS。

OCS 是光路交换，不关心速率和协议。

但 OCS 端口数量有限。

WDM 可以让每根光纤承载多个波长，从而：

```text
提高 OCS 端口利用率
减少 OCS 端口需求
减少光纤数量
```

所以 WDM 和 OCS 是互补的。

---

### 12. 与加速器网络的联系

6.3 讲 GPU/TPU 时提到：

- AI 训练需要高带宽；
- 大规模 collective communication；
- 网络成本敏感；
- 光互连非常关键。

在 AI 集群中，互连介质选择尤其重要。

例如：

- GPU 节点内：NVLink、PCIe、铜缆；
- 机架内：短距铜或 AOC；
- 机架间：并行光或 WDM；
- pod 内：高速 Ethernet/InfiniBand；
- TPU pod：ICI + OCS；
- 长距：WDM。

AI 集群的网络性能不仅取决于交换机芯片，也取决于：

```text
光模块
光纤
距离
功耗
布线
OCS
WDM
```

---

### 13. 关键术语表

|术语|含义|
| -----------------------| --------------------------------------------|
|copper link|铜链路|
|DAC|Direct Attach Cable，直连铜缆|
|AOC|Active Optical Cable，有源光缆|
|optoelectronic module|光电转换模块|
|optical transceiver|光收发模块|
|pluggable optic|可插拔光模块|
|QSFP|Quad Small Form-factor Pluggable|
|QSFP-DD|QSFP Double Density|
|OSFP|Octal Small Form-factor Pluggable|
|parallel fiber|并行光纤|
|short reach optics|短距光模块|
|WDM|Wavelength Division Multiplexing，波分复用|
|wavelength|波长|
|lane|通道|
|breakout|端口拆分|
|lane shuffling|lane 重排/调度|
|reach|链路最大传输距离|
|fiber bulk|光纤体积/数量负担|
|fault tolerance|故障容忍|
|insertion loss|插入损耗|
|link budget|链路预算|
|TCO|总拥有成本|

---

### 14. 可以用来检验理解的问题

---

#### 问题 1：为什么数据中心尽可能使用铜链路？

因为铜链路：

- 更便宜；
- 更省电；
- 延迟低；
- 维护简单；
- 不需要光电转换。

但随着速率提高，铜缆距离变短，所以高速铜链路通常只适合机架内。

---

#### 问题 2：AOC 和铜缆有什么区别？

AOC 两端使用铜连接器，但连接器内部有光电转换模块，中间使用光纤。

它比铜缆：

- 距离更长；
- 线缆更轻；
- 体积更小；

但通常比无源铜缆贵。

---

#### 问题 3：AOC 为什么比传统光模块便宜？

因为 AOC 的光学接口是封闭的，工厂集成，不需要用户直接接触光纤端面或单独插拔光收发器。

这降低了：

- 成本；
- 污染风险；
- 安装复杂度；
- 维护复杂度。

---

#### 问题 4：QSFP、QSFP-DD、OSFP 是什么？

它们都是可插拔光模块或电接口的形态标准。

区别主要在于：

- 通道数；
- 密度；
- 散热能力；
- 支持带宽；
- 兼容性。

它们使交换机端口可以灵活选择光模块，并支持故障替换。

---

#### 问题 5：短距并行光纤适合什么场景？

适合约 100m 级别短距高带宽链路。

例如：

```text
ToR 到 aggregation blocks
```

它支持 lane breakout 和 lane shuffling，有助于提高端口利用率和故障容忍度。

---

#### 问题 6：什么是 lane breakout？

lane breakout 是把一个高速端口的多个 lane 拆成多个低速端口。

例如：

```text
400G → 4 × 100G
```

这可以提高端口灵活性，连接更多设备。

---

#### 问题 7：WDM 为什么适合长距离和 OCS？

WDM 可以在一根光纤中传输多个波长，从而：

- 减少光纤数量；
- 减少线缆体积；
- 降低长距光纤成本；
- 提高 OCS 端口利用率。

因此长距离链路和 OCS 场景常用 WDM。

---

#### 问题 8：为什么不能所有链路都用同一种光模块？

因为不同链路的距离、成本、功耗、光纤数量和带宽需求不同。

短距链路用长距 WDM 会浪费成本。

长距链路用铜或并行光纤可能不可行。

所以必须根据距离和用途选择合适互连介质。

---

### 15. 这一节可以整理成的精简笔记

```text
6.4.5 Optics in warehouse-scale data centers

1. 核心观点：
   数据中心内部互连需要根据距离、速率、成本、功耗、
   体积、可维护性和故障容忍度选择合适介质。
   基本原则是：
   能用铜就用铜；
   铜不够用 AOC；
   再不够用并行光纤；
   更长距离或 OCS 场景用 WDM。

2. 铜链路：
   - 数据中心内尽可能使用铜链路；
   - 优点：便宜、功耗低、延迟低、维护简单；
   - 但随着链路速率提高，铜缆最大长度下降；
   - 如今高速铜链路主要适合机架内；
   - 常用于 NIC 到 ToR，以及密集交换架内 switch-to-switch。

3. AOC：
   - AOC 是 Active Optical Cable，有源光缆；
   - 两端是铜连接器；
   - 连接器头内有光电转换模块；
   - 中间使用光纤传输；
   - 光接口封闭，因此比传统光收发器便宜；
   - 用于替代铜链路，延长距离并减少铜缆体积；
   - 常用于 row 内短距连接。

4. 可插拔光模块：
   - 数据中心光链路根据距离使用不同 optics；
   - 每个交换端口通常使用可插拔光模块；
   - 常见形态包括 QSFP、QSFP-DD、OSFP；
   - 可插拔模块支持不同配置；
   - 故障时可单独替换；
   - 有利于多厂商生态和运维灵活性。

5. 短距并行光纤：
   - 短距光链路使用 parallel fiber；
   - reach 约 100m；
   - 常用于 ToR 到 aggregation blocks；
   - 适合短距、高带宽、多端口场景；
   - 支持 lane breakout 和 lane shuffling；
   - 可提高端口利用率和故障容忍度。

6. lane breakout 和 lane shuffling：
   - breakout：
       将一个高速端口拆成多个低速端口，
       例如 400G 拆成 4 × 100G；
   - shuffling：
       重新排列或分配 lane，
       以避开故障 lane、使用备用光纤或重组端口；
   - 二者都有助于提高大规模网络的灵活性和可维护性。

7. WDM：
   - WDM 是 Wavelength Division Multiplexing，波分复用；
   - 每根光纤携带多个波长的光；
   - 可减少光纤数量和线缆体积；
   - 适合更长距离链路；
   - 也适合 OCS 场景；
   - 能更高效利用 OCS 端口。

8. WDM 与 OCS 的关系：
   - OCS 端口是稀缺资源；
   - 如果一个 OCS 端口只承载一个 lane，效率有限；
   - WDM 可让一个光路承载多个波长通道；
   - 因此 WDM 提高 OCS 端口利用率；
   - 并减少光纤和布线成本。

9. 介质选择权衡：
   - copper：
       最便宜、最省电，但高速距离最短；
   - AOC：
       比铜更远、更轻，适合 row 内；
   - parallel fiber：
       适合约 100m 短距高带宽，但光纤数量多；
   - WDM：
       适合长距和少纤场景，但光器件更复杂、成本更高；
   - 选择依据是 reach、成本、功耗、光纤数量、
     安装维护、故障容忍和升级能力。

10. 总结：
   6.4.5 说明 WSC 网络性能不仅取决于交换机和路由协议，
   还取决于底层互连介质选择。
   数据中心网络设计必须按距离分层优化：
   机架内用铜，row 内用 AOC，短距用并行光纤，
   长距和 OCS 用 WDM。
   这样可以在高速率、大规模、低功耗、
   可维护性和 TCO 之间取得平衡。
```

---

### 16. 如果考试或讨论中要回答这一节，可以这样说

> 6.4.5 节讨论 warehouse-scale 数据中心中的光互连和铜互连选择。核心思想是：数据中心内部互连不是统一使用某一种介质，而是根据距离、速率、成本、功耗、体积和可维护性做分层优化。
>
> 首先，数据中心内尽可能使用铜链路，因为铜缆便宜、功耗低、延迟低、维护简单。但随着链路速率不断提高，铜缆的最大可用距离越来越短。今天高速铜链路通常只适合机架内使用，例如 NIC 到 ToR 的连接，以及密集交换架内部的 switch-to-switch 连接。
>
> 当铜缆距离不够时，可以使用 AOC，即 Active Optical Cable。AOC 两端是铜连接器，连接器内部有光电转换模块，中间使用光纤传输。由于 AOC 的光学接口是封闭的，它比传统可插拔光收发器更便宜，也更容易安装和维护。AOC 通常用于替代铜链路，以延长距离并减少铜缆体积，常见于 row 内连接。
>
> 在数据中心内部，光链路会根据距离使用不同类型的光模块，以优化成本。交换机端口通常使用可插拔光模块，例如 QSFP、QSFP-DD 或 OSFP。这些标准化形态支持不同速率和距离配置，并允许在故障时单独替换模块。
>
> 对于约 100m 级别的短距光链路，常使用并行光纤。并行光纤中，每个 lane 使用单独光纤或多个 lane 并行传输。它常用于 ToR 到 aggregation blocks 的连接，因为这些链路距离较短，同时需要 lane breakout 和 lane shuffling 来提高端口利用率和故障容忍度。breakout 可以把一个高速端口拆成多个低速端口，例如 400G 拆成 4 个 100G；shuffling 可以重新分配 lane，以避开故障 lane或使用备用光纤。
>
> 对于更长距离链路，以及涉及 OCS 的场景，通常使用 WDM，即波分复用。WDM 让一根光纤同时携带多个波长的光，从而减少光纤数量和线缆体积。由于 OCS 端口是稀缺资源，WDM 还可以让一个 OCS 光路承载多个波长通道，提高 OCS 端口利用率。
>
> 总体而言，这一节的核心结论是：WSC 网络设计必须在物理互连层做精细的 TCO 优化。机架内优先使用铜，row 内可用 AOC，短距高带宽使用并行光纤，长距和 OCS 场景使用 WDM。正确的互连介质选择可以在速率、距离、成本、功耗、可维护性和故障容忍度之间取得平衡。


**专栏导航**

- ← 上一篇：[6.4.4 Spine-less networking](/posts/6-4-4-spine-less-networking/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.4.6 Special-purpose networks 和 6.4.7 WANs →](/posts/6-4-6-special-purpose-networks-6-4-7-wans/)
