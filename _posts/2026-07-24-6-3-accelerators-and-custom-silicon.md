---
title: "6.3 Accelerators and custom silicon"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：6.3 Accelerators and custom silicon。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.3 Accelerators and custom silicon。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.3 Accelerators and custom silicon

下面这一部分 **6.3 Accelerators and custom silicon**，尤其是 **6.3.1 Specialization and the end of Moore’s Law** 和 **6.3.2 ML accelerators and TPU systems**，是整本书中非常关键的一节。

它回答了一个很大的问题：

> **为什么早期 WSC 不愿意使用专用加速器，而今天 WSC 却大规模部署 GPU、TPU、FPGA、自研 ASIC 等专用芯片？**

这一节的核心可以概括为：

> **当通用 CPU 的性能/成本增长变慢，而 AI 等新型 workload 的计算需求爆炸式增长时，专用化就从“可选项”变成了“必选项”。**

---

### 1. 这一节在书中的位置

前面几节讲：

- 6.2.1：服务器硬件；
- 6.2.2：机架；
- 6.2.3：服务器本身作为分布式系统；
- 6.3：加速器和定制硅。

也就是说，前面讲的是“通用计算平台如何组织”，而 6.3 开始讲：

> **当通用计算不够用时，WSC 如何通过专用硬件扩展计算能力。**

这一节不是单纯讲“GPU/TPU 很快”，而是在讲：

- 经济学；
- 工艺缩放；
- workload 特征；
- 系统架构；
- 数据中心设计；
- 软件栈；
- 云厂商战略。

---

### 2. 6.3 开头：加速器采用已经指数级扩展

原文开头说：

> In the prior edition of the book, we discussed the introduction of specialized computing accelerators. Their adoption has since expanded exponentially, with a host of new accelerators for machine learning, video processing, networking, data movement, security, etc.

这句话说明一个趋势：

> 加速器已经从“实验性/边缘性技术”变成 WSC 的核心基础设施。

现在的加速器不只用于 ML，还用于：

|领域|加速器示例|
| --------------| ---------------------------------------|
|机器学习训练|GPU、TPU、Trainium、Maia、MTIA|
|机器学习推理|GPU、TPU、Inferentia、MTIA|
|视频处理|VCU、视频转码 ASIC|
|网络|SmartNIC、DPU、网络交换 ASIC|
|数据移动|DPU、存储加速器、压缩/解压加速器|
|安全|加密加速器、压缩/解压、零信任 offload|
|存储|NVMe controller、纠删码加速器|
|数据库|压缩、排序、join 加速器|

这说明 WSC 已经进入：

> **通用 CPU + 大量专用加速器** 的异构计算时代。

---

### 3. 6.3.1 的核心：为什么 WSC 从“避免专用”转向“拥抱专用”？

6.3.1 的标题是：

> Specialization and the end of Moore’s Law

它的关键不是“摩尔定律真的完全结束了”，而是：

> **摩尔定律和 Dennard scaling 带来的通用 CPU 性能/成本指数增长已经明显放缓。**

因此，专用硬件的经济性发生了变化。

---

### 4. 早期 WSC 为什么回避专用计算？

原文说：

> Historically, when we designed the first WSCs, we shied away from deploying special-purpose computing.

早期 WSC 避免专用硬件，主要有几个原因。

---

#### 4.1 专用硬件只适合有限 workload

原文说：

> While it promised greater computing efficiencies, those benefits came at the expense of specializing to a limited number of workloads that could only benefit from them...

专用加速器的问题是：

> 它对某些 workload 很快，但对其他 workload 可能没用。

例如一个视频转码 ASIC 可能非常适合视频编码，但不能用来做：

- 数据库查询；
- Web serving；
- 通用批处理；
- 分布式文件系统；
- 机器学习训练；
- 安全认证。

早期 WSC 更重视通用性，因为：

```text
通用服务器可以运行很多种 workload
→ 提高利用率
→ 降低部署风险
→ 简化管理
```

---

#### 4.2 专用化与 WSC 的 scale/volume 原则冲突

原文说：

> antithetical to the fundamental WSC principles of scale and volume.

WSC 的早期成功依赖：

- 大量采购标准化服务器；
- 大量部署同构机器；
- 统一运维；
- 统一调度；
- 统一软件栈；
- 通过规模降低成本。

如果引入很多专用硬件，会出现：

- 硬件种类变多；
- 驱动和固件变复杂；
- 调度变复杂；
- 故障类型变多；
- 运维成本上升；
- 利用率可能下降；
- 供应链更复杂。

所以早期 WSC 更偏好：

