---
title: "7.5.2 Software-defined fleet"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-29
description: "《The Data Center as a Computer》AI 导读专栏正文：7.5.2 Software-defined fleet。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.5.2 Software-defined fleet。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.5.2 Software-defined fleet

下面把 **7.5.2 Software-defined fleet** 作为一个独立小节来深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这一节虽然短，但它把前面所有 software-defined infrastructure 的思想汇总到一个更高层的问题上：

> 如何自动化管理整个服务器机群，也就是 fleet 的容量、放置和伸缩。

如果说前面几节分别讲的是：

- 软件定义服务器；
- 软件定义加速器；
- 软件定义网络；
- 软件定义存储；
- 软件定义电力；

那么 7.5.2 讲的是：

> 软件定义整个机群。

---

### 7.5.2 Software-defined fleet 深入理解

#### 一、什么是 software-defined fleet？

原文没有给一个非常正式的定义，但从内容可以概括为：

> software-defined fleet 是指通过软件系统自动管理整个服务器机群的容量、集群选择、任务放置和资源伸缩，使机群像一台可编程、可自动调整的大计算机。

这里的 fleet 指：

> Google 的所有服务器机群，包括多个数据中心、多个集群、多种硬件平台。

software-defined fleet 关心的不只是：

```text
某个任务现在能不能跑
```

而是：

```text
整个生产系统长期是否有足够容量
任务应该放在哪个集群
任务应该分配多少资源
流量变化时如何自动伸缩
硬件故障时如何保持冗余
```

---

### 二、为什么需要自动化容量管理？

原文说：

> Software-defined infrastructure provides the convenience of automating capacity management.

也就是说：

> 软件定义基础设施带来了自动化容量管理的便利。

在超大规模生产环境中，容量管理极其复杂。

---

#### 1. 服务数量巨大

Google 有非常多生产服务：

- Search；
- Gmail；
- YouTube；
- Ads；
- Photos；
- Drive；
- Maps；
- Cloud 服务；
- 内部基础设施；
- ML 训练和推理服务。

每个服务都需要：

- CPU；
- memory；
- storage；
- network；
- accelerator；
- 冗余；
- SLO 保障。

---

#### 2. 流量和需求不断变化

服务需求不是静态的：

- 用户增长；
- 产品功能增加；
- 流量有昼夜周期；
- 有节假日高峰；
- 有突发事件；
- 有新模型上线；
- 有数据量增长；
- 有硬件退役；
- 有数据中心容量变化。

如果靠人工判断：

```text
哪个服务需要扩容？
扩多少？
放在哪个集群？
需要多少冗余？
什么时候采购机器？
```

几乎不可能做好。

---

#### 3. 容量过多或过少都有代价

容量管理本质上是在两类风险之间平衡。

---

##### 容量过少

会导致：

- 服务延迟升高；
- SLO 违约；
- 请求失败；
- 用户体验下降；
- 故障恢复困难；
- 没有冗余应对机器故障。

---

##### 容量过多

会导致：

- 机器利用率低；
- 成本高；
- 资源闲置；
- 数据中心空间浪费；
- 电力浪费；
- 冷却浪费。

因此容量管理目标是：

```text
在正确的时间
把正确数量的资源
放到正确的位置
给正确的服务
```

---

### 三、Autocap：长期容量管理

原文说：

> Autocap is a comprehensive internal tool that automates capacity management for production services by taking into account long-term planning and upcoming growth needs, and redundancy targets, N + 1 or N + 2.

也就是说：

> Autocap 是一个综合内部工具，它通过考虑长期规划、未来增长需求和冗余目标，自动管理生产服务的容量。

Autocap 更偏长期和宏观。

---

#### 1. Autocap 考虑长期规划

长期规划可能包括：

- 未来几个月的用户增长；
- 新产品发布；
- 新模型上线；
- 数据量增长；
- 服务迁移；
- 数据中心容量变化；
- 硬件采购周期；
- 机器退役计划；
- 区域合规要求。

它不是只看当前负载，而是看：

```text
未来需要多少容量？
```

---

#### 2. Autocap 考虑 upcoming growth needs

