---
title: "6.4.4 Spine-less networking"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：6.4.4 Spine-less networking。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.4.4 Spine-less networking。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.4.4 Spine-less networking

下面这一节 **6.4.4 Spine-less networking** 非常精彩。它讲的是数据中心网络架构中一个很重要的演进方向：

> **用光电路交换 OCS 替代传统电子 spine 层，使数据中心网络从“固定布线的 Clos”变成“可动态重配置的光网络”。**

这一节的核心可以概括为：

> **传统 Clos 网络的 spine 层必须速度统一、布线固定，升级和扩容成本很高；OCS 通过纯光交换实现协议、波长和速率无关的端口连接，使数据中心可以增量升级、混合速率、动态调整拓扑，并首次让 topology engineering 成为常规操作。**

---

### 1. 这一节要解决的核心问题

原文开头说：

> WSCs are not only deployed at large scale, e.g., 40 MW or more of infrastructure, but the compute, storage and accelerator devices deployed are always evolving, which requires regularly refreshing the native network interconnect speeds from 40 Gbps common just a few years ago to the 400 Gbps of today.

这里提出了一个现实矛盾：

```text
WSC 规模巨大
+
设备代际不断演进
+
网络速率不断升级
+
不能停止已有服务
```

也就是说，数据中心网络必须能够：

- 从 40G 升级到 100G；
- 从 100G 升级到 200G；
- 从 200G 升级到 400G；
- 甚至未来 800G；
- 同时保持已有服务器、存储、加速器继续运行；
- 不能因为网络升级导致整个集群下线。

40 MW 级别的数据中心意味着巨大的已部署基础设施。

如果每次网络升级都要：

- 关闭服务；
- 拔插大量光纤；
- 更换整个 spine；
- 重新布线；
- 重新测试；
- 重新调度 workload；

那么成本会非常高。

---

### 2. 传统 Clos 网络的问题：spine 层太“刚性”

原文说：

> Unfortunately, Clos topologies in data centers need a uniform high-speed spine layer. Thus, the entire spine must be upgraded to accommodate faster port speed in any part of the cluster, which is too costly to be practical.

传统 Clos 网络通常有：

```text
ToR / leaf
   ↓
aggregation
   ↓
spine
```

spine 层的一个关键特点是：

> 它通常需要统一的高速端口。

例如，如果 spine 是 100G 网络，那么很多上行链路都必须按 100G 设计。

如果你想引入 400G 设备，就会遇到问题：

```text
新设备是 400G
但 spine 还是 100G
```

为了支持 400G，你可能需要：

- 更换 spine 交换芯片；
- 更换 spine 机箱；
- 更换大量光模块；
- 重新布线；
- 升级 aggregation；
- 升级路由和 ECMP；
- 升级监控系统；
- 升级故障处理流程。

这会导致：

> 局部升级变成全网升级。

原文说：

> This inflexibility makes it difficult to incrementally add faster devices to the network without disrupting the entire infrastructure.

也就是说，传统 Clos 的 spine 层缺乏增量演进能力。

---

### 3. 什么是 spine-less networking？

6.4.4 的标题是：

> Spine-less networking

这里的 “spine-less” 不是说数据中心没有骨干网络，而是说：

> 用 OCS 光交换层替代传统电子 packet-switching spine 层。

传统结构：

```text
aggregation block A
        ↓
electronic spine switches
        ↓
aggregation block B
```

spine-less 结构：

```text
aggregation block A
        ↓
Optical Circuit Switch OCS
        ↓
aggregation block B
```

OCS 不解析包，不做电子转发，而是：

```text
直接建立光路
```

也就是：

```text
fiber port A ↔ OCS mirrors ↔ fiber port B
```

---

### 4. OCS 的工作原理：MEMS 镜子转向光束

原文说：

> An optical circuit switch uses two sets of microelectromechanical systems MEMS mirrors to dynamically connect input and output fiber ports, creating flexible port-to-port connections.

OCS 的核心器件是：

```text
MEMS mirrors
```

即微机电系统镜子。

---

#### 4.1 MEMS mirror array

原文：

> A MEMS mirror array is a collection of tiny, individually controllable mirrors fabricated using microelectromechanically controlled mirrors. The individual millimeter-sized mirrors can be tilted along two axes to precisely control the direction of light beams.

