---
title: "7.4.2 Transparent SSD caching、7.4.3 Trading data center space between compute and storage、7.4.4 Other software-managed hardware optimizations"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-29
description: "《The Data Center as a Computer》AI 导读专栏正文：7.4.2 Transparent SSD caching、7.4.3 Trading data center space between compute and storage、7.4.4 Other software-managed hardware optimizations。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：7.4.2 Transparent SSD caching、7.4.3 Trading data center space between compute and storage、7.4.4 Other software-managed hardware optimizations。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 7.4.2 Transparent SSD caching、7.4.3 Trading data center space between compute and storage、7.4.4 Other software-managed hardware optimizations

下面把 **7.4.2 Transparent SSD caching**、**7.4.3 Trading data center space between compute and storage**、**7.4.4 Other software-managed hardware optimizations** 放在一起深入理解，并在最后附上可以直接加入笔记的**精简笔记版**。

这三节继续围绕 7.4 的核心问题展开：

> 存储系统中最稀缺的资源并不总是容量 bytes，也可能是 IOPS、数据中心空间、电力、冷却、设备寿命或写入带宽。  
> 软件定义存储的目标，就是让这些资源在全球范围内尽可能可互换、可调度、可优化。

---

### 一、三节之间的总体关系

先给一个整体框架。

|小节|核心错配|软件定义存储的解决方式|
| -------------------------------------------------------------| ------------------------------------| -----------------------------------------|
|7.4.2 Transparent SSD caching|HDD 容量很大，但 IOPS 不足|用 SSD 做透明缓存，补足 IOPS|
|7.4.3 Trading data center space between compute and storage|不同数据中心的计算和存储需求不平衡|用可移动冷存储平衡空间、电力和容量|
|7.4.4 Other software-managed hardware optimizations|SSD 写放大、HDD SMR/CMR 管理复杂|软件利用应用 hints 控制设备内部数据放置|

可以把它们理解为：

```text
7.4.2：
解决“容量够，但 IOPS 不够”的问题。

7.4.3：
解决“这个地方缺存储，那个地方缺计算”的问题。

7.4.4：
解决“设备内部介质如何更聪明地写数据”的问题。
```

它们都体现了同一个思想：

> 不让硬件固定服务于某类负载，而是让软件在全局层面决定数据放在哪里、如何访问、如何优化。

---

### 7.4.2 Transparent SSD caching 深入理解

#### 一、问题：HDD 越来越大，但 IOPS 没有同步增长

原文说：

> With the growth in the size of deployed HDDs, the demand for IOPS has surpassed the IOPS provided by the HDDs from deployed bytes.

也就是说：

> 随着部署的 HDD 容量越来越大，系统需要的 IOPS 已经超过了这些 HDD 所能提供的 IOPS。

这背后有一个关键趋势：

```text
HDD 容量增长很快
但 HDD 的 IOPS 增长很慢
```

因为 HDD 是机械设备，IOPS 受限于：

- 磁头寻道；
- 盘片旋转；
- 机械臂移动；
- 随机访问延迟。

一块 HDD 容量可以从：

```text
4 TB → 8 TB → 16 TB → 20 TB → 30 TB+
```

但它的随机 IOPS 并不会同步翻倍。

因此每 TB 能提供的 IOPS 会下降：

```text
小容量 HDD：
每 TB IOPS 较高

大容量 HDD：
每 TB IOPS 较低
```

---

#### 二、如果只靠 HDD 补 IOPS，会产生 stranded bytes

原文说：

> Meeting the collective IOPS demand using current HDD sizes would require significantly more HDDs, leading to stranded bytes.

假设系统需要更多 IOPS。

如果只靠 HDD 提供 IOPS，就必须买更多 HDD。

但每买一块 HDD，不仅买到 IOPS，也买到大量容量。

例如：

```text
需要：100,000 IOPS
一块大容量 HDD：200 IOPS，30 TB

为了满足 IOPS：
需要 500 块 HDD

但同时会得到：
500 × 30 TB = 15 PB 容量
```

如果系统其实并不需要 15 PB 容量，那么这些容量就会闲置。

这就是：

> stranded bytes，搁浅容量。

也就是：

```text
你为了 IOPS 买硬盘
结果容量太多用不掉
```

这在经济上非常浪费。

---

#### 三、解决方式：用 SSD 做全球共享存储缓存

原文说：

> To achieve an optimal balance between HDDs deployed and IOPS utilization, we leverage a global shared storage cache implemented on SSDs.

