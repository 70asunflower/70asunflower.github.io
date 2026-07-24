---
title: "6.1.2.1 A model to reason about scale-up versus scale-out"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-23
description: "《The Data Center as a Computer》AI 导读专栏正文：6.1.2.1 A model to reason about scale-up versus scale-out。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.1.2.1 A model to reason about scale-up versus scale-out。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.1.2.1 A model to reason about scale-up versus scale-out

下面我结合你提供的原文，把 **6.1.2.1 A model to reason about scale-up versus scale-out** 这一小节读深。

这一节是整本书里非常经典的一部分。它用一个非常简单的模型，回答了一个很重要的问题：

> 既然大型 SMP 服务器通信更快，为什么 WSC 仍然主要选择 scale-out 集群？  
> 什么时候 scale-up 有优势？  
> 什么时候 scale-out 的成本效率更好？  
> 为什么在 warehouse scale 下，高端服务器的性能优势会被稀释？

---

# 一、这一节要解决的核心问题

在上一节中，原文提到：

```text
scale-up：大型共享内存系统
scale-out：大量普通服务器集群
```

直觉上，scale-up 系统有一个明显优势：

> 单机内部通信非常快。

而 scale-out 系统有一个明显劣势：

> 跨机器通信慢。

因此，如果只看单台机器，高端 SMP 服务器似乎应该更快。

但问题是：

> WSC 应用通常大到不可能放进一台高端服务器里。

所以真正要比较的不是：

```text
一台大服务器 vs 一台小服务器
```

而是：

```text
由多台大 SMP 服务器组成的集群
vs
由大量低端服务器组成的集群
```

当系统规模达到几千个 CPU 核心时，哪种平台更划算？

这就是这一节模型要回答的问题。

---

# 二、为什么简单的“处理器成本效率分析”不够？

原文开头说：

> Simple processor-centric cost-efficiency analyses show that a single server of capacity N × M is much more expensive than N servers of capacity M.

最简单的分析是：

```text
一台容量为 N × M 的大服务器
通常比 N 台容量为 M 的小服务器贵很多。
```

例如：

```text
一台 128 核大服务器
通常比 32 台 4 核小服务器贵得多。
```

如果只看 CPU 性能和价格，结论似乎是：

```text
低端服务器集群更划算。
```

但原文指出，这种分析忽略了一件重要事情：

> 大型 SMP 服务器的内部通信性能远远好于普通服务器集群。

---

# 三、SMP 和集群通信延迟的巨大差异

原文说：

> Nodes in a large SMP can communicate at latencies on the order of 100 ns, whereas LAN-based networks, usually deployed in clusters of servers, can experience latencies on the order of 100 µs.

这里给出了两个数量级：

```text
SMP 内部通信：约 100 ns
LAN 集群通信：约 100 µs
```

注意：

```text
100 µs = 100,000 ns
```

所以两者相差：

```text
100,000 ns / 100 ns = 1000 倍
```

也就是说，远程网络访问可能比本地共享内存访问慢大约 1000 倍。

---

## 1. SMP 内部通信为什么快？

SMP，Shared-Memory Multiprocessor，共享内存多处理器。

在 SMP 系统里，多个 CPU 共享同一个内存地址空间。

例如：

```text
CPU 0
CPU 1
CPU 2
...
CPU 127
```

它们可以通过共享内存通信：

```text
CPU A 写内存
CPU B 读内存
```

底层依赖：

```text
内存总线
片内互连
缓存一致性协议
NUMA 互连
```

因此延迟可以接近：

```text
DRAM 访问延迟
约 100 ns
```

---

## 2. 集群通信为什么慢？

在服务器集群里，不同机器之间通过网络通信。

例如：

```text
Server A -> Ethernet switch -> Server B
```

一次远程访问通常涉及：

```text
系统调用
协议栈
序列化
网卡发送
交换机转发
网卡接收
中断
反序列化
上下文切换
内存拷贝
```

因此延迟通常是：

```text
几十微秒到几百微秒
```

原文用：

```text
约 100 µs
```

作为典型 LAN 延迟。

---

# 四、哪些应用会从大型 SMP 中受益？

原文说：

> For parallel applications that fit within a single large SMP, the efficient communication can translate into dramatic performance gains.

