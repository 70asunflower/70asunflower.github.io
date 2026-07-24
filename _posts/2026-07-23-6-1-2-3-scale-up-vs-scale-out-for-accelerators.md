---
title: "6.1.2.3 Scale-up vs scale-out for accelerators"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-23
description: "《The Data Center as a Computer》AI 导读专栏正文：6.1.2.3 Scale-up vs scale-out for accelerators。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.1.2.3 Scale-up vs scale-out for accelerators。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.1.2.3 Scale-up vs scale-out for accelerators

下面我结合你提供的原文，把 **6.1.2.3 Scale-up vs scale-out for accelerators** 这一节读深。

这一节是前面 scale-up vs scale-out 讨论的延伸。前面主要讨论传统 CPU 服务器：

```text
大型 SMP 服务器
vs
低端服务器集群
```

而这一节讨论的是：

```text
加速器系统
```

例如：

```text
GPU
TPU
VCU
其他 AI / 视频加速器
```

核心问题是：

> 对于加速器系统，应该把系统设计成更大的 scale-up 域，还是继续走传统 scale-out 集群路线？  
> 为什么 ML 加速器倾向于一定程度的 scale-up，而视频加速器 VCU 却更彻底地 scale-out？

---

### 一、这一节的核心观点

原文最后其实已经给出了总结：

> Scale-up will offer significant performance and related performance-per-cost advantages for smaller-sized workloads, but cost efficiency and the ability to leverage industry hardware and the large software investment in distributed systems management will always make scale-out important for much larger workloads.

可以概括为：

```text
对于较小或通信密集的工作负载：
  scale-up 有显著性能和性能成本优势。

对于非常大的工作负载：
  scale-out 仍然重要，
  因为它成本低、可使用行业标准硬件、
  并能复用大量分布式系统软件投资。
```

但加速器系统和传统 CPU 系统有一个关键不同：

```text
加速器系统通常是定制设计的，
因此可以连网络互连一起定制，
从而改变 scale-up 和 scale-out 的边界。
```

---

### 二、为什么加速器系统会面临类似但不同的权衡？

原文说：

> Since accelerator systems are custom-designed and target vertically-integrated solutions for specific workloads, often with lower volumes than for traditional servers, their design tradeoffs can be different.

这句话有几个关键词。

---

#### 1. custom-designed：定制设计

传统服务器通常使用通用 CPU、通用主板、通用以太网、通用操作系统。

而加速器系统通常是为特定负载定制的：

```text
芯片架构定制
内存系统定制
互连网络定制
主板/托盘定制
机架定制
冷却定制
编译器定制
运行时定制
调度器定制
```

例如：

```text
TPU 为机器学习训练和推理定制
GPU 为并行计算和图形/ML 定制
VCU 为视频编解码定制
```

---

#### 2. vertically-integrated：垂直整合

垂直整合意味着：

```text
芯片
硬件
网络
系统软件
编译器
框架
调度器
应用
```

可以由同一套设计团队或同一套技术栈协同优化。

例如：

```text
TPU + XLA + JAX/TensorFlow + Borg + 数据中心网络
GPU + CUDA + NCCL + PyTorch + 集群调度
VCU + 视频编码库 + 转码调度系统
```

这种垂直整合让硬件和软件可以深度协同。

---

#### 3. specific workloads：特定工作负载

加速器不是通用 CPU。

它通常只擅长某类任务：

```text
GPU：矩阵计算、并行数据流、图形、ML
TPU：张量计算、ML 训练/推理
VCU：视频编码/解码/转码
```

因为目标负载明确，所以可以针对通信模式、内存访问模式、计算模式做专门优化。

---

#### 4. lower volumes：产量较低

传统服务器 CPU 出货量巨大。

而某些加速器产量相对较小。

这意味着：

```text
定制硬件的研发成本更难摊薄
```

但如果加速器能显著提升：

```text
性能
能效
每美元性能
```

那么对于超大规模公司来说，定制仍然值得。

---

### 三、回到前面的模型：加速器可以改变“远程访问延迟”

