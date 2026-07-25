---
title: "7.1.2 Case study: Library optimizations"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：7.1.2 Case study: Library optimizations。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.1.2 Case study: Library optimizations。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.1.2 Case study: Library optimizations

下面把 **7.1.2 Case study: Library optimizations** 作为一个独立小节来深入理解，并在最后附上和你前面风格一致的**精简笔记版**。

---

### 7.1.2 Case study: Library optimizations 深入理解

这一节是 7.1 “Software-defined servers” 的一个具体案例。前面原文讲的是软件定义服务器的整体思想：  
软件要能理解硬件、配置硬件、调度硬件，从而让应用和硬件更好匹配。

而这一节把视角下沉到一个非常基础但非常重要的地方：

> 共享基础软件库，例如内存分配器、RPC、加密库等，也可以做硬件感知优化。

它说明了一件事：

> 软件定义服务器不只是集群调度器的事，也不只是操作系统的事；  
> 底层 runtime 和基础库同样可以成为软件定义基础设施的一部分。

---

#### 一、为什么库优化如此重要？

原文一开始提出一个关键概念：

> data center tax，数据中心税。

很多软件栈都共享一些基础组件，例如：

- memory management，内存管理；
- RPC，远程过程调用；
- encryption，加密；
- compression，压缩；
- serialization，序列化；
- logging，日志；
- monitoring，监控。

这些组件不是某个应用独有的，而是几乎所有服务都要支付的基础开销。

原文说：

> 这些组件在 WSC 环境中可能消耗高达 30% 的处理周期。

这意味着：

> 如果一个基础库能提升 10%，那么整个数据中心的收益会被放大到所有应用上。

这就是库优化的价值：

|优化对象|影响范围|
| ------------| --------------------------------|
|单个应用|只影响该应用|
|基础库|影响所有依赖该库的应用|
|内存分配器|影响几乎所有需要分配内存的服务|

所以原文把库优化作为 software-defined servers 的案例，非常自然：  
因为基础库是软件栈中最适合做“全局放大式优化”的位置之一。

---

#### 二、本节案例：内存分配器中的 hugepage 优化

这一节重点讲的是：

> 优化内存分配器中的 hugepage coverage，也就是巨页覆盖率。

要理解这个优化，需要先理解两个背景：

1. TLB miss 是 WSC 中的重要性能瓶颈；
2. hugepage 可以减少 TLB miss，但也可能增加内存浪费。

---

### 三、背景：为什么 TLB miss 在 WSC 中很重要？

原文说：

> Cache and TLB misses are major performance bottlenecks in WSCs; around 20% of cycles in WSCs are stalled due to TLB misses.

也就是说：

> 在 WSC 中，大约 20% 的 CPU 周期因为 TLB miss 而停顿。

这个比例非常高。

---

#### 1. TLB 是什么？

TLB，Translation Lookaside Buffer，翻译旁路缓冲区。

它缓存的是：

> 虚拟地址到物理地址的映射。

现代程序使用虚拟地址，CPU 访问内存时，需要把虚拟地址翻译成物理地址。

如果每次翻译都查页表，代价很高。  
因此 CPU 使用 TLB 来缓存最近用过的页表项。

简化流程如下：

```text
CPU 访问虚拟地址
    ↓
查 TLB
    ↓
如果命中：得到物理地址，继续访问内存
如果未命中：发生 TLB miss，需要查页表
```

---

#### 2. TLB miss 为什么昂贵？

TLB miss 可能导致：

- 访问多级页表；
- 多次内存访问；
- 增加延迟；
- 降低指令流水线效率；
- 增加 cache 压力。

如果程序工作集很大，TLB 无法覆盖常用地址，就会频繁 miss。

在 WSC 应用中尤其严重，因为很多服务有：

- 很大的内存 footprint；
- 很多并发连接；
- 很多对象；
- 很大的堆；
- 多租户共享；
- 长时间运行；
- 复杂数据结构。

所以 TLB miss 成为数据中心级性能问题。

---

### 四、Hugepages 是什么？

原文说：

> Hugepages are TLB entries that cover a much larger block of memory, from several megabytes to several gigabytes.

更准确地说：

> hugepage 是更大的内存页；  
> 一个 hugepage 对应的 TLB entry 可以覆盖更大的地址范围。

普通页通常是：

```text
4 KiB
```

而 hugepage 可能是：

```text
2 MiB
1 GiB
```

甚至更大。

---

#### 1. Hugepage 为什么能减少 TLB miss？

假设一个程序访问 1 GiB 内存。

