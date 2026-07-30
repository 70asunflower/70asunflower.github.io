---
title: "5.1.4 Cloud and AI implications for data center design"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-23
description: "《The Data Center as a Computer》AI 导读专栏正文：5.1.4 Cloud and AI implications for data center design。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：5.1.4 Cloud and AI implications for data center design。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 5.1.4 Cloud and AI implications for data center design

下面我结合你提供的原文，把 **5.1.4 Cloud and AI implications for data center design** 这一节读深。

这一节非常重要，因为它讲的是：

> 过去 WSC 数据中心设计主要围绕“超大规模同质负载”和“规模经济”。  
> 但今天，Cloud 和 AI/ML 负载改变了数据中心设计的核心权衡：  
> **功率密度、可用性等级、部署模式、地理分布、区域隔离、交付速度** 都发生了变化。

换句话说，这一节是从“传统数据中心设计”过渡到“现代 Cloud/AI 数据中心设计”的关键。

---

### 一、这一节的核心问题：WSC 不再只有一种工作负载

原文开头说：

> Traditionally, the key design philosophy underpinning WSC data center design embraced economies of scale, and targeted designs customized to hyperscale workloads and systems.

传统 WSC 数据中心的设计哲学是：

```text
economies of scale
规模经济
```

并且针对：

```text
hyperscale workloads
超大规模工作负载
```

做定制优化。

---

#### 1. 什么是 economies of scale？

规模经济指的是：

> 规模越大，单位成本越低。

例如：

```text
采购 10,000 台服务器比采购 100 台更便宜；
建设 100 MW 数据中心比建设 10 个 10 MW 小数据中心更便宜；
统一设计、统一运维、统一采购可以降低成本；
自研硬件、自研网络、自研冷却可以压低单位成本。
```

传统超大规模数据中心通常追求：

```text
单一大型园区
高度标准化
高度自动化
大规模部署
长期稳定运行
高利用率
低单位成本
```

---

#### 2. 什么是 hyperscale workloads？

<span data-type="text" style="color: var(--b3-font-color11);">Hyperscale workloads 通常指超大规模互联网服务负载</span>，例如：

```text
搜索
广告
社交网络
视频服务
邮件
对象存储
大规模数据库
内容分发
```

这些负载的特点通常是：

```text
请求量大；
服务长期在线；
延迟敏感；
跨大量服务器分布；
软件层有强容错；
硬件可以定制；
部署规模巨大。
```

传统 WSC 数据中心就是为这类负载优化的。

---

### 二、今天的 WSC 更加多样化：Cloud 和 AI/ML

原文接着说：

> But as discussed in Chapter 3, today’s WSCs show a lot more diversity via Cloud and AI/ML workloads.

今天的数据中心不再只运行传统超大规模互联网服务，还包括：

```text
Cloud workloads
云工作负载

AI/ML workloads
人工智能和机器学习工作负载
```

这两类负载和传统 hyperscale 负载有很大不同。

可以粗略分成三类：

```text
1. Hyperscale workloads
   传统超大规模互联网服务

2. Cloud workloads
   多租户云服务、企业应用、数据库、开发平台

3. AI/ML workloads
   模型训练、推理、向量检索、GPU/TPU 加速计算
```

这三类负载对数据中心的要求不同。

---

### 三、AI/ML 对数据中心的第一个冲击：功率密度大幅上升

原文说：

> ML workloads in particular have posed interesting new challenges for data center design by greatly increasing power density.

AI/ML 负载给数据中心设计带来的第一个大挑战是：

```text
power density
功率密度
```

显著上升。

---

#### 1. 什么是功率密度？

功率密度通常指：

```text
每个机柜消耗多少功率
kW/rack
```

或者：

```text
每平方米消耗多少功率
kW/m²
```

在数据中心里，常用：

```text
kW per rack
每机柜千瓦数
```

---

#### 2. 传统服务器机柜功率密度

原文说：

```text
10–30 kW/racks for traditional servers
```

也就是传统服务器机柜通常在：

```text
10 kW/rack 到 30 kW/rack
```

例如：

```text
普通计算服务器机柜：10 kW
存储服务器机柜：15 kW
高密度计算机柜：25 kW
```

这类机柜通常可以用风冷解决。

---

#### 3. AI 加速器机柜功率密度