如果一个并行应用可以完整放进一台大型 SMP，那么它可以充分利用 SMP 内部快速通信。

原文举例：

```text
SAP HANA
```

这类负载可能具有：

```text
大量共享数据结构
频繁内存访问
多个线程紧密协作
需要低延迟通信
```

如果它们能放进一台大机器，那么 SMP 的优势很明显。

---

## 1. 为什么“fit within a single large SMP”很关键？

关键词是：

```text
fit
```

也就是说，应用的数据集和工作集必须能放进单台大机器的内存和 CPU 规模里。

如果可以：

```text
所有线程都在同一台机器内
所有全局数据访问都是本地内存访问
```

那么通信延迟大约是：

```text
100 ns
```

---

## 2. 如果不能 fit 怎么办？

如果应用太大，必须跨多台机器：

```text
数据分布在多个节点
线程访问远程数据
```

那么很多访问会变成：

```text
远程分布式访问
```

延迟变成：

```text
约 100 µs
```

这时性能可能严重下降。

---

# 五、为什么 WSC 应用通常不能 fit 进单台 SMP？

原文说：

> However, as discussed earlier in the discussion on WSC applications, most large workloads are unlikely to fit within an SMP.

WSC 应用通常非常大，例如：

```text
搜索索引
广告系统
社交网络
视频存储
对象存储
大规模数据库
推荐系统
AI 训练
日志分析
```

这些系统的数据量和计算量通常远超单台服务器。

例如：

```text
搜索索引可能是 PB 级
用户数据可能是 EB 级
训练数据可能是 TB/PB 级
模型参数可能是 TB 级
```

单台 SMP 再大，也不可能装下整个系统。

因此 WSC 必须使用分布式集群。

---

# 六、模型的目标：比较大 SMP 集群和低端服务器集群

原文说：

> Therefore, it is important to understand the relative performance of clusters of large SMPs with respect to clusters of low-end servers each with smaller number of CPU sockets or cores.

也就是说，真正要比较的是：

```text
集群 A：少量大型 SMP 服务器
集群 B：大量低端小服务器
```

例如：

```text
集群 A：16 台 128 核 SMP 服务器
集群 B：512 台 4 核低端服务器
```

两者总核心数可能相同：

```text
16 × 128 = 2048 cores
512 × 4 = 2048 cores
```

问题是：

```text
集群 A 是否比集群 B 快很多？
如果快，快多少？
值不值得为集群 A 付更高价格？
```

---

# 七、模型的基本假设

原文给出的模型非常简单。

---

## 1. 任务执行时间由两部分组成

原文说：

> Assume that a given parallel task execution time can be modeled as a fixed local computation time plus the latency penalty of accesses to global data structures.

也就是：

```text
执行时间 = 本地计算时间 + 全局数据访问延迟惩罚
```

可以写成：

```text
time = local computation + global access penalty
```

---

## 2. 本地计算时间固定为 1 ms

原文说：

> If the fixed local computation time is of the order of 1 ms—a reasonable value for high-throughput internet services.

也就是说，每完成一个工作单元，本地计算大约花：

```text
1 ms
```

这对应高吞吐互联网服务中常见的小工作单元。

例如：

```text
处理一个请求的一部分
执行一个任务的一片
完成一个小型计算单元
```

---

## 3. 全局访问次数用 f 表示

原文说：

> the variable f is the number of global accesses per work unit.

也就是：

```text
f = 每个 1 ms 工作单元需要访问全局数据结构的次数
```

例如：

```text
f = 1：轻通信
f = 10：中等通信
f = 100：高通信
```

---

## 4. 本地访问和远程访问延迟不同

如果数据在本地节点：

```text
本地访问延迟 ≈ 100 ns
```

如果数据在远程节点：

```text
远程访问延迟 ≈ 100 µs
```

---

# 八、模型公式推导

原文给出第一个公式：

```text
time = 1ms + f · (100ns · LocalAccessesFraction + 100µs · RemoteAccessesFraction)
```

---

## 1. 公式含义

每个工作单元：

```text
本地计算：1 ms
```

此外还有 f 次全局访问。

每次全局访问可能是：

```text
本地访问
或
远程访问
```

本地访问延迟：

```text
100 ns
```

远程访问延迟：

```text
100 µs
```

所以总延迟惩罚是：

