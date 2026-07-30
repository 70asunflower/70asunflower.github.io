---
title: "6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-23
description: "《The Data Center as a Computer》AI 导读专栏正文：6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores

下面我结合你提供的原文，把 **6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores** 这一节读深。

这一节承接上一节的 scale-up vs scale-out 模型，进一步追问：

> 如果我们已经选择了 scale-out，那么 scale-out 的“颗粒度”应该多细？  
> 是应该使用少量很强的 CPU 核心，还是使用大量很简单、很省电的小核心？  
> 这就是所谓的：  
> **brawny cores vs wimpy cores**  
> 强核 vs 弱核。

---

### 一、这一节的核心问题：scale-out 的粒度应该多细？

上一节讨论的是：

```text
大型 SMP 服务器
vs
低端服务器集群
```

这一节进一步问：

```text
既然低端服务器更划算，
那是不是可以把服务器做得更小、核心做得更弱、数量做得更多？
```

也就是说，scale-out 可以有不同粒度。

---

#### 1. 粗粒度 scale-out

例如：

```text
少量大型服务器
每台服务器有强 CPU
每个核心单线程性能高
```

这对应：

```text
brawny cores
强核
```

---

#### 2. 细粒度 scale-out

例如：

```text
大量小服务器
每台服务器使用低功耗、低性能核心
核心数量多，但单核较弱
```

这对应：

```text
wimpy cores
弱核
```

---

#### 3. 问题本质

问题不是简单地问：

```text
强核好还是弱核好？
```

而是问：

```text
对于特定工作负载，
在成本、功耗、延迟、吞吐、软件开发复杂度、资源利用率之间，
哪种核心粒度更合适？
```

---

### 二、历史上对 wimpy cores 的探索

原文列举了几个代表性项目。

---

#### 1. Piranha：早期多核低功耗服务器探索

原文说：

> The Piranha chip multiprocessor was one of the earliest systems to advocate the use of lower-end cores in enterprise-class server systems.

Piranha 是较早期的研究，主张：

```text
用很多低端核心构建服务器系统
```

它的思想是：

```text
不追求单个核心极快，
而是通过大量核心获得总吞吐。
```

---

#### 2. Lim et al.：低功耗核心用于服务器平台

原文说：

> Lim et al. made the case for low-end power-efficient processor cores in server platforms.

这项研究强调：

```text
低功耗核心
能效高
适合服务器平台
```

它推动了后来 HP Moonshot 服务器。

---

#### 3. HP Moonshot：高密度 ARM / mobile-x86 服务器

原文说：

> This work led to HP’s Moonshot Servers that had 45 ARM-based or mobile-x86-based blade servers in one 4.3U enclosure.

HP Moonshot 的特点是：

```text
4.3U 机箱
45 个刀片服务器
使用 ARM 或 mobile-x86 核心
```

它试图通过：

```text
高密度
低功耗
低成本
```

来服务某些 Web 和轻量级工作负载。

---

#### 4. Hamilton：PC 级组件构建数据中心

原文说：

> Hamilton made a similar argument for PC-class components, setting the stage for Amazon’s Graviton-based line of ARM servers.

Hamilton 主张使用：

```text
PC-class components
个人电脑级组件
```

而不是昂贵企业级组件。

这种思想影响了后来的：

```text
Amazon Graviton
AWS ARM 服务器
```

---

#### 5. FAWN：<span data-type="text" style="color: var(--b3-font-color11);">弱核 + Flash 构建高效存储系统</span>

原文说：

> The FAWN project explored the utility of wimpy cores as the basis for building an energy efficient key-value storage system using flash memory.

FAWN，Fast Array of Wimpy Nodes，意思是：

```text
由弱节点组成的高速阵列
```

它使用：

```text
wimpy cores
flash memory
```

构建：

```text
key-value storage system
```

它关注的不是 CPU 密集型计算，而是：

```text
I/O-bound
memory-bound
存储服务器
```

也就是说，<span data-type="text" style="color: var(--b3-font-color11);">对于某些存储负载，CPU 不需要特别强，</span>关键是：

```text
I/O 吞吐
内存效率
能耗效率
```

---

### 三、为什么有人主张使用 wimpy cores？

原文总结了几个优势。

---

#### 1. <span data-type="text" style="color: var(--b3-font-color11);">低端 CPU 的价格性能更好</span>