> 大量通用 CPU 服务器，而不是少量专用加速器。

---

#### 4.3 专用硬件开发周期长，容易被通用 CPU 进步淘汰

原文给了一个非常直观的论证：

> when CPU speeds double every year, and an ASIC takes two years to deploy, then it needs to provide a speedup of much more than 4x to amortize its development costs.

这个逻辑非常重要。

假设：

- 通用 CPU 性能每年翻倍；
- 一个 ASIC 需要 2 年设计、流片、部署；
- 那么 2 年后通用 CPU 性能大约是原来的：

```text
2 × 2 = 4 倍
```

也就是说，如果你的 ASIC 两年后上线，它面对的不是“今天的 CPU”，而是“两年后已经快 4 倍的 CPU”。

所以 ASIC 必须：

```text
比两年后的 CPU 还要快很多
```

才能抵消：

- 高昂 NRE 成本；
- 流片成本；
- 验证成本；
- 软件栈成本；
- 运维成本；
- 风险成本。

这就是早期专用硬件难以证明合理性的原因。

---

### 5. Dennard scaling 和 Moore’s Law 的放缓

原文说：

> with the slowing of traditional technology scaling – first, Dennard scaling for power efficiency, and later Moore’s law scaling for cost efficiency – we are no longer seeing compounding high growth rates in general-purpose CPU performance per unit cost.

这句话是理解现代计算机体系结构的关键。

---

#### 5.1 Moore’s Law：晶体管密度增长

摩尔定律通常指：

> 集成电路上的晶体管数量大约每 18–24 个月翻倍。

它带来的好处是：

- 每个晶体管成本下降；
- 同样面积可以放更多逻辑；
- CPU 可以更大 cache、更多核心、更复杂执行单元；
- 计算能力持续提升。

但近年来：

- 先进工艺成本极高；
- mask set 成本极高；
- 良率挑战大；
- 物理限制增强；
- 每代性能提升幅度变小；
- 成本下降速度变慢。

所以原文说的是：

> Moore’s law scaling for cost efficiency 放缓。

不是说晶体管完全不增长了，而是：

> 通用 CPU 每单位成本性能不再像过去那样高速复合增长。

---

#### 5.2 Dennard scaling：功率密度缩放

Dennard scaling 指：

> 当晶体管尺寸缩小时，电压和电流也相应缩小，因此功率密度大致保持不变。

在过去，这意味着：

```text
晶体管更小
→ 可以跑得更快
→ 功率密度不爆炸
→ CPU 频率可以持续提升
```

但后来 Dennard scaling 失效，原因包括：

- 漏电流增加；
- 阈值电压缩放困难；
- 短沟道效应；
- 功耗密度上升；
- 散热受限；
- 暗硅问题。

结果就是：

> 不能简单靠缩小工艺来持续提升频率。

于是出现：

- power wall；
- thermal wall；
- memory wall；
- dark silicon。

---

#### 5.3 通用 CPU 的黄金时代结束

过去：

```text
工艺进步
→ 频率提升
→ 单核性能快速提升
→ 软件不用改也能变快
```

现在：

```text
工艺进步
→ 单核性能提升有限
→ 更多靠多核、cache、加速器、软件并行
→ 通用 CPU 每美元性能增长放缓
```

这改变了体系结构设计的方向。

---

### 6. 为什么专用化重新变得有吸引力？

当通用 CPU 性能/成本增长放缓时，专用硬件的相对优势上升。

---

#### 6.1 专用硬件可以针对固定计算模式优化

很多 workload 有稳定且重复的计算模式。

例如深度学习中的核心操作：

- 矩阵乘法；
- 卷积；
- attention；
- normalization；
- softmax；
- embedding lookup；
- reduce；
- all-reduce。

这些操作非常适合专用硬件优化。

专用加速器可以优化：

- 数据流；
- 片上 SRAM；
- 矩阵乘加阵列；
- 低精度计算；
- 内存带宽；
- 片间互连；
- collective communication；
- 稀疏性；
- 量化；
- 功耗效率。

通用 CPU 为了通用性，必须支持：

- 分支预测；
- 乱序执行；
- 复杂 ISA；
- 通用寄存器；
- 各种数据类型；
- 操作系统；
- 虚拟化；
- 大量 legacy 软件。

这些通用能力对矩阵计算来说可能是开销。

---

#### 6.2 专用硬件可以提高 performance per watt

在 WSC 中，限制往往不是“能不能算”，而是：

- 电力；
- 冷却；
- 机架功率密度；
- 每瓦性能；
- 每美元性能。

