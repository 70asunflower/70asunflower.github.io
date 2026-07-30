---
title: "7.6 Self-driving systems"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-29
description: "《The Data Center as a Computer》AI 导读专栏正文：7.6 Self-driving systems。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.6 Self-driving systems。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.6 Self-driving systems

下面把 **7.6 Self-driving systems** 作为一个独立小节来深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这一节是第 7 章的收束部分。前面几节分别讲了：

- software-defined servers；
- software-defined accelerators；
- software-defined networks；
- software-defined storage；
- software-defined power；
- software-defined fleet。

而 7.6 提出一个更高层的方向：

> 不仅要用软件定义基础设施，还要用机器学习让这些系统具备一定程度的自主设计、自主优化和自主恢复能力。

这就是：

> self-driving systems，自驾式系统。

---

### 7.6 Self-driving systems 深入理解

#### 一、核心命题：ML 既是被服务的对象，也是设计系统的工具

原文第一句非常关键：

> Machine learning is driving computing demand, and systems are being redesigned for ML workloads.

也就是说：

> 机器学习正在推动计算需求，系统正在为 ML 工作负载重新设计。

这对应前面章节，尤其是：

- 加速器；
- TPU；
- 高带宽互联；
- ML 训练网络；
- 大规模存储；
- 电力和冷却压力。

但原文马上转折：

> But machine learning can also be used to better design systems.

也就是说：

> ML 不仅可以作为工作负载运行在系统上，也可以反过来帮助设计、优化和运行系统。

可以概括成两个方向：

```text
Systems for ML：
为 ML 工作负载设计更好的系统。

ML for Systems：
用 ML 把系统设计、优化和运维做得更好。
```

7.6 主要讲的是后者：

> ML for Systems。

---

### 二、什么是 self-driving systems？

原文标题是：

> Self-driving systems。

这个词可以类比自动驾驶汽车。

自动驾驶汽车通常有：

```text
传感器
    ↓
感知环境
    ↓
预测未来状态
    ↓
做出决策
    ↓
控制车辆
    ↓
持续反馈
```

self-driving systems 在数据中心中也是类似：

```text
遥测数据 telemetry
    ↓
ML 分析系统状态
    ↓
预测性能、故障、拥塞、功耗
    ↓
生成优化策略
    ↓
调整硬件、调度、网络、存储、功率
    ↓
观察结果并继续学习
```

也就是说：

> self-driving systems 是能够基于数据和 ML 模型，自动感知、分析、决策和优化的大型系统。

它不是完全不需要人，而是：

> 把大量复杂、重复、高维、实时的优化工作交给软件和数据驱动模型。

---

### 三、为什么 self-driving systems 与 software-defined infrastructure 高度相关？

第 7 章的核心是 software-defined infrastructure。

软件定义基础设施已经提供了：

- 可编程硬件；
- 集中控制平面；
- 全局遥测；
- 统一抽象；
- 自动化策略；
- 跨层优化接口。

这为 ML 优化系统提供了基础。

如果没有软件定义基础设施，ML 很难直接控制系统，因为：

- 硬件不可编程；
- 配置静态；
- 遥测不足；
- 控制接口不统一；
- 全局视图缺失；
- 策略下发困难。

而 software-defined infrastructure 让系统变成：

```text
可观测
    +
可编程
    +
可控制
    +
可自动化
```

这就为 self-driving systems 创造了条件。

可以这样理解：

```text
Software-defined infrastructure：
让系统可以被软件控制。

Self-driving systems：
让软件控制本身由 ML 自动优化。
```

---

### 四、原文给出的四类代表性例子

原文列举了 ML for Systems 的几个方向：

1. 自动识别代码中的加速目标；
2. 用 ML 做芯片和 PCB 生成式设计；
3. 用 ML 优化节点级控制系统；
4. 用 ML 优化大规模分布式系统。

下面逐个展开。

---

### 五、例子 1：用 ML 自动识别适合加速的代码

原文说：

> Machine learning can automate the identification of suitable accelerators for large codebases by analyzing code patterns, automatically pinpointing potential acceleration targets, and suggesting optimal hardware/software co-design strategies.