原文说：

> Multicore CPUs in mid-range servers typically carry a price-performance premium over lower-end processors so that the same amount of throughput can be bought two to five times cheaper with multiple smaller CPUs.

也就是说：

```text
中端服务器 CPU 往往有价格溢价。
```

如果你要买同样总吞吐量，使用多个低端 CPU 可能便宜：

```text
2 到 5 倍
```

---

##### 直观例子

假设你需要 1000 单位吞吐。

方案 A：

```text
1 颗高端 CPU
性能 1000
价格 $5000
```

方案 B：

```text
10 颗低端 CPU
每颗性能 100
总性能 1000
总价 $1500
```

那么方案 B 的价格性能更好。

当然，这只是理想情况。实际还要考虑：

```text
主板
内存
网络
机柜
电源
软件复杂度
运维成本
```

但基本思想是：

```text
低端核心更容易获得好的价格性能比。
```

---

#### 2<span data-type="text" style="color: var(--b3-font-color11);">. 很多应用是内存或 I/O 瓶颈，不是 CPU 瓶颈</span>

原文说：

> Many applications are memory- or I/O-bound so that faster CPUs do not scale well for large applications, further enhancing the price advantage of simpler CPUs.

很多数据中心应用并不是 CPU 密集型。

例如：

```text
对象存储
键值存储
日志服务
消息队列
网络转发
缓存服务
数据分析中的 I/O 阶段
```

这些负载常常受限于：

```text
内存带宽
内存容量
磁盘 I/O
网络带宽
序列化/反序列化
锁竞争
```

如果瓶颈不是 CPU，那么更快的 CPU 带来的收益有限。

例如：

```text
CPU 提升 2 倍
但应用只快 10%
```

这时为更快 CPU 付高价就不划算。

---

#### 3. <span data-type="text" style="color: var(--b3-font-color11);">慢 CPU 通常更省电</span>

原文说：

> Slower CPUs tend to be more power efficient. Typically, CPU power decreases by O(k²) when CPU frequency decreases by a factor of k.

这里涉及 CPU 功耗模型。

---

##### 动态功耗近似公式

CPU 动态功耗大致满足：

```text
P ∝ C × V² × f
```

其中：

```text
C：负载电容
V：电压
f：频率
```

如果频率降低 k 倍，同时电压也降低，那么功耗可能近似降低：

```text
O(k²)
```

也就是说：

```text
频率降低
功耗下降更快
```

这使得弱核在能效上可能有优势。

---

##### 举例

假设某核心频率降低：

```text
2 倍
```

如果电压也下降，功耗可能降低约：

```text
4 倍
```

当然性能也会下降，但对于高度并行、吞吐导向的负载，可能：

```text
每瓦吞吐更好
```

---

### 四、wimpy cores 的风险：不是所有负载都能无限并行

原文接着提醒：

> At the same time, there are perils in going down this path too indiscriminately.

也就是说，不能不加区分地全面转向弱核。

原因有几个。

---

### 五、风险一：<span data-type="text" style="color: var(--b3-font-color11);">Amdahl 定律仍然有效</span>

原文说：

> although many internet services benefit from seemingly unbounded request- and data-level parallelism, such systems are not immune from Amdahl’s law.

很多互联网服务看起来可以无限并行，因为：

```text
请求级并行：
  很多用户请求彼此独立

数据级并行：
  数据可以分片处理
```

但它们仍然受 Amdahl 定律限制。

---

#### 1. Amdahl 定律是什么？

Amdahl 定律说明：

> 如果程序中有一部分必须串行执行，那么增加再多处理器也无法无限加速。

<span data-type="text" style="color: var(--b3-font-color11);">假设程序中串行部分比例是：</span>

```text
s
```

并行部分比例是：

```text
1 - s
```

使用 N 个处理器时，加速比约为：

```text
Speedup = 1 / (s + (1 - s)/N)
```

当 N 很大时：

```text
Speedup -> 1/s
```

---

#### 2. 例子

如果程序有 10% 必须串行：

```text
s = 0.1
```

那么最大加速比是：

```text
1 / 0.1 = 10
```

<span data-type="text" style="color: var(--b3-font-color11);">即使你有 1000 个核心，也只能快约 10 倍。</span>

---

#### 3. 对 wimpy cores 的影响