```text
f × (本地访问比例 × 100ns + 远程访问比例 × 100µs)
```

---

## 2. 本地访问比例如何计算？

原文假设：

> accesses to the global store are uniformly distributed among all nodes.

也就是全局访问均匀分布在所有节点上。

如果系统有 N 个节点，那么某个访问正好落在本地节点的概率是：

```text
1/N
```

远程访问比例是：

```text
(N - 1)/N
```

因此公式变成：

```text
time = 1ms + f · (1/N · 100ns + (N - 1)/N · 100µs)
```

---

# 九、如何理解这个公式？

这个公式最重要的地方是：

> 节点数 N 越大，远程访问比例越高。

当：

```text
N = 1
```

所有访问都是本地：

```text
本地比例 = 1
远程比例 = 0
```

当：

```text
N = 2
```

本地比例：

```text
1/2 = 50%
```

远程比例：

```text
1/2 = 50%
```

当：

```text
N = 10
```

本地比例：

```text
10%
```

远程比例：

```text
90%
```

当：

```text
N = 100
```

本地比例：

```text
1%
```

远程比例：

```text
99%
```

当 N 很大时：

```text
远程比例接近 100%
```

---

# 十、为什么从 1 个节点到 2 个节点性能下降最剧烈？

原文说：

> the penalties can be quite severe, but they are most dramatic when moving from a single node to two, with rapidly decreasing additional penalties for increasing the cluster size.

这是这一节非常关键的洞察。

---

## 1. N = 1 时

所有访问都是本地：

```text
远程比例 = 0
```

延迟惩罚：

```text
f × 100ns
```

---

## 2. N = 2 时

远程比例突然变成：

```text
50%
```

延迟惩罚变成：

```text
f × (0.5 × 100ns + 0.5 × 100µs)
```

由于 100 µs 比 100 ns 大 1000 倍，所以即使只有一半访问远程，延迟惩罚也会急剧上升。

---

## 3. N 继续增加时

从：

```text
N = 2 到 N = 3
```

远程比例从：

```text
50% -> 66.7%
```

增加 16.7%。

从：

```text
N = 10 到 N = 11
```

远程比例从：

```text
90% -> 90.9%
```

只增加 0.9%。

从：

```text
N = 100 到 N = 101
```

远程比例从：

```text
99% -> 99.01%
```

几乎不变。

所以：

```text
最大性能损失发生在从单机变成两机的时候。
之后随着节点数增加，额外损失越来越小。
```

---

# 十一、用数值例子理解 Figure 6.1

原文 Figure 6.1 画了三条曲线：

```text
f = 1：轻通信
f = 10：中等通信
f = 100：高通信
```

我们可以手动算一些值。

---

## 1. f = 1：轻通信

### N = 1

```text
time = 1ms + 1 × 100ns
     = 1ms + 0.0001ms
     = 1.0001ms
```

### N = 2

```text
time = 1ms + 1 × (0.5 × 100ns + 0.5 × 100µs)
     ≈ 1ms + 50µs
     = 1.05ms
```

### N 很大

```text
time ≈ 1ms + 1 × 100µs
     = 1.1ms
```

所以轻通信下，即使扩展到很多节点，执行时间也只从：

```text
1.0001ms
增加到
1.1ms
```

影响不大。

---

## 2. f = 10：中等通信

### N = 1

```text
time = 1ms + 10 × 100ns
     = 1ms + 1µs
     = 1.001ms
```

### N = 2

```text
time ≈ 1ms + 10 × 50µs
     = 1ms + 500µs
     = 1.5ms
```

### N 很大

```text
time ≈ 1ms + 10 × 100µs
     = 1ms + 1ms
     = 2ms
```

中等通信下，性能最多大约下降：

```text
2 倍
```

---

## 3. f = 100：高通信

### N = 1

```text
time = 1ms + 100 × 100ns
     = 1ms + 10µs
     = 1.01ms
```

### N = 2

```text
time ≈ 1ms + 100 × 50µs
     = 1ms + 5ms
     = 6ms
```

### N 很大

```text
time ≈ 1ms + 100 × 100µs
     = 1ms + 10ms
     = 11ms
```

高通信下，性能可能下降约：

```text
11 / 1.01 ≈ 10.9 倍
```

这正好对应原文说的：

