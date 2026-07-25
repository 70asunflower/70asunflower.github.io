---
title: "6.4.6 Special-purpose networks 和 6.4.7 WANs"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：6.4.6 Special-purpose networks 和 6.4.7 WANs。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.4.6 Special-purpose networks 和 6.4.7 WANs。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.4.6 Special-purpose networks 和 6.4.7 WANs

下面这两节 **6.4.6 Special-purpose networks** 和 **6.4.7 WANs** 是 6.4 Networking 的收尾部分。

如果说前面几节讲的是：

```text
主机网络
集群 Clos
OCS
光互连
```

那么这两节讲的是：

> **除了通用数据中心 fabric 之外，WSC 还会为特定流量构建专用网络；同时云厂商还需要私有 WAN 和边缘网络，把全球数据中心连接起来。**

这两节的核心可以概括为：

> **网络可扩展性不仅靠更大的 Clos，也靠“流量分层和网络分平面”。存储、AI 加速器、应用、管理、**​**WAN 等不同流量可以走不同专用网络** **，以优化性能、成本、协议和故障域。**

---

### 1. 6.4.6 的核心：专用网络是另一种扩展方式

原文开头说：

> Another way to tackle network scalability is to offload some traffic to a special-purpose network.

这是非常重要的一句。

前面 6.4.3 和 6.4.4 讲的是如何把通用数据中心网络做大：

- Clos；
- fat-tree；
- spine；
- OCS；
- optics；
- oversubscription。

但还有另一种思路：

> 不要把所有流量都放在同一个通用网络里，而是把某些大流量、特殊流量卸载到专用网络。

例如：

```text
存储流量 → storage network / SAN
AI 训练流量 → accelerator interconnect / backend network
应用流量 → general data center fabric
管理流量 → management network
WAN 流量 → private WAN / edge network
```

这就是“网络分平面”的思想。

---

### 2. Storage Area Network：SAN

原文说：

> For example, we could build a separate network to connect servers to storage units. Such networks usually are called Storage Area Networks, or SANs.

SAN 是专门连接服务器和存储设备的网络。

传统上，服务器访问磁盘可以通过：

```text
本地磁盘
   ↓
直接附加存储 DAS
   ↓
网络附加存储 NAS
   ↓
存储区域网络 SAN
```

SAN 的典型特点是：

- 服务器看到远程磁盘像本地块设备；
- 使用块级存储协议；
- 低延迟；
- 高可靠；
- 独立于普通 IP/Ethernet 网络；
- 常用于企业数据库、虚拟化、关键业务存储。

---

#### 2.1 为什么 SAN 可以降低成本？

原文说：

> If that traffic is more localized, not all servers need to be attached to all storage units, we could build smaller-scale networks, thus reducing costs.

这是专用网络的重要经济学基础。

如果存储流量是局部性的：

```text
不是所有服务器都访问所有存储
```

那么就不需要把所有服务器和所有存储都接入一个巨大的 full-mesh 网络。

可以构建较小规模的存储网络：

```text
一组服务器
   ↓
SAN fabric
   ↓
一组存储阵列
```

这样可以：

- 减少交换机端口；
- 减少光模块；
- 减少布线；
- 降低网络规模；
- 降低拥塞；
- 提高存储流量隔离性；
- 降低 TCO。

---

### 3. 从 Fibre Channel 到 Ethernet：存储网络演进

原文说：

> Historically, all storage was networked this way: a SAN connected servers to disks, typically using FibreChannel networks rather than Ethernet.

传统 SAN 常用：

```text
Fibre Channel
```

而不是 Ethernet。

---

#### 3.1 Fibre Channel 的特点

Fibre Channel 是专为存储网络设计的协议。

它的特点包括：

- 低延迟；
- 高可靠；
- 无损传输；
- 块存储语义；
- 适合 SCSI 命令；
- 独立于普通 IP 网络；
- 适合企业存储阵列。

但缺点也明显：

- 成本高；
- 生态相对封闭；
- 专用设备昂贵；
- 与通用数据中心网络融合困难；
- 运维体系独立；
- 不适合超大规模 WSC 的通用化需求。

---

#### 3.2 Ethernet 成为主流

原文说：

> Today, Ethernet is more common since it offers comparable speeds and protocols such as FibreChannel over Ethernet FCoE, SCSI over IP iSCSI, and more recently NVMe allow “converged” Ethernet networks to provide the functionality of traditional SANs.

现在 Ethernet 越来越常见，因为：

