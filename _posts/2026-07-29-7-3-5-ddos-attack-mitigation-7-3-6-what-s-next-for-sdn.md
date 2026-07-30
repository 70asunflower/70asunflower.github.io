---
title: "7.3.5 DDoS attack mitigation 和 7.3.6 What’s next for SDN"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-29
description: "《The Data Center as a Computer》AI 导读专栏正文：7.3.5 DDoS attack mitigation 和 7.3.6 What’s next for SDN。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.3.5 DDoS attack mitigation 和 7.3.6 What’s next for SDN。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.3.5 DDoS attack mitigation 和 7.3.6 What’s next for SDN

下面把 **7.3.5 DDoS attack mitigation** 和 **7.3.6 What’s next for SDN** 放在一起深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这两小节一个讲：

> SDN 如何用于安全与隔离，尤其是 DDoS 攻击缓解和 noisy neighbor 控制；

另一个讲：

> SDN 的未来方向，尤其是 AI/ML 超算网络和去中心化 SDN。

---

### 7.3.5 DDoS attack mitigation 深入理解

这一节的核心是：

> 在大规模云和 WSC 网络中，既要防外部 DDoS 攻击，也要防内部 noisy neighbor。  
> 两者本质上都是：某些流量破坏了其他用户或服务的网络体验，需要检测、隔离和限速。

---

#### 一、什么是 DDoS 攻击？

原文说：

> Distributed denial of service, DDoS, attacks attempt to disable a service by overwhelming it with synthetic network traffic.

DDoS，分布式拒绝服务攻击，目标是：

> 用大量合成流量让服务不可用。

关键词：

- distributed：来自很多源；
- denial of service：让正常用户无法使用服务；
- synthetic traffic：人为制造的流量，不是正常用户流量。

---

#### 二、两类 DDoS 攻击

原文把 DDoS 分成两类：

1. network layer attack，网络层攻击；
2. application layer attack，应用层攻击。

---

##### 1. 网络层攻击

原文说：

> at the network layer, by exhausting the capacity of the site’s internet links.

网络层攻击的目标是：

> 耗尽站点互联网链路容量。

例如：

- UDP flood；
- ICMP flood；
- DNS amplification；
- NTP amplification；
- SYN flood；
- 大量垃圾包。

这类攻击通常表现为：

```text
流量非常大
    ↓
入口链路带宽被打满
    ↓
正常流量进不来
```

它不一定需要复杂请求，只要流量足够大，就能造成拥塞。

---

##### 2. 应用层攻击

原文说：

> at the application layer, with requests designed to overload the application’s front or back end capacity.

应用层攻击的目标不是链路带宽，而是：

> 应用前端或后端处理能力。

例如：

- HTTP flood；
- 高频搜索请求；
- 高频登录请求；
- 昂贵 API 查询；
- 慢速连接攻击；
- 爬虫式资源抓取；
- 触发复杂数据库查询的请求。

这类攻击可能流量不大，但每个请求很昂贵。

例如：

```text
正常请求：
轻量查询，1 ms 处理完成

攻击请求：
触发复杂 join、全表扫描、加密计算，100 ms 处理完成
```

即使带宽没满，CPU、数据库、缓存、后端服务也可能被打垮。

---

### 三、Cloud Armor 的作用

原文说：

> Cloud Armor globally monitors and detects DDoS attacks.

Cloud Armor 是 Google 的 DDoS 防护系统。  
它的作用包括：

- 全球监控；
- 检测攻击；
- 手动或自动下发 ACL；
- 阻断特定流量模式；
- 缓解攻击。

---

#### 1. ACL 是什么？

ACL，Access Control List，访问控制列表。

它可以定义：

```text
如果数据包匹配某些条件：
    允许 / 拒绝 / 限速
```

匹配条件可能包括：

- 源 IP；
- 目的 IP；
- 源端口；
- 目的端口；
- 协议；
- 地理区域；
- 包大小；
- 流量速率；
- 特定 header 模式。

---

#### 2. 手动推送 ACL

原文说：

> It allows network operators to manually push network Access Control Lists when necessary to block specific traffic patterns.

也就是说，网络运营者可以在必要时手动下发 ACL。

适用场景：

- 已确认攻击模式；
- 需要人工判断；
- 自动策略可能误伤正常流量；
- 特殊攻击需要定制规则。

---

#### 3. 自动生成 ACL

