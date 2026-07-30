---
title: "7.3.3 Bandwidth enforcer 和 7.3.4 B4 traffic engineering"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-29
description: "《The Data Center as a Computer》AI 导读专栏正文：7.3.3 Bandwidth enforcer 和 7.3.4 B4 traffic engineering。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.3.3 Bandwidth enforcer 和 7.3.4 B4 traffic engineering。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.3.3 Bandwidth enforcer 和 7.3.4 B4 traffic engineering

下面把 **7.3.3 Bandwidth enforcer** 和 **7.3.4 B4 traffic engineering** 放在一起深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这两小节都讲的是：

> SDN 在 Google 广域网，也就是 WAN 中的实践。  
> 重点不再只是数据中心内部网络，而是数据中心之间、以及 Google 与外部互联网之间的网络优化。

---

### 7.3.3 Bandwidth enforcer 深入理解

这一节讲的是：

> 如何在 WAN 上实时分配和执行带宽。

核心系统是：

> Google’s Bandwidth Enforcer，简称 BwE。

---

#### 一、为什么 WAN 需要 Bandwidth Enforcer？

原文说：

> BwE is crucial for supporting distributed computing and large-scale data transfers.

WAN，Wide Area Network，广域网，连接不同数据中心。

WAN 和数据中心内部网络不同：

|维度|数据中心网络|WAN|
| ----------| ---------------------------------| ----------------------------------------|
|距离|建筑内或园区内|城市、国家、洲际|
|带宽成本|相对可控|非常昂贵|
|链路容量|容易扩展|扩展慢、成本高|
|故障影响|局部|可能影响全球服务|
|流量类型|东西向、shuffle、存储、服务通信|数据复制、批量传输、用户流量、视频流量|
|优化目标|低延迟、高吞吐|成本、利用率、优先级、可用性|

WAN 链路很贵，所以必须：

1. 尽量用满；
2. 不能让低优先级流量饿死高优先级流量；
3. 不能让某个应用占满所有带宽；
4. 要能应对链路故障；
5. 要支持大规模数据传输和分布式计算。

因此需要 BwE。

---

#### 二、BwE 的核心目标

原文说：

> It distributes WAN capacity amongst competing applications, prioritizing them based on business needs while maintaining high overall network utilization, and accounting for a global view of bandwidth and failure conditions.

可以拆成四个目标。

---

##### 1. 在竞争应用之间分配 WAN 容量

WAN 上有很多应用同时竞争带宽，例如：

- 用户请求流量；
- 视频流量；
- 数据复制；
- 机器学习训练数据传输；
- 日志聚合；
- 备份；
- 搜索索引更新；
- 内部服务通信。

这些应用的重要性不同。

BwE 要在它们之间分配带宽。

---

##### 2. 根据业务需求确定优先级

原文说：

> prioritizing them based on business needs

也就是说，不是所有流量平等。

例如：

|流量类型|可能优先级|
| ----------------------| ------------|
|用户交互流量|高|
|视频播放|高或中高|
|金融交易类流量|很高|
|数据复制|中|
|离线备份|低|
|批量数据迁移|低|
|可延迟的 ML 数据传输|低或弹性|

BwE 根据业务价值、SLO、用户体验和成本来决定优先级。

---

##### 3. 保持高整体网络利用率

WAN 链路昂贵，不能轻易闲置。

如果只强调优先级，可能会导致：

> 高优先级流量没用满时，低优先级流量也不敢用，链路浪费。

BwE 的目标不是简单限制流量，而是：

> 在保证高优先级应用的前提下，尽量让链路跑满。

这体现了系统优化中的常见思想：

> 隔离不是目的，利用率也要高。

---

##### 4. 考虑全局带宽和故障条件

BwE 不只看单条链路，而是看：

- 全局拓扑；
- 全局链路利用率；
- 全局流量需求；
- 故障链路；
- 备用路径；
- 应用优先级；
- 业务策略。

这就是 software-defined infrastructure 的核心：

> 用全局视图做带宽分配。

---

### 三、BwE 的层次结构

原文说：

> BwE uses global knowledge of network topology and link utilization as input to a hierarchy of bandwidth enforcers, ranging from a global enforcer down to rate enforcers on each host.

也就是说，BwE 是一个层级系统。

可以理解为：