原文说：

```text
accelerator systems can range from 50–200 kW/rack, trending even higher in future generations.
```

AI 加速器机柜可能达到：

```text
50 kW/rack
100 kW/rack
150 kW/rack
200 kW/rack
甚至更高
```

这里的 accelerator 包括：

```text
GPU
TPU
NPU
ASIC
其他 AI 加速芯片
```

例如一个装满高端 GPU 的机柜，功耗可能远超传统 CPU 机柜。

---

### 四、功率密度上升为什么是数据中心设计的大问题？

因为数据中心设计本质上是：

```text
供电 + 散热
```

当每个机柜功率从 15 kW 上升到 100 kW 或 200 kW 时，供电和冷却系统都要重新设计。

---

#### 1. 对供电系统的影响

高功率密度意味着每个机柜需要更大电流和更强配电能力。

例如：

```text
15 kW/rack
100 kW/rack
```

后者需要的电力容量大约是前者的：

```text
100 / 15 ≈ 6.7 倍
```

这会影响：

```text
变压器容量
UPS 容量
发电机容量
配电柜容量
母线槽容量
PDU 容量
电缆截面积
断路器规格
机柜电源设计
电源转换效率
```

---

#### 2. 对冷却系统的影响

功率几乎最终都变成热。

如果一个机柜消耗：

```text
100 kW
```

它大约会产生：

```text
100 kW 热量
```

这些热必须被持续带走。

传统风冷在低密度下有效，但在高密度下可能不足。

因此 AI 数据中心常需要：

```text
液冷
direct-to-chip liquid cooling
rear door heat exchanger
immersion cooling
更高温度供水
更大流量冷却水
更复杂管路
漏液检测
冷却分配单元 CDU
```

---

#### 3. 对建筑布局的影响

高功率密度还影响：

```text
机柜数量
机房面积
楼板承重
管路布置
气流组织
维护通道
消防设计
安全距离
```

例如同样 10 MW IT 负载：

```text
如果每机柜 20 kW：
  10,000 kW / 20 kW = 500 个机柜

如果每机柜 100 kW：
  10,000 kW / 100 kW = 100 个机柜
```

机柜数量减少，但每个机柜的供电和冷却难度大幅上升。

---

### 五、如何理解原文中的“功率密度分布曲线右移”？

原文提到 Figure 5.5：

> The curve on the left shows a mix of traditional compute and storage systems, while the curve on the right shows the impact of introducing machine learning racks. The right shift in the curves indicates the increased power densities of accelerator systems.

这里可以用统计分布理解。

---

#### 1. 传统数据中心的功率密度分布

传统数据中心里，机柜功率密度可能集中在：

```text
10 kW
15 kW
20 kW
25 kW
```

分布曲线偏左。

```text
低功率密度区域
```

---

#### 2. 引入 AI 机柜后的功率密度分布

加入 AI 机柜后，出现高功率密度：

```text
50 kW
100 kW
150 kW
200 kW
```

分布曲线向右移动。

```text
高功率密度区域
```

---

#### 3. “右移”的工程含义

右移意味着：

```text
数据中心必须支持更高功率密度的机柜。
```

这会影响：

```text
电力设计
冷却设计
机柜设计
机房分区
运维方式
未来扩展能力
```

---

### 六、什么是“bimodality”？为什么它带来新设计权衡？

原文说：

> The bimodality of lower-density traditional servers and higher-power-density for emerging accelerators motivate new design tradeoffs to support this wider range.

这里的关键词是：

```text
bimodality
双峰性
```

---

#### 1. 双峰是什么意思？

过去数据中心机柜功率密度可能比较单一：

```text
大多数机柜都在 10–30 kW
```

现在则可能同时存在两类：

```text
低密度传统服务器：
  10–30 kW/rack

高密度 AI 加速器：
  50–200 kW/rack
```

于是功率密度分布出现两个峰：

```text
一个峰在低密度区
一个峰在高密度区
```

这就是 bimodal distribution，双峰分布。

---

#### 2. 为什么双峰带来设计困难？

因为低密度和高密度机柜对基础设施要求完全不同。

例如：