如果使用很多弱核，那么并行线程数量会增加。

但随着线程数增加：

```text
串行部分
通信开销
同步开销
锁竞争
```

会越来越明显。

原文说：

> In the limit, the amount of inherently serial work performed on behalf of a user request by extremely slow single-threaded hardware will dominate overall execution time.

也就是说，如果单线程硬件太慢，那么用户请求中必须串行的部分会被放大。

例如：

```text
请求解析
权限检查
事务顺序
状态更新
全局排序
一致性检查
```

这些工作可能很难并行。

如果单核很慢，这些串行部分就会拖慢整体延迟。

---

### 六、风险二：<span data-type="text" style="color: var(--b3-font-color11);">尾延迟问题会被放大</span>

原文说：

> the more threads handle a parallelized request, the larger the variability in response times from all these parallel tasks will be, exacerbating the tail latency problem.

<span data-type="text" style="color: var(--b3-font-color11);">如果一个请求被拆成很多并行任务，那么整体响应时间往往取决于最慢的那个子任务。</span>

---

#### <span data-type="text" style="color: var(--b3-font-color11);">1. 扇出越多，越容易被慢任务拖累</span>

假设一个请求需要 100 个并行子任务：

```text
subtask 1
subtask 2
...
subtask 100
```

整体延迟可能是：

```text
max(subtask latencies)
```

即使 99 个子任务都很快，只要 1 个很慢，整体请求就慢。

---

#### <span data-type="text" style="color: var(--b3-font-color11);">2. 弱核可能增加延迟波动</span>

弱核通常：

```text
缓存更小
乱序能力更弱
单线程性能更低
对内存延迟更敏感
```

因此某些任务可能偶尔很慢。

当并行任务数量很大时，这种偶发慢任务会显著影响：

```text
P99 latency
P999 latency
```

这就是尾延迟问题。

---

### 七、风险三：<span data-type="text" style="color: var(--b3-font-color11);">硬件成本下降，但软件开发成本上升</span>

原文说：

> although hardware costs may diminish, software development costs may increase because more applications must be explicitly parallelized or further optimized.

弱核方案可能让硬件更便宜，但软件会更难写。

---

#### <span data-type="text" style="color: var(--b3-font-color11);">1. 强核的好处：单线程性能高</span>

如果核心很强，很多代码不需要深度并行化就能跑得不错。

例如：

```text
单线程逻辑
复杂控制流
缓存局部性好的代码
传统应用
```

可以直接受益于高主频和大缓存。

---

#### <span data-type="text" style="color: var(--b3-font-color11);">2. 弱核的要求：必须充分并行</span>

如果使用大量弱核，开发者必须：

```text
显式并行化
减少锁
减少串行路径
优化数据结构
优化内存访问
减少通信
处理负载不均
```

这会增加工程成本。

---

### 八、原文给出的延迟例子：<span data-type="text" style="color: var(--b3-font-color11);">慢 3 倍核心如何导致延迟翻倍？</span>

原文举了一个很直观的例子。

---

#### 1. 原始服务

假设一个 Web 服务每个用户请求延迟：

```text
1 秒
```

其中一半来自 CPU 时间：

```text
CPU time = 0.5s
non-CPU time = 0.5s
```

<span data-type="text" style="color: var(--b3-font-color11);">non-CPU 时间可能包括：</span>

```text
网络
磁盘
内存等待
RPC
锁等待
```

---

#### 2. 换成单线程慢 3 倍的服务器

如果新服务器单线程性能慢 3 倍，那么 CPU 时间变成：

```text
0.5s × 3 = 1.5s
```

非 CPU 时间不变：

```text
0.5s
```

总延迟变成：

```text
1.5s + 0.5s = 2.0s
```

所以延迟翻倍。

---

#### 3. 工程含义

虽然新服务器可能更便宜，但服务延迟从：

```text
1s -> 2s
```

这可能不可接受。

为了恢复到 1s，开发者可能需要：

```text
并行化 CPU 密集部分
优化算法
减少序列化
减少内存分配
改进缓存
减少系统调用
```

这些都需要工程投入。

---

### 九、风险四：<span data-type="text" style="color: var(--b3-font-color11);">小服务器可能降低资源利用率</span>

原文说：

> Smaller servers may also lead to lower utilization.