1. Ethernet 速度已经非常高；
2. Ethernet 生态规模巨大；
3. 成本远低于专用存储网络；
4. RDMA/RoCE 提供低延迟；
5. DCB 提供无损能力；
6. 存储协议可以在 Ethernet 上运行。

典型协议包括：

|协议|含义|
| ---------| ------------------------------|
|FCoE|Fibre Channel over Ethernet|
|iSCSI|SCSI over IP|
|NVMe-oF|NVMe over Fabrics|
|RDMA|Remote Direct Memory Access|
|RoCE|RDMA over Converged Ethernet|

这些协议让 Ethernet 可以提供传统 SAN 的功能。

这就是所谓的：

```text
converged Ethernet network
```

也就是融合网络：

```text
同一个 Ethernet fabric
同时承载：
- 数据流量
- 存储流量
- 管理流量
- 虚拟化流量
```

---

### 4. WSC 中的存储流量：可能完全不用传统存储协议

原文说：

> In WSCs, storage traffic may eschew traditional storage protocols entirely; for example, Google’s storage layer is accessed via Colossus RPCs. Similarly, AWS uses SRD, a proprietary protocol over Ethernet.

这里很关键。

超大规模 WSC 不一定使用传统 SAN 协议，例如 Fibre Channel、iSCSI。

它们可能使用自己的分布式存储协议。

---

#### 4.1 Google Colossus RPC

原文提到：

> Google’s storage layer is accessed via Colossus RPCs.

Colossus 是 Google 的分布式存储系统。

在 WSC 中，存储不是简单的：

```text
server → SAN → disk array
```

而是：

```text
application
   ↓
Colossus client
   ↓
RPC
   ↓
distributed storage service
   ↓
replication / erasure coding / metadata / scheduling
```

也就是说，存储是一个分布式服务，而不是传统块存储网络。

它通过 RPC 访问，底层可能仍然使用 Ethernet 和数据中心 fabric，但上层协议不是传统 SCSI/FC。

---

#### 4.2 AWS SRD

原文提到：

> AWS uses SRD, a proprietary protocol over Ethernet.

SRD 可以理解为 AWS 自研的高性能传输协议。

它运行在 Ethernet 上，但替代传统 TCP/IP 存储协议。

这类协议通常优化：

- 多路径；
- packet spraying；
- 低延迟；
- 高吞吐；
- 可靠传输；
- NIC offload；
- 拥塞控制；
- 大规模数据中心 fabric。

这说明：

> 超大规模云厂商常常不用传统存储网络协议，而是自研适合 WSC 的传输协议。

---

### 5. 存储流量曾经是数据中心主要流量

原文说：

> Historically, storage traffic dominated all other traffic, application RPCs, in data centers.

传统数据中心中，存储流量常常占主导。

原因包括：

- 数据库读写；
- 虚拟机磁盘；
- 日志写入；
- 备份；
- 存储复制；
- 虚拟化存储；
- 企业应用 I/O。

过去很多网络设计都围绕：

```text
server → storage
```

这条路径优化。

---

### 6. ML 流量成为新的大流量来源

原文说：

> More recently, ML traffic, GPU-GPU or TPU-TPU, has emerged as another large source of traffic.

这是现代 WSC 网络的重要变化。

AI 训练和推理产生大量加速器之间通信。

例如：

```text
GPU ↔ GPU
TPU ↔ TPU
node ↔ node
pod ↔ pod
```

这些流量包括：

- all-reduce；
- all-gather；
- reduce-scatter；
- all-to-all；
- activation 传输；
- gradient 同步；
- KV cache 传输；
- pipeline parallel 通信；
- tensor parallel 通信；
- expert parallel 通信。

AI 流量正在成为数据中心网络中最大、最敏感的流量之一。

---

### 7. 加速器带宽极高：每芯片数百 Gbps

原文说：

> Given that these chips can perform hundreds of Teraflops per second, they consume or produce hundreds of Gbps per device, often from or to other chips.

加速器计算能力极高。

如果每颗芯片能做数百 TFLOPS，那么它与其他芯片交换的数据量也非常大。

因此每颗芯片需要的互连带宽不是几 Gbps，而是：

```text
数百 Gbps
甚至数 Tbps
```

---

#### 7.1 TPUv5 node 示例

原文：

> a TPUv5 node provides 4.8 Tbps of ICI bandwidth for 459 TFLOPs of 16-bit computations.

也就是说：