如果使用 4 KiB 页：

```text
1 GiB / 4 KiB = 262,144 个页
```

需要很多 TLB entries 才能覆盖。

如果使用 2 MiB hugepage：

```text
1 GiB / 2 MiB = 512 个页
```

需要的 TLB entries 大幅减少。

如果使用 1 GiB hugepage：

```text
1 GiB / 1 GiB = 1 个页
```

当然实际系统不会总是使用 1 GiB 页，但这个例子说明：

> 页越大，覆盖同样内存所需的 TLB entry 越少。

因此：

> hugepage 可以显著减少 TLB miss。

---

#### 2. 但 hugepage 也有代价

原文马上指出问题：

> But the larger a page, the higher the risk that internal fragmentation within that page causes physical memory to be unused.

也就是说：

> 页越大，内部碎片导致物理内存浪费的风险越高。

---

##### 什么是内部碎片？

假设一个 hugepage 是 2 MiB。

如果某个应用只需要 100 KiB，但系统给它分配了一整个 2 MiB hugepage，那么剩下的大部分内存可能无法被有效使用。

这就是：

> internal fragmentation，内部碎片。

页越大，单个页内未被利用的空间可能越多。

---

#### 3. 因此关键不是“多用 hugepage”，而是“用好 hugepage”

这里有一个典型系统权衡：

|目标|手段|风险|
| ---------------| ------------------------------| -------------------|
|减少 TLB miss|使用更多 hugepage|可能增加内存浪费|
|减少内存浪费|少用 hugepage 或更细粒度分配|可能增加 TLB miss|

所以原文强调：

> optimizing hugepage coverage

不是简单地说：

> 全部使用 hugepage。

而是要让 hugepage 的覆盖范围和利用率达到最佳平衡。

---

### 五、TCMalloc 是什么？

原文引入 TCMalloc：

> TCMalloc is a memory allocator often used in large-scale distributed applications.

TCMalloc 是 Google 常用的一种高性能内存分配器。  
TCMalloc 的名字来自：

> Thread-Caching Malloc。

它的核心目标是：

- 降低分配延迟；
- 减少锁竞争；
- 提高多线程扩展性；
- 改善内存局部性；
- 降低碎片；
- 更好地利用 hugepage。

---

### 六、TCMalloc 的内存组织方式

原文描述了 TCMalloc 的基本结构。

---

#### 1. 对象按大小分类

原文说：

> Objects are segregated by size.

也就是说，不同大小的对象不会随便混在一起，而是按大小分开管理。

这很关键。

如果大小对象混放，会导致：

- 小对象之间留下空洞；
- 大对象无法放入已有空间；
- 页难以整体释放；
- hugepage 利用率下降。

按大小分类后，同一类对象可以更紧凑地排列。

---

#### 2. 内存被划分成 spans

原文说：

> TCMalloc partitions memory into spans, aligned to page size.

span 是 TCMalloc 管理内存的基本单位之一。

可以粗略理解为：

> 一段连续的页，或者一段连续内存区域。

span 对齐到 page size，这有利于：

- 页级管理；
- hugepage 对齐；
- 操作系统交互；
- 内存回收；
- 减少碎片。

---

#### 3. 大对象单独占用 span

原文说：

> Sufficiently large allocations are fulfilled with a span containing only the allocated object.

也就是说：

> 足够大的分配会由一个只包含该对象的 span 满足。

这避免大对象和小对象混在一起。

例如：

```text
一个大对象 = 一个独立 span
```

好处是：

- 管理简单；
- 释放时可以直接归还整个 span；
- 不会因小对象卡住导致大 span 无法回收。

---

#### 4. 小对象共享 span

原文说：

> Other spans contain multiple smaller objects of the same size, a size class.

对于小对象，TCMalloc 会把它们按 size class 分组。

一个 span 中可能存放多个相同 size class 的小对象。

例如：

```text
size class = 32 bytes
一个 span 里放很多 32 bytes 对象
```

或者：

```text
size class = 128 bytes
一个 span 里放很多 128 bytes 对象
```

这样做的好处是：

- 减少内部碎片；
- 提高内存密度；
- 改善 cache locality；
- 更容易填满 hugepage；
- 更容易整页回收。

---

#### 5. 小对象边界是 256 KiB

原文说：

> The “small” object size boundary is 256 KiB.

也就是说：

```text
小于等于 256 KiB 的分配：small object
大于 256 KiB 的分配：large object
```

对于 small object：

- 分配请求会被 round up 到某个 size class；
- 然后从对应 size class 的缓存或 span 中分配。