小服务器不一定利用率更高。

---

#### 1. 把服务器分配看成 bin packing

原文建议把应用部署看成：

```text
bin packing problem
装箱问题
```

每台服务器是一个 bin。

我们要把很多应用装进这些 bin 里，尽量装满。

---

#### 2. 小 bin 更难装

如果服务器很大：

```text
CPU 多
内存多
```

那么可以同时装很多应用：

```text
App A
App B
App C
App D
```

统计复用效果更好。

如果服务器很小：

```text
CPU 少
内存少
```

可能出现：

```text
App A 占了 70% CPU 和 60% 内存
```

这时它没有装满服务器，但剩余资源又不足以再放一个应用。

结果：

```text
资源浪费
利用率下降
```

---

#### 3. 大服务器 vs 小服务器的利用率权衡

大服务器优点：

```text
更容易装箱
统计复用更好
碎片更少
```

大服务器缺点：

```text
故障域更大
NUMA 更复杂
成本更高
```

小服务器优点：

```text
便宜
故障域小
部署灵活
```

<span data-type="text" style="color: var(--b3-font-color11);">小服务器缺点：</span>

```text
装箱碎片多
利用率可能低
管理数量多
```

---

### 十、风险五：<span data-type="text" style="color: var(--b3-font-color11);">即使 embarrassingly parallel 算法也可能因细分而低效</span>

原文说：

> even embarrassingly parallel algorithms are sometimes intrinsically less efficient when computation and data are partitioned into smaller pieces.

有些算法看起来“令人尴尬地可并行”，也就是几乎不需要通信。

但即使如此，当计算和数据被切得太碎时，也可能变低效。

---

#### 1. 全局停止条件问题

原文举例：

> the stop criterion for a parallel computation is based on global information.

<span data-type="text" style="color: var(--b3-font-color11);">很多并行算法需要知道全局信息才能停止。</span>

例如：

```text
全局误差是否收敛？
全局任务队列是否为空？
全局迭代是否完成？
全局计数是否达到阈值？
```

如果频繁获取全局信息，就需要：

```text
全局通信
全局锁
全局同步
```

这很昂贵。

---

#### 2. 本地启发式更保守

<span data-type="text" style="color: var(--b3-font-color11);">为了避免昂贵全局通信，局部任务可能只看本地进度</span>：

```text
local progress
```

但本地信息不完整，所以启发式往往更保守。

结果是：

```text
局部子任务可能执行得更久
```

因为它们不知道全局已经接近完成。

---

#### 3. <span data-type="text" style="color: var(--b3-font-color11);">分区越小，开销越大</span>

当计算被切成更多小块时：

```text
任务更多
协调更多
终止检测更难
局部保守带来的浪费更多
```

所以即使是可并行算法，也不是切得越细越好。

---

### 十一、<span data-type="text" style="color: var(--b3-font-color11);">Cloud 应用视角：多数客户偏好单 VM 性能</span>

原文说：

> from the perspective of cloud applications, most workloads emphasize single-VM performance, preferring higher-performance cores with a focus on single-threaded performance per VM.

云平台上大多数客户工作负载更看重：

```text
单个 VM 的性能
```

尤其是：

```text
每个 vCPU 的单线程性能
```

---

#### 1. 为什么云客户关心单 VM 性能？

因为很多客户应用并不是为超大规模分布式设计的。

例如：

```text
企业应用
数据库
中间件
内部系统
单体应用
小型 SaaS
开发测试环境
```

这些应用可能无法轻易横向扩展。

客户更希望：

```text
买一个 VM
它就很快
```

而不是：

```text
为了性能必须重写成分布式系统
```

---

#### 2. 数据库例子

原文说：

> a database serving many applications often wants to run on the fastest server available since database performance limits application performance.

数据库常常是很多应用的性能瓶颈。

如果数据库慢，上层应用都慢。

因此数据库通常偏好：

```text
高主频
大缓存
强单线程性能
快内存
```

而不是单纯追求很多弱核。

---

#### <span data-type="text" style="color: var(--b3-font-color11);">3. 大系统更容易切成小 VM，反之不然</span>

原文说：

> a bigger system is more amenable to being deployed and sold as smaller VM shapes, but the converse is not true.

一台大服务器可以切成很多小 VM：

```text
large server -> many small VMs
```