> the performance advantage of a single 128-processor SMP over a cluster of thirty-two 4-processor SMPs could be more than a factor of 10×.

也就是说，在高通信负载下，如果应用能放进单台大 SMP，性能可能比集群快 10 倍以上。

---

# 十二、Figure 6.1 的核心结论

Figure 6.1 想表达的是：

```text
通信越少，scale-out 损失越小；
通信越多，scale-out 损失越大；
但最大损失发生在从 1 个节点变成 2 个节点时。
```

---

## 1. 轻通信负载

```text
f = 1
```

扩展到多节点几乎没什么影响。

因为每个工作单元只有 1 次全局访问，即使远程访问慢 1000 倍，总时间增加也有限。

---

## 2. 中等通信负载

```text
f = 10
```

扩展到多节点会有明显影响，但不致命。

---

## 3. 高通信负载

```text
f = 100
```

扩展到多节点会显著变慢。

但如果应用必须跨很多节点，那么从 2 个节点到 100 个节点的额外损失其实不大，因为远程访问比例已经接近 100%。

---

# 十三、为什么单台 128 核 SMP 可能比 32 台 4 核服务器集群快 10 倍以上？

原文说：

> Using this model, the performance advantage of a single 128-processor SMP over a cluster of thirty-two 4-processor SMPs could be more than a factor of 10×.

这是因为：

```text
单台 128 核 SMP：
  所有访问都可以是本地共享内存访问
  延迟约 100 ns

32 台 4 核服务器集群：
  很多访问必须跨网络
  延迟约 100 µs
```

如果通信很重，例如：

```text
f = 100
```

那么单机 SMP 的执行时间约为：

```text
1.01 ms
```

而多节点集群约为：

```text
11 ms
```

差距约：

```text
10.9 倍
```

所以原文说可能超过 10 倍。

---

# 十四、但 WSC 不是单台机器，而是几千核系统

原文说：

> By definition, WSC systems consist of thousands of CPUs.

WSC 系统通常有：

```text
数千 CPU
数万 CPU
甚至更多
```

所以不能只比较：

```text
一台 128 核 SMP
vs
32 台 4 核服务器
```

还要比较：

```text
由多台 128 核 SMP 组成的大集群
vs
由大量 4 核服务器组成的大集群
```

---

# 十五、Figure 6.2：高端 SMP 集群优势随规模增加而消失

原文说：

> In Figure 6.2, we apply our model to clusters varying between 512 and 4,192 cores.

这里比较的集群规模是：

```text
512 cores 到 4096 cores
```

比较对象是：

```text
高端服务器：128 cores，单共享内存域
低端服务器：4 cores SMP
```

例如：

```text
高端集群：16 台 128 核服务器 = 2048 cores
低端集群：512 台 4 核服务器 = 2048 cores
```

---

## 1. 为什么高端集群有优势？

高端集群节点数少。

例如同样是 2048 cores：

```text
高端：16 节点
低端：512 节点
```

如果全局访问均匀分布：

```text
高端集群本地访问比例 = 1/16 = 6.25%
低端集群本地访问比例 = 1/512 = 0.195%
```

高端集群远程访问比例：

```text
15/16 = 93.75%
```

低端集群远程访问比例：

```text
511/512 ≈ 99.8%
```

高端集群仍然有更多本地访问，所以通信延迟略低。

---

## 2. 但优势为什么很快变小？

因为两者远程访问比例都已经很高。

高端集群远程比例：

```text
93.75%
```

低端集群远程比例：

```text
99.8%
```

差距只有：

```text
约 6%
```

对于每次访问，高端集群平均延迟约为：

```text
0.0625 × 100ns + 0.9375 × 100µs
≈ 93.75µs
```

低端集群平均延迟约为：

```text
0.00195 × 100ns + 0.998 × 100µs
≈ 99.8µs
```

差距约：

```text
6µs
```

如果 f = 100，那么总差距约：

```text
100 × 6µs = 600µs = 0.6ms
```

而总执行时间大约是：

```text
10ms 左右
```

所以性能差距约：

```text
5% 左右
```

这正是原文说的：

> If the application requires more than 2,000 cores, a cluster of 512 low-end servers performs within approximately 5% of one built with 16 high-end servers, even under a heavy communication pattern.

---

