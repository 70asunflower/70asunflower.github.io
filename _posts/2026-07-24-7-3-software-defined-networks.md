---
title: "7.3 Software-defined networks"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：7.3 Software-defined networks。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.3 Software-defined networks。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.3 Software-defined networks

下面把 **7.3 Software-defined networks** 作为一个独立小节来深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

---

### 7.3 Software-defined networks 深入理解

这一节讲的是 software-defined infrastructure 在网络层面的体现：  
也就是 **Software-Defined Networking，SDN**。

如果说：

- 7.1 讲的是软件定义服务器；
- 7.2 讲的是软件定义加速器；
- 那么 7.3 讲的是软件定义网络。

它们共同服务于一个核心思想：

> 用软件控制平面把底层硬件抽象、集中管理和全局优化，使基础设施更灵活、更高效、更容易演进。

---

#### 一、为什么网络需要软件定义？

原文开头说：

> Networks with many elements, whether they are in a WAN or a LAN, need to be managed automatically.

无论是 WAN，广域网，还是 LAN，局域网，只要网络设备数量很多，就必须自动管理。

在 WSC 中，网络规模非常大：

- 成千上万台交换机；
- 大量服务器；
- 大量链路；
- 多集群；
- 多数据中心；
- 跨地域 WAN；
- 动态应用部署；
- 多租户隔离；
- 故障恢复；
- 流量工程。

如果靠人工配置每台交换机，几乎不可能。

因此原文说：

> The need for a programmable network has led to much interest in OpenFlow, P4, and software-defined networking.

也就是说，网络需要可编程，于是出现了：

- OpenFlow；
- P4；
- SDN。

---

### 二、SDN 的核心思想：控制平面从设备中抽出来

原文说：

> SDN moves the network control plane out of individual switches into a logically centralized controller.

这是 SDN 最核心的定义：

> 把网络控制平面从单个交换机中移出来，放到一个逻辑上集中的控制器中。

要理解这句话，需要先理解网络的三个平面。

---

#### 1. Data plane，数据平面

data plane 负责：

> 真正转发数据包。

例如：

```text
数据包进入交换机
    ↓
查转发表
    ↓
从某个端口转发出去
```

data plane 关心的是：

- packet forwarding；
- packet processing；
- queueing；
- dropping；
- rewriting；
- encapsulation；
- ACL；
- NAT；
- tunneling。

它通常由交换芯片、ASIC、NPU 等硬件高速执行。

---

#### 2. Control plane，控制平面

control plane 负责：

> 决定数据包应该怎么转发。

例如：

- 计算网络拓扑；
- 计算可达性；
- 计算最短路径；
- 计算流量路径；
- 生成转发表；
- 下发路由规则。

传统网络中，control plane 通常运行在每台路由器或交换机内部。

例如：

```text
每台路由器自己运行路由协议
    ↓
和邻居交换信息
    ↓
自己计算路由表
    ↓
自己生成转发表
```

SDN 则把 control plane 集中到控制器中：

```text
SDN controller 拥有全局视图
    ↓
计算路径和策略
    ↓
把规则下发给交换机
```

---

#### 3. Management plane，管理平面

management plane 负责：

- 配置；
- 监控；
- 策略；
- 升级；
- 故障处理；
- 回滚；
- telemetry；
- 容量规划。

原文说：

> SDN separates data, control, and management planes, with the latter two implemented in software.

也就是说：

> SDN 把 data、control、management 三个平面分离，其中 control 和 management 由软件实现。

---

### 三、SDN 的架构：商品硬件 + 软件控制

原文说：

> Software-defined networks leverage commodity hardware components while addressing control and management requirements in software.

也就是说：

> SDN 使用商品化硬件，而把控制和管理需求放到软件中实现。

这里有两个关键词。

---

#### 1. commodity hardware / merchant silicon

commodity hardware 指通用、商品化硬件。  
merchant silicon 指商用芯片，例如交换 ASIC。

传统网络设备往往是：

```text
专有硬件 + 专有软件 + 专有控制平面
```

SDN 则更倾向于：

```text
商用交换芯片 + 通用服务器控制器 + 软件控制平面
```

这带来几个好处：

