---
title: "7.4 Software-defined storage 和 7.4.1 Storage workload diversity"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-29
description: "《The Data Center as a Computer》AI 导读专栏正文：7.4 Software-defined storage 和 7.4.1 Storage workload diversity。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.4 Software-defined storage 和 7.4.1 Storage workload diversity。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.4 Software-defined storage 和 7.4.1 Storage workload diversity

下面把 **7.4 Software-defined storage** 和 **7.4.1 Storage workload diversity** 放在一起深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这一节把 software-defined infrastructure 的思想扩展到存储层：

> 不再为每类工作负载单独部署一套存储系统，而是通过软件把各种存储设备、各种服务类型、各种工作负载统一到一个全球可调度、可互换、可优化的存储池中。

---

### 7.4 Software-defined storage 深入理解

#### 一、核心思想：让存储资源具有 fungibility

原文说：

> Google optimizes storage efficiency via software-defined storage providing fungibility across various data centers and storage devices.

关键词是：

> fungibility，可互换性。

fungible 的意思是：

> 资源之间可以互相替代、统一使用。

例如货币是 fungible 的：  
一张 100 元和另一张 100 元可以互换。

在存储中，fungibility 意味着：

> 不同数据中心、不同设备类型、不同工作负载之间的存储资源，可以通过软件统一调度和复用。

也就是说：

```text
不是：
归档系统用一批 HDD
数据库系统用一批 SSD
对象存储用另一批设备
彼此孤立

而是：
所有存储资源组成统一池
由软件决定谁用什么设备、什么容量、什么 IOPS、什么延迟等级
```

---

#### 二、传统存储系统的问题

原文说：

> Conventional storage systems are often deployed specifically for particular workload types.

传统存储系统通常为特定负载专门部署。

例如：

|工作负载|传统部署方式|
| ----------| --------------------------------------|
|数据库|高端 SSD，追求低延迟和高 IOPS|
|归档存储|最大容量 HDD，追求最低 cost per byte|
|视频存储|大容量磁盘，偏重吞吐|
|日志分析|便宜磁盘，偏重容量|
|在线服务|高性能磁盘或 SSD|

这种方式的问题是：

> 每个系统都为自身工作负载独立优化，但整体数据中心利用率不一定高。

---

##### 例子 1：数据库存储

原文说：

> a storage system might prioritize performance by placing database workloads on high-end SSD devices.

数据库通常需要：

- 低延迟；
- 高 IOPS；
- 随机读写；
- 高可靠；
- 稳定吞吐。

因此会选高端 SSD。

但 SSD 的 cost per byte 很高。  
如果数据库容量需求不大，但 IOPS 需求高，那么 SSD 的容量可能没有充分利用。

---

##### 例子 2：归档存储

原文说：

> an archival cloud service might select the largest-capacity HDD drives available leaving IOPS unused.

归档存储通常：

- 数据很少访问；
- 容量巨大；
- 对延迟不敏感；
- 对 IOPS 要求很低。

因此会选最大容量 HDD，追求最低每字节成本。

但这会导致：

> HDD 的 IOPS 能力大量闲置。

也就是说：

```text
容量用满了
IOPS 没用满
```

---

#### 三、为什么 WSC 需要软件定义存储？

原文说：

> Given the extensive range of WSC services and workloads discussed in Chapter 3, maximizing the efficiency of the deployed data center footprint requires storage resources to be as fungible as possible.

WSC 中有大量不同服务和工作负载：

- 搜索；
- Gmail；
- YouTube；
- Photos；
- Drive；
- BigQuery；
- Spanner；
- Borg 任务；
- ML 训练；
- 日志分析；
- 数据复制；
- 备份；
- 归档。

这些负载差异巨大：

- 有些热，有些冷；
- 有些延迟敏感，有些延迟容忍；
- 有些容量大但 IOPS 低；
- 有些容量小但 IOPS 高；
- 有些需要强一致；
- 有些只需要最终一致；
- 有些需要全球分布；
- 有些只需要区域存储。

如果每类负载都单独部署存储系统，会导致：

- 设备碎片化；
- 利用率低；
- 容量和 IOPS 不匹配；
- 运维复杂；
- 成本上升；
- 难以全球调度。

因此需要：

> software-defined storage。

---

### 四、Google 的统一全局分层存储系统

原文说：

> At Google, we employ a unified global layered storage system.