原文说：

> can automatically generate ACLs to thwart incoming attacks.

也就是说，Cloud Armor 可以自动生成 ACL 来阻止攻击。

这很重要，因为大规模 DDoS 攻击速度很快，人工响应可能太慢。

自动 ACL 可以：

- 快速识别异常流量模式；
- 自动下发过滤规则；
- 在边缘阻断攻击；
- 减少人工干预；
- 缩短缓解时间。

---

### 四、攻击还是真实流量尖峰？

原文提出一个很重要的问题：

> Some “attacks” are just genuine traffic spikes that cause a temporary bottleneck.

也就是说：

> 有些看起来像攻击的流量，其实只是真实流量尖峰。

例如：

- 热门新闻事件；
- 产品发布；
- 促销活动；
- 视频热点；
- 突发公共事件；
- 应用病毒式传播。

这些流量可能突然暴涨，看起来像 DDoS，但其实是正常用户流量。

---

#### 1. 为什么区分很重要？

如果把真实流量尖峰误判为攻击：

- 正常用户被阻断；
- 服务可用性下降；
- 收入受损；
- 用户体验变差；
- 自动 ACL 可能误伤合法用户。

如果只把它当流量尖峰，而实际上是攻击：

- 服务可能被打垮；
- 后端资源耗尽；
- 链路拥塞；
- 其他租户受影响。

因此 DDoS 缓解系统必须结合：

- 全局 telemetry；
- 历史流量模式；
- 应用信号；
- 来源分布；
- 请求特征；
- 拥塞信号。

---

### 五、虚拟化网络中的隔离问题

原文说：

> A core objective of virtualized networks is to provide consistent availability and performance, preventing one Virtual Machine, VM, from negatively impacting another’s network experience.

在云环境中，很多 VM 共享底层网络。

虚拟化网络的核心目标之一是：

> 隔离。

也就是：

```text
VM A 的流量不应该破坏 VM B 的网络体验。
```

---

#### 1. noisy neighbor 问题

原文说：

> “noisy neighbors” where one VM causes congestion that affects another VM’s performance, poses a similar challenge.

noisy neighbor，吵闹邻居，指：

> 一个 VM 占用过多共享资源，影响其他 VM。

在网络中，noisy neighbor 可能表现为：

- 某 VM 突然发送大量数据；
- 某 VM 下载大文件；
- 某 VM 运行批量 shuffle；
- 某 VM 触发大量跨 zone 流量；
- 某 VM 被攻陷后发送垃圾流量。

这些流量可能导致：

- 共享链路拥塞；
- 其他 VM 延迟升高；
- 丢包增加；
- 吞吐下降；
- SLO 被破坏。

---

#### 2. 为什么 LAN link 不超额订阅，上游链路仍会拥塞？

原文说：

> While the host’s LAN link may not be oversubscribed, upstream links, inside a building, or across zones, or out of a region, will be.

这里涉及数据中心网络常见的 oversubscription。

---

##### 主机 LAN link 可能不超额订阅

例如一台服务器有：

```text
100 Gbps NIC
```

接入交换机可能给它足够带宽。

所以在主机接入层，可能不会立刻拥塞。

---

##### 但上游链路通常超额订阅

往上走：

```text
服务器 → ToR → aggregation → building → zone → region → WAN
```

越往上，链路越共享。

例如：

- 建筑内链路；
- 跨 zone 链路；
- 出 region 链路；
- WAN 链路。

这些链路通常不可能做到所有服务器同时全线速通信。

因此当某个用户突然发送或接收大量流量时，可能影响其他用户。

原文说：

> a user suddenly sending or receiving lots of traffic may affect other users and thus needs to be contained.

也就是说：

> 需要遏制这种突发流量。

---

### 六、DDoS 缓解的两种极端方案及其问题

原文比较了集中式和纯主机式方案。

---

#### 1. 集中式系统的问题

原文说：

> Centralized systems often have delayed response times and limited information to restore isolation.

集中式系统有全局视图，但可能：

- 响应慢；
- 信息延迟；
- 控制环路长；
- 对瞬时拥塞反应不够快；
- 在攻击爆发初期无法及时隔离。

例如：

```text
主机检测到拥塞
    ↓
上报中央系统
    ↓
中央系统分析
    ↓
下发策略
    ↓
主机执行
```

这个环路可能太长。

---

