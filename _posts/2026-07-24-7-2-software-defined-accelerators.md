---
title: "7.2 Software-defined accelerators"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：7.2 Software-defined accelerators。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.2 Software-defined accelerators。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.2 Software-defined accelerators

下面把 **7.2 Software-defined accelerators** 作为一个独立小节来深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

---

### 7.2 Software-defined accelerators 深入理解

这一节把 software-defined infrastructure 的思想从 CPU、服务器、集群调度，进一步扩展到：

> accelerators，加速器。

原文举的例子是：

> H2O-NAS：hyperscale hardware optimized neural architecture search。

这个小节的核心不是讲如何设计一块新的加速器芯片，而是讲：

> 如何用软件、算法和自动搜索，让运行在加速器上的 ML 模型更适合底层硬件，从而在超大规模加速器系统上获得更高性能、更高能效和更好利用率。

这和前面几节形成很有意思的对照：

|前面几节|这一节|
| --------------------------------| -----------------------------------------|
|给定工作负载，选择最合适的硬件|给定硬件平台，自动设计/调整工作负载本身|
|platform-aware scheduling|hardware-aware model design|
|调度适配硬件|模型适配硬件|
|software-defined servers|software-defined accelerators|

---

#### 一、为什么 software-defined infrastructure 可以扩展到加速器？

原文开头说：

> The idea of software-defined infrastructure can, at a broad level, also be applied to accelerators.

也就是说，软件定义基础设施的思想并不只适用于 CPU、服务器、网络或存储，也可以用于加速器。

在 ML 时代，加速器越来越重要，例如：

- GPU；
- TPU；
- FPGA；
- 自定义 AI 芯片；
- domain-specific accelerators。

但加速器本身只是硬件。  
要真正发挥加速器潜力，还需要软件层决定：

- 跑什么模型；
- 模型结构如何；
- 模型多大；
- 如何并行；
- 如何切分；
- 如何利用内存层级；
- 如何匹配加速器计算单元；
- 如何在大规模集群上高效训练或推理。

因此：

> 加速器不只是被“使用”，也可以被软件“定义”和“优化”。

---

### 二、背景：ML 模型对算力的需求不断增长

原文提到：

> In Chapter 6.3 we discussed how ML models demand ever-increasing computational power.

这与第 6.3 章相关。ML 模型，尤其是大模型，对算力需求持续增长：

- 模型参数越来越多；
- 训练数据越来越大；
- 模型结构越来越复杂；
- 训练和推理成本越来越高；
- 对加速器依赖越来越强。

因此原文提出一个关键观点：

> To fully harness the potential of ML hardware at scale, model efficiency has become as important as building new hardware infrastructure.

也就是说：

> 要在大规模 ML 硬件上充分释放潜力，模型效率和建造新硬件同样重要。

这句话很重要。

它意味着：

> 不能只靠“更强的硬件”解决 ML 算力问题，还必须让模型本身更高效。

---

#### 1. 什么是 model efficiency？

model efficiency 可以包括很多方面：

- 更少的计算量；
- 更少的参数；
- 更低的内存占用；
- 更适合硬件并行；
- 更少的通信开销；
- 更高的加速器利用率；
- 更短的训练时间；
- 更低的能耗；
- 在相同质量下更低成本。

换句话说：

> 不是单纯追求模型准确率，而是追求“准确率 / 成本 / 延迟 / 能耗 / 硬件利用率”的综合最优。

---

#### 2. 为什么模型效率在超大规模硬件上特别重要？

因为在大加速器集群上，低效模型会造成巨大浪费。

例如：

- 模型太大，无法高效放入 TPU pod；
- 模型形状不适合加速器 tile；
- 模型并行切分不均衡；
- 某些加速器核心空闲；
- 通信开销过高；
- batch size 上不去；
- 内存频繁换入换出；
- 训练时间过长；
- 能耗过高。

