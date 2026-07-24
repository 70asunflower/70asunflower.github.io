---
title: "6.1 WSC building blocks and design considerations"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-23
description: "《The Data Center as a Computer》AI 导读专栏正文：6.1 WSC building blocks and design considerations。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.1 WSC building blocks and design considerations。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.1 WSC building blocks and design considerations

下面我结合你提供的原文，把 **6.1 WSC building blocks and design considerations** 以及其中的 **6.1.1 Overall architecture** 和 **6.1.2 Building scale-out systems** 读深。

这一节是第 6 章的开头，视角从前面几章的：

```text
数据中心建筑
电力
冷却
Tier
Cloud/AI 对基础设施的影响
```

进一步下沉到：

```text
WSC 的硬件构建块
服务器架构选择
scale-up vs scale-out
CPU 核心选择
加速器系统设计
硬件-软件协同设计
```

也就是说，这一节开始回答一个核心问题：

> 如果把整个数据中心看作一台计算机，那么这台计算机的“零件”应该怎么选？  
> 这些零件又如何影响上层软件系统的设计？

---

### 一、6.1.1 Overall architecture：WSC 是由硬件构建块组成的系统

原文说：

> Building upon the previously discussed data center infrastructure, we now focus on the individual hardware building blocks that define the architecture of warehouse-scale computers.

这句话说明，第 6 章从“数据中心基础设施”转向“WSC 硬件架构”。

前面讲的数据中心基础设施是：

```text
电力
冷却
建筑
安全
Tier
```

而这里开始关注：

```text
芯片
CPU
内存
存储
网络
主板
服务器
机柜
加速器
分布式系统
```

---

#### 1. WSC 的类比：从逻辑门到芯片，从芯片到服务器，从服务器到 WSC

原文说：

> Just as logic elements form a microprocessor or chipsets create a server, WSC systems are composed of diverse components across compute, storage, and networking from individual chips to motherboards and distributed systems.

这里用了一个层级类比：

```text
逻辑门 -> 微处理器
芯片组 -> 服务器
计算/存储/网络组件 -> WSC
```

也就是说，WSC 不是一个单一设备，而是由大量硬件构建块组成的系统。

可以把它看成一个多层结构：

```text
单个晶体管 / 逻辑门
  -> CPU / GPU / TPU / NIC / SSD 控制器
    -> 主板 / 内存 / 存储 / 网卡 / 加速器
      -> 单台服务器
        -> 机柜
          -> 集群
            -> 数据中心
              -> 全球分布式系统
```

---

#### 2. WSC 的三大硬件构建块：计算、存储、网络

原文明确提到：

```text
compute
storage
networking
```

这是 WSC 硬件架构的三大基础。

---

##### 计算 compute

包括：

```text
CPU
GPU
TPU
NPU
ASIC
FPGA
SmartNIC
DPU
内存
缓存
```

计算构建块决定：

```text
单机性能
并行能力
能效
加速能力
虚拟化能力
任务调度方式
```

---

##### 存储 storage

包括：

```text
DRAM
NVMe SSD
HDD
持久内存
对象存储
分布式文件系统
缓存层
```

存储构建块决定：

```text
容量
延迟
吞吐
持久性
一致性
成本
数据保护方式
```

---

##### 网络 networking

包括：

```text
NIC
交换机
光模块
光纤
RDMA
网络拓扑
拥塞控制
负载均衡
```

网络构建块决定：

```text
通信延迟
带宽
扩展性
故障域
集群训练效率
存储访问性能
服务调用性能
```

---

### 二、Hardware-software codesign：硬件选择和软件设计不能分开

原文说：

> This chapter aims to provide insights into the selection of these building blocks and the resulting hardware-software codesign decisions.

这里的关键词是：

```text
hardware-software codesign
硬件-软件协同设计
```

---

#### 1. 什么是 hardware-software codesign？

它的意思是：