```text
459 TFLOPs BF16 计算
对应
4.8 Tbps ICI 带宽
```

这说明 TPU 的计算和互连是协同设计的。

如果只有计算能力，没有足够 ICI 带宽，就会出现：

```text
计算单元等待数据
同步等待
通信瓶颈
训练 goodput 下降
```

---

#### 7.2 H100 GPU 示例

原文：

> a H100 GPU supports 7.2 TBps of NVLink bandwidth for 2671 TFLOPs of 16-bit computations.

也就是说：

```text
2671 TFLOPs 16-bit 计算
对应
7.2 TB/s NVLink 带宽
```

这说明现代 GPU 也不只是计算芯片，而是：

```text
计算 + 高带宽内存 + 高速互连
```

的系统。

---

### 8. 加速器互连更像共享内存互连，而不是 Ethernet

原文说：

> In both cases, this bandwidth is provided by a separate network that’s specialized for small block transfers and more closely resembles a shared-memory interconnect than an Ethernet network.

这句话非常关键。

TPU 的 ICI 和 GPU 的 NVLink 不是普通 Ethernet。

它们更像：

```text
shared-memory interconnect
```

也就是共享内存式互连。

---

#### 8.1 Ethernet 的特点

Ethernet 是通用包交换网络。

它适合：

- IP 包；
- TCP/UDP；
- RPC；
- 存储；
- 多租户；
- 路由；
- 广域互连；
- 通用数据中心 fabric。

但它通常不是为极细粒度内存语义优化的。

---

#### 8.2 ICI/NVLink 的特点

ICI 和 NVLink 更适合：

- 小块数据传输；
- 远程内存访问；
- DMA；
- tensor 切分通信；
- collective communication；
- 低延迟；
- 高带宽；
- 紧耦合并行计算；
- GPU/TPU 之间直接通信。

它们更像：

```text
把多个加速器连接成一个大内存/大计算系统
```

而不是简单把多台机器连成网络。

---

#### 8.3 对比表

|维度|Ethernet|ICI / NVLink|
| ----------| ------------------------| ---------------------------------|
|定位|通用网络|加速器专用互连|
|语义|packet/network|memory/DMA/collective|
|延迟|相对较高|更低|
|带宽|高，但受网络层级限制|极高|
|扩展范围|机架/集群/数据中心/WAN|pod/node 内为主|
|协议|IP/Ethernet/RDMA|专用互连协议|
|适合流量|通用数据、存储、应用|tensor 通信、梯度同步、远程内存|
|拓扑|Clos/fabric|torus、NVLink mesh、pod|

---

### 9. 专用加速器互连规模有限

原文说：

> However, these special-purpose accelerator interconnects have limited sizes.

虽然 ICI/NVLink 很快，但它们不能无限扩展。

原文给出 2025 年例子：

```text
最大 TPUv7 pod：9,216 chips
最大 NVLink pod：256 H100 GPUs
```

这说明专用加速器互连的规模是有限的。

---

#### 9.1 为什么规模有限？

因为专用互连通常要求：

- 极低延迟；
- 极高带宽；
- 紧耦合；
- 专用物理链路；
- 专用交换或光互连；
- 严格拓扑；
- 高功耗；
- 高成本；
- 复杂布线；
- 故障域控制。

所以它很难像 Ethernet 一样无限扩展。

---

### 10. 大模型训练需要 inter-pod 网络

原文说：

> Large training runs need more than that, requiring data center networks to support high-bandwidth interconnects between multiple pods at speeds of multiple hundreds of Gbps per node.

如果训练任务超过单个 pod 规模，就需要：

```text
pod ↔ pod
```

的高带宽网络。

例如：

```text
TPU pod A
   ↓
inter-pod network
   ↓
TPU pod B
```

或者：

```text
GPU pod A
   ↓
InfiniBand / Ethernet backend network
   ↓
GPU pod B
```

每节点可能需要：

```text
数百 Gbps
```

的跨 pod 带宽。

---

#### 10.1 inter-pod 网络通常也是专用网络

原文说：

> Often, this inter-pod network is a separate network as well so that accelerator-to-accelerator traffic travels solely on that network.

也就是说，加速器之间的流量不应该和普通应用流量混在一起。

它会走单独的：

```text
accelerator backend network
```

例如：

- GPU 训练网络；
- InfiniBand fabric；
- 高性能 Ethernet fabric；
- TPU inter-pod network；
- AI backend network。

---

#### 10.2 为什么加速器流量要单独网络？