|维度|低密度传统服务器|高密度 AI 加速器|
| ------| ------------------| ----------------------------|
|功率|10–30 kW/rack|50–200 kW/rack|
|冷却|风冷通常足够|常需要液冷|
|供电|常规 PDU|高电流/高密度配电|
|气流|冷热通道|可能需要封闭或液冷回路|
|维护|传统运维|液冷、漏液、快接头等新要求|
|部署|通用机房|专用或改造机房|
|成本|相对低|高|

如果同一个数据中心既要支持传统服务器，又要支持 AI 加速器，就必须做新的设计权衡。

---

#### 3. 可能的架构选择

面对双峰负载，数据中心可能有几种设计方式。

---

##### 方案一：分区设计

把低密度和高密度设备放在不同区域：

```text
Hall A：传统服务器，风冷
Hall B：AI 加速器，液冷
```

优点：

```text
设计简单；
冷却和供电更匹配；
运维边界清晰。
```

缺点：

```text
灵活性较低；
未来转换用途可能有成本。
```

---

##### 方案二：灵活机房

设计可支持多种功率密度的通用机房。

例如：

```text
预留液冷管路；
支持高功率母线；
机柜位置可按功率分配；
冷却容量模块化。
```

优点：

```text
灵活性高；
适应未来变化。
```

缺点：

```text
初期成本可能更高；
设计复杂。
```

---

##### 方案三：模块化 Pod

把供电和冷却封装成模块化单元：

```text
Power Pod
Cooling Pod
AI Pod
```

优点：

```text
部署快；
扩展灵活；
适合增量建设。
```

缺点：

```text
需要标准化接口和运维流程。
```

---

### 七、AI/ML 对数据中心的第二个冲击：可用性和 uptime 要求不同

原文说：

> ML workloads also have diverging availability and uptime requirements relative to cloud and hyperscale workloads.

也就是说，ML 负载对可用性和持续运行时间的要求，和传统云或超大规模负载不同。

---

#### 1. ML 训练负载通常是 bulk-synchronous

原文说：

> these workloads are bulk-synchronous and more throughput oriented.

bulk-synchronous 指的是：

> <span data-type="text" style="color: var(--b3-font-color11);">计算过程分成若干阶段，每个阶段结束后需要同步。</span>

例如典型的分布式训练：

```text
每个 worker 计算梯度
  -> all-reduce 同步梯度
  -> 更新模型参数
  -> 进入下一步
```

这类负载更关注：

```text
吞吐量
训练完成时间
GPU/TPU 利用率
网络同步效率
```

而不是像 Web 服务那样关注每个请求的即时响应。

---

#### 2. ML 训练可以通过 checkpoint-restart 容错

原文说：

> have mechanisms for checkpoint-restarting and customer SLOs that allow them to be more tolerant to sporadic infrastructure downtime.

<span data-type="text" style="color: var(--b3-font-color11);">ML 训练任务通常会定期保存 checkpoint。</span>

例如：

```text
每 30 分钟保存一次模型状态
每 1000 步保存一次参数和优化器状态
```

如果某个节点故障，任务可以：

```text
从最近的 checkpoint 恢复
重新调度失败节点
继续训练
```

因此，短时间基础设施停机不一定导致训练任务彻底失败。

---

#### 3. 这<span data-type="text" style="color: var(--b3-font-color11);">意味着 ML 训练可以接受更低 Tier</span>？

原文说：

> compared to enterprise workloads on cloud that often need Tier-3 or higher data center requirements, some ML workloads, especially training workloads, can potentially use Tier-1-like data centers.

这是一个很重要的观点。

传统企业云负载通常需要：

```text
Tier III 或更高
```

因为它们可能不能容忍计划维护停机。

但某些 ML 训练负载可能可以接受：

```text
Tier I-like
```

也就是更低冗余等级的数据中心。

原因是：

```text
训练任务可以 checkpoint；
可以重启；
可以重新调度；
对偶发停机有一定容忍；
更关注总训练成本和吞吐，而不是连续 uptime。
```

---

#### 4. 但要注意：不是所有 ML 负载都能接受低 Tier

这里需要补充一个关键区分。

ML 负载至少可以分成：

```text
训练 training
推理 inference
```

---

##### 训练负载

训练负载通常：

```text
批处理式；
可 checkpoint；
可重启；
吞吐导向；
对偶发停机有一定容忍。
```

因此可能接受较低设施 Tier。