- 降低硬件锁定；
- 降低设备成本；
- 更容易规模化；
- 更容易统一编程；
- 更容易快速演进软件。

---

#### 2. standardized protocols

原文说：

> using standardized protocols to program the data plane.

SDN 控制器需要通过标准协议或接口来编程 data plane。

原文后面提到的例子包括：

- OpenFlow；
- P4；
- OpenConfig；
- SAI。

这些接口让软件可以控制不同厂商、不同芯片、不同设备。

---

### 四、SDN 的解耦带来什么好处？

原文说：

> This decoupling enables the network to be managed as a unified entity rather than individual devices.

也就是说：

> 这种解耦让网络可以作为一个统一实体来管理，而不是作为一堆独立设备来管理。

这非常重要。

---

#### 1. 从“设备视角”变成“网络视角”

传统网络管理往往是：

```text
配置交换机 A
配置交换机 B
配置交换机 C
...
希望整体行为正确
```

SDN 管理则是：

```text
控制器拥有全局网络视图
    ↓
计算整体策略
    ↓
下发到所有相关交换机
```

网络被看成一台统一设备。

---

#### 2. 独立扩展

原文说：

> It also allows for independent scaling, e.g., hardware can be upgraded without modifying the control algorithms.

也就是说：

> 硬件和软件可以独立演进。

例如：

- 交换芯片升级，但控制算法不变；
- 控制器算法升级，但交换机硬件不变；
- 新增设备类型，只要支持标准接口即可；
- 管理平面升级，不影响 data plane 转发。

这降低了系统演进成本。

---

#### 3. 更容易集成新算法

原文说：

> This separation also enabled the control and management planes to better integrate new algorithms to optimize the underlying hardware.

因为控制逻辑集中在软件中，所以可以更容易引入：

- 更好的路由算法；
- 更好的流量工程；
- 更好的故障恢复；
- 更好的负载均衡；
- 更好的拥塞控制；
- 更好的节能策略；
- 更好的安全策略。

传统网络中，算法升级可能要更新成千上万台设备的固件。  
SDN 中，可以主要升级控制器软件。

---

### 五、集中控制为什么更简单？

原文说：

> Controlling a network from a logically centralized server offers many advantages.

这里的“逻辑集中”很重要。

它不一定意味着只有一台物理服务器。  
实际系统中，SDN controller 通常是分布式集群，但对外表现为一个逻辑控制器。

---

#### 1. 全局视图让问题更简单

原文举例：

> common networking algorithms such as computing reachability, shortest paths, or max-flow traffic placement become much simpler to solve centrally.

常见网络问题包括：

|问题|含义|
| ----------------------------| ---------------------|
|reachability|哪些节点之间可达|
|shortest paths|最短路径计算|
|max-flow traffic placement|最大流/流量放置优化|

如果有一个全局视图，这些问题更容易求解。

因为控制器知道：

- 整个拓扑；
- 所有链路容量；
- 所有交换机状态；
- 所有流量需求；
- 所有策略约束；
- 所有故障信息。

---

#### 2. 分布式路由的难点

原文说：

> In networks where each individual router must solve the same problem, it’s harder to reach a consistent state.

传统网络中，每台路由器都要自己解决路由问题。

但它们面临三个困难。

---

##### 困难 1：有限可见性

原文说：

> limited visibility, direct neighbors only.

传统路由器通常只能直接看到邻居。

它必须通过路由协议逐步传播信息，才能得到全局拓扑。

这会导致：

- 收敛慢；
- 信息延迟；
- 临时环路；
- 临时黑洞；
- 局部最优而非全局最优。

---

##### 困难 2：状态不一致

原文说：

> inconsistent network state, routers that are out of sync with the current network state.

不同路由器可能在某一时刻看到不同网络状态。

例如：

- 某条链路已经故障；
- 一些路由器已经知道；
- 另一些路由器还不知道；
- 导致转发不一致。

这就是分布式系统中的经典问题：

> 多个节点对世界状态认知不一致。

---

##### 困难 3：大量独立并发参与者

原文说：

> many independent and concurrent actors, routers.

网络中有很多路由器同时运行协议、同时做决策。

这会导致：

- 协调困难；
- 状态震荡；
- 配置冲突；
- 收敛竞争；
- 难以保证全局策略一致。