#### 2. 纯主机系统的问题

原文说：

> a purely host-based system can lead to excessive communication overhead from distributing state.

如果完全由主机之间互相协调，也会有问题：

- 每台主机都要维护全局状态；
- 主机之间通信开销大；
- 状态同步复杂；
- 容易出现不一致；
- 难以做全局公平；
- 难以识别跨主机攻击模式。

---

### 七、混合方案：主机快速检测 + 中央 DoS Server

原文给出解决方案：

> a hybrid solution combines fast, reactive receiver-driven DoS detection at the host level with a centralized DoS Server.

也就是说：

> 混合方案结合主机层快速、反应式、接收端驱动的 DoS 检测，以及集中式 DoS Server。

---

#### 1. 主机层：快速、反应式、receiver-driven detection

receiver-driven 指：

> 由接收端主机检测异常。

因为受害主机最先知道：

- 收到了多少流量；
- 哪些流异常；
- 是否出现拥塞；
- 是否影响应用；
- 是否丢包；
- 是否 RTT 升高。

主机层可以快速反应：

```text
检测到异常
    ↓
立即限速 / 丢弃 / 标记
    ↓
先保护自身
```

这比等待中央系统更快。

---

#### 2. 中央 DoS Server：全局分析和执行速率计算

原文说：

> The server receives congestion signals from hosts and utilizes additional telemetry data to accurately calculate and distribute enforcement rates.

中央 DoS Server 收到主机拥塞信号后，还会结合：

- 交换机 telemetry；
- 链路利用率；
- 全局流量模式；
- 历史基线；
- 攻击特征；
- 应用优先级；
- 租户策略。

然后计算：

> enforcement rates，执行速率。

也就是告诉主机或网络设备：

```text
某 VM 最多发送多少速率
某流量类最多允许多少带宽
某源 IP 应该被限速到多少
```

---

#### 3. 混合方案的优势

混合方案结合两者优点：

|组件|优势|
| ------------| ------------------------------|
|主机检测|快，接近受害端，低延迟|
|中央服务器|全局视图，准确判断，公平策略|

它可以：

- 快速缓解攻击；
- 减少误判；
- 控制 noisy neighbor；
- 保持租户隔离；
- 对大类网络中断快速响应。

---

### 八、7.3.5 的核心逻辑

```text
DDoS 攻击和 noisy neighbor 都会破坏网络隔离
  ↓
攻击可能发生在网络层或应用层
  ↓
Cloud Armor 全球监控并检测攻击
  ↓
手动或自动 ACL 阻断异常流量
  ↓
真实流量尖峰也可能造成类似拥塞
  ↓
虚拟化网络必须隔离 VM 之间的影响
  ↓
上游链路通常超额订阅，需要遏制突发流量
  ↓
集中式响应慢，纯主机式开销大
  ↓
混合方案：主机快速检测 + 中央 DoS Server 全局计算执行速率
```

---

### 7.3.6 What’s next for SDN 深入理解

这一节讲 SDN 的未来，主要两个方向：

1. AI/ML 超算网络；
2. 去中心化 SDN，dSDN。

---

### 九、SDN 与 AI/ML 工作负载

原文说：

> The groundwork laid by SDN helps address the unique challenges posed by emerging AI/ML workloads.

也就是说：

> SDN 打下的基础，有助于应对新兴 AI/ML 工作负载带来的独特挑战。

---

#### 1. ML 训练任务与传统分布式应用不同

原文说：

> Unlike loosely coupled distributed applications, ML training jobs demand simultaneously healthy compute and networking supercomputer resources.

传统分布式应用可能是 loosely coupled，松散耦合。

例如 Web 服务：

- 某个节点慢一点，可以重试；
- 某个副本不可用，可以切流；
- 某些请求延迟高，对整体影响有限。

但 ML 训练任务通常是 tightly coupled，紧耦合。

例如大规模训练：

- 很多加速器同时参与；
- 每一步都要同步梯度；
- all-reduce 通信需要高带宽和低延迟；
- 一个节点慢，整个训练步变慢；
- 一个链路故障，整个任务可能停滞。

因此 ML 训练需要：

```text
计算资源健康
    +
网络资源健康
    +
加速器互联健康
```

三者必须同时满足。

---

#### 2. ML 训练需要前所未有的加速器和网络资源

原文说：

> These jobs also necessitate unprecedented amounts of accelerators and networking.