因为 AI 训练流量非常敏感。

如果和普通应用流量混跑，会出现：

- 拥塞；
- 尾延迟；
- all-reduce 变慢；
- 训练 goodput 下降；
- 故障干扰；
- QoS 难保证；
- 调度复杂。

所以单独网络可以：

- 隔离流量；
- 优化 collective communication；
- 使用专门拥塞控制；
- 使用专门路由；
- 提高利用率；
- 降低尾延迟；
- 提高训练稳定性。

---

### 11. 服务器仍然需要连接通用数据中心 fabric

原文说：

> In contrast, the servers attached to the accelerators contain their own NICs that connect them to the rest of the data center fabric, and application traffic travels solely on that network.

加速器节点通常不只有加速器互连。

它们还有：

```text
host server NIC
```

用于连接通用数据中心 fabric。

这条网络承载：

- 应用流量；
- 控制平面；
- 存储访问；
- 日志；
- 监控；
- 调度；
- 模型加载；
- checkpoint；
- 用户请求；
- 管理流量。

所以一个 AI 节点可能同时连接多个网络平面。

---

### 12. 多网络平面架构

可以把现代 WSC 网络理解成多个平面。

```text
1. accelerator interconnect
   GPU-GPU / TPU-TPU
   NVLink / ICI
   pod 内高速互连

2. accelerator backend network
   pod 间训练流量
   InfiniBand / Ethernet / 高性能 fabric

3. storage network
   存储访问
   Colossus RPC / SRD / NVMe-oF / iSCSI

4. application network
   用户请求、RPC、服务间通信

5. management/control network
   BMC、IPU、调度、telemetry、attestation

6. WAN/edge network
   跨数据中心、用户接入、Internet peering
```

不同平面有不同目标：

|网络平面|主要目标|
| --------------------------| ------------------------------|
|accelerator interconnect|极低延迟、极高带宽|
|backend network|高吞吐、低尾延迟、collective|
|storage network|高 IOPS、低延迟、可靠|
|application network|通用 RPC、多租户|
|management network|安全、可靠、隔离|
|WAN|长距、弹性、流量工程|

---

### 13. 专用网络的设计权衡

专用网络不是永远好，它也有代价。

---

#### 13.1 优点

##### 1. 性能优化

可以针对特定流量优化：

- 协议；
- 路由；
- 拥塞控制；
- 队列；
- 拓扑；
- 互连语义。

---

##### 2. 成本优化

如果流量是局部性的，可以建 smaller-scale network。

例如不是所有服务器访问所有存储，就不需要 full fabric。

---

##### 3. 隔离

不同流量互不干扰。

例如：

- 存储流量不影响 AI 训练；
- 应用流量不影响管理流量；
- 租户流量不影响控制平面。

---

##### 4. 安全

专用网络可以限制访问范围。

例如管理网络不应暴露给租户。

---

##### 5. 协议适配

不同流量适合不同协议：

- 存储：NVMe-oF、SRD、RPC；
- AI：NCCL、ICI、NVLink；
- 应用：TCP、QUIC、gRPC；
- WAN：SDN、BGP、traffic engineering。

---

#### 13.2 缺点

##### 1. 网络数量增加

多平面意味着：

- 更多 NIC；
- 更多交换机；
- 更多布线；
- 更多运维；
- 更多故障域。

---

##### 2. 资源利用率可能降低

如果某个专用网络空闲，它的带宽不能轻易给其他流量使用。

---

##### 3. 系统复杂度增加

需要：

- 多网络调度；
- 多平面监控；
- 多协议栈；
- 多安全域；
- 多故障处理流程。

---

### 14. 6.4.7 WANs：连接全球数据中心

6.4.7 开始讲 WAN。

原文说：

> In this book we focus mainly on the data center aspects of the networking architecture and thus will only briefly cover WAN and edge networking.

这本书重点是数据中心网络，所以 WAN 和 edge 只是简要介绍。

但 WAN 对云厂商极其重要。

---

### 15. 云厂商为什么要私有 WAN？（**Wide Area Network（广域网）** ）

原文说：

> Cloud providers have developed private WANs to connect their data centers across the globe.

云厂商不依赖公共 Internet 来连接自己的数据中心。

它们建设私有 WAN。

原因包括：

1. **性能更可控**

   - 延迟更低；
   - 抖动更小；
   - 丢包更少；
   - 带宽更可预测。