也就是说：

> ML 可以通过分析大型代码库中的代码模式，自动识别适合加速的部分，并建议最优的软硬件协同设计策略。

---

#### 1. 大型代码库的加速难题

在大型代码库中，可能存在数百万行甚至更多代码。

人工寻找加速目标很困难：

- 代码量太大；
- 热点不明显；
- 依赖关系复杂；
- 不同模块行为不同；
- 加速器选择很多；
- 软硬件协同成本高。

传统方法通常依赖：

- profiling；
- 工程师经验；
- 手动重写；
- 手动选择库；
- 手动设计加速器。

但这很慢，而且难以覆盖整个代码库。

---

#### 2. ML 可以做什么？

ML 可以分析：

- 代码模式；
- 控制流；
- 数据流；
- 循环结构；
- 内存访问模式；
- 并行性；
- 热点函数；
- 算子类型；
- 计算密度；
- 数据重用；
- 历史性能数据。

然后识别：

```text
哪些代码适合 GPU
哪些代码适合 TPU
哪些代码适合 FPGA
哪些代码适合定制 ASIC
哪些代码适合向量化
哪些代码适合专用库
哪些代码值得软硬件协同重构
```

---

#### 3. 例子

例如 ML 分析代码后发现：

```text
某模块大量进行矩阵乘法
```

它可能建议：

```text
使用 TPU / GPU
或使用高度优化的矩阵库
```

再例如：

```text
某模块频繁做正则匹配、压缩、加密
```

它可能建议：

```text
使用专用加速器或 SmartNIC
```

再例如：

```text
某模块内存访问不规则，但计算密集
```

它可能建议：

```text
重新设计数据结构或引入 prefetching
```

---

#### 4. 价值

原文说：

> This accelerates development and fosters innovative interfaces and ecosystems.

也就是说：

> 这可以加速开发，并促进创新接口和生态系统。

价值在于：

- 降低加速器使用门槛；
- 自动发现优化机会；
- 减少人工分析；
- 推动软硬件协同；
- 形成新的编程接口；
- 帮助大型代码库持续演进。

---

### 六、例子 2：ML 驱动的芯片和 PCB 生成式设计

原文说：

> ML-driven generative design can be used to automate chip and PCB layouts, optimizing for performance, power efficiency, and reliability while accommodating heterogeneity.

也就是说：

> ML 驱动的生成式设计可以用于自动化芯片和 PCB 布局，在容纳异构性的同时，优化性能、功耗效率和可靠性。

---

#### 1. 芯片和 PCB 设计为什么难？

芯片设计和 PCB 设计都是超复杂优化问题。

例如芯片布局要考虑：

- 模块位置；
- 线长；
- 拥塞；
- 时序；
- 功耗；
- 热分布；
- 信号完整性；
- 电源网络；
- 制造约束；
- 可靠性；
- 面积；
- 异构模块摆放。

PCB 设计也要考虑：

- 器件布局；
- 布线路径；
- 电源完整性；
- 信号完整性；
- 散热；
- 电磁干扰；
- 制造成本；
- 可维修性。

传统设计流程：

```text
工程师经验
    +
EDA 工具
    +
多轮迭代
    +
人工调整
```

往往耗时很长。

---

#### 2. ML 如何帮助？

ML 可以在巨大设计空间中搜索：

```text
哪种布局更好
哪种布线更优
哪种模块摆放能降低功耗
哪种设计能改善热分布
哪种结构更适合异构芯片
```

它可以把设计问题变成优化问题：

```text
输入：
模块列表
连接关系
约束条件
性能目标
功耗目标
面积目标
可靠性目标

输出：
候选布局 / 布线 / 设计参数
```

---

#### 3. 原文的设想

原文说：

> It’s conceivable that in the future, a dozen people could design a chip in three months that today takes a hundred people a year to finish, while also optimizing to a better design.

也就是说：

> 未来可能十几个人用三个月就能设计出一颗今天需要一百人一年才能完成的芯片，而且设计质量更好。

这说明 ML 不只是加速现有流程，还可能改变设计流程本身。