```text
Global Enforcer
    ↓
Regional / Site Enforcers
    ↓
Cluster / Application Enforcers
    ↓
Host Rate Enforcers
```

---

#### 1. Global Enforcer

全局执行器拥有：

- 全局网络拓扑；
- 全局链路利用率；
- 全局流量需求；
- 全局故障状态；
- 全局业务优先级。

它负责做宏观决策：

- 每个应用可以获得多少 WAN 带宽；
- 每个数据中心可以发送多少流量；
- 哪些流量可以走哪些路径；
- 故障时如何重新分配；
- 如何保持高利用率。

---

#### 2. Host Rate Enforcers

原文特别强调：

> It actively controls the rate of traffic transmission at the source host, before traffic enters the network.

也就是说：

> BwE 在源主机上主动控制发送速率，在流量进入网络之前进行限制。

这一点很重要。

---

##### 为什么在源主机控制？

如果在网络中间控制流量，常见手段是：

- 丢包；
- 排队；
- 限速；
- 拥塞通知。

但这些方式可能造成：

- 已经浪费带宽；
- 数据包被丢弃；
- 重传；
- 延迟增加；
- 应用体验变差。

如果在源主机控制：

```text
应用/主机知道带宽配额
    ↓
按配额发送
    ↓
避免网络过载
```

好处是：

- 更早控制；
- 更少丢包；
- 更低延迟；
- 更好应用隔离；
- 更容易执行业务优先级；
- 更容易与拥塞控制协同。

---

### 四、BwE 如何使用 telemetry？

原文说：

> It utilizes telemetry data from both hosts and switches to understand traffic patterns and identify potential bottlenecks.

也就是说，BwE 使用两类 telemetry：

1. 主机侧 telemetry；
2. 交换机侧 telemetry。

---

#### 1. 主机侧 telemetry

主机可以提供：

- 应用发送需求；
- 每条流的速率；
- 每条流的目的地；
- 应用优先级；
- 拥塞窗口；
- RTT；
- 重传情况；
- 任务类型。

这帮助 BwE 理解：

> 谁想发多少流量，发给谁，优先级如何。

---

#### 2. 交换机侧 telemetry

交换机可以提供：

- 链路利用率；
- 队列长度；
- 丢包；
- 端口状态；
- 路径故障；
- 拥塞热点。

这帮助 BwE 理解：

> 网络哪里忙，哪里快拥塞，哪里已经故障。

---

### 五、BwE 与 per-flow congestion control 的关系

原文说：

> Host-based per-flow congestion control mechanisms complement BwE by providing a rapid response to congestion on a per round-trip time, RTT, basis.

也就是说：

> 基于主机的每流拥塞控制机制补充 BwE，提供 RTT 级别的快速拥塞响应。

这里要理解两种机制的时间尺度和职责不同。

---

#### 1. BwE：较长时间尺度的应用隔离

BwE 关注：

- 应用之间带宽分配；
- 业务优先级；
- 全局 WAN 利用率；
- 故障下的容量重分配；
- 防止应用互相干扰。

它的时间尺度相对较宽，例如：

- 秒级；
- 分钟级；
- 策略级。

BwE 的目标是：

> 让不同应用获得可预测的带宽份额。

---

#### 2. per-flow congestion control：RTT 级快速反应

per-flow congestion control 关注：

- 单条流；
- 丢包；
- RTT 增加；
- 拥塞窗口；
- 发送速率微调。

它的时间尺度很快，例如：

- 毫秒级；
- RTT 级。

它的目标是：

> 在拥塞刚出现时迅速降速，保持低丢包和低延迟。

---

#### 3. 两者互补

可以这样理解：

```text
BwE：
决定每个应用/主机“最多可以发多少”。

per-flow congestion control：
决定每条流“现在应该发多快”。
```

如果没有 BwE：

- 应用之间可能互相抢占；
- 低优先级流量可能影响高优先级流量；
- 全局策略难以执行。

如果没有 per-flow congestion control：

- 网络瞬时拥塞无法快速缓解；
- 队列可能迅速填满；
- 丢包和延迟会升高。

两者结合，才能在 WAN 上同时实现：

- 应用隔离；
- 高利用率；
- 低延迟；
- 低丢包；
- 可预测体验。

---

### 六、7.3.3 的核心逻辑