也就是说：

> Google 使用统一的、全球范围的、分层存储系统。

这里有三个关键词。

---

#### 1. unified，统一

不是每个服务自己搞一套底层存储，而是建立在统一存储基础之上。

原文说：

> various storage service types, such as block, database, object, key-value, and file, are all built upon a single, modular distributed storage system, Colossus.

也就是说：

- block storage；
- database storage；
- object storage；
- key-value storage；
- file storage；

这些不同存储服务都构建在同一个分布式存储系统上：

> Colossus。

---

#### 2. global，全球

存储资源不只属于某一台机器或某一个集群，而是可以跨数据中心、跨地区、跨洲进行调度。

原文后面举例：

> storage for low-IOPS archival workloads can be spread across continents or even world-wide.

低 IOPS 归档负载可以分布到全球，只要哪里有：

- 空闲容量；
- 未用 IOPS；
- 合适成本；
- 合适可用性要求。

---

#### 3. layered，分层

不同工作负载对性能、容量、延迟、成本的要求不同。  
因此存储系统需要分层：

```text
高性能层：SSD / 低延迟设备
容量层：HDD
归档层：大容量 HDD / 更低成本介质
跨地域层：远程复制 / 冷数据分布
服务层：block / object / file / key-value / database
```

软件负责决定：

- 数据放在哪一层；
- 哪些数据热；
- 哪些数据冷；
- 哪些 IOPS 需要优先保障；
- 哪些任务可以后台运行；
- 哪些服务需要 bounded latency。

---

### 五、Colossus 的作用

原文提到：

> Colossus.

可以把它理解为 Google 的底层分布式存储基座。

它上面可以承载多种存储服务：

```text
        应用 / 服务
            ↓
block / object / file / key-value / database
            ↓
        Colossus
            ↓
HDD / SSD / 其他存储设备 / 多数据中心
```

这种结构的好处是：

- 底层设备统一抽象；
- 上层服务共享存储基础设施；
- 数据放置全局优化；
- 故障恢复统一处理；
- 复制、加密、压缩、计费统一；
- 设备可互换；
- 工作负载可混合部署。

---

### 7.4.1 Storage workload diversity 深入理解

这一节重点讲：

> 存储工作负载的多样性，尤其是 bytes 和 IOPS 之间的比例差异。

这是理解 software-defined storage 的关键。

---

#### 一、存储设备的两个核心资源

原文说：

> Storage devices combine a fixed amount of storage, bytes, with a fixed amount of access to that storage, limiting both the number I/O operations per second and the total data transfer bandwidth.

也就是说，存储设备主要有两类资源：

1. bytes，容量；
2. I/O capability，访问能力。

访问能力又包括：

- IOPS，每秒 I/O 操作数；
- bandwidth，数据传输带宽。

可以简化为：

```text
存储设备 = 容量 bytes + 访问能力 IOPS/bandwidth
```

---

#### 二、不同工作负载需要不同的 bytes / IOPS 比例

原文说：

> Each workload requires a different ratio of bytes vs IOPS.

这是核心。

有些工作负载需要很多容量，但很少访问。  
有些工作负载容量不大，但访问极频繁。

---

##### 1. 冷归档负载

例如：

- 用户旧照片；
- 旧视频；
- 备份；
- 合规归档；
- 历史日志；
- 很少访问的数据。

特点：

```text
bytes 很大
IOPS 很低
```

例如：

```text
1 PB 归档数据
每天只访问几千次
```

这种负载最适合：

- 大容量 HDD；
- 低成本介质；
- 高容量密度；
- 低 cost per byte。

但它会浪费 IOPS。

---

##### 2. 数据库负载

例如：

- 交易数据库；
- 元数据服务；
- 用户账户系统；
- 订单系统；
- 索引服务。

特点：

```text
bytes 可能不大
IOPS 很高
延迟敏感
```

这种负载最适合：

- SSD；
- 低延迟设备；
- 高随机 IOPS；
- 稳定 QoS。

但它可能浪费容量，因为 SSD 每字节成本高。

---

##### 3. 视频服务负载

例如：

- YouTube 视频；
- 大文件下载；
- 流媒体播放。

特点：

```text
bytes 很大
bandwidth 高
IOPS 不一定很高
延迟要求中等
```

这种负载更关心：

- 吞吐；
- 容量；
- CDN；
- 缓存；
- 顺序读。

---