---

#### 4. 与 7.2 的关系

7.2 讲 H2O-NAS：

> 用 ML 自动搜索适合硬件的模型架构。

7.6 这里进一步：

> 用 ML 自动设计硬件本身。

可以形成闭环：

```text
ML 设计更适合硬件的模型
    +
ML 设计更适合模型的硬件
```

这就是更深层次的软硬件协同。

---

### 七、例子 3：用 ML 优化节点级控制系统

原文说：

> ML can also be used in most control systems at the node level.

也就是说：

> ML 可以用于节点级的大多数控制系统。

node level 指单台服务器或单个节点。

---

#### 1. 节点级控制有哪些旋钮？

一台服务器有很多可调参数，例如：

- CPU 频率；
- turbo boost；
- power state；
- hardware prefetcher；
- LLC 分配；
- memory bandwidth 控制；
- NUMA 绑定；
- hugepage 策略；
- 内存层级放置；
- 风扇控制；
- QoS 等级；
- 加速器分配；
- 功耗上限。

这些参数组合非常多。

---

#### 2. 为什么 ML 有用？

因为不同工作负载对这些参数敏感度不同。

例如：

- 某应用对 cache 分配敏感；
- 某应用对内存带宽敏感；
- 某应用对频率敏感；
- 某应用对 prefetcher 敏感；
- 某应用对 NUMA 距离敏感；
- 某应用对功耗限制敏感。

人工为每个应用调参不现实。

ML 可以：

```text
分析系统级 telemetry
    ↓
识别工作负载特征
    ↓
预测参数调整效果
    ↓
动态调整参数
    ↓
优化 QoS、效率和利用率
```

---

#### 3. 与前面章节的联系

这直接对应 7.1 中的 software-defined servers。

例如：

- Limoncello 动态调整 CPU 配置；
- TCMalloc 优化 hugepage；
- QoS 控制 LLC 和内存带宽；
- tiered memory 管理热冷数据。

ML 可以让这些优化更自动化：

```text
从人工规则驱动
    ↓
数据驱动
    ↓
自主学习驱动
```

---

#### 4. 原文的概括

原文说：

> ML models can analyze system-wide telemetry data to dynamically adjust various parameters and optimize resource allocation based on real-time workload characteristics.

也就是说：

> ML 模型可以分析系统级遥测数据，根据实时工作负载特征动态调整各种参数并优化资源分配。

结果是：

> enhanced quality of service, efficiency, and resource utilization across a wide range of vendors, platforms, jobs, clusters, and applications.

也就是在广泛厂商、平台、作业、集群和应用中提升：

- QoS；
- 效率；
- 资源利用率。

---

### 八、例子 4：用 ML 优化大规模分布式系统

原文说：

> ML can also be used in large-scale distributed systems.

也就是说：

> ML 也可以用于大规模分布式系统。

这比节点级更宏观。

---

#### 1. 分布式系统的复杂性

大规模分布式系统包括：

- 网络；
- 存储；
- 计算集群；
- 加速器集群；
- 电力；
- 冷却；
- 跨数据中心 WAN；
- 边缘网络。

这些系统之间存在复杂交互。

例如：

```text
调度一个 ML 训练任务
    ↓
影响网络流量
    ↓
影响存储读取
    ↓
影响电力负载
    ↓
影响冷却需求
    ↓
影响其他任务延迟
```

传统规则很难捕捉所有交互。

---

#### 2. ML 可以建模复杂交互

原文说：

> ML-based approaches can model intricate interactions within disaggregated systems like networks, storage, and clusters.

也就是说：

> 基于 ML 的方法可以建模网络、存储和集群等解耦系统中的复杂交互。

ML 可以帮助：

- 预测网络拥塞；
- 预测存储热点；
- 预测任务运行时间；
- 预测尾延迟；
- 预测故障；
- 预测功耗；
- 预测冷却需求；
- 预测资源竞争；
- 优化全局调度。

---

#### 3. 原文提到的优化方向

原文举了几个方向。

---

##### 优化 power/cooling distribution

也就是：

> 优化电力和冷却分配。

例如：

