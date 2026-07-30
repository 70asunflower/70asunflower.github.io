---
title: "7.5 Software-defined data center 中的 7.5.1 Software-defined power"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-29
description: "《The Data Center as a Computer》AI 导读专栏正文：7.5 Software-defined data center 中的 7.5.1 Software-defined power。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.5 Software-defined data center 中的 7.5.1 Software-defined power。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.5 Software-defined data center 中的 7.5.1 Software-defined power

下面把 **7.5 Software-defined data center** 中的 **7.5.1 Software-defined power** 作为一个独立小节来深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这一节非常关键，因为它把 software-defined infrastructure 的思想从：

- 计算；
- 加速器；
- 网络；
- 存储；

进一步推进到了：

> 数据中心的物理基础设施，尤其是电力。

也就是说，软件不只是管理服务器、网络和磁盘，还可以管理：

- 功率；
- 电力拓扑；
- 断路器风险；
- 冷却限制；
- 发电机容量；
- 任务优先级；
- 数据中心总容量。

---

### 7.5 Software-defined data center 的核心思想

这一节的总标题是：

> Software-defined data center。

它的意思是：

> 整个数据中心，包括计算、存储、网络、电力、冷却等，都可以通过软件进行抽象、监控、控制和优化。

前面的章节已经体现了这个方向：

|方向|软件定义什么|
| -------------------------------| ------------------------------|
|Software-defined servers|服务器配置、调度、硬件旋钮|
|Software-defined accelerators|加速器上的模型和计算结构|
|Software-defined networks|网络路径、带宽、拓扑、安全|
|Software-defined storage|存储容量、IOPS、介质、放置|
|Software-defined power|电力使用、功率上限、负载节流|

7.5.1 讲的是：

> 如何用软件定义电力管理，从而安全地提高数据中心电力超额订阅能力。

---

### 7.5.1 Software-defined power 深入理解

#### 一、什么是 power oversubscription？

原文说：

> Power oversubscription boosts data center efficiency and reduces costs by deploying more servers in a data center than its power supply can nominally support.

也就是说：

> 电力超额订阅通过在数据中心中部署超过其名义供电能力的服务器，来提高效率并降低成本。

关键词：

> nominally support，名义上支持。

例如一个数据中心设计供电能力是：

```text
10 MW
```

如果严格按照最坏情况设计：

```text
所有服务器同时满载
```

那么最多只能部署：

```text
10 MW 的服务器
```

但实际上，所有服务器很少同时达到峰值。

因此可以部署：

```text
12 MW 甚至更多的服务器
```

这就是：

```text
power oversubscription
```

---

#### 二、为什么 power oversubscription 能提高效率？

数据中心成本很高，尤其是：

- 电力基础设施；
- 变压器；
- UPS；
- 发电机；
- 配电柜；
- 断路器；
- 冷却系统；
- 机房空间。

如果按最坏峰值配置所有设施，会导致：

```text
绝大多数时间设施利用率很低
```

例如：

```text
设计容量：10 MW
日常负载：6 MW
峰值负载：9 MW
```

那么大部分时间有：

```text
4 MW 基础设施闲置
```

这很浪费。

电力超额订阅的思路是：

> 利用负载不会同时达到峰值这一统计规律，提高实际部署密度。

这和很多系统设计思想类似：

|场景|超额订阅思想|
| ------| --------------------------------|
|网络|不是所有主机同时全线速通信|
|内存|不是所有进程同时用满内存|
|CPU|不是所有任务同时需要全部 CPU|
|电力|不是所有服务器同时达到功率峰值|

---

#### 三、电力超额订阅的风险

原文说：

> If all servers peaked at the same time in an oversubscribed data center, they would trip breakers, or overload cooling, or overload generators, or all of the above.

也就是说：

> 如果所有服务器同时达到峰值，超额订阅的数据中心可能会：

- 触发断路器跳闸；
- 冷却系统过载；
- 发电机过载；
- 或上述情况同时发生。