专用加速器通常可以在特定任务上实现更高：

```text
performance / watt
performance / dollar
performance / rack
```

这对超大规模数据中心极其重要。

---

#### 6.3 专用硬件可以突破 dark silicon 限制

dark silicon 指：

> 在固定功耗预算下，不能同时打开芯片上所有晶体管。

因此，与其设计一个巨大但无法全开的通用 CPU，不如把面积用于：

- 专用矩阵单元；
- 专用视频编码单元；
- 专用网络处理单元；
- 专用加密单元；
- 专用压缩单元。

这些单元在执行特定任务时更高效。

---

### 7. TPU 的动机：AI 需求可能压垮通用数据中心

原文举了一个非常经典的例子：

> A key motivation for building TPUs was the observation that if every Android user needed only a few minutes of voice recognition capabilities, we would have needed to double the entire computing capacity of Google at that time.

这个例子非常重要。

它的意思是：

> 如果 AI workload 成为大规模用户功能，那么通用 CPU 的算力根本不够。

假设 2013 年：

- 每个 Android 用户每天使用几分钟语音识别；
- 语音识别需要在服务器端推理；
- 如果全部用通用 CPU 跑；
- 那么 Google 可能需要把整个数据中心容量翻倍。

这在经济上和物理上都不可行。

所以必须：

> 用专用加速器大幅提高每瓦、每美元推理性能。

这就是 TPU 出现的核心动机之一。

---

#### 7.1 supply-demand gap

原文说：

> Optimizing hardware for large classes of workloads through special-purpose accelerators such as GPUs or TPUs was the only option to address this supply-demand gap.

这里有一个关键概念：

> supply-demand gap，即算力供给和需求之间的差距。

AI 需求增长非常快：

```text
更多用户
更多模型
更大模型
更复杂推理
更多训练
更多实时服务
```

而通用 CPU 的算力供给增长变慢：

```text
Moore/Dennard 放缓
单核性能增长有限
功耗受限
成本下降变慢
```

因此必须通过专用硬件弥补差距。

---

### 8. 6.3.2：ML accelerators 和 TPU systems

6.3.2 进入 AI workload 和加速器系统。

原文说：

> Deep neural networks and AI workloads are computationally intensive. They are characterized by the need for fast linear algebra operations, large-scale distributed computation, and high bandwidth memory.

这句话概括了 AI workload 的三大特征：

1. 快速线性代数；
2. 大规模分布式计算；
3. 高带宽内存。

---

### 9. AI workload 的计算特征

---

#### 9.1 快速线性代数操作

DNN 的核心计算大量依赖线性代数。

典型操作包括：

- GEMM：通用矩阵乘法；
- batched GEMM；
- convolution；
- attention QKV projection；
- feed-forward network；
- embedding projection；
- gradient computation；
- optimizer updates。

例如 Transformer 中大量操作都是矩阵乘法：

```text
Q = XWq
K = XWk
V = XWv
Attention = softmax(QK^T / sqrt(d))V
Output = AttentionWo
FFN = GeLU(XW1)W2
```

这些操作具有：

- 高并行性；
- 高算术强度；
- 规则数据访问；
- 可批量处理；
- 可低精度计算；
- 可硬件流水线化。

因此非常适合专用加速器。

---

#### 9.2 大规模分布式计算

现代大模型不能只靠一颗芯片训练或推理。

需要：

- 数据并行；
- 张量并行；
- 流水线并行；
- 专家并行；
- 序列并行；
- 多机多卡；
- 多 pod；
- collective communication。

常见 collective operations：

- all-reduce；
- all-gather；
- reduce-scatter；
- all-to-all；
- broadcast；
- barrier。

因此 AI 加速器不只是“算得快”，还必须：

- 芯片间互连快；
- 机架间网络快；
- collective communication 优化；
- 支持大规模同步；
- 支持故障恢复；
- 支持 checkpoint；
- 支持长时间训练。

这就是为什么原文强调：

> large-scale distributed computation

---

#### 9.3 高带宽内存

AI workload 对内存带宽极其敏感。

原因：

- 模型参数很大；
- activation 很大；
- gradient 很大；
- optimizer state 很大；
- KV cache 很大；
- batch size 增大；
- 长上下文增加内存压力。

例如 LLM 推理中，decode 阶段常常是：

```text
memory-bandwidth bound
```

因为每生成一个 token，都要读取大量模型权重或 KV cache。

所以加速器需要：

- HBM；
- 大内存容量；
- 高内存带宽；
- 高片上 SRAM；
- 数据压缩；
- 量化；
- 稀疏；
- 高效数据搬运。