> 硬件设计不能只看硬件指标，软件设计也不能只看软件逻辑。  
> 两者必须一起设计、一起权衡。

例如：

```text
如果硬件选择廉价服务器，
那么软件必须能处理频繁故障。

如果硬件提供 RDMA 网络，
那么存储和通信协议可以重新设计。

如果硬件使用大量加速器，
那么编译、调度、内存管理都要改变。

如果硬件功率密度很高，
那么任务调度和冷却策略要协同考虑。
```

---

#### 2. WSC 中典型的 codesign 例子

---

##### 例子一：廉价服务器 + 软件容错

WSC 常使用大量普通服务器。

这些服务器可能故障率不低，但便宜。

因此软件必须假设：

```text
机器会坏
磁盘会坏
电源会坏
网卡会坏
```

然后设计：

```text
数据副本
自动重调度
健康检查
故障转移
滚动升级
```

这就是硬件和软件协同设计。

---

##### 例子二：SSD + 分布式存储

SSD 相比 HDD 有更低延迟和更高 IOPS。

因此存储系统可以设计成：

```text
更多副本？
更少副本？
更细粒度分片？
更激进的缓存？
更低延迟的元数据服务？
```

硬件变化会改变软件架构。

---

##### 例子三：RDMA 网络 + 高性能存储

如果网络支持 RDMA：

```text
远程内存访问可以绕过 CPU
```

那么存储系统可以设计成：

```text
更低延迟
更少上下文切换
更高吞吐
```

这也是 codesign。

---

##### 例子四：GPU/TPU + AI 训练系统

AI 加速器需要：

```text
高带宽互联
大内存
高功率
液冷
集体通信优化
模型并行
流水线并行
checkpoint
```

因此 AI 系统必须和硬件一起设计：

```text
训练框架
通信库
调度器
网络拓扑
冷却系统
故障恢复机制
```

---

### 三、6.1.2 Building scale-out systems：构建大规模系统的两条路

原文说：

> When building large-scale distributed hardware systems, we have two choices: scale-up, or scale-out.

构建大规模系统时，有两条基本路线：

```text
scale-up
纵向扩展

scale-out
横向扩展
```

这是理解 WSC 架构的关键。

---

### 四、什么是 scale-up？

原文说：

> scale-up: large shared-memory systems

scale-up 指的是：

> 把单台机器做得非常强大。

也就是：

```text
更多 CPU
更多内存
更多 I/O
更大机箱
更强可靠性
```

最终形成一个大型共享内存系统。

---

#### 1. Scale-up 系统的特征

典型 scale-up 系统可能有：

```text
4 路 CPU
8 路 CPU
16 路 CPU
32 路 CPU
甚至更多
```

以及：

```text
TB 级内存
大型 NUMA 架构
高端固件
复杂 RAS 特性
专有互连
昂贵硬件
```

---

#### 2. Scale-up 的优点

##### 编程模型简单

因为系统对外看起来像一台大机器：

```text
single system image
```

应用可以直接访问共享内存：

```text
所有 CPU 看到同一个地址空间
```

这对传统数据库、ERP、大型事务系统很友好。

---

##### 局部通信快

如果多个线程在同一台大机器里通信：

```text
通过内存
通过锁
通过共享数据结构
```

通常比跨网络通信快。

---

##### 适合某些传统企业负载

例如：

```text
大型关系数据库
SAP
Oracle
传统事务处理
大型内存数据库
```

这些负载历史上常运行在高端 SMP/NUMA 系统上。

---

#### 3. Scale-up 的缺点

##### 成本非常高

高端服务器通常：

```text
专有设计
专有固件
专有互连
高可靠性部件
厂商支持费用高
```

因此单位性能成本往往不如普通服务器。

---

##### 扩展有限

单台机器能塞进去的 CPU、内存、I/O 总是有限。

当业务增长到超过单台机器上限时，scale-up 就很难继续。

---

##### 故障域大