---

##### 1. breaker trip，断路器跳闸

断路器是电力系统的保护机制。

当电流超过安全限制时，断路器会断开电路，防止：

- 火灾；
- 设备损坏；
- 电缆过热；
- 供电系统故障。

但如果数据中心运行中触发 breaker trip：

```text
部分服务器断电
    ↓
服务中断
    ↓
用户受影响
```

这是非常严重的事件。

---

##### 2. cooling overload，冷却过载

服务器耗电最终大部分转化为热量。

如果功率过高：

```text
发热量超过冷却能力
    ↓
机房温度升高
    ↓
硬件降频或损坏
    ↓
服务不可用
```

因此功率限制不只是电力问题，也是冷却问题。

---

##### 3. generator overload，发电机过载

如果市电故障，数据中心可能依赖发电机。

发电机也有容量上限。

如果总功率超过发电机能力：

```text
发电机无法支撑全部负载
    ↓
可能掉电
```

---

#### 四、为什么需要 power capping？

原文说：

> Thus, oversubscribed data centers need a power capping mechanism to drop a subset of load if critical power draw approaches the physical limits of the data center.

也就是说：

> 因此，超额订阅的数据中心需要一种功率封顶机制，当关键功耗接近数据中心物理限制时，丢弃一部分负载。

power capping 可以理解为：

> 功率封顶 / 功率限制 / 功率节流。

当总功率接近危险阈值时，系统会主动降低某些任务的资源使用，从而降低功耗。

例如：

```text
总功率接近上限
    ↓
降低低优先级批处理任务 CPU 配额
    ↓
服务器功耗下降
    ↓
避免断路器跳闸
```

---

### 五、高优先级 serving 与低优先级 batch 的区别

原文说：

> Fortunately, data centers run both high-priority serving tasks and lower-priority batch workloads.

数据中心通常同时运行两类任务。

---

#### 1. high-priority serving tasks

高优先级服务任务，例如：

- Gmail；
- YouTube；
- Search；
- 用户 API；
- 登录服务；
- 支付服务；
- 实时推荐；
- 数据库前端。

它们的特点是：

- 直接服务用户；
- 延迟敏感；
- SLO 严格；
- 不能随便节流；
- 不能随便停止；
- 影响收入和用户体验。

---

#### 2. lower-priority batch workloads

低优先级批处理任务，例如：

- 数据分析；
- 日志处理；
- 索引构建；
- ML 训练中的可暂停任务；
- 数据复制；
- 备份；
- 离线计算；
- 科学计算。

它们的特点是：

- 延迟容忍；
- 可以减速；
- 可以暂停；
- 可以重试；
- 可以迁移；
- 对用户影响较小。

---

#### 六、power capping 优先节流谁？

原文说：

> Power capping systems throttle the latter but try not to throttle the former.

也就是说：

> 功率封顶系统会节流低优先级批处理任务，但尽量不节流高优先级服务任务。

这是非常合理的设计。

例如：

```text
高优先级服务：
必须保持低延迟

低优先级批处理：
可以慢一点
```

当功率接近上限时：

```text
先节流 batch
保护 serving
```

原文进一步说：

> they typically don’t oversubscribe the power needed by high-priority serving tasks.

也就是说：

> 高优先级服务所需的功率通常不会被超额订阅。

换句话说：

```text
超额订阅主要来自低优先级 batch 的弹性容量
```

---

### 七、为什么 oversubscription 能增加数十个百分点容量？

原文说：

> With a reasonable workload diversity, where not all loads peak at the same time, combined with significant batch loads, oversubscription can increase available capacity by tens of percent.

这里有两个条件。

---

#### 1. workload diversity，工作负载多样性

不同负载的峰值时间不同。

例如：

- 用户服务可能白天高；
- 批处理任务可能夜间高；
- 某些业务有地区差异；
- 某些任务周期性运行；
- 不同服务的流量高峰不同。

如果所有负载同时峰值，那么超额订阅很危险。

