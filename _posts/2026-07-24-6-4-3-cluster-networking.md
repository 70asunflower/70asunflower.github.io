---
title: "6.4.3 Cluster networking"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：6.4.3 Cluster networking。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.4.3 Cluster networking。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.4.3 Cluster networking

下面这一节 **6.4.3 Cluster networking** 是 6.4 Networking 中非常核心的一部分。

前面 6.4.1 讲的是：

> 数据包如何从 tray 走到 planet。

6.4.2 讲的是：

> 主机侧网络如何通过 SmartNIC/IPU 做卸载、虚拟化和安全隔离。

而 6.4.3 讲的是：

> **如何把成千上万台服务器高速连接成一个集群网络。**

这一节的核心可以概括为：

> **WSC 集群网络不能依赖一个“无限大的交换机”，而必须用 Clos/fat-tree 等多级交换结构，把大量小型交换芯片组合成大型 fabric；同时在带宽、成本、光模块、oversubscription、局部性和调度之间做系统级权衡。**

---

### 1. 为什么集群网络是 WSC 的关键？

原文开头说：

> WSC clusters must interconnect thousands of servers at high speed.

WSC cluster 要连接：

- 数千台服务器；
- 数万端口；
- 高带宽 NIC；
- 存储流量；
- RPC 流量；
- shuffle 流量；
- 训练流量；
- 复制流量；
- 控制平面流量；
- 监控 telemetry 流量。

所以集群网络必须同时满足：

- 高吞吐；
- 低延迟；
- 低尾延迟；
- 高可用；
- 可扩展；
- 可运维；
- 可调试；
- 成本可控；
- 功耗可控。

---

### 2. 为什么不能直接造一个超大交换机？

原文说：

> Unfortunately, we can’t just buy or make an arbitrarily large switch. At any given time, the available technology limits total per-chip capacity because all chips are power- and pin-limited.

这是集群网络设计的出发点。

直觉上，如果有一个超大交换机：

```text
所有服务器都接到这一个交换机
```

那网络会很简单。

但现实中做不到，因为交换芯片受限于：

1. **功耗**

   - 高速 SerDes 很耗电；
   - 包处理很耗电；
   - 转发查找很耗电；
   - 散热能力有限。
2. **引脚和封装**

   - 每个高速端口需要 SerDes lanes；
   - 每个 lane 需要封装引脚；
   - 封装面积和 pin 数有限；
   - 信号完整性要求高。
3. **工艺和良率**

   - 超大 die 良率低；
   - 成本高；
   - 制造困难。
4. **端口密度和物理尺寸**

   - 光模块/线缆空间有限；
   - 面板密度有限；
   - 散热风道有限。

所以单颗交换芯片容量有上限。

原文举例：

> as of 2024, a typical merchant silicon switch chip supports a bisection bandwidth of up to 51.2 Tbps, 128x 400 GbE ports, and no chips are available that can deliver more than 200 Tbps.

也就是说，2024 年左右典型商用交换芯片大约是：

```text
51.2 Tbps
= 128 × 400 GbE
```

但没有单芯片能提供 200 Tbps 以上容量。

因此必须：

> 用多颗交换芯片组成更大的网络 fabric。

---

### 3. Clos / fat-tree：用多级小交换机组成大网络

原文说：

> We can build larger switches by cascading individual switch chips, typically in the form of a fat tree or Clos network.

这就是现代数据中心网络的核心结构：

```text
Clos network
```

也常叫：

```text
fat-tree
leaf-spine
```

---

#### 3.1 Clos 网络的来源

原文说：

> Clos networks are named after Charles Clos, who first formalized their properties in 1952.

Clos 网络最早由 Charles Clos 在 1952 年形式化。

它最初用于电话交换系统，后来被数据中心网络广泛采用。

---

#### 3.2 基本思想：leaf 和 spine

原文：

> The basic idea is that each leaf switch divides its ports into downward server-facing ports and upwards spine-facing ports.

Clos 网络中的 leaf switch，也就是接入交换机，会把端口分成两类：

```text
向下：连接服务器
向上：连接 spine 交换机
```

在 rack 网络中，leaf 通常就是：

```text
ToR switch
```

---

#### 3.3 k-port switch 的简单例子

原文：

> In a fully connected tree, half of the ports go each way, so if we have k-port switches, k/2 ports connect to the servers and the others connect to one of k/2 spine switches.

假设交换机有 k 个端口。

在理想 full-throughput 设计中：

```text
k/2 端口向下连服务器
k/2 端口向上连 spine
```

例如 k = 64：

```text
32 端口连服务器
32 端口连 spine
```

每个 leaf 到 spine 都有链路。

---

#### 3.4 多路径和冗余

原文：

> With this topology, every leaf switch has k/2 paths to every other leaf switch, each path going through a different spine switch.