大模型训练需要：

- 大量 GPU/TPU；
- 高带宽互联；
- 低延迟集合通信；
- 大规模存储；
- 高速数据加载；
- 跨节点参数同步。

这使网络不再只是“连接服务器”，而是：

> 超算资源的一部分。

---

#### 3. 故障间隔时间变短

原文说：

> leading to significantly shorter mean time between failures.

mean time between failures，MTBF，平均故障间隔时间。

当系统中有：

- 成千上万加速器；
- 大量光模块；
- 大量链路；
- 大量交换机；
- 复杂互联；

故障概率会显著增加。

即使单个组件可靠性很高，规模一大，整体故障频率也会变高。

例如：

```text
100 个组件：
故障少见

100,000 个组件：
故障常见
```

因此 ML 超算网络必须：

- 快速检测故障；
- 快速绕开故障；
- 动态重配置；
- 保持任务可用；
- 减少训练中断。

---

#### 4. 共享集群需要动态重配置和再平衡

原文说：

> In shared clusters, the competition for supercomputer resources requires dynamic reconfiguration and rebalancing of resources.

在共享集群中，多个任务竞争：

- 加速器；
- 网络带宽；
- 存储；
- 内存；
- 互联拓扑。

因此系统需要动态：

- 分配资源；
- 重新配置网络；
- 平衡负载；
- 隔离干扰；
- 迁移任务；
- 恢复故障。

这正是 SDN 擅长的事情。

---

### 十、TPU v4、ICI 和 optical circuit switching

原文说：

> Starting with TPU v4, SDN has been instrumental in managing high bandwidth inter-chip interconnect, ICI, using optical circuit switching to dynamically reroute traffic around failures and increase job availability.

这里涉及几个关键概念。

---

#### 1. ICI，Inter-Chip Interconnect

ICI 是：

> 芯片间互联。

在 TPU pod 中，很多 TPU 芯片需要高速通信。

例如：

- 梯度同步；
- tensor 并行；
- pipeline 并行；
- all-reduce；
- all-gather；
- reduce-scatter。

这些通信对带宽和延迟非常敏感。

因此 ICI 是 ML 超算网络的核心部分。

---

#### 2. optical circuit switching，光电路交换

optical circuit switching，OCS，指：

> 使用光学交换结构建立芯片间或设备间的光路连接。

与传统 packet switching 相比，OCS 可以：

- 提供高带宽；
- 降低某些网络层级成本；
- 支持拓扑动态重配置；
- 绕开故障链路；
- 适配 ML 任务通信模式。

但它也有特点：

- 重配置不是无限快；
- 需要集中调度；
- 需要知道任务通信需求；
- 需要故障检测和路径切换。

因此需要 SDN。

---

#### 3. SDN 在 TPU v4 中的作用

原文说：

> SDN has been instrumental in managing high bandwidth ICI.

也就是说：

> SDN 被用来管理高带宽芯片间互联。

它可以帮助：

- 动态配置光路；
- 绕开故障；
- 重新连接拓扑；
- 提高任务可用性；
- 支持大规模 ML 训练；
- 让网络拓扑适配训练任务。

这说明 SDN 已经从：

```text
数据中心以太网
    ↓
WAN
    ↓
加速器互联网络
```

不断扩展。

---

### 十一、SDN 的未来：AI/ML 的 compute-networking substrate

原文说：

> SDN’s continued evolution is essential to deliver a highly available, scalable compute-networking substrate to support the ever-growing demands of AI/ML workloads.

也就是说：

> SDN 必须继续演进，以提供高可用、可扩展的计算-网络基底，支持 AI/ML 工作负载不断增长的需求。

这里的关键词是：

> compute-networking substrate，计算-网络基底。

这意味着：

> 网络和计算不再分开设计，而是一个统一的超算基础设施。

未来 SDN 可能要管理：

- GPU/TPU 互联；
- 光交换；
- 高带宽集合通信；
- 故障快速恢复；
- 任务拓扑感知调度；
- 网络-计算联合优化；
- 训练任务可用性；
- 能耗优化；
- 跨集群资源编排。

---

### 十二、去中心化 SDN，dSDN

原文后半部分介绍另一种方向：

> decentralized SDN, dSDN.

这是对标准集中式 SDN 的一种替代。

---

#### 1. 标准集中式 SDN 的问题

