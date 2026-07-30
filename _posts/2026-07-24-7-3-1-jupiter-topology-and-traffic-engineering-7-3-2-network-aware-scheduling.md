---
title: "7.3.1 Jupiter topology and traffic engineering 和 7.3.2 Network aware scheduling"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：7.3.1 Jupiter topology and traffic engineering 和 7.3.2 Network aware scheduling。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.3.1 Jupiter topology and traffic engineering 和 7.3.2 Network aware scheduling。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.3.1 Jupiter topology and traffic engineering 和 7.3.2 Network aware scheduling

下面把 **7.3.1 Jupiter topology and traffic engineering** 和 **7.3.2 Network aware scheduling** 放在一起深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这两小节都讲的是：

> SDN 不只是“把网络控制集中起来”，还要用全局视图去优化网络拓扑、流量路径和任务调度。

---

### 7.3.1 Jupiter topology and traffic engineering 深入理解

这一节的核心是：

> 数据中心网络通过 Topology Engineering 和 Traffic Engineering 一起优化吞吐量和效率。

可以把这两个概念理解为：

|概念|优化对象|时间尺度|主要问题|
| ----------------------| --------------------| ------------| ----------------------------------------|
|Topology Engineering|物理网络结构|慢，计划性|网络应该长什么样？哪些块之间需要直连？|
|Traffic Engineering|流量在路径上的分配|快，动态|当前流量应该走哪条路？如何避免拥塞？|

它们一个管“路怎么修”，一个管“车怎么走”。

---

#### 一、Topology Engineering：根据流量模式设计网络拓扑

原文说：

> Topology Engineering exploits the fact that multi-tenant and building-scale fabrics exhibit predictable traffic patterns with manageable uncertainty.

也就是说：

> 多租户和建筑级数据中心网络的流量模式具有可预测性，并且不确定性可以管理。

这是 Topology Engineering 能成立的前提。

---

##### 1. 为什么流量可预测？

在超大规模数据中心中，很多流量不是完全随机的。

例如：

- 某些服务之间长期有大量通信；
- 某些存储系统和计算集群之间流量稳定；
- 某些用户流量有周期性；
- 某些机器学习训练任务有固定通信模式；
- 某些模块之间的调用关系长期存在。

因此，从“块”级别看，流量矩阵往往有规律：

```text
Block A ↔ Block B：很高流量
Block A ↔ Block C：中等流量
Block B ↔ Block D：低流量
```

这给了网络设计者机会：

> 不必按照最坏情况设计网络，而可以根据真实流量模式设计拓扑。

---

#### 2. 传统 Clos 拓扑的问题

原文提到：

> we don’t need to provision for non-blocking forwarding of worst-case traffic in a Clos topology.

先理解几个概念。

---

##### Clos topology

在 Chapter 6 中，Jupiter 网络使用 five-stage Clos topology。

简化理解，Clos 通常是：

```text
服务器
  ↓
ToR / leaf switch
  ↓
spine switches
  ↓
其他 leaf / ToR
  ↓
其他服务器
```

Clos 的优点是：

- 结构规则；
- 容易扩展；
- 多路径；
- 适合 ECMP；
- 适合大规模数据中心。

但完整 Clos 如果要做到：

> non-blocking forwarding

也就是任意端口之间都能同时以全线速通信，成本会很高。

---

##### non-blocking forwarding

non-blocking 意思是：

> 即使所有端口同时以最大带宽通信，网络也不会阻塞。

这在理论上很好，但代价是：

- 更多 spine switches；
- 更多链路；
- 更多光模块；
- 更多端口；
- 更高功耗；
- 更高成本。

而在真实数据中心中，所有服务器同时以最坏情况互相通信的概率很低。

所以原文说：

> 不需要为最坏情况流量提供 non-blocking forwarding。

这允许更便宜的设计。

---

#### 3. Topology Engineering 的做法：移除 spine blocks，建立 direct-connect fabrics

