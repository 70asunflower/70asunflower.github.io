---
title: "7.1.3 Case study: Platform-aware scheduling"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：7.1.3 Case study: Platform-aware scheduling。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.1.3 Case study: Platform-aware scheduling。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.1.3 Case study: Platform-aware scheduling

下面把 **7.1.3 Case study: Platform-aware scheduling** 作为一个独立小节来深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

---

### 7.1.3 Case study: Platform-aware scheduling 深入理解

这一节是 7.1 “Software-defined servers” 的第二个案例。  
如果说 7.1.2 的 TCMalloc 是**单机内部、基础库层面的硬件感知优化**，那么 7.1.3 讲的是**集群层面的硬件感知优化**：

> 不只是把程序跑起来，而是把程序调度到最适合它的硬件平台上运行。

这正是 software-defined servers 在集群调度层的核心体现。

---

#### 一、这一节的核心命题

原文第一句已经概括得很清楚：

> Platform-aware scheduling is another classic software-defined server optimization, where we schedule workloads to specific platforms where they perform best for improved performance and utilization.

可以理解为：

> 平台感知调度是一种经典的软件定义服务器优化，它根据工作负载在不同平台上的实际表现，把任务调度到最适合它的平台上，从而提升性能和利用率。

这里有两个关键词：

1. **performance**：让任务跑得更快；
2. **utilization**：让合适的硬件被合适的任务充分利用。

---

### 二、为什么需要平台感知调度？

#### 1. 不同工作负载对不同硬件的敏感度不同

原文说：

> Workload performance can vary significantly on different platforms due to varying sensitivities to the underlying micro-architecture.

也就是说：

> 工作负载性能在不同平台上可能差异很大，因为它们对底层微架构的敏感程度不同。

这背后的意思是：

> 应用不是只看“CPU 有多快”或“核数有多少”，而是会受 cache、内存带宽、SMT、频率、指令集、NUMA、加速器等微架构特性影响。

---

#### 2. 三类典型工作负载与硬件偏好

原文给了三个例子。

|工作负载类型|例子|更适合的平台特征|原因|
| -------------------------------| --------------------| ------------------| ----------------------------|
|memory-intensive|video transcoding|每核内存带宽高|数据搬运多，内存带宽是瓶颈|
|heavily multithreaded|web search|SMT 或大核数|并发任务多，并行度高|
|single-threaded compute-bound|单线程计算密集任务|高时钟频率|单线程性能依赖频率|

这几个例子说明：

> 不存在一种平台对所有工作负载都最好。

---

##### 例子 1：内存密集型负载

原文说：

> memory-intensive workloads, like video transcoding, thrive on platforms with high memory bandwidth per core.

如果某个应用每个核心需要读取大量数据，那么它更关心：

- 内存通道数；
- 内存频率；
- 每核可用带宽；
- cache 行为；
- NUMA 局部性。

即使某台机器核数更多，但如果每核内存带宽不足，实际性能也可能不好。

---

##### 例子 2：高并发多线程负载

原文说：

> heavily multithreaded workloads, such as web search, favor platforms with simultaneous multithreading, SMT, or a large core count.

像 web search 这类服务通常有大量并发请求。

它更关心：

- 核数；
- 线程数；
- SMT 能力；
- 调度延迟；
- 网络栈效率；
- cache 分享行为。

因此，多核或 SMT 强的平台可能更适合。

> [!NOTE]
> Intel 将其实现的 SMT 技术称为 **超线程技术（Hyper-Threading Technology，简称 HT）** 。AMD 的 Zen 架构以及 IBM 的 POWER 系列则直接称之为 SMT。
>
> **SMT（同步多线程，Simultaneous Multithreading）是一项让单个物理 CPU 核心在同一时刻能并行执行多个（通常是2个）线程的硬件技术。**

---

##### 例子 3：单线程计算密集型负载

原文说：

> Single-threaded compute-bound workloads perform best on platforms with higher clock speeds.

如果任务很难并行，那么核数再多也不一定有用。  
它更依赖：

- 单核频率；
- 分支预测；
- cache latency；
- 指令级并行；
- 微架构效率。

因此高频率平台可能比多核平台更适合。

---

### 三、如何理解 Figure 7.4？

原文描述了 Figure 7.4：

> Figure 7.4 shows the performance of a particular binary across the five most common platforms in the fleet at the time of the measurement.

这张图展示的是：

> 某个二进制程序在 fleet 中五个最常见平台上的相对性能。

---

#### 1. 该 binary 的性能表现是稳定的

原文说：

> The binary’s performance was consistent over time and shows a clear preference for platform A.

这说明两件事：

1. 这个工作负载的性能特征比较稳定；
2. 它对平台有明显偏好，尤其偏好 platform A。

