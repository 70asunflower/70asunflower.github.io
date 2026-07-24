---
title: "6.2.2 Hardware racks"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：6.2.2 Hardware racks。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.2.2 Hardware racks。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.2.2 Hardware racks

下面这一节 **6.2.2 Hardware racks** 看起来是在讲“机架”，但它真正强调的是：

> **在 WSC 中，rack 不只是一个放服务器的铁架子，而是服务器、网络、供电、电池备份、冷却、管理、故障域和部署运维的基本物理单元。**

如果说 6.2.1 讲的是“单台服务器如何设计”，那么 6.2.2 讲的是：

> **这些服务器如何被组织成一个可规模化部署、可供电、可冷却、可管理、可维修的物理系统。**

---

### 1. 这一节的核心观点

原文第一句：

> The rack is the physical structure that holds tens of servers together.

表面意思是：

> 机架是把几十台服务器固定在一起的物理结构。

但在 WSC 语境下，应该理解为：

> **rack 是 WSC 的物理部署单元。**

一个机架不仅承载服务器，还承载：

- 服务器 tray；
- 网络交换机；
- 电源转换设备；
- 电池备份；
- 电源分配总线；
- 管理控制器；
- 线缆管理；
- 冷却气流或液冷管路；
- 故障域边界；
- 运维操作单元。

所以 rack 是连接“单台服务器”和“整个数据中心 fabric”的中间层。

可以把它理解成：

```text
server tray
   ↓
rack
   ↓
pod / clique / row
   ↓
data center fabric
   ↓
WSC
```

---

### 2. 机架不只是机械结构，还承担共享电力基础设施

原文：

> Racks not only provide the physical support structures, but they also handle shared power infrastructure, including power delivery, battery backup, and power conversion such as AC to 48V DC.

这句话非常关键。

它说明机架至少有三重身份：

1. **机械承载结构**  
   放服务器、交换机、电源模块、线缆。
2. **电力分配系统**  
   把数据中心来的电力转换成服务器可用的电力。
3. **可靠性与备份单元**  
   通过电池备份和冗余设计提高可用性。

---

#### 2.1 power delivery：电力输送

数据中心从电网拿到的是高压交流电，但服务器内部需要的是低压直流电。

典型路径可以抽象为：

```text
电网 AC
  ↓
数据中心配电系统
  ↓
UPS / 发电机 / 高压配电
  ↓
机架电源模块 / power shelf
  ↓
48V DC busbar
  ↓
server tray
  ↓
DC-DC voltage regulators
  ↓
CPU / DRAM / SSD / NIC / accelerator
```

原文特别提到：

> AC to 48V DC

也就是交流转 48V 直流。

---

#### 2.2 为什么是 48V DC？

这是一个很值得展开的点。

传统服务器常见的是：

```text
AC 输入 → 服务器电源 PSU → 12V DC → 主板/设备
```

但在超大规模数据中心中，越来越多系统采用机架级 48V DC 分配。

原因主要有几个。

---

##### 1. 降低电流

功率公式：

```text
P = V × I
```

在同样功率下，电压越高，电流越小。

例如一个机架 IT 负载是 10 kW。

如果用 12V：

```text
I = 10000 / 12 ≈ 833 A
```

如果用 48V：

```text
I = 10000 / 48 ≈ 208 A
```

电流从 833A 降到 208A。

电流降低意味着：

- 铜损降低；
- 线缆可以更细；
- 连接器发热减少；
- 电源效率提高；
- 安全性更好；
- 机架内配电更容易。

损耗公式：

```text
P_loss = I² × R
```

电流降低 4 倍，电阻不变时损耗降低约 16 倍。

所以 48V DC 对高功率机架非常重要。

---

##### 2. 提高电源转换效率

如果每台服务器都自带 AC-DC 电源，那么：

- 每个 PSU 都要做交流转直流；
- 每个 PSU 都有转换损耗；
- 每个 PSU 都占用空间；
- 每个 PSU 都是潜在故障点。

机架级集中转换可以：

- 使用更大、更高效的电源模块；
- 做冗余配置；
- 统一监控；
- 减少服务器内部电源复杂度；
- 提高整体效率。

---

##### 3. 方便电池备份

48V DC 系统可以很方便地接入电池组。

很多数据中心使用 48V 电池系统作为短时备用电源。

它可以在电网波动或短时断电时提供：

- ride-through；
- 等待发电机启动；
- 避免瞬时掉电；
- 保护关键负载。

---

#### 2.3 battery backup：电池备份

原文提到：

> battery backup

机架级电池备份不一定是要支撑很长时间。

在 WSC 中，它常见目标是：

1. **应对瞬时断电**  
   电网闪断几秒，电池顶住。
2. **等待发电机启动**  
   发电机通常需要几秒到几十秒启动并稳定。
3. **减少服务中断**  
   避免服务器因短时掉电重启。
4. **提高可用性**  
   即使某一路电源故障，电池和冗余电源可以维持运行。

要注意：

> WSC 的电池备份设计通常不是为了“靠电池跑几小时”，而是为了跨越最危险的断电窗口。

真正长时间供电通常依赖：

- 柴油发电机；
- 天然气发电机；
- 多路市电；
- 冗余配电；
- 分布式系统容错。

---

#### 2.4 power conversion redundancy：电源转换冗余

原文 Figure 6.7 描述：