原文说：

> Returning to the model discussed at the beginning of this chapter, a custom design opens up the opportunity to also customize the network, so that the latency variable for remote node access can differ from the 100 µs we assumed in the prior model.

前面模型中有一个关键假设：

```text
本地共享内存访问：约 100 ns
远程网络访问：约 100 µs
```

二者相差约：

```text
1000 倍
```

这个巨大差距是 scale-up 优势的核心来源。

---

#### 1. 传统集群为什么远程访问慢？

传统服务器集群通常使用 Ethernet。

一次远程访问要经过：

```text
CPU
内存
PCIe
网卡
交换机
对端网卡
对端 CPU
对端内存
协议栈
软件开销
```

所以延迟通常是微秒级。

---

#### 2. 加速器系统可以定制互连

加速器系统可以设计专用互连，例如：

```text
Google TPU ICI
NVIDIA NVLink
NVSwitch
AMD Infinity Fabric
UAL Ultra Accelerator Link
定制 rack-scale interconnect
```

这些互连通常比传统 Ethernet 提供：

```text
更低延迟
更高带宽
更适合集体通信
更适合加速器之间紧耦合通信
```

因此原本模型中的：

```text
remote access = 100 µs
```

在加速器 scale-up 域内可能变成：

```text
远低于 100 µs
甚至接近本地内存访问量级
```

这就扩大了 scale-up 的有效范围。

---

### 四、TPU 系统：用 ICI 扩大 scale-up 域

原文说：

> TPU systems, for example, have an innovative ICI-based network that allow larger TPU supercomputers with shared-memory abstractions.

TPU 是 Google 的机器学习加速器。

它使用：

```text
ICI
Inter-Chip Interconnect
芯片间互连
```

来连接大量 TPU 芯片。

---

#### 1. ICI 的作用

ICI 的目标是让很多 TPU 芯片之间可以高速通信。

它不是普通 Ethernet，而是专门为 TPU 集体通信设计的互连。

它支持：

```text
高带宽
低延迟
all-reduce
all-gather
reduce-scatter
collective communication
```

这些操作正是 ML 训练中最常见的通信模式。

---

#### 2. “shared-memory abstractions”是什么意思？

原文说 TPU 超算可以提供：

```text
shared-memory abstractions
共享内存抽象
```

这里不一定是说所有 TPU 芯片真的像一台传统 SMP 那样拥有完全硬件一致的共享内存。

更准确地说，它指的是：

```text
编程模型和系统抽象上，
可以让多个加速器看起来像一个更大的计算系统。
```

例如：

```text
模型可以跨多个芯片切分
张量可以分布在多个芯片上
集体通信可以被高效执行
程序员不需要完全手动管理所有远程数据移动
```

这使得大型模型训练更容易扩展。

---

#### 3. TPU pod：深度 scale-up

原文说：

> For ML accelerators, TPU designers chose to go fairly deep on scaling up, with pod sizes of 9,216 chips.

也就是说，TPU 系统设计了一个很大的 scale-up 域：

```text
TPU pod
```

一个 pod 可以包含大量 TPU 芯片，例如原文提到：

```text
9,216 chips
```

这意味着很多 ML 训练通信可以发生在一个高速互连域内部，而不是走外部 Ethernet。

---

#### 4. 为什么 ML 训练需要这么大的 scale-up 域？

因为大模型训练通信非常密集。

例如：

```text
数据并行需要梯度同步
张量并行需要激活值通信
流水线并行需要阶段间传输
专家并行需要 token 路由
模型并行需要参数分片访问
```

这些操作如果都走普通 Ethernet，可能成为瓶颈。

因此 TPU 通过 ICI 把很多芯片组成一个大 scale-up 域，减少跨慢速网络的通信。

---

### 五、NVIDIA NVLink：GPU 系统的 scale-up 域

原文说：

> NVIDIA offers NVLink interconnects allowing up to 256 GPUs.

NVIDIA 使用：

```text
NVLink
NVSwitch
```

来构建 GPU 之间的高速互连。

---