---

### 10. AI workload 的不同阶段

原文说：

> AI workloads encompass multiple phases with distinct computational needs.

这点非常重要。

AI 不只是“训练”或“推理”，而是多个阶段，每个阶段对硬件需求不同。

---

#### 10.1 Training：训练

原文：

> Training requires hundreds or thousands of chips to accommodate large models with many parameters and large volumes of training data, while meeting time-to-convergence requirements.

训练的特点：

- 模型参数多；
- 数据量大；
- 计算量大；
- 需要大规模并行；
- 需要高带宽互连；
- 需要长时间稳定运行；
- 需要 checkpoint；
- 需要故障恢复；
- 需要高利用率；
- 需要尽快收敛。

训练的关键指标不是单卡 FLOPs，而是：

```text
goodput
```

也就是有效训练吞吐，要考虑：

- 计算利用率；
- 通信开销；
- checkpoint 开销；
- 故障重启；
- 数据加载；
- 调试时间；
- 收敛速度。

---

#### 10.2 Inference / ML serving：推理服务

原文：

> Inference, or ML serving, is user-facing with strict latency deadlines but can run in smaller pods.

推理的特点：

- 面向用户；
- 延迟敏感；
- 有 SLO；
- 需要高吞吐；
- 需要成本敏感；
- 需要 batching；
- 需要 autoscaling；
- 需要量化；
- 需要稳定性。

推理不一定需要最大集群，但对：

```text
latency / throughput / cost per request
```

非常敏感。

对于 LLM 推理，还要区分：

##### prefill 阶段

处理输入 prompt，通常：

```text
compute-bound
```

##### decode 阶段

逐 token 生成，通常：

```text
memory-bandwidth-bound
```

因此 LLM 推理系统需要同时优化：

- 计算；
- 内存带宽；
- KV cache；
- batch scheduling；
- continuous batching；
- speculative decoding；
- quantization；
- paged attention；
- 长上下文管理。

---

#### 10.3 Fine-tuning：微调

原文：

> Fine-tuning and distillation occupy a middle ground, but with unique considerations, e.g., large models with small datasets on moderate-scale systems.

微调特点：

- 模型可能很大；
- 数据集相对小；
- 不一定需要超大规模集群；
- 但仍需要大内存；
- 可能需要 optimizer state；
- 可能需要 LoRA / QLoRA 等参数高效微调；
- 对成本和灵活性敏感。

微调常见场景：

- 行业模型；
- 企业私有数据；
- 指令微调；
- RLHF；
- DPO；
- 安全对齐；
- 多语言适配。

---

#### 10.4 Distillation：蒸馏

蒸馏通常用一个大 teacher 模型指导小 student 模型。

特点：

- 需要运行 teacher 生成 logits / labels；
- 需要训练 student；
- 可能同时涉及大模型推理和训练；
- 对内存和吞吐都有要求；
- 通常用于降低推理成本。

蒸馏的价值：

```text
大模型能力
→ 迁移到小模型
→ 降低部署成本
```

---

### 11. LLM 放大了 AI 系统需求

原文：

> The rise of Large Language Models has amplified these demands.

LLM 对系统的需求被极大放大。

原因包括：

- 模型参数巨大；
- 上下文长度增加；
- token 生成长序列；
- KV cache 很大；
- 训练需要数千甚至更多加速器；
- 推理需要低延迟和高吞吐；
- 多轮对话增加状态管理；
- agent/workflow 增加调用次数；
- 多模态增加计算复杂度；
- 安全和对齐增加额外开销。

LLM 不只是模型问题，而是系统问题：

```text
模型
+ 编译器
+ 调度器
+ 加速器
+ 内存
+ 网络
+ 存储
+ checkpoint
+ 监控
+ 安全
+ 成本优化
```

---

### 12. GPU：从图形渲染到 ML 加速基石

原文：

> GPUs, originally used primarily for graphics rendering, have emerged as a cornerstone of modern ML acceleration.

GPU 成功的原因：

1. 大规模并行架构；
2. 高内存带宽；
3. SIMT 执行模型适合规则并行；
4. CUDA 生态成熟；
5. 深度学习框架支持好；
6. 可编程性强；
7. 适合快速演进的算法；
8. 训练和推理都能用；
9. 产业链成熟。

GPU 的优势是：

> 灵活性 + 高性能 + 成熟生态。

但 GPU 也有挑战：

- 功耗高；
- 成本高；
- 供应紧张；
- 软件栈复杂；
- 多卡互连和集群网络复杂；
- 对数据中心的电力和冷却压力很大。

---