也就是即将到来的增长需求。

例如：

```text
某服务当前需要 10,000 CPU
预计下季度增长 20%
```

那么 Autocap 需要提前准备：

```text
12,000 CPU
再加冗余
```

而不是等到流量已经上涨、服务已经过载才扩容。

---

#### 3. Autocap 考虑冗余目标：N + 1 或 N + 2

原文提到：

> redundancy targets, N + 1 or N + 2.

这是容量规划中常见的冗余模型。

---

##### N + 1 冗余

假设服务正常需要：

```text
N 份资源
```

为了容忍一份资源故障，额外准备：

```text
1 份资源
```

总容量：

```text
N + 1
```

例如：

```text
正常需要 10 台机器
N + 1 = 11 台机器
```

如果一台机器故障：

```text
剩下 10 台仍可支撑服务
```

---

##### N + 2 冗余

如果希望容忍两个故障，或者需要更高安全边界：

```text
N + 2
```

例如：

```text
正常需要 10 台机器
N + 2 = 12 台机器
```

这可以应对：

- 两台机器同时故障；
- 维护期间一台机器下线；
- 故障恢复期间另一台机器故障；
- 更保守的可用性目标。

---

##### N + 1 / N + 2 的权衡

|冗余策略|优点|缺点|
| ----------| ------------------------| ------------------|
|N + 1|成本较低|容忍故障能力有限|
|N + 2|更安全、更适合关键服务|成本更高|

关键服务可能用：

```text
N + 2
```

普通服务可能用：

```text
N + 1
```

---

#### 4. Autocap 自动化集群选择和作业放置

原文说：

> With Autocap, cluster selection and job placement are automated.

也就是说：

> 使用 Autocap 后，集群选择和作业放置都可以自动化。

---

##### cluster selection，集群选择

一个服务可能可以运行在多个集群中。

Autocap 会考虑：

- 哪个集群有容量；
- 哪个集群硬件适合；
- 哪个集群网络更近；
- 哪个集群成本更低；
- 哪个集群有加速器；
- 哪个集群满足数据本地化要求；
- 哪个集群有足够冗余；
- 哪个集群电力和冷却有余量。

---

##### job placement，作业放置

作业放置决定：

```text
具体任务放在哪些机器上
```

它要考虑：

- CPU 剩余；
- memory 剩余；
- 网络带宽；
- 存储位置；
- 加速器可用性；
- 故障域；
- 反亲和性；
- QoS；
- 能耗；
- 热点避免。

这部分和前面的：

- platform-aware scheduling；
- network-aware scheduling；

密切相关。

---

### 四、Autopilot：短期实时伸缩

原文说：

> On the other hand, another internal tool, Autopilot, makes short-term adjustments by using the current CPU utilization to scale jobs in real time.

也就是说：

> 另一个内部工具 Autopilot 通过当前 CPU 利用率实时扩展作业，进行短期调整。

Autopilot 更偏短期和实时。

---

#### 1. Autocap 与 Autopilot 的区别

可以先记住这个对比：

|工具|时间尺度|主要问题|
| -----------| ----------| ----------------------------------------------|
|Autocap|长期|需要多少总容量？放在哪个集群？冗余多少？|
|Autopilot|短期|当前任务应该扩多少？缩多少？资源限制设多少？|

Autocap 像：

> 城市长期规划，决定修多少路、建多少电厂。

Autopilot 像：

> 实时交通调度，根据当前车流调整信号灯和车道。

---

#### 2. horizontal scaling，水平扩展

原文说：

> It can adjust the number of concurrent tasks in a job, horizontal scaling.

horizontal scaling 指：

> 改变并发任务数量。

例如一个服务当前有：

```text
100 个副本
```

流量上升后，Autopilot 可能扩到：

```text
150 个副本
```

流量下降后，再缩到：

```text
80 个副本
```

这就是水平扩展。

---

##### 水平扩展的特点

优点：

- 适合无状态服务；
- 容易分摊负载；
- 提高可用性；
- 可以跨故障域分布。

挑战：