- 把高功耗任务分配到冷却余量充足的数据中心；
- 根据温度预测调整任务；
- 在电力峰值时降低低优先级负载；
- 利用热惯性做短期功率调度。

这和 7.5.1 software-defined power 相关。

---

##### intelligently scheduling tasks across clusters

也就是：

> 跨集群智能调度任务。

例如：

- 把任务调度到最合适集群；
- 考虑硬件、网络、存储、电力、成本；
- 避免热点；
- 提高利用率；
- 保护高优先级服务。

这和：

- platform-aware scheduling；
- network-aware scheduling；
- software-defined fleet；

都密切相关。

---

##### minimizing tail latency

也就是：

> 最小化尾延迟。

尾延迟是大规模服务中的关键问题。

例如：

```text
平均延迟很好
但 P99 或 P99.9 延迟很差
```

ML 可以帮助识别：

- 哪些请求慢；
- 哪些节点异常；
- 哪些资源竞争导致延迟；
- 哪些调度决策增加尾延迟；
- 哪些重试策略更有效。

---

#### 4. 最终目标

原文说：

> ML can enable efficient scaling, fault tolerance, and overall performance improvement in these complex environments.

也就是说：

> ML 可以帮助这些复杂环境实现高效扩展、容错和整体性能提升。

具体包括：

- 更高效扩展；
- 更快故障恢复；
- 更准确异常检测；
- 更好资源利用；
- 更低尾延迟；
- 更低能耗；
- 更高可用性。

---

### 九、self-driving systems 的统一模式

虽然原文举了四个不同例子，但它们背后有统一模式。

---

#### 1. 感知

系统收集大量 telemetry：

- CPU 利用率；
- cache miss；
- TLB miss；
- 内存带宽；
- 网络流量；
- 链路拥塞；
- 存储 IOPS；
- 延迟；
- 功耗；
- 温度；
- 故障事件；
- 任务运行历史；
- 代码特征；
- 硬件配置。

---

#### 2. 分析

ML 模型分析：

- 当前状态；
- 历史模式；
- 异常；
- 趋势；
- 因果关系；
- 工作负载特征；
- 资源瓶颈；
- 未来需求。

---

#### 3. 决策

系统生成决策：

- 调整 CPU 配置；
- 改变调度策略；
- 迁移任务；
- 改变网络路径；
- 调整带宽配额；
- 改变存储放置；
- 降低低优先级负载；
- 推荐加速器；
- 生成芯片布局。

---

#### 4. 执行

通过软件定义基础设施执行：

- cluster manager；
- SDN controller；
- storage system；
- node controller；
- power capping system；
- EDA 工具；
- 编译器；
- runtime；
- allocator。

---

#### 5. 反馈

系统观察结果：

```text
性能是否改善？
延迟是否下降？
功耗是否降低？
利用率是否提高？
是否引入新问题？
```

然后继续学习。

---

### 十、为什么 ML 对未来 WSC 很重要？

原文最后说：

> While these examples show the promise of ML, we are still in the early days of using machine learning for systems.

也就是说：

> 虽然这些例子展示了 ML 的潜力，但用 ML 优化系统仍处于早期阶段。

但它很重要，因为未来 WSC 面临的挑战越来越复杂。

---

#### 1. 系统规模太大

未来 WSC 可能有：

- 数百万台服务器；
- 大量加速器；
- 复杂网络；
- 多层存储；
- 跨洲数据中心；
- 动态工作负载。

人工规则难以覆盖。

---

#### 2. 异构性太强

硬件包括：

- 多代 CPU；
- 不同 GPU；
- TPU；
- FPGA；
- SmartNIC；
- CXL memory；
- SMR HDD；
- SSD；
- 光交换；
- 不同厂商设备。

软件定义基础设施已经抽象了这些异构性，但优化空间巨大。

ML 可以帮助在巨大异构空间中找到更优策略。

---

#### 3. 工作负载变化太快

负载可能因为：

- 用户行为；
- 产品发布；
- 模型训练；
- 突发事件；
- 节假日；
- 攻击；
- 故障；

而快速变化。