如果一台大型 scale-up 系统故障，可能影响很大。

例如：

```text
一台 32 路大型数据库服务器宕机
上面所有服务都受影响
```

---

##### 升级困难

高端系统升级往往涉及：

```text
固件升级
硬件兼容性
停机窗口
厂商支持
```

灵活性不如普通服务器集群。

---

### 五、什么是 scale-out？

原文说：

> scale-out: large clusters

scale-out 指的是：

> 用很多普通服务器组成集群。

也就是：

```text
横向增加机器数量
```

而不是把单台机器做得无限大。

---

#### 1. Scale-out 系统的特征

典型 scale-out 系统包括：

```text
大量 1-socket 或 2-socket 服务器
标准以太网或专用网络
分布式存储
分布式调度
分布式文件系统
副本机制
分片机制
负载均衡
```

例如：

```text
搜索集群
广告集群
存储集群
数据库集群
AI 训练集群
视频处理集群
```

---

#### 2. Scale-out 的优点

##### 成本效率高

普通服务器是大批量生产的：

```text
标准化
竞争激烈
供应链成熟
单位性能好
```

因此通常比高端专有服务器更便宜。

---

##### 容易扩展

需要更多容量时，可以：

```text
加机器
加机柜
加集群
加数据中心
```

而不是替换一台更大的机器。

---

##### 故障域小

一台机器故障只影响一部分任务或副本。

软件可以通过：

```text
副本
重调度
自动恢复
```

保持整体服务可用。

---

##### 适合分布式软件

现代互联网服务天然适合分布式：

```text
请求可以分发
数据可以分片
服务可以复制
任务可以并行
```

---

#### 3. Scale-out 的缺点

##### 软件复杂度高

你必须自己处理：

```text
网络分区
节点故障
数据一致性
副本同步
分布式事务
负载均衡
热点
拥塞
```

---

##### 通信开销大

跨机器通信比本地内存通信慢得多。

例如：

```text
本地内存访问：纳秒级
跨机器 RPC：微秒到毫秒级
```

因此系统设计必须尽量减少不必要通信。

---

##### 运维复杂

大规模集群需要：

```text
自动化部署
监控
故障检测
容量管理
配置管理
版本管理
安全补丁
```

---

### 六、为什么 WSC 历史上选择 scale-out？

原文说：

> WSCs have historically chosen scale-out to build clusters of low-end or mid-range servers, for a variety of reasons.

WSC 选择 scale-out 的原因很多，但最核心的是：

```text
成本效率
```

---

#### 1. 低端/中端服务器成本效率更高

原文说：

> The primary motivation has been the underlying cost-efficiency of such servers relative to high-end shared-memory systems.

普通服务器通常比高端共享内存系统更划算。

原因是：

```text
出货量大；
标准化程度高；
竞争充分；
使用通用组件；
不需要专有互连；
不需要复杂固件；
可以批量部署。
```

---

#### 2. 核心数增长让普通服务器已经足够强

原文说：

> Continuing trends on increasing core count also mean that most VM or task instances can comfortably fit into a two-socket or even a one-socket server.

随着 CPU 核心数增加，单台普通服务器已经很强。

例如现代服务器 CPU 可能有：

```text
32 cores
64 cores
96 cores
128 cores
甚至更多
```

因此很多任务不需要大型 scale-up 系统。

一个 VM 或容器通常只需要：

```text
1 vCPU
2 vCPU
4 vCPU
8 vCPU
16 vCPU
```

所以一台物理服务器可以运行很多 VM 或容器。

原文说：

> In fact, a typical physical server often hosts tens or hundreds of VMs today.

也就是：

```text
一台物理服务器承载几十到几百个 VM。
```

这进一步说明：

> 普通服务器已经足够强大，可以通过虚拟化和容器化提高利用率。

---

### 七、TPC-C 历史比较：低端服务器为什么更划算？

原文提到旧版书中比较过：