# 十六、为什么高端服务器价格溢价让它失去吸引力？

原文说：

> With a performance gap this low, the price premium of the high-end server renders it an unattractive option.

高端服务器价格可能是低端服务器的：

```text
4 到 20 倍
```

但性能差距只有：

```text
约 5%
```

那么从成本效率看：

```text
多花 4–20 倍价格
只换来约 5% 性能优势
```

这显然不划算。

---

# 十七、这一节的定性结论

原文最后说：

> The point of this analysis is qualitative in nature.

也就是说，这个模型的价值不在于精确数字，而在于定性结论。

---

## 结论一：当应用能放进单台 SMP 时，scale-up 优势很大

如果应用可以完全放进一台大型 SMP：

```text
所有全局访问都是本地访问
延迟约 100 ns
```

那么对于高通信负载，性能可能比集群快：

```text
10 倍以上
```

---

## 结论二：当应用必须跨很多节点时，scale-up 优势被稀释

如果应用需要几千核，任何单台服务器都装不下。

那么无论使用：

```text
128 核高端服务器
还是
4 核低端服务器
```

大多数全局访问都已经是远程访问。

高端服务器的本地通信优势只能影响一小部分访问。

因此整体性能差距变小。

---

## 结论三：在 WSC 规模下，成本效率比单机性能更重要

原文说：

> Performance enhancements that have the greatest impact on computation, that are local to a single node, are still very important. But if they carry a heavy additional cost, their cost-efficiency may not be as competitive for WSCs as it is for small-scale computers.

单节点内部性能增强当然重要。

例如：

```text
快速 SMP 通信
大缓存
高内存带宽
低延迟互连
```

这些都很重要。

但如果这些增强带来很高成本，那么在 WSC 规模下未必划算。

因为 WSC 关心的是：

```text
整个数据中心的总性能 / 总成本
```

而不是：

```text
单台机器的极致性能
```

---

# 十八、这个模型的直观图示

可以用下面这个图理解。

---

## 单机情况

```text
N = 1

所有访问：
  本地 100%
  远程 0%

平均访问延迟：
  100 ns
```

---

## 两机情况

```text
N = 2

本地访问：
  50%

远程访问：
  50%

平均访问延迟：
  约 50 µs
```

性能急剧下降。

---

## 多机情况

```text
N = 100

本地访问：
  1%

远程访问：
  99%

平均访问延迟：
  约 99 µs
```

继续增加节点，性能下降越来越慢。

---

# 十九、这个模型的数学本质：远程比例趋近 100%

公式中的远程比例是：

```text
(N - 1)/N
```

当 N 增大时：

```text
(N - 1)/N -> 1
```

所以执行时间趋近于：

```text
time -> 1ms + f × 100µs
```

而单机执行时间是：

```text
time = 1ms + f × 100ns
```

最大性能差距约为：

```text
(1ms + f × 100µs) / (1ms + f × 100ns)
```

对于 f = 100：

```text
(1ms + 10ms) / (1ms + 0.01ms)
≈ 11ms / 1.01ms
≈ 10.9
```

所以高通信负载下，单机 SMP 相对多机集群可能有约 10 倍优势。

但当比较的是：

```text
高端集群 vs 低端集群
```

而不是：

```text
单机 vs 集群
```

两者都已经处于多节点状态，远程访问比例都很高，因此差距缩小。

---

# 二十、这个模型的局限

原文也承认：

> Although our model is exceedingly simple, for example, it does not account for contention effects.

这个模型非常简化。

它没有考虑很多现实因素。

---

## 1. 没有考虑争用

实际系统中可能出现：

```text
内存带宽争用
缓存争用
网络带宽争用
锁争用
I/O 争用
CPU 争用
```

这些会改变性能。

---

## 2. 假设访问均匀分布

原文假设：

```text
全局访问均匀分布在所有节点
```

但实际系统可以通过数据局部性优化减少远程访问。

例如：

```text
数据分片
副本放置
缓存
亲和性调度
一致性哈希
rack-aware placement
```

如果局部性很好，远程访问比例可能远低于：

```text
(N - 1)/N
```

---

## 3. 没有考虑网络拓扑

实际网络可能有：

```text
同机架低延迟
跨机架较高延迟
跨集群更高延迟
网络拥塞
ECMP 不均衡
incast
```