但很多小服务器很难合并成一个大 VM：

```text
many small servers -> one large VM? 很难
```

因此云平台通常偏好足够大的服务器，因为可以提供更多 VM 形状：

```text
small VM
medium VM
large VM
extra-large VM
```

这提高了产品灵活性。

---

### 十二、<span data-type="text" style="color: var(--b3-font-color11);">吞吐导向负载偏好不同：数据分析喜欢高吞吐低成本核心</span>

原文说：

> throughput-oriented workloads like data analytics prefer systems that minimize the cost of computation, leading to servers with somewhat slower cores but higher throughput, and less memory per core to reduce system cost.

吞吐导向负载例如：

```text
数据分析
批处理
日志处理
ETL
对象存储
某些 AI 推理
大规模扫描
```

它们更关心：

```text
每美元吞吐
每瓦吞吐
总计算成本
```

而不是单个请求的极致延迟。

因此它们可以接受：

```text
稍慢核心
更多核心
更少内存每核
```

只要总吞吐足够高。

---

### 十三、CPU 厂商开始提供不同产品线

原文说：

> Recently, CPU vendors have started to provide CPU variants optimized for each of the two scenarios.

现在 CPU 厂商不再只提供一种通用服务器 CPU，而是提供不同优化方向的产品。

---

#### 1. ARM 的产品线

原文说：

```text
ARM offers the “V” series for performance,
the “N” series for scale-out,
and the “E” series for efficiency.
```

可以理解为：

|ARM 系列|优化方向|
| ----------| ----------------|
|V series|高性能|
|N series|scale-out 吞吐|
|E series|能效|

---

#### 2. Intel 的产品线

原文说：

> Intel offers two parallel lines of Xeon processors, again focused on performance and efficiency.

例如 Intel Xeon 有偏性能线和偏效率线。

---

#### 3. AMD 的产品线

原文说：

> AMD offers multiple processor lines in their EPYC systems, optimized for different performance and efficiency design points.

AMD EPYC 也有不同系列，针对不同：

```text
性能
核心数
能效
成本
```

---

### 十四、为什么云厂商的 ARM 处理器成功了？

原文说：

> The success of ARM processors offered by cloud providers illustrates the demand for “brawny” cores.

这里有个很有意思的点：

> ARM 云处理器的成功，并不是因为它们只是“弱核”，而是因为它们提供了足够强的核心，也就是 brawny cores。

例如：

```text
AWS Graviton
GCP Axion
```

它们成功的原因之一是：

```text
提供好的每 vCPU 性能
同时价格更低
```

---

### 十五、为什么当前 ARM VM 价格性能更好？

原文给出两个原因。

---

#### 1. ARM VM 通常 1 vCPU = 1 物理核心

原文说：

> the respective CPUs do not use hyperthreading, and thus 1 vCPU = 1 physical core.

ARM 云 VM 通常不使用 SMT / hyperthreading。

所以：

```text
1 vCPU = 1 physical core
```

---

#### 2. x86 VM 常见 2 vCPU = 1 物理核心

原文说：

> On x86 VMs using two-way hyperthreading, 2 vCPUs = 1 physical core.

在 x86 平台上，常见超线程：

```text
1 physical core = 2 logical CPUs
```

云厂商通常把逻辑 CPU 映射为 vCPU。

因此：

```text
2 vCPUs = 1 physical core
```

---

#### 3. 每 vCPU 性能差异

当比较每 vCPU 性能时：

```text
ARM：
  1 vCPU 是完整物理核心

x86：
  1 vCPU 可能只是物理核心的一个硬件线程
```

所以 ARM VM 的每 vCPU 性能可能明显更强。

---

##### 直观理解

<span data-type="text" style="color: var(--b3-font-color11);">假设一个物理核心有两个硬件线程。</span>

两个线程共享：

```text
缓存
执行单元
内存带宽
分支预测器
```

因此单个硬件线程通常达不到完整物理核心的性能。

如果 ARM 的 vCPU 直接对应完整物理核心，那么单 vCPU 性能自然更好。

---

### 十六、为什么 ARM 服务器更便宜：内存配置差异

原文说：

> they are also cheaper because they have half the physical DRAM per core.

这里需要仔细理解。

---

#### 1. 云 VM 按 vCPU 配置内存

原文说：