也就是说：

> 为了在 HDD 部署量和 IOPS 利用率之间取得最佳平衡，Google 使用基于 SSD 的全球共享存储缓存。

这里的核心是：

```text
HDD 提供大容量
SSD 提供高 IOPS
```

让两者分工：

|介质|优势|角色|
| ------| -----------------| --------------------------|
|HDD|便宜、大容量|存储大量冷数据|
|SSD|高 IOPS、低延迟|缓存热数据或高 IOPS 数据|

这样就不必为了 IOPS 买大量 HDD。

---

#### 四、为什么是 global shared storage cache？

原文强调：

> global shared storage cache

不是每台服务器自己加一块 SSD 做本地缓存，而是：

> 全球共享的存储缓存池。

这有几个好处。

---

##### 1. 可以动态分配 IOPS

不同工作负载的 IOPS 需求会变化。

例如：

- 白天用户服务热；
- 晚上批处理任务热；
- 某个视频突然爆火；
- 某个分析任务临时扫描大量数据；
- 某个数据库促销活动时 IOPS 激增。

如果 SSD 缓存是全球共享池，就可以：

```text
哪里需要 IOPS，就把缓存资源倾斜到哪里
```

---

##### 2. 避免为每个应用单独预留 SSD

传统方式可能：

```text
数据库应用 → 专用 SSD
分析应用 → 专用 HDD
归档应用 → 专用大容量 HDD
```

这样会导致：

- 某些 SSD 闲置；
- 某些 HDD IOPS 闲置；
- 某些容量用不完；
- 某些 IOPS 不够用。

全球共享缓存可以统计复用：

```text
所有负载共享 SSD 缓存池
    ↓
整体 IOPS 需求更平滑
    ↓
利用率更高
```

---

##### 3. 与前面的 fungible storage 一致

7.4 一开始就强调：

> fungibility，可互换性。

SSD 缓存池也是这个思想：

> SSD 不是固定属于某个应用，而是作为全局 IOPS 资源被软件动态分配。

---

#### 五、为什么是 transparent？

原文说：

> By leveraging a cache behind the unified storage API, we can seamlessly balance the system without requiring modifications to existing workloads.

关键词：

> transparent，透明。

也就是说：

> 应用不需要知道自己读的是 SSD 缓存还是 HDD 容量。

应用只通过统一存储 API 访问数据：

```text
应用：
读某个对象 / 文件 / block
    ↓
统一存储 API
    ↓
存储系统判断：
如果在 SSD cache 中，快速返回
如果不在，从 HDD 读取，并可能缓存
```

应用不需要：

- 修改代码；
- 手动指定 SSD；
- 管理缓存；
- 决定冷热数据；
- 处理数据迁移。

这就是软件定义存储的价值：

> 把复杂性放在存储系统内部，对应用保持简单抽象。

---

#### 六、SSD caching 如何帮助利用 HDD 的 bytes 和 IOPS？

原文说：

> This storage cache enables us to effectively utilize all deployed HDD bytes and IOPS capacity.

可以这样理解。

没有 SSD cache 时：

```text
HDD 容量很大
但 IOPS 不够
    ↓
为了 IOPS 加 HDD
    ↓
容量过剩，stranded bytes
```

有 SSD cache 后：

```text
HDD 存大量数据
SSD 缓存热数据 / 高 IOPS 数据
    ↓
HDD 容量被充分利用
HDD 的有限 IOPS 用于冷数据
SSD 补足热数据 IOPS
    ↓
整体 bytes 和 IOPS 都更接近充分利用
```

这相当于把存储系统变成一个分层结构：

```text
热数据 / 高 IOPS 数据
        ↓
     SSD cache
        ↓
冷数据 / 大容量数据
        ↓
      HDD pool
```

---

#### 七、一个直观例子

假设有一个照片存储服务。

数据总量：

```text
100 PB
```

但绝大多数照片很少访问。

例如：

```text
99% 照片：冷数据
1% 照片：热数据，经常被用户查看
```

如果全部用 HDD：

```text
容量够
但热照片 IOPS 可能不够
```

如果全部用 SSD：

```text
IOPS 够
但成本极高，容量不划算
```

透明 SSD caching：

```text
100 PB 主要放 HDD
热照片自动缓存到 SSD
用户访问热照片时从 SSD 读取
用户访问旧照片时从 HDD 读取
```

这样：

- 成本低；
- 容量大；
- 热数据快；
- 应用无感知；
- 全局利用率高。