原文说：

> Topology Engineering removes spine blocks and creates direct-connect fabrics optimized through joint traffic and topology engineering.

也就是说：

> Topology Engineering 可以移除部分 spine blocks，直接在某些 block 之间建立直连链路。

这里的 block 可以理解为一组服务器、机架或网络单元。

传统方式可能是：

```text
Block A → spine → Block B
```

Topology Engineering 后可能变成：

```text
Block A → direct link → Block B
```

如果某些 block 之间流量很大，直连会更高效。

---

#### 4. direct-connect fabrics 的好处

原文列举了几个好处。

---

##### 好处 1：路径更短、更高效

原文说：

> yields shorter, more efficient paths

直连链路减少中间跳数。

例如：

```text
原来：
Block A → spine block → Block B

现在：
Block A → Block B
```

路径更短意味着：

- 延迟更低；
- 故障点更少；
- 中间设备负载更低；
- 转发效率更高。

---

##### 好处 2：降低成本和功耗

原文说：

> reduces costs and power consumption associated with spine blocks

spine blocks 需要：

- 交换机；
- ASIC；
- 光模块；
- 线缆；
- 电源；
- 散热；
- 运维。

如果可以用直连链路替代部分 spine blocks，就能降低：

- 资本支出，CapEx；
- 运营支出，OpEx；
- 功耗；
- 散热成本。

---

##### 好处 3：允许新 block 之间高速直连

原文说：

> allows higher-speed direct links between newer blocks without needing to refresh the intermediate spine blocks

这很重要。

如果所有流量都必须经过 spine blocks，那么升级新 block 之间的高速链路时，可能也要升级 spine blocks。

但如果允许 direct links：

```text
新 Block X ↔ 新 Block Y：直接升级到更高速链路
```

就不必同时刷新中间 spine。

这支持增量演进：

> 哪里需求高，就在哪里升级直连链路。

---

##### 好处 4：让拓扑与长期需求对齐

原文说：

> effectively aligning topology with long-term demand.

也就是说：

> 网络拓扑不是固定模板，而是根据长期流量需求演化。

高流量 block 之间加直连。  
低流量 block 之间可以走间接路径。  
这样网络投资更贴近真实需求。

---

### 二、Traffic Engineering：动态优化流量路径

原文说：

> Traffic Engineering dynamically optimizes traffic forwarding across different paths based on real-time demand.

Traffic Engineering，TE，关注的是：

> 在已有拓扑上，如何根据实时流量需求，把流量分配到不同路径。

---

#### 1. 为什么需要 TE？

原文说：

> compensating for imbalances caused by striping, failures, or management actions.

即使网络拓扑设计得很好，实际流量仍然可能不均衡。

原因包括：

---

##### 原因 1：striping 造成的不均衡

striping 指把流量分散到多条链路或路径上。

例如使用 ECMP 或 WCMP 把流哈希到不同路径。

但哈希可能造成：

- 某些路径过忙；
- 某些路径过闲；
- 大象流撞到同一条路径；
- 路径数量变化导致重新哈希。

因此需要 TE 动态调整。

---

##### 原因 2：故障

链路或交换机故障后，流量需要绕路。

例如：

```text
原本：
Block A → direct link → Block B

故障后：
Block A → Block C → Block B
```

TE 需要重新分配流量，避免绕路造成拥塞。

---

##### 原因 3：管理动作

例如：

- 维护某台交换机；
- 升级固件；
- 隔离某条链路；
- 改变策略；
- 迁移服务。

这些都会改变流量分布。

---

#### 2. 理想情况：流量直接流动

原文说：

> Ideally, traffic would flow directly between blocks.

最理想的是：

> 有流量的 block 之间都有直连链路。

但现实不可能完全做到，因为：

- 需求动态变化；
- 不可能所有 block 两两直连；
- 成本太高；
- 端口数量有限；
- 流量有不确定性。