#### 1. NVLink 的作用

NVLink 是 GPU 之间的高速互连，相比 PCIe 和传统网络，它提供：

```text
更高带宽
更低延迟
更适合 GPU 直接通信
```

这对于：

```text
多 GPU 训练
大模型并行
集体通信
GPU 间内存访问
```

非常重要。

---

#### 2. 从单节点到多节点 scale-up

早期 GPU 服务器通常是：

```text
一台服务器 4/8 GPU
GPU 通过 PCIe 或 NVLink 连接
```

现在趋势是扩大到：

```text
机架级 GPU 互连
多节点 GPU 互连
```

原文提到 NVIDIA 可支持：

```text
up to 256 GPUs
```

这意味着 scale-up 域不再只是单台服务器，而可以是：

```text
一个 GPU 超级节点
一个机架级 GPU 域
```

---

### 六、UAL：行业标准化的高速加速器互连

原文说：

> A new industry consortium is working on an “ultra accelerator link” to enable similar faster networking as an industry standard.

UAL，Ultra Accelerator Link，是一个行业联盟推动的标准。

它的目标是：

```text
让加速器之间的高速互连不再完全依赖单一厂商私有方案。
```

---

#### 1. 为什么需要 UAL？

目前不同厂商加速器互连可能不兼容：

```text
NVIDIA NVLink
Google ICI
AMD Infinity Fabric
其他定制互连
```

如果行业有统一标准，那么可能实现：

```text
多厂商加速器互操作
更成熟的供应链
更低集成成本
更大规模生态
```

---

#### 2. UAL 的意义

UAL 试图把原本私有、垂直整合的 scale-up 互连变成行业标准。

这类似于历史上：

```text
Ethernet 标准化数据中心网络
PCIe 标准化设备互连
InfiniBand 提供高性能互连
```

如果 UAL 成功，加速器 scale-up 域可能更容易扩展和普及。

---

### 七、大应用仍然需要 Ethernet scale-out

原文说：

> For large applications, multiple such highly-interconnected pods are connected via Ethernet-based scale-out network fabrics.

即使 TPU pod 或 GPU 超级节点内部互连很快，当应用超过单个 pod 时，仍然需要跨 pod 通信。

这时通常使用：

```text
Ethernet-based scale-out network
```

---

#### 1. 为什么跨 pod 用 Ethernet？

Ethernet 有很多优势：

```text
标准化
多厂商支持
成本低
规模大
运维成熟
软件生态丰富
可扩展到超大规模
```

因此即使加速器内部使用定制高速互连，跨 pod 仍然可以使用 Ethernet。

---

#### 2. 典型层级结构

现代 AI 集群通常是多层互连：

```text
芯片内互连
  -> 芯片间互连
    -> 节点内互连
      -> 机架内互连
        -> pod 内互连
          -> Ethernet scale-out 网络
            -> 跨集群/跨数据中心网络
```

例如：

```text
TPU pod 内：ICI
GPU 超级节点内：NVLink/NVSwitch
跨 pod：Ethernet
跨数据中心：长距光纤
```

---

### 八、ML 加速器为什么倾向 scale-up？

这一节虽然没有展开很多，但背后原因非常重要。

---

#### 1. ML 训练通信密集

大模型训练常见集体通信：

```text
all-reduce
all-gather
reduce-scatter
broadcast
all-to-all
```

这些操作需要：

```text
高带宽
低延迟
稳定可预测
低抖动
```

如果通信走普通 Ethernet，可能成为训练瓶颈。

---

#### 2. 模型并行需要紧耦合

大模型经常使用：

```text
张量并行
流水线并行
序列并行
专家并行
```

这些并行方式可能需要加速器之间频繁交换中间结果。

例如张量并行中，一个矩阵乘法可能被切到多个 GPU/TPU 上：

```text
GPU 0 计算一部分
GPU 1 计算一部分
然后需要合并结果
```

如果互连慢，计算会被通信拖慢。

---

#### 3. scale-up 域越大，越多通信变“本地通信”