---

##### 推理负载

推理负载通常：

```text
在线服务；
延迟敏感；
需要持续可用；
面向终端用户或客户 API。
```

例如：

```text
聊天机器人
搜索排序
推荐系统
广告排序
实时翻译
图像识别 API
```

<span data-type="text" style="color: var(--b3-font-color11);">这些服务通常需要高可用，不能随便停机。</span>

因此推理负载往往更接近云负载，需要：

```text
高可用设计
多副本
多可用区
负载均衡
故障转移
较高 Tier 或软件容错
```

---

### 八、Tier 成本差异带来的新权衡

原文说：

> As discussed earlier, the range of costs across these tiers is fairly significant, leading to new tradeoffs in data center design.

不同 Tier 的成本差异很大。

例如：

```text
Tier I：最简单，成本最低
Tier III：可并发维护，成本更高
Tier IV：容错级，成本最高
```

如果某些 ML 训练负载可以接受较低 Tier，那么就可以：

```text
用更低成本建设训练数据中心
```

这会带来新的设计选择：

```text
是花更多钱建 Tier III/IV？
还是用软件容错和 checkpoint 来接受偶发停机？
```

---

#### 1. 传统思路

传统企业系统通常依赖设施高可用：

```text
高 Tier 数据中心
冗余电力
冗余冷却
不停机维护
```

---

#### 2. 超大规模/AI 训练思路

超大规模系统更常依赖软件容错：

```text
checkpoint
restart
replication
rescheduling
failure detection
automatic recovery
```

<span data-type="text" style="color: var(--b3-font-color11);">如果软件能处理故障，那么设施等级可以适当降低。</span>

这就是：

```text
用软件可靠性替代部分基础设施可靠性
```

---

### 九、Cloud 数据中心部署带来的不同考虑

原文说：

> Cloud data center deployments bring different considerations.

Cloud 负载和 ML 训练负载不同，它更强调：

```text
地理多样性
区域隔离
增量部署
按需付费
部署速度
```

---

### 十、Cloud 的地理多样性

原文说：

> They introduce more geodiversity, matched to the wide diversity of customer requirements.

云服务面向大量不同客户，客户需求差异很大。

例如：

```text
有些客户需要低延迟；
有些客户需要数据本地化；
有些客户需要灾备；
有些客户需要合规；
有些客户需要靠近特定区域用户；
有些客户需要多区域高可用。
```

因此云厂商需要在多个地理区域部署：

```text
regions
zones
availability zones
edge locations
```

---

#### 1. 为什么地理多样性重要？

##### 低延迟

用户离数据中心越近，网络延迟通常越低。

例如：

```text
欧洲用户访问欧洲 region
亚洲用户访问亚洲 region
```

比跨洲访问快得多。

---

##### 数据合规

很多国家或地区要求数据存储在本地。

例如：

```text
用户数据不能出境；
金融数据必须本地存储；
医疗数据有隐私要求；
政府数据有主权要求。
```

因此云厂商必须在多个地区建设数据中心。

---

##### 灾难恢复

如果一个 region 发生重大故障，另一个 region 可以接管。

例如：

```text
Region A 故障
流量切换到 Region B
```

这提高了整体可用性。

---

### 十一、Cloud 对 regional and zonal isolation 的更高要求

原文说：

> also impose more stringent requirements on regional and zonal isolation.

这里涉及云架构中非常重要的概念：

```text
region
zone / availability zone
```

---

#### 1. Region

Region 通常是一个地理区域，例如：

```text
us-central1
europe-west1
asia-east1
```

一个 region 内可能有多个 zone。

---

#### 2. Zone

Zone 是 region 内相对独立的故障域。

例如：

```text
Zone A
Zone B
Zone C
```

每个 zone 通常有独立的：

```text
电力
冷却
网络
物理建筑
```

这样即使一个 zone 出现故障，其他 zone 仍可运行。

---

#### 3. 为什么 zonal isolation 很重要？

云服务是多租户的。

客户可能把关键业务放在云上：

```text
数据库
企业应用
电商平台
金融系统
SaaS 服务
```

如果多个 zone 共享关键基础设施，一个故障可能同时影响多个 zone。

这会破坏云的高可用承诺。

因此云厂商必须保证：