MEMS mirror array 是很多非常小的镜子，每个镜子都可以单独控制。

这些镜子通常：

- 毫米级大小；
- 可沿两个轴倾斜；
- 可以精确改变光束方向；
- 用来把输入光纤的光导向指定输出光纤。

可以把它想象成一个：

```text
光路 crossbar switch
```

但不是电信号 crossbar，而是光束 crossbar。

---

#### 4.2 输入光纤和输出光纤必须精确准直

原文：

> All incoming and outgoing fibers are very precisely aligned collimated so that the laser beam in each fiber hits its first mirror.

这里关键词是：

> collimated，准直。

光纤出来的激光需要通过透镜变成平行光束。

这样光束才能：

- 稳定传播；
- 被镜子精确转向；
- 准确进入目标输出光纤；
- 降低插入损耗；
- 降低串扰。

---

#### 4.3 如何连接到输出端口 (x, y)？

原文：

> To reach output port x, y the first mirror steers the beam to output mirror column x, and that mirror is oriented to send the light to the fiber in row y.

OCS 使用两组镜子。

可以理解为：

```text
第一组镜子：选择输出 column x
第二组镜子：选择输出 row y
```

最终确定输出端口：

```text
(x, y)
```

这就像一个二维光交换矩阵。

例如：

```text
input fiber i
   ↓
first mirror
   ↓
second mirror
   ↓
output fiber j
```

通过控制每对镜子的角度，可以建立任意输入到输出的光路。

---

#### 4.4 为什么准直必须极其精确？

原文：

> To keep optical losses low, collimation needs to be incredibly precise because the outgoing laser beam needs to hit the output fiber head-on.

如果光束没有正面进入输出光纤，就会出现：

- 插入损耗；
- 信号衰减；
- 反射；
- 串扰；
- 误码率上升；
- 链路不稳定。

所以 OCS 的机械设计、光学设计和控制精度要求非常高。

---

### 5. OCS 的最大优势：协议、波长、速率无关

原文说：

> Because the OCS merely steers light, it is oblivious to the network protocol, wavelengths, and speeds being used, and thus doesn’t need to be upgraded when newer optics are introduced, and simultaneously handles ports with multiple speeds.

这是 OCS 最关键的优势。

OCS 只做一件事：

```text
把光从输入端口导向输出端口
```

它不关心：

- 这是 Ethernet 还是其他协议；
- 是 10G、40G、100G、200G 还是 400G；
- 是什么波长；
- 包里是什么内容；
- 是 IP、TCP、RDMA 还是存储协议；
- 是否加密；
- 属于哪个租户；
- 使用什么 FEC；
- 使用什么 modulation。

只要光信号在 OCS 支持的光学范围内，它就可以通过。

---

#### 5.1 这意味着什么？

这意味着 OCS 可以长期存在，而端侧设备可以不断升级。

例如：

```text
过去：40G optics
现在：400G optics
未来：800G optics
```

你只需要升级：

- NIC；
- 交换机端口；
- 光模块；
- aggregation block；
- 服务器；
- 加速器。

而不需要升级 OCS。

因为 OCS 只是光路交换，不解析速率和协议。

这极大提高了网络演进能力。

---

#### 5.2 可以同时混合多种速率

OCS 可以同时连接不同速率端口。

例如：

```text
aggregation block A：100G
aggregation block B：400G
aggregation block C：200G
```

只要光链路设计合理，OCS 可以在它们之间建立光路。

这对 WSC 非常重要，因为数据中心中总是多代设备共存。

---

### 6. OCS 如何替代 spine 层？

原文说：

> By using an Optical Circuit Switch OCS layer, the traditional spine layer can be removed from the data center network, enabling a direct optical connection between diverse aggregation blocks.

传统 Clos：

```text
aggregation block
       ↓
electronic spine
       ↓
aggregation block
```

OCS spine-less：

```text
aggregation block
       ↓
OCS
       ↓
aggregation block
```

OCS 直接在 aggregation blocks 之间建立光连接。

这带来几个好处：

1. 不需要统一速率的电子 spine；
2. 可以连接不同代际 aggregation blocks；
3. 可以动态改变连接关系；
4. 可以增量扩容；
5. 可以减少电子交换设备；
6. 可以降低功耗；
7. 可以降低升级成本。

---

### 7. 增量扩容：不用拔插大量光纤

原文说：