但如果负载多样：

```text
总峰值 < 各任务峰值之和
```

这就给超额订阅提供了空间。

---

#### 2. significant batch loads，有大量批处理负载

批处理负载越大，可调节空间越大。

例如：

```text
总部署容量：12 MW
高优先级服务：8 MW
低优先级批处理：4 MW
```

如果电力限制接近 10 MW：

```text
可以节流 batch
把总功率压到 10 MW 以下
```

这样就能安全部署 12 MW 服务器，而不是只部署 10 MW。

这就是：

```text
可用容量增加 20%
```

原文给出的实际收益是：

> between 9% and 25%.

---

### 八、Software-defined power 的核心机制

原文说：

> Software-defined power employs a hardware-agnostic power capping system to allow for safe power oversubscription with minimal disruption to workloads.

关键词：

> hardware-agnostic，硬件无关。

也就是说：

> 这个功率封顶系统不依赖特定服务器硬件。

这很重要，因为 WSC 中服务器异构：

- 不同 CPU；
- 不同主板；
- 不同电源；
- 不同 BMC；
- 不同厂商；
- 不同代际。

如果功率控制依赖特定硬件，就很难大规模部署。

软件定义电力控制使用更通用的机制，例如：

> Linux kernel 的 CPU bandwidth control。

---

#### 九、使用 Linux CPU bandwidth control 做 QoS-aware throttling

原文说：

> the system utilizes the CPU bandwidth control feature of the Linux kernel to enable task-level Quality of Service, QoS, aware throttling.

也就是说：

> 系统利用 Linux 内核的 CPU 带宽控制功能，实现任务级、QoS 感知的节流。

---

##### 1. CPU bandwidth control 是什么？

Linux 中可以通过 cgroup 的 CPU bandwidth control 限制某个任务组在单位时间内能使用多少 CPU 时间。

例如：

```text
任务组 A：
每 100 ms 最多使用 50 ms CPU
```

这相当于给它 0.5 个 CPU 的配额。

如果降低配额：

```text
任务可用 CPU 减少
    ↓
执行速度变慢
    ↓
功耗下降
```

---

##### 2. 为什么 CPU 节流能降功耗？

服务器功耗中，CPU 是重要部分。

当 CPU 做更多工作时：

- 频率可能更高；
- 活跃核心更多；
- cache 访问更多；
- 内存访问更多；
- 电压可能更高；
- 功耗更高。

降低任务 CPU 配额后：

```text
CPU 活动减少
    ↓
功耗下降
```

---

##### 3. QoS-aware throttling 是什么？

QoS-aware 指：

> 根据任务服务质量等级进行节流。

例如：

```text
高优先级 serving：
CPU 配额尽量不动

中优先级任务：
必要时适度节流

低优先级 batch：
优先大幅节流
```

这样可以保护用户服务。

---

### 十、控制策略：two-threshold, randomized unthrottling / multiplicative decrease

原文说：

> The system implements a two-threshold, randomized unthrottling/multiplicative decrease control policy that balances power safety with performance optimization.

这是一种控制策略。

可以拆成几个部分理解。

---

#### 1. two-threshold，双阈值

系统有两个阈值：

```text
high threshold，高阈值
low threshold，低阈值
```

高阈值用于安全保护。  
低阈值用于恢复正常。

这类似恒温器中的：

```text
温度太高 → 开冷气
温度足够低 → 关冷气
```

双阈值可以避免频繁开关。

---

#### 2. randomized unthrottling，随机化解节流

当功率下降后，系统需要恢复被节流任务。

如果所有被节流任务同时恢复：

```text
大量任务同时增加 CPU
    ↓
功率突然上升
    ↓
再次触发节流
```

这会造成振荡。

随机化解节流指：

> 不同任务在不同时间逐步恢复，而不是同时恢复。

这样可以平滑功率上升。

---

#### 3. multiplicative decrease，乘性减少

multiplicative decrease 是控制论中常见策略。