```text
WAN 带宽昂贵且多应用竞争
  ↓
需要根据业务优先级分配带宽
  ↓
BwE 使用全局拓扑、链路利用率和故障信息
  ↓
通过层级化 bandwidth enforcers 分配带宽
  ↓
在源主机控制发送速率
  ↓
使用主机和交换机 telemetry 识别瓶颈
  ↓
BwE 在较长时间尺度保证应用隔离
  ↓
per-flow congestion control 在 RTT 时间尺度快速响应拥塞
```

---

### 7.3.4 B4 traffic engineering 深入理解

这一节讲的是：

> 如何在跨数据中心 WAN 上优化路径和隧道。

核心系统是：

> B4 Traffic Engineering，B4 TE。

如果说 BwE 关注：

> 每个应用/主机能用多少带宽？

那么 B4 TE 关注：

> 这些流量应该走哪些路径？

---

#### 一、B4 TE 是什么？

原文说：

> B4 Traffic Engineering, a centralized traffic engineering service, optimizes network flow paths and tunnels across inter-data center WANs.

也就是说：

> B4 TE 是一个集中式流量工程服务，优化跨数据中心 WAN 上的流路径和隧道。

它是 SDN 在 WAN 中的典型应用。

---

#### 二、为什么集中式 TE 比传统分布式路由更好？

原文说：

> This approach yields superior resource utilization compared to traditional distributed routing methods.

传统路由协议，例如 OSPF、IS-IS、BGP，通常是分布式的。

它们的问题在于：

- 每台路由器只有局部视图；
- 路径选择基于局部或静态策略；
- 难以做全局流量优化；
- 容易造成某些链路过载，另一些链路闲置；
- 对流量需求变化反应不够灵活；
- 难以按应用优先级精细分配路径。

集中式 TE 则拥有：

- 全局拓扑；
- 全局链路状态；
- 全局流量需求；
- 全局应用优先级；
- 全局故障信息。

因此可以做：

> globally optimized path allocation，全局优化路径分配。

---

### 三、B4 TE 如何工作？

原文说：

> The centralized TE server receives real-time network topology, link state updates, and flow demands, then computes a globally optimized path allocation.

可以拆成输入、计算、输出三部分。

---

#### 1. 输入

TE server 接收：

##### real-time network topology

实时网络拓扑，包括：

- 哪些数据中心相连；
- 哪些链路存在；
- 链路容量；
- 链路故障；
- 网络设备状态。

---

##### link state updates

链路状态更新，包括：

- 链路利用率；
- 链路拥塞；
- 链路故障；
- 链路恢复；
- 维护状态。

---

##### flow demands

流量需求，包括：

- 哪个数据中心要发多少流量；
- 发往哪个数据中心；
- 属于哪个应用；
- 优先级如何；
- 是否有 SLO；
- 是否可以延迟；
- 是否可以拆分。

---

#### 2. 计算

TE server 计算：

> globally optimized path allocation

也就是全局最优路径分配。

它要同时考虑：

- 链路容量；
- 路径可用性；
- 应用优先级；
- 流量需求；
- 故障恢复；
- 负载均衡；
- 成本；
- 利用率。

---

#### 3. 输出

输出是：

- 每条流走哪条路径；
- 是否拆分到多条路径；
- 每条路径分配多少流量；
- 隧道如何建立；
- 故障时如何切换。

---

### 四、B4 TE 的目标：接近 100% 利用率

原文说：

> achieve near 100% utilization

WAN 链路非常昂贵。  
如果某些链路拥塞，而另一些链路闲置，就是巨大浪费。

集中式 TE 可以通过全局优化，让流量更均匀地分布在可用路径上。

例如：

```text
传统路由：
所有流量都走最短路径
    ↓
最短路径拥塞
其他路径闲置

集中 TE：
部分流量走最短路径
部分流量走次优路径
    ↓
整体利用率更高
```

这就是为什么集中式 TE 能比传统分布式路由获得更高资源利用率。

---

### 五、B4 TE 如何拆分流量？

原文说：

> splitting application flows among multiple paths to balance capacity against application priority/demands.

也就是说：

> B4 TE 可以把应用流拆分到多条路径上，以平衡容量和应用优先级/需求。

例如某个应用要从数据中心 A 发 100 Gbps 到数据中心 B。

如果只有一条路径，可能拥塞。  
TE 可以拆成：

```text
路径 1：40 Gbps
路径 2：35 Gbps
路径 3：25 Gbps
```