### 13. TPU：Google 的专用 AI 加速器

原文：

> Google has designed and deployed multiple generations of even more specialized accelerators for AI, called TPUs.

TPU 是 domain-specific accelerator。

它的设计目标通常包括：

- 高效矩阵乘法；
- 高吞吐 tensor 计算；
- 高能效；
- 与 TensorFlow / JAX / XLA 深度集成；
- 大规模 pod 互连；
- 高带宽内存；
- 训练和推理系统优化。

TPU 与 GPU 的关键区别在于：

> GPU 更通用，TPU 更专用。

专用化的好处是：

- 对目标 workload 更高 performance/watt；
- 更高 performance/dollar；
- 更适合 Google 自有 workload；
- 可与数据中心系统协同设计。

代价是：

- 灵活性较低；
- 软件栈需要适配；
- 对非目标 workload 可能不友好；
- 硬件演进需要与模型演进匹配。

---

### 14. FPGA、ASIC 和其他加速器

原文列举了多家公司的路线。

---

#### 14.1 Microsoft：FPGA 到 ASIC

原文：

> Microsoft has utilized FPGAs through the Catapult and Brainwave programs, and later introduced the dedicated ASIC Maia.

Microsoft 的路径很有代表性。

##### FPGA 的优点

FPGA 可重新编程。

适合：

- 算法快速演进；
- 低延迟推理；
- 网络 offload；
- 搜索排序；
- 实验性加速器；
- 避免 ASIC 高 NRE 风险。

FPGA 比 CPU 更高效，但通常不如 ASIC 极致。

##### ASIC 的优点

ASIC 固定功能更强，适合：

- workload 已稳定；
- 规模足够大；
- 需要极致 performance/watt；
- 需要长期部署。

Maia 代表 Microsoft 进入自研 AI ASIC。

---

#### 14.2 Meta：MTIA

原文：

> Meta has developed MTIA, Meta Training and Inference Accelerator.

Meta 有巨大推荐系统和 AI workload。

自研加速器可以帮助：

- 降低推理成本；
- 提高推荐系统效率；
- 减少对通用 GPU 的依赖；
- 针对内部模型优化；
- 与数据中心基础设施协同。

---

#### 14.3 Amazon：Inferentia 和 Trainium

原文：

> Amazon has introduced its Inferentia and Trainium systems.

AWS 的路线很清晰：

- Inferentia：面向推理；
- Trainium：面向训练。

云厂商自研芯片的动机：

- 降低云上 AI 成本；
- 提供差异化实例；
- 提高供应稳定性；
- 优化自有服务；
- 提高长期利润率；
- 构建软硬件生态。

---

### 15. 为什么超大规模云厂商能做 custom silicon？

定制芯片非常贵，但超大规模厂商有特殊优势。

---

#### 15.1 有足够 workload 量摊销 NRE

ASIC 的 NRE 成本很高，包括：

- 架构设计；
- RTL；
- 验证；
- 物理设计；
- mask set；
- 封装；
- 测试；
- 软件栈；
- 编译器；
- 驱动；
- 运维工具；
- 可靠性验证。

如果产量小，成本无法摊销。

但超大规模厂商有：

- 自有云服务；
- 自有搜索/推荐/广告；
- 自有 AI 产品；
- 大量内部 workload；
- 长期部署需求。

因此可以摊销高昂开发成本。

---

#### 15.2 可以软硬协同设计

云厂商可以一起设计：

- 芯片；
- 编译器；
- 框架；
- 调度器；
- 网络；
- 存储；
- 冷却；
- 机架；
- 监控；
- 安全；
- 运维系统。

这种垂直整合可以带来系统级优化。

---

#### 15.3 可以降低供应链风险

依赖单一 GPU 供应商存在风险：

- 供应不足；
- 价格波动；
- 交付周期长；
- 产品路线不可控；
- 云厂商议价能力受限。

自研芯片可以：

- 多元化供应；
- 提高议价能力；
- 控制产品路线；
- 针对自身业务优化。

---

### 16. 专用加速器不是“芯片问题”，而是“系统问题”

这一节虽然讲 accelerators and custom silicon，但必须放在 WSC 视角理解。

加速器要成功，不只是芯片快。

还需要：

- 高速互连；
- 高带宽内存；
- 机架供电；
- 液冷；
- 高速网络；
- 存储系统；
- checkpoint；
- 调度器；
- 编译器；
- 框架支持；
- 监控；
- attestation；
- 故障恢复；
- 运维自动化；
- 成本控制。

这与前面章节紧密相关：