所以原文说：

> in practice, demand varies and doesn’t perfectly match the topology.

---

#### 3. Jupiter 中的 TE：direct paths + one-hop indirect paths

原文说：

> In the Jupiter network, TE combines direct and one-hop indirect paths to balance performance and robustness.

也就是说，Jupiter 不只使用直连路径，也使用一跳间接路径。

例如：

```text
direct path:
Block A → Block B

one-hop indirect path:
Block A → Block C → Block B
```

为什么用 one-hop indirect？

因为它在性能和鲁棒性之间取得平衡。

---

##### direct path 的优点

- 延迟低；
- 路径短；
- 中间节点少；
- 适合高流量 block 对。

---

##### one-hop indirect path 的优点

- 提供冗余；
- 直连链路故障时可绕路；
- 可以平衡负载；
- 不需要完整 spine 层级；
- 提高拓扑灵活性。

---

### 三、Traffic Matrix 和 WCMP

原文进一步解释 TE 如何工作。

---

#### 1. Flow measurements 聚合成 block-level traffic matrix

原文说：

> Flow measurements from each server are aggregated into a block-level traffic matrix, with each entry indicating the bytes transferred between blocks.

也就是说：

> 每台服务器的流量测量数据被聚合成一个 block 级别的流量矩阵。

可以想象成：

||Block A|Block B|Block C|
| ---------| --------: | --------: | --------: |
|Block A|0|800 GB|100 GB|
|Block B|750 GB|0|200 GB|
|Block C|90 GB|180 GB|0|

每个条目表示：

> 某段时间内，从一个 block 到另一个 block 传输了多少字节。

---

#### 2. Predicted traffic matrix

原文说：

> This matrix feeds into a predicted traffic matrix used for Weighted Cost Multipathing, WCMP, optimization.

也就是说：

> 历史流量矩阵会生成预测流量矩阵，用于 WCMP 优化。

这个预测矩阵不是简单当前值，而是用来预测未来一段时间的流量需求。

---

#### 3. 预测矩阵使用过去一小时的峰值发送速率

原文说：

> composed of peak sending rates for each pair in the last hour.

也就是说：

> 对每一对 block，使用过去一小时内的峰值发送速率。

为什么用峰值？

因为网络容量规划通常要照顾高峰流量。

如果使用平均值，可能低估高峰拥塞。  
使用最近一小时的峰值是一种保守但实用的预测方式。

---

#### 4. 什么时候更新预测矩阵？

原文说：

> This predicted matrix is updated when large changes in observed traffic occur, or periodically for freshness.

更新条件有两类：

1. 观测到流量发生大变化；
2. 定期更新，保持新鲜。

这体现了典型的控制系统思想：

```text
监控流量
  ↓
发现显著变化
  ↓
更新预测
  ↓
重新计算路径权重
  ↓
下发新策略
```

---

### 四、WCMP 是什么？

原文提到：

> Weighted Cost Multipathing, WCMP.

WCMP 可以理解为：

> 带权重的多路径转发。

---

#### 1. ECMP 与 WCMP

ECMP，Equal-Cost Multipathing，是等价多路径：

> 多条路径成本相同，流量平均分配。

例如：

```text
路径 1：权重 1
路径 2：权重 1
路径 3：权重 1
```

WCMP 则允许不同路径有不同权重：

```text
路径 1：权重 5
路径 2：权重 3
路径 3：权重 2
```

这样可以根据：

- 链路容量；
- 预测流量；
- 路径质量；
- 拥塞情况；
- 故障状态；

来分配流量。

---

#### 2. WCMP 在 TE 中的作用

TE 根据预测流量矩阵计算：

- 哪些 block 对流量高；
- 哪些直连链路应该承担更多流量；
- 哪些间接路径可以分担；
- 如何避免某些链路过载。

然后通过 WCMP 权重把流量分配到不同路径。

---