静态规则很难及时适应。

---

#### 4. 优化目标太多

WSC 优化目标包括：

- 性能；
- 延迟；
- 尾延迟；
- 吞吐；
- 成本；
- 能耗；
- 可靠性；
- 可用性；
- 安全；
- 合规；
- 可维护性；
- 硬件寿命。

这些目标经常冲突。

ML 可以帮助在多目标之间找平衡。

---

### 十一、但为什么仍处于早期？

原文强调：

> we are still in the early days.

这提醒我们不要过度神化 ML。

---

#### 1. 系统控制需要安全性

数据中心是关键基础设施。

错误决策可能导致：

- 服务中断；
- 数据丢失；
- 网络拥塞；
- 功率事故；
- 尾延迟飙升；
- 资源浪费。

因此 ML 决策必须有：

- guardrails；
- fallback；
- 人工审核；
- 安全边界；
- 回滚机制。

---

#### 2. 在线实验有风险

ML 通常需要试错。

但在生产系统中试错可能影响用户。

因此需要：

- shadow mode；
- canary deployment；
- A/B testing；
- 仿真；
- 离线回放；
- 保守策略。

---

#### 3. 模型可能漂移

工作负载和硬件都会变化。

今天训练好的模型，未来可能失效。

例如：

- 新 CPU 代际；
- 新加速器；
- 新应用；
- 新流量模式；
- 新故障类型。

因此需要持续学习和监控。

---

#### 4. 可解释性和可信度

工程师需要理解：

```text
为什么 ML 做出这个决策？
```

否则很难信任它。

尤其在故障排查时，黑箱决策会增加复杂性。

---

#### 5. 因果关系 difficult

ML 擅长发现相关性，但系统优化常常需要因果关系。

例如：

```text
延迟升高是因为 cache 不足？
还是因为网络拥塞？
还是因为 GC？
还是因为功率节流？
```

如果只靠相关性，可能做出错误优化。

---

### 十二、与第 7 章整体的关系

7.6 可以看作第 7 章的总结升级。

---

#### 1. 从软件定义到自驾式

第 7 章前半部分：

```text
Software-defined infrastructure
```

强调：

- 软件控制硬件；
- 全局视图；
- 自动化策略；
- 可编程接口。

7.6 进一步：

```text
Self-driving systems
```

强调：

- ML 分析数据；
- 自动发现优化机会；
- 自动生成策略；
- 自动设计和自动调优。

---

#### 2. 各节与 ML 的对应

|前面章节|ML 可以做什么|
| -------------------------------| -------------------------------------|
|Software-defined servers|自动调 CPU、cache、prefetcher、NUMA|
|Software-defined accelerators|自动搜索模型架构或加速目标|
|Software-defined networks|自动流量工程、攻击检测、路径优化|
|Software-defined storage|自动冷热分层、缓存、设备放置|
|Software-defined power|功率预测、风险预测、节流策略优化|
|Software-defined fleet|容量预测、自动伸缩、集群选择|
|Self-driving systems|跨层自主优化和自主设计|

---

### 十三、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.6 Self-driving systems

1. 核心命题：
   - ML 正在推动计算需求
   - 系统正在为 ML workloads 重新设计
   - 但 ML 也可以反过来用于更好地设计系统
   - 特别是在 software-defined infrastructure 中
   - 目标：
     - 提升性能
     - 提升效率
     - 提升 resilience

2. Systems for ML vs ML for Systems：
   - Systems for ML：
     - 为 ML 工作负载设计更好的硬件和系统
   - ML for Systems：
     - 用 ML 优化系统设计、控制和运维
   - 7.6 主要讲 ML for Systems

3. Self-driving systems 的含义：
   - 类比自动驾驶
   - 系统通过 telemetry 感知状态
   - 用 ML 分析和预测
   - 自动做出优化决策
   - 通过软件定义基础设施执行
   - 持续反馈和学习
   - 目标：
     - 自主优化
     - 自主调参
     - 自主恢复
     - 自主设计