> It also provides configurable power conversion and battery backup support, with redundancy, to match the IT power load.

这里有两个关键词：

1. **configurable**  
   可根据 IT 负载配置电源模块数量、容量、冗余方式。
2. **redundancy**  
   电源路径不是单点，而是有备份。

常见冗余思想：

- N+1：需要 N 个模块即可满足负载，额外加 1 个备份；
- 2N：两套完整电源路径；
- 分布式冗余；
- 电池冗余；
- 电源总线冗余。

冗余的好处：

- 单个电源模块故障不会导致机架掉电；
- 可以在线更换；
- 提高可用性；
- 便于维护。

代价：

- 成本更高；
- 占用空间；
- 效率可能略降；
- 系统更复杂。

---

### 3. 机架尺寸：width 和 depth 不只是机械问题

原文：

> The width and depth of racks vary across WSCs: some are classic 19-in wide, 48-in deep racks, while others can be wider or shallower.

这里提到两类典型尺寸：

- 19 英寸宽；
- 48 英寸深。

这是传统数据中心常见标准。

但 WSC 不一定遵守传统尺寸，可能：

- 更宽；
- 更浅；
- 更高；
- 更开放；
- 更定制化。

---

#### 3.1 19 英寸机架

19 英寸是传统 IT 机架标准宽度。

优点：

- 生态成熟；
- 兼容大量设备；
- 适合企业数据中心；
- 适合 colo；
- 维护习惯成熟。

缺点：

- 对超大规模高密度计算可能空间不足；
- 布线、供电、冷却可能受限；
- 不适合某些大型加速器 tray。

---

#### 3.2 更宽的机架

更宽机架可以容纳：

- 更宽的 server tray；
- 更多并排节点；
- 更多 PCIe 卡；
- 更大散热器；
- 更粗电源线；
- 更多光纤；
- 更复杂的液冷管路。

优点：

- 提高单机架计算密度；
- 改善布线和气流；
- 适合加速器；
- 适合定制化 tray。

缺点：

- 不兼容传统 19 英寸设备；
- 机房布局要重新设计；
- 运输、安装、维护更复杂。

---

#### 3.3 更浅的机架

更浅机架可能有助于：

- 缩短气流路径；
- 改善冷却效率；
- 方便前后维护；
- 减少机房占地面积；
- 降低线缆长度；
- 降低重量。

但也可能限制：

- 服务器深度；
- 内存 DIMM 数量；
- PCIe 卡长度；
- 散热器尺寸；
- 电源模块空间。

---

### 4. 机架设计取决于用途：server、networking、accelerator

原文：

> Rack design can also vary depending on whether they are targeted at server trays, networking, or accelerators...

这说明机架不是“一种设计打天下”。

不同用途的机架差异很大。

---

#### 4.1 服务器机架

服务器机架主要放：

- compute tray；
- storage tray；
- ToR switch；
- 电源模块；
- 电池；
- 管理单元。

设计重点：

- 计算密度；
- 内存容量；
- 本地存储；
- 网络接入；
- 可维护性；
- 通用性；
- 功耗均衡。

---

#### 4.2 网络机架

网络机架主要放：

- ToR；
- aggregation switch；
- spine switch；
- optical patch panel；
- 光纤配线；
- 电源和备份。

设计重点：

- 端口密度；
- 光纤管理；
- 散热；
- 低延迟；
- 高可靠；
- 布线可维护性；
- 故障隔离。

---

#### 4.3 加速器机架

加速器机架放：

- GPU；
- TPU；
- 其他 AI 加速器；
- 高速互连；
- 高功率电源；
- 液冷系统；
- 高速网络。

设计重点：

- 极高功率密度；
- 极高带宽；
- 极低通信延迟；
- 液冷；
- 大电流配电；
- 高可靠互连；
- 机械承重；
- 故障域控制。

原文后面 Figure 6.8 就是这种：

> high-density racks containing TPU accelerators and their associated networking.

---

### 5. primary campus、edge、colo 的机架设计差异

原文：

> ...whether they are used in the primary campus or in edge or colo campuses.

这里提到三种部署环境。

---

#### 5.1 primary campus

primary campus 可以理解为超大规模数据中心园区。

特点：

- 规模巨大；
- 可高度定制；
- 电力基础设施强；
- 冷却系统可定制；
- 运维团队完善；
- 可以使用非标准机架；
- 可以部署高密度加速器。

在这里，机架设计可以非常激进，例如：

- 更宽机架；
- 液冷机架；
- 48V DC 配电；
- 自定义 tray；
- 自定义电源 shelf；
- 自定义管理模块。

---

#### 5.2 edge

edge 是边缘数据中心或边缘节点。

特点：

- 空间小；
- 电力有限；
- 冷却能力有限；
- 运维人员可能不在现场；
- 网络延迟要求低；
- 部署地点分散；
- 环境控制较弱。

edge 机架设计更重视：

- 小型化；
- 低功耗；
- 远程管理；
- 可靠性；
- 易部署；
- 少维护；
- 环境适应能力。

---

#### 5.3 colo

colo 是 colocation，托管数据中心。

企业租用机房空间、电力、冷却和网络接入。

特点：

- 机架尺寸通常标准化；
- 功率有合同限制；
- 冷却方式受限；
- 不能随意改造机房；
- 运维依赖远程或现场代维；
- 成本按空间、功率、带宽计费。

colo 中通常更偏好：