---

#### 3. 集中控制可以更容易做一致性更新

原文说：

> Network management operations also become simple because a global view can be used to move a network domain, often consisting of thousands of individual switches, from one consistent state to another.

也就是说：

> 网络管理操作可以变得更简单，因为全局视图可以把一个包含成千上万交换机的网络域，从一个一致状态迁移到另一个一致状态。

这很关键。

例如网络升级或策略变更：

```text
旧一致状态
    ↓
控制器计算迁移计划
    ↓
逐步下发规则
    ↓
新一致状态
```

如果中间出错，还可以：

> rollback，回滚。

原文说：

> simultaneously accounting for errors that may require rollback of the higher-level management operation underway.

也就是说，集中控制器可以在执行高层管理操作时考虑错误处理和回滚。

这比在成千上万台设备上手动配置安全得多。

---

### 六、为什么服务器比交换机更适合做控制平面？

原文说：

> servers are easier to program and offer more powerful hardware than CPUs embedded in switches and routers.

交换机和路由器内部通常有嵌入式 CPU。  
它们适合运行简单控制任务，但不一定适合复杂算法。

相比之下，服务器有：

- 更强 CPU；
- 更多内存；
- 更好编程环境；
- 更容易部署复杂软件；
- 更容易更新；
- 更容易做集群高可用；
- 更容易运行数据库、优化器、分析系统。

因此原文说：

> Centralizing the control plane to a few servers also makes it easier to update their software.

把控制平面集中到少量服务器上，比更新成千上万台交换机更容易。

---

### 七、为什么 SDN 特别适合数据中心？

原文说：

> SDN is a natural match for data center networking, since the applications running in a WSC are already managed by a central entity, the cluster manager.

这是一个非常重要的观察。

在 WSC 中，应用本来就已经由一个中央实体管理：

> cluster manager。

cluster manager 知道：

- 哪些服务在运行；
- 哪些任务被调度到哪里；
- 哪些服务需要通信；
- 哪些租户需要隔离；
- 哪些服务有 SLO；
- 哪些节点故障；
- 哪些资源紧张。

因此很自然地，可以让 SDN controller 和 cluster manager 协同：

```text
cluster manager 调度应用
    ↓
SDN controller 配置网络
    ↓
应用获得所需网络连接和策略
```

这比让网络设备自己猜测应用需求更合理。

---

#### 数据中心 SDN 的典型价值

在数据中心中，SDN 可以帮助实现：

- 虚拟机/容器迁移；
- 多租户隔离；
- 安全组策略；
- 负载均衡；
- 服务发现；
- 网络虚拟化；
- 故障快速恢复；
- 带宽保障；
- 拥塞控制；
- 网络可观测性。

这些都适合集中控制。

---

### 八、为什么 SDN 也适合 WAN？

原文说：

> SDN is equally attractive to manage WAN networks, where logically centralized control simplifies many routing and traffic engineering problems.

WAN 是跨数据中心的广域网。

WAN 的难点包括：

- 链路昂贵；
- 带宽有限；
- 流量波动大；
- 多路径选择；
- 故障恢复复杂；
- 需要流量工程；
- 需要成本优化；
- 需要全局拥塞管理。

集中控制可以更容易做：

- traffic engineering；
- 路径优化；
- 带宽预留；
- 故障绕路；
- 成本感知路由；
- 拥塞避免。

因此 SDN 不只适合数据中心内部，也适合数据中心之间。

---

### 九、Google 的 SDN 实践：B4

原文提到：

> the first real-world implementations of SDN were developed at Google.

Google 是早期大规模生产环境部署 SDN 的代表。

---

#### 1. B4 是什么？

原文说：

> The first production SDN network, B4, addressed the growing video traffic and other bulk traffic on Google’s network.

B4 是 Google 的第一个生产 SDN 网络。  
它主要处理：

- 视频流量；
- 其他 bulk traffic，大批量流量。

---

#### 2. B4 的目标：让流量走更便宜的骨干网

原文说：

> allowed it to travel on the cheaper B4 backbone instead of the more expensive, full-feature B2 backbone.

也就是说：