##### 4. 数据分析负载

例如：

- BigQuery；
- MapReduce；
- Spark；
- 日志分析；
- 数据仓库扫描。

特点：

```text
bytes 很大
顺序读多
IOPS 可能中等
延迟容忍
```

这种负载可以在后台使用空闲 IOPS。

---

#### 三、简单静态匹配为什么不够？

原文说：

> The simple way to match disk sizes to workloads deploys large HDDs for cold workloads and small HDDs, or SSDs, for hot workloads.

简单方法是：

```text
冷负载 → 大 HDD
热负载 → 小 HDD 或 SSD
```

这看起来合理，但原文指出：

> Even then, it’s unlikely that the workload perfectly matches available devices, leaving at least one of the device’s capabilities underutilized.

也就是说：

> 即使这样匹配，工作负载也很难完美匹配设备，总会浪费至少一种资源。

---

##### 情况 1：容量用满，IOPS 闲置

归档负载放在大容量 HDD 上：

```text
容量：100% 使用
IOPS：10% 使用
```

浪费 IOPS。

---

##### 情况 2：IOPS 用满，容量闲置

数据库负载放在 SSD 上：

```text
IOPS：100% 使用
容量：30% 使用
```

浪费容量。

---

##### 情况 3：今天合适，一年后不合适

原文说：

> applications change over time, so it’s unlikely that the best fitting device today will still be the right choice a year from now.

应用访问模式会变。

例如：

- 某个服务刚上线时很热；
- 一年后数据变冷；
- 某个归档系统突然被分析任务频繁访问；
- 某个 ML 训练需要读取历史数据；
- 某个老照片功能突然流行。

如果存储设备是静态绑定的，就很难适应变化。

---

### 四、软件定义存储如何解决？

原文说：

> With software-defined storage, we can combine these workloads together onto shared devices and right-size the overall fleet mix for the overall ratio of IOPS/TB.

也就是说：

> 软件定义存储可以把不同工作负载混合到共享设备上，并根据整体 IOPS/TB 比例来优化整个设备组合。

这里有两个关键思想。

---

#### 1. 混合工作负载到共享设备

传统方式：

```text
归档负载 → 专用归档 HDD 池
数据库负载 → 专用 SSD 池
分析负载 → 专用分析存储池
```

软件定义存储：

```text
所有负载进入统一存储系统
    ↓
软件按 QoS、延迟等级、IOPS 需求、容量需求混合放置
```

例如：

- 低 IOPS 归档数据填充 HDD 容量；
- 高 IOPS 数据库数据使用 SSD；
- 延迟容忍分析任务使用空闲 IOPS；
- 延迟敏感服务获得优先 IOPS。

---

#### 2. 优化整体设备组合，而不是单个应用

原文说：

> It’s much easier to optimize capacity for large pools than for individual applications.

大池比单个应用更容易优化。

这是因为统计复用效应。

单个应用可能非常极端：

```text
应用 A：极冷，容量大，IOPS 极低
应用 B：极热，容量小，IOPS 极高
```

如果单独部署，都很难匹配设备。

但如果合并成一个大池：

```text
总体容量需求 + 总体 IOPS 需求
    ↓
选择整体 IOPS/TB 最合适的设备组合
```

这样更容易达到高利用率。

---

### 五、全球范围填充设备

原文说：

> storage for low-IOPS archival workloads can be spread across continents or even world-wide to fill devices that are close to their IOPS limits but have free bytes.

也就是说：

> 低 IOPS 归档负载可以跨洲甚至全球分布，用来填充那些 IOPS 接近上限但还有空闲容量的设备。

这很关键。

假设某个数据中心的设备：

```text
IOPS：95% 使用
容量：60% 使用
```

那么它还有大量空闲 bytes，但 IOPS 快用完了。

这时适合放：

```text
低 IOPS、大容量归档数据
```

因为归档数据几乎不消耗 IOPS，只消耗容量。

这样就能把剩余容量利用起来。

---

### 六、如何理解 Figure 7.7？

原文说：

> Figure 7.7 shows the wide range of I/O needs of Google workloads that use disk storage.

这张图展示的是：

> Google 使用磁盘存储的工作负载有非常宽的 I/O 需求范围。

---

#### 1. theoretical HDD size 是什么？

原文说：

> For each byte stored, we calculate the theoretical HDD size that it could fit on while running at 100% utilization, i.e., maximum seek rate.