|前面章节|与加速器关系|
| -------------------------------| -------------------------------------|
|server hardware|加速器卡、PCIe、CXL、电源、散热|
|rack|高功率密度、液冷、ToR、电源|
|server as distributed systems|accelerator arena、RoT、attestation|
|data center fabric|大规模训练互连|
|pods/cliques|AI 训练集群拓扑|
|control plane|加速器 fleet 管理|

---

### 17. 专用化的核心权衡

这一节背后有一个经典体系结构权衡。

---

#### 17.1 通用性 vs 专用性

通用 CPU：

```text
优点：灵活、可编程、适合多 workload
缺点：每瓦性能不是最优
```

专用加速器：

```text
优点：目标 workload 高效
缺点：灵活性差、开发成本高、依赖软件栈
```

---

#### 17.2 灵活性 vs 效率

GPU 比 ASIC 灵活。

ASIC 比 GPU 更高效。

FPGA 处于中间：

```text
灵活性：CPU > GPU > FPGA > ASIC
效率：ASIC > FPGA > GPU > CPU
```

这只是粗略排序，实际取决于 workload。

---

#### 17.3 短期成本 vs 长期 TCO

ASIC 短期成本高：

- 设计贵；
- 流片贵；
- 软件栈贵。

但如果 workload 足够大且稳定，长期 TCO 可能更低。

---

#### 17.4 硬件寿命 vs 算法演进

AI 算法变化很快。

如果硬件太专用，可能：

- 两年后模型架构变化；
- 新算子不支持；
- 软件栈迁移困难；
- 利用率下降。

因此专用硬件需要一定可编程性。

---

### 18. 关键术语表

|术语|含义|
| ------------------------------| -------------------------------------------------------|
|accelerator|加速器，针对特定计算任务优化|
|custom silicon|定制芯片|
|ASIC|Application-Specific Integrated Circuit，专用集成电路|
|FPGA|Field-Programmable Gate Array，现场可编程门阵列|
|GPU|Graphics Processing Unit，图形处理器/并行加速器|
|TPU|Tensor Processing Unit，张量处理器|
|DNN|Deep Neural Network，深度神经网络|
|LLM|Large Language Model，大语言模型|
|Moore’s Law|晶体管密度增长趋势|
|Dennard scaling|工艺缩放时功率密度大致恒定的规律|
|performance per watt|每瓦性能|
|performance per dollar|每美元性能|
|NRE|Non-Recurring Engineering，一次性工程成本|
|HBM|High Bandwidth Memory，高带宽内存|
|GEMM|General Matrix Multiply，通用矩阵乘法|
|training|模型训练|
|inference|模型推理|
|fine-tuning|微调|
|distillation|蒸馏|
|time-to-convergence|收敛所需时间|
|pod|一组加速器/机架构成的计算单元|
|clique|高带宽互连的加速器组|
|domain-specific architecture|领域专用架构|
|dark silicon|固定功耗下无法同时启用的芯片区域|
|supply-demand gap|算力供给与需求之间的差距|

---

### 19. 可以用来检验理解的问题

---

#### 问题 1：为什么早期 WSC 不喜欢专用硬件？

因为早期 WSC 强调：

- 通用性；
- 规模化；
- 同构部署；
- 高利用率；
- 简运维；
- 低成本采购。

专用硬件只适合有限 workload，且开发周期长，容易被快速进步的通用 CPU 淘汰。

---

#### 问题 2：为什么 ASIC 需要远大于 4x 加速？

如果 CPU 每年性能翻倍，ASIC 两年后上线时，CPU 已经快约 4 倍。

ASIC 必须比两年后的 CPU 还快很多，才能摊销：

- 设计成本；
- 流片成本；
- 软件成本；
- 运维成本；
- 风险成本。

---

#### 问题 3：Dennard scaling 放缓意味着什么？

意味着工艺缩小不再自动带来等比例功耗效率提升。

结果：

- 频率提升受限；
- 功耗密度上升；
- 散热受限；
- dark silicon 出现；
- 通用 CPU 单核性能增长放缓。

---

#### 问题 4：为什么 AI workload 适合专用加速器？

因为 AI workload 有大量规则计算，例如：

- 矩阵乘法；
- 卷积；
- attention；
- normalization；
- collective communication。

这些操作适合通过专用数据流、片上存储、低精度计算和高带宽内存优化。

---

#### 问题 5：training 和 inference 的硬件需求有什么不同？

training：

- 需要大规模芯片；
- 高互连带宽；
- 高内存容量；
- 高可靠性；
- 长时间运行；
- 关注 time-to-convergence。

inference：