这些问题不是简单“买更多加速器”就能解决的。  
更好的办法之一是：

> 从模型设计阶段就让模型适合硬件。

---

### 三、什么是 Neural Architecture Search，NAS？

原文引入 NAS：

> Neural architecture search, NAS, has shown significant promise in automatically designing ML model architectures that rival the best human-designed models.

NAS 是：

> 神经架构搜索。

它的目标是：

> 自动搜索神经网络结构，而不是完全依赖人工设计。

传统 ML 模型结构通常由工程师设计，例如：

- 多少层；
- 每层多宽；
- 卷积核多大；
- 使用什么激活函数；
- 如何残差连接；
- 如何下采样；
- 如何组合模块。

NAS 则试图让算法自动搜索这些设计选择。

原文说：

> NAS approaches have four key dimensions.

也就是 NAS 方法有四个关键维度。

---

### 四、NAS 的四个关键维度

这一部分值得展开理解。

---

#### 1. search strategy：搜索策略

原文例子：

> one-shot vs. multi-trial

---

##### multi-trial

multi-trial 指：

> 每个候选架构都单独训练和评估。

优点是评估比较准确。  
缺点是成本极高，因为每个架构都要从头训练。

例如：

```text
架构 A：训练一次
架构 B：训练一次
架构 C：训练一次
...
```

如果搜索空间很大，成本会非常夸张。

---

##### one-shot

one-shot 指：

> 训练一个包含许多候选架构的超级网络，然后从其中采样或派生子网络进行评估。

优点是可以大幅降低搜索成本。  
因为不同候选架构可以共享训练结果或权重。

可以粗略理解为：

```text
训练一个大的 supernet
    ↓
从中抽取多个子架构
    ↓
评估这些子架构
```

这在大规模 NAS 中非常重要。

---

#### 2. search algorithm：搜索算法

原文例子：

> reinforcement learning, gradient-based algorithm, and evolution algorithm.

常见 NAS 搜索算法包括：

|算法|思想|
| ------------------------| ------------------------------------------|
|reinforcement learning|把架构设计看成动作，用奖励信号训练控制器|
|gradient-based|用梯度方法优化连续化的架构参数|
|evolution algorithm|用进化、变异、选择方式搜索架构|

原文后面说 H2O-NAS：

> augments the traditional reinforcement-learning-based search algorithm

说明它主要基于强化学习，并做了硬件感知扩展。

---

#### 3. search space：搜索空间

原文提到：

> hardware-specialization and weight-sharing

search space 是：

> NAS 可以搜索哪些模型结构。

例如搜索空间可以包括：

- 层数；
- 隐藏维度；
- attention head 数；
- kernel size；
- expansion ratio；
- 模块连接方式；
- 是否使用某种算子；
- 模型宽度；
- 模型深度；
- 并行友好结构。

---

##### hardware-specialization

hardware-specialization 指：

> 搜索空间不是任意模型结构，而是针对硬件特性专门设计。

例如，对于 TPU 或 GPU，可能更适合：

- 矩阵乘法密集结构；
- 规则 tensor shape；
- 较大 tile；
- 高并行度；
- 少量不规则控制流；
- 适合模型并行或数据并行的结构；
- 内存访问模式友好的结构。

如果搜索空间完全不考虑硬件，可能搜出来的模型理论上准确率高，但实际硬件效率很差。

---

##### weight-sharing

weight-sharing 指：

> 不同候选架构之间共享部分或全部权重，以降低训练和搜索成本。

这在 one-shot NAS 中很常见。

例如一个 supernet 包含很多子网，不同子网可以共享已训练的权重，这样不需要每个子网都从零训练。

---

#### 4. search objective：搜索目标

原文说：

> reward functions, quality and performance signals.

search objective 是：

> NAS 到底优化什么。

传统 NAS 可能主要优化：

- accuracy；
- loss；
- validation quality。

但 hardware-aware NAS 还会优化：