2. **可靠性更高**

   - 多路径；
   - 快速故障切换；
   - 私有运维；
   - 流量工程。
3. **成本优化**

   - 长期看自建 WAN 可能比购买公网传输更划算；
   - 可以优化链路利用率。
4. **安全**

   - 数据中心间流量不暴露在公共 Internet；
   - 可加密；
   - 可审计；
   - 可控制。
5. **服务一致性**

   - 跨区域复制；
   - 全局负载均衡；
   - 多区域数据库；
   - 容灾；
   - 内容分发。

---

### 16. Google 网络规模极大

原文说：

> Because of internal demands from YouTube traffic, Google Drive, Google Ads serving, etc., Google’s network is an order of magnitude bigger than that of other public cloud providers.

这是因为 Google 不只是云服务商，还拥有巨大消费级流量：

- YouTube；
- Google Drive；
- Google Ads；
- Search；
- Gmail；
- Android；
- Google Photos；
- Google Maps。

这些业务产生巨大：

- 用户访问流量；
- 视频流量；
- 广告请求；
- 数据复制；
- 日志；
- 训练数据；
- 推理请求。

所以 Google 的网络规模非常大。

原文还提到：

> As of 2024, Google owns or co-owns 31 submarine cables.

海底电缆是洲际网络容量的关键基础设施。

拥有或共同拥有海底电缆可以：

- 保证跨洲带宽；
- 降低长期传输成本；
- 提高可靠性；
- 控制网络路径；
- 支持全球服务。

---

### 17. WAN 设计：SDN 和 traffic engineering

原文说：

> WANs are designed to handle massive bandwidth requirements and elastic traffic demand, and use software-defined networking SDN and traffic engineering to optimize performance.

WAN 与数据中心网络不同。

WAN 的特点：

- 距离长；
- 带宽贵；
- 链路容量有限；
- 流量需求波动大；
- 故障影响大；
- 延迟传播时间长；
- 跨运营商/跨洲；
- 维护复杂。

因此 WAN 非常依赖：

```text
SDN
+
traffic engineering
```

---

#### 17.1 SDN 的作用

SDN，Software-Defined Networking，把控制平面集中化。

在 WAN 中，SDN 可以：

- 集中查看全网链路利用率；
- 动态调整路由；
- 根据应用需求分配带宽；
- 快速故障切换；
- 做流量调度；
- 做容量规划；
- 快速部署新策略；
- 支持应用感知路由。

---

#### 17.2 traffic engineering 的作用

traffic engineering 指主动优化流量分布。

例如：

- 避免某些链路过载；
- 利用低利用率链路；
- 根据时区调度批量流量；
- 优先保障实时流量；
- 延迟非关键复制流量；
- 根据成本选择路径；
- 根据延迟选择路径；
- 根据丢包率选择路径。

例如：

```text
用户实时请求 → 低延迟路径
后台数据复制 → 低成本/低利用率路径
视频预分发 → 靠近用户的边缘节点
```

---

### 18. Internet peering edge

原文说：

> Cloud providers have also developed SDN-based Internet peering edge infrastructures. These infrastructures are designed to scale cost-effectively and to enable application-aware routing at Internet-peering scale.

云厂商不仅要连接自己的数据中心，还要连接公共 Internet。

这就需要 edge infrastructure。

---

#### 18.1 什么是 Internet peering？

Internet peering 指：

> 不同网络之间直接交换流量。

例如 Google 网络与 ISP 网络直接互联。

这样可以：

- 降低延迟；
- 提高吞吐；
- 减少中转成本；
- 改善用户体验；
- 控制路径质量。

---

#### 18.2 application-aware routing

在 Internet peering 规模做 application-aware routing，意味着网络可以根据应用需求选择出口路径。

例如：

- YouTube 视频流量选择靠近用户的 ISP；
- Search 请求选择低延迟路径；
- Drive 上传选择高吞吐路径；
- Ads 请求选择可靠路径；
- 内部复制选择低成本路径。

这需要：

- 应用层信息；
- 网络 telemetry；
- SDN 控制；
- BGP 策略；
- 流量测量；
- 自动化决策。

---

### 19. 高速部署新网络功能

原文说：

> These innovations have helped cloud providers improve the performance and reliability of their networks, and have also made it possible for them to deploy new networking features with high velocity.

SDN 和软件化网络让网络像软件系统一样快速迭代。

传统网络可能依赖：

- 手工配置；
- 设备 CLI；
- 厂商固件升级；
- 缓慢变更窗口。