- 需要调度资源；
- 新副本启动需要时间；
- 可能增加网络通信；
- 有状态服务扩展更复杂。

---

#### 3. vertical scaling，垂直扩展

原文说：

> and the CPU/memory limits for individual tasks, vertical scaling.

vertical scaling 指：

> 改变单个任务的 CPU/memory limits。

例如某个任务原来限制为：

```text
4 CPU
16 GB memory
```

Autopilot 根据历史使用和当前利用率，调整为：

```text
6 CPU
24 GB memory
```

或者在负载下降时调低：

```text
2 CPU
8 GB memory
```

---

##### 垂直扩展的特点

优点：

- 不需要增加任务数量；
- 对单任务资源利用更精细；
- 适合批处理任务；
- 适合资源需求波动但副本数不宜频繁变化的服务。

挑战：

- 单机资源有限；
- 可能需要重启或迁移；
- 内存限制过紧可能导致 OOM；
- CPU 限制过紧可能导致延迟升高。

---

### 五、Autopilot 如何使用当前 CPU utilization？

原文说：

> using the current CPU utilization to scale jobs in real time.

也就是说：

> Autopilot 使用当前 CPU 利用率实时伸缩作业。

例如：

```text
某服务副本 CPU 利用率持续 85%
```

可能说明资源紧张。

Autopilot 可能：

- 增加副本数；
- 或提高单任务 CPU limit。

再例如：

```text
某服务副本 CPU 利用率长期 15%
```

可能说明资源过多。

Autopilot 可能：

- 减少副本数；
- 或降低单任务 CPU limit。

---

#### 1. 为什么 CPU utilization 是重要信号？

CPU utilization 可以反映：

- 服务是否资源紧张；
- 是否有扩容需求；
- 是否过度配置；
- 是否负载下降；
- 是否任务资源请求不合理。

但它不是唯一信号。

真实系统还可能看：

- memory usage；
- latency；
- request rate；
- queue length；
- error rate；
- cache miss；
- network bandwidth；
- disk I/O；
- accelerator utilization。

不过原文这里强调的是：

> Autopilot 用当前 CPU utilization 做实时伸缩。

---

### 六、ML 与启发式结合

原文说：

> Both services rely on machine learning algorithms that analyze historical data about prior executions of a job, in combination with finely-tuned heuristics.

也就是说：

> Autocap 和 Autopilot 都依赖机器学习算法分析作业历史执行数据，并结合精细调优的启发式规则。

---

#### 1. 为什么用机器学习？

因为很多资源使用模式复杂。

ML 可以帮助发现：

- 周期性流量；
- 每日高峰；
- 每周模式；
- 节假日效应；
- 历史增长趋势；
- 任务资源使用分布；
- 异常峰值；
- 任务运行时间变化；
- 内存使用增长；
- CPU 使用相关性。

例如：

```text
某服务每天 18:00–23:00 流量上升
```

ML 可以学到这个模式，并提前或及时扩容。

---

#### 2. 为什么还需要启发式？

ML 不是万能的。

它可能遇到：

- 新服务没有历史数据；
- 突发事件没有先例；
- 数据异常；
- 模型预测偏差；
- 极端流量；
- correlated failures；
- 产品活动导致流量异常。

因此需要启发式规则保证安全。

例如：

```text
最小副本数不能低于 X
最大资源限制不能超过 Y
扩容必须保留安全余量
缩容必须缓慢进行
关键服务必须保留 N + 2 冗余
内存 limit 不能低于历史 P99 使用量
```

这就是：

> ML 提供智能预测，启发式提供安全边界。

---

### 七、responsiveness 与 efficiency 的平衡

原文说：

> These features help maintain a balance between responsiveness and efficiency, providing optimal capacity management for production services.

也就是说：

> 这些特性帮助在响应性和效率之间保持平衡，为生产服务提供最优容量管理。

---

#### 1. responsiveness，响应性

响应性指：

> 系统能否快速应对负载变化。

如果响应性不足：

```text
流量突然上升
    ↓
资源不足
    ↓
延迟升高
    ↓
用户受影响
```

因此需要：

- 快速扩容；
- 足够冗余；
- 实时资源调整；
- 预测性容量准备。