如果 leaf A 要和 leaf B 通信，它可以走多个 spine。

例如：

```text
leaf A → spine 1 → leaf B
leaf A → spine 2 → leaf B
leaf A → spine 3 → leaf B
...
```

这带来几个好处：

1. **带宽聚合**

   - 多条路径可以同时使用；
   - 提高总带宽。
2. **冗余**

   - 某个 spine 故障，其他 spine 仍可转发。
3. **负载均衡**

   - 流量可以分散到多条路径。
4. **可扩展**

   - 增加 spine 可以增加带宽。

---

### 4. 递归构建：从芯片到数据中心 fabric

原文说：

> In real networks, this concept is applied recursively: a switch may be combined inside a chassis to form a larger switch, and multiple switch chassis may be combined to form a “block” that looks like an even larger virtual switch.

Clos 思想可以递归使用。

层级可以抽象为：

```text
switch chip
  ↓
line card
  ↓
chassis
  ↓
block
  ↓
fabric
  ↓
data center network
```

例如：

- 多颗交换芯片组成一个 chassis；
- 多个 chassis 组成一个 block；
- 多个 block 组成整个 cluster fabric；
- 对外看起来像一个很大的虚拟交换机。

这就是 Figure 6.24 展示的 three-stage Clos topology。

---

### 5. Clos 的规模与成本

原文说：

> A tree using k-port switches can support full throughput among k<sup>3/4 servers using 5k</sup>2/4 switches...

这里原文公式可能因排版显示不完整，但核心意思是：

> 多级 Clos 可以支持数量随 k 的高次方增长的服务器规模，但交换机数量也会随 k^2 量级增长。

也就是说：

```text
网络规模可以很大
但成本也会显著增长
```

---

#### 5.1 单级交换：路径端口少，成本低，但规模小

最简单的网络是：

```text
所有服务器接一个中央交换机
```

一条路径只需要：

```text
switch in
switch out
```

也就是两个交换机端口。

优点是：

- 简单；
- 延迟低；
- 成本相对低；
- 路径短。

缺点是：

- 交换机端口数有限；
- 无法扩展到数万端口；
- 单点故障；
- 单芯片容量受限。

---

#### 5.2 多级 Clos：规模大，但路径端口多

原文说：

> The above three-stage network quintuples that to 10 ports, significantly increasing cost per server since every server port needs to be matched with 8 additional switch ports in the tree.

多级 Clos 中，一个服务器端口要穿过多个交换层级。

这意味着：

```text
每个服务器端口
不仅需要 ToR 端口
还需要 uplink 端口
spine 端口
aggregation 端口
...
```

所以每个服务器端口对应的网络端口数增加。

端口数增加意味着：

- 更多交换芯片；
- 更多光模块；
- 更多线缆；
- 更多功耗；
- 更多故障点；
- 更高成本。

因此原文强调：

> as the size of the cluster and thus the bisection bandwidth grows, the cost per connected server grows as well.

集群越大，full-throughput 成本越高。

---

### 6. bisection bandwidth：集群网络的关键指标

这一节多次隐含一个概念：

> bisection bandwidth

---

#### 6.1 什么是 bisection bandwidth？

bisection bandwidth 指：

> 把网络切成两半后，两半之间可用的最小总带宽。

可以理解为：

```text
网络最窄处的带宽
```

如果一个网络有 full bisection bandwidth，那么：

```text
任意一半服务器和另一半服务器之间
可以同时达到线速通信
```

这就是 nonblocking network。

---

#### 6.2 为什么 bisection bandwidth 重要？

WSC 中很多流量是东西向流量：

- 服务器到服务器；
- 存储到计算；
- GPU 到 GPU；
- shard 到 shard；
- worker 到 parameter server；
- 分布式训练 all-reduce；
- 数据库复制；
- shuffle。

如果 bisection bandwidth 不足，就会出现：

```text
局部通信很快
跨集群通信拥塞
整体吞吐下降
尾延迟上升
训练 goodput 下降
```

---

### 7. 光模块成本：数据中心网络最大的单项成本之一

原文说：

> Port costs are substantial, especially if a link spans more than a few meters, thus requiring an optical interface.

网络成本不只是交换机芯片。

真正非常贵的是：

```text
optics
```

也就是光模块和光纤连接。

---

#### 7.1 光链路成本构成

原文举例：

> Today the optical components of a 100 m 100 Gbps link can cost several hundred dollars, including the cost of the two optical ports, fiber cable, fiber termination and installation, not including the networking components themselves.

一个 100m 100Gbps 光链路可能包括：

- 两个光模块；
- 光纤；
- 光纤端接；
- 安装；
- 测试；
- 维护；
- 配线架；
- 连接器。

这些成本加起来可能数百美元。

而这还不包括：