如果很多加速器在同一个高速互连域里，那么原本跨 Ethernet 的远程通信可以变成：

```text
pod 内高速互连通信
```

这相当于把前面模型中的：

```text
remote access penalty
```

大幅降低。

---

### 九、VCU 系统为什么完全拥抱 scale-out？

原文说：

> VCU systems, on the other hand, fully embrace traditional WSC scale-out because video coding tasks don’t communicate with each other.

VCU 是视频处理加速器。

它和 ML 加速器不同。

---

#### 1. 视频编码任务通常彼此独立

视频转码任务通常是：

```text
输入视频
  -> 分成多个片段
  -> 每个片段独立编码
  -> 输出结果
```

不同任务之间很少需要通信。

例如：

```text
视频 A 转码
视频 B 转码
视频 C 转码
```

它们彼此独立。

甚至同一个视频的不同片段也可以独立处理。

---

#### 2. 因此不需要高速 scale-up 互连

既然任务之间不通信，就不需要：

```text
NVLink
ICI
高速 all-reduce
紧耦合共享内存
```

普通 Ethernet 已经足够。

---

#### 3. VCU 更适合传统 WSC scale-out

VCU 系统可以设计成：

```text
大量独立 VCU 节点
通过 Ethernet 连接
由分布式调度器分配任务
从分布式存储读取视频
将结果写回分布式存储
```

这非常符合传统 WSC 的 scale-out 思想。

---

### 十、ML 加速器 vs VCU：为什么设计选择不同？

可以用下面这张表理解。

|维度|ML 加速器，如 TPU/GPU|视频加速器 VCU|
| ------------------| --------------------------------------| --------------------------|
|典型负载|模型训练、推理|视频编码、解码、转码|
|任务间通信|高，尤其训练|低，任务通常独立|
|关键操作|all-reduce、all-gather、模型并行通信|独立帧/片段处理|
|延迟敏感性|集体通信延迟影响训练效率|单任务吞吐更重要|
|互连需求|高带宽、低延迟 scale-up 互连|Ethernet scale-out 足够|
|典型 scale-up 域|TPU pod、GPU NVLink domain|通常不需要大 scale-up 域|
|跨节点网络|Ethernet 用于跨 pod scale-out|Ethernet 是主要网络|
|设计重点|紧耦合并行、通信效率|任务吞吐、成本效率|

---

### 十一、用前面的模型理解加速器设计

前面模型是：

```text
time = 1ms + f · (1/N · 100ns + (N - 1)/N · 100µs)
```

其中：

```text
f：全局访问次数
N：节点数
100ns：本地访问延迟
100µs：远程访问延迟
```

---

#### 1. 传统 CPU 集群

在传统集群里：

```text
本地访问：100 ns
远程访问：100 µs
```

差距约 1000 倍。

因此如果通信很重，scale-out 会明显变慢。

---

#### 2. 加速器 scale-up 域

加速器通过定制互连，可以把“远程访问”延迟降低。

例如：

```text
本地访问：100 ns
pod 内远程访问：可能远低于 100 µs
跨 pod Ethernet：仍然较慢
```

于是模型可以变成：

```text
time = compute
     + f_local · local_latency
     + f_pod · pod_interconnect_latency
     + f_ethernet · ethernet_latency
```

其中：

```text
local_latency < pod_interconnect_latency << ethernet_latency
```

设计目标是尽量让通信落在：

```text
local 或 pod_interconnect
```

而不是：

```text
ethernet
```

---

#### 3. ML 训练的设计目标

对于 ML 训练：

```text
f 很大
通信很频繁
```

所以必须扩大高速 scale-up 域：

```text
更多 GPU/TPU 放入同一 NVLink/ICI 域
```

---

#### 4. VCU 的设计目标

对于 VCU：

```text
f 很小
任务间几乎不通信
```

所以不需要扩大高速 scale-up 域。

直接用 Ethernet scale-out 即可。

---

### 十二、为什么 scale-up 对小负载优势明显？

原文说：

> Scale-up will offer significant performance and related performance-per-cost advantages for smaller-sized workloads.