- 面向用户；
- 延迟敏感；
- 成本敏感；
- 关注吞吐、SLO、每请求成本；
- 可在较小 pod 中运行。

---

#### 问题 6：为什么超大规模云厂商纷纷自研 AI 芯片？

因为他们有：

- 巨大 workload 量；
- 长期部署需求；
- 软硬协同能力；
- 降低 TCO 动机；
- 供应链多元化需求；
- 差异化云服务需求。

---

### 20. 这一节可以整理成的精简笔记

```text
6.3 Accelerators and custom silicon
6.3.1 Specialization and the end of Moore’s Law
6.3.2 ML accelerators and TPU systems

1. 核心问题：
   为什么 WSC 从早期回避专用硬件，
   转向今天大规模部署 GPU、TPU、FPGA 和自研 ASIC？

2. 早期 WSC 回避专用计算的原因：
   - 专用硬件只适合有限 workload；
   - 与 WSC 的 scale、volume、同质化原则冲突；
   - 会增加硬件种类、运维复杂度和软件成本；
   - 专用硬件开发周期长，容易被通用 CPU 快速进步淘汰。

3. ASIC 的经济学直觉：
   - 如果通用 CPU 性能每年翻倍；
   - ASIC 需要两年才能部署；
   - 两年后通用 CPU 性能约提升 4 倍；
   - ASIC 必须比未来 CPU 快很多，才能摊销高昂开发成本。

4. 技术缩放放缓：
   - Dennard scaling 放缓后，工艺缩小不再自动带来等比例功耗效率提升；
   - Moore’s law 的成本效率增长也放缓；
   - 通用 CPU 每单位成本性能不再高速复合增长；
   - 专用化的相对收益上升。

5. 专用化重新变得重要的原因：
   - 通用 CPU 性能/成本增长变慢；
   - AI 等新 workload 需求爆炸；
   - 数据中心受功耗、冷却和 TCO 约束；
   - 专用硬件可提高 performance/watt 和 performance/dollar；
   - 超大规模 workload 可以摊销 NRE。

6. TPU 的关键动机：
   - 如果每个 Android 用户只需要几分钟语音识别，
     Google 可能需要翻倍当时全部计算容量；
   - 通用 CPU 无法经济地满足这种大规模 AI 推理需求；
   - 专用加速器是弥补算力供需差距的必要手段。

7. AI workload 的计算特征：
   - 大量线性代数操作，如 GEMM、卷积、attention；
   - 高并行性；
   - 高算术强度；
   - 需要高带宽内存；
   - 需要大规模分布式计算；
   - 需要高速片间和机架间互连；
   - 需要 collective communication 优化。

8. AI workload 的不同阶段：
   - Training：
       需要数百到数千芯片，
       大模型、大数据、高互连、高可靠性，
       关注 time-to-convergence；
   - Inference / ML serving：
       面向用户，延迟敏感，
       可在较小 pod 中运行，
       关注吞吐、SLO 和每请求成本；
   - Fine-tuning：
       大模型、小数据集、中等规模系统，
       关注内存、优化器状态和成本；
   - Distillation：
       用大模型指导小模型，
       同时涉及推理和训练，
       目标是降低部署成本。

9. LLM 的影响：
   - 模型参数更大；
   - 上下文更长；
   - KV cache 更大；
   - 训练集群规模更大；
   - 推理延迟和吞吐要求更高；
   - prefill 常偏 compute-bound，decode 常偏 memory-bandwidth-bound；
   - LLM 放大了对加速器、内存、网络和系统软件的需求。

10. GPU：
   - 原本用于图形渲染；
   - 现在成为现代 ML 加速基石；
   - 优势是并行性、高内存带宽、可编程性和 CUDA 生态；
   - 适合训练、推理和快速演进的算法；
   - 挑战是功耗、成本、供应和集群互连复杂性。

11. TPU：
   - Google 设计的专用 AI 加速器；
   - 针对 tensor/矩阵计算优化；
   - 强调高能效、高吞吐和系统级集成；
   - 与 Google AI 软件栈和数据中心基础设施协同设计；
   - 相比 GPU 更专用，灵活性较低但目标 workload 效率更高。

12. 其他加速器路线：
   - Microsoft 先用 FPGA，如 Catapult 和 Brainwave，
     后推出专用 ASIC Maia；
   - Meta 开发 MTIA；
   - Amazon 推出 Inferentia 和 Trainium；
   - 说明超大规模厂商普遍走向 custom silicon。

13. 超大规模厂商自研芯片的原因：
   - 有足够 workload 量摊销 NRE；
   - 可软硬协同设计；
   - 可降低 TCO；
   - 可提高供应稳定性；
   - 可形成云服务差异化；
   - 可减少对单一供应商依赖。

14. 专用加速器是系统问题：
   - 不只是芯片快；
   - 还需要网络、内存、存储、冷却、电源、调度、
     编译器、框架、监控、attestation 和运维系统；
   - 加速器必须放在 rack、pod、data center fabric
     和 control plane 中理解。

15. 核心权衡：
   - 通用性 vs 专用性；
   - 灵活性 vs 效率；
   - 短期开发成本 vs 长期 TCO；
   - 硬件寿命 vs 算法演进；
   - 单芯片性能 vs 集群 goodput；
   - 供应商生态 vs 自研控制力。

16. 总结：
   专用加速器的兴起不是因为“加速器天然更好”，
   而是因为通用 CPU 的性能/成本增长放缓，
   同时 AI 等 workload 的规模、带宽和能效需求爆炸。
   WSC 通过 GPU、TPU、FPGA 和自研 ASIC
   构建异构计算基础设施，
   以在性能、成本、功耗和规模化部署之间取得新的平衡。
```