- 交换机；
- NIC；
- 芯片；
- 电源；
- 冷却；
- 运维。

所以原文说：

> optics represent the largest single cost item.

光模块是数据中心网络中最大的单项成本之一。

---

#### 7.2 不同距离使用不同光模块

原文：

> Since the optical links inside the data center have different reach, different types of optics optimize cost and power based on reach, link budget and signal-noise-ratio requirements.

数据中心内部链路距离不同：

- 机架内几米；
- 机架间十几米；
- 机房内几十米；
- 楼内上百米；
- 园区几公里；
- WAN 更远。

距离越远，对光模块要求越高：

- 更高 link budget；
- 更好 SNR；
- 更复杂激光器件；
- 更高功耗；
- 更高成本。

因此需要按距离优化。

例如粗略分层：

|距离|常见介质/光模块|
| ------------| -----------------|
|机架内短距|DAC/AOC|
|几十米|SR 类短距光模块|
|几百米|DR/FR 类|
|几公里|LR 类|
|更远|园区/WAN 光传输|

---

#### 7.3 短距优化可以显著降低成本

原文：

> Since most links inside the data center are short, optimized versions can reduce costs substantially.

数据中心内大多数链路其实很短。

如果所有链路都按长距标准设计，会浪费成本。

所以可以：

- 使用短距光模块；
- 使用低功耗光器件；
- 使用定制光模块；
- 使用 parallel optics；
- 优化光纤类型；
- 减少不必要的长距能力。

原文还提到：

> Even the very first iteration of Google’s interconnect Saturn used nonstandard optics to reduce costs.

Google 早期 Saturn 网络就使用非标准光模块来降低成本。

这说明：

> WSC 网络设计常常需要定制光互连，而不是完全依赖通用长距光模块。

---

### 8. Oversubscription：为什么网络不必 1:1 full bandwidth？

原文说：

> To further reduce networking costs per machine, WSC designers often oversubscribe the network upwards north of the top-of-rack switch.

这是数据中心网络设计的核心权衡。

---

#### 8.1 机架内 full bandwidth 比较便宜

原文：

> Providing full bandwidth inside the rack is fairly inexpensive since the rack contains a small enough number of servers to be connected with a single switch.

一个机架内服务器数量有限。

例如一个 ToR 有 64 个端口，可以：

```text
64 servers × 200 Gbps
```

用单台交换机就能提供机架内 full bandwidth。

机架内 full bandwidth 相对便宜，因为：

- 只需一台 ToR；
- 距离短；
- 可用 DAC/AOC；
- 光模块少；
- 不需要复杂多级 fabric。

---

#### 8.2 如果整个集群都 full bandwidth，会非常贵

原文：

> In a full fat tree, each such switch would need the same number of ports facing the cluster fabric.

如果 ToR 有 64 个 200G 服务器端口，那么 full fat-tree 设计需要同样多的上行端口：

```text
64 × 200G 下行
64 × 200G 上行
```

然后上行还需要 aggregation/core 层更多链路。

这会导致：

- 交换机数量暴增；
- 光模块数量暴增；
- 功耗暴增；
- 成本暴增；
- 布线复杂；
- 机房空间浪费。

所以 full nonblocking 网络非常昂贵。

---

#### 8.3 什么是 oversubscription？

oversubscription 指：

> 服务器总带宽大于上行到 fabric 的总带宽。

也就是：

```text
server-side bandwidth : fabric-side bandwidth > 1:1
```

例如：

```text
2:1 oversubscription
3:1 oversubscription
4:1 oversubscription
```

---

#### 8.4 2:1 oversubscription 示例

原文：

> with 2:1 oversubscription, we build a fat tree for only half the aggregate bandwidth of the servers connected to the rack switches.

如果每个服务器 NIC 是 200Gbps。

2:1 oversubscription 意味着：

```text
每台服务器平均可用 fabric 带宽 = 100Gbps
```

原文说：

> Each server can still peak at 200 Gbps of traffic, but if all servers are simultaneously sending traffic, they’ll only be able to average 100 Gbps.

也就是说：

- 单台服务器短时间可以跑到 200Gbps；
- 但如果所有服务器同时满负载发送；
- 平均只能达到 100Gbps。

---

#### 8.5 3:1 oversubscription 示例

原文：

> a 64-port rack switch with 200 Gbps ports could connect 48 servers to 16 uplinks, for a 3:1 oversubscription, 66.7 Gbps per server.

例子：

```text
48 servers × 200G = 9.6Tbps server-side bandwidth
16 uplinks × 200G = 3.2Tbps fabric-side bandwidth
```

比例：

```text
9.6 / 3.2 = 3
```

所以是 3:1 oversubscription。

每台服务器平均 fabric 带宽：

```text
3.2Tbps / 48 = 66.7Gbps
```