### 五、Topology Engineering 和 Traffic Engineering 的时间尺度不同

原文说：

> Traffic engineering and topology engineering operate at different times scales.

这很关键。

---

#### 1. Traffic Engineering 快速适应

TE 处理的是：

- 实时流量变化；
- 链路故障；
- 短期拥塞；
- 管理动作；
- 流量矩阵变化。

它的时间尺度较快，可能是：

- 秒级；
- 分钟级；
- 小时级。

---

#### 2. Topology Engineering 是慢速计划过程

原文说：

> topology engineering is a slower, planned process for implementing new network structures.

Topology Engineering 涉及物理变化：

- 增加链路；
- 移除 spine blocks；
- 部署新交换机；
- 调整光模块；
- 改变 block 直连关系；
- 升级网络结构。

因此它的时间尺度较慢，可能是：

- 周级；
- 月级；
- 季度级；
- 年级。

---

#### 3. 两者配合

可以这样理解：

```text
Topology Engineering：
决定道路结构，修哪些高速公路。

Traffic Engineering：
决定车辆如何走，如何实时导流。
```

如果只有拓扑设计，没有 TE，网络无法应对实时变化。  
如果只有 TE，没有拓扑设计，物理路径可能本身不够高效。

两者结合，才能在成本、性能和鲁棒性之间取得平衡。

---

### 六、Host-based Multipathed Network Load Balancing

原文最后说：

> To address potential load balancing issues across parallel links, host-based Multipathed Network Load Balancing adaptively distributes traffic based on congestion at the RTT level.

这是另一个层次的负载均衡。

---

#### 1. 为什么网络侧多路径还不够？

即使网络使用 ECMP 或 WCMP，仍然可能出现：

- 哈希不均；
- 大象流冲突；
- 某些路径拥塞；
- 某些路径 RTT 增加；
- 路径故障恢复后负载不均。

网络侧负载均衡不一定能感知每条主机流的真实拥塞。

---

#### 2. 主机侧多路径负载均衡

host-based Multipathed Network Load Balancing 是：

> 在主机端根据拥塞情况自适应分配流量。

它可以根据：

- RTT 变化；
- 丢包；
- 拥塞信号；
- 路径延迟；
- 吞吐表现；

来决定把不同流或子流放到哪条路径。

---

#### 3. RTT-level congestion 的含义

RTT，Round-Trip Time，往返时延。

如果某条路径 RTT 明显升高，通常意味着：

- 队列变长；
- 链路拥塞；
- 交换机缓冲增加；
- 路径质量下降。

主机可以据此判断：

> 这条路径可能拥塞。

然后把部分流量迁移到其他路径。

---

### 七、7.3.1 的核心逻辑

```text
数据中心流量具有可预测性
  ↓
不需要为最坏情况做完全 non-blocking Clos
  ↓
Topology Engineering 根据长期流量设计拓扑
  ↓
移除部分 spine blocks，增加 direct-connect fabrics
  ↓
降低成本、功耗，缩短路径
  ↓
Traffic Engineering 根据实时需求分配流量
  ↓
使用 traffic matrix、predicted matrix、WCMP
  ↓
结合 direct path 和 one-hop indirect path
  ↓
主机侧多路径负载均衡进一步缓解拥塞
```

---

### 7.3.2 Network aware scheduling 深入理解

这一节从网络层进一步扩展到：

> 集群调度器如何感知网络状态。

前面 7.3.1 主要讲网络自身如何优化。  
7.3.2 讲的是：

> 计算和存储任务的调度也要考虑网络流量和热点。

这正是 software-defined infrastructure 的进一步体现：

> 不只是网络控制器知道网络状态，集群调度器也要知道网络状态。

---

#### 一、为什么调度器需要感知网络？

原文说：

> Network aware scheduling provides proactive and reactive mechanisms for placing compute and storage jobs, enhancing centralized schedulers like Borg with insights into network traffic patterns and sustained hotspots.