- 标准 19 英寸机架；
- 标准深度；
- 标准电源接口；
- 合规设备；
- 低功率密度或可预测功率密度。

---

### 6. pods 和 cliques：机架不是孤立的

原文：

> Rack design considerations can also change when used in “pods” or “cliques”.

这里出现两个重要概念：**pod** 和 **clique**。

---

#### 6.1 pod

pod 通常指一组机架组成的部署单元。

例如：

```text
pod
├── rack 1
├── rack 2
├── rack 3
├── ...
└── rack N
```

一个 pod 可能共享：

- 网络聚合层；
- 电力容量；
- 冷却区域；
- 故障域；
- 运维边界；
- 部署计划。

pod 的好处：

- 模块化部署；
- 容易扩容；
- 故障隔离；
- 网络规划清晰；
- 电力和冷却规划清晰。

---

#### 6.2 clique

clique 更常用于加速器或高性能计算网络中。

它通常表示：

> 一组高度互连的加速器或机架，彼此之间具有高带宽、低延迟连接。

在 AI 训练中，很多 collective communication 需要：

- all-reduce；
- all-gather；
- reduce-scatter；
- parameter synchronization；
- tensor parallelism；
- pipeline parallelism。

这些通信模式对网络要求极高。

因此 accelerator clique 可能强调：

- 高 bisection bandwidth；
- 低延迟；
- 非阻塞互连；
- 光互连；
- 机架间短距离；
- 共同电力和冷却域；
- 共同故障域管理。

原文说：

> We will discuss accelerator rack design in pods more in the next section.

说明后面会进一步讲加速器 pod 的机架设计。

---

### 7. 冷却方式改变机架设计：air vs liquid

原文：

> ...with different cooling considerations air vs liquid.

冷却方式会深刻影响机架设计。

---

#### 7.1 风冷机架

传统服务器机架多为风冷。

典型气流：

```text
冷通道 → 机架前部 → 服务器 → 机架后部 → 热通道
```

设计重点：

- 前后通风；
- 风扇墙；
- 冷热通道隔离；
- 风道密封；
- 温度监控；
- 风扇冗余；
- 防尘。

优点：

- 成熟；
- 成本低；
- 维护简单；
- 部署灵活。

缺点：

- 高功率密度下能力有限；
- 风扇功耗高；
- 噪声大；
- 对机房温度要求高。

---

#### 7.2 液冷机架

加速器和高 TDP CPU 越来越多使用液冷。

常见形式：

1. **direct-to-chip liquid cooling**  
   冷板直接贴在 CPU/GPU/TPU 上。
2. **rear-door heat exchanger**  
   机架后门换热器。
3. **immersion cooling**  
   设备浸入绝缘冷却液。

液冷机架设计要考虑：

- 冷却液分配单元 CDU；
- 供水/回水 manifold；
- 快接头；
- 漏液检测；
- 防腐蚀；
- 压力监控；
- 重量；
- 维护安全；
- 管路冗余。

优点：

- 散热能力强；
- 可支持高功率密度；
- 可降低风扇功耗；
- 有利于 AI 加速器。

缺点：

- 成本高；
- 运维复杂；
- 漏液风险；
- 机房基础设施要求高。

---

### 8. 机架约束 tray form factor

原文：

> The width and depth of a rack constrains tray form factors.

这句话把 6.2.1 和 6.2.2 连起来了。

服务器 tray 不是想设计多大就多大，它必须适配：

- 机架宽度；
- 机架深度；
- 机架高度；
- 电源接口；
- 网络接口；
- 气流方向；
- 液冷接口；
- 维护方式；
- 机械承重；
- 线缆管理。

也就是说：

> **server tray 是 rack 的子模块，rack 是 data center 的子模块。**

设计服务器时必须从机架角度反向约束。

例如：

- 如果机架宽度固定，tray 宽度不能超；
- 如果机架深度较浅，主板和 DIMM 布局要重新设计；
- 如果机架是液冷，tray 要预留冷板和快接头；
- 如果 ToR 在顶部，网线和光纤走线要向上汇聚；
- 如果电源在机架底部或顶部，tray 电源接口位置要匹配。

---

### 9. Top of Rack switch：机架顶部交换机

原文：

> It is often convenient to connect the network cables at the top of the rack; such a rack-level switch is appropriately called a Top of Rack ToR switch.

ToR 是数据中心网络中非常基础的概念。

---

#### 9.1 什么是 ToR？

ToR，Top of Rack switch，就是安装在机架顶部的接入交换机。

它连接：

- 本机架服务器；
- 本机架管理网络；
- 上联到 aggregation / spine / data center fabric。

抽象结构：

```text
        data center fabric
               ↑
          uplink links
               ↑
        +--------------+
        |  ToR switch  |
        +--------------+
          |  |  |  |
        server trays
```

---

#### 9.2 为什么 ToR 常放在机架顶部？

因为这样方便：

- 光纤和网线向上走线；
- 接入 overhead cable tray；
- 减少地面线缆；
- 统一布线；
- 方便维护；
- 减少气流阻挡；
- 连接同一机架内服务器。

---

#### 9.3 ToR 的作用

ToR 是机架接入数据中心网络的第一跳。

它负责：

- 服务器网络接入；
- VLAN / VxLAN；
- RDMA；
- 流量转发；
- 拥塞控制；
- QoS；
- 机架内东西向流量交换；
- 上联到 spine；
- 网络故障域边界。