虽然每台服务器 NIC 是 200Gbps，但跨机架平均可用带宽只有约 66.7Gbps。

---

#### 8.6 为什么 oversubscription 可行？

因为现实中并不是所有服务器同时以线速向所有其他服务器发送数据。

很多 workload 有：

- 局部性；
- 周期性通信；
- 突发但非持续满负载；
- 读写不对称；
- 调度控制；
- 流量工程；
- 拥塞控制。

所以可以通过 oversubscription 降低成本。

但 oversubscription 也有代价：

- worst-case bandwidth 降低；
- incast 更容易拥塞；
- all-to-all 性能下降；
- 尾延迟可能上升；
- 需要更好的调度和拥塞控制。

---

### 9. Google Jupiter 网络

原文：

> Figure 6.25 shows the structure of Google’s Jupiter Clos network first deployed more than a decade ago with a bisection bandwidth of 1.3 petabits per second.

Jupiter 是 Google 著名的数据中心 Clos 网络。

第一代 Jupiter 的 bisection bandwidth 达到：

```text
1.3 petabits per second
```

这在当时非常巨大。

---

#### 9.1 Jupiter 使用 low-radix merchant silicon

原文：

> This multistage network fabric used low-radix switches built from merchant silicon, each supporting 16x40 Gbps ports.

Jupiter 的关键设计哲学是：

> 不依赖超大、昂贵、专有的高基数交换机，而是用大量小型商用交换芯片构建大 fabric。

每个交换芯片支持：

```text
16 × 40 Gbps ports
```

这是 low-radix switch。

radix 指交换机端口数。

low-radix 意味着：

```text
单芯片端口数不大
```

但通过 Clos 多级组合，可以构建非常大的网络。

---

#### 9.2 40G 端口可拆成 4x10G

原文：

> Each 40G port could be configured in 4x10G or 40G mode.

这体现了端口 breakout。

一个 40G 物理端口可以拆成：

```text
4 × 10G
```

或者作为：

```text
1 × 40G
```

这提高了灵活性。

例如：

- 服务器用 10G NIC；
- fabric 上行用 40G；
- 或者某些链路用 40G burst。

---

#### 9.3 Centauri switch

原文：

> Jupiter’s primary building block was the Centauri switch, a 4RU chassis housing two line cards, each with two switch chips.

Centauri 是 Jupiter 的主要构建块。

结构：

```text
4RU chassis
├── line card 1
│   ├── switch chip 1
│   └── switch chip 2
└── line card 2
    ├── switch chip 3
    └── switch chip 4
```

也就是说，一个 chassis 里有多颗交换芯片。

---

#### 9.4 ToR 配置和 3:1 oversubscription

原文：

> In an example ToR configuration, each switch chip is configured with 48x10G to servers and 16x10G to the fabric, yielding an oversubscription ratio of 3:1.

每个交换芯片：

```text
48 × 10G 向下连服务器
16 × 10G 向上连 fabric
```

比例：

```text
48 / 16 = 3
```

所以是：

```text
3:1 oversubscription
```

服务器也可以配置成 40G mode：

> Servers could also be configured with 40G mode to have 40G burst bandwidth.

也就是说，服务器可以短时间 burst 到 40G，但 fabric 上行仍然是 oversubscribed。

---

### 10. Middle Block 和 aggregation blocks

原文：

> The ToR switches connect to layers of aggregation blocks to increase the scale of the network fabric.

ToR 不是孤立的，它们连接到 aggregation blocks。

---

#### 10.1 Middle Block

原文：

> Each Middle Block MB had four Centauri chassis. The logical topology of an MB was a two-stage non-blocking network, with 256x10G links available for ToR connectivity and 64x40G available for connectivity to the rest of the fabric through the spine blocks.

每个 Middle Block：

```text
4 × Centauri chassis
```

逻辑上是一个 two-stage non-blocking network。

它提供：

```text
256 × 10G 链路连接 ToR
64 × 40G 链路连接 spine blocks
```

可以理解为：

```text
ToR
 ↓ 10G
Middle Block
 ↓ 40G
Spine Block
```

---

#### 10.2 为什么需要 aggregation？

因为 ToR 数量很多。

如果每个 ToR 都直接连到核心，会出现：

- 核心端口不足；
- 布线爆炸；
- 光模块爆炸；
- 管理复杂；
- 故障域复杂。

aggregation block 的作用：

- 聚合 ToR 上行；
- 减少核心链路数量；
- 提供局部 nonblocking；
- 模块化扩展；
- 简化布线；
- 提高可维护性。

---

### 11. external connectivity 和 FBR

原文：

> Jupiter employs a separate aggregation block for external connectivity, which provides the entire pool of external bandwidth to each aggregation block.

Jupiter 有专门的 aggregation block 用于外部连接。

---