SDN 网络可以：

- 集中下发策略；
- 快速实验；
- 灰度发布；
- 自动回滚；
- 实时监控；
- A/B testing；
- 快速修复。

这使得网络功能可以高速迭代。

---

### 20. 与前面章节的联系

---

#### 20.1 与 6.4.3 Clos 的联系

6.4.3 讲通用集群网络。

6.4.6 说明：

> 有些流量不适合放在通用 Clos 中，而应该走专用网络。

例如：

- 存储；
- AI 训练；
- 管理；
- WAN。

---

#### 20.2 与 6.4.4 OCS 的联系

OCS 可以用于：

- 数据中心 spine-less network；
- TPU pod 可重构互连；
- 动态 topology engineering。

专用加速器网络和 OCS 常常结合，用于：

- 大规模 AI 训练；
- 故障恢复；
- 拓扑定制；
- 增量部署。

---

#### 20.3 与 6.3 accelerators 的联系

6.3 讲 GPU/TPU。

6.4.6 进一步说明：

```text
加速器不只是芯片
还需要专用互连网络
```

例如：

- TPU ICI；
- GPU NVLink；
- inter-pod backend network；
- NCCL；
- collective communication。

---

#### 20.4 与 4.1.2 Colossus 的联系

原文提到：

> Google’s storage layer is accessed via Colossus RPCs.

这说明 WSC 存储不是传统 SAN，而是分布式存储服务。

存储流量通过 RPC 和数据中心网络访问，底层依赖：

- 网络；
- 复制；
- 纠删码；
- 调度；
- 安全；
- 监控。

---

### 21. 关键术语表

|术语|含义|
| ----------------------------| ----------------------------------------------|
|special-purpose network|专用网络|
|SAN|Storage Area Network，存储区域网络|
|Fibre Channel|传统存储网络协议|
|FCoE|Fibre Channel over Ethernet|
|iSCSI|SCSI over IP|
|NVMe|Non-Volatile Memory Express|
|NVMe-oF|NVMe over Fabrics|
|converged Ethernet|融合以太网|
|Colossus|Google 分布式存储系统|
|RPC|Remote Procedure Call|
|SRD|Scalable Reliable Datagram，AWS 自研传输协议|
|ML traffic|机器学习流量|
|ICI|Inter-Chip Interconnect，TPU 芯片间互连|
|NVLink|NVIDIA GPU 高速互连|
|shared-memory interconnect|共享内存式互连|
|pod|加速器集群单元|
|inter-pod network|pod 间网络|
|backend network|后端计算/训练网络|
|NIC|网络接口卡|
|WAN|Wide Area Network，广域网|
|SDN|Software-Defined Networking|
|traffic engineering|流量工程|
|submarine cable|海底电缆|
|Internet peering|互联网对等互联|
|edge infrastructure|边缘基础设施|
|application-aware routing|应用感知路由|

---

### 22. 可以用来检验理解的问题

---

#### 问题 1：为什么 WSC 要使用专用网络？

因为不同流量有不同需求。

把某些流量卸载到专用网络可以：

- 提高性能；
- 降低成本；
- 隔离故障；
- 优化协议；
- 提高安全性；
- 减少通用 fabric 压力。

---

#### 问题 2：SAN 是什么？

SAN 是 Storage Area Network，专门连接服务器和存储设备的网络。

传统 SAN 常使用 Fibre Channel，现在越来越多使用 Ethernet 和 NVMe-oF、iSCSI、FCoE 等协议。

---

#### 问题 3：为什么 WSC 中存储流量可能不使用传统 SAN 协议？

因为超大规模存储通常是分布式存储服务，而不是传统块存储阵列。

例如 Google 使用 Colossus RPC，AWS 使用 SRD over Ethernet。

这些协议更适合：

- 大规模；
- 多路径；
- 软件定义；
- 分布式复制；
- NIC offload；
- 高吞吐；
- 低延迟。

---

#### 问题 4：为什么 ML 流量成为数据中心网络的重要流量？

因为 GPU/TPU 计算能力极高，训练时需要大量芯片间通信，例如 all-reduce、all-gather、all-to-all。

每颗加速器可能需要数百 Gbps 带宽，因此 ML 流量成为大流量来源。

---

#### 问题 5：ICI/NVLink 为什么更像共享内存互连，而不是 Ethernet？

因为它们优化：

- 小块传输；
- 远程内存访问；
- DMA；
- collective communication；
- 低延迟；
- 高带宽；
- 紧耦合并行计算。