> Cloud VMs are provisioned with a standard amount of DRAM per vCPU, not per physical core.

云平台通常有标准 VM 形状，例如：

```text
1 vCPU : 4 GB RAM
2 vCPU : 8 GB RAM
4 vCPU : 16 GB RAM
```

也就是说，内存是按：

```text
每 vCPU
```

配置的，而不是按物理核心。

---

#### 2. x86 使用超线程时，每物理核心对应更多 vCPU

假设一台 x86 服务器有：

```text
64 physical cores
two-way hyperthreading
```

那么它提供：

```text
128 vCPUs
```

如果标准是：

```text
4 GB / vCPU
```

那么服务器需要：

```text
128 × 4 GB = 512 GB RAM
```

---

#### 3. ARM 不使用超线程

如果一台 ARM 服务器也有：

```text
64 physical cores
```

但：

```text
1 physical core = 1 vCPU
```

那么它只提供：

```text
64 vCPUs
```

按同样标准：

```text
4 GB / vCPU
```

需要：

```text
64 × 4 GB = 256 GB RAM
```

所以内存只有 x86 服务器的一半。

原文说：

> thus the ARM server contains only half the memory, saving 20-25% in cost per server.

<span data-type="text" style="color: var(--b3-font-color11);">因为内存是服务器成本的重要组成部分，少一半内存可以显著降低成本。</span>

---

### 十七、这里需要注意一个细节

ARM 服务器便宜并不只是因为“ARM 核心天然便宜”，还因为：

```text
vCPU 与物理核心映射方式不同
云 VM 内存按 vCPU 配置
无超线程导致每服务器内存需求更低
```

当然，这也意味着同样物理核心数下：

```text
ARM 服务器提供的 vCPU 数量可能更少
```

所以比较时要看：

```text
每 vCPU 性能
每 vCPU 价格
每物理核心吞吐
每服务器总吞吐
每瓦性能
应用实际表现
```

不能只看一个指标。

<span data-type="text" style="color: var(--b3-font-color11);">每 vCPU 性能
每 vCPU 价格
每物理核心吞吐
每服务器总吞吐
每瓦性能
应用实际表现</span>

---

### 十八、Brawny vs Wimpy 的适用场景

可以把这一节总结成一个设计指南。

---

#### 1. 更适合 brawny cores 的场景

适合强核的负载通常包括：

```text
延迟敏感服务
数据库
单 VM 性能敏感的云负载
传统企业应用
复杂控制流
串行部分较多的应用
事务处理
高缓存敏感应用
需要强单线程性能的服务
```

这些负载关心：

```text
单请求延迟
单线程性能
缓存命中率
分支预测能力
内存延迟
```

---

#### 2. 更适合 wimpy / scale-out cores 的场景

<span data-type="text" style="color: var(--b3-font-color11);">适合弱核或高吞吐核心的负载通常包括：</span>

```text
对象存储
键值存储
日志处理
数据分析
批处理
消息队列
网络功能
缓存服务
某些推理服务
可高度并行的 Web 前端
I/O-bound 服务
```

这些负载关心：

```text
总吞吐
每美元吞吐
每瓦吞吐
并行扩展能力
```

---

### 十九、现代趋势：不是二选一，而是异构组合

这一节最后说：

> Designs maximizing single-core speed, and designs improving per-socket throughput by reducing single-core speed, both have their place in server fleets.

也就是说：

```text
强核设计和吞吐导向设计都有位置。
```

现代数据中心通常不是只用一种 CPU，而是混合使用：

```text
高性能核心服务器
高核心数吞吐服务器
ARM 服务器
x86 服务器
GPU/TPU 加速器
SmartNIC/DPU
存储优化节点
内存优化节点
```

根据负载选择最合适的硬件。

---

### 二十、<span data-type="text" style="color: var(--b3-font-color11);">为什么“速度差越大”，弱核优势越难兑现？</span>

原文最后说：

> But the further apart their speeds are, the less likely any single-socket price-per-throughput advantage will play out in actual deployments, due to the overheads discussed above.

这句话的意思是：

```text
如果强核和弱核单线程性能差距太大，
弱核的理论价格吞吐优势在真实部署中可能消失。
```

原因是：

```text
Amdahl 定律
串行部分放大
尾延迟增加
软件优化成本增加
装箱碎片增加
全局协调开销增加
```