> To connect or remove a new aggregation block, the OCS simply needs to be reprogrammed to reorient its mirrors to establish the new links.

如果使用 OCS，添加新的 aggregation block 时，只需要：

```text
重新编程 OCS
调整镜子角度
建立新光路
```

而不需要人工拔插大量光纤。

---

#### 7.1 没有 OCS 时的扩容痛苦

原文：

> Without OCS, adding a new aggregation block requires unplugging and re-plugging hundreds or thousands of fiber ports to “re-stripe” the Clos mesh, a process that is tedious and error prone.

在传统 Clos 中，添加新 aggregation block 通常需要：

- 拔很多光纤；
- 插很多光纤；
- 重新 stripe；
- 重新连接 leaf/spine；
- 重新测试链路；
- 重新验证路由；
- 重新检查 ECMP；
- 重新排查错连；
- 可能需要停部分服务。

“re-stripe” 可以理解为：

> 重新排列 Clos mesh 中的链路连接，使新设备均匀接入网络。

这在大规模网络中非常痛苦：

- 光纤数量巨大；
- 容易插错；
- 容易污染光纤端面；
- 容易损坏光模块；
- 排障困难；
- 运维成本高。

OCS 把这些物理布线工作变成了：

```text
软件控制的光路重配置
```

---

### 8. 动态拓扑：根据应用需求调整网络

原文说：

> OCS layers also enable dynamic topologies that adapt to application-specific communication patterns like “elephant flows”.

这是 OCS 的另一个革命性优势。

传统数据中心网络的物理拓扑通常是固定的：

```text
布线一次
运行多年
```

而 OCS 让网络拓扑变成可编程的：

```text
网络拓扑可以根据 workload 动态调整
```

---

#### 8.1 elephant flows 是什么？

elephant flow 指：

> 大流量、长时间、高带宽的网络流。

例如：

- 大规模 ML 训练；
- 大模型参数同步；
- shuffle；
- 大规模数据复制；
- 备份；
- 存储迁移；
- 视频转码数据搬运；
- 数据库 bulk load。

与之相对的是 mice flows：

```text
小流量、短连接、大量并发
```

例如：

- 小 RPC；
- 网页请求；
- 控制消息；
- 心跳；
- 监控查询。

---

#### 8.2 OCS 如何服务 elephant flows？

原文举例：

> if a large computation like an ML training run spans two aggregation blocks and needs more bandwidth, the OCS spine can be reconfigured to allocate additional ports to these two blocks.

假设一个 ML 训练任务跨越：

```text
aggregation block A
aggregation block B
```

它需要 A 和 B 之间更多带宽。

传统网络中，A 和 B 之间的带宽由固定布线决定。

而 OCS 可以：

```text
增加 A 和 B 之间的光路数量
```

也就是分配更多端口给这两个 block。

这样可以在需要时提供：

- 更高带宽；
- 更低拥塞；
- 更好训练吞吐；
- 更低尾延迟；
- 更少跨 fabric 竞争。

任务结束后，OCS 又可以恢复原来的拓扑。

---

### 9. topology engineering：数据中心网络拓扑工程

原文说：

> With OCS, reconfiguring network connectivity has become a standard practice, enabling topology engineering in the data center for the first time.

这句话非常重要。

过去数据中心网络设计是：

```text
静态物理拓扑
+
动态路由/ECMP
```

而 OCS 让物理拓扑本身也可以动态变化：

```text
动态物理拓扑
+
动态路由/流量工程
+
调度系统协同
```

这就是：

> topology engineering

也就是根据流量需求主动设计网络拓扑。

---

#### 9.1 为什么 topology engineering 很重要？

因为不同 workload 的通信模式不同。

例如：

##### Web serving

流量较分散，很多小流。

适合：

- 稳定 Clos；
- ECMP；
- 多路径；
- 拥塞控制。

---

##### 分布式存储

可能有大量复制、恢复、读写流。

需要：

- 高带宽；
- 低尾延迟；
- 局部性；
- QoS。

---

##### ML 训练

常有大规模 collective communication：

- all-reduce；
- all-gather；
- reduce-scatter；
- all-to-all；
- pipeline communication。

需要：

- 高 bisection bandwidth；
- 低延迟；
- 可预测带宽；
- 特定拓扑形状；
- 局部高带宽。