---

#### 9.4 ToR 的设计权衡

优点：

- 每机架独立接入；
- 布线清晰；
- 扩展方便；
- 故障域较小；
- 服务器接入延迟低。

缺点：

- 每个机架都要部署交换机；
- 交换机数量多；
- 管理复杂；
- 占用机架空间；
- 消耗电力和冷却；
- 上联带宽需要规划，可能存在 oversubscription。

---

### 10. data center fabric：连接很多机架

原文：

> The ToR switch and rack management unit are located at the top of the rack and are further connected to a data center fabric to connect many racks.

这里出现 **data center fabric**。

fabric 可以理解为数据中心网络骨干结构。

常见架构是：

```text
server
  ↓
ToR
  ↓
spine / aggregation
  ↓
super spine
  ↓
many racks / pods
```

在 WSC 中，fabric 的目标是：

- 高带宽；
- 低延迟；
- 高可用；
- 可扩展；
- 非阻塞或可控 oversubscription；
- 支持 RDMA；
- 支持大规模东西向流量；
- 支持故障快速切换。

---

### 11. rack management unit：机架管理单元

原文提到：

> rack management unit

这是机架级管理设备。

如果说 6.2.1 中的 BMC 是单台服务器的管理控制器，那么 rack management unit 就是机架级管理控制器。

它可能负责：

- 机架电源监控；
- 电池状态监控；
- 温度传感器；
- 湿度传感器；
- 风扇控制；
- 功率封顶；
- 电源冗余状态；
- 机架级日志；
- 远程管理；
- 固件更新；
- 与数据中心管理系统通信。

可以理解为：

```text
BMC 管理单台服务器
rack management unit 管理整个机架
data center management system 管理整个数据中心
```

---

### 12. Figure 6.7：Google 数据中心机架示例

原文描述 Figure 6.7：

> It supports a configurable physical structure for server trays with different widths and heights; for example, it can host four narrow server trays per row. It also provides configurable power conversion and battery backup support, with redundancy, to match the IT power load. The ToR switch and rack management unit are located at the top of the rack and are further connected to a data center fabric to connect many racks.

这段信息量很大。

---

#### 12.1 可配置物理结构

> configurable physical structure for server trays with different widths and heights

说明这个机架不是只为一种服务器设计，而是可以适配：

- 不同宽度 tray；
- 不同高度 tray；
- 不同代际服务器；
- 不同 workload 节点；
- 不同计算/存储/加速配置。

这很重要，因为 WSC 需要：

- 长期演进；
- 多代硬件共存；
- 灵活部署；
- 减少机架闲置；
- 提高利用率。

---

#### 12.2 每行四个窄 tray

> host four narrow server trays per row

这说明机架宽度足够容纳多个窄 tray 并排。

这种设计可能带来：

- 更高节点密度；
- 更细粒度故障域；
- 更灵活 scale-out；
- 更适合云原生 workload；
- 更容易独立维护单个节点。

例如一个机架如果每行 4 个窄 tray，多行堆叠，就可以在一个机架中放很多独立计算节点。

---

#### 12.3 可配置电源转换和电池备份

> configurable power conversion and battery backup support, with redundancy, to match the IT power load

说明电源系统不是固定配置，而是根据实际 IT 负载选择：

- 电源模块数量；
- 电池容量；
- 冗余等级；
- 功率预算；
- 冷却匹配。

这体现 WSC 的精细化 TCO 管理。

如果电源配置过大：

- 成本高；
- 效率低；
- 空间浪费。

如果电源配置过小：

- 可靠性不足；
- 无法支持峰值；
- 无法冗余。

所以要 “match the IT power load”。

---

#### 12.4 ToR 和 rack management unit 在顶部

> The ToR switch and rack management unit are located at the top of the rack

这是典型设计：

- 网络向上汇聚；
- 管理接口集中；
- 布线整齐；
- 便于连接 overhead fiber tray；
- 便于维护。

---

### 13. Figure 6.8：高密度 TPU 加速器机架

原文：

> Figure 6.8 shows high-density racks containing TPU accelerators and their associated networking. Compared to regular racks, these racks have much higher bandwidth and power per rack.

这说明加速器机架和普通服务器机架有本质差异。

---

#### 13.1 更高功率密度

TPU/GPU 加速器机架通常功耗极高。

普通服务器机架可能是几 kW 到十几 kW。

加速器机架可能达到：

- 数十 kW；
- 甚至更高。

因此需要：

- 更强电源；
- 更粗 busbar；
- 更高电流能力；
- 更强冷却；
- 液冷；
- 更严格安全设计。

---

#### 13.2 更高网络带宽

AI 训练不是单卡训练，而是大规模并行。

加速器之间需要频繁通信。

因此加速器机架需要：

- 更多高速 NIC；
- 更高上联带宽；
- 更低延迟；
- 更高 bisection bandwidth；
- 可能使用光互连；
- 可能使用专用加速器互连；
- 更复杂网络拓扑。

原文说：

> associated networking

说明加速器机架不是只有加速器，还包括：

- 网络交换机；
- 光模块；
- 光纤；
- NIC；
- 可能 DPU/SmartNIC；
- 管理网络。

---

#### 13.3 加速器机架是“计算 + 网络 + 电力 + 冷却”的极端形态

普通服务器机架追求通用性和成本。