而 Ethernet 是通用包交换网络，适合更广泛的流量。

---

#### 问题 6：为什么大模型训练需要 inter-pod 网络？

因为单个加速器 pod 规模有限。

大训练任务可能跨越多个 pod，因此需要 pod 间高带宽网络，通常每节点数百 Gbps。

---

#### 问题 7：为什么加速器流量通常走单独网络？

因为 AI 训练流量对带宽、延迟、尾延迟和拥塞非常敏感。

单独网络可以：

- 隔离应用流量；
- 优化 collective communication；
- 提高训练 goodput；
- 降低干扰；
- 使用专门拥塞控制和路由。

---

#### 问题 8：云厂商为什么要建设私有 WAN？

因为私有 WAN 可以提供：

- 更可控性能；
- 更低延迟；
- 更高可靠性；
- 更好安全；
- 更低长期成本；
- 更强流量工程能力；
- 全球数据中心互联。

---

#### 问题 9：SDN 和 traffic engineering 在 WAN 中有什么作用？

SDN 提供集中控制和快速策略下发。

traffic engineering 根据链路利用率、延迟、成本、应用需求优化路径。

二者结合可以提高 WAN 性能、可靠性和利用率，并支持快速部署新网络功能。

---

### 23. 这一节可以整理成的精简笔记

```text
6.4.6 Special-purpose networks
6.4.7 WANs

1. 核心观点：
   网络可扩展性不仅靠更大的通用 Clos fabric，
   还可以通过把特定流量卸载到专用网络来实现。
   存储、AI 加速器、应用、管理、WAN 等流量
   可以分别走不同网络平面，以优化性能、成本、
   协议、隔离和故障域。

2. SAN：
   - Storage Area Network，存储区域网络；
   - 用于连接服务器和存储设备；
   - 如果存储流量是局部性的，
     可以构建较小规模网络以降低成本；
   - 历史上 SAN 常使用 Fibre Channel 而非 Ethernet。

3. 存储网络从 Fibre Channel 到 Ethernet：
   - Fibre Channel 低延迟、可靠，但成本高、生态封闭；
   - Ethernet 速度提升后逐渐成为主流；
   - FCoE、iSCSI、NVMe 等协议使 Ethernet
     可以提供传统 SAN 功能；
   - converged Ethernet 可同时承载数据和存储流量。

4. WSC 中的存储协议：
   - 超大规模 WSC 可能完全不用传统存储协议；
   - Google 存储层通过 Colossus RPC 访问；
   - AWS 使用 SRD，一种基于 Ethernet 的专有协议；
   - 这说明 WSC 存储是分布式服务，
     而不是传统块存储 SAN。

5. 流量结构变化：
   - 历史上存储流量主导数据中心网络；
   - 现在 ML 流量，GPU-GPU 或 TPU-TPU，
     成为另一大流量来源；
   - AI 训练产生大量加速器间通信。

6. 加速器带宽需求：
   - 加速器可达数百 TFLOPS；
   - 每芯片需要数百 Gbps 甚至更高互连带宽；
   - TPUv5 node：4.8 Tbps ICI 对应 459 TFLOPs BF16；
   - H100 GPU：7.2 TB/s NVLink 对应 2671 TFLOPs BF16；
   - 这些带宽由专用互连提供。

7. 加速器互连 vs Ethernet：
   - ICI/NVLink 专为小块传输和加速器通信优化；
   - 更像 shared-memory interconnect；
   - 支持低延迟、高带宽、远程内存访问、collective communication；
   - Ethernet 更通用，但适合跨节点/跨集群网络。

8. 加速器互连规模有限：
   - 2025 年最大 TPUv7 pod 为 9,216 chips；
   - 最大 NVLink pod 为 256 H100 GPUs；
   - 大训练任务需要跨多个 pod；
   - 因此需要数据中心网络支持 inter-pod 高带宽互连；
   - 每节点可能需要数百 Gbps。

9. 多网络平面：
   - accelerator-to-accelerator 流量通常走单独 inter-pod 网络；
   - host servers 通过自己的 NIC 连接数据中心 fabric；
   - application traffic 走通用 fabric；
   - 这样实现性能隔离、协议优化和故障隔离。

10. WAN：
   - 云厂商建设私有 WAN 连接全球数据中心；
   - Google 因 YouTube、Drive、Ads 等需求，
     网络规模比其他公有云大一个数量级；
   - 截至 2024 年，Google 拥有或共同拥有 31 条海底电缆；
   - WAN 需要处理巨大带宽和弹性流量需求。

11. WAN 的 SDN 和 traffic engineering：
   - 使用 SDN 集中控制和快速部署策略；
   - 使用 traffic engineering 优化路径、利用率、延迟和成本；
   - 云厂商还建设 SDN-based Internet peering edge；
   - 支持在 Internet-peering 规模做 application-aware routing。

12. 总结：
   WSC 网络不是单一通用 fabric，
   而是由多个专用和通用网络平面组成：
   存储网络、加速器互连、inter-pod 训练网络、
   应用网络、管理网络、WAN 和 edge。
   这种分层和专用化设计可以在性能、成本、
   可靠性、隔离性和可演进性之间取得平衡。
```