因此不能只看：

```text
每核心价格
每瓦性能
理论吞吐
```

还要看：

```text
真实应用延迟
软件开发成本
运维复杂度
资源利用率
尾延迟
客户体验
```

---

### 二十一、用一个综合例子理解这一节

假设你要部署一个服务。

---

#### 方案 A：强核服务器

```text
32 个高性能核心
每核心单线程强
价格高
功耗高
```

优点：

```text
单请求快
延迟稳定
开发简单
适合数据库和延迟敏感服务
```

缺点：

```text
价格高
每美元吞吐可能不占优
```

---

#### 方案 B：弱核服务器

```text
128 个低功耗核心
每核心单线程弱
价格低
功耗低
```

优点：

```text
并行吞吐高
每瓦吞吐好
硬件便宜
```

缺点：

```text
单请求慢
尾延迟可能高
需要更多并行优化
软件复杂度高
```

---

#### 负载决定选择

如果负载是：

```text
数据库
事务系统
单 VM 高性能云实例
```

方案 A 更合适。

如果负载是：

```text
日志分析
对象存储
批量数据处理
高度并行 Web 服务
```

方案 B 可能更合适。

---

### 二十二、这一节与前一节的关系

前一节告诉我们：

```text
当应用大到必须跨很多节点时，
高端 SMP 相对低端集群的性能优势会被稀释。
```

这一节进一步告诉我们：

```text
即使选择低端 scale-out，
也不是核心越弱越好。
```

因为：

```text
单线程性能太弱会增加延迟和软件复杂度。
```

所以 WSC 设计要在两个极端之间找平衡：

```text
太大太贵的强核系统
vs
太小太弱的细粒度系统
```

---

### 二十三、这一节的关键概念总结

---

#### 1. Granularity of scale-out

scale-out 的粒度可以是：

```text
大型 SMP
2-socket 服务器
1-socket 服务器
很多小核心节点
```

粒度越小，硬件可能越便宜，但软件和系统开销越大。

---

#### 2. Brawny cores

强核优势：

```text
单线程性能高
延迟低
适合单 VM 性能
适合数据库和复杂服务
```

---

#### 3. Wimpy cores

弱核优势：

```text
价格低
功耗低
密度高
适合吞吐导向和 I/O 导向负载
```

---

#### 4. Wimpy cores 的风险

```text
Amdahl 定律
串行部分主导延迟
尾延迟恶化
软件开发成本上升
小服务器装箱碎片
全局协调开销增加
```

---

#### 5. Cloud 负载偏好

多数云客户偏好：

```text
单 VM 性能
强单线程性能
大服务器切小 VM
```

---

#### 6. 吞吐负载偏好

数据分析和存储负载偏好：

```text
高吞吐
低成本
多核心
少内存每核
```

---

#### 7. ARM 云成功原因

```text
1 vCPU = 1 physical core
每 vCPU 性能强
无超线程导致内存配置更少
服务器成本更低
```

---

### 二十四、这一节可以整理成的精简笔记

```text
6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores

1. 问题：
   scale-out 是否应该使用更小、更弱的 CPU 核心？

2. 历史探索：
   - Piranha：早期低端核心服务器
   - Lim et al.：低功耗服务器核心
   - HP Moonshot：45 个 ARM/mobile-x86 刀片服务器
   - Hamilton：PC 级组件，影响 AWS Graviton
   - FAWN：弱核 + flash，构建高效 key-value 存储

3. 弱核优势：
   - 多个小 CPU 可能比中端大 CPU 便宜 2–5 倍获得同等吞吐
   - 很多应用是 memory/IO bound，快 CPU 收益有限
   - 慢 CPU 更省电，频率降 k 倍，功耗约降 O(k²)

4. 弱核风险：
   - Amdahl 定律：串行和通信开销限制扩展
   - 单线程太慢会使串行工作主导延迟
   - 更多并行任务增加响应时间波动，加剧尾延迟
   - 硬件成本降低，但软件开发成本增加
   - 小服务器 bin packing 更难，可能降低利用率
   - 即使 embarrassingly parallel 算法，切太细也可能因全局停止条件等变低效

5. 云应用视角：
   - 多数云负载强调单 VM 性能
   - 数据库等负载偏好最快服务器
   - 大服务器更容易切成小 VM，小服务器难以合并成大 VM

6. 吞吐导向负载：
   - 数据分析等偏好高吞吐、低成本
   - 可接受稍慢核心和更少内存每核

7. CPU 厂商产品线：
   - ARM：V 性能，N scale-out，E 效率
   - Intel：性能和效率两条 Xeon
   - AMD：EPYC 多产品线

8. ARM 云处理器成功：
   - AWS Graviton、GCP Axion
   - 说明市场需要 brawny cores，不只是弱核

9. ARM VM 价格性能优势：
   - ARM 通常不使用 hyperthreading：1 vCPU = 1 physical core
   - x86 常见 two-way HT：2 vCPUs = 1 physical core
   - 因此 ARM 每 vCPU 性能更强
   - 云 VM 按 vCPU 配置内存
   - ARM 服务器每物理核心对应更少 vCPU，因此内存更少
   - 可节省 20–25% 服务器成本

10. 结论：
   - 强核和吞吐导向核心都有适用场景
   - 不能不加区分追求最弱最小核心
   - 单核速度差距越大，弱核的理论价格吞吐优势越难在真实部署中实现
```