例如当功率过高时，不是简单减一点，而是按比例减少：

```text
当前 CPU 配额 × 0.5
```

或者：

```text
当前 CPU 配额 × 0.7
```

这样可以快速降低负载。

这和 TCP 拥塞控制中的思想有点像：

```text
拥塞时快速降窗口
恢复时谨慎增加
```

---

### 十一、软件架构模块

原文描述了 Figure 7.8 中的几个模块。

---

#### 1. meter watcher，电表观察器

原文说：

> The meter watcher module is responsible for polling power readings from meters at a rate of one reading per second.

它负责：

```text
每秒从电表读取功率数据
```

然后做两件事：

1. 把读数传给 power notifier；
2. 把读数存入 power history datastore。

---

##### 为什么是每秒一次？

因为功率变化可能很快，但也不需要微秒级控制。

每秒一次可以：

- 及时发现功率上升；
- 提供足够控制频率；
- 避免过多遥测开销；
- 支持历史分析。

---

#### 2. power history datastore，功率历史数据库

它存储历史功率读数。

用途包括：

- 趋势分析；
- 风险评估；
- 遥测缺失时预测；
- 长期容量规划；
- 控制策略参考。

---

#### 3. power notifier，功率通知器 / 中央控制模块

原文说：

> The power notifier module serves as the central control module, implementing both reactive and proactive capping logic.

它是中央控制模块。

它实现两类逻辑：

1. reactive capping，反应式封顶；
2. proactive capping，主动式封顶。

---

##### reactive capping

当有实时功率读数时：

```text
实时功率接近阈值
    ↓
立即触发 capping
```

这是反应式控制。

---

##### proactive capping

当功率读数不可用时：

```text
无法直接判断当前功率
    ↓
查询 risk assessor
    ↓
根据历史数据评估风险
    ↓
必要时提前 capping
```

这是主动式控制。

这提高了鲁棒性。

因为电力安全不能等到遥测恢复再处理。

---

#### 4. risk assessor，风险评估器

原文说：

> The risk assessor utilizes historical power information from the power history datastore to assess the risk of breaker trips.

它根据历史功率信息评估：

> 断路器跳闸风险。

例如：

- 最近功率趋势；
- 历史峰值；
- 当前时间负载模式；
- 当前任务量；
- 历史故障；
- 功率域容量；
- 遥测缺失时长。

如果风险高，即使没有实时读数，也可以主动节流。

---

#### 5. machine manager，机器管理器

原文说：

> If either logic determines that capping is necessary, the power notifier module passes the appropriate capping parameters to the machine manager module.

也就是说：

> 如果反应式或主动式逻辑认为需要封顶，power notifier 会把封顶参数传给 machine manager。

machine manager 负责：

```text
向具体机器下发节流命令
```

原文说：

> The machine manager then sends remote procedure call, RPC, requests to the node controller of individual machines to reduce power consumption concurrently.

也就是说：

> machine manager 向各机器的 node controller 发送 RPC 请求，并发降低功耗。

这体现了分布式执行：

```text
中央控制逻辑
    ↓
machine manager
    ↓
RPC
    ↓
各机器 node controller
    ↓
调整任务 CPU 配额
```

---

#### 6. power topology datastore，电力拓扑数据库

原文说：

> The power topology datastore is a repository containing critical information about the power delivery topology.

它存储电力输送拓扑信息。

包括：

- protected power limits，受保护的功率限制；
- 某个 power domain 内有哪些机器；
- 电力域边界；
- 断路器归属；
- 配电关系；
- UPS 关系；
- 发电机关系。

---

##### 为什么 power topology 很重要？

因为节流必须作用在正确的机器集合上。

例如某个断路器保护一组机器：

```text
Power Domain A：
机器 1–500
限制：5 MW
```

如果 Power Domain A 接近上限，就必须节流：

```text
机器 1–500 中的任务
```

而不是节流其他 power domain 的机器。

否则没有效果。

---

#### 7. power domain 的规模