OCS 可以根据训练任务调整拓扑，使网络更匹配通信模式。

---

### 10. OCS 与电子 packet spine 的对比

可以把 OCS spine 和传统电子 spine 做对比。

|维度|电子 packet spine|OCS spine|
| --------------------| --------------------| ----------------------------|
|交换方式|电子包交换|光路交换|
|是否解析包|是|否|
|是否感知协议|是|否|
|是否感知速率|是|否|
|是否支持缓存|是|否|
|是否支持逐包多路径|是|通常否|
|是否支持 QoS 队列|是|依赖端侧|
|升级成本|高，需换芯片/端口|低，OCS 通常不用换|
|混合速率|受端口限制|更容易支持|
|扩容方式|重新布线|重编程光路|
|动态拓扑|困难|容易|
|功耗|高|相对低|
|适合流量|通用、小包、多路径|大流、稳定带宽、拓扑工程|
|挑战|成本、功耗、升级|调度、控制平面、重配置时间|

---

### 11. OCS 的本质：电路交换思想回到数据中心

OCS 很像传统电话网络中的电路交换。

它建立的是：

```text
专用光路
```

而不是：

```text
每个包独立转发
```

也就是说：

```text
packet switch：每个包动态找路径
OCS：提前建立一条光路径
```

这带来优点：

- 低电子开销；
- 高速率无关；
- 低功耗；
- 适合大流；
- 适合稳定带宽需求。

但也带来挑战：

- 不能逐包负载均衡；
- 不能缓存突发；
- 需要中央控制器提前规划；
- 需要准确流量需求矩阵；
- 需要避免拥塞；
- 需要路由协议配合。

---

### 12. OCS 需要强大的控制平面

虽然原文这里没有展开，但 OCS 动态拓扑必须依赖强控制平面。

控制平面需要知道：

- 哪些 aggregation blocks 之间需要带宽；
- 哪些任务正在运行；
- 哪些流量是 elephant flows；
- 当前链路利用率；
- 故障状态；
- 光路健康状态；
- 路由拓扑；
- 调度计划；
- 未来任务需求。

然后控制平面决定：

```text
如何调整 OCS 镜子
建立哪些光路
拆除哪些光路
何时重配置
如何避免路由环路
如何迁移流量
```

这与 6.2.3 讲的 control plane、model-driven management 高度一致。

---

### 13. OCS 与 TPU OCS 的关系

这一节和 6.3.2.1 TPU 中提到的 OCS 是同一类技术，但应用场景不同。

---

#### 13.1 TPU 中的 OCS

在 TPUv4 中，OCS 用于：

```text
连接 4x4x4 cubes
形成 TPU pod
```

作用包括：

- 故障时替换 cube；
- 保持逻辑拓扑；
- 支持增量部署；
- 定制 3D torus 形状；
- 匹配并行策略。

---

#### 13.2 数据中心网络中的 OCS

在 6.4.4 中，OCS 用于：

```text
连接 aggregation blocks
替代 spine 层
```

作用包括：

- 支持异构速率；
- 增量扩容；
- 避免 re-stripe；
- 动态拓扑；
- topology engineering；
- 服务 elephant flows。

---

#### 13.3 共同思想

两者共同点是：

```text
用光路可重构性
换取系统灵活性、可用性和演进能力
```

也就是说：

> OCS 不只是网络器件，而是系统架构工具。

---

### 14. OCS 的局限性

虽然 OCS 很强，但它不是万能的。

---

#### 14.1 重配置不是瞬时完成

MEMS 镜子调整需要时间。

虽然可能很快，但不是逐包交换。

所以 OCS 更适合：

- 较稳定的大流量；
- 计划性拓扑调整；
- 故障恢复；
- 任务级带宽分配。

不适合：

- 每个包随机改变路径；
- 极细粒度负载均衡；
- 瞬时微突发缓冲。

---

#### 14.2 没有包缓存

电子交换机可以缓存突发包。

OCS 只是光路，没有缓存。

因此必须通过：

- 容量规划；
- 拥塞控制；
- traffic shaping；
- 调度；
- QoS；

来避免拥塞。

---

#### 14.3 需要准确流量需求

OCS 动态拓扑需要知道：

```text
哪里需要带宽
```

如果流量预测不准，可能出现：

- 某些链路空闲；
- 某些链路拥塞；
- 重配置收益下降；
- 拓扑频繁变化。