> the HP Integrity Superdome-Itanium2 and the HP ProLiant ML350 G5 and showed how the cost-efficiency of the low-end servers was four times better than the high-end shared-memory system.

这里涉及 TPC-C benchmark。

---

#### 1. TPC-C 是什么？

TPC-C 是一个经典事务处理基准测试。

它模拟订单处理系统：

```text
新订单
支付
订单状态
发货
库存查询
```

常用指标是：

```text
tpmC
transactions per minute C
```

以及：

```text
price/performance
价格性能比
```

---

#### 2. 旧版比较的结论

旧版比较中：

```text
高端系统：HP Integrity Superdome + Itanium2
低端系统：HP ProLiant ML350 G5
```

结论是：

```text
低端服务器的成本效率大约是高端系统的 4 倍。
```

也就是说，花同样的钱，低端服务器集群能提供更多事务处理能力。

---

#### 3. 为什么低端服务器成本效率更好？

因为：

```text
低端服务器标准化；
大量生产；
组件通用；
竞争激烈；
扩展方式灵活；
不需要昂贵专有系统。
```

而高端系统虽然单机强，但：

```text
价格高；
扩展贵；
专有部件多；
维护成本高。
```

---

### 八、为什么原文说现在不再强调具体系统比较？

原文说：

> However, over subsequent years and editions, the high-end server market has increasingly become niche, with hyperscale servers now being much more common and higher-volume.

意思是：

> 高端服务器市场已经越来越小众，超大规模服务器更常见、出货量更大。

---

#### 1. 高端服务器市场变成 niche

过去大型企业可能购买：

```text
大型 SMP 服务器
专有 UNIX 系统
大型 Itanium 系统
大型 Power 系统
大型 mainframe
```

但现在很多负载已经迁移到：

```text
x86 服务器集群
Arm 服务器
分布式数据库
云原生系统
 commodity hardware
```

高端服务器仍然存在，但更多用于：

```text
特定企业负载
传统大型数据库
关键事务系统
某些行业遗留系统
```

不再是 WSC 的主流。

---

#### 2. Hyperscale 服务器成为主流

超大规模服务器是专门为数据中心批量部署设计的：

```text
标准化
高密度
易维护
远程管理
自动化部署
低功耗
高吞吐
```

它们通常不追求单机极致可靠，而是依赖：

```text
集群软件
副本
调度
监控
自动恢复
```

---

### 九、用一个简单数学模型理解 scale-up vs scale-out

原文说：

> below, we present a simple mathematical model to reason about scale-up versus scale-out tradeoffs.

我们可以建立一个简化模型。

---

#### 1. 假设单台普通服务器性能为 p，成本为 c

例如：

```text
p = 1 单位性能
c = 1 单位成本
```

如果用 N 台普通服务器做 scale-out：

```text
总性能 = N × p × E(N)
总成本 = N × c + 网络成本 + 软件复杂度成本
```

其中：

```text
E(N) 是扩展效率
```

如果扩展完美：

```text
E(N) = 1
```

如果扩展有损耗：

```text
E(N) < 1
```

损耗来自：

```text
通信开销
同步开销
数据分片不均
网络拥塞
故障恢复
负载不均衡
```

---

#### 2. Scale-up 系统

假设一台高端系统性能为：

```text
P_up
```

成本为：

```text
C_up
```

高端系统通常：

```text
P_up 很大
C_up 更大
```

而且随着规模增加，成本可能超线性增长：

```text
C_up 增长比 P_up 更快
```

---

#### 3. 比较单位成本性能

scale-out 的单位成本性能：

```text
Performance per dollar_out = N × p × E(N) / (N × c + overhead)
```

scale-up 的单位成本性能：

```text
Performance per dollar_up = P_up / C_up
```

如果：

```text
Performance per dollar_out > Performance per dollar_up
```

那么 scale-out 更划算。

---

#### 4. 关键权衡

scale-out 的优势是：