如果一个工作负载可以放进一个 scale-up 域，例如：

```text
一个 TPU pod
一个 GPU NVLink domain
```

那么它可以享受：

```text
低延迟通信
高带宽通信
更简单的编程模型
更少的网络瓶颈
更高的训练效率
```

这时 scale-up 的性能优势很明显。

---

#### 1. 小负载能放进 scale-up 域

例如一个模型可以放进：

```text
256 GPUs
或
一个 TPU pod
```

那么大部分通信都在高速互连内完成。

---

#### 2. 性能成本优势

如果高速互连能显著提升训练吞吐，那么即使硬件更贵，也可能有更好的：

```text
performance per cost
```

因为：

```text
训练时间缩短
GPU/TPU 利用率提高
通信等待减少
```

---

### 十三、为什么 scale-out 对超大负载仍然重要？

原文说：

> cost efficiency and the ability to leverage industry hardware and the large software investment in distributed systems management will always make scale-out important for much larger workloads.

当工作负载超过单个 scale-up 域时，就必须 scale-out。

---

#### 1. 超大模型可能超过单个 pod

例如：

```text
模型参数太大
训练数据太大
batch size 太大
需要数千甚至数万加速器
```

单个 pod 装不下，就必须跨 pod。

---

#### 2. Ethernet scale-out 的成本优势

Ethernet 的优势是：

```text
便宜
标准
可扩展
多厂商
成熟
```

如果所有互连都用定制高速互连，成本可能非常高。

因此合理设计是：

```text
局部高速 scale-up
全局 Ethernet scale-out
```

---

#### 3. 复用分布式系统软件投资

WSC 已经在 scale-out 软件上投入巨大：

```text
集群调度
故障检测
自动恢复
监控
配置管理
网络管理
存储系统
安全系统
```

如果加速器系统完全脱离 scale-out 体系，会增加很多新成本。

因此使用 Ethernet 和现有分布式系统基础设施可以复用这些投资。

---

### 十四、加速器系统的典型分层架构

可以把现代加速器系统理解成多层结构。

---

#### 1. 芯片级 scale-up

单个加速器芯片内部：

```text
计算单元
片上内存
片上互连
```

---

#### 2. 节点级 scale-up

一台服务器或托盘内：

```text
多个加速器
高速互连
共享内存或近共享内存
高速 PCIe/CXL
```

---

#### 3. 机架级 / pod 级 scale-up

多个节点组成：

```text
GPU superpod
TPU pod
AI rack
```

使用：

```text
NVLink
NVSwitch
ICI
UAL
定制互连
```

---

#### 4. Ethernet scale-out

多个 pod 之间使用：

```text
Ethernet
RDMA
RoCE
InfiniBand 或定制网络
```

---

#### 5. 跨数据中心

多个数据中心之间使用：

```text
长距光纤
DWDM
骨干网
```

---

### 十五、加速器系统带来的新设计挑战

虽然原文没有展开，但这一节背后有很多工程挑战。

---

#### 1. 功率密度

加速器功率通常很高。

例如：

```text
单个 GPU/TPU 可能几百瓦到上千瓦
一个机柜可能 50–200 kW
```

因此需要：

```text
液冷
高密度供电
强化配电
机架级冷却
```

---

#### 2. 故障域

scale-up 域越大，故障影响可能越大。

例如一个 pod 内网络故障可能影响很多加速器。

因此需要：

```text
快速故障检测
checkpoint
自动重调度
节点隔离
pod 级可靠性设计
```

---

#### 3. 软件复杂度

高速互连虽然提升性能，但也需要软件支持：

```text
编译器
集合通信库
拓扑感知调度
故障恢复
内存管理
并行策略
```

例如 ML 框架需要知道：

```text
哪些 GPU 在同一个 NVLink domain
哪些 TPU 在同一个 ICI domain
如何放置模型分片
如何安排 all-reduce
```

---

#### 4. 定制与标准化之间的权衡

定制互连性能高，但可能：

```text
生态封闭
供应商锁定
集成复杂
规模有限
```