原文说：

> These power domains can vary in scale, with some being as small as a few megawatts while others can be as large as tens of megawatts.

也就是说：

> 电力域规模可以从几 MW 到几十 MW。

这说明系统必须支持不同粒度：

```text
小电力域：几 MW
大电力域：几十 MW
```

不同电力域可能有不同限制和不同风险。

---

### 十二、双阈值节流机制

这一部分非常关键。

原文说：

> Two capping thresholds, high and low, strike a balance between responsiveness for power safety and efficiency for minimizing performance impact.

也就是：

> 高阈值和低阈值在功率安全响应和性能影响最小化之间取得平衡。

---

#### 1. high threshold：高阈值

当负载超过 high threshold：

```text
hard throttling 开始
```

原文说：

> hard throttling starts and sets the CPU allocation of “victim” tasks to near zero, thus effectively stopping them.

也就是说：

> hard throttling 会把受害任务的 CPU 配额设置为接近零，实际上相当于停止它们。

这里的 victim tasks 通常是：

```text
低优先级 batch 任务
```

而不是高优先级 serving 任务。

---

##### 为什么 high threshold 要 hard throttling？

因为高阈值意味着：

```text
功率已经接近物理安全边界
```

此时必须快速降功率。

慢慢节流可能来不及。

所以要：

```text
立即停止部分低优先级任务
```

---

#### 2. soft throttling：软节流

原文说：

> Once actual power subsequently drops below the high threshold, soft throttling takes over and progressively increases CPU allocations while attempting to keep usage below the high threshold.

也就是说：

> 一旦实际功率降到 high threshold 以下，soft throttling 接管，并逐步增加 CPU 配额，同时尽量让功率保持在 high threshold 以下。

这很重要。

如果功率刚低于 high threshold 就立即完全恢复所有任务：

```text
功率可能再次冲高
    ↓
再次 hard throttling
    ↓
反复振荡
```

soft throttling 的作用是：

```text
谨慎恢复
平滑功率
避免振荡
```

---

#### 3. low threshold：低阈值

原文说：

> Below the low threshold there is no throttling.

也就是说：

> 低于 low threshold 时，不节流。

low threshold 是恢复正常状态的阈值。

例如：

```text
high threshold = 9.5 MW
low threshold = 8.5 MW
```

当功率：

```text
> 9.5 MW：hard throttling
< 9.5 MW：soft throttling
< 8.5 MW：无节流
```

---

#### 4. low threshold 只在之前达到 high threshold 后激活

原文说：

> The low threshold is active only when the high threshold was reached previously.

也就是说：

> low threshold 只有在之前达到过 high threshold 时才激活。

这避免了过度反应。

例如：

```text
功率短暂超过 low threshold
但没有达到 high threshold
```

此时不会节流。

因为小波动很常见，不必立即干预。

---

#### 5. low threshold timer

原文说：

> After the load has stayed below the low threshold for a certain amount of time, the low threshold timer expires and soft throttling deactivates.

也就是说：

> 当负载持续低于 low threshold 一段时间后，low threshold timer 过期，soft throttling 停用。

这相当于系统确认：

```text
功率已经稳定
可以完全恢复正常
```

---

### 十三、用状态机理解节流过程

可以把整个过程理解成一个状态机。

```text
正常状态
    ↓
功率超过 high threshold
    ↓
hard throttling
    ↓
功率低于 high threshold
    ↓
soft throttling
    ↓
功率持续低于 low threshold
    ↓
恢复正常状态
```

---

#### 状态 1：正常

```text
功率 < low threshold
或从未触发 high threshold
```

系统不节流。

---

#### 状态 2：hard throttling

```text
功率 > high threshold
```

系统立即把 victim tasks 的 CPU 配额降到接近零。

目标是：

```text
快速降功率，保护电力安全
```

---

#### 状态 3：soft throttling

```text
功率 < high threshold
但 low threshold 仍激活
```

系统逐步恢复 CPU 配额。