```text
zone 之间故障隔离
电力独立
冷却独立
网络路径冗余
物理距离适当
运维边界清晰
```

---

### 十二、Cloud 偏好 “pay as you go” 和增量部署

原文说：

> relative to the large-scale deployments that hyperscale and ML workloads prefer, cloud deployments prefer a “pay as you go” model especially for growth in new locations where data center capacity is more incrementally deployed in smaller chunks.

这里对比了两种部署模式。

---

#### 1. Hyperscale / ML 训练偏好大规模部署

超大规模负载和大型 AI 训练集群通常偏好：

```text
一次性大规模建设
大规模服务器部署
高度定制化
长期稳定运行
追求单位成本最低
```

例如：

```text
建设一个 100 MW AI 训练园区
部署数万张 GPU/TPU
```

<span data-type="text" style="color: var(--b3-font-color11);">这类部署追求：</span>

```text
pure cost efficiency at scale
规模成本效率
```

---

#### 2. Cloud 偏好增量部署

云服务面对不确定的客户需求。

云厂商不知道：

```text
某个新区域未来会有多少客户；
客户增长有多快；
哪些服务类型会增长；
哪些行业会进入；
竞争环境如何变化。
```

<span data-type="text" style="color: var(--b3-font-color11);">因此云厂商更倾向于：</span>

```text
incremental deployment
增量部署
```

<span data-type="text" style="color: var(--b3-font-color11);">也就是：</span>

```text
先部署一小块容量；
根据需求增长再扩展；
避免一次性过度建设。
```

---

#### 3. “pay as you go” 的含义

“pay as you go” 不仅是客户付费模式，也影响数据中心建设策略。

对客户来说：

```text
用多少资源付多少钱
```

对云厂商来说：

```text
容量投资要尽量匹配需求增长
避免大量闲置容量
降低资本风险
```

因此云数据中心建设更重视：

```text
模块化
标准化
可复制
快速交付
增量扩展
```

---

### 十三、Cloud 更重视部署速度

原文说：

> focus in on velocity of deployment over pure cost efficiency at scale.

也就是说，<span data-type="text" style="color: var(--b3-font-color11);">云部署有时更看重：</span>

```text
velocity of deployment
部署速度
```

而不是单纯追求：

```text
pure cost efficiency at scale
极致规模成本效率
```

---

#### 1. 为什么部署速度重要？

云市场竞争激烈。

如果某个地区有客户需求，但云厂商需要三年才能建好数据中心，客户可能选择其他云。

<span data-type="text" style="color: var(--b3-font-color11);">因此云厂商需要快速进入新区域：</span>

```text
更快拿地
更快建设
更快上线
更快交付容量
```

---

#### 2. 如何提升部署速度？

常见方法包括：

```text
预制模块化数据中心
标准化电力模块
标准化冷却模块
标准化网络架构
自动化部署
自动化测试
快速验收流程
供应链预制
可复制建筑设计
```

---

#### 3. 速度和成本的权衡

极致规模成本效率可能需要：

```text
高度定制
长周期建设
大规模一次性投入
```

而快速部署可能需要：

```text
标准化模块
更高初始单位成本
更小建设规模
更快交付
```

云厂商必须权衡：

```text
建设成本
交付速度
容量风险
客户需求
竞争压力
```

---

### 十四、Hyperscale、Cloud、AI/ML 的设计差异对比

可以用下面这张表理解这一节。

|维度|Hyperscale|Cloud|AI/ML 训练|AI/ML 推理|
| ------------| ------------------------| --------------------------| --------------------------| ------------------|
|典型负载|搜索、广告、视频、社交|多租户云服务、企业应用|大模型训练、批量训练|在线模型服务|
|部署规模|很大|多区域、多可用区|很大，尤其 GPU/TPU 集群|可大可小|
|功率密度|中等到高|中等到高|很高|中到高|
|冷却方式|风冷/液冷混合|风冷/液冷混合|常需液冷|风冷或液冷|
|可用性要求|高|很高|可接受一定停机|高|
|容错方式|软件分布式容错|多可用区、多副本|checkpoint/restart|多副本、负载均衡|
|Tier 倾向|根据负载选择|Tier III 或更高|某些可用 Tier I-like|接近云负载|
|建设策略|大规模、定制化|增量、模块化|大规模高密度|灵活部署|
|关键目标|规模成本效率|地理覆盖、隔离、交付速度|吞吐、训练效率、功率密度|延迟、可用性|