标准化互连性能可能稍低，但：

```text
生态更好
成本更低
可维护性更好
```

UAL 就是试图在二者之间找平衡。

---

### 十六、这一节与前面章节的联系

这一节把前面几个概念串起来了。

---

#### 1. 与 scale-up vs scale-out 模型的联系

前面模型说明：

```text
通信越重，scale-up 越有价值。
```

加速器系统通过定制互连，把 scale-up 域扩大，从而降低通信惩罚。

---

#### 2. 与 brawny vs wimpy cores 的联系

前面讨论 CPU 核心粒度：

```text
强核适合单线程/延迟敏感
弱核适合吞吐/并行
```

加速器则更进一步：

```text
不是通用核心强弱问题，
而是专用加速器如何互连、如何扩展的问题。
```

---

#### 3. 与 Cloud/AI 数据中心设计的联系

前面 5.1.4 节提到：

```text
AI 负载提高功率密度
改变供电和冷却设计
```

这一节则说明：

```text
AI 负载还改变互连和系统架构设计。
```

---

### 十七、一个直观例子：ML 训练 vs 视频转码

---

#### 1. ML 训练任务

假设训练一个大模型，需要：

```text
4096 个加速器
```

训练每一步都需要：

```text
梯度同步
参数更新
张量通信
```

如果这些通信都走普通 Ethernet：

```text
通信可能成为瓶颈
训练效率下降
```

因此设计者会尽量：

```text
把加速器放入同一个高速互连域
使用 ICI/NVLink/UAL
减少跨 Ethernet 通信
```

---

#### 2. 视频转码任务

假设有 100 万个视频需要转码。

每个视频可以独立处理：

```text
video_001.mp4 -> VCU node A
video_002.mp4 -> VCU node B
video_003.mp4 -> VCU node C
```

节点之间几乎不需要通信。

因此设计者会更关心：

```text
每美元转码吞吐
每瓦转码吞吐
任务调度效率
存储 I/O 效率
```

而不是节点间高速互连。

所以 VCU 系统可以完全使用 Ethernet scale-out。

---

### 十八、这一节的核心思想总结

---

#### 1. 加速器系统也面临 scale-up vs scale-out 权衡

不是只有 CPU 服务器需要选择：

```text
大型共享内存系统
vs
集群
```

加速器系统同样需要选择：

```text
紧耦合 scale-up 域
vs
松耦合 scale-out 集群
```

---

#### 2. 定制设计可以改变网络延迟变量

传统模型假设远程访问约：

```text
100 µs
```

但加速器可以定制互连，使 scale-up 域内通信远快于普通 Ethernet。

---

#### 3. ML 加速器倾向更深 scale-up

因为 ML 训练通信密集。

TPU 使用：

```text
ICI
```

NVIDIA 使用：

```text
NVLink
```

行业也在推动：

```text
UAL
```

目标都是扩大高速互连域。

---

#### 4. VCU 更倾向 scale-out

因为视频编码任务彼此独立，通信少。

所以 VCU 使用：

```text
Ethernet
分布式任务调度
```

即可高效扩展。

---

#### 5. 超大负载仍然需要 scale-out

即使有大型 scale-up 域，超大应用仍然会超过单个域。

这时需要：

```text
Ethernet scale-out
分布式系统软件
跨 pod 调度
故障恢复
```

---

### 十九、这一节可以整理成的精简笔记