---

#### 2. efficiency，效率

效率指：

> 资源是否被充分利用。

如果只追求响应性，可能会：

```text
每个服务都预留大量资源
```

这会导致：

- 利用率低；
- 成本高；
- 资源碎片；
- 电力和空间浪费。

因此需要：

- 精确资源请求；
- 自动缩容；
- 混部低优先级任务；
- 动态调整 limits；
- 长期容量规划。

---

#### 3. 最优容量管理

最优不是：

```text
资源最多
```

也不是：

```text
成本最低
```

而是：

```text
在满足 SLO、冗余和增长需求的前提下，成本最低、利用率最高。
```

---

### 八、Autocap 和 Autopilot 如何协同？

可以把它们看成两个不同时间尺度的容量控制系统。

---

#### 1. Autocap：战略层

Autocap 决定：

```text
总容量池怎么规划
```

例如：

- 某服务下季度需要多少 CPU；
- 应该部署在哪些集群；
- 需要多少 N + 2 冗余；
- 是否需要新硬件；
- 是否需要跨 region 分布；
- 哪些服务可以共享容量池。

---

#### 2. Autopilot：战术层

Autopilot 决定：

```text
当前任务如何伸缩
```

例如：

- 现在增加多少副本；
- 现在降低多少 CPU limit；
- 某个 batch job 是否需要更多内存；
- 某个服务是否可以缩容；
- 当前流量下降后如何回收资源。

---

#### 3. 两者关系

```text
Autocap：
长期准备足够容量
    ↓
Autopilot：
短期实时使用这些容量
```

如果没有 Autocap：

```text
Autopilot 想扩容，但集群没有足够容量
```

如果没有 Autopilot：

```text
Autocap 准备了容量，但具体任务资源分配不精细，利用率低
```

两者结合，才能实现：

```text
长期容量充足
短期伸缩灵活
整体利用率高
```

---

### 九、与前面章节的关系

7.5.2 是第 7 章 software-defined infrastructure 的一个汇总。

---

#### 1. 与 software-defined servers 的关系

software-defined servers 关注：

```text
单台服务器或平台如何适配工作负载
```

software-defined fleet 关注：

```text
整个机群如何自动规划、放置和伸缩
```

---

#### 2. 与 platform-aware scheduling 的关系

platform-aware scheduling 是：

```text
把任务放到最合适平台
```

Autocap / Autopilot 更进一步：

```text
不仅选择平台，还决定容量和伸缩
```

---

#### 3. 与 network-aware scheduling 的关系

network-aware scheduling 考虑：

```text
网络热点和带宽
```

fleet-level capacity management 也需要考虑：

```text
哪个集群有网络容量
哪个区域有带宽
哪个数据中心适合放某类任务
```

---

#### 4. 与 software-defined power 的关系

software-defined power 利用低优先级 batch 做电力弹性。

software-defined fleet 也需要知道：

```text
哪些容量可以弹性使用
哪些服务必须保障
哪些任务可以被节流或迁移
```

---

### 十、一个完整例子

假设有一个视频推荐服务。

---

#### 1. Autocap 做长期规划

Autocap 分析：

```text
过去 12 个月流量增长 30%
预计下季度新增用户 10%
视频推荐模型更复杂，CPU 需求增加
需要 N + 2 冗余
```

于是决定：

```text
在 Region A 和 Region B 各预留一定容量
选择支持新 CPU 指令集的集群
为关键服务保留冗余
```

---

#### 2. Autopilot 做实时伸缩

某一天晚上流量高峰：

```text
CPU utilization 从 55% 上升到 82%
```

Autopilot 判断需要扩容：

```text
副本数从 1,000 增加到 1,400
```

凌晨流量下降：

```text
CPU utilization 降到 25%
```

Autopilot 缩容：

```text
副本数降回 900
```

---

#### 3. 结果

这样系统既：

- 保证高峰期用户体验；
- 又避免低峰期资源浪费；
- 还保留故障冗余；
- 并支持长期增长。

---

### 十一、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.5.2 Software-defined fleet