目标是：

```text
恢复性能
但不让功率再次超过 high threshold
```

---

#### 状态 4：恢复

```text
功率持续低于 low threshold 一段时间
```

系统取消 soft throttling，回到正常状态。

---

### 十四、为什么这种设计能减少振荡？

这是控制系统的经典问题。

如果只有一个阈值：

```text
功率超过阈值 → 节流
功率低于阈值 → 恢复
```

可能出现：

```text
节流 → 功率下降 → 恢复 → 功率上升 → 节流 → 功率下降 → 恢复
```

这就是振荡。

双阈值设计引入：

> hysteresis，迟滞。

也就是：

```text
进入节流状态的条件
和
退出节流状态的条件
不一样
```

这能显著提高稳定性。

---

### 十五、software-defined power 的收益

原文说：

> This approach to software-defined power has been successfully implemented at scale in multiple production clusters, resulting in power oversubscription gains of between 9% and 25%.

也就是说：

> 这种方法已经在多个生产集群大规模实现，带来 9% 到 25% 的电力超额订阅收益。

这个收益非常大。

---

#### 1. 9%–25% 意味着什么？

假设一个数据中心原本只能部署：

```text
10 MW 服务器
```

通过 software-defined power，可以部署：

```text
10.9 MW 到 12.5 MW 服务器
```

这意味着：

- 更多服务器；
- 更多计算容量；
- 更多批处理能力；
- 更高资源利用率；
- 更低单位成本；
- 更少新建电力设施需求。

在超大规模数据中心中，这会节省巨额成本。

---

### 十六、与前面软件定义思想的关系

software-defined power 和前面几节有共同模式。

---

#### 1. 全局遥测

它需要：

- 电表读数；
- 历史功率；
- 电力拓扑；
- 机器归属；
- 任务优先级；
- 风险模型。

这和 SDN 中的全局网络视图类似。

---

#### 2. 中央控制 + 分布式执行

结构是：

```text
中央控制模块 power notifier
    ↓
machine manager
    ↓
各机器 node controller
    ↓
任务级 CPU 节流
```

这和 SDN controller 下发规则到交换机类似。

---

#### 3. QoS 隔离

它保护高优先级服务，节流低优先级批处理。

这和：

- 网络中的带宽 QoS；
- 存储中的 latency-optimized IOPS；
- 服务器中的 LLC QoS；

思想一致。

---

#### 4. 反馈控制

它是一个闭环：

```text
监控功率
    ↓
评估风险
    ↓
决定是否节流
    ↓
下发 CPU 配额
    ↓
功率变化
    ↓
继续监控
```

这和 traffic engineering、congestion control、storage caching 都是控制系统。

---

### 十七、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.5 Software-defined data center
7.5.1 Software-defined power

1. 核心思想：
   - 软件定义思想扩展到数据中心电力管理
   - 通过软件监控、预测和控制功率使用
   - 支持安全的 power oversubscription
   - 提高数据中心容量和效率

2. Power oversubscription：
   - 部署超过数据中心名义供电能力的服务器
   - 前提：
     - 并非所有服务器同时达到峰值
   - 好处：
     - 提高数据中心效率
     - 降低成本
     - 增加可用计算容量

3. 为什么需要 power capping：
   - 如果所有服务器同时峰值：
     - 可能 trip breakers
     - 可能 overload cooling
     - 可能 overload generators
   - 因此需要 power capping：
     - 当关键功耗接近物理限制时
     - 主动降低部分负载

4. 工作负载优先级：
   - high-priority serving tasks：
     - 用户服务
     - 延迟敏感
     - 尽量不节流
   - lower-priority batch workloads：
     - 离线分析
     - 数据移动
     - 可延迟
     - 可节流
   - power capping 主要节流 batch
   - 通常不超额订阅高优先级 serving 所需功率