#### 11.1 外部带宽比例

原文：

> As a rule of thumb, 10% of aggregate intra-cluster bandwidth is allocated for external connectivity using one to three aggregation blocks.

经验法则：

```text
外部带宽 ≈ 集群内部总带宽的 10%
```

这说明大多数流量是集群内部流量，而不是离开集群的流量。

例如：

- 内部 RPC；
- 存储访问；
- shuffle；
- 复制；
- 训练通信；
- 日志；
- 监控。

只有部分流量需要：

- 跨集群；
- 跨数据中心；
- 到用户；
- 到 CDN；
- 到 WAN。

---

#### 11.2 Fabric Border Routers

原文：

> With Jupiter, the intra-cluster fabric connects to the inter-cluster networking layer with Fabric Border Routers, FBRs.

FBR 是集群边界路由器。

它连接：

```text
cluster fabric
   ↓
inter-cluster network
   ↓
campus / WAN / other clusters
```

---

#### 11.3 调度利用 building/campus locality

原文：

> Multiple cluster fabrics may be deployed within the same building and multiple buildings on the same campus. The job scheduling and resource allocation infrastructure leverages campus-level and building-level locality.

这很重要。

网络不是孤立设计，而是和调度系统协同。

如果任务可以放在同一 building 或 campus：

- 延迟更低；
- 带宽更高；
- WAN 成本更低；
- 外部拥塞更少；
- 可靠性更高。

所以 job scheduler 会考虑：

```text
machine locality
rack locality
cluster locality
building locality
campus locality
region locality
```

这体现了 WSC 的软硬件协同设计。

---

### 12. WSC 网络 vs HPC 网络

原文最后比较了 HPC。

---

#### 12.1 HPC 的计算/网络带宽比更低

原文：

> Compared with WSCs, High-Performance Computing supercomputer clusters often have a much lower ratio of computation to network bandwidth.

也就是说，HPC 应用相对于计算量，需要更多网络带宽。

例如天气模拟：

```text
数据分布在所有节点 RAM 中
每次计算少量浮点
然后需要和邻居节点交换数据
```

这类应用通信频繁。

---

#### 12.2 HPC 传统上使用专有互连

原文：

> traditional HPC systems have used proprietary interconnects with leading-edge link bandwidths, much lower latencies...

HPC 互连通常强调：

- 极低延迟；
- 极高带宽；
- barrier synchronization 硬件支持；
- scatter/gather 硬件支持；
- collective acceleration；
- global address space；
- RDMA；
- one-sided communication；
- 网络与 CPU cache/虚拟地址集成。

典型 HPC 互连包括：

- InfiniBand；
- Cray Slingshot；
- Intel OmniPath；
- 专有 torus；
- 专有 dragonfly；
- 定制互连。

---

#### 12.3 WSC 更强调成本、规模和通用性

WSC 网络通常更强调：

- 商用 Ethernet；
- merchant silicon；
- Clos/fat-tree；
- oversubscription；
- 多租户；
- 故障容忍；
- 成本效率；
- 可运维性；
- 大规模部署。

而 HPC 更强调：

- 极致低延迟；
- 极致 collective performance；
- 紧耦合并行；
- nonblocking；
- 专用互连。

---

#### 12.4 但两者正在融合

原文：

> Increasingly Ethernet, HPC optimized variants of Ethernet, and Infiniband have started to dominate Supercomputing as the performance of commodity interconnects continues to improve rapidly.

随着商用网络性能提升，HPC 和 WSC 网络界限越来越模糊。

例如：

- RoCE；
- RDMA over Ethernet；
- Ultra Ethernet；
- 高性能 Ethernet；
- InfiniBand；
- AI 训练集群；
- GPU superpod；
- TPU pod。

AI 训练网络尤其像 HPC：

- all-reduce；
- all-gather；
- all-to-all；
- 低延迟；
- 高带宽；
- 紧耦合；
- 大规模同步。

所以现代 AI 集群常常同时具有：

```text
WSC 的规模和成本意识
+
HPC 的低延迟高带宽互连需求
```

---

### 13. 与前面章节的联系

---

#### 13.1 与 6.2.2 hardware racks 的联系

6.2.2 提到：

- ToR；
- data center fabric；
- rack；
- pod；
- accelerator rack。

6.4.3 具体展开：

```text
ToR 如何通过 Clos 连接到 aggregation/spine/fabric
```

---

#### 13.2 与 6.3 accelerators 的联系

AI 加速器集群对网络要求极高。

例如：

- GPU pod 需要 InfiniBand/Ethernet；
- TPU pod 使用 ICI/OCS；
- all-reduce 对 bisection bandwidth 敏感；
- 网络拓扑影响并行策略。

6.4.3 的 Clos/oversubscription/HPC 比较，正是理解 AI 网络的基础。

---