也就是说：

> 网络感知调度为计算和存储任务放置提供主动和被动机制，使 Borg 等集中调度器能够了解网络流量模式和持续热点。

传统调度器主要看：

- CPU；
- memory；
- disk；
- GPU；
- 存储容量；
- 机器亲和性；
- 优先级；
- SLO。

但网络也可能成为瓶颈。

如果调度器不知道网络状态，可能会出现：

- 把两个高通信任务放到跨 block 位置；
- 把带宽密集型任务放到延迟敏感服务附近；
- 把多个大象流任务放到同一组链路；
- 网络故障后仍把任务放到拥塞区域；
- 计算资源充足，但网络拥塞导致性能下降。

因此调度器需要网络感知。

---

### 二、网络热点从哪里来？

原文说：

> These hotspots, often caused by workload fluctuations or network failures, can impact performance.

网络热点常来自：

---

#### 1. 工作负载波动

例如：

- 批处理任务突然 shuffle 大量数据；
- 机器学习训练进入 all-reduce 阶段；
- 数据备份任务开始；
- 视频转码任务高峰；
- 某个服务流量突增；
- 日志聚合突然增加。

这些都会造成某些链路或交换机拥塞。

---

#### 2. 网络故障

例如：

- 某条链路故障；
- 某台交换机故障；
- 某个 spine block 维护；
- 某条光链路质量下降。

故障后流量绕路，可能导致原本不拥塞的路径变成热点。

---

### 三、Network aware scheduling 的两类机制

原文把机制分成：

1. proactive，主动；
2. reactive，被动/响应式。

---

#### 1. Proactive：主动任务放置

原文说：

> Network aware scheduling proactively binpacks jobs within a cluster, considering not only compute and storage utilization but also network bandwidth.

也就是说：

> 网络感知调度在任务放置时主动进行 binpacking，不仅考虑计算和存储利用率，也考虑网络带宽。

---

##### 什么是 binpacking？

binpacking 是“装箱”思想：

> 把任务尽量紧凑地放到合适资源容器中，提高利用率，减少碎片。

传统 binpacking 可能看：

```text
CPU 剩余
内存剩余
磁盘剩余
GPU 剩余
```

网络感知 binpacking 还会看：

```text
网络带宽剩余
block 间流量矩阵
链路热点
任务通信模式
任务对延迟的敏感度
```

---

##### 主动调度的例子

假设有两个任务：

- Task A：计算密集型，但网络流量低；
- Task B：网络密集型，需要和 Block X 大量通信。

网络感知调度可能把 Task B 放到靠近 Block X 的位置，减少跨 block 流量。

再比如：

- Task C：延迟敏感服务；
- Task D：带宽密集型批处理任务。

调度器可能避免把 Task D 放到 Task C 附近，防止网络干扰。

---

#### 2. Reactive：响应式迁移

原文说：

> reactive mechanisms within network-aware scheduling can relocate demanding jobs away from latency-sensitive workloads in the event of network disruptions or changes in traffic patterns.

也就是说：

> 当网络中断或流量模式变化时，响应式机制可以把高资源需求任务从延迟敏感工作负载附近迁移走。

---

##### 响应式调度的例子

假设原本：

```text
延迟敏感服务 S 和批处理任务 B 在同一区域
```

平时没问题。

但某条链路故障后，B 的流量绕路，导致 S 所在区域网络拥塞。

网络感知调度可以：

- 检测到持续热点；
- 判断 B 是主要干扰源；
- 把 B 迁移到其他区域；
- 保护 S 的延迟 SLO。

这就是响应式网络感知调度。

---

### 四、Network aware scheduling 与拥塞控制的关系

原文说：

> Through proactive and reactive schemes, network aware scheduling complements per-flow congestion control mechanisms, which focus on managing individual flows to maximize link utilization.

也就是说：

> 网络感知调度和 per-flow congestion control 是互补关系。