这很重要，因为如果工作负载行为稳定，那么通过历史 profile 生成平台偏好列表就是可行的。

---

#### 2. platform D 是最差选择

原文说：

> platform D would be the worst choice to run this binary.

也就是说，同一个 binary：

- 在 platform A 上表现最好；
- 在 platform D 上表现最差。

这说明：

> 调度器如果只看“有没有资源”，而不看“资源是否适合”，可能会把任务放到不合适的平台上。

---

#### 3. 图中 100% 的含义

原文说：

> In this graph, 100% refers to the performance that would be expected purely from the performance rating of each platform.

这里的 100% 不是绝对性能，而是一个预期基线：

> 如果只根据平台的通用性能评级来预测，该应用应该达到的性能。

可以理解为：

```text
100% = 按照平台通用性能评级预期的性能
```

如果某平台上的实际性能低于 100%，说明：

> 该平台对这个特定应用并不像通用评级看起来那么合适。

---

#### 4. 原文中的具体数字

原文说：

> this particular application runs about 3% slower than expected on the top two platforms but 10% slower than expected on platform D.

也就是说：

|平台|相对表现|
| -------------------| ----------------|
|top two platforms|比预期慢约 3%|
|platform D|比预期慢约 10%|

这说明即使最好的平台也没有完全达到通用评级预期，但 platform D 的偏差更大。

换句话说：

> 通用平台评级只能反映平均或通用性能，不能准确预测每个工作负载在平台上的真实表现。

---

### 四、平台感知调度的系统流程

原文给出了一个完整的数据驱动流程。

---

#### 1. 生产环境中采集 workload profiles

原文说：

> A data processing pipeline captures profiles of workloads running in production environments.

也就是说，平台偏好不是靠人工猜测，而是来自真实生产环境数据。

这些 profile 可能包括：

- CPU 利用率；
- cache miss；
- TLB miss；
- 内存带宽；
- 指令混合；
- 延迟；
- 吞吐；
- 每平台性能表现；
- 资源竞争情况；
- 加速器利用率。

重点是：

> 用真实运行数据刻画 workload 与 hardware 的交互。

---

#### 2. 使用排序算法分析 profiles

原文说：

> A ranking algorithm employs data mining techniques, like hierarchical agglomerative clustering, to analyze the profiles and create a ranked list of preferred platforms for each workload.

这里的关键是：

> 不只是收集数据，还要从数据中挖掘出“每个 workload 更喜欢哪些平台”。

---

##### hierarchical agglomerative clustering 是什么？

可以简单理解为一种聚类方法：

> 自底向上把相似的对象逐步合并成簇。

在这里，它可能用于：

- 把性能特征相似的 workload 聚成一类；
- 把平台偏好相似的任务归为一类；
- 从大量 profile 中发现稳定模式；
- 为 workload 或 workload 类别生成平台偏好排名。

你不需要记住算法细节，只要理解它的作用是：

> 从历史性能数据中自动发现 workload-platform 亲和性。

---

#### 3. 为每个 workload 生成平台偏好列表

原文说：

> create a ranked list of preferred platforms for each workload.

也就是说，每个工作负载可能得到一个类似下面的偏好列表：

```text
Workload X preferred platforms:
1. Platform A
2. Platform B
3. Platform C
4. Platform E
5. Platform D
```

这表示：

> 对 Workload X 来说，Platform A 最合适，Platform D 最不合适。

---

#### 4. 上传到 cluster manager

原文说：

> These workload-specific platform preferences are then uploaded to the cluster manager.

cluster manager 是集群管理器，负责决定：

- 哪个任务跑在哪台机器；
- 哪些任务可以混部；
- 哪些机器有空闲资源；
- 哪些机器满足硬件要求；
- 哪些任务需要优先保障 SLO。

现在它不仅知道资源余量，还知道：

> 某个 workload 在哪些平台上表现更好。

---

#### 5. cluster manager 调度到最合适平台

原文说：

> the cluster manager schedules workloads onto the most suitable hardware platforms available.

注意这里有两个约束：

1. **suitable**：适合该 workload；
2. **available**：当前有可用资源。

调度器要在两者之间做权衡。

例如：

```text
Workload X 最喜欢 Platform A，
但 Platform A 当前资源不足，
调度器可能选择次优的 Platform B。
```

这就是真实集群调度中的常见权衡：

> 最优平台偏好 vs 当前资源可用性。

---

### 五、平台感知调度的收益

原文给出的效果非常显著。

---

#### 1. 关键工作负载平均性能提升 7–10%

原文说：

> Enabling platform-aware scheduling for all critical workloads improved average performance by 7–10%.

在 WSC 规模下，7–10% 的平均性能提升非常大。

因为这意味着：