```text
6.1.2.3 Scale-up vs scale-out for accelerators

1. 加速器系统也面临 scale-up vs scale-out 权衡。
   但由于加速器通常是定制设计、垂直整合、面向特定负载，
   其权衡与传统 CPU 服务器不同。

2. 定制设计允许定制网络互连。
   因此远程访问延迟不一定像传统 Ethernet 模型那样是 100 µs。

3. TPU 系统：
   - 使用 ICI，Inter-Chip Interconnect
   - 支持大型 TPU pod / hypercomputer
   - 提供共享内存抽象
   - pod 规模可达 9,216 chips
   - 选择较深的 scale-up 路线

4. NVIDIA GPU 系统：
   - 使用 NVLink 互连
   - 可支持最多 256 GPUs
   - 构建高速 GPU scale-up 域

5. UAL：
   - Ultra Accelerator Link
   - 行业联盟推动的标准
   - 目标是让高速加速器互连成为行业标准

6. 对于大型应用：
   - 多个高速互连 pod 之间通过 Ethernet scale-out 网络连接

7. VCU 系统：
   - 用于视频编码/解码/转码
   - 视频任务之间通常不通信
   - 完全拥抱传统 WSC scale-out
   - 使用 Ethernet 和 scale-out 任务调度

8. 总体原则：
   - 对较小或通信密集负载，scale-up 有显著性能和性能成本优势
   - 对非常大的负载，scale-out 仍然重要
   - scale-out 的优势包括：
     成本效率
     行业标准硬件
     分布式系统管理软件投资

9. 核心结论：
   - ML 加速器倾向局部 scale-up + 全局 scale-out
   - VCU 等通信少的加速器更适合纯 scale-out
   - 加速器系统设计的关键是根据负载通信模式选择互连和扩展方式
```

---

### 二十、如果考试或讨论中要回答这一节，可以这样说

你可以这样概括：

> 6.1.2.3 节讨论加速器系统中的 scale-up 与 scale-out 权衡。虽然传统 WSC 主要使用 scale-out 集群，但加速器系统由于定制设计和垂直整合，可以重新定义这一权衡。关键在于，定制加速器不仅可以定制计算单元，还可以定制互连网络，从而改变远程访问延迟。TPU 使用 ICI 互连构建大型 pod，甚至可达 9,216 个芯片，形成具有共享内存抽象的超算系统；NVIDIA 使用 NVLink 支持最多 256 个 GPU 的高速互连；行业也在推动 UAL 标准。由于机器学习训练通信密集，尤其是 all-reduce、模型并行和张量并行等操作需要高带宽低延迟互连，因此 ML 加速器倾向于在 pod 或超级节点内部深度 scale-up。但当应用超过单个 pod 时，多个 pod 仍然通过 Ethernet scale-out 网络连接。相比之下，VCU 视频处理系统完全拥抱 scale-out，因为视频编码任务彼此独立，几乎不需要相互通信，所以 Ethernet 和分布式任务调度就足够高效。总体来看，scale-up 对较小或通信密集负载具有明显性能和性能成本优势，而 scale-out 则因为成本效率、行业标准硬件和成熟的分布式系统软件投资，对超大负载仍然不可或缺。

---

### 二十一、最后给你一个形象类比

可以把这一节理解成“城市交通系统”。

---

#### 传统 CPU 集群

```text
很多普通办公室
办公室之间靠普通公路通信
公路便宜但慢
```

如果任务需要频繁跨办公室沟通，效率会受影响。

---

#### ML 加速器集群

```text
很多超级办公室组成一个高速园区
园区内部有高速地铁
园区之间再用普通高速公路连接
```

因为 AI 训练需要频繁沟通，所以要在园区内部建高速地铁。

例如：

```text
TPU pod = ICI 高速地铁
GPU superpod = NVLink 高速地铁
跨 pod = Ethernet 高速公路
```

---

#### VCU 视频转码集群

```text
很多独立工厂
每个工厂处理自己的视频任务
工厂之间几乎不需要运输半成品
```

因此不需要昂贵高速地铁，用普通公路调度任务即可。

---

这一节的核心提醒是：

> 加速器时代并不是简单回到 scale-up，也不是简单坚持 scale-out。  
> 真正的设计原则是：  
> **根据工作负载的通信模式，在局部使用高速 scale-up，在全局使用低成本 scale-out。**


**专栏导航**

- ← 上一篇：[6.1.2.2 Granularity of scale-out: Brawny versus wimpy cores](/posts/6-1-2-2-granularity-of-scale-out-brawny-versus-wimpy-cores/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.2.1 Server hardware →](/posts/6-2-1-server-hardware/)