同时，对于高优先级应用，TE 可能给它更稳定、更低延迟路径。  
对于低优先级批量流量，TE 可能让它走剩余容量。

这体现了：

> 路径分配不只考虑容量，也考虑优先级。

---

### 六、B4 TE 是 overlay，传统路由是 fallback

原文说：

> Traffic Engineering continuously recalculates paths in response to changing network conditions and acts as an overlay, with traditional routing serving as a fallback in case of failures.

这很重要。

---

#### 1. TE 作为 overlay

TE 是在底层网络之上的一层集中控制逻辑。

它计算路径，然后通过隧道或转发规则引导流量。

底层网络仍然可以运行传统路由协议。

---

#### 2. 传统路由作为 fallback

如果：

- TE server 故障；
- 控制器不可达；
- 某些路径信息失效；
- 网络发生快速故障；

传统路由仍然可以作为兜底。

这提高了系统可靠性。

也就是说：

> SDN 不是完全抛弃传统路由，而是把传统路由作为安全网。

---

### 七、Protective ReRoute：主机侧快速重路由

原文说：

> To further enhance availability, host-based mechanisms, Protective ReRoute, adaptively reroute flows from end-hosts.

也就是说：

> 为了进一步提高可用性，Google 使用主机侧机制 Protective ReRoute，从端主机自适应重路由流。

---

#### 1. 什么是 black hole？

原文说：

> If a flow encounters a black hole due to a network failure.

black hole 指：

> 数据包被网络静默丢弃，发送方没有收到明确错误。

例如：

- 某条链路故障；
- 路由尚未收敛；
- 中间设备不知道如何转发；
- 包被丢弃；
- 发送方只发现 ACK 没回来。

---

#### 2. Protective ReRoute 如何工作？

如果主机发现某条流出现：

- ACK 延迟；
- 重传；
- RTT 异常；
- 疑似 black hole；

它可以在几个 RTT 内切换到替代路径。

原文说：

> path rerouting quickly switches to an alternative working path within a few round-trip times.

这比等待集中 TE 重新计算更快。

---

#### 3. 为什么需要主机侧快速重路由？

因为集中 TE 虽然全局最优，但时间尺度较慢。

对于短时间故障：

- 控制器可能还没来得及重算；
- 路由协议可能还没收敛；
- 用户流量已经受到影响。

主机侧快速重路由可以在：

```text
几个 RTT 内
```

切换路径，保持可用性。

---

### 八、B4 TE 与 Protective ReRoute 的时间尺度配合

原文总结：

> Such rapid repathing keeps the network available for user traffic in the face of failures even at short timescales, multiple RTTs, while TE provides high-quality routes at longer timescales.

也就是说：

> Protective ReRoute 在短时间尺度保证可用；  
> TE 在较长时间尺度提供高质量路径。

可以整理成时间尺度表。

|机制|时间尺度|职责|
| -----------------------------| --------------| ---------------------|
|per-flow congestion control|RTT 级|快速降速，避免拥塞|
|Protective ReRoute|几个 RTT|快速绕过 black hole|
|BwE|秒级到分钟级|应用带宽分配和隔离|
|B4 TE|秒级到分钟级|全局路径优化|
|Topology Engineering|周到月级|物理拓扑演进|

这体现了一个重要系统设计原则：

> 不同时间尺度的问题，用不同机制解决。

---

### 九、Espresso：把 SDN 扩展到全球 peering edge

原文最后介绍 Espresso。

---

#### 1. 什么是 peering edge？

peering edge 是 Google 网络与外部互联网或其他网络互联的边缘。

可以理解为：

> Google 网络与外部 ISP、运营商、其他网络之间的接口。

它面对的是：

- 终端用户；
- 外部网络；
- 不同运营商路径；
- 复杂 BGP 策略；
- 动态互联网性能变化。

---

#### 2. 传统 Internet Protocols 的问题

原文说：

> Espresso was developed to address the underutilization of peering links caused by traditional Internet Protocols.

传统互联网协议，例如 BGP，通常基于：

- 静态策略；
- IP 前缀；
- AS path；
- 路由属性；
- 运营商关系。

它们可能不会根据实时性能选择路径。

结果可能是：

- 某些 peering links 利用不足；
- 某些路径拥塞；
- 用户体验不佳；
- 故障切换慢；
- 无法根据应用质量优化路径。

---