5. 为什么 oversubscription 可行：
   - workload diversity：
     - 不同负载峰值时间不同
   - significant batch loads：
     - 提供可调节弹性
   - 两者结合可增加可用容量数十个百分点
   - 实际生产收益：
     - 9% 到 25%

6. Software-defined power 的特点：
   - hardware-agnostic power capping system
   - 不依赖特定服务器硬件
   - 使用 Linux kernel CPU bandwidth control
   - 实现 task-level QoS-aware throttling
   - 保持延迟敏感任务低延迟

7. 控制策略：
   - two-threshold：
     - high threshold
     - low threshold
   - randomized unthrottling：
     - 避免被节流任务同时恢复
     - 防止功率再次冲高
   - multiplicative decrease：
     - 超过阈值时按比例快速降低 CPU 配额
   - 目标：
     - 平衡功率安全和性能影响

8. 软件架构模块：

   a. meter watcher：
      - 每秒轮询电表功率读数
      - 将读数传给 power notifier
      - 将读数存入 power history datastore

   b. power history datastore：
      - 存储历史功率信息
      - 用于趋势分析和风险评估

   c. power notifier：
      - 中央控制模块
      - 实现 reactive capping
      - 实现 proactive capping
      - 有功率读数时使用 reactive logic
      - 无功率读数时查询 risk assessor

   d. risk assessor：
      - 使用历史功率信息
      - 评估 breaker trips 风险
      - 在遥测不可用时提供 proactive capping 决策

   e. machine manager：
      - 接收 capping parameters
      - 向各机器 node controller 发 RPC
      - 并发降低机器功耗

   f. power topology datastore：
      - 存储电力输送拓扑
      - 包括 protected power limits
      - 包括某个 power domain 内的机器
      - power domain 规模可从几 MW 到几十 MW

9. 双阈值节流机制：

   a. high threshold：
      - 功率超过 high threshold
      - 启动 hard throttling
      - 将 victim tasks 的 CPU allocation 设为接近零
      - 快速降低功率

   b. soft throttling：
      - 功率降到 high threshold 以下后启动
      - 逐步增加 CPU allocations
      - 尽量保持功率低于 high threshold
      - 防止负载振荡

   c. low threshold：
      - 功率低于 low threshold 时无节流
      - low threshold 只在之前达到 high threshold 后激活
      - 短暂超过 low threshold 但未达 high threshold：
        - 不会触发节流
      - 功率持续低于 low threshold 一段时间后：
        - low threshold timer 过期
        - soft throttling 停用

10. 控制状态机：
   正常
     → 功率超过 high threshold
     → hard throttling
     → 功率低于 high threshold
     → soft throttling
     → 功率持续低于 low threshold
     → 恢复正常

11. 为什么双阈值有效：
   - 提供 hysteresis，迟滞
   - 避免频繁 throttle / unthrottle
   - 避免功率振荡
   - 在安全和性能之间取得平衡

12. 核心逻辑：
   电力基础设施昂贵
     → 按最坏峰值设计利用率低
     → power oversubscription 提高利用率
     → 但需要防止同时峰值造成事故
     → software-defined power 用遥测和控制策略安全节流
     → 优先节流低优先级 batch
     → 保护高优先级 serving
     → 提高数据中心容量 9%–25%
```

---

### 十八、一句话总结这一节

> 7.5.1 说明：software-defined power 通过全局功率遥测、电力拓扑感知、双阈值控制策略和任务级 QoS 节流，让数据中心能够安全地进行电力超额订阅，在保护高优先级服务的同时，用低优先级批处理任务吸收功率波动，从而显著提高数据中心容量和成本效率。


**专栏导航**

- ← 上一篇：[7.4.2 Transparent SSD caching、7.4.3 Trading data center space between compute and storage、7.4.4 Other software-managed hardware optimizations](/posts/7-4-2-transparent-ssd-caching-7-4-3-trading-data-center-space-between-compute-and-storage-7-4-4-other-software-managed-hardware-optimizations/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.5.2 Software-defined fleet →](/posts/7-5-2-software-defined-fleet/)