因此需要：

- telemetry；
- flow measurement；
- job scheduler 信息；
- traffic matrix estimation；
- 预测模型；
- 优化算法。

---

#### 14.4 光学精度和可靠性要求高

OCS 依赖精密光学。

需要处理：

- 插入损耗；
- 光纤准直；
- 镜面污染；
- 机械寿命；
- 温度变化；
- 振动；
- 光功率预算；
- 链路测试。

---

### 15. 与前面章节的联系

---

#### 15.1 与 6.2.2 hardware racks 的联系

6.2.2 提到：

- ToR；
- data center fabric；
- rack；
- pod；
- accelerator rack。

6.4.4 进一步说明：

> fabric 本身可以通过 OCS 动态重构，而不是固定布线。

---

#### 15.2 与 6.3.2.1 TPU 的联系

TPUv4 使用 OCS：

- 连接 TPU cubes；
- 形成可重构 pod；
- 故障替换；
- 拓扑定制。

6.4.4 使用 OCS：

- 连接 aggregation blocks；
- 替代 spine；
- 动态网络拓扑；
- 增量扩容。

二者都体现：

```text
光交换 = 系统灵活性
```

---

#### 15.3 与 6.4.3 Clos 网络的联系

6.4.3 讲 Clos：

- leaf/spine；
- fat-tree；
- bisection bandwidth；
- oversubscription；
- optical cost；
- Jupiter。

6.4.4 讲 Clos 的演进：

```text
传统电子 spine
→ OCS spine-less
→ 动态 topology engineering
```

---

### 16. 关键术语表

|术语|含义|
| ------------------------| ----------------------------------------------|
|spine-less networking|用 OCS 替代传统电子 spine 的网络架构|
|OCS|Optical Circuit Switch，光电路交换|
|MEMS|Micro-Electro-Mechanical Systems，微机电系统|
|MEMS mirror|微机电控制的小镜子|
|collimation|光束准直|
|optical loss|光损耗|
|insertion loss|插入损耗|
|circuit switching|电路交换|
|packet switching|包交换|
|aggregation block|聚合模块|
|spine layer|脊层|
|re-stripe|重新排列 Clos mesh 光纤连接|
|elephant flow|大流量、长持续时间网络流|
|mice flow|小流量、短持续时间网络流|
|topology engineering|拓扑工程|
|incremental deployment|增量部署|
|heterogeneous speeds|异构速率|
|protocol oblivious|协议无关|
|speed oblivious|速率无关|
|dynamic topology|动态拓扑|
|traffic engineering|流量工程|
|control plane|控制平面|
|ECMP|Equal-Cost Multi-Path|
|Clos network|多级交换网络|
|fat-tree|胖树网络|

---

### 17. 可以用来检验理解的问题

---

#### 问题 1：为什么 WSC 网络需要动态演进？

因为 WSC 规模巨大，设备代际不断更新，网络速率从 40G、100G、200G 到 400G 持续升级。

同时已部署的基础设施不能轻易下线，所以网络必须支持增量升级和混合速率。

---

#### 问题 2：传统 Clos spine 层有什么问题？

传统 Clos 的 spine 层通常需要统一高速端口。

如果集群中任何部分要升级到更高速率，可能需要升级整个 spine。

这导致：

- 成本高；
- 扩容困难；
- 升级 disruptive；
- 难以混合不同速率设备。

---

#### 问题 3：OCS 的基本工作原理是什么？

OCS 使用两组 MEMS 镜子。

输入光纤的光经过准直后打到第一组镜子。

第一组镜子把光束导向目标输出镜列 x，第二组镜子再把光导向输出光纤 row y。

这样就建立了输入端口到输出端口的光路。

---

#### 问题 4：为什么 OCS 对协议、波长和速率不敏感？

因为 OCS 只是转向光束，不解析数据包，不处理 Ethernet/IP/TCP，也不关心速率和波长。

因此当端侧光模块升级时，OCS 通常不需要升级。

---

#### 问题 5：OCS 如何帮助增量扩容？

添加新的 aggregation block 时，不需要拔插大量光纤重新 re-stripe Clos mesh。

只需要重编程 OCS，调整镜子角度，建立新光路。

这显著降低运维复杂度和错误率。

---

#### 问题 6：OCS 如何支持动态拓扑？