- latency；
- throughput；
- energy；
- model size；
- memory footprint；
- hardware utilization；
- training speed；
- inference cost；
- 是否适合 TPU pod；
- 是否适合大规模并行。

也就是说，奖励函数不再只是：

```text
reward = accuracy
```

而可能变成：

```text
reward = accuracy + hardware_efficiency - cost
```

或者某种综合目标。

---

### 五、H2O-NAS 是什么？

原文说：

> H2O-NAS takes this traditional NAS approach and extends it to be hardware-aware.

H2O-NAS 的核心是：

> hardware-aware NAS。

也就是：

> 在神经架构搜索中显式考虑超大规模加速器硬件的约束和效率。

它不是只找一个“准确率最高”的模型，而是找一个：

- 质量足够好；
- 能适配硬件；
- 训练更快；
- 更适合 TPU pod；
- 更省能耗；
- 更适合生产流量；
- 总体收益更高的模型。

---

#### 1. H2O-NAS 对传统 NAS 的扩展

原文说：

> It augments the traditional reinforcement-learning-based search algorithm with hardware optimized search spaces optimized for weight-sharing.

可以拆成两点。

---

##### 第一：基于强化学习搜索算法

H2O-NAS 使用 RL-based search algorithm。

强化学习可以理解为：

```text
agent 选择模型架构
    ↓
环境返回奖励
    ↓
agent 更新策略
    ↓
未来选择更好的架构
```

奖励信号可以包括：

- 模型质量；
- 训练速度；
- 硬件利用率；
- 能耗；
- 是否适合 TPU pod。

---

##### 第二：硬件优化的搜索空间

H2O-NAS 的搜索空间不是任意架构，而是针对硬件优化过的。

也就是说，它限制或引导搜索算法去找：

- 更适合加速器计算模式的结构；
- 更适合 weight-sharing 的结构；
- 更适合大规模训练的结构；
- 更适合 TPU pod 的结构。

这体现了：

> hardware constraints enter the model design process.

---

### 六、原文中的关键例子：模型略大导致无法适配 TPU pod

原文给了一个非常直观的例子：

> the highest-quality model, given a fixed training budget, might be just a bit too large to fit into a TPU pod, and tweaking its size and architecture could produce a revised model that trains twice as fast in practice, at a minimal loss in quality.

这个例子很关键。

---

#### 1. “最高质量模型”不一定是最优系统选择

在固定训练预算下，搜索算法可能找到一个质量最高的模型。

但它可能：

> just a bit too large to fit into a TPU pod.

也就是稍微太大，不能很好地放入 TPU pod。

这时会出现什么问题？

- 无法部署；
- 需要更低效的切分；
- 需要更多通信；
- 需要更小 batch size；
- 某些 TPU 核心无法充分利用；
- 内存压力大；
- 训练速度下降。

所以它虽然“质量最高”，但系统效率可能很差。

---

#### 2. 稍微调整模型大小和结构，可能获得巨大系统收益

原文说：

> tweaking its size and architecture could produce a revised model that trains twice as fast in practice, at a minimal loss in quality.

也就是说：

> 把模型稍微调小或调整结构，虽然质量略有损失，但训练速度可能快两倍。

这说明系统优化中常见的思想：

> 局部最优不等于全局最优。

从模型准确率看，最大的模型可能最好。  
但从整个训练系统看，能高效跑在 TPU pod 上的模型可能总体更好。

---

#### 3. 这体现了 hardware-aware 的核心价值

传统模型设计可能问：

> 哪个模型准确率最高？

hardware-aware NAS 问的是：

> 哪个模型在给定硬件上综合收益最好？

综合收益包括：

```text
accuracy
+ training speed
+ hardware utilization
+ energy efficiency
+ deployability
- quality loss
- infrastructure cost
```

---

### 七、H2O-NAS 如何适应超大规模硬件和数据？

原文说：