加速器机架追求：

- 极致计算密度；
- 极致互连带宽；
- 极致散热能力；
- 极致电力供给；
- 极致 collective communication 性能。

所以它往往是 WSC 设计中最复杂、最昂贵的部分。

---

### 14. Open Compute Project：开放硬件规范

原文最后：

> The Open Compute Project provides detailed specifications of many WSC hardware components.

OCP，Open Compute Project，是开放计算项目。

它提供很多数据中心硬件开放规范，例如：

- Open Rack；
- 电源 shelf；
- 电池备份；
- BMC；
- DC-SCM；
- 服务器主板；
- 网络设备；
- 存储；
- 加速器接口；
- 液冷相关规范。

---

#### 14.1 为什么 OCP 对 WSC 很重要？

因为超大规模数据中心需要：

1. **降低成本**  
   开放规范减少厂商锁定。
2. **提高可替换性**  
   多厂商可以供应兼容部件。
3. **加快创新**  
   行业共同演进标准。
4. **提高可维护性**  
   标准化模块更容易更换。
5. **支持规模化运维**  
   统一接口、统一固件、统一管理。
6. **提高能效**  
   例如 48V DC、高效电源、液冷规范。

---

### 15. 把 rack 看成 WSC 的“中间层抽象”

这一节最值得建立的思维是：

> **rack 是 WSC 中承上启下的关键抽象层。**

向下，它承载：

- server tray；
- NIC；
- SSD；
- accelerator；
- ToR；
- power shelf；
- battery；
- cooling。

向上，它连接：

- pod；
- row；
- data center fabric；
- power infrastructure；
- cooling infrastructure；
- management system；
- capacity planning。

所以 rack 同时是：

|视角|rack 是什么|
| ------------| --------------------------|
|机械视角|服务器支架|
|电力视角|配电和备份单元|
|网络视角|ToR 接入域|
|冷却视角|风道或液冷单元|
|运维视角|部署和维修单元|
|故障视角|故障域边界|
|成本视角|功率、空间、端口成本单元|
|加速器视角|高密度计算互连单元|

---

### 16. 机架设计中的关键权衡

可以把这一节背后的设计权衡总结成下面几组。

---

#### 16.1 密度 vs 可维护性

高密度意味着：

- 单机架更多计算；
- 更省空间；
- 更高功率利用率。

但可能带来：

- 更难维修；
- 更热；
- 更重；
- 更复杂布线；
- 更大故障影响。

---

#### 16.2 标准化 vs 定制化

标准化：

- 成本低；
- 兼容性好；
- 运维简单。

定制化：

- 更适合特定 workload；
- 更高性能密度；
- 更适合加速器。

WSC 常常在两者之间找平衡：

> 对外接口标准化，内部模块定制化。

---

#### 16.3 风冷 vs 液冷

风冷：

- 成熟；
- 便宜；
- 易维护。

液冷：

- 散热强；
- 支持高功率；
- 适合 AI。

但液冷会改变整个机房设计。

---

#### 16.4 大故障域 vs 小故障域

大机架/大节点：

- 资源集中；
- 通信快；
- 管理简单。

小节点/小故障域：

- 故障影响小；
- 更适合分布式系统；
- 更适合 scale-out。

---

#### 16.5 电源冗余 vs 成本效率

冗余电源提高可用性，但增加：

- 成本；
- 空间；
- 重量；
- 复杂度。

WSC 要在 SLA 和 TCO 之间平衡。

---

### 17. 与 6.2.1 的关系：从 server 到 rack

6.2.1 讲 server tray：

- CPU；
- DIMM；
- PCIe；
- NIC；
- accelerator；
- BMC；
- DC-SCM；
- power/cooling；
- mechanical design。

6.2.2 讲 rack：

- 机架尺寸；
- 电力分配；
- 电池备份；
- ToR；
- rack management unit；
- fabric；
- pod；
- accelerator rack；
- OCP。

二者关系可以这样理解：

```text
6.2.1：如何设计一个好用的计算节点？
6.2.2：如何把很多计算节点组织成可规模化运行的机架？
```

如果没有 rack 视角，服务器设计可能只追求单机性能。

有了 rack 视角，服务器设计必须考虑：

- 是否适合机架供电；
- 是否适合机架冷却；
- 是否方便布线；
- 是否方便维修；
- 是否支持远程管理；
- 是否匹配 ToR 带宽；
- 是否匹配机架功率密度；
- 是否支持开放标准。

---

### 18. 读 Figure 6.7 和 Figure 6.8 的建议

---

#### 18.1 读 Figure 6.7：通用服务器机架

看这张图时，可以关注：

1. **机架顶部**

   - ToR switch 在哪里？
   - rack management unit 在哪里？
   - 上联光纤如何走？
2. **服务器区域**

   - 每行有几个 tray？
   - tray 是窄是宽？
   - 是否模块化？
   - 是否支持热插拔？
3. **电源区域**

   - power shelf 在哪里？
   - 电池在哪里？
   - 是否冗余？
   - 是否可在线更换？
4. **布线和气流**

   - 网线/光纤如何管理？
   - 冷风从哪里进？
   - 热风从哪里出？
   - 是否避免线缆阻挡气流？

---

#### 18.2 读 Figure 6.8：TPU 高密度机架

看这张图时，可以关注：