> B4 让这些流量走更便宜的 B4 backbone，而不是更昂贵、功能更全的 B2 backbone。

这说明 SDN 的一个直接收益是：

> 成本优化。

通过集中控制，Google 可以更精细地决定：

- 哪些流量走哪条骨干；
- 哪些流量可以容忍较低可靠性；
- 哪些流量需要高可用路径；
- 如何最大化链路利用率；
- 如何降低带宽成本。

---

#### 3. 为什么视频流量适合早期 SDN？

原文说：

> Video traffic was an ideal use case for a nascent technology like SDN because it combined high scale with a lower availability requirement.

视频流量有两个特点：

1. 规模很大；
2. 对可用性要求相对较低。

原文进一步解释：

> At the time, YouTube’s overall availability was significantly below 99.99%, and thus carrying its non-cached traffic at lower reliability was acceptable.

也就是说，当时 YouTube 的整体可用性显著低于 99.99%。  
因此用可靠性稍低但更便宜的网络承载其非缓存流量是可以接受的。

这体现了系统设计中常见策略：

> 新技术先用于高价值但可容忍一定风险的场景。

视频流量规模大，优化收益高；  
同时它对瞬时丢包或短暂不可用的容忍度比关键交易类流量更高。

---

#### 4. B4 如何实现？

原文说：

> B4 performed all key management and control plane functions on servers running the SDN stack and programmed the network’s Ethernet switches via OpenFlow.

也就是说：

- 关键 management 和 control plane 功能运行在服务器上；
- 通过 OpenFlow 编程以太网交换机。

这体现了 SDN 的典型结构：

```text
服务器上的 SDN stack
    ↓
OpenFlow
    ↓
以太网交换机 data plane
```

---

### 十、数据中心网络中的 SDN：Saturn 到 Jupiter

原文说：

> Concurrently, SDN also took over data center networks.

也就是说，SDN 同时也进入了数据中心网络。

---

#### 1. Saturn 网络：部分集中化

原文说：

> In the 2008-era Saturn network, the centralized controllers performed configuration and helped switches understand the global state, but switch-based software programmed the switch’s actual forwarding tables.

Saturn 是 2008 年前后的数据中心网络。

它的特点是：

- 集中控制器负责配置；
- 帮助交换机理解全局状态；
- 但交换机自己的软件仍然负责编程实际转发表。

也就是说，Saturn 是：

> 集中控制的一部分，但转发规则生成仍部分留在交换机侧。

这是一种渐进式 SDN 化。

---

#### 2. Jupiter 网络：更完整的 SDN

原文说：

> The 2012-era Jupiter network implemented a five-stage Clos network topology and used Onix SDN controllers using OpenFlow to push routing and configuration information to fabric switches.

Jupiter 是 2012 年前后的数据中心网络。

它的特点包括：

- 使用 five-stage Clos network topology；
- 使用 Onix SDN controllers；
- 使用 OpenFlow；
- 把路由和配置信息推送到 fabric switches。

这比 Saturn 更进一步：

> 控制器直接参与转发和路由信息的下发。

---

#### 3. 当前 Jupiter：从 OpenFlow 到 P4

原文说：

> Current Jupiter generations provide additional functionality, having replaced OpenFlow with P4.

当前 Jupiter 用 P4 替代了 OpenFlow。

这说明 SDN 编程能力在演进：

```text
OpenFlow：主要编程转发表
    ↓
P4：更灵活地编程整个 packet processing pipeline
```

---

### 十一、从 OpenFlow 到 P4

原文专门讲了 P4 的演化。

---

#### 1. OpenFlow 的局限

原文说：

> P4 evolved out of OpenFlow, recognizing that SDN requires more than programming forwarding tables.

也就是说：

> P4 从 OpenFlow 演化而来，因为人们认识到 SDN 不只是编程转发表。

OpenFlow 主要用于：

- 匹配 packet header；
- 执行动作；
- 转发到端口；
- 修改部分字段；
- 送到控制器。

但随着网络功能复杂化，交换机需要处理更多事情。

---

#### 2. 交换芯片从简单转发变成复杂包处理

原文说：

> Ethernet switch chips evolved from pure packet switching to sophisticated packet processing.

例如，进入交换机的数据包可能需要：