---

### 21. 如果考试或讨论中要回答这一节，可以这样说

> 6.3.1 和 6.3.2 讨论的是 WSC 为什么从早期回避专用硬件，转向大规模部署加速器和定制硅。早期 WSC 设计强调通用性、规模经济和同构部署。专用加速器虽然对某些 workload 更高效，但只能服务有限任务，会增加硬件种类、软件栈和运维复杂度，这与 WSC 的 scale 和 volume 原则相冲突。此外，专用硬件开发周期长、NRE 成本高。如果通用 CPU 性能每年翻倍，而 ASIC 需要两年才能部署，那么 ASIC 上线时面对的 CPU 已经快了约 4 倍，因此 ASIC 必须提供远大于 4 倍的实际收益，才能摊销开发成本。
>
> 但是，随着 Dennard scaling 和 Moore’s law 的收益逐渐放缓，通用 CPU 每单位成本性能不再像过去那样高速复合增长。与此同时，AI 等新型 workload 的计算需求爆炸式增长。原文举了 TPU 的动机：如果每个 Android 用户只需要几分钟语音识别，Google就可能需要翻倍当时全部计算容量。通用 CPU 无法经济地满足这种规模的需求，因此必须通过 GPU、TPU 等专用加速器来弥补算力供给和需求之间的差距。
>
> 6.3.2 进一步说明 AI workload 为什么适合专用加速器。DNN 和 AI workload 高度依赖线性代数操作，例如矩阵乘法、卷积和 attention，同时需要大规模分布式计算和高带宽内存。AI workload 还包含多个阶段：训练需要数百到数千颗芯片、大模型、大数据集、高互连带宽和长时间可靠运行；推理面向用户，对延迟、吞吐和每请求成本敏感；微调和蒸馏则处于中间地带，需要在大模型、小数据集和中等规模系统之间平衡。LLM 的兴起进一步放大了对计算、内存、网络和系统软件的需求。
>
> 在加速器路线方面，GPU 从图形渲染发展为现代 ML 加速的基石，优势在于并行性、高内存带宽、可编程性和成熟生态。Google 设计了多代 TPU，作为更专用的 tensor 加速器，强调高能效和系统级集成。Microsoft 早期通过 Catapult 和 Brainwave 使用 FPGA，后来推出专用 ASIC Maia；Meta 开发了 MTIA；Amazon 推出了 Inferentia 和 Trainium。超大规模云厂商之所以能够自研芯片，是因为他们拥有足够大的 workload 量来摊销高昂 NRE，并且可以通过软硬件协同设计降低 TCO、提高供应稳定性、形成差异化云服务。
>
> 总体而言，这一节的核心结论是：专用加速器的兴起不是因为专用硬件天然优于通用 CPU，而是因为通用 CPU 的性能/成本增长放缓，同时 AI workload 的规模、带宽和能效需求急剧上升。现代 WSC 不再是单一通用计算集群，而是由 CPU、GPU、TPU、FPGA、ASIC、SmartNIC 和各类加速器组成的异构系统。评价加速器也不能只看单芯片性能，而要看它在机架、pod、网络、存储、调度、编译器和数据中心运维中的整体 performance per watt、performance per dollar 和系统级 goodput。


**专栏导航**

- ← 上一篇：[6.2.3 Individual servers as distributed systems](/posts/6-2-3-individual-servers-as-distributed-systems/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.3.2.1 TPUs →](/posts/6-3-2-1-tpus/)