1. **加速器布局**

   - TPU tray 如何排列？
   - 每个 tray 有多少加速器？
   - 是否高密度？
2. **网络布局**

   - associated networking 在哪里？
   - 是否有大量光纤？
   - 是否有高速交换机？
   - 是否有机架间互连？
3. **电力和冷却**

   - 是否液冷？
   - 是否有更粗电源线或 busbar？
   - 是否有更高功率模块？
   - 是否有漏液检测或液冷 manifold？
4. **与普通机架差异**

   - 功率密度是否更高？
   - 带宽是否更高？
   - 维护方式是否不同？
   - 故障域是否不同？

---

### 19. 关键术语表

|术语|含义|
| ----------------------| ------------------------------------|
|rack|机架，WSC 的基本物理部署单元|
|server tray|服务器托盘|
|power delivery|电力输送|
|power conversion|电源转换|
|AC|交流电|
|DC|直流电|
|48V DC|常见机架级低压直流配电|
|battery backup|电池备份|
|redundancy|冗余|
|ToR|Top of Rack switch，机架顶部交换机|
|data center fabric|数据中心网络骨干结构|
|rack management unit|机架管理单元|
|pod|一组机架构成的模块化部署单元|
|clique|高带宽互连的加速器/机架组|
|primary campus|主数据中心园区|
|edge|边缘数据中心|
|colo|colocation，托管数据中心|
|air cooling|风冷|
|liquid cooling|液冷|
|OCP|Open Compute Project，开放计算项目|
|power density|单机架功率密度|
|fault domain|故障域|
|TCO|总拥有成本|

---

### 20. 可以用来检验理解的问题

---

#### 问题 1：为什么 rack 不只是机械结构？

因为 rack 还承担：

- 电力分配；
- 电池备份；
- 电源转换；
- 网络接入；
- 冷却组织；
- 机架管理；
- 故障域划分；
- 运维部署。

---

#### 问题 2：为什么机架级 48V DC 很重要？

因为在高功率机架中，48V 相比 12V 可以显著降低电流，从而减少：

- 线缆损耗；
- 发热；
- 铜材成本；
- 连接器压力；
- 配电复杂度。

同时 48V 也方便电池备份和集中电源转换。

---

#### 问题 3：ToR switch 的作用是什么？

ToR 是机架的网络接入交换机。

它连接本机架服务器，并上联到 data center fabric。

它使机架成为网络接入和故障域的基本单元。

---

#### 问题 4：为什么加速器机架比普通机架更复杂？

因为加速器机架通常具有：

- 更高功率；
- 更高带宽；
- 更高散热需求；
- 更复杂互连；
- 更重；
- 更依赖液冷；
- 更依赖高速网络；
- 更高成本。

---

#### 问题 5：为什么机架尺寸会影响 server tray 设计？

因为 tray 的宽度、深度、高度、接口位置、散热方向、电源接口都必须适配机架。

服务器不能脱离机架独立设计。

---

#### 问题 6：primary campus、edge、colo 的机架设计有什么不同？

primary campus：

- 可定制；
- 可高密度；
- 可液冷；
- 可非标准尺寸。

edge：

- 小型化；
- 低功耗；
- 远程管理；
- 少维护。

colo：

- 标准化；
- 受功率和空间限制；
- 兼容性重要；
- 运维依赖托管方。

---

### 21. 用一句话总结这一节

这一节的核心可以概括为：

> **rack 是 WSC 中把服务器、网络、电力、电池、冷却和管理整合在一起的物理系统单元；它的设计直接决定了服务器如何部署、如何供电、如何散热、如何维修、如何扩展，以及最终的 TCO 和可靠性。**

---

### 22. 进一步延伸思考

如果你想更深入，可以继续思考下面几个问题：

1. **如果一个机架功率从 15 kW 提升到 100 kW，会对电力、冷却、网络、运维产生什么影响？**
2. **为什么 AI 训练集群越来越倾向于以 pod 或 clique 为单位设计，而不是单机架？**
3. **ToR 交换机故障会影响整个机架吗？如何通过冗余和 fabric 设计降低风险？**
4. **48V DC 相比传统 AC PSU 在超大规模数据中心中的优势是什么？**
5. **OCP 开放规范如何帮助降低 WSC 的 TCO？**

下面按你给的模板，把 **6.2.1 Server hardware** 和 **6.2.2 Hardware racks** 合并整理成两节，方便直接接在笔记后面。

---

### 这一节可以整理成的精简笔记