原文说：

> Within this “small” threshold, allocation requests are rounded up to one of 100 size classes.

例如应用请求：

```text
37 bytes
```

TCMalloc 可能把它归类到：

```text
48 bytes
```

或者某个接近的 size class。

这会带来少量内部碎片，但换来：

- 更快分配；
- 更好复用；
- 更紧凑布局；
- 更适合 hugepage 管理。

---

### 七、TCMalloc 的 hugepage 优化目标

原文说：

> The objective is to maximize the utilization of hugepages.

目标不是简单使用 hugepage，而是：

> 最大化 hugepage 的利用率。

这包含两个互相配合的目标。

---

#### 目标 1：把活跃对象紧密打包到常用 hugepages 上

原文说：

> Heuristics enable the allocator to pack objects tightly onto frequently used hugepages.

也就是说，TCMalloc 会尽量把对象集中放到正在使用的 hugepage 中。

这样可以：

- 提高 hugepage 填充率；
- 减少活跃 hugepage 数量；
- 让活跃地址范围更集中；
- 提高 TLB 覆盖率；
- 减少 TLB miss。

---

#### 目标 2：制造完全空闲的 hugepages 归还操作系统

原文继续说：

> while also creating fully unused hugepages for return to the operating system.

也就是说，TCMalloc 不只是把内存塞满，还会尽量腾出完全空闲的 hugepage。

完全空闲的 hugepage 可以：

- 归还操作系统；
- 降低进程 RSS；
- 降低 RAM 使用；
- 给其他服务使用；
- 提高整机内存利用率。

这解释了为什么原文最后说：

> RAM usage decreased 2.4%.

因为优化后的分配器不仅提升性能，还减少了内存浪费。

---

### 八、HugeAllocator、HugeCache、HugeFiller 的作用

原文提到三个关键组件。

---

#### 1. HugeAllocator

原文说：

> The main component, called HugeAllocator, deals with virtual memory and the operating system.

HugeAllocator 是主要负责 hugepage 内存管理的组件。

它处理：

- 虚拟内存；
- 与操作系统交互；
- hugepage 的申请；
- hugepage 的释放；
- hugepage 的管理。

可以理解为：

> HugeAllocator 是 TCMalloc 与 OS 虚拟内存系统之间的桥梁。

---

#### 2. HugeCache

原文说：

> a cache of fully-empty hugepages called the HugeCache.

HugeCache 缓存的是：

> 完全空闲的 hugepages。

为什么需要缓存完全空闲 hugepage？

因为如果每次需要 hugepage 都立刻向 OS 申请，每次释放都立刻归还 OS，可能带来：

- 系统调用开销；
- 页表更新开销；
- TLB shootdown 开销；
- 分配延迟波动。

所以 TCMalloc 可以保留一些完全空闲 hugepage 在 HugeCache 中，以便快速复用。

---

#### 3. HugeFiller

原文说：

> a list of partially filled single hugepages, referred to as the HugeFiller, is densely filled by subsequent small allocations.

HugeFiller 管理的是：

> 部分填充的 hugepages。

它的作用是：

> 后续的小分配优先填充这些部分使用的 hugepage，而不是打开新的 hugepage。

这有助于：

- 提高已有 hugepage 的填充率；
- 减少半满 hugepage 数量；
- 让某些 hugepage 有机会被完全腾空；
- 最终提高 hugepage 利用率。

---

### 九、如何直观理解这个优化？

可以用一个“装箱”类比。

假设 hugepage 是一个大集装箱。

---

#### 策略 1：随便放

如果来了货物就随便放进一个集装箱：

- 很多集装箱半满；
- 没有集装箱完全空；
- 需要运输的集装箱数量很多；
- 无法把空集装箱退回去。

这对应：

> TLB 覆盖浪费，内存也浪费。

---

#### 策略 2：密集装箱

TCMalloc 的策略是：

- 尽量把货物集中装进少数集装箱；
- 把某些集装箱装满；
- 让另一些集装箱完全空出来；
- 完全空的集装箱可以退回仓库。

这对应：

- 活跃内存集中在少数 hugepages；
- TLB 覆盖更有效；
- 完全空闲 hugepages 可归还 OS；
- 内存使用下降。

---

### 十、为什么这个优化能同时改善性能和内存？

原文给出的结果非常漂亮：

> Using a memory allocator that is aware of hugepages led to:
>
> - 7.7% performance improvement；
> - 2.4% decrease in RAM usage；
> - 6% fewer stalls due to TLB misses；
> - 26% reduction in memory waste caused by fragmentation.