1. 核心思想：
   - software-defined infrastructure 扩展到整个服务器 fleet
   - 通过软件自动化管理：
     - 容量
     - 集群选择
     - 作业放置
     - 资源伸缩
     - 冗余目标
   - 目标：
     - 让 fleet 像一台可编程、可自动调整的大计算机

2. 为什么需要自动化容量管理：
   - 生产服务数量巨大
   - 流量和需求持续变化
   - 人工管理不可扩展
   - 容量过少：
     - SLO 违约
     - 延迟升高
     - 故障恢复困难
   - 容量过多：
     - 利用率低
     - 成本高
     - 电力和空间浪费

3. Autocap：长期容量管理：
   - 综合内部工具
   - 自动化生产服务容量管理
   - 考虑：
     - long-term planning
     - upcoming growth needs
     - redundancy targets：N + 1 或 N + 2
   - 自动化：
     - cluster selection
     - job placement

4. N + 1 / N + 2 冗余：
   - N：
     - 正常运行所需资源数量
   - N + 1：
     - 额外一份冗余
     - 可容忍一份资源故障
   - N + 2：
     - 额外两份冗余
     - 更高可用性
     - 更高成本
   - 关键服务通常使用更高冗余目标

5. Autopilot：短期实时伸缩：
   - 使用当前 CPU utilization 实时 scale jobs
   - 进行 short-term adjustments
   - 可调整两类资源：

   a. horizontal scaling：
      - 调整 job 中 concurrent tasks 数量
      - 例如增加或减少副本数

   b. vertical scaling：
      - 调整单个 task 的 CPU/memory limits
      - 例如提高或降低单任务资源配额

6. Autocap vs Autopilot：
   - Autocap：
     - 长期
     - 战略层
     - 总容量规划
     - 集群选择
     - 冗余目标
   - Autopilot：
     - 短期
     - 战术层
     - 实时伸缩
     - 单任务资源调整
   - 两者协同：
     - Autocap 准备长期容量
     - Autopilot 实时高效使用容量

7. ML 与启发式结合：
   - Autocap 和 Autopilot 都使用 machine learning
   - ML 分析 job 历史执行数据
   - 用于发现：
     - 周期性流量
     - 增长趋势
     - 资源使用模式
     - 异常行为
   - 同时结合 finely-tuned heuristics
   - 启发式用于：
     - 安全边界
     - 最小/最大资源限制
     - SLO 保护
     - 稳定性
     - 冗余保障

8. responsiveness vs efficiency：
   - responsiveness：
     - 快速响应流量变化
     - 避免资源不足
     - 保持低延迟和可用性
   - efficiency：
     - 避免过度配置
     - 提高资源利用率
     - 降低成本
   - 最优容量管理：
     - 在满足 SLO、冗余和增长需求的前提下
     - 实现成本和利用率平衡

9. 与前面内容的关系：
   - software-defined servers：
     - 优化单机/平台适配
   - platform-aware scheduling：
     - 把任务放到合适平台
   - network-aware scheduling：
     - 考虑网络热点和带宽
   - software-defined power：
     - 利用低优先级负载做电力弹性
   - software-defined fleet：
     - 在更高层自动化整个机群容量和伸缩

10. 核心逻辑：
   fleet 规模和复杂性巨大
     → 需要自动化容量管理
     → Autocap 做长期容量规划和集群选择
     → Autopilot 做短期实时伸缩
     → ML 分析历史数据
     → heuristics 保证安全和稳定
     → 在响应性和效率之间取得平衡
```

---

### 十二、一句话总结这一节

> 7.5.2 说明：software-defined fleet 通过 Autocap 和 Autopilot 等系统，把长期容量规划、集群选择、作业放置、冗余管理和实时资源伸缩自动化，使整个服务器机群能够在保证服务质量和冗余的前提下，实现更高效率和更低成本。


**专栏导航**

- ← 上一篇：[7.5 Software-defined data center 中的 7.5.1 Software-defined power](/posts/7-5-software-defined-data-center-7-5-1-software-defined-power/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.6 Self-driving systems →](/posts/7-6-self-driving-systems/)