---

### 7.4.3 Trading data center space between compute and storage 深入理解

这一节把视角从“设备”提升到“数据中心”。

核心问题是：

> 不同数据中心对计算和存储的需求不一样。  
> 软件定义存储可以让冷数据跨数据中心移动，从而平衡空间、电力、容量和计算资源。

---

#### 一、数据中心面临计算和存储比例不平衡

原文说：

> Data centers face varying demands for compute and storage, affecting the ratio between them.

也就是说：

> 不同数据中心对计算和存储的需求不同，这会影响计算与存储之间的比例。

例如：

|数据中心|可能情况|
| ----------| ----------------------------------|
|DC A|计算机架满，存储有空余|
|DC B|存储机架满，计算有空余|
|DC C|电力充足，但空间紧张|
|DC D|空间充足，但电力紧张|
|DC E|网络带宽充足，适合放冷数据|
|DC F|网络带宽紧张，不适合放大量冷数据|

数据中心不是无限资源。  
它受限于：

- 机架空间；
- 电力；
- 冷却；
- 网络带宽；
- 运维成本；
- 地理位置；
- 法律合规；
- 故障域；
- 延迟要求。

---

#### 二、冷存储可以 location-independent

原文说：

> A significant portion of disk-based storage is “cold” and thus can be placed anywhere in a particular region or continent, or even globally.

也就是说：

> 很大一部分磁盘存储是冷数据，因此可以放在某个 region、某个 continent，甚至全球任何地方。

冷数据的特点是：

- 很少访问；
- 延迟不敏感；
- 不需要靠近用户；
- 不需要高带宽；
- 可以容忍较高访问延迟；
- 主要目标是低成本和高容量。

例如：

- 用户十年前上传的照片；
- 很少播放的视频；
- 历史备份；
- 归档日志；
- 合规数据；
- 冷数据集。

这些数据不需要放在离用户最近的数据中心。

---

#### 三、冷存储 placement 主要受数据本地化法律限制

原文说：

> Since cold storage requires little bandwidth per Tbyte of storage, placement isn’t constrained by network bandwidth but only by jurisdictional requirements for data locality.

也就是说：

> 冷存储每 TB 所需带宽很少，因此放置不受网络带宽限制，而主要受数据本地化司法管辖要求限制。

---

##### 1. 为什么不受网络带宽限制？

因为冷数据访问少。

例如：

```text
1 PB 冷数据
每天只访问几次
```

它不需要持续高带宽。

所以即使放在远端数据中心，也不会明显占用网络。

---

##### 2. 什么是 jurisdictional requirements？

jurisdictional requirements 指：

> 法律、监管或合规要求数据必须存储在特定地区或国家。

例如：

- 某些用户数据必须存在欧洲；
- 某些金融数据必须存在本国；
- 某些医疗数据有地区限制；
- 某些政府数据不能跨境。

因此冷数据虽然可以全球放，但仍要满足：

```text
数据主权
隐私法规
合规要求
审计要求
```

---

#### 四、Fungible storage 如何平衡数据中心需求？

原文说：

> Fungible storage allows us to balance demand and capacity across data centers.

也就是说：

> 可互换存储允许跨数据中心平衡需求和容量。

这非常关键。

---

##### 例子 1：用冷存储填充多余空间和电力

原文说：

> if a data center has excess space and power, unoccupied by compute, we can allocate a flexible amount of cold storage capacity to fill that space over time.

假设某个数据中心：

```text
计算需求不高
但有机架空间
有电力
有冷却
```

如果空着，就是浪费。

可以放什么？

> 冷存储。

因为冷存储：

- 不需要大量 CPU；
- 不需要高网络带宽；
- 不需要低延迟；
- 可以慢慢部署；
- 可以长期存放数据；
- 能利用闲置空间和电力。

这样就把原本闲置的数据中心资源利用起来。

---

##### 例子 2：利用 otherwise stranded bytes

原文说：

> if there’s an imbalance between IOPS and bytes, we can relocate the cold portion of location-independent storage to that data center, utilizing available bytes that would otherwise go stranded.

假设某数据中心：

```text
IOPS 已接近上限
但还有很多空闲容量
```

也就是说：

```text
IOPS 不够
bytes 很多
```

如果放热数据，会加剧 IOPS 压力。  
但放冷数据很合适，因为冷数据几乎不消耗 IOPS。

于是可以把冷数据迁移过来：

```text
冷数据 → 迁移到有空闲 bytes 的数据中心
热数据 → 留在 IOPS 充足的地方
```