```text
单节点便宜
可以线性扩展
```

scale-out 的代价是：

```text
分布式软件复杂
通信开销
故障处理
运维复杂
```

scale-up 的优势是：

```text
编程简单
本地共享内存
```

scale-up 的代价是：

```text
硬件昂贵
扩展有限
故障域大
```

WSC 的选择通常是：

```text
用软件复杂度换硬件成本效率。
```

---

### 十、Scale-up vs Scale-out 的直观对比

|维度|Scale-up|Scale-out|
| ------------| ----------------------| -----------------------------------|
|扩展方式|增强单机|增加机器数量|
|典型系统|大型 SMP/NUMA 服务器|服务器集群|
|成本|高，常超线性增长|较低，接近线性增长|
|编程模型|共享内存，较简单|分布式，较复杂|
|故障域|大|小|
|扩展上限|受单机限制|理论上可很大|
|通信方式|内存/总线|网络|
|通信延迟|低|较高|
|可靠性策略|高端硬件 RAS|软件容错|
|典型应用|传统大型数据库、ERP|Web 服务、云、分布式存储、AI 集群|
|WSC 主流|否|是|

---

### 十一、Brawny cores vs Wimpy cores：强核 vs 弱核辩论

原文提到：

> the “brawny versus wimpy cores” debates.

这是数据中心 CPU 设计中的经典辩论。

---

#### 1. 什么是 brawny cores？

brawny 可以理解为“强壮的”。

brawny cores 指高性能核心：

```text
高单线程性能
大缓存
复杂乱序执行
高分支预测能力
高主频
高功耗
```

典型例子：

```text
高性能 x86 核心
服务器级 Arm 核心
```

---

#### 2. 什么是 wimpy cores？

wimpy 可以理解为“简单、低功耗的”。

wimpy cores 指简单核心：

```text
单线程性能较低
缓存较小
功耗低
面积小
可以堆很多核
```

典型例子：

```text
早期 Atom 类核心
某些嵌入式核心
某些 throughput-oriented 核心
```

---

#### 3. 辩论的核心问题

问题是：

> 数据中心应该使用少量强核，还是大量弱核？

---

##### 支持 brawny cores 的理由

很多数据中心负载是延迟敏感的。

例如：

```text
Web 搜索
广告排序
数据库查询
在线事务
RPC 服务
```

这些负载需要：

```text
高单线程性能
低延迟
大缓存
强分支预测
```

如果核心太弱，单请求延迟会变差。

---

##### 支持 wimpy cores 的理由

有些负载是吞吐导向的。

例如：

```text
批处理
日志处理
对象存储
视频转码
网络包处理
某些 AI 推理
```

这些负载可以并行化，关心：

```text
总吞吐
能效
每瓦性能
每美元性能
```

因此大量简单核心可能更划算。

---

#### 4. 这个辩论如何演变？

原文说：

> how those have evolved over the years.

早期辩论中，人们常把选择看成：

```text
少量大核
vs
大量小核
```

但现代服务器 CPU 已经让两者界限模糊。

例如现代服务器 CPU 可能有：

```text
64 个高性能核心
128 个高性能核心
```

它们既是：

```text
很多核
```

又是：

```text
每个核都很强
```

因此现代趋势不是简单选择 wimpy，而是：

```text
大量足够强的核心
```

同时根据负载选择：

```text
通用 CPU
高主频 CPU
高核心数 CPU
Arm CPU
加速器
```

---

### 十二、加速器系统中的 scale-up vs scale-out 不同

原文最后说：

> We also discuss how the scale-up versus scale-out consideration has been different for emerging accelerator systems.

这是现代 WSC 架构中非常重要的点。

对于 CPU 集群，WSC 历史上偏向：

```text
scale-out
```

但对于 AI 加速器系统，scale-up 和 scale-out 的关系更复杂。

---

#### 1. 为什么加速器系统需要更强的 scale-up？