不是所有远程访问都一样慢。

---

## 4. 没有考虑软件优化

分布式系统可以通过：

```text
批量访问
异步通信
本地缓存
预取
压缩
RDMA
零拷贝
```

降低远程访问成本。

---

## 5. 没有考虑故障和运维

scale-out 集群需要处理：

```text
节点故障
磁盘故障
网络分区
滚动升级
容量调度
```

这些不是性能模型直接体现的，但会影响总体成本效率。

---

# 二十一、这一节与现代 AI 系统的关系

原文这个模型虽然简单，但对理解现代 AI 系统也很有帮助。

---

## 1. 传统 Web 服务通常通信较轻或可分区

很多互联网服务可以通过：

```text
无状态服务
分片
缓存
副本
负载均衡
```

减少跨节点通信。

因此 scale-out 很有效。

---

## 2. AI 训练可能通信很重

大模型训练经常需要：

```text
all-reduce
all-gather
reduce-scatter
参数同步
梯度同步
张量并行
流水线并行
```

这些通信非常频繁。

如果跨普通以太网，通信延迟和带宽可能成为瓶颈。

因此现代 AI 系统常在节点内或机架内使用高速互连：

```text
NVLink
NVSwitch
Infinity Fabric
ICI
RDMA
RoCE
InfiniBand
定制网络
```

这本质上是在尽量扩大“本地通信域”。

也就是把原本：

```text
100 µs 远程访问
```

尽量变成：

```text
更低延迟、更高带宽的局部访问
```

---

## 3. 加速器系统重新引入 scale-up 需求

对于 GPU/TPU 集群，单节点或单机架内的 scale-up 很重要。

例如：

```text
8 个 GPU 紧耦合
16 个加速器紧耦合
一个机架内加速器高速互连
```

这可以减少通信惩罚。

但当模型和数据规模继续增大时，仍然需要跨机架、跨 Pod、跨集群 scale-out。

所以现代 AI 基础设施是：

```text
局部 scale-up
全局 scale-out
```

---

# 二十二、这一节的核心思想总结

这一节最重要的不是公式本身，而是它给出的思维方式。

---

## 1. 不要只看单机性能

高端 SMP 单机很快，但 WSC 应用通常放不进单机。

---

## 2. 不要只看处理器价格

低端服务器便宜，但集群通信慢。

真正要比较的是：

```text
总性能 / 总成本
```

---

## 3. 通信模式决定 scale-out 损失

```text
轻通信：scale-out 损失小
中通信：scale-out 有损失但可接受
高通信：scale-out 损失大
```

---

## 4. 最大损失来自从单机到多机

从：

```text
N = 1
到
N = 2
```

远程访问比例从 0 跳到 50%。

之后增加节点，远程比例增长越来越慢。

---

## 5. 当系统规模很大时，高端服务器优势被稀释

如果应用需要几千核：

```text
高端集群和低端集群的大多数访问都是远程访问。
```

因此高端服务器的本地通信优势只影响一小部分访问。

如果高端服务器价格贵 4–20 倍，而性能只快 5%，那么不划算。

---

## 6. WSC 设计关心 warehouse-scale 成本效率

原文最后的核心是：

> Performance effects that matter most are those that benefit the system at the warehouse scale.

真正重要的是：

```text
在整个数据中心规模下有效的性能提升
```

而不是：

```text
只在单台机器内有效但成本很高的性能提升
```

---

# 二十三、这一节可以整理成的精简笔记