|功能|例子|
| ----------------| ---------------|
|filtering|firewall 功能|
|rewriting|NAT|
|encapsulation|GRE tunnel|
|access control|ACL|
|load balancing|ECMP|
|telemetry|INT、mirror|
|segmentation|VLAN、VXLAN|

这些不是简单“从一个端口转发到另一个端口”。

---

#### 3. P4 的作用

原文说：

> P4 lets SDN controllers specify this packet processing in a high-level, hardware-independent language.

P4 是一种高级、硬件无关语言。

它允许控制器描述：

- packet 如何解析；
- 匹配哪些字段；
- 执行什么动作；
- 如何修改包头；
- 如何封装；
- 如何转发；
- 如何上报 telemetry。

然后：

> P4 compilers translate that specification into a chip-specific implementation.

也就是说，P4 编译器把高级描述编译成具体芯片实现。

这样：

> vendor-specific details are hidden from the SDN controller.

控制器不需要知道底层 ASIC 的具体细节。

---

#### 4. OpenFlow 与 P4 的简单对比

|维度|OpenFlow|P4|
| ----------| ------------------| ---------------------------------|
|本质|协议|语言|
|主要目标|编程 flow table|编程 packet processing pipeline|
|灵活性|相对固定|更灵活|
|协议支持|主要围绕已有协议|可定义新协议处理|
|硬件抽象|有限|更强|
|编译|不强调编译模型|P4 编译到目标芯片/软件交换机|

---

### 十二、商用网络设备中的 SDN：OpenConfig、SAI、SONiC

原文最后说：

> SDN has also taken hold in networks composed of commercially available networking equipment.

也就是说，SDN 不仅存在于自研网络，也进入商用网络设备生态。

---

#### 1. OpenConfig

原文说：

> OpenConfig allows such equipment to be programmed and managed via a vendor-agnostic standard API.

OpenConfig 提供：

- 厂商无关；
- 标准 API；
- 配置模型；
- telemetry 模型。

它让不同厂商设备可以用统一方式管理。

---

#### 2. SAI，Switch Abstraction Interface

原文说：

> The Switch Abstraction Interface, SAI, provides a vendor-independent way of controlling forwarding elements, such as a switching ASIC, an NPU or a software switch.

SAI 是交换抽象接口。

它位于：

```text
网络操作系统 / 控制软件
        ↓
       SAI
        ↓
交换 ASIC / NPU / 软件交换机
```

作用是：

> 让上层软件不用关心底层交换芯片厂商细节。

---

#### 3. SONiC

原文说：

> The SONiC stack includes the networking software components necessary for a fully functional L3 device in a cloud data center.

SONiC 是一个网络软件栈，包含云数据中心 L3 设备所需的网络软件组件。

可以理解为：

> 一个运行在商用交换机上的网络操作系统栈。

它通常与 SAI 配合，屏蔽不同 ASIC 差异。

---

#### 4. 标准化组件的意义

原文总结：

> while WSC management and control planes are not standardized, they can take advantage of standardized components and APIs.

也就是说：

> WSC 的管理和控制平面本身可能没有统一标准，但可以使用标准化的组件和 API。

这很符合超大规模数据中心的现实：

- 每家 hyperscaler 的控制平面可能不同；
- 但底层设备接口、配置模型、交换抽象可以标准化；
- 这样可以降低厂商锁定，提高可维护性。

---

### 十三、SDN 与 software-defined infrastructure 的关系

这一节和整章主题高度一致。

---

#### 1. 全局视图优化局部决策

原文前面说 software-defined infrastructure 的核心是：

> take advantage of a global view to optimize local decisions.

SDN 正是如此：

- 单个交换机只看局部端口和邻居；
- SDN controller 看整个网络；
- 因此可以计算更优路径和策略。

---

#### 2. 硬件商品化，软件智能化

SDN 的结构是：

```text
商品化交换硬件
    +
集中软件控制
    +
标准接口
```

这和 software-defined servers 的思想一致：

> 不依赖单一专有硬件，而通过软件提升整体灵活性和效率。

---

#### 3. 抽象层和效率层

SDN 也有类似抽象层和效率层：