AI 训练，尤其是大模型训练，需要大量加速器之间高速通信。

例如：

```text
数据并行
模型并行
张量并行
流水线并行
专家并行
all-reduce
all-gather
```

这些操作需要：

```text
极低延迟
极高带宽
稳定集体通信
```

如果加速器之间通过网络 scale-out，通信可能成为瓶颈。

因此现代 AI 系统常在节点内或机架内做 scale-up：

```text
多个 GPU/TPU 紧耦合
高速互连
共享内存或近共享内存
NVLink / NVSwitch / ICI / 自定义互连
```

---

#### 2. 加速器系统的典型层级

现代 AI 集群通常是：

```text
单芯片 scale-up
  -> 单节点 scale-up
    -> 单机架 scale-up
      -> 多机架 scale-out
        -> 多 Pod scale-out
          -> 多数据中心 scale-out
```

例如：

```text
一个 GPU 节点内：
  8 个 GPU 通过高速互连紧耦合

一个机架内：
  多个节点通过高速网络互连

多个机架之间：
  通过数据中心网络 scale-out
```

---

#### 3. 为什么这和传统 CPU 系统不同？

传统 CPU 服务通常可以：

```text
无状态横向扩展
请求级负载均衡
数据分片
副本复制
```

节点间通信相对可容忍较高延迟。

但大模型训练中：

```text
每一步都可能需要集体同步
加速器之间通信频繁
通信延迟直接影响训练效率
```

因此加速器系统必须同时重视：

```text
scale-up：节点内/机架内高速互连
scale-out：跨机架/跨集群扩展
```

---

#### 4. 加速器系统还带来功率和冷却挑战

原文前一节已经提到，AI 加速器功率密度很高：

```text
50–200 kW/rack
```

因此加速器 scale-up 还涉及：

```text
高功率供电
液冷
机架级设计
高密度互连
故障域管理
checkpoint
快速替换
```

这也是 hardware-software codesign 的典型场景。

---

### 十三、这一节的核心思想：WSC 架构是权衡的结果

这一节不是简单说“scale-out 好”，而是告诉我们：

> WSC 架构选择是由成本、性能、扩展性、可靠性、软件复杂度和负载特征共同决定的。

---

#### 1. 传统 WSC 为什么选择 scale-out？

因为：

```text
普通服务器成本效率高；
核心数增长让单节点足够强；
集群可以线性扩展；
故障域小；
适合分布式软件；
适合大规模部署。
```

---

#### 2. Scale-out 的代价是什么？

代价是：

```text
分布式系统复杂；
通信开销大；
需要容错机制；
运维复杂；
一致性、调度、负载均衡困难。
```

---

#### 3. 为什么高端 scale-up 系统变 niche？

因为：

```text
价格高；
扩展有限；
专有性强；
单位成本性能不如普通服务器集群；
很多负载已经分布式化。
```

---

#### 4. 为什么加速器系统让问题变复杂？

因为 AI 负载需要：

```text
高带宽
低延迟
紧耦合互连
高功率
液冷
集体通信优化
```

所以加速器系统既需要 scale-up，也需要 scale-out。

---

### 十四、这一节可以整理成的精简笔记