```text
6.2 Computing: servers and racks
6.2.1 Server hardware / 6.2.2 Hardware racks

1. 核心问题：
   WSC 中的服务器和机架不是单纯追求单机性能，
   而是要在 performance、TCO、power、cooling、security、
   serviceability 和 fleet-scale operation 之间做系统优化。

2. 服务器在 WSC 中的角色：
   - server tray 是 WSC 的基本计算单元；
   - 多个 tray 装入 rack；
   - rack 通过 ToR 和 data center fabric 连接成大规模系统；
   - 服务器必须适配机架的供电、冷却、网络、管理和机械约束。

3. 服务器硬件组成：
   - tray 通常包含 motherboard、CPU、DIMM、PCH、NIC、
     SSD/Flash/HDD、accelerator、BMC/DC-SCM、电源调节和冷却模块；
   - CPU 直接连接高速资源：DRAM、PCIe、accelerator、inter-socket link；
   - PCH 管理低速、非关键 I/O，如 USB、SATA、部分 Ethernet 和平台管理接口。

4. CPU 设计考虑：
   - TDP：热设计功耗，影响散热、电源和机架功率密度；
   - socket 数量：1S、2S 影响容量、NUMA、故障域和成本；
   - NUMA：多 socket 下本地内存快、远端内存慢；
   - core count、frequency、cache size、inter-socket coherency links
     共同决定单机计算能力和扩展性。

5. 内存设计考虑：
   - 关键不是只有容量，而是 memory channels、DIMMs per channel、
     DIMM type 和 DDR standard；
   - 1DPC 通常更利于高频和带宽效率；
   - 2DPC 更利于容量，但可能降低频率和信号裕度；
   - RDIMM、LRDIMM 等用于提高容量和信号完整性；
   - DDR5 提供更高带宽，但内存带宽扩展仍受物理限制。

6. I/O 设计考虑：
   - PCIe 连接 NIC、SSD、GPU、TPU、VCU、CXL 设备等；
   - PCIe Gen5 提供高带宽，但 lanes、功耗和 form factor 都受限；
   - CXL 可用于内存扩展、内存池化和加速器一致性访问；
   - NIC quad-furcation 可让多个节点共享一个高速 NIC，
     提高 Perf/TCO，但增加隔离、QoS 和故障域复杂度。

7. 电源、冷却和管理：
   - voltage regulators 和 per-core DVFS 提高能效；
   - air cooling 成熟便宜，但高功率密度下受限；
   - liquid cooling 更适合高 TDP CPU/GPU/TPU；
   - BMC 提供单节点远程管理；
   - Root-of-Trust 和 secure boot 提供安全基础；
   - DC-SCM 将 BMC、RoT、固件存储等从主板分离，
     提高标准化、安全性、可恢复性和可维护性。

8. 机械设计：
   - server tray 的 width、height、depth 必须适配 rack；
   - form factor 影响 power density、cooling、serviceability；
   - 前后维护方式影响运维效率；
   - WSC 中服务器设计必须考虑部署、维修、替换和自动化管理。

9. 三个服务器示例：
   - Intel Sapphire Rapids：
       2 socket，350W TDP，8 DDR5 channels/CPU，2DPC，
       32 DIMMs/tray，强调大容量内存、PCIe Gen5 和 DC-SCM；
   - AMD Genoa：
       高核心数、高 TDP，12 DDR5 channels/CPU，1DPC，
       支持 CXL，强调更高内存带宽和吞吐；
   - Google Axion：
       ARM Neoverse V2，10 DDR5 controllers/CPU，
       tray 内两个独立 compute node，支持 NIC quad-furcation，
       强调 scale-out、Perf/TCO 和高密度部署。

10. 关键矛盾：memory bandwidth wall：
   - 制程进步让增加 core 数相对容易；
   - 但内存带宽受 memory PHY、package pins、die shoreline、
     board routing、DIMM 信号和功耗限制；
   - core count 增长快于 memory bandwidth 增长时，
     每核可用带宽下降；
   - 解决方向包括更多 memory channels、1DPC、高频 DDR、
     CXL memory、cache 优化、数据局部性和软件调度。

11. 2-socket vs bifurcated 2x1-socket：
   - two-socket server：
       一个系统、两个 CPU、更大内存容量、NUMA 域更大，
       适合大内存、数据库、虚拟化等负载；
   - bifurcated 2x1-socket：
       一个 tray 中两个独立单路节点，
       故障域更小，更适合 scale-out、云原生和高密度部署；
   - WSC 常常偏好小故障域、标准化节点和软件层容错。

12. Hardware racks 的核心观点：
   - rack 不只是机械结构；
   - rack 是 WSC 的物理部署、供电、冷却、网络接入和管理单元；
   - rack 把 server tray、ToR switch、power shelf、battery backup、
     rack management unit 和 data center fabric 连接起来。

13. 机架机械尺寸：
   - 常见传统机架：19-in wide、48-in deep；
   - WSC 也可能使用更宽或更浅机架；
   - rack width/depth 直接约束 tray form factor；
   - 更宽机架可提高密度和布线空间；
   - 更浅机架可改善维护、气流和机房空间利用。

14. 机架电力基础设施：
   - rack 处理 shared power infrastructure；
   - 包括 power delivery、power conversion、battery backup；
   - 常见趋势是 AC to 48V DC；
   - 48V DC 在高功率机架中可降低电流和 I²R 损耗；
   - 机架级电源转换可提高效率、冗余和可管理性。

15. 电池备份和冗余：
   - battery backup 主要用于 ride-through；
   - 应对电网闪断、等待发电机启动、避免瞬时掉电；
   - redundancy 可避免单点故障；
   - 电源配置需要 match IT power load，避免过度配置或不足配置。

16. ToR switch 和 data center fabric：
   - ToR 通常位于机架顶部；
   - 连接本机架服务器，并上联到 data center fabric；
   - 使 rack 成为网络接入和故障域的基本单元；
   - 顶部布线便于光纤和网线管理，也利于连接 overhead cable tray。

17. rack management unit：
   - 机架级管理控制器；
   - 可监控电源、电池、温度、功耗、风扇和机架事件；
   - 与 BMC 形成层级关系：
       BMC 管单节点，rack management unit 管整机架；
   - 支持远程管理、功率封顶、故障诊断和自动化运维。

18. 不同机架类型：
   - server rack：通用计算、存储、虚拟化；
   - networking rack：交换机、光纤配线、网络 fabric；
   - accelerator rack：GPU/TPU/其他 AI 加速器；
   - accelerator rack 通常具有更高功率、更高带宽和更强冷却需求。

19. 不同部署场景：
   - primary campus：
       超大规模自有数据中心，可定制机架、电力和液冷；
   - edge：
       空间、电力、冷却和运维受限，强调小型化和远程管理；
   - colo：
       托管机房，强调标准机架、功率限制和兼容性。

20. pods 和 cliques：
   - pod 是一组机架构成的模块化部署单元；
   - clique 常用于描述高带宽、低延迟互连的加速器组；
   - AI 训练集群常需要 pod/clique 级高 bisection bandwidth；
   - 机架设计必须和网络拓扑、 collective communication 共同优化。

21. 冷却方式：
   - air cooling：成熟、便宜、易维护，但功率密度受限；
   - liquid cooling：适合高 TDP CPU/GPU/TPU；
   - 液冷改变机架设计，需要 manifold、CDU、漏液检测、快接头等；
   - 冷却方式会反向约束服务器 tray 和 rack 形态。

22. Open Compute Project：
   - OCP 提供开放硬件规范；
   - 覆盖 rack、power、BMC、DC-SCM、server、networking 等；
   - 目标是降低成本、减少厂商锁定、提高兼容性和可运维性；
   - 对超大规模 WSC 非常重要。

23. 总结：
   - 6.2.1 说明 server tray 是计算、内存、I/O、管理和安全的集成单元；
   - 6.2.2 说明 rack 是服务器进入 WSC 的物理、电力、冷却和网络载体；
   - WSC 设计的关键不是单机最强，而是：
       high Perf/TCO、可运维、可扩展、可冷却、可供电、
       可远程管理、可容错、可规模化部署。
```