这四个指标可以一起理解。

---

#### 1. 为什么性能提升 7.7%？

因为：

- TLB miss 减少；
- 地址翻译更快；
- 内存访问停顿减少；
- 程序工作集更容易被 TLB 覆盖；
- CPU 流水线更少因地址翻译停滞。

原文也给出直接原因：

> TLB miss 导致的 stall 减少 6%。

这会直接转化为性能提升。

---

#### 2. 为什么 RAM usage 反而下降 2.4%？

直觉上，hugepage 更大，似乎更容易浪费内存。

但优化后的 TCMalloc 通过：

- 更紧密打包；
- 更少半满 hugepage；
- 更多完全空闲 hugepage；
- 更高效归还 OS；
- 减少碎片；

反而降低了总体 RAM 使用。

这说明：

> hugepage 优化的关键不是“多用大页”，而是“提高大页利用率”。

---

#### 3. 为什么 TLB stall 减少 6%？

因为活跃内存被更集中地覆盖在更少的 hugepages 中。

原本可能需要很多小页才能覆盖的工作集，现在可以用更少的 hugepage 覆盖。

因此 TLB 命中率提高。

---

#### 4. 为什么碎片浪费减少 26%？

因为 TCMalloc：

- 按 size class 分类对象；
- 小对象密集填充；
- 优先填充部分使用的 hugepage；
- 避免 hugepage 半满散落；
- 更容易形成完全空闲 hugepage。

所以内部碎片和布局浪费显著下降。

---

### 十一、这一节如何体现 software-defined servers？

这一节看起来是在讲内存分配器，但它其实体现了 software-defined servers 的核心思想。

---

#### 1. 软件理解硬件瓶颈

TCMalloc 知道：

- TLB 是瓶颈；
- hugepage 能减少 TLB miss；
- 大页也有碎片风险；
- 页大小会影响地址翻译效率。

这就是：

> software understands hardware behavior.

---

#### 2. 软件主动管理硬件资源

TCMalloc 不只是调用 `malloc`，而是主动管理：

- 虚拟内存；
- 页大小；
- hugepage 覆盖；
- 对象布局；
- 内存归还；
- 碎片控制。

这就是：

> software controls hardware resource usage.

---

#### 3. 软件根据工作负载动态优化

TCMalloc 使用启发式决定：

- 哪些对象放在一起；
- 哪些 hugepage 应该继续填充；
- 哪些 hugepage 应该腾空；
- 哪些 hugepage 应该缓存；
- 哪些 hugepage 应该归还 OS。

这就是：

> dynamic, workload-aware optimization.

---

#### 4. 基础库成为效率层的一部分

在前面原文的 Figure 7.1 中，software-defined servers 有：

- abstraction layer；
- efficiency layer。

TCMalloc 可以看作 efficiency layer 的一部分。

它通过库层面的优化，把底层硬件特性转化为应用性能收益。

---

### 十二、这一节的关键系统权衡

这一节最值得记住的不是 TCMalloc 的每个组件，而是它背后的系统权衡。

---

#### 权衡 1：TLB 覆盖率 vs 内存浪费

```text
更多 hugepage
    → 更少 TLB miss
    → 但可能更多内部碎片
```

---

#### 权衡 2：快速分配 vs 内存紧凑

```text
简单分配策略
    → 分配快
    → 但可能布局差、碎片多
```

TCMalloc 通过 size class 和 hugepage packing 在两者之间取得平衡。

---

#### 权衡 3：缓存空闲 hugepage vs 归还 OS

```text
保留空闲 hugepage
    → 分配更快
    → 但占用内存

归还空闲 hugepage
    → 降低 RAM 使用
    → 但可能增加后续分配成本
```

HugeCache 就是用来平衡这个矛盾的。

---

#### 权衡 4：局部最优 vs 全局最优

单个分配请求可能只希望：

> 快速拿到内存。

但分配器还要考虑：

- 整个堆的布局；
- hugepage 利用率；
- 未来释放；
- OS 内存压力；
- 其他应用；
- 整机内存效率。

这就是数据中心级系统设计和单机程序设计的不同。

---

### 十三、如果只记几个核心点

可以记这几条：

1. **data center tax**  
   基础库开销在 WSC 中非常大，可能消耗 30% CPU cycles。
2. **TLB miss 是 WSC 中的重要瓶颈**  
   原文说约 20% cycles 因 TLB miss 停顿。
3. **hugepages 可以减少 TLB miss**  
   因为一个 TLB entry 覆盖更大内存范围。