OCS 可以根据应用通信模式动态调整 aggregation blocks 之间的连接。

例如某个 ML 训练任务跨两个 aggregation block，需要更多带宽，OCS 可以给这两个 block 分配更多光路。

---

#### 问题 7：什么是 topology engineering？

topology engineering 指主动调整网络物理拓扑，使其匹配当前 workload 的通信需求。

OCS 使数据中心第一次可以常规化地做 topology engineering。

---

#### 问题 8：OCS 和电子 packet spine 的主要区别是什么？

电子 packet spine：

- 解析包；
- 支持缓存；
- 支持逐包转发；
- 支持 ECMP；
- 但速率/协议相关，升级成本高。

OCS spine：

- 只建立光路；
- 不解析包；
- 速率/协议无关；
- 支持动态拓扑；
- 但没有缓存，需要控制平面和调度配合。

---

### 18. 这一节可以整理成的精简笔记

```text
6.4.4 Spine-less networking

1. 核心问题：
   WSC 规模巨大，例如 40MW 级基础设施，
   且计算、存储和加速器设备不断演进。
   网络速率需要从 40Gbps 定期升级到 400Gbps，
   但已部署服务不能轻易下线。
   因此网络必须支持动态、增量、非破坏性演进。

2. 传统 Clos 的限制：
   - Clos 网络通常需要统一高速 spine 层；
   - 如果集群中任何部分要支持更快端口速率，
     整个 spine 都可能需要升级；
   - 这成本过高且不实际；
   - 传统 Clos 难以增量引入更快设备；
   - 添加新 aggregation block 需要拔插大量光纤，
     重新 re-stripe Clos mesh，繁琐且易错。

3. OCS 的作用：
   - Optical Circuit Switch，光电路交换；
   - 支持异构速率；
   - 支持增量集群扩展；
   - 可替代传统电子 spine 层；
   - 在 aggregation blocks 之间建立直接光连接；
   - 使网络拓扑可动态重配置。

4. OCS 工作原理：
   - 使用两组 MEMS mirrors；
   - MEMS mirror array 由大量毫米级小镜子组成；
   - 每个镜子可沿两个轴倾斜；
   - 输入/输出光纤经过精密准直 collimation；
   - 第一组镜子把光束导向输出 mirror column x；
   - 第二组镜子把光导向 row y 的输出光纤；
   - 为降低光损，光束必须非常精确地正面进入输出光纤。

5. OCS 的关键优势：
   - OCS 只是转向光，不解析数据包；
   - 因此对网络协议、波长和速率不敏感；
   - 新光模块或新速率引入时，OCS 不需要升级；
   - 可以同时处理多种速率端口；
   - 适合多代设备共存的 WSC 环境。

6. Spine-less networking：
   - 使用 OCS 层替代传统 spine 层；
   - aggregation blocks 之间通过 OCS 直接光连接；
   - 不再需要统一速率的电子 spine；
   - 可以连接不同代际、不同速率的 aggregation blocks。

7. 增量部署优势：
   - 添加或移除 aggregation block 时，
     只需重编程 OCS 镜子；
   - 不需要人工拔插数百或数千光纤；
   - 避免 re-stripe Clos mesh；
   - 降低运维复杂度、错误率和停机风险。

8. 动态拓扑：
   - OCS 可根据应用通信模式调整拓扑；
   - 适合 elephant flows，即大流量、长持续时间流；
   - 例如 ML 训练跨两个 aggregation blocks 需要更多带宽时，
     OCS 可分配更多端口给这两个 blocks；
   - 任务结束后拓扑可恢复。

9. topology engineering：
   - OCS 使网络连接重配置成为标准实践；
   - 数据中心首次可以常规化进行 topology engineering；
   - 网络拓扑不再只是静态布线，
     而可以根据 workload、流量矩阵和调度需求动态调整。

10. OCS vs 电子 packet spine：
   - 电子 spine：
       包交换、缓存、逐包转发、ECMP、QoS，
       但速率/协议相关，升级成本高；
   - OCS：
       光路交换、协议/速率无关、低功耗、
       支持动态拓扑和增量扩容，
       但没有缓存，需要控制平面和调度协同。

11. 局限与挑战：
   - OCS 重配置不是逐包进行；
   - 没有包缓存，不能靠交换芯片吸收突发；
   - 需要准确流量需求和控制平面；
   - 需要路由协议、调度和拥塞控制配合；
   - 光学准直、插入损耗和可靠性要求高。

12. 与 TPU OCS 的联系：
   - TPUv4 使用 OCS 连接 4x4x4 cubes，
     形成可重构 TPU pod；
   - 数据中心 spine-less networking 使用 OCS
     连接 aggregation blocks，替代电子 spine；
   - 两者共同思想是：
       用光路可重构性提高系统灵活性、
       可用性、增量部署能力和拓扑匹配能力。

13. 总结：
   Spine-less networking 的核心是用 OCS
   解决传统 Clos 网络升级难、扩容难、
   速率异构难和拓扑僵化的问题。
   OCS 通过 MEMS 镜子建立动态光路，
   使数据中心网络可以混合速率、增量扩展、
   动态重配置，并支持 topology engineering。
   这让 WSC 网络从“静态布线基础设施”
   变成“可编程系统资源”。
```