> To better optimize for scale of hyperscale hardware and data, H2O-NAS uses a massively parallel single-step reinforcement learning search algorithm to search the model architecture and train the model weights simultaneously using real-time production traffic.

这句话信息量很大。

---

#### 1. massively parallel：大规模并行

H2O-NAS 不是小规模慢慢搜，而是利用超大规模计算资源并行搜索。

这很适合 hyperscale 环境，因为 WSC 本身有大量计算资源，可以并行评估许多候选架构。

---

#### 2. single-step reinforcement learning：单步强化学习搜索

原文说它使用：

> massively parallel single-step reinforcement learning search algorithm。

这里不需要过度纠结算法细节。可以理解为：

> H2O-NAS 使用一种高效、可大规模并行的 RL 搜索方式，减少传统 NAS 中反复训练、多轮试错的成本。

传统 NAS 可能很昂贵：

```text
搜索架构 → 训练 → 评估 → 再搜索 → 再训练
```

H2O-NAS 试图让搜索和训练更高效地结合。

---

#### 3. 搜索模型架构和训练模型权重同时进行

原文说：

> search the model architecture and train the model weights simultaneously

这很关键。

传统方式可能是：

```text
先搜索架构
    ↓
再训练最终模型
```

H2O-NAS 则是：

```text
搜索架构的同时训练权重
```

这样可以：

- 减少额外搜索成本；
- 让架构搜索直接基于真实训练过程；
- 更快反馈；
- 更适合生产环境。

---

#### 4. 使用 real-time production traffic

原文说：

> using real-time production traffic.

也就是说，它不是只用离线数据集搜索，而是利用实时生产流量。

这意味着模型优化更贴近真实业务：

- 真实数据分布；
- 真实请求模式；
- 真实质量要求；
- 真实硬件负载；
- 真实生产约束。

这比离线 benchmark 更能反映实际收益。

---

### 八、H2O-NAS 的效果

原文说：

> this approach, deployed at Google, has demonstrated significant performance and energy efficiency gains at scale with comparable or better model accuracies and quality.

也就是说，H2O-NAS 在 Google 部署后实现了：

- 显著性能提升；
- 显著能效提升；
- 模型精度和质量相当或更好。

这个结果非常重要，因为它说明：

> hardware-aware model design 不只是牺牲质量换效率，而是可能同时改善系统效率并保持甚至提升质量。

---

### 九、如何理解 “software-defined accelerators”？

这一节标题是 software-defined accelerators，但例子是 NAS。  
理解时要注意：这里的“软件定义加速器”不是说加速器硬件不存在，而是说：

> 软件可以定义加速器上运行的计算结构、模型形态和优化目标，从而让加速器系统表现得更像为特定工作负载量身定制。

可以从三个层面理解。

---

#### 1. 软件定义“加速器上跑什么”

传统方式：

> 人设计模型，然后放到加速器上跑。

软件定义方式：

> 算法根据硬件自动搜索最适合的模型。

---

#### 2. 软件定义“模型如何适配硬件”

H2O-NAS 会考虑：

- TPU pod 容量；
- 加速器并行方式；
- 内存限制；
- 计算单元效率；
- 训练吞吐；
- 能耗。

因此模型不是硬件无关的，而是硬件共同设计出来的。

---

#### 3. 软件定义“加速器系统的优化目标”

传统目标可能是：

> accuracy 最大。

软件定义加速器系统目标可能是：

> 在真实生产环境中，以最低能耗和最高硬件利用率，达到足够好的模型质量。

---

### 十、与前面几节的联系

这一节可以和 7.1 的几个案例形成完整图景。

---

#### 1. 与 software-defined servers 的关系

software-defined servers 强调：

> 软件理解和控制服务器硬件。

software-defined accelerators 则进一步强调：

> 软件不仅控制硬件资源，还可以塑造运行在硬件上的模型和计算。

---