```text
6.1.2.1 A model to reason about scale-up versus scale-out

1. 简单成本分析认为：
   - 一台 N×M 大服务器比 N 台 M 小服务器贵很多。
   但它忽略了：
   - 大型 SMP 内部通信远快于集群网络通信。

2. 通信延迟差异：
   - SMP 内部访问：约 100 ns
   - LAN 远程访问：约 100 µs
   - 相差约 1000 倍

3. 如果应用能放进单台大型 SMP：
   - 全局访问大多是本地访问
   - 高通信负载下性能优势明显
   - 可能比集群快 10 倍以上
   - 例如 SAP HANA 这类适合大 SMP 的应用

4. 但 WSC 应用通常太大，无法放进单台 SMP。
   因此需要比较：
   - 大型 SMP 服务器集群
   - 低端小服务器集群

5. 简单模型：
   time = 1ms + f · (100ns · LocalFraction + 100µs · RemoteFraction)

   若访问均匀分布：
   LocalFraction = 1/N
   RemoteFraction = (N - 1)/N

   所以：
   time = 1ms + f · (1/N · 100ns + (N - 1)/N · 100µs)

6. f 表示每个 1ms 工作单元的全局访问次数：
   - f = 1：轻通信
   - f = 10：中通信
   - f = 100：高通信

7. 模型结论：
   - 轻通信时，多节点性能损失小。
   - 中高通信时，性能损失严重。
   - 最严重损失发生在 N=1 到 N=2。
   - 继续增加节点，额外损失迅速减小。

8. 单机 128 核 SMP 相对 32 台 4 核服务器集群：
   - 在高通信模式下可能快 10 倍以上。

9. 但 WSC 通常有数千核。
   比较 128 核高端服务器集群和 4 核低端服务器集群时：
   - 高端服务器优势随集群规模增加迅速下降。
   - 超过 2000 核时，512 台低端服务器与 16 台高端服务器性能差约 5%。
   - 高端服务器价格溢价 4–20 倍，因此成本效率差。

10. 核心结论：
   - 单节点性能增强仍然重要。
   - 但如果成本高，只利于单节点的性能增强在 WSC 规模下可能不划算。
   - WSC 平台选择应关注 warehouse-scale 的成本效率，而不是单机极致性能。
```

---

# 二十四、如果考试或讨论中要回答这一节，可以这样说

你可以这样概括：

> 6.1.2.1 节用一个简单模型分析 scale-up 与 scale-out 的权衡。虽然低端服务器集群在处理器成本效率上通常优于大型 SMP 服务器，但大型 SMP 的优势在于内部通信延迟极低，约为 100 ns，而集群网络访问延迟约为 100 µs，二者相差约 1000 倍。因此，对于能够放入单台大型 SMP 的高通信并行应用，scale-up 可能带来显著性能优势。模型将任务执行时间建模为固定本地计算时间加上全局访问延迟惩罚。假设每个工作单元本地计算约 1 ms，全局访问次数为 f，本地访问比例约为 1/N，远程访问比例约为 (N-1)/N。随着节点数增加，远程访问比例迅速上升，性能惩罚在从单节点到两节点时最明显，之后增加节点带来的额外惩罚逐渐减小。对于高通信负载，单台 128 核 SMP 可能比 32 台 4 核服务器集群快 10 倍以上。但 WSC 系统通常包含数千核心，应用往往无法放入单台 SMP。此时比较大型 SMP 集群和低端服务器集群，高端服务器的优势会随着集群规模扩大而迅速缩小。例如在超过 2000 核时，512 台低端服务器与 16 台高端服务器性能差距可能只有约 5%，而高端服务器价格可能贵 4 到 20 倍，因此成本效率不具吸引力。该模型说明，在 warehouse scale 下，真正重要的是整个系统的成本效率，而不是单节点内部的极致性能。

---

# 二十五、最后给你一个形象类比

可以把这一节理解成“办公室沟通效率”。

---

## 单台大 SMP：一个巨型办公室

```text
128 个人坐在同一个大办公室
沟通靠面对面说话
延迟很低
```

如果任务需要频繁沟通，这个办公室效率很高。

---

## 低端服务器集群：很多小办公室

```text
32 个小办公室
每个办公室 4 个人
办公室之间靠打电话沟通
```

打电话比面对面慢很多。

如果任务需要频繁跨办公室沟通，效率会下降。

---

## WSC 规模：整个城市办公

当任务大到需要几千人参与时：

```text
无论用大办公室还是小办公室，
大多数沟通都要跨办公室甚至跨楼。
```

这时大办公室的优势被稀释。

如果大办公室租金贵 10 倍，但整体效率只高 5%，那么就不划算。

这就是这一节的核心：

> 在 warehouse scale 下，选择基础平台不能只看单机通信优势，而要看整个分布式系统的总成本和总性能。

---

**专栏导航**

- ← 上一篇：[6.1 WSC building blocks and design considerations](/posts/6-1-wsc-building-blocks-and-design-considerations/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores →](/posts/6-1-2-2-granularity-of-scale-out-brawny-versus-wimpy-cores/)