4. **hugepages 也可能造成内部碎片**  
   页越大，未用空间浪费风险越高。
5. **TCMalloc 通过 size class 和 hugepage packing 优化**  
   小对象按大小分类，密集填充 hugepage。
6. **HugeAllocator / HugeCache / HugeFiller 协同工作**

   - HugeAllocator：管理虚拟内存和 OS 交互；
   - HugeCache：缓存完全空闲 hugepage；
   - HugeFiller：继续填充部分使用的 hugepage。
7. **结果是性能和内存同时改善**

   - 性能提升 7.7%；
   - RAM 使用下降 2.4%；
   - TLB stall 下降 6%；
   - 碎片浪费下降 26%。

---

### 十四、可以加入你的笔记中的精简版

下面这一段可以直接加入你的笔记，风格与前面的 `7.1` 精简笔记一致。

```text
7.1.2 Case study: Library optimizations

1. 背景：data center tax
   - 很多软件栈共享基础组件：
     - memory management
     - RPC
     - encryption
     - 等
   - 这些组件称为 data center tax
   - 在 WSC 中可能消耗高达 30% CPU cycles
   - 因此优化基础库有巨大放大效应

2. 本节案例：
   - 优化内存分配器中的 hugepage coverage
   - 代表 hardware-aware library optimization

3. 为什么关注 TLB：
   - Cache 和 TLB miss 是 WSC 主要瓶颈
   - 约 20% cycles 因 TLB miss 停顿
   - WSC 应用通常内存 footprint 大
   - TLB 覆盖不足会显著降低性能

4. Hugepages：
   - 普通页通常较小，例如 4 KiB
   - hugepage 覆盖更大内存范围，例如 MiB 到 GiB 级
   - 一个 hugepage 对应更大的 TLB 覆盖范围
   - 因此可以显著减少 TLB miss

5. Hugepage 的代价：
   - 页越大，内部碎片风险越高
   - 如果 hugepage 未被充分利用，会浪费物理内存
   - 关键不是“多用 hugepage”，而是“提高 hugepage 利用率”

6. TCMalloc 基本结构：
   - 对象按大小分类
   - 内存被划分为 spans，对齐 page size
   - 大对象：
     - 单独占用一个 span
   - 小对象：
     - 多个相同 size class 的对象共享 span
   - small object 边界：
     - 256 KiB
   - 小于 256 KiB 的请求：
     - round up 到约 100 个 size classes 之一

7. TCMalloc hugepage 优化目标：
   - 最大化 hugepage 利用率
   - 两个方向：
     a. 把对象紧密打包到常用 hugepages
     b. 制造完全空闲 hugepages 归还 OS

8. 关键组件：
   - HugeAllocator：
     - 处理虚拟内存
     - 与操作系统交互
   - HugeCache：
     - 缓存完全空闲 hugepages
     - 便于快速复用
   - HugeFiller：
     - 管理部分填充的 hugepages
     - 后续小分配优先密集填充这些页

9. 优化效果：
   - 性能提升 7.7%
   - RAM 使用下降 2.4%
   - TLB miss 导致的 stall 减少 6%
   - 碎片导致的内存浪费减少 26%

10. 为什么能同时提升性能并降低内存：
   - 更密集的对象打包
   - 更少半满 hugepages
   - 更多完全空闲 hugepages
   - 更少碎片
   - 更高 TLB 覆盖率
   - 更少地址翻译停顿

11. 与 software-defined servers 的关系：
   - 基础库也可以 hardware-aware
   - 内存分配器理解 TLB、page size、内存层级等硬件特性
   - 通过软件优化底层资源使用
   - 是 software-defined server 效率层的一部分

12. 核心逻辑：
   data center tax 很重
     → 基础库优化收益大
     → TLB miss 是主要瓶颈
     → hugepages 可减少 TLB miss
     → 但 hugepages 可能浪费内存
     → TCMalloc 通过 size class + hugepage packing 优化
     → 同时提升性能、降低内存浪费
```

---

### 十五、一句话总结这一节

> 7.1.2 通过 TCMalloc 说明：软件定义服务器不只是宏观调度异构硬件，也可以通过基础库的硬件感知优化，在内存管理这种“数据中心税”上获得显著的性能和内存收益。


**专栏导航**

- ← 上一篇：[7.1 Software-defined servers](/posts/7-1-software-defined-servers/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.1.3 Case study: Platform-aware scheduling →](/posts/7-1-3-case-study-platform-aware-scheduling/)