---

### 19. 如果考试或讨论中要回答这一节，可以这样说

> 6.4.4 节讨论 spine-less networking，核心是如何用光电路交换 OCS 解决传统 Clos 网络在升级、扩容和异构速率支持上的困难。WSC 部署规模巨大，例如 40MW 级基础设施，同时计算、存储和加速器设备不断演进，网络速率需要从 40Gbps 定期升级到 400Gbps。但传统 Clos 网络需要统一高速 spine 层，如果集群中任何部分要引入更高速率，往往需要升级整个 spine，这成本过高且会干扰已部署服务。添加新的 aggregation block 时，还需要拔插大量光纤，重新 re-stripe Clos mesh，过程繁琐且容易出错。
>
> OCS 通过光路交换解决这些问题。OCS 使用两组 MEMS 镜子动态连接输入和输出光纤端口。MEMS mirror array 由大量毫米级小镜子组成，每个镜子可以沿两个轴倾斜，从而精确控制光束方向。输入和输出光纤必须精密准直，使激光束能够准确打到镜子并最终进入目标输出光纤。要连接到输出端口 x,y，第一组镜子把光束导向输出镜列 x，第二组镜子再把光导向 row y 的光纤。为了降低光损耗，准直必须极其精确。
>
> OCS 的关键优势在于它只是转向光，不解析数据包，因此对网络协议、波长和速率不敏感。当新的光模块或更高速率端口引入时，OCS 本身通常不需要升级，并且可以同时处理多种速率端口。通过使用 OCS 层，传统电子 spine 层可以被移除，aggregation blocks 之间可以通过 OCS 建立直接光连接。添加或移除 aggregation block 时，只需要重编程 OCS 镜子，而不需要人工拔插数百或数千光纤。
>
> OCS 还支持动态拓扑。传统数据中心网络的物理拓扑通常是固定布线，而 OCS 使网络连接重配置成为标准实践。对于 elephant flows，例如跨多个 aggregation blocks 的大规模 ML 训练任务，OCS 可以动态分配更多端口给相关 blocks，从而提高带宽、降低拥塞。任务结束后，拓扑可以重新调整。这样，数据中心第一次可以常规化地进行 topology engineering，使网络拓扑根据应用通信模式动态优化。
>
> 当然，OCS 也不是替代所有电子交换。电子 packet spine 支持缓存、逐包转发、ECMP 和细粒度 QoS，而 OCS 没有包缓存，也不做逐包转发，因此需要强大的控制平面、流量测量、调度系统和拥塞控制配合。OCS 更适合大流量、较稳定、可预测的带宽需求，以及增量部署和异构速率演进。
>
> 总体而言，这一节的核心结论是：spine-less networking 通过 OCS 将数据中心网络从固定布线的 Clos 架构，演进为可动态重配置的光网络。它解决了传统 spine 层速率统一、升级昂贵、扩容困难的问题，使 WSC 网络能够支持多代设备共存、增量扩展、动态拓扑和 topology engineering。这与 TPUv4 中使用 OCS 构建可重构 pod 的思想一致，都是用光路可重构性提高系统灵活性、可用性和长期演进能力。


**专栏导航**

- ← 上一篇：[6.4.3 Cluster networking](/posts/6-4-3-cluster-networking/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.4.5 Optics in warehouse-scale data centers →](/posts/6-4-5-optics-in-warehouse-scale-data-centers/)