前面章节强调集中式 SDN 的优点：

- 全局视图；
- 更容易优化；
- 更容易管理；
- 更容易做 TE；
- 更容易一致性更新。

但集中式 SDN 也有问题：

- 控制器可能成为依赖；
- 控制器故障可能影响整个网络；
- 控制器与数据平面故障范围不一致；
- 需要外部组件；
- 可能依赖传统协议做 fallback。

---

#### 2. dSDN 的基本思想

原文说：

> In this decentralized SDN, dSDN, every router runs an operator-defined dSDN controller.

也就是说：

> 在 dSDN 中，每个路由器都运行一个运营商定义的 dSDN controller。

不是把控制平面放到外部服务器集群，而是：

```text
每个路由器内部都有自己的 dSDN controller
```

---

#### 3. 每个 dSDN controller 如何获得全局视图？

原文说：

> Each dSDN controller constructs a global network view via a simple flooding-based dissemination protocol.

也就是说：

> 每个 dSDN controller 通过简单的 flooding 分发协议构建全局网络视图。

flooding 指：

> 把状态信息传播给所有路由器。

这类似传统 link-state routing 的思想：

```text
每个路由器广播自己的链路状态
    ↓
所有路由器收到全网状态
    ↓
每个路由器构建全局拓扑图
```

但这里传播的是 SDN 需要的网络状态。

---

#### 4. 本地运行 TE 算法

原文说：

> then locally runs a traffic engineering algorithm to compute capacity-aware paths.

也就是说：

> 每个路由器本地运行流量工程算法，计算考虑容量的路径。

这和集中式 TE 不同。

集中式 TE：

```text
中央 TE server 计算所有路径
    ↓
下发给设备
```

dSDN：

```text
每个路由器都有全局视图
    ↓
每个路由器本地计算路径
```

---

#### 5. source routing：源路由

原文说：

> For simple consensus-free path selection dSDN uses source routing.

source routing 指：

> 路径由源路由器决定，并写在数据包头部。

中间路由器不需要自己决定路径，只需要按照包头中的路径转发。

例如：

```text
源路由器 R1 决定：
R1 → R3 → R7 → R9

数据包携带这个路径
    ↓
中间路由器按路径转发
```

---

##### 为什么 source routing 可以 consensus-free？

原文说：

> a router is the sole decision maker for paths that originate at that router.

也就是说：

> 对于从某路由器出发的流量，该路由器是唯一路径决策者。

不需要其他路由器同意。

这避免了复杂共识或中央协调。

---

#### 6. dSDN 消除外部依赖和传统协议依赖

原文说：

> The dSDN architecture eliminates any dependency on components external to the data plane and on legacy protocols.

也就是说：

> dSDN 不依赖数据平面外部组件，也不依赖传统协议。

集中式 SDN 通常依赖：

- 外部 controller；
- controller 集群；
- controller 与交换机之间通道；
- 有时还要传统路由协议做 fallback。

dSDN 则把控制逻辑放回路由器内部。

---

### 十三、dSDN 的弹性：fate-sharing

原文说：

> dSDN retains the benefits of traditional centralized SDN while restoring the fate-sharing of traditional protocols that provides resiliency.

这里的关键概念是：

> fate-sharing，命运共享。

---

#### 1. 什么是 fate-sharing？

fate-sharing 指：

> 控制平面故障范围与数据平面故障范围一致。

传统分布式路由协议中：

```text
一台路由器故障
    ↓
只影响这台路由器相关的控制状态和数据转发
```

控制平面损害和数据平面损害是匹配的。

---

#### 2. 集中式 SDN 的 fate-sharing 问题

集中式 SDN 中：

```text
中央控制器故障
    ↓
可能影响整个网络
```

但此时数据平面交换机可能都正常。

也就是说：

> 控制平面故障范围可能远大于数据平面故障范围。

这会带来风险。

---

#### 3. dSDN 恢复 fate-sharing

dSDN 中：

```text
一台路由器故障
    ↓
只损失这台路由器的控制逻辑和转发能力
```

不会影响其他路由器的控制逻辑。

原文说：

> When a router goes down, the damage to the control plane is aligned with the damage to the data plane, unlike with centralized SDN.

这就是 dSDN 的弹性优势。

---

### 十四、dSDN 的代价

原文也指出 dSDN 有成本。

---

#### 1. 路由器 CPU 负担更高