#### 13.3 与 6.4.2 host networking 的联系

主机侧 IPU 处理：

- 虚拟化；
- 加密；
- QoS；
- traffic shaping；
- congestion control endpoint。

集群网络处理：

- leaf/spine；
- bisection bandwidth；
- oversubscription；
- optical cost；
- fabric scaling。

两者共同决定端到端性能。

---

### 14. 关键术语表

|术语|含义|
| --------------------------| -----------------------------|
|cluster networking|集群网络|
|merchant silicon|商用交换芯片|
|bisection bandwidth|二分带宽|
|Clos network|多级交换网络|
|fat-tree|胖树网络|
|leaf switch|接入层交换机|
|spine switch|脊交换机|
|ToR|Top-of-Rack switch|
|aggregation block|聚合模块|
|middle block|中间层模块|
|spine block|脊层模块|
|oversubscription|超额订阅/带宽收敛|
|full bisection bandwidth|全二分带宽|
|nonblocking|无阻塞|
|optical transceiver|光模块|
|reach|光链路最大距离|
|link budget|链路预算|
|SNR|信噪比|
|Jupiter|Google 数据中心 Clos 网络|
|Centauri|Jupiter 中的交换机构建块|
|FBR|Fabric Border Router|
|locality|局部性|
|HPC|High-Performance Computing|
|InfiniBand|高性能网络互连|
|RDMA|Remote Direct Memory Access|
|global address space|全局地址空间|
|collective communication|集合通信|
|barrier synchronization|屏障同步|
|scatter/gather|分散/聚集操作|

---

### 15. 可以用来检验理解的问题

---

#### 问题 1：为什么不能直接造一个超大交换机连接所有服务器？

因为交换芯片受功耗、引脚、封装、SerDes、良率和散热限制。

单芯片容量有限，所以必须用多级 Clos/fat-tree 将多个小交换机组合成大 fabric。

---

#### 问题 2：Clos 网络的基本思想是什么？

Clos 网络把交换机端口分为：

```text
向下连服务器
向上连 spine
```

每个 leaf 到另一个 leaf 有多条路径，每条路径经过不同 spine。

这提供：

- 高带宽；
- 多路径；
- 冗余；
- 负载均衡；
- 可扩展性。

---

#### 问题 3：为什么集群越大，每台服务器的网络成本越高？

因为多级 Clos 中，每个服务器端口需要经过更多交换层级。

这意味着：

- 更多交换机端口；
- 更多光模块；
- 更多线缆；
- 更多功耗；
- 更多设备成本。

所以 full-throughput 大集群成本很高。

---

#### 问题 4：为什么光模块成本如此重要？

因为超过几米的链路通常需要光接口。

光链路成本包括：

- 光模块；
- 光纤；
- 端接；
- 安装；
- 测试。

在数据中心网络中，光模块常常是最大的单项成本之一。

---

#### 问题 5：什么是 oversubscription？

oversubscription 指服务器总带宽大于上行 fabric 带宽。

例如 3:1 oversubscription：

```text
服务器侧总带宽 : fabric 侧总带宽 = 3:1
```

它可以降低网络成本，但在所有服务器同时满负载时，平均可用带宽会下降。

---

#### 问题 6：为什么 WSC 常在 ToR 以北做 oversubscription？

因为机架内 full bandwidth 比较便宜，可以用单台 ToR 实现。

但如果机架上行也 full bandwidth，会导致 aggregation/core 层规模爆炸，成本过高。

所以通常在 ToR 以北做 oversubscription。

---

#### 问题 7：Jupiter 网络的关键设计是什么？

Jupiter 使用：

- low-radix merchant silicon；
- 多级 Clos；
- leaf/spine；
- aggregation blocks；
- spine blocks；
- oversubscription；
- external aggregation blocks；
- Fabric Border Routers；
- 调度局部性优化。

它用大量小商用交换芯片构建超大规模数据中心网络。

---

#### 问题 8：WSC 网络和 HPC 网络的主要区别是什么？

WSC 网络更强调：

- 成本；
- 规模；
- 通用 Ethernet；
- oversubscription；
- 多租户；
- 可运维。

HPC 网络更强调：

- 极低延迟；
- 极高带宽；
- collective acceleration；
- barrier/scatter/gather；
- global address space；
- 紧耦合并行。

但 AI 时代两者正在融合。

---

### 16. 这一节可以整理成的精简笔记