也就是说：

> 对每个存储字节，计算它理论上可以放在多大的 HDD 上，同时让该 HDD 达到 100% 利用率。

这里的 100% 利用率指：

> HDD 的 I/O 能力，例如最大 seek rate，被充分利用。

可以理解为：

```text
某工作负载每 byte 只产生很少 IOPS
    ↓
它理论上可以放在一个非常大的 HDD 上
    ↓
因为即使磁盘容量很大，I/O 需求也足够把磁盘 IOPS 用满
```

---

#### 2. 最冷负载理论上可以用超过 300 TB 的磁盘

原文说：

> the coldest workloads could use disks in excess of 300 TB, ten times larger than the largest actual disks available in 2024.

也就是说：

> 最冷的工作负载理论上可以放在超过 300 TB 的磁盘上。

而 2024 年实际最大磁盘容量大约只有它的十分之一。

这意味着：

```text
最冷负载的 IOPS / byte 极低
```

如果用真实最大磁盘服务它：

```text
磁盘容量可能合适
但 IOPS 远远用不完
```

原文说：

> those workloads would run even the largest disks available at <10% of their available I/O rates.

也就是说：

> 如果用专用存储 fleet 服务这些冷负载，即使使用最大磁盘，也只能利用不到 10% 的 I/O 能力。

这就是专用部署的浪费。

---

#### 3. 最热 bytes 需要小得多磁盘

原文说：

> Conversely, the hottest bytes need much smaller disks.

热数据每 byte 产生更多 IOPS。

因此它适合：

- 小容量磁盘；
- 高 IOPS 设备；
- SSD；
- 低延迟介质。

---

#### 4. Google 的数据整体偏冷

原文说：

> even at the 80th percentile, data fits drives that are larger than what’s commercially available today.

也就是说：

> 即使到第 80 百分位，Google 的数据仍然可以适配比当前商用磁盘更大的磁盘。

这说明：

> Google 有大量半归档、低 IOPS 数据。

原文进一步解释：

> Google’s storage needs differ from that of typical enterprises, which do not have the large semi-archival storage demands stemming from storing people’s rarely accessed old photos and videos.

Google 存储需求与典型企业不同，因为 Google 要存储：

- 用户旧照片；
- 用户旧视频；
- 很少访问但长期保留的数据。

这些数据量巨大，但访问频率低。

---

### 七、为什么分别计费 IOPS 和 bytes？

原文说：

> the internal billing system charges for the cost of IOPS and cost of bytes separately.

也就是说：

> Google 内部计费系统分别收取 IOPS 成本和 bytes 成本。

这很重要。

---

#### 1. 如果只按容量计费会怎样？

如果只按 bytes 收费：

```text
开发者只关心容量价格
    ↓
可能随意使用高 IOPS
    ↓
昂贵 IOPS 被浪费
```

例如：

- 一个冷数据服务本来只需要低 IOPS；
- 但因为 IOPS 不收费；
- 它可能频繁扫描；
- 导致设备 IOPS 被耗尽；
- 影响其他服务。

---

#### 2. 如果只按 IOPS 计费会怎样？

如果只按 IOPS 收费：

```text
开发者只关心 IOPS 价格
    ↓
可能浪费容量
```

例如：

- 为了减少 IOPS 成本；
- 把数据压缩或组织得不合理；
- 或者过度删除；
- 或者选择不适合的数据布局；
- 导致容量利用变差。

---

#### 3. 分别计费让开发者做经济权衡

原文说：

> This cost model allows us to incentivize developers to correctly trade off between bytes and IOPS to achieve an economic balance.

也就是说：

> 这种成本模型激励开发者在 bytes 和 IOPS 之间做正确权衡。

开发者会考虑：

```text
是多存一些 bytes，减少 IOPS？
还是少存一些 bytes，增加 IOPS？
是使用冷存储？
还是使用高性能存储？
```

这样技术决策和经济成本对齐。

---

### 八、workload class separation：工作负载类别隔离

原文说：

> To support the sharing of I/O among varied workloads, the storage API enables workload class separation.

也就是说：

> 为了支持不同工作负载共享 I/O，存储 API 支持工作负载类别分离。

---

#### 1. 为什么需要类别分离？

如果把所有负载混在一起，没有任何隔离：

```text
延迟敏感服务 + 延迟容忍批处理
```