---

### 如果考试或讨论中要回答这一节，可以这样说

> 6.2.1 和 6.2.2 讨论的是 WSC 中计算硬件的两个关键层次：**server tray** 和 **hardware rack**。
>
> 首先，6.2.1 强调，WSC 中的服务器不是简单追求单机性能，而是要在性能、TCO、功耗、冷却、安全、可维护性和规模化运维之间做综合优化。服务器通常以 tray 的形式存在，内部包含 CPU、DIMM、PCH、NIC、SSD、加速器、BMC 或 DC-SCM 等组件。CPU 直接连接 DRAM、PCIe 和高速互连，而 PCH 负责 USB、SATA 等低速 I/O。服务器设计需要同时考虑 CPU 的 TDP、socket 数量、NUMA 拓扑、核心数、频率和 cache；也需要考虑内存通道数、DIMM 类型、DDR 速率和 1DPC/2DPC 的权衡。因为很多 workload 的瓶颈不是 CPU 计算，而是内存带宽和 I/O 带宽，所以 memory channels、PCIe lanes、CXL、NIC 和加速器接口都非常关键。
>
> 原文通过三个例子说明不同设计取向：Intel Sapphire Rapids 平台强调双路、大容量内存、PCIe Gen5 和 DC-SCM；AMD Genoa 平台强调更高核心数、12 个 DDR5 通道和 CXL 支持；Google Axion 平台则使用 ARM Neoverse V2 核心，每个 tray 包含两个独立计算节点，并通过 NIC quad-furcation 共享网卡以提升 Perf/TCO。这些例子共同说明一个关键问题：随着工艺进步，增加核心数相对容易，但内存带宽受到 PHY、封装引脚、die shoreline、主板走线和功耗限制，因此会出现“内存带宽墙”。
>
> 6.2.2 进一步说明，rack 不只是放服务器的机械架子，而是 WSC 的基本物理部署单元。机架承载服务器 tray、ToR switch、rack management unit、电源模块、电池备份和配电总线，同时约束 tray 的宽度、深度和高度。机架还负责共享电力基础设施，包括 power delivery、power conversion 和 battery backup。现代高密度机架常采用 48V DC 配电，因为高功率下 48V 可以降低电流和线路损耗。ToR switch 通常位于机架顶部，用于连接本机架服务器并上联到 data center fabric；rack management unit 则负责机架级电源、温度、电池和功耗监控。
>
> 此外，机架设计还会因用途和部署环境不同而变化。服务器机架、网络机架和加速器机架的设计重点不同；primary campus、edge 和 colo 的约束也不同。加速器机架尤其重要，因为 GPU/TPU 机架通常具有更高功率密度、更高网络带宽和更强冷却需求，常常需要液冷，并以 pod 或 clique 的形式组织，以支持 AI 训练中的高带宽 collective communication。OCP 等开放规范则帮助降低硬件成本、提高兼容性和可运维性。
>
> 总体而言，这一部分的核心结论是：WSC 的服务器和机架设计不能只看单点性能，而要从系统角度理解。server tray 是计算单元，rack 是部署、供电、冷却、网络和管理单元，二者必须协同设计，最终目标是在超大规模环境中实现高 Perf/TCO、高可靠性、高利用率和可自动化运维。


**专栏导航**

- ← 上一篇：[6.2.1 Server hardware](/posts/6-2-1-server-hardware/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.2.3 Individual servers as distributed systems →](/posts/6-2-3-individual-servers-as-distributed-systems/)