---

### 二十五、如果考试或讨论中要回答这一节，可以这样说

你可以这样概括：

> 6.1.2.2 节讨论 scale-out 的粒度问题，即是否应该使用更小的“wimpy”核心。历史上 Piranha、HP Moonshot、FAWN 和 Hamilton 的工作都探索过低功耗、低成本核心在服务器中的使用。弱核的优势在于价格性能更好、适合内存或 I/O 瓶颈应用，并且通常更省电。但它们也有明显风险：首先，Amdahl 定律仍然有效，串行和通信开销会限制并行扩展；其次，更多并行任务会加剧尾延迟；再次，硬件成本下降可能被软件开发成本上升抵消；此外，小服务器在 bin packing 中更容易产生资源碎片，甚至降低利用率。云应用通常更重视单 VM 性能，尤其是数据库等负载偏好强单线程核心；而数据分析等吞吐导向负载则可以接受稍慢但高吞吐的核心。现代 CPU 厂商因此提供性能、scale-out 和效率等不同产品线。ARM 云处理器如 AWS Graviton 和 GCP Axion 的成功说明市场需要的并不是单纯弱核，而是具有良好单 vCPU 性能的“brawny”核心。其价格性能优势部分来自 ARM VM 通常 1 vCPU 对应 1 物理核心，而 x86 VM 在使用超线程时 2 vCPU 才对应 1 物理核心；同时云 VM 按 vCPU 配置内存，使 ARM 服务器内存成本更低。总体而言，强核和弱核都有适用场景，但在真实 WSC 部署中，不能只看理论价格吞吐，还要考虑延迟、尾延迟、软件复杂度和资源利用率。

---

### 二十六、最后给你一个形象类比

可以把 brawny 和 wimpy cores 想象成两种运输团队。

---

#### Brawny cores：少数强力卡车

```text
每辆卡车很快
能拉重货
适合紧急、单件、高价值货物
```

优点是：

```text
单任务快
延迟低
调度简单
```

缺点是：

```text
车贵
油耗高
```

---

#### Wimpy cores：大量小型电动车

```text
每辆车便宜
省电
数量多
适合大量不紧急的小包裹
```

优点是：

```text
总吞吐高
成本低
能效好
```

缺点是：

```text
单车慢
如果一件货物必须一辆车完整运输，就会很慢
车辆太多也增加调度复杂度
```

---

而 WSC 的智慧在于：

> 不是所有货物都用同一种车。  
> 紧急数据库查询用强核；  
> 大规模日志分析用吞吐核；  
> 存储服务可能用弱核加 Flash；  
> 云平台同时提供不同 VM 形状。

这就是这一节的核心：

> 选择 CPU 构建块不是追求单一指标最优，而是要根据工作负载，在单线程性能、吞吐、功耗、成本、延迟、尾延迟和软件复杂度之间做系统级权衡。


**专栏导航**

- ← 上一篇：[6.1.2.1 A model to reason about scale-up versus scale-out](/posts/6-1-2-1-a-model-to-reason-about-scale-up-versus-scale-out/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.1.2.3 Scale-up vs scale-out for accelerators →](/posts/6-1-2-3-scale-up-vs-scale-out-for-accelerators/)