原文说：

> dSDN imposes a higher computational load on the router CPU, to run TE.

因为每个路由器都要：

- 维护全局视图；
- 运行 TE 算法；
- 计算路径；
- 处理状态更新。

这比简单转发设备更复杂。

---

#### 2. 包头需要携带 source route

原文说：

> additional packet header state, to carry source-routes.

source routing 需要在包头中携带路径信息。

这会增加：

- 包头大小；
- 解析复杂度；
- 某些情况下的带宽开销。

---

#### 3. 但现代路由器可以承受

原文说：

> both are easily accommodated by modern routers.

也就是说：

> 现代路由器能够承受这些额外计算和包头开销。

因此 dSDN 是可行方案。

---

### 十五、集中式 SDN 与 dSDN 的对比

|维度|集中式 SDN|dSDN|
| --------------| ------------------------| ----------------------------------|
|控制平面位置|外部控制器集群|每个路由器内部|
|全局视图|控制器拥有|每个路由器通过 flooding 拥有|
|路径计算|中央计算|本地计算|
|路径选择|控制器下发|源路由器决定|
|转发方式|控制器安装规则|source routing|
|外部依赖|依赖控制器|不依赖外部组件|
|传统协议依赖|可能需要 fallback|可减少对传统协议依赖|
|故障范围|控制器故障可能影响全网|路由器故障只影响该路由器|
|fate-sharing|较弱|较强|
|路由器复杂度|较低|较高|
|包头开销|较低|source route 增加包头|
|全局优化|容易|可实现，但依赖本地算法和状态同步|

---

### 十六、7.3.6 的核心逻辑

```text
AI/ML 工作负载紧耦合
  ↓
需要计算和网络同时健康
  ↓
加速器和网络规模巨大
  ↓
故障更频繁，MTBF 更短
  ↓
需要动态重配置和资源再平衡
  ↓
SDN 管理 TPU v4 ICI 和光交换
  ↓
提高 ML 任务可用性
  ↓
同时，dSDN 提供去中心化替代
  ↓
每个路由器运行 dSDN controller
  ↓
flooding 构建全局视图
  ↓
本地 TE + source routing
  ↓
保留 SDN 优点，同时恢复 fate-sharing
```

---

### 十七、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.3.5 DDoS attack mitigation

1. DDoS 攻击目标：
   - 用合成流量使服务不可用
   - distributed：来自多个源
   - denial of service：破坏正常服务可用性

2. 两类 DDoS 攻击：
   a. 网络层攻击：
      - 耗尽站点互联网链路容量
      - 例如 volumetric attacks
      - 目标是带宽和链路资源
   b. 应用层攻击：
      - 用请求压垮应用前端或后端
      - 目标是 CPU、数据库、应用逻辑、后端容量
      - 流量不一定很大，但请求可能很昂贵

3. Cloud Armor：
   - 全球监控和检测 DDoS 攻击
   - 允许运营者手动推送 ACLs
   - 也可以自动生成 ACLs 阻断攻击
   - ACL 用于匹配和阻断特定流量模式

4. 攻击 vs 真实流量尖峰：
   - 有些“攻击”其实是真实流量尖峰
   - 例如热点事件、促销、突发新闻
   - 需要区分攻击和合法流量暴涨
   - 否则可能误伤正常用户

5. 虚拟化网络中的隔离目标：
   - 提供一致可用性和性能
   - 防止一个 VM 影响另一个 VM 的网络体验
   - 核心挑战：
     - noisy neighbors

6. noisy neighbor 问题：
   - 一个 VM 发送/接收大量流量
   - 导致共享网络拥塞
   - 影响其他 VM 性能
   - 虽然主机 LAN link 可能未超额订阅
   - 但上游链路可能超额订阅：
     - building 内
     - cross-zone
     - out-of-region
   - 因此突发流量需要被遏制

7. 集中式 vs 纯主机式缓解：
   - 集中式系统：
     - 有全局视图
     - 但响应可能延迟
     - 信息可能不足
   - 纯主机式系统：
     - 响应快
     - 但分发状态会带来通信开销
     - 难以全局一致

8. 混合方案：
   - 主机层：
     - fast
     - reactive
     - receiver-driven DoS detection
   - 中央 DoS Server：
     - 接收主机拥塞信号
     - 利用额外 telemetry
     - 准确计算 enforcement rates
     - 分发执行速率
   - 目标：
     - 快速缓解
     - 保持隔离
     - 处理大类网络中断