#### 2. 与 TCMalloc 的关系

TCMalloc 是：

> 优化基础库，让程序更好使用内存和 TLB。

H2O-NAS 是：

> 优化模型架构，让 ML 模型更好使用加速器。

两者都是：

> hardware-aware software optimization。

---

#### 3. 与 platform-aware scheduling 的关系

platform-aware scheduling 是：

> 给定模型/任务，找最合适平台。

H2O-NAS 是：

> 给定平台，找最合适模型架构。

两者合起来就是更完整的软硬件协同：

```text
一方面：把 workload 调度到合适 hardware。
另一方面：把 workload 设计成适合 hardware。
```

---

### 十一、这一节的关键系统思想

---

#### 1. 模型设计不再是纯算法问题，也是系统问题

过去模型设计主要关心：

- accuracy；
- loss；
- generalization。

现在还要关心：

- 是否能放入加速器；
- 是否适合并行；
- 是否通信友好；
- 是否能耗低；
- 是否训练快；
- 是否适合生产流量。

---

#### 2. 最优模型不是“准确率最高”，而是“系统综合最优”

原文例子非常清楚：

> 最高质量模型可能略大，不适合 TPU pod；  
> 稍作调整后训练快两倍，质量损失很小。

这说明：

> 系统层面的最优解往往不是单一指标最优解。

---

#### 3. 自动化搜索比人工设计更容易发现硬件友好结构

人工设计模型可能依赖经验和直觉。  
NAS 可以在巨大搜索空间中发现：

- 人不容易想到的结构；
- 对特定硬件特别友好的结构；
- 在质量和效率之间更优的折中结构。

---

#### 4. 超大规模系统需要超大规模搜索方法

H2O-NAS 使用：

- massively parallel；
- single-step RL；
- real-time production traffic；
- simultaneous architecture search and weight training。

这些都是为了适应 hyperscale 环境。

---

### 十二、可以进一步思考的问题

---

#### 1. 为什么“模型略大”会在 TPU pod 上造成很大问题？

因为大规模加速器系统非常依赖：

- 规则并行；
- 内存容量；
- 模型切分；
- batch size；
- 通信带宽；
- 计算单元利用率。

如果模型略大，可能导致：

- 无法放入设备内存；
- 切分方式变差；
- 通信增加；
- 某些核心空闲；
- 训练吞吐下降。

所以“略大”可能造成“显著低效”。

---

#### 2. 为什么 hardware-aware NAS 可能比事后调度更有效？

因为如果模型本身不适合硬件，调度只能缓解，不能根治。

例如：

- 模型结构不规则；
- 算子不支持；
- 内存访问差；
- 并行度低；
- 通信多。

这些问题最好在模型设计阶段解决。

---

#### 3. NAS 的成本会不会很高？

会。  
所以原文强调：

- weight-sharing；
- one-shot；
- massively parallel；
- single-step RL；
- simultaneous search and training。

这些方法都是为了降低搜索成本，提高可扩展性。

---

#### 4. real-time production traffic 有什么好处？

好处是搜索出的模型更贴近真实业务，而不是只在离线数据集上好。

它可以帮助模型适应：

- 真实输入分布；
- 真实延迟要求；
- 真实流量规模；
- 真实硬件状态；
- 真实质量指标。

---

### 十三、这一节的核心逻辑链

```text
ML 模型算力需求不断增长
  ↓
只靠新硬件不够，模型效率同样重要
  ↓
NAS 可以自动设计模型架构
  ↓
传统 NAS 主要优化模型质量
  ↓
H2O-NAS 引入硬件感知
  ↓
搜索空间、搜索目标、搜索算法都考虑加速器效率
  ↓
模型更适合 TPU pod 等超大规模硬件
  ↓
训练更快、能效更高、利用率更高
  ↓
模型质量保持相当或更好
```

---

### 十四、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.2 Software-defined accelerators