|层次|SDN 中对应|
| --------| ----------------------------------------|
|抽象层|OpenFlow、P4、OpenConfig、SAI|
|控制层|SDN controller|
|管理层|网络管理、策略、telemetry、rollback|
|优化层|路由算法、流量工程、拥塞控制、故障恢复|

---

### 十四、可以用一个类比理解 SDN

可以把传统网络想象成：

> 很多司机各自看局部路况，自己决定怎么走。

每个路由器只知道邻居，靠分布式协议慢慢同步信息。

SDN 则像：

> 一个城市交通指挥中心，看到全部道路、车流和事故，然后统一指挥。

指挥中心可以：

- 看到全局拥堵；
- 统一规划路径；
- 临时调整信号灯；
- 处理事故；
- 回滚错误决策；
- 优化整体通行时间。

这就是集中控制的优势。

---

### 十五、这一节的关键系统权衡

---

#### 1. 集中控制 vs 单点故障

集中控制器有全局视图，但如果控制器故障怎么办？

实际系统通常用：

- 多控制器集群；
- 复制状态；
- 故障切换；
- 本地 fallback；
- data plane 独立转发能力。

所以原文说：

> logically centralized

而不是：

> physically single point。

---

#### 2. 全局最优 vs 实时性

集中控制器可以算全局最优，但网络变化很快。

因此需要：

- 快速 telemetry；
- 增量更新；
- 局部快速恢复；
- 控制器扩展性。

---

#### 3. 灵活性 vs 硬件限制

P4 提高了灵活性，但最终仍要编译到具体芯片。

不是所有 packet processing 都能在所有硬件上高效实现。

因此需要：

- 硬件能力抽象；
- 编译器优化；
- 功能降级；
- 软件交换机补充。

---

#### 4. 标准化 vs 自研优化

WSC 控制平面往往自研，因为每家需求不同。  
但底层 API 和组件标准化可以降低成本。

所以原文说：

> WSC management and control planes are not standardized, but they can take advantage of standardized components and APIs.

---

### 十六、这一节的核心逻辑链

```text
网络规模巨大，设备众多
  ↓
传统分布式网络设备难以全局优化
  ↓
SDN 把 control plane 和 management plane 从设备中抽出
  ↓
控制平面集中到服务器上的软件控制器
  ↓
data plane 仍由交换硬件高速转发
  ↓
控制器拥有全局视图
  ↓
更容易计算路径、流量工程、一致性更新、回滚
  ↓
OpenFlow 提供早期 data plane 编程协议
  ↓
P4 提供更高级、更灵活的 packet processing 编程
  ↓
OpenConfig / SAI / SONiC 推动商用设备标准化
  ↓
SDN 支撑数据中心网络和 WAN
```

---

### 十七、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.3 Software-defined networks

1. 核心问题：
   - WAN 和 LAN 中都有大量网络设备
   - 网络必须自动管理和编程
   - 因此出现：
     - OpenFlow
     - P4
     - SDN

2. SDN 的核心定义：
   - 将网络控制平面从单个交换机中移出
   - 放到逻辑上集中的控制器中
   - 分离三个平面：
     - data plane：转发数据包
     - control plane：决定如何转发
     - management plane：配置、监控、策略、回滚
   - control plane 和 management plane 由软件实现

3. SDN 的基本架构：
   - 使用 commodity hardware / merchant silicon
   - 使用软件实现控制和管理
   - 使用标准化协议编程 data plane
   - 网络被当作统一实体管理，而不是单个设备集合

4. SDN 解耦的好处：
   - 统一管理整个网络
   - 硬件和软件可独立扩展
   - 硬件升级不必修改控制算法
   - 更容易集成新算法
   - 更容易优化底层硬件
   - 更容易支持大规模 WSC 网络

5. 集中控制的优势：
   - 全局视图
   - 更容易解决：
     - reachability
     - shortest paths
     - max-flow traffic placement
   - 传统分布式路由的问题：
     - 每个路由器只能看到直接邻居
     - 网络状态可能不一致
     - 多个路由器并发决策
     - 难以达到一致状态
   - SDN 可以：
     - 将大型网络域从一个一致状态迁移到另一个一致状态
     - 在错误时进行 rollback