---

### 24. 如果考试或讨论中要回答这一节，可以这样说

> 6.4.6 和 6.4.7 讨论 WSC 网络中的专用网络和 WAN。核心思想是：网络可扩展性不仅依靠更大的通用 Clos fabric，还可以通过把特定流量卸载到专用网络来实现。
>
> 首先是存储网络。历史上，服务器通常通过 SAN 访问远程磁盘。SAN 是专门连接服务器和存储设备的网络，传统上常使用 Fibre Channel，而不是 Ethernet。如果存储流量具有局部性，即不是所有服务器都需要访问所有存储单元，那么可以构建较小规模的专用网络，从而降低成本。随着 Ethernet 速度提升，FCoE、iSCSI 和 NVMe 等协议使 Ethernet 可以提供传统 SAN 的功能，因此融合 Ethernet 网络越来越常见。但在超大规模 WSC 中，存储流量甚至可能完全绕过传统存储协议。例如 Google 的存储层通过 Colossus RPC 访问，AWS 使用基于 Ethernet 的专有协议 SRD。这说明 WSC 存储更像分布式存储服务，而不是传统块存储 SAN。
>
> 其次，ML 流量已经成为数据中心网络的重要流量来源。过去存储流量主导数据中心网络，但现在 GPU-GPU 和 TPU-TPU 通信产生巨大流量。由于加速器可以达到数百 TFLOPS，每颗芯片往往需要数百 Gbps 的互连带宽。例如 TPUv5 node 提供 4.8 Tbps ICI 带宽，对应 459 TFLOPs 的 16-bit 计算；H100 GPU 支持 7.2 TB/s NVLink 带宽，对应 2671 TFLOPs 的 16-bit 计算。这些互连不是普通 Ethernet，而是专为小块传输和加速器通信设计的专用网络，更像共享内存互连。
>
> 不过，专用加速器互连规模有限。到 2025 年，最大 TPUv7 pod 为 9,216 chips，最大 NVLink pod 为 256 H100 GPUs。大型训练任务往往需要更多加速器，因此需要数据中心网络支持多个 pod 之间的高带宽互连，每节点可能达到数百 Gbps。这个 inter-pod 网络通常也是单独网络，使加速器到加速器流量只走该网络。与此同时，连接加速器的服务器仍然有自己的 NIC，连接到通用数据中心 fabric，应用流量走该网络。这样就形成了多网络平面架构：加速器互连、训练后端网络、存储网络、应用网络和管理网络分别承担不同流量。
>
> 6.4.7 简要讨论 WAN。云厂商建设私有 WAN 来连接全球数据中心。由于 YouTube、Google Drive、Google Ads 等业务需求，Google 的网络规模比其他公有云大一个数量级。截至 2024 年，Google 拥有或共同拥有 31 条海底电缆。WAN 需要处理巨大带宽和弹性流量需求，因此广泛使用 SDN 和 traffic engineering 来优化性能。云厂商还建设了基于 SDN 的 Internet peering edge 基础设施，以成本高效地扩展，并在 Internet-peering 规模实现 application-aware routing。
>
> 总体而言，这两节的核心结论是：WSC 网络不是单一通用网络，而是由多个通用和专用网络平面组成的系统。存储、AI 加速器、应用、管理、WAN 和 edge 流量各有不同需求，通过专用网络和 SDN 流量工程可以在性能、成本、可靠性、隔离性和快速演进之间取得平衡。


**专栏导航**

- ← 上一篇：[6.4.5 Optics in warehouse-scale data centers](/posts/6-4-5-optics-in-warehouse-scale-data-centers/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[7.1 Software-defined servers →](/posts/7-1-software-defined-servers/)