---

### 十五、这一节对后续 power 和 cooling 章节的铺垫

原文最后说：

> We will discuss how these considerations change the design tradeoffs for WSC data centers below as we deep dive into the key elements of the data center – the power subsystems and the cooling subsystems.

这句话是过渡。

它告诉我们，后面的章节会重点讨论：

```text
power subsystems
供电子系统

cooling subsystems
冷却子系统
```

而 5.1.4 节已经给出了为什么这些子系统需要重新设计。

---

#### 1. Power 子系统会受什么影响？

AI 高功率密度会要求：

```text
更高机柜功率
更高配电容量
更高电压等级
更高效率电源
更强母线系统
更灵活冗余策略
更大发电机和 UPS 容量
```

Cloud 增量部署会要求：

```text
模块化电力单元
分阶段建设
按需扩容
标准化配电设计
```

---

#### 2. Cooling 子系统会受什么影响？

AI 高功率密度会要求：

```text
液冷
更高冷却能力
更高供水温度
更大流量
更复杂管路
漏液检测
CDU 冷却分配单元
维护流程变化
```

Cloud 部署会要求：

```text
模块化冷却
快速部署
灵活适配不同机柜密度
分阶段扩容
```

---

### 十六、这一节的深层思想：数据中心设计从“单一最优”变成“多目标权衡”

传统 WSC 设计可能追求：

```text
单一超大规模负载下的最低单位成本
```

但现代 WSC 必须同时考虑：

```text
功率密度
冷却能力
可用性
地理分布
区域隔离
部署速度
资本效率
客户需求
负载类型
未来扩展
可持续性
```

因此数据中心设计不再是简单的：

```text
建一个尽可能大的数据中心
```

而是：

```text
根据负载特征选择合适的功率、冷却、Tier、部署模式和地理布局。
```

---

### 十七、一个直观例子：同一个 10 MW 机房如何变化？

假设一个机房有：

```text
10 MW IT capacity
```

---

#### 1. 传统服务器场景

如果每机柜：

```text
20 kW
```

那么可以放：

```text
10,000 kW / 20 kW = 500 racks
```

冷却可能主要用：

```text
风冷
冷热通道
精密空调
```

---

#### 2. AI 加速器场景

如果每机柜：

```text
100 kW
```

那么只能放：

```text
10,000 kW / 100 kW = 100 racks
```

但每个机柜的计算能力可能远高于传统机柜。

冷却可能需要：

```text
液冷
direct-to-chip
rear-door heat exchanger
immersion
```

供电可能需要：

```text
更高电流
更高电压
更粗电缆
更强 PDU
```

---

#### 3. 设计含义

同样的 10 MW：

```text
传统场景：500 个低密度机柜
AI 场景：100 个高密度机柜
```

机房面积可能没有用满，但电力和冷却已经到上限。

这说明：

> 现代 AI 数据中心的限制越来越不是“有多少地板面积”，而是“能供多少电、能散多少热”。

---

### 十八、这一节的关键概念总结

---

#### 1. 传统 WSC 设计哲学

```text
规模经济
面向超大规模负载
高度定制
追求单位成本最低
```

---

#### 2. AI/ML 带来功率密度上升

```text
传统服务器：10–30 kW/rack
AI 加速器：50–200 kW/rack，未来更高
```

导致：

```text
供电压力上升
冷却压力上升
设计双峰化
```

---

#### 3. AI/ML 训练负载可用性要求不同

```text
bulk-synchronous
throughput-oriented
checkpoint-restart
可容忍偶发停机
```

因此某些训练负载可以使用较低 Tier 数据中心。

---

#### 4. Cloud 负载强调地理多样性和区域隔离

```text
geodiversity
regional isolation
zonal isolation
```

原因是：

```text
低延迟
合规
灾备
多租户高可用
```

---

#### 5. Cloud 偏好增量部署和部署速度

```text
pay as you go
smaller chunks
velocity of deployment
```

而不是单纯追求极致规模成本效率。

---

### 十九、这一节可以整理成的精简笔记