- 同样的硬件可以服务更多请求；
- 同样的延迟目标可以用更少资源达成；
- 整体 TCO 下降；
- 关键服务体验更稳定。

---

#### 2. 收益不仅限于通用计算

原文说：

> the benefits of such an approach extend beyond general computing, to also accelerators and GPU-based platforms.

也就是说，平台感知调度不仅适用于 CPU 平台，也适用于：

- GPU；
- TPU；
- FPGA；
- 其他 domain-specific accelerators。

这很符合前面章节提到的趋势：

> WSC 越来越异构，加速器越来越多。

---

#### 3. 某些平台利用率翻倍

原文说：

> implementing this approach for accelerators and GPUs has doubled the utilization of some platforms.

这说明之前可能存在错配：

- 某些加速器平台没有被合适的任务使用；
- 合适任务没有被调度到这些平台上；
- 或者调度器不知道哪些任务能充分利用这些硬件。

平台感知调度之后：

> 合适的任务被放到合适的加速器上，平台利用率显著提高。

---

#### 4. 用户体验保持透明

原文说：

> all while maintaining a seamless experience for end-users, who remain shielded from the complexities of underlying hardware differences.

也就是说：

> 用户不需要知道 Platform A、Platform D、GPU 型号、加速器差异。

用户只需要提交任务，系统自动选择合适平台。

这正是 software-defined infrastructure 的理想状态：

> 底层硬件复杂性由软件控制平面吸收，用户看到简单统一的抽象。

---

### 六、这一节如何体现 software-defined servers？

这一节非常典型地体现了 software-defined servers 的几个核心思想。

---

#### 1. 软件拥有全局视图

单个服务器只知道自己的状态。  
cluster manager 知道：

- 所有平台类型；
- 所有节点资源；
- 所有工作负载；
- 所有历史 profile；
- 所有平台偏好。

因此它可以做全局最优匹配。

---

#### 2. 软件理解硬件差异

平台感知调度不是简单按 CPU 核数或内存大小调度，而是理解：

- 微架构差异；
- 内存带宽差异；
- SMT 差异；
- 频率差异；
- 加速器差异；
- workload 对硬件特性的敏感度。

这就是：

> software understands hardware heterogeneity.

---

#### 3. 软件动态匹配 workload 和 hardware

它不是静态规定：

> 某类服务永远跑在某类机器上。

而是基于数据生成：

> 每个 workload 的平台偏好排名。

然后由 cluster manager 动态调度。

---

#### 4. 用户不需要感知硬件复杂性

原文强调 end-users remain shielded。

这说明 software-defined servers 不只是提高性能，也改善可用性：

> 把复杂硬件选择问题交给系统，而不是开发者。

---

### 七、与 7.1.2 TCMalloc 案例的关系

这两个案例可以放在一起理解。

|案例|优化层次|优化对象|核心问题|
| ---------------------------------| ---------------| -----------------------------| -------------------------------------|
|7.1.2 TCMalloc|单机 / 库层|内存分配器|TLB miss、hugepage 利用率、内存碎片|
|7.1.3 Platform-aware scheduling|集群 / 调度层|workload 到 platform 的匹配|异构平台性能差异、利用率、调度质量|

两者都属于 software-defined servers，但层次不同：

```text
TCMalloc：
让程序在单台机器上更好地使用内存和页表。

Platform-aware scheduling：
让程序在整个集群中被放到最合适的机器上。
```

---

### 八、可以进一步思考的问题

学习这一节时，可以带着几个问题。

---

#### 1. 为什么不能只靠“平台性能评级”？

因为平台评级通常是通用指标，例如：

- CPU benchmark；
- 核数；
- 频率；
- 内存容量；
- 厂商标称性能。

但真实应用可能更关心：

- 每核内存带宽；
- LLC；
- NUMA；
- TLB；
- 指令集；
- 加速器；
- 网络；
- 存储。

所以：

> 通用评级不能替代 workload-specific profiling。

---

#### 2. 为什么 profile 要在生产环境中采集？

因为生产环境最真实。

合成 benchmark 可能无法反映：

- 真实流量；
- 真实数据分布；
- 真实并发；
- 真实混部干扰；
- 真实 SLO；
- 真实硬件状态。

---

#### 3. 如果工作负载行为变化怎么办？

原文说这个 binary 的性能 consistent over time。  
但并非所有 workload 都稳定。

如果 workload 行为变化很快，就需要：

- 持续 profiling；
- 在线学习；
- 动态更新偏好；
- 反馈式调度。

---

#### 4. 如果最佳平台资源不足怎么办？

调度器不能总是把任务放到第一名平台。

它需要权衡：

- 平台偏好；
- 资源可用性；
- 优先级；
- QoS；
- 能耗；
- 故障域；
- 负载均衡；
- 混部干扰。