#### 3. Espresso 的做法：动态选择 serving endpoints

原文说：

> Espresso dynamically selects serving endpoints based on real-time network performance rather than static assignments mapping users based on IP addresses.

传统方式可能：

```text
用户 IP 属于某地区
    ↓
静态映射到某个服务节点
```

Espresso 则：

```text
实时测量网络性能
    ↓
选择当前最优 serving endpoint
```

它考虑的不是静态地理映射，而是：

- 实时延迟；
- 丢包；
- 吞吐；
- 拥塞；
- 可用性；
- peering link 状态；
- 用户体验信号。

---

#### 4. Espresso 集中流量管理逻辑

原文说：

> Espresso centralizes traffic management logic, moving it from individual routers to a distributed system.

也就是说：

> Espresso 把流量管理逻辑从单个路由器移到一个分布式系统中。

这仍然是 SDN 思想：

```text
路由器只负责转发
    ↓
控制逻辑放到集中/分布式软件系统
```

---

#### 5. Espresso 利用 WSC 计算基础设施和应用信号

原文说：

> This system leverages WSC’s computing infrastructure together with application signals to analyze aggregated network data and optimize individual flows based on the end user’s experience.

也就是说，Espresso 不只使用网络层指标，还使用应用信号。

应用信号可能包括：

- 视频缓冲；
- 页面加载时间；
- 请求延迟；
- 错误率；
- 用户重试；
- 吞吐表现；
- 连接质量。

这使优化目标从：

> 网络路径看起来好不好

变成：

> 终端用户体验好不好

---

### 十、BwE、B4 TE、Espresso 的关系

这三个系统都属于 SDN 在 WAN 和边缘网络中的实践，但职责不同。

|系统|作用域|核心问题|
| ----------| ---------------------| ----------------------------------|
|BwE|WAN 带宽分配|每个应用/主机能用多少带宽？|
|B4 TE|跨数据中心 WAN 路径|流量应该走哪些路径？|
|Espresso|全球 peering edge|用户流量应该从哪个边缘节点服务？|

它们可以组合理解：

```text
BwE：
控制“发多少”。

B4 TE：
决定“怎么走”。

Espresso：
决定“从哪个边缘服务用户”。
```

---

### 十一、与前面 7.3.1 和 7.3.2 的关系

整个 7.3 后半部分形成了一个完整的 SDN 优化体系。

|小节|场景|优化对象|
| -------| --------------------------------| --------------------------------|
|7.3.1|数据中心网络 Jupiter|拓扑和流量工程|
|7.3.2|集群调度|计算/存储任务的网络感知放置|
|7.3.3|WAN 带宽|应用带宽分配和执行|
|7.3.4|跨数据中心 WAN 和 peering edge|路径优化、快速重路由、边缘选择|

共同思想是：

> 用集中软件控制、全局 telemetry 和多层级机制，把网络、计算和应用作为一个整体优化。

---

### 十二、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.3.3 Bandwidth enforcer

1. 核心系统：
   - Google Bandwidth Enforcer，BwE
   - 实时优化 WAN 带宽分配和执行
   - 支持分布式计算和大规模数据传输

2. BwE 的目标：
   - 在竞争应用之间分配 WAN 容量
   - 根据业务需求确定优先级
   - 保持高整体网络利用率
   - 考虑带宽和故障条件的全局视图

3. BwE 的输入：
   - 全局网络拓扑
   - 链路利用率
   - 故障条件
   - 主机和交换机 telemetry
   - 应用流量需求
   - 业务优先级

4. BwE 的层级结构：
   - global enforcer：
     - 全局带宽分配
     - 全局策略
   - 中间层级 enforcers：
     - 区域/站点/应用级分配
   - host rate enforcers：
     - 在源主机控制发送速率
     - 在流量进入网络前执行限制

5. 为什么在源主机控制速率：
   - 更早防止拥塞
   - 减少网络中丢包
   - 降低延迟
   - 更容易执行应用隔离
   - 更容易与拥塞控制协同

6. BwE 与 per-flow congestion control 的关系：
   - BwE：
     - 较长时间尺度
     - 应用间带宽隔离
     - 全局 WAN 利用率
   - per-flow congestion control：
     - RTT 时间尺度
     - 单流快速拥塞响应
     - 保持低丢包和低延迟
   - 两者互补：
     - BwE 决定应用/主机可以用多少带宽
     - congestion control 决定单流当前应该发多快