```text
6.1 WSC building blocks and design considerations

6.1.1 Overall architecture
1. 本章从数据中心基础设施转向 WSC 硬件构建块。
2. WSC 由计算、存储、网络等多类组件组成。
   - 从芯片到主板，再到服务器、机柜和分布式系统。
3. 本章关注：
   - 如何选择硬件构建块
   - 硬件选择如何影响软件设计
   - hardware-software codesign

6.1.2 Building scale-out systems
1. 构建大规模系统有两条路：
   - scale-up：大型共享内存系统
   - scale-out：大型集群

2. WSC 历史上选择 scale-out。
   主要原因：
   - 低端/中端服务器成本效率更高
   - 核心数增加使单节点足够强
   - 单台服务器可承载数十到数百 VM

3. 旧版书中通过 TPC-C 比较高端与低端服务器。
   - HP Integrity Superdome-Itanium2
   - HP ProLiant ML350 G5
   - 低端服务器成本效率约为高端系统 4 倍

4. 高端服务器市场逐渐 niche。
   - hyperscale 服务器更常见
   - 出货量更大
   - 更标准化

5. 可以用简单数学模型理解 scale-up vs scale-out：
   - scale-out：N 台普通服务器，总性能约 N×p×E(N)
   - scale-up：单台大系统，性能高但成本常超线性增长
   - WSC 通常用软件复杂度换硬件成本效率

6. CPU 选择中的 brawny vs wimpy cores：
   - brawny：高性能核心，适合延迟敏感负载
   - wimpy：简单低功耗核心，适合吞吐导向负载
   - 现代趋势是大量足够强的核心，界限逐渐模糊

7. 加速器系统中的 scale-up vs scale-out 不同：
   - AI 训练需要加速器之间高带宽、低延迟互连
   - 节点内/机架内常需要 scale-up
   - 跨机架/跨集群仍需要 scale-out
   - 同时带来高功率密度和冷却挑战
```

---

### 十五、如果考试或讨论中要回答这一节，可以这样说

你可以这样概括：

> 6.1 节开始讨论 WSC 的硬件构建块和架构设计。首先，WSC 不是单一设备，而是由计算、存储和网络等组件组成的系统，涵盖从芯片、主板到服务器、机柜和分布式系统的多个层次。因此，硬件选择必须与软件设计协同考虑。其次，在构建大规模系统时，有 scale-up 和 scale-out 两条路线。Scale-up 依赖大型共享内存系统，编程模型简单但成本高、扩展受限；scale-out 使用大量普通服务器组成集群，成本效率高、扩展灵活，但需要复杂的分布式软件来处理故障、通信和一致性。WSC 历史上选择 scale-out，主要原因是低端和中端服务器相对高端系统具有更好的成本效率。随着 CPU 核心数增加，单台普通服务器已经可以承载大量 VM 或任务，这进一步支持了 scale-out 架构。旧版书中通过 TPC-C 比较说明低端服务器的成本效率显著优于高端系统，而高端服务器市场如今已经变成小众市场。最后，原文还引出 CPU 核心选择中的 brawny versus wimpy cores 辩论，以及加速器系统中 scale-up 与 scale-out 的新权衡。对于 AI 训练等加速器负载，节点内或机架内高速互连非常重要，因此 scale-up 的意义与传统 CPU 集群不同。

---

### 十六、最后给你一个形象类比

可以把 scale-up 和 scale-out 想象成两种运输系统。

---

#### Scale-up：造一辆超级大卡车

```text
一辆卡车非常大
能装很多货
维护复杂
造价昂贵
一旦坏了，所有货都受影响
```

这类似大型共享内存服务器。

---

#### Scale-out：组建一个标准化车队

```text
很多普通卡车
每辆便宜
坏了一辆，其他车继续跑
可以按需增加车辆
但需要调度系统、路线规划和货物分配
```

这类似 WSC 服务器集群。

---

而 AI 加速器系统则像：

```text
某些超大型货物必须几辆车紧密协同运输。
车与车之间必须保持极近距离和高速通信。
因此既需要单车内部强大，
也需要车队之间高效协同。
```

这就是现代 WSC 硬件架构的核心：

> 不是简单选择“大机器”或“小机器”，而是根据负载特征，在成本、性能、扩展性、可靠性和能效之间做系统级权衡。


**专栏导航**

- ← 上一篇：[5.1.4 Cloud and AI implications for data center design](/posts/5-1-4-cloud-and-ai-implications-for-data-center-design/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.1.2.1 A model to reason about scale-up versus scale-out →](/posts/6-1-2-1-a-model-to-reason-about-scale-up-versus-scale-out/)