4. 与 software-defined infrastructure 的关系：
   - software-defined infrastructure 提供：
     - 可编程硬件
     - 全局遥测
     - 集中控制平面
     - 统一抽象
     - 自动化策略接口
   - self-driving systems 在此基础上加入：
     - ML 分析
     - 预测
     - 自动决策
     - 闭环优化
   - 可以理解为：
     software-defined infrastructure 让系统可被软件控制
     self-driving systems 让控制策略由 ML 自动优化

5. ML for Systems 的代表性例子：

   a. 自动识别加速器目标：
      - 分析大型代码库
      - 识别代码模式
      - 自动发现潜在加速目标
      - 建议 hardware/software co-design 策略
      - 好处：
        - 加速开发
        - 降低加速器使用门槛
        - 促进创新接口和生态

   b. ML 驱动的 generative design：
      - 自动化 chip layout
      - 自动化 PCB layout
      - 优化：
        - performance
        - power efficiency
        - reliability
      - 容纳异构性
      - 克服传统设计流程僵硬、耗时的问题
      - 未来可能：
        - 十几个人三个月设计一颗芯片
        - 今天可能需要一百人一年
        - 同时得到更优设计

   c. 节点级控制系统：
      - ML 分析 system-wide telemetry
      - 动态调整各种参数
      - 基于实时 workload 特征优化资源分配
      - 可优化：
        - CPU 频率
        - power state
        - prefetcher
        - LLC 分配
        - memory bandwidth
        - NUMA 绑定
        - QoS
      - 好处：
        - 提升 QoS
        - 提升效率
        - 提升资源利用率
      - 适用范围：
        - 多厂商
        - 多平台
        - 多作业
        - 多集群
        - 多应用

   d. 大规模分布式系统：
      - ML 建模网络、存储、集群等解耦系统中的复杂交互
      - 可优化：
        - power/cooling distribution
        - 跨集群任务调度
        - tail latency
      - 目标：
        - efficient scaling
        - fault tolerance
        - overall performance improvement

6. self-driving systems 的统一闭环：
   telemetry
     → ML 分析
     → 预测状态/异常/需求
     → 生成策略
     → 通过软件定义基础设施执行
     → 观察效果
     → 反馈学习

7. 为什么 ML 对未来 WSC 很重要：
   - 系统规模巨大
   - 硬件异构性强
   - 工作负载变化快
   - 优化目标多且相互冲突
   - 人工规则难以覆盖
   - ML 可以在高维、动态、复杂环境中寻找优化策略

8. 为什么仍处于早期：
   - 生产系统需要安全性
   - 在线实验有风险
   - 模型可能漂移
   - 可解释性不足
   - 因果关系难以建立
   - 需要 guardrails、fallback 和人工监督
   - 需要持续监控和再训练

9. 与第 7 章其他部分的关系：
   - software-defined servers：
     - ML 自动调节点参数
   - software-defined accelerators：
     - ML 自动搜索模型架构或加速目标
   - software-defined networks：
     - ML 自动流量工程、攻击检测、路径优化
   - software-defined storage：
     - ML 自动冷热分层、缓存和放置
   - software-defined power：
     - ML 预测功率风险和优化节流
   - software-defined fleet：
     - ML 预测容量和自动伸缩
   - self-driving systems：
     - 将上述能力整合为自主优化系统

10. 核心逻辑：
   ML 工作负载推动系统重新设计
     → software-defined infrastructure 提供可编程基础
     → ML 反过来用于分析和优化系统
     → 从代码加速、芯片设计、节点控制到分布式系统优化
     → 系统逐步走向 self-driving
     → 目前仍处早期，但将成为未来 WSC 设计的重要部分
```

---

### 十四、一句话总结这一节

> 7.6 说明：在 software-defined infrastructure 提供的可编程、可观测和可控制基础之上，机器学习可以进一步用于代码加速识别、芯片与 PCB 生成式设计、节点级自动调参和大规模分布式系统优化，使数据中心逐步走向 self-driving systems；这既是 ML for Systems 的核心方向，也是未来 WSC 设计的重要趋势。


**专栏导航**

- ← 上一篇：[7.5.2 Software-defined fleet](/posts/7-5-2-software-defined-fleet/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