批处理任务可能占满磁盘 I/O，导致：

- Gmail 延迟升高；
- YouTube 请求变慢；
- 用户服务 SLO 被破坏。

因此需要隔离。

---

#### 2. 延迟敏感 vs 延迟容忍

原文说：

> Latency-sensitive workloads are isolated from latency-tolerant workloads through distinct storage service categories.

也就是：

```text
延迟敏感服务：
Gmail
YouTube
用户搜索
在线交易

延迟容忍任务：
数据分析
数据移动
批处理
备份
归档
ML 数据预处理
```

存储系统给它们不同服务类别。

---

#### 3. bounded latency，有界延迟

原文说：

> This approach ensures bounded latency for service-oriented workloads such as Gmail and YouTube.

bounded latency 指：

> 延迟有可预测上限。

例如：

```text
99% 请求 < 10 ms
99.9% 请求 < 30 ms
```

这对用户服务非常重要。

---

#### 4. 批处理任务使用后台 I/O

原文说：

> a batch analytics job can access disks “in the background” while the storage system prioritizes services paying for latency-optimized IOPS.

也就是说：

> 批处理分析任务可以在后台访问磁盘，而存储系统优先服务那些为低延迟 IOPS 付费的服务。

这类似于 CPU 调度中的：

```text
高优先级交互任务
    +
低优先级批处理任务
```

存储系统也可以做：

```text
高优先级 I/O
    +
低优先级后台 I/O
```

这样既保证延迟敏感服务，又利用空闲 IOPS。

---

### 九、software-defined storage 与前面几节的关系

整个第 7 章都在讲 software-defined infrastructure。

可以把各节放在一起看：

|小节|对象|核心思想|
| -----------------------------------| ------------------| ----------------------------------------|
|7.1 Software-defined servers|服务器 / 计算|软件理解和调度异构计算硬件|
|7.2 Software-defined accelerators|加速器 / ML 硬件|软件自动设计适合加速器的模型|
|7.3 Software-defined networks|网络|软件集中控制网络拓扑、路径、带宽、安全|
|7.4 Software-defined storage|存储|软件让容量和 IOPS 在全球设备间可互换|

共同思想是：

```text
硬件异构、资源有限、负载多样
    ↓
通过软件抽象、全局视图、策略控制、QoS、计费
    ↓
实现更高利用率、更低成本、更好性能
```

---

### 十、这一节的核心逻辑链

```text
WSC 工作负载极其多样
  ↓
传统存储为单一负载专用部署
  ↓
容量和 IOPS 很难同时用满
  ↓
Google 使用统一全局分层存储系统
  ↓
多种存储服务构建在 Colossus 上
  ↓
软件定义存储让 bytes 和 IOPS 可互换
  ↓
混合负载、全球分布、大池优化
  ↓
按 IOPS 和 bytes 分别计费
  ↓
通过 workload class separation 隔离延迟敏感和延迟容忍负载
  ↓
同时提高利用率和保证服务质量
```

---

### 十一、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.4 Software-defined storage

1. 核心目标：
   - 通过 software-defined storage 优化存储效率
   - 在不同数据中心和存储设备之间提供 fungibility
   - fungibility：
     - 存储资源可互换
     - 可统一调度
     - 可混合服务多种工作负载

2. 传统存储系统的问题：
   - 常为特定工作负载专门部署
   - 数据库：
     - 使用高端 SSD
     - 优先性能
   - 归档云：
     - 使用最大容量 HDD
     - 优先 cost per byte
     - IOPS 大量闲置
   - 结果：
     - 设备专用化
     - 资源碎片化
     - 至少一种设备能力未被充分利用

3. WSC 为什么需要软件定义存储：
   - WSC 服务和负载类型非常多
   - 要最大化数据中心 footprint 效率
   - 存储资源必须尽可能 fungible
   - 需要跨设备、跨数据中心统一优化

4. Google 的存储架构：
   - 使用 unified global layered storage system
   - 统一：
     - 多种存储服务共享底层系统
   - 全球：
     - 存储资源可跨数据中心调度
   - 分层：
     - 不同性能、容量、延迟、成本层级

5. Colossus：
   - Google 的模块化分布式存储系统
   - 多种存储服务构建在其上：
     - block
     - database
     - object
     - key-value
     - file
   - 好处：
     - 无缝集成
     - 全局优化
     - 全球可扩展
     - 提高资源互换性