6. 为什么服务器适合做控制平面：
   - 服务器比交换机嵌入式 CPU 更强
   - 更容易编程
   - 更容易更新软件
   - 更容易运行复杂算法
   - 更容易构建高可用控制器集群

7. 为什么 SDN 适合数据中心：
   - WSC 应用已经由 cluster manager 集中管理
   - 因此用 SDN controller 配置网络很自然
   - 可以协同应用调度和网络配置
   - 支持：
     - 多租户隔离
     - 虚拟机/容器迁移
     - 安全策略
     - 负载均衡
     - 故障恢复

8. 为什么 SDN 适合 WAN：
   - WAN 有复杂路由和流量工程问题
   - 逻辑集中控制可以简化：
     - 路径选择
     - 带宽优化
     - 成本优化
     - 拥塞控制
     - 故障恢复

9. Google B4：
   - 第一个生产 SDN 网络
   - 处理视频流量和其他 bulk traffic
   - 让流量走更便宜的 B4 backbone
   - 而不是更昂贵、全功能的 B2 backbone
   - 视频流量适合早期 SDN：
     - 规模大
     - 可用性要求相对较低
   - 当时 YouTube 可用性显著低于 99.99%
   - B4 在服务器上运行 SDN stack
   - 通过 OpenFlow 编程以太网交换机

10. 数据中心 SDN 演进：
   - Saturn，2008 年前后：
     - 集中控制器负责配置
     - 帮助交换机理解全局状态
     - 交换机软件仍编程实际转发表
   - Jupiter，2012 年前后：
     - 五级 Clos 网络拓扑
     - 使用 Onix SDN controllers
     - 使用 OpenFlow 推送路由和配置
   - 当前 Jupiter：
     - 用 P4 替代 OpenFlow
     - 提供更灵活的数据平面编程能力

11. OpenFlow 到 P4：
   - OpenFlow：
     - 主要用于编程 forwarding tables
   - P4：
     - 认识到 SDN 不只是转发
     - 提供协议无关、交换机无关的高级语言
     - 可描述复杂 packet processing
   - 现代交换芯片支持：
     - filtering / firewall
     - NAT
     - GRE encapsulation
     - 更复杂的包处理
   - P4 编译器：
     - 将高级描述翻译成芯片特定实现
     - 向控制器隐藏厂商细节

12. 商用网络设备中的 SDN：
   - OpenConfig：
     - 厂商无关标准 API
     - 用于设备编程和管理
   - SAI：
     - Switch Abstraction Interface
     - 厂商无关地控制 forwarding elements
     - 支持 switching ASIC、NPU、software switch
   - SONiC：
     - 网络软件栈
     - 提供云数据中心 L3 设备所需组件

13. 标准化现状：
   - WSC 的 management plane 和 control plane 通常不统一标准化
   - 但可以使用标准化组件和 API
   - 这样既保留自研控制平面的灵活性
   - 又降低硬件厂商锁定

14. 与 software-defined infrastructure 的关系：
   - SDN 是 software-defined infrastructure 在网络层的体现
   - 核心思想：
     - 用软件控制平面管理硬件
     - 用全局视图优化局部决策
     - 用标准接口抽象底层设备
   - 与 software-defined servers 类似：
     - 硬件商品化
     - 控制软件化
     - 管理集中化
     - 优化自动化

15. 核心逻辑：
   网络设备数量巨大
     → 分布式控制难以全局优化
     → SDN 分离 data/control/management planes
     → 控制平面集中到软件控制器
     → 全局视图简化路由、流量工程和管理
     → OpenFlow/P4 提供数据平面编程
     → SDN 支撑数据中心和 WAN
```

---

### 十八、一句话总结这一节

> 7.3 说明：SDN 通过把网络控制平面和管理平面从单个交换机中抽出来，集中到软件控制器中，使网络能够以全局视图进行统一编程、优化和管理；这正是 software-defined infrastructure 在网络层面的核心体现。


**专栏导航**

- ← 上一篇：[7.2 Software-defined accelerators](/posts/7-2-software-defined-accelerators/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.3.1 Jupiter topology and traffic engineering 和 7.3.2 Network aware scheduling →](/posts/7-3-1-jupiter-topology-and-traffic-engineering-7-3-2-network-aware-scheduling/)