这样原本会闲置的 bytes 就被利用起来了。

---

#### 五、计算和存储之间的“空间交易”

这一节标题是：

> Trading data center space between compute and storage

可以理解为：

> 在数据中心内部和数据中心之间，对计算资源与存储资源进行动态交换。

例如：

```text
DC A：
计算满，存储空
    ↓
少放存储，多保留计算

DC B：
计算空，存储满
    ↓
少放计算，多放冷存储
```

或者：

```text
某机房未来计算需求增长
    ↓
逐步把冷存储迁走
    ↓
腾出空间和电力给计算
```

这说明存储不是固定放在某处的静态资产，而是：

> 可以根据全局需求移动的资源。

---

#### 六、与 7.4.2 的关系

7.4.2 解决：

```text
同一个存储池内部：
HDD bytes 多，但 IOPS 少
    ↓
用 SSD cache 补 IOPS
```

7.4.3 解决：

```text
不同数据中心之间：
有的地方缺计算
有的地方缺存储
有的地方 IOPS 紧张但 bytes 空闲
    ↓
用冷数据迁移平衡全局
```

两者合起来：

```text
设备层：
HDD + SSD cache 平衡 bytes/IOPS

数据中心层：
冷数据全球放置平衡 space/power/compute/storage
```

---

### 7.4.4 Other software-managed hardware optimizations 深入理解

这一节说明：

> 软件定义存储不仅可以在系统层做缓存和放置，还可以深入到存储设备内部，优化介质管理。

原文举了两个例子：

1. SmartFTL；
2. hybrid SMR HDD。

---

#### 一、SmartFTL：让 SSD 更聪明地写数据

原文说：

> SmartFTL, Flash Translation Layer, optimizations use application-provided write hints to manage media placement to reduce write amplification.

要理解这个，需要先理解 FTL 和 write amplification。

---

#### 二、什么是 FTL？

FTL，Flash Translation Layer，闪存转换层。

SSD 内部不能像 HDD 那样直接原地覆盖写入。  
NAND flash 有擦除块限制：

```text
读取：可以按页
写入：可以按页
擦除：必须按块，而且块很大
```

因此 SSD 需要 FTL 做：

- 逻辑块地址到物理页地址映射；
- 垃圾回收；
- 磨损均衡；
- 坏块管理；
- 写入合并；
- 数据搬迁。

可以简单理解为：

```text
操作系统看到：
逻辑块 LBA

SSD 内部实际：
物理 NAND page

FTL 负责把 LBA 映射到物理 page
```

---

#### 三、什么是 write amplification？

write amplification，写放大。

它指：

> 主机写入少量数据，但 SSD 内部实际写入更多数据。

例如：

```text
主机写入：1 GB
SSD 内部实际写入：3 GB
```

那么写放大是：

```text
WA = 3
```

写放大会导致：

- NAND 寿命消耗更快；
- 内部带宽浪费；
- GC 压力增大；
- 延迟升高；
- 性能下降。

---

#### 四、为什么应用 hints 有帮助？

原文说：

> application-provided write hints

应用通常比 SSD 更了解数据特征。

例如应用知道：

- 哪些数据是热数据；
- 哪些数据是冷数据；
- 哪些数据马上会被覆盖；
- 哪些数据会长期保存；
- 哪些写入是顺序写；
- 哪些写入是随机写；
- 哪些数据属于日志；
- 哪些数据属于元数据；
- 哪些数据可以丢弃；
- 哪些数据需要高耐久。

如果 SSD 不知道这些，它只能猜测。  
猜测错误会导致：

```text
冷数据和热数据放在同一个擦除块
    ↓
GC 时不得不搬移大量冷数据
    ↓
写放大增加
```

如果应用提供 hints：

```text
SSD 可以把相似生命周期的数据放在一起
    ↓
GC 更高效
    ↓
写放大降低
```

---

#### 五、SmartFTL 的价值

SmartFTL 的核心是：

> 让应用知识参与 SSD 内部介质放置决策。

例如：

```text
应用告诉 SSD：
这是短生命周期日志数据
```

SSD 可以把它放到：

```text
容易被整体擦除的块
```

因为很快会失效，GC 时不需要搬移。

再比如：

```text
应用告诉 SSD：
这是长期冷数据
```

SSD 可以把它放到：

```text
稳定块中，减少搬移
```

这样可以：

- 降低写放大；
- 提高 SSD 寿命；
- 提高写入性能；
- 降低 GC 干扰；
- 改善尾延迟。