```

```text
7.4.1 Storage workload diversity

1. 存储设备的两类资源：
   - bytes：
     - 存储容量
   - access capability：
     - IOPS
     - bandwidth
   - 每个设备都有固定容量和固定访问能力

2. 工作负载差异：
   - 每个 workload 需要不同 bytes vs IOPS 比例
   - 冷负载：
     - 大容量
     - 低 IOPS
   - 热负载：
     - 小容量或中等容量
     - 高 IOPS
   - 数据库：
     - 高 IOPS、低延迟
   - 归档：
     - 大容量、低 IOPS
   - 分析：
     - 大容量、延迟容忍、可后台使用空闲 I/O

3. 静态匹配的问题：
   - 简单方法：
     - 冷负载用大 HDD
     - 热负载用小 HDD 或 SSD
   - 但工作负载很难完美匹配设备
   - 总会浪费至少一种资源：
     - 容量用满，IOPS 闲置
     - IOPS 用满，容量闲置
   - 应用访问模式会随时间变化
   - 今天合适设备一年后未必合适

4. 软件定义存储的解决方式：
   - 将不同工作负载合并到共享设备
   - 按整体 fleet 的 IOPS/TB 比例 right-size 设备组合
   - 大池比单个应用更容易优化
   - 低 IOPS 归档负载可以跨洲或全球分布
   - 填充那些 IOPS 接近上限但仍有空闲 bytes 的设备

5. Figure 7.7 的含义：
   - 展示 Google 磁盘工作负载的 I/O 需求范围
   - 对每个 byte 计算理论 HDD size：
     - 使该 HDD 在 100% I/O 利用率下运行
   - 最冷工作负载：
     - 理论磁盘大小超过 300 TB
     - 比 2024 年最大实际磁盘大约十倍
     - 若用专用 fleet，即使用最大磁盘也只利用 <10% IOPS
   - 最热 bytes：
     - 需要小得多磁盘
   - Google 数据整体偏冷：
     - 即使 80th percentile 也适配比当前商用更大的磁盘
   - Google 与典型企业不同：
     - 有大量半归档数据
     - 例如用户很少访问的旧照片和视频
   - 图右端：
     - 磁盘无法维持所需 IOPS
     - 数据需要存 SSD
     - 原文省略该部分

6. 内部计费模型：
   - IOPS 成本和 bytes 成本分别计费
   - 目的：
     - 正确反映实际成本
     - 帮助容量和性能规划
     - 激励开发者在 bytes 和 IOPS 之间权衡
   - 如果只按 bytes 计费：
     - 可能浪费 IOPS
   - 如果只按 IOPS 计费：
     - 可能浪费容量
   - 分别计费促使经济平衡

7. workload class separation：
   - 存储 API 支持工作负载类别分离
   - 延迟敏感负载与延迟容忍负载隔离
   - 延迟敏感：
     - Gmail
     - YouTube
     - 用户服务
     - 需要 bounded latency
   - 延迟容忍：
     - data analytics
     - data movement
     - batch jobs
   - batch analytics job 可后台访问磁盘
   - 存储系统优先服务为 latency-optimized IOPS 付费的服务

8. 核心逻辑：
   存储负载多样
     → bytes 和 IOPS 比例差异巨大
     → 专用部署导致资源浪费
     → software-defined storage 统一池化
     → 全球范围混合负载
     → 分别计费 IOPS 和 bytes
     → workload class separation 保证延迟隔离
     → 同时提高利用率和用户体验
```

---

### 十二、一句话总结这两小节

> 7.4 和 7.4.1 说明：软件定义存储通过统一底层存储系统、全球池化设备资源、混合不同 bytes/IOPS 比例的工作负载，并配合分别计费和工作负载类别隔离，使存储资源像计算和网络资源一样可软件定义、可全局调度、可高效复用。


**专栏导航**

- ← 上一篇：[7.3.5 DDoS attack mitigation 和 7.3.6 What’s next for SDN](/posts/7-3-5-ddos-attack-mitigation-7-3-6-what-s-next-for-sdn/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.4.2 Transparent SSD caching、7.4.3 Trading data center space between compute and storage、7.4.4 Other software-managed hardware optimizations →](/posts/7-4-2-transparent-ssd-caching-7-4-3-trading-data-center-space-between-compute-and-storage-7-4-4-other-software-managed-hardware-optimizations/)