7. 核心逻辑：
   WAN 带宽昂贵
     → 多应用竞争带宽
     → BwE 用全局视图分配带宽
     → 在源主机执行速率限制
     → telemetry 识别瓶颈
     → per-flow congestion control 快速处理瞬时拥塞
```

```text
7.3.4 B4 traffic engineering

1. 核心系统：
   - B4 Traffic Engineering，B4 TE
   - 集中式 traffic engineering service
   - 优化跨数据中心 WAN 的 flow paths 和 tunnels

2. 为什么集中式 TE 优于传统分布式路由：
   - 传统路由：
     - 局部视图
     - 静态或分布式决策
     - 难以全局优化
     - 容易部分链路过载、部分链路闲置
   - 集中 TE：
     - 全局拓扑
     - 全局链路状态
     - 全局流量需求
     - 全局路径优化
     - 更高资源利用率

3. B4 TE 的输入：
   - real-time network topology
   - link state updates
   - flow demands

4. B4 TE 的输出：
   - globally optimized path allocation
   - 路径选择
   - 隧道分配
   - 多路径流量拆分
   - 故障下的路径调整

5. B4 TE 的优化目标：
   - 接近 100% 链路利用率
   - 平衡容量和应用优先级/需求
   - 将应用流拆分到多条路径
   - 高优先级流量获得更好路径
   - 低优先级流量使用剩余容量

6. B4 TE 作为 overlay：
   - TE 持续根据网络变化重算路径
   - TE 作为覆盖网络控制层
   - 传统路由作为 fallback
   - 当 TE 或控制器故障时，传统路由仍可提供基本转发

7. Protective ReRoute：
   - host-based mechanism
   - 从端主机自适应重路由流
   - 当流遇到 network failure 导致的 black hole：
     - 在几个 RTT 内切换到替代工作路径
   - 目标：
     - 在短时间尺度保持网络可用
     - 快速应对故障
     - 补充集中 TE 的较慢时间尺度

8. 时间尺度配合：
   - Protective ReRoute：
     - 几个 RTT
     - 快速故障恢复
   - B4 TE：
     - 较长时间尺度
     - 提供高质量全局路径
   - per-flow congestion control：
     - RTT 级
     - 快速拥塞控制

9. Espresso：
   - 将 SDN 扩展到 Google global peering edge
   - 目标：
     - 解决传统 Internet Protocols 导致的 peering links 利用不足
   - 方法：
     - 根据实时网络性能动态选择 serving endpoints
     - 不再仅基于 IP 地址静态映射用户
     - 将流量管理逻辑从单个路由器移到分布式系统
     - 利用 WSC 计算基础设施
     - 利用 application signals
     - 基于终端用户体验优化单个流
   - 效果：
     - 比 router-centric protocols 更高可用性
     - 更高性能

10. BwE、B4 TE、Espresso 的关系：
   - BwE：
     - 控制应用/主机可以使用多少 WAN 带宽
   - B4 TE：
     - 决定 WAN 流量走哪些路径
   - Espresso：
     - 决定用户流量从哪个 peering edge / serving endpoint 服务

11. 核心逻辑：
   WAN 路径昂贵且动态变化
     → 集中 TE 全局优化路径
     → 多路径拆分提高利用率
     → 传统路由作为 fallback
     → 主机侧 Protective ReRoute 快速处理故障
     → Espresso 将 SDN 扩展到 peering edge
     → 根据实时性能和用户体验优化边缘流量
```

---

### 十三、一句话总结这两小节

> 7.3.3 和 7.3.4 说明：在 WAN 中，SDN 不仅要集中优化路径，还要实时分配和执行带宽；BwE 控制应用能发多少，B4 TE 决定流量怎么走，Protective ReRoute 提供主机侧快速故障恢复，Espresso 则把 SDN 扩展到全球 peering edge，根据实时性能和用户体验优化边缘流量。


**专栏导航**

- ← 上一篇：[7.3.1 Jupiter topology and traffic engineering 和 7.3.2 Network aware scheduling](/posts/7-3-1-jupiter-topology-and-traffic-engineering-7-3-2-network-aware-scheduling/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.3.5 DDoS attack mitigation 和 7.3.6 What’s next for SDN →](/posts/7-3-5-ddos-attack-mitigation-7-3-6-what-s-next-for-sdn/)