---

#### 1. per-flow congestion control 是什么？

per-flow congestion control 是：

> 针对单个流进行拥塞控制。

例如 TCP 拥塞控制会做：

- 检测丢包；
- 检测 RTT 增加；
- 调整拥塞窗口；
- 降低发送速率；
- 避免链路过载。

它关注的是：

> 已经存在的流如何公平、高效地共享链路。

---

#### 2. per-flow congestion control 的局限

拥塞控制很重要，但它主要是事后反应。

它可能无法解决：

- 任务放置本身不合理；
- 多个重任务被放到同一区域；
- 高通信任务远离数据源；
- 延迟敏感服务和批处理任务混部在拥塞链路附近；
- 结构性网络热点。

换句话说：

> 拥塞控制管理流，但不改变任务布局。

---

#### 3. network aware scheduling 补充拥塞控制

网络感知调度从更高层次解决问题：

```text
拥塞控制：
让现有流不要太 aggressive。

网络感知调度：
从一开始就避免把任务放到会造成严重拥塞的位置。
```

两者结合：

|机制|层次|作用|
| -----------------------------| --------| --------------------------------|
|per-flow congestion control|流级|控制发送速率，最大化链路利用|
|network aware scheduling|任务级|放置和迁移任务，避免结构性热点|
|traffic engineering|路径级|调整流量路径和权重|
|topology engineering|拓扑级|改变物理路径结构|

---

### 五、网络、调度、应用三者的协同

这两小节合起来说明：

> 在 WSC 中，网络优化不是孤立进行的，而是和计算调度、存储放置、应用需求协同。

可以形成一个多层优化体系：

```text
Topology Engineering
    ↓
决定物理路径结构

Traffic Engineering
    ↓
决定流量路径和权重

Network-aware Scheduling
    ↓
决定计算/存储任务放在哪里

Per-flow Congestion Control
    ↓
控制单个流的发送行为

Host-based Multipath Load Balancing
    ↓
主机侧根据 RTT 调整路径使用
```

这正是 software-defined infrastructure 的核心：

> 用集中软件控制，把网络、计算、存储和应用作为一个整体来优化。

---

### 六、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.3.1 Jupiter topology and traffic engineering

1. 核心目标：
   - 优化数据中心网络吞吐量和效率
   - 使用两类工程：
     - Topology Engineering
     - Traffic Engineering

2. Topology Engineering：
   - 利用多租户和建筑级 fabric 流量可预测
   - 不需要为 Clos 最坏情况流量做完全 non-blocking
   - 可以设计更便宜但仍满足容量需求的拓扑
   - 方法：
     - 移除部分 spine blocks
     - 创建 direct-connect fabrics
     - 联合流量和拓扑工程优化网络结构

3. Topology Engineering 的好处：
   - 路径更短、更高效
   - 降低 spine blocks 带来的成本和功耗
   - 新 block 之间可直接使用更高速链路
   - 不需要为了升级新 block 而刷新中间 spine blocks
   - 让网络拓扑与长期流量需求对齐

4. Traffic Engineering，TE：
   - 根据实时需求动态优化流量转发路径
   - 补偿由以下原因造成的不平衡：
     - striping
     - failures
     - management actions
   - 理想情况：
     - 流量直接在 block 之间流动
   - 实际情况：
     - 需求变化
     - 不可能完全匹配拓扑

5. Jupiter 中的 TE：
   - 结合 direct paths 和 one-hop indirect paths
   - 平衡性能和鲁棒性
   - direct path：
     - 更短
     - 更快
     - 更适合高流量 block 对
   - one-hop indirect path：
     - 提供冗余
     - 故障绕路
     - 负载均衡

6. Traffic matrix：
   - 每台服务器的 flow measurements 聚合成 block-level traffic matrix
   - 每个条目表示 block 之间传输的字节数
   - 用于生成 predicted traffic matrix