```text
5.1.4 Cloud and AI implications for data center design

1. 传统 WSC 设计哲学：
   - economies of scale
   - 面向 hyperscale workloads
   - 定制化、大规模、低成本

2. 现代 WSC 更多样：
   - Cloud workloads
   - AI/ML workloads

3. AI/ML 对数据中心的影响一：功率密度上升
   - 传统服务器：10–30 kW/rack
   - 加速器系统：50–200 kW/rack，未来更高
   - 功率密度分布曲线右移
   - 出现低密度传统服务器和高密度加速器的双峰分布
   - 需要新的供电和冷却设计权衡

4. AI/ML 对数据中心的影响二：可用性要求不同
   - ML 训练通常是 bulk-synchronous
   - 更关注吞吐而非单请求延迟
   - 可通过 checkpoint-restart 恢复
   - 对偶发基础设施停机更容忍
   - 企业云负载通常需要 Tier III 或更高
   - 某些 ML 训练负载可能使用 Tier I-like 数据中心
   - Tier 成本差异大，因此产生新设计权衡

5. Cloud 部署的不同考虑：
   - 更多地理多样性
   - 匹配客户低延迟、合规、灾备等需求
   - 更严格的 regional 和 zonal isolation
   - 相比 hyperscale/ML 的大规模部署，cloud 更偏好 pay-as-you-go
   - 新地点常增量部署小块容量
   - 更重视部署速度，而非单纯规模成本效率

6. 后续影响：
   - 这些变化会改变 power subsystems 和 cooling subsystems 的设计权衡
```

---

### 二十、如果考试或讨论中要回答这一节，可以这样说

你可以这样概括：

> 5.1.4 节讨论了 Cloud 和 AI/ML 负载如何改变 WSC 数据中心设计。传统 WSC 设计强调规模经济，并针对超大规模负载进行定制优化。但今天的数据中心需要支持更多样的工作负载。首先，AI/ML 负载显著提高了机柜功率密度。传统服务器机柜通常为 10–30 kW，而 AI 加速器机柜可能达到 50–200 kW，未来还会更高。这使得功率密度分布曲线右移，并形成本地传统低密度服务器与高密度加速器并存的双峰特征，从而要求供电和冷却系统支持更宽的功率范围。其次，ML 训练负载通常是批量同步、吞吐导向的，并且可以通过 checkpoint-restart 恢复，因此相比企业云负载，它们对偶发基础设施停机更有容忍度。某些训练负载甚至可以使用类似 Tier I 的低冗余数据中心，从而在成本和可靠性之间做出新的权衡。Cloud 部署则带来不同考虑：它需要更多地理分布以满足延迟、合规和灾备需求，同时要求更严格的区域和可用区隔离。与超大规模和 ML 训练偏好大规模部署不同，Cloud 更偏好按需增长和增量部署，尤其在新地点更重视部署速度而非单纯的规模成本效率。因此，现代 WSC 数据中心设计不再是单一追求规模经济，而是要在功率密度、可用性、地理分布、隔离性、部署速度和成本之间进行综合权衡。

---

### 二十一、最后给你一个形象类比

可以把传统 WSC 数据中心想象成：

```text
一个超大型集装箱港口
```

它追求：

```text
超大规模
统一标准
低成本
高吞吐
```

而现代 Cloud/AI 数据中心更像：

```text
既要处理普通集装箱，
又要处理超重超大货物，
还要在全球多个城市快速建临时货运站。
```

其中：

```text
传统服务器：
  标准集装箱

AI 机柜：
  超重高耗电集装箱，需要特殊吊机和散热通道

Cloud：
  需要在多个地区快速部署小型货运站，并保证彼此隔离

ML 训练：
  可以接受某个站点短暂停工，只要任务能从检查点继续

企业云：
  客户要求不能停工，因此需要更高可靠设施
```

这一节的核心提醒是：

> 现代数据中心设计不再只是“建得更大更便宜”，而是要根据 Cloud、AI/ML、企业负载的不同特征，重新设计电力、冷却、可用性、地理分布和交付速度之间的平衡。


**专栏导航**

- ← 上一篇：[5.1.3 Data center taxonomy: Tiers](/posts/5-1-3-data-center-taxonomy-tiers/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.1 WSC building blocks and design considerations →](/posts/6-1-wsc-building-blocks-and-design-considerations/)