---

### 六、Hybrid SMR HDD：软件控制 CMR 和 SMR 数据放置

原文说：

> hybrid SMR HDD drives incorporate software control of how data is managed across CMR and SMR, conventional and shingled magnetic recordings.

这里涉及 HDD 的两种记录方式：

1. CMR，Conventional Magnetic Recording；
2. SMR，Shingled Magnetic Recording。

---

#### 1. CMR 是什么？

CMR 是传统磁记录。

磁道之间不重叠。

优点：

- 随机写性能好；
- 写入简单；
- 不需要重写相邻磁道；
- 适合频繁修改数据。

缺点：

- 磁道间距大；
- 容量密度较低；
- 每 TB 成本相对高。

---

#### 2. SMR 是什么？

SMR 是瓦楞式磁记录。

磁道像屋顶瓦片一样部分重叠。

优点：

- 磁道更密；
- 容量更高；
- 每 TB 成本更低。

缺点：

- 写入更复杂；
- 修改某个磁道可能影响相邻磁道；
- 随机写性能差；
- 通常需要顺序写或 zone 管理；
- GC 和整理成本高。

---

#### 3. Hybrid SMR HDD 的思想

hybrid SMR HDD 同时包含：

```text
CMR 区域
SMR 区域
```

然后由软件控制数据放置：

```text
热数据 / 随机写数据 → CMR
冷数据 / 顺序写大容量数据 → SMR
```

这样可以兼顾：

- CMR 的写性能；
- SMR 的容量密度。

---

#### 4. 为什么这也是 software-defined storage？

因为设备内部不是固定使用某种介质策略，而是：

> 软件根据数据特征决定数据放在 CMR 还是 SMR。

这和前面 SSD caching 的思想一致：

```text
不同数据有不同的访问特征
    ↓
软件把数据放到最合适介质
```

只不过这里不是：

```text
SSD vs HDD
```

而是：

```text
HDD 内部 CMR vs SMR
```

---

### 七、这三节共同体现的存储设计原则

---

#### 1. 存储资源不是单一的，而是多维的

存储不只有容量。

它至少包括：

```text
bytes
IOPS
bandwidth
latency
space
power
cooling
network
device lifetime
write bandwidth
legal locality
```

软件定义存储要同时优化这些维度。

---

#### 2. 不同负载的资源比例差异巨大

例如：

|负载|bytes|IOPS|latency|可移动性|
| ------------| ------: | -----: | --------: | ---------: |
|归档照片|很高|很低|不敏感|高|
|数据库|中|很高|敏感|低|
|视频播放|高|中|中|中|
|批处理分析|高|中|容忍|中高|
|元数据服务|低|很高|敏感|低|

因此不能用一种设备、一种放置策略服务所有负载。

---

#### 3. 软件负责“匹配”

软件定义存储的本质是匹配：

```text
把合适的数据
放到合适的介质
合适的数据中心
合适的性能等级
合适的成本等级
```

---

### 八、可以直接加入笔记的精简版

下面这一段可以加入你的笔记，风格与前面一致。

```text
7.4.2 Transparent SSD caching

1. 背景问题：
   - HDD 容量不断增长
   - 但 HDD 的 IOPS 增长有限
   - 大容量 HDD 的每 TB IOPS 更低
   - 总体 IOPS 需求可能超过已部署 HDD 能提供的 IOPS

2. 如果只靠 HDD 满足 IOPS：
   - 需要部署更多 HDD
   - 但同时会引入大量额外 bytes
   - 如果容量需求没有这么大：
     - 额外 bytes 会闲置
   - 这就是 stranded bytes，搁浅容量

3. 解决方式：
   - 使用 global shared storage cache
   - cache 由 SSD 实现
   - HDD 提供大容量
   - SSD 提供高 IOPS 和低延迟

4. Transparent caching：
   - cache 位于统一存储 API 之后
   - 应用无需修改
   - 应用不感知数据是在 SSD 还是 HDD
   - 存储系统自动管理冷热数据和缓存

5. 效果：
   - 平衡 HDD 部署量和 IOPS 利用率
   - 避免为了 IOPS 买太多 HDD
   - 避免 stranded bytes
   - 更有效利用所有已部署 HDD 的 bytes 和 IOPS

6. 核心逻辑：
   HDD 容量大但 IOPS 不足
     → 只加 HDD 会造成容量搁浅
     → 用 SSD 做透明共享缓存
     → 热数据 / 高 IOPS 数据走 SSD
     → 冷数据 / 大容量数据走 HDD
     → 同时提高容量利用率和 IOPS 利用率
```