```text
6.4.3 Cluster networking

1. 核心问题：
   WSC cluster 要高速互连数千甚至数万台服务器。
   但单颗交换芯片受功耗、引脚、封装和工艺限制，
   无法无限扩大，因此必须用多级 Clos/fat-tree
   将多个小交换芯片组合成大 fabric。

2. 单芯片交换容量限制：
   - 2024 年左右典型商用交换芯片约 51.2 Tbps；
   - 例如 128 × 400 GbE；
   - 单芯片很难超过 200 Tbps；
   - 原因是 power-limited 和 pin-limited；
   - 因此需要 cascading switch chips。

3. Clos / fat-tree 基本思想：
   - leaf switch 端口分为向下服务器端口和向上 spine 端口；
   - k-port switch 可一半向下、一半向上；
   - 每个 leaf 到另一个 leaf 有多条路径；
   - 每条路径经过不同 spine；
   - 提供多路径、冗余、负载均衡和可扩展性。

4. 递归构建：
   - switch chip 可组成 chassis；
   - chassis 可组成 block；
   - block 可组成 data center fabric；
   - 多级 Clos 看起来像一个大型虚拟交换机；
   - Figure 6.24 展示 three-stage Clos topology。

5. 规模与成本：
   - 多级 Clos 可支持非常大的服务器规模；
   - 但每增加一级，路径涉及更多交换端口；
   - 单级中央交换路径只需 2 个端口；
   - 多级网络可能需要约 10 个端口；
   - 每个服务器端口需要匹配更多 switch ports；
   - 因此集群越大，full-throughput 每服务器成本越高。

6. bisection bandwidth：
   - 把网络切成两半后可用的最小总带宽；
   - full bisection bandwidth 意味着任意两半可线速通信；
   - WSC 东西向流量大，因此 bisection bandwidth 很关键；
   - 但 full bisection bandwidth 成本很高。

7. 光模块成本：
   - 超过几米的链路通常需要光接口；
   - 100m 100Gbps 光链路成本可达数百美元；
   - 包括光模块、光纤、端接和安装；
   - 光模块是数据中心网络最大单项成本之一；
   - 不同距离使用不同 reach 的光模块；
   - 短距优化可显著降低成本和功耗；
   - Google Saturn 曾使用非标准光模块降低成本。

8. Oversubscription：
   - 为降低成本，常在 ToR 以北做 oversubscription；
   - 机架内 full bandwidth 比较便宜；
   - 如果整个 fabric 都 1:1 full bandwidth，会非常昂贵；
   - oversubscription 提高 server:fabric 带宽比；
   - 2:1 oversubscription：所有服务器同时发送时平均带宽减半；
   - 3:1 或更高很常见；
   - 例：64-port 200G ToR，48 servers + 16 uplinks = 3:1；
     每台服务器平均 fabric 带宽约 66.7Gbps。

9. Oversubscription 的权衡：
   - 优点：降低交换机、光模块、功耗和布线成本；
   - 缺点：worst-case 跨机架带宽下降；
   - 需要依赖流量局部性、调度、QoS 和拥塞控制；
   - 对 all-to-all 或 incast 敏感 workload 不友好。

10. Google Jupiter：
   - 第一代 Jupiter bisection bandwidth 达 1.3 Pb/s；
   - 使用 low-radix merchant silicon；
   - 每芯片 16 × 40Gbps 端口；
   - 40G 端口可拆成 4 × 10G；
   - 主要构建块是 Centauri：
       4RU chassis，两个 line cards，每个 line card 两个 switch chips；
   - ToR 示例：每芯片 48 × 10G 向服务器，16 × 10G 向 fabric；
       oversubscription = 3:1；
   - 服务器可用 40G mode 获得 burst bandwidth。

11. Jupiter aggregation：
   - ToR 连接到 aggregation blocks；
   - Middle Block 有四个 Centauri chassis；
   - 逻辑上是 two-stage non-blocking network；
   - 提供 256 × 10G 连 ToR；
   - 提供 64 × 40G 连 spine blocks。

12. 外部连接：
   - Jupiter 有单独 aggregation block 做 external connectivity；
   - 经验法则：外部带宽约为集群内部总带宽的 10%；
   - 使用 1 到 3 个 aggregation blocks；
   - intra-cluster fabric 通过 Fabric Border Routers 连到 inter-cluster network；
   - job scheduler 利用 building/campus locality 降低跨域流量。

13. WSC vs HPC：
   - HPC 应用计算/网络带宽比更低；
   - 天气模拟等应用频繁交换邻居数据；
   - HPC 传统使用专有互连；
   - 强调低延迟、barrier、scatter/gather、global address space；
   - WSC 更强调 Ethernet、merchant silicon、Clos、成本和规模；
   - 随着 Ethernet、InfiniBand 和高性能互连发展，
     HPC 和 WSC 网络正在融合，尤其在 AI 训练集群中。

14. 总结：
   集群网络设计的核心不是“买更大的交换机”，
   而是用 Clos/fat-tree 把大量小交换芯片组织成可扩展 fabric。
   设计必须同时考虑：
   单芯片容量、bisection bandwidth、光模块成本、
   oversubscription、局部性、调度、功耗、运维和 TCO。
   Jupiter 是这一思想的典型实践：
   用 low-radix merchant silicon、多级 Clos、
   aggregation blocks、oversubscription 和 locality-aware scheduling
   构建超大规模数据中心网络。
```