1. 核心思想：
   - software-defined infrastructure 的思想可扩展到 accelerators
   - 不只是调度加速器资源
   - 还可以通过软件/算法定义和优化运行在加速器上的模型
   - 例子：
     - H2O-NAS
     - hyperscale hardware optimized neural architecture search

2. 背景：
   - ML 模型需要越来越强的算力
   - 仅靠构建新硬件不够
   - model efficiency 与硬件基础设施同样重要
   - 目标：
     - 充分释放 ML 硬件潜力
     - 提高性能
     - 提高能效
     - 提高利用率

3. NAS 是什么：
   - Neural Architecture Search
   - 自动设计 ML 模型架构
   - 目标：
     - 找到可媲美甚至超过人工设计的模型结构

4. NAS 四个关键维度：

   a. search strategy：
      - one-shot
      - multi-trial
      - one-shot 通常更高效
      - multi-trial 更昂贵但评估更直接

   b. search algorithm：
      - reinforcement learning
      - gradient-based algorithm
      - evolution algorithm

   c. search space：
      - hardware-specialization
      - weight-sharing
      - 搜索空间可以限制或引导模型结构
      - hardware-specialization：
        让搜索空间适配加速器特性
      - weight-sharing：
        降低搜索和训练成本

   d. search objective：
      - reward functions
      - quality signals
      - performance signals
      - 不只优化 accuracy
      - 也优化 latency、throughput、energy、hardware utilization 等

5. H2O-NAS 的核心：
   - 在传统 NAS 基础上引入 hardware-aware
   - 扩展传统 RL-based search algorithm
   - 使用硬件优化的搜索空间
   - 优化 weight-sharing
   - 目标：
     - 找到既高质量又适合硬件的模型

6. 关键例子：
   - 固定训练预算下质量最高的模型
     - 可能略大
     - 无法很好 fit 到 TPU pod
   - 调整模型大小和架构后：
     - 质量损失很小
     - 实际训练速度可能快两倍
   - 结论：
     - 最优模型不是单纯 accuracy 最高
     - 而是 accuracy、hardware fit、training speed、energy 的综合最优

7. H2O-NAS 的方法特点：
   - massively parallel
   - single-step reinforcement learning
   - 同时搜索模型架构和训练模型权重
   - 使用 real-time production traffic
   - 更适合 hyperscale hardware 和 hyperscale data

8. 效果：
   - 在 Google 部署
   - 显著提升性能
   - 显著提升能效
   - 模型精度和质量相当或更好

9. 与前面内容的关系：
   - 7.1.2 TCMalloc：
     - 库层优化
     - 让程序更好使用内存和 TLB
   - 7.1.3 Platform-aware scheduling：
     - 集群调度层优化
     - 把 workload 调度到最合适平台
   - 7.2 H2O-NAS：
     - 加速器/模型设计层优化
     - 让模型本身更适合加速器

10. 核心逻辑：
   ML 算力需求增长
     → 模型效率很重要
     → NAS 自动搜索模型架构
     → H2O-NAS 加入硬件感知
     → 模型更适合 TPU pod 等加速器
     → 训练更快、能效更高、利用率更高
     → 质量保持相当或更好

11. 一句话总结：
   Software-defined accelerators 的关键思想，
   是不只让加速器适应模型，
   也让模型通过自动搜索和软件优化适应加速器。
```

---

### 十五、一句话总结这一节

> 7.2 通过 H2O-NAS 说明：在超大规模 ML 系统中，软件定义加速器不仅意味着调度加速器资源，更意味着用硬件感知的自动模型设计，让模型结构本身适配加速器，从而在性能、能效和模型质量之间取得更优的系统级平衡。


**专栏导航**

- ← 上一篇：[7.1.3 Case study: Platform-aware scheduling](/posts/7-1-3-case-study-platform-aware-scheduling/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.3 Software-defined networks →](/posts/7-3-software-defined-networks/)