```text
7.4.3 Trading data center space between compute and storage

1. 背景问题：
   - 不同数据中心对 compute 和 storage 的需求不同
   - 计算和存储之间的比例会变化
   - 工作负载对 IOPS 和 bytes 的需求也不同

2. location-independent storage：
   - 很多磁盘存储是 cold data
   - 冷数据可以放在：
     - 某个 region 内
     - 某个 continent 内
     - 甚至全球范围
   - 冷数据每 TB 所需带宽很低
   - 放置主要不受网络带宽限制
   - 主要受 jurisdictional requirements 限制：
     - 数据主权
     - 隐私法规
     - 合规要求
     - 数据本地化

3. Fungible storage 的作用：
   - 允许跨数据中心平衡需求和容量
   - 存储不是固定绑定在某个数据中心
   - 冷数据可以作为灵活资源移动

4. 例子 1：填充空闲空间和电力：
   - 如果某数据中心有计算未占用的空间和电力
   - 可以部署灵活数量的冷存储
   - 逐步填满闲置资源

5. 例子 2：利用 stranded bytes：
   - 如果某数据中心 IOPS 和 bytes 不平衡
   - 例如 IOPS 接近上限但 bytes 空闲
   - 可以把 location-independent 的冷数据迁移过去
   - 冷数据消耗很少 IOPS
   - 因此能利用原本会闲置的 bytes

6. 核心逻辑：
   数据中心之间 compute/storage 需求不均
     → 冷数据 location-independent
     → 软件定义存储可全球移动冷数据
     → 用冷存储填充空闲空间、电力和容量
     → 平衡全局数据中心资源利用率
```

```text
7.4.4 Other software-managed hardware optimizations

1. 核心思想：
   - 软件定义存储不仅优化系统层
   - 也可以深入设备内部优化介质管理
   - 设计空间很大

2. SmartFTL：
   - FTL：
     - Flash Translation Layer
     - 管理 SSD 中逻辑地址到物理 NAND 的映射
     - 处理垃圾回收、磨损均衡、写入合并等
   - write amplification：
     - 主机写入少量数据
     - SSD 内部实际写入更多数据
     - 会增加 NAND 磨损和性能开销
   - SmartFTL：
     - 使用 application-provided write hints
     - 管理 media placement
     - 降低 write amplification
   - hints 可以包括：
     - 数据冷热
     - 生命周期
     - 顺序写 / 随机写
     - 是否短期有效
     - 是否需要高耐久
   - 好处：
     - 更少 GC 搬移
     - 更低写放大
     - 更长 SSD 寿命
     - 更稳定性能

3. Hybrid SMR HDD：
   - SMR：
     - Shingled Magnetic Recording
     - 磁道部分重叠
     - 容量密度高
     - 随机写性能差
   - CMR：
     - Conventional Magnetic Recording
     - 随机写性能更好
     - 容量密度低于 SMR
   - hybrid SMR HDD：
     - 同时包含 CMR 和 SMR
     - 软件控制数据在 CMR 和 SMR 之间放置
   - 典型策略：
     - 热数据 / 随机写数据放 CMR
     - 冷数据 / 顺序写大容量数据放 SMR
   - 好处：
     - 兼顾容量密度和写性能
     - 更适合软件定义存储管理

4. 核心逻辑：
   设备内部介质管理也很复杂
     → 应用比设备更了解数据特征
     → 软件提供 hints 或控制策略
     → SSD 降低写放大
     → HDD 在 CMR/SMR 之间优化放置
     → 提高寿命、性能和容量利用率
```

---

### 九、一句话总结这三节

> 7.4.2 到 7.4.4 说明：软件定义存储不仅要在全球范围池化容量和 IOPS，还要用 SSD 透明缓存补足 HDD 的 IOPS 不足，用冷数据跨数据中心迁移平衡计算与存储资源，并深入到 SSD FTL 和 SMR/CMR HDD 等设备内部，通过软件控制数据放置来提高整体效率。


**专栏导航**

- ← 上一篇：[7.4 Software-defined storage 和 7.4.1 Storage workload diversity](/posts/7-4-software-defined-storage-7-4-1-storage-workload-diversity/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.5 Software-defined data center 中的 7.5.1 Software-defined power →](/posts/7-5-software-defined-data-center-7-5-1-software-defined-power/)