因此平台偏好是调度输入，不是唯一约束。

---

#### 5. 平台感知调度会不会造成某些平台过载？

有可能。

如果很多 workload 都喜欢 Platform A，Platform A 可能成为热点。

因此系统还需要：

- 容量规划；
- 负载均衡；
- 次优平台回退；
- QoS 隔离；
- 优先级调度。

---

### 九、这一节的核心逻辑链

可以把这一节压缩成如下逻辑：

```text
不同平台微架构不同
  ↓
不同 workload 对微架构敏感度不同
  ↓
同一个 workload 在不同平台上的性能差异很大
  ↓
通用平台评级不足以预测真实性能
  ↓
通过生产环境 profiling 分析 workload-platform 亲和性
  ↓
为每个 workload 生成平台偏好排名
  ↓
cluster manager 根据偏好调度任务
  ↓
提升性能、利用率和用户透明性
```

---

### 十、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.1.3 Case study: Platform-aware scheduling

1. 核心定义：
   - Platform-aware scheduling 是 software-defined server 的经典优化
   - 目标：
     - 把 workload 调度到表现最好的平台
     - 提升性能
     - 提升利用率

2. 为什么需要平台感知调度：
   - 不同平台微架构不同
   - 不同 workload 对微架构敏感度不同
   - 同一 workload 在不同平台上性能差异可能很大
   - 通用平台评级不能准确预测真实性能

3. 典型 workload-platform 匹配：
   - memory-intensive workloads：
     - 例如 video transcoding
     - 适合 high memory bandwidth per core
   - heavily multithreaded workloads：
     - 例如 web search
     - 适合 SMT 或 large core count
   - single-threaded compute-bound workloads：
     - 适合 higher clock speeds

4. Figure 7.4 的含义：
   - 展示某个 binary 在五个常见平台上的相对性能
   - 该 binary 性能随时间稳定
   - 明显偏好 platform A
   - platform D 是最差选择
   - 图中 100%：
     - 表示仅根据平台性能评级预期的性能
   - 该应用：
     - 在 top two platforms 上比预期慢约 3%
     - 在 platform D 上比预期慢约 10%
   - 结论：
     - 平台通用评级不足以反映 workload-specific 性能

5. 平台感知调度流程：
   a. 数据采集：
      - 在生产环境中捕获 workload profiles
   b. 数据分析：
      - 使用 ranking algorithm
      - 使用数据挖掘技术
      - 例如 hierarchical agglomerative clustering
   c. 生成偏好：
      - 为每个 workload 创建 preferred platforms ranked list
   d. 上传集群管理器：
      - cluster manager 获得 workload-platform preferences
   e. 调度执行：
      - cluster manager 把 workload 调度到最合适的可用平台

6. 关键思想：
   - 不是只看资源是否足够
   - 而是看平台是否适合该 workload
   - 调度目标从：
     “找到能跑的机器”
     变成：
     “找到最适合跑的机器”

7. 优化效果：
   - 对所有关键 workload 启用后：
     - 平均性能提升 7–10%
   - 收益不仅限于通用计算
   - 也适用于 accelerators 和 GPU-based platforms
   - 某些 accelerator/GPU 平台利用率翻倍

8. 用户体验：
   - end-users 不需要理解底层硬件差异
   - 硬件复杂性被软件控制平面吸收
   - 用户仍然看到简单、统一的服务抽象

9. 与 software-defined servers 的关系：
   - 体现软件对硬件异构性的理解
   - 体现全局视图优化局部决策
   - 体现 workload-hardware matching
   - 是集群层 software-defined server 优化的典型例子

10. 与 7.1.2 的关系：
   - 7.1.2 TCMalloc：
     - 单机 / 库层优化
     - 关注 TLB、hugepage、内存分配
   - 7.1.3 Platform-aware scheduling：
     - 集群 / 调度层优化
     - 关注 workload 与 platform 的匹配

11. 核心逻辑：
   平台微架构不同
     → workload 对硬件敏感度不同
     → 同一 workload 在不同平台性能不同
     → 通过 profiling 和 clustering 生成平台偏好
     → cluster manager 按偏好调度
     → 提升性能、利用率和透明度
```

---

### 十一、一句话总结这一节

> 7.1.3 说明：在异构 WSC 中，调度器不应只根据资源余量分配任务，而应根据工作负载在不同平台上的真实表现，把任务调度到最合适的硬件平台上；这正是软件定义服务器在集群层的核心价值。


**专栏导航**

- ← 上一篇：[7.1.2 Case study: Library optimizations](/posts/7-1-2-case-study-library-optimizations/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.2 Software-defined accelerators →](/posts/7-2-software-defined-accelerators/)