---

### 17. 如果考试或讨论中要回答这一节，可以这样说

> 6.4.3 节讨论 WSC 集群网络如何互连成千上万台服务器。核心问题是：我们无法制造或购买任意大的单台交换机，因为交换芯片受功耗、引脚、封装和工艺限制。2024 年左右典型商用交换芯片容量约为 51.2 Tbps，例如 128 个 400GbE 端口，但单芯片很难做到 200 Tbps 以上。因此，现代数据中心网络通常使用 Clos 或 fat-tree 结构，把大量低基数商用交换芯片级联成大型 fabric。
>
> Clos 网络的基本思想是，每个 leaf switch 把端口分成向下连接服务器的端口和向上连接 spine 的端口。对于 k 端口交换机，理想情况下可以用 k/2 端口连服务器，k/2 端口连 spine。这样每个 leaf 到另一个 leaf 都有多条路径，每条路径经过不同 spine，从而提供高带宽、冗余和负载均衡。实际网络会递归应用这一结构：交换芯片组成 chassis，多个 chassis 组成 block，多个 block 组成整个数据中心 fabric。
>
> 多级 Clos 可以扩展到非常大的规模，但成本也会上升。单级中央交换机中，一条路径只需要两个交换机端口；而在多级网络中，每个服务器端口需要经过更多交换层级，可能需要约 10 个端口。因此，随着集群规模和 bisection bandwidth 增长，每台服务器的网络连接成本也会增长。光模块成本尤其重要，因为超过几米的链路通常需要光接口，而光模块、光纤、端接和安装成本可能占网络成本的最大单项。数据中心内大多数链路距离较短，因此可以使用短距优化光模块来降低成本和功耗。
>
> 为了进一步降低成本，WSC 常在 ToR 以北做 oversubscription。机架内 full bandwidth 比较便宜，因为一个 ToR 就可以连接机架内所有服务器。但如果每个 ToR 都以 1:1 带宽上行到 fabric，整个网络会非常昂贵。oversubscription 通过减少上行带宽来降低成本。例如 2:1 oversubscription 下，每台服务器仍可峰值达到 NIC 带宽，但如果所有服务器同时发送，平均带宽减半；3:1 或更高也很常见。例如一个 64 端口 200G ToR 可以连接 48 台服务器和 16 个上行端口，形成 3:1 oversubscription，每台服务器平均 fabric 带宽约 66.7Gbps。
>
> Google 的 Jupiter 网络是典型 Clos 实践。第一代 Jupiter 的 bisection bandwidth 达到 1.3 Pb/s，使用 low-radix merchant silicon 构建。每个交换芯片支持 16 个 40Gbps 端口，并可拆分为 4 个 10Gbps 端口。Jupiter 的主要构建块是 Centauri，一个 4RU chassis，包含两个 line card，每个 line card 有两个交换芯片。在 ToR 配置中，每个芯片可以用 48 个 10G 端口连服务器，16 个 10G 端口连 fabric，形成 3:1 oversubscription。ToR 再连接到 aggregation blocks，其中 Middle Block 由四个 Centauri chassis 组成，逻辑上是 two-stage non-blocking network，并通过 spine blocks 连接到更大 fabric。Jupiter 还使用单独的 aggregation block 提供外部连接，经验上外部带宽约为集群内部总带宽的 10%。集群 fabric 通过 Fabric Border Routers 连接到 inter-cluster 网络，调度系统则利用 building 和 campus locality 来减少跨域流量。
>
> 最后，原文比较了 WSC 和 HPC 网络。HPC 应用通常计算/网络带宽比更低，例如天气模拟需要频繁在节点间交换数据，因此传统 HPC 使用专有互连，强调极低延迟、barrier synchronization、scatter/gather 和 global address space。WSC 网络则更强调 Ethernet、merchant silicon、Clos、成本、规模和可运维性。但随着 Ethernet、InfiniBand 和高性能互连的发展，HPC 和 WSC 网络正在融合，尤其在 AI 训练集群中，既需要 WSC 级别的规模和成本意识，也需要 HPC 级别的低延迟和高带宽。
>
> 总体而言，这一节的核心结论是：WSC 集群网络不是靠单一超大交换机，而是靠 Clos/fat-tree、多级 aggregation、光互连优化、oversubscription 和 locality-aware scheduling 共同实现大规模、高带宽、低成本和可运维的集群互连。


**专栏导航**

- ← 上一篇：[6.4 Networking](/posts/6-4-networking/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.4.4 Spine-less networking →](/posts/6-4-4-spine-less-networking/)