9. 核心逻辑：
   DDoS / noisy neighbor 破坏隔离
     → Cloud Armor 检测和下发 ACL
     → 区分攻击和真实流量尖峰
     → 主机快速检测保护受害端
     → 中央服务器全局计算限速策略
     → 混合方案兼顾速度和准确性
```

```text
7.3.6 What’s next for SDN

1. SDN 与 AI/ML workloads：
   - SDN 的基础帮助应对 AI/ML 工作负载挑战
   - ML training jobs 不同于松散耦合分布式应用
   - ML 训练需要：
     - 健康的计算资源
     - 健康的网络资源
     - 健康的加速器互联
   - 这些资源必须同时可用

2. AI/ML 对网络的压力：
   - 需要前所未有的 accelerators 和 networking
   - 大规模训练需要高带宽、低延迟通信
   - 组件数量巨大
   - mean time between failures 显著变短
   - 故障更常见
   - 需要快速绕开故障和动态重配置

3. 共享集群中的资源竞争：
   - 多任务竞争超算资源
   - 需要动态 reconfiguration
   - 需要动态 rebalancing
   - 需要网络与计算联合调度

4. TPU v4 和 ICI：
   - 从 TPU v4 开始
   - SDN 管理高带宽 inter-chip interconnect, ICI
   - 使用 optical circuit switching
   - 动态绕开故障重路由流量
   - 提高 job availability

5. SDN 的未来角色：
   - 不只是数据中心网络或 WAN 控制
   - 而是 AI/ML 超算的 compute-networking substrate
   - 目标：
     - 高可用
     - 可扩展
     - 支持不断增长的 AI/ML 需求

6. decentralized SDN, dSDN：
   - 近期工作提出集中式 SDN 的替代方案
   - 每个路由器运行 operator-defined dSDN controller
   - 每个 controller 通过 flooding-based dissemination protocol 构建全局网络视图
   - 每个路由器本地运行 traffic engineering algorithm
   - 计算 capacity-aware paths

7. dSDN 的路径选择：
   - 使用 source routing
   - 源路由器是唯一决策者
   - 决定源自该路由器的路径
   - 不需要集中共识
   - 中间路由器按包头中的路径转发

8. dSDN 的优点：
   - 消除对数据平面外部组件的依赖
   - 减少对 legacy protocols 的依赖
   - 保留集中式 SDN 的许多优点
   - 恢复传统协议的 fate-sharing
   - 路由器故障时：
     - 控制平面损害与数据平面损害一致
     - 不像集中式 SDN 那样可能因控制器故障影响全网

9. dSDN 的代价：
   - 路由器 CPU 需要运行 TE
   - 计算负载更高
   - 包头需要携带 source-route
   - 增加 packet header state
   - 但现代路由器可以承受

10. 集中式 SDN vs dSDN：
   - 集中式 SDN：
     - 外部控制器
     - 全局优化强
     - 控制器故障可能影响全网
   - dSDN：
     - 每路由器控制逻辑
     - 本地 TE + source routing
     - 更强 fate-sharing
     - 更高路由器复杂度和包头开销

11. 核心逻辑：
   AI/ML 训练紧耦合
     → 需要计算和网络同时健康
     → 故障更频繁
     → SDN 管理加速器互联和光交换
     → 提高任务可用性
     → dSDN 提供去中心化 SDN 替代
     → 保留 SDN 优点并增强弹性
```

---

### 十八、一句话总结这两小节

> 7.3.5 说明 SDN 不仅用于性能优化，也用于安全与隔离：Cloud Armor 和混合式 DoS 缓解系统共同应对外部 DDoS 攻击与内部 noisy neighbor；7.3.6 则说明 SDN 正在扩展到 AI/ML 超算网络和加速器互联，并出现 dSDN 这样的去中心化架构，在保留 SDN 全局优化优势的同时增强故障弹性。


**专栏导航**

- ← 上一篇：[7.3.3 Bandwidth enforcer 和 7.3.4 B4 traffic engineering](/posts/7-3-3-bandwidth-enforcer-7-3-4-b4-traffic-engineering/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.4 Software-defined storage 和 7.4.1 Storage workload diversity →](/posts/7-4-software-defined-storage-7-4-1-storage-workload-diversity/)