7. Predicted traffic matrix：
   - 用于 Weighted Cost Multipathing, WCMP 优化
   - 由过去一小时每对 block 的 peak sending rates 组成
   - 更新时机：
     - 观测流量发生大变化
     - 定期更新以保持新鲜

8. WCMP：
   - Weighted Cost Multipathing
   - 带权重的多路径转发
   - 相比 ECMP，可以按路径容量和需求分配流量
   - 是 Traffic Engineering 的重要执行机制

9. 两种工程的时间尺度：
   - Traffic Engineering：
     - 快速适应拓扑和流量变化
   - Topology Engineering：
     - 慢速、计划性
     - 实现新的网络结构

10. Host-based Multipathed Network Load Balancing：
   - 解决并行链路负载均衡问题
   - 在主机侧自适应分配流量
   - 根据 RTT 级别拥塞信号调整路径使用
   - 补充网络侧 ECMP/WCMP

11. 核心逻辑：
   流量模式可预测
     → 不必完全 non-blocking Clos
     → Topology Engineering 设计 direct-connect fabric
     → Traffic Engineering 动态分配流量
     → WCMP 优化路径权重
     → 主机侧多路径负载均衡缓解局部拥塞
```

```text
7.3.2 Network aware scheduling

1. 核心思想：
   - 集群调度器不仅考虑 compute 和 storage
   - 还要考虑 network traffic patterns 和 sustained hotspots
   - 例子：
     - 增强 Borg 等集中调度器

2. 为什么需要 network aware scheduling：
   - 网络热点会影响性能
   - 热点来源：
     - workload fluctuations
     - network failures
   - 如果调度器不感知网络：
     - 可能把高带宽任务放到延迟敏感任务附近
     - 可能造成结构性拥塞
     - 可能故障后仍把任务放到拥塞区域

3. Proactive 机制：
   - 主动 binpack jobs
   - 考虑：
     - compute utilization
     - storage utilization
     - network bandwidth
   - 目标：
     - 更合理放置任务
     - 减少跨 block 不必要流量
     - 避免网络热点

4. Reactive 机制：
   - 当网络中断或流量模式变化时
   - 将 demanding jobs 从 latency-sensitive workloads 附近迁移走
   - 目标：
     - 保护延迟敏感服务
     - 最小化网络拥塞影响
     - 保持资源利用率

5. 与 per-flow congestion control 的关系：
   - per-flow congestion control：
     - 管理单个流
     - 目标是最大化链路利用率
   - network aware scheduling：
     - 管理任务放置
     - 目标是避免结构性热点
   - 两者互补：
     - 一个控制已有流
     - 一个优化任务布局

6. 与其他网络优化的关系：
   - Topology Engineering：
     - 改变物理拓扑
   - Traffic Engineering：
     - 调整路径和权重
   - Network aware scheduling：
     - 调整计算/存储任务位置
   - Congestion control：
     - 调整单流发送速率
   - Host multipath load balancing：
     - 主机侧选择路径

7. 核心逻辑：
   网络状态会影响任务性能
     → 调度器需要感知网络流量和热点
     → proactive binpacking 优化任务放置
     → reactive relocation 应对故障和流量变化
     → 与拥塞控制共同提供可预测网络体验
```

---

### 七、一句话总结这两小节

> 7.3.1 说明 Jupiter 网络通过 Topology Engineering 优化物理结构、通过 Traffic Engineering 动态分配流量；7.3.2 进一步说明集群调度器也要感知网络热点，把计算和存储任务放置到合适位置；两者共同体现了 software-defined infrastructure 用全局视图协同优化网络与计算的核心思想。


**专栏导航**

- ← 上一篇：[7.3 Software-defined networks](/posts/7-3-software-defined-networks/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.3.3 Bandwidth enforcer 和 7.3.4 B4 traffic engineering →](/posts/7-3-3-bandwidth-enforcer-7-3-4-b4-traffic-engineering/)
