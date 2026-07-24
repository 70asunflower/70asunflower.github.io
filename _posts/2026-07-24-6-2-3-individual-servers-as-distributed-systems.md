---
title: "6.2.3 Individual servers as distributed systems"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-24
description: "《The Data Center as a Computer》AI 导读专栏正文：6.2.3 Individual servers as distributed systems。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：6.2.3 Individual servers as distributed systems。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 6.2.3 Individual servers as distributed systems

下面这一节 **6.2.3 Individual servers as distributed systems** 非常关键。它把前面对 server / rack 的硬件讨论进一步提升到一个新的抽象层：

> **现代服务器已经不是一台“单机”，而是一个由多个互不信任的计算域组成的“小型分布式系统”。**

如果说 6.2.1 讲的是“服务器里有什么硬件”，6.2.2 讲的是“服务器如何装进机架并接入电力/网络/冷却”，那么 6.2.3 讲的是：

> **这些硬件组件如何在安全、信任、管理和控制平面上被组织成一个可规模化运维的逻辑机器。**

---

# 1. 这一节的核心观点

原文开头说：

> In the past, server designs were “monoliths”, single node machines... with one main compute complex and managed by a single operating system.

过去服务器是 **monolith**，也就是“单体机器”：

```text
一台服务器
├── CPU
├── 内存
├── I/O
├── 存储
└── 一个操作系统统一管理
```

但今天不是这样。

原文继续说：

> systems today include multiple compute elements outside the primary CPU: management controllers, smart NICs, accelerators – each running their own operating systems.

现代服务器内部有很多“计算元素”：

- CPU host；
- BMC；
- SmartNIC / DPU；
- GPU / TPU / 其他加速器；
- 存储控制器；
- 电源管理控制器；
- 机架管理单元；
- 其他固件和嵌入式 OS。

它们各自可能运行自己的操作系统或固件栈。

因此，服务器变成了：

```text
一台“服务器”
├── host CPU / host OS
├── BMC OS / firmware
├── SmartNIC OS / firmware
├── accelerator firmware
├── storage controller firmware
├── power/thermal controller firmware
└── 多个信任域 / 控制域
```

所以原文的标题非常准确：

> **Individual servers as distributed systems**  
> 单台服务器本身就是分布式系统。

---

# 2. 从 monolith 到 multi-node / multi-brained server

这一节最重要的思想转变是：

> 服务器不再是一个由单一 OS 完全控制的硬件盒子，而是多个“脑”共同组成的系统。

可以把它理解成从：

```text
single-brained server
```

变成：

```text
multi-brained server
```

---

## 2.1 传统 monolith 服务器

传统服务器中，主机操作系统几乎管理一切：

- CPU 调度；
- 内存管理；
- 设备驱动；
- 文件系统；
- 网络栈；
- 存储；
- 风扇控制；
- 电源管理；
- 硬件监控。

这种设计的问题是：

1. **安全边界不清晰**  
   如果 host OS 被攻破，攻击者可能控制整个机器。
2. **管理复杂**  
   每新增一种硬件，host OS 都要增加驱动和管理逻辑。
3. **云场景不友好**  
   如果客户要 bare-metal，云厂商很难在不暴露管理权的情况下把机器交给客户。
4. **异构硬件难以抽象**  
   不同服务器有不同 NIC、GPU、SSD、BMC、电源模块，软件栈会越来越复杂。

---

## 2.2 现代 multi-node 服务器

现代服务器把很多功能从 host CPU 移出去：

- 系统管理移到 BMC；
- 网络虚拟化移到 SmartNIC / DPU；
- 存储处理可能移到存储控制器或 DPU；
- 加速器有自己的固件和控制栈；
- 安全信任根独立于 host OS；
- 机架级管理由 rack management unit 参与。

于是服务器内部变成多个节点：

```text
+--------------------------------------------------+
|                   server tray                    |
|                                                  |
|  host CPU node        BMC node       SmartNIC    |
|  host OS              BMC OS         NIC OS      |
|  workload             management     offload     |
|                                                  |
|  accelerator node     storage node   power node  |
|  accelerator FW       storage FW     power FW    |
+--------------------------------------------------+
```

这些节点之间通过总线、网络、RPC、telemetry、attestation 接口交互。

所以从系统视角看，它已经是分布式系统。

---

# 3. 为什么要把服务器拆成多个计算域？

原文说：

> This approach improves security and manageability, and also enables “bare-metal” servers where cloud customers have non-virtualized access to the CPU.

这里给出了三个关键收益：

1. security；
2. manageability；
3. bare-metal support。

我们逐个展开。

---

## 3.1 提高安全性

如果所有控制功能都在 host OS 中，那么 host OS 一旦被攻破，攻击者可能：

- 修改固件；
- 控制 BMC；
- 篡改启动链；
- 关闭安全日志；
- 访问管理网络；
- 持久化恶意代码。

把管理功能移到独立 arena 后，可以建立硬件级信任边界。

例如：

```text
host OS 被攻破
        ↓
不能直接修改 BMC firmware
不能直接修改 NIC firmware
不能直接篡改 Root-of-Trust
不能直接控制电源和风扇
```

这就是原文所说的：

> The OS that runs the computing workload cannot access or modify the OS that manages the system.

运行 workload 的 OS 不能访问或修改管理系统 OS。

这是一种非常重要的安全原则：

> **workload plane 和 management plane 必须分离。**

---

## 3.2 提高可管理性

超大规模数据中心中，运维不可能依赖人工登录每台机器。

需要：

- 远程开关机；
- 固件升级；
- 故障诊断；
- 传感器采集；
- 风扇控制；
- 电源监控；
- 安全证明；
- 自动修复；
- 资产发现；
- 配置管理。

这些功能如果都塞进 host OS，会出现问题：

- host 关机后无法管理；
- host OS 崩溃后无法诊断；
- 客户 OS 可能不受云厂商控制；
- 不同硬件需要不同驱动；
- 管理逻辑和 workload 逻辑耦合。

把管理功能移到 BMC、SmartNIC、rack manager 等独立节点后，可以实现：

```text
即使 host OS 崩溃，
BMC 仍然可以上报状态、重启机器、收集日志。
```

这对 WSC 运维至关重要。

---

## 3.3 支持 bare-metal 服务器

bare-metal server 指云客户直接获得物理 CPU，而不是虚拟机。

客户希望：

- 没有 hypervisor 开销；
- 直接控制 CPU；
- 直接访问某些设备；
- 更高性能；
- 更确定的安全边界。

但云厂商仍然需要：

- 管理机器；
- 接入网络；
- 接入存储；
- 监控硬件；
- 执行安全策略；
- 远程维护；
- 故障恢复；
- 计费与隔离。

解决办法是：

> 把云厂商需要的管理、网络、存储、安全功能卸载到独立硬件域，例如 SmartNIC / DPU / BMC。

这样客户可以使用 host CPU，而云厂商仍然可以通过独立控制域管理机器。

抽象来看：

```text
客户控制：
  host CPU
  host memory
  workload OS

云厂商控制：
  BMC
  SmartNIC
  attestation
  network fabric
  storage fabric
  power/thermal management
```

这就是现代 bare-metal 云服务器的基础。

---

# 4. Disaggregated designs：服务器变成“虚拟构造”

原文进一步说：

> Disaggregated designs further redefine the server as a virtual construct where system resources are configured as dynamically re-allocatable pools with resource slices multiplexed over a network of individual hardware components.

这句话非常值得细读。

它的意思是：

> 服务器不一定是一个物理盒子，而可以是一个逻辑组合体。

传统服务器：

```text
server = CPU + DRAM + SSD + NIC + GPU
         全部装在一个机箱里
```

disaggregated server：

```text
server = CPU slice
       + memory slice
       + storage slice
       + accelerator slice
       + network slice
       通过 PCIe / CXL / Ethernet 动态组合
```

也就是说，服务器可以不再物理拥有所有资源，而是从资源池中租用切片。

---

## 4.1 资源池化示例

原文举例：

> instead of physically containing a local SSD or GPU, the server may connect to a rack-level pool of such devices via PCIe or CXL, or even via Ethernet.

例如：

### 本地 SSD 变成 pooled SSD

传统：

```text
server tray
└── local SSD
```

disaggregated：

```text
server tray
   ↓ PCIe / NVMe-oF / Ethernet
rack-level SSD pool
```

### 本地 GPU 变成 pooled accelerator

传统：

```text
server tray
└── local GPU
```

disaggregated：

```text
server tray
   ↓ PCIe / CXL / fabric
rack-level GPU/accelerator pool
```

### 本地内存变成 pooled memory

传统：

```text
CPU
└── local DRAM
```

CXL 架构：

```text
CPU
├── local DRAM
└── CXL memory pool
```

---

## 4.2 disaggregation 的好处

### 1. 提高资源利用率

如果每台服务器都自带 GPU、SSD、内存，可能出现：

- 有些机器 GPU 空闲；
- 有些机器 SSD 空闲；
- 有些机器内存空闲；
- 有些机器 CPU 空闲。

资源池化后，可以按需分配。

---

### 2. 独立升级硬件

传统服务器中，CPU、内存、SSD、NIC 生命周期绑定。

disaggregation 后：

- SSD 池可以独立升级；
- GPU 池可以独立换代；
- 内存池可以独立扩容；
- 网络池可以独立演进。

这可以降低硬件迭代成本。

---

### 3. 减少资源碎片

例如某些 workload 需要：

- 高 CPU；
- 低存储；
- 高内存。

另一些 workload 需要：

- 高存储；
- 低 CPU；
- 高网络。

如果资源固定在某台服务器中，容易产生 stranded resources，即“闲置但无法被其他机器使用的资源”。

池化可以减少这种浪费。

---

### 4. 更灵活的服务器规格

服务器可以按需组合：

```text
small CPU + large memory
large CPU + small memory
large CPU + large accelerator
small CPU + large storage
```

而不是被固定硬件型号限制。

---

## 4.3 disaggregation 的挑战

但 disaggregation 不是免费的。

它引入很多新问题。

### 1. 延迟增加

本地 SSD / GPU / DRAM 通常延迟最低。

通过 PCIe fabric、CXL 或 Ethernet 访问会增加延迟。

例如：

```text
local DRAM      最低延迟
CXL memory      较高延迟
remote storage  更高延迟
```

因此需要分层设计。

---

### 2. 带宽和 QoS

多个服务器共享资源池时，会出现：

- 带宽竞争；
- 尾延迟；
- 噪声邻居；
- 隔离问题。

需要 QoS、调度、拥塞控制和监控。

---

### 3. 故障域变化

本地 SSD 故障通常只影响一台机器。

资源池故障可能影响多台机器。

因此需要：

- 副本；
- 纠删码；
- 多路径；
- 故障检测；
- 快速切换。

---

### 4. 安全边界更复杂

资源池中的设备可能被多个租户或 workload 使用。

需要：

- 设备隔离；
- I/O 虚拟化；
- 加密；
- 访问控制；
- 审计；
- attestation。

---

# 5. arenas：互不信任的抽象组件

原文中一个关键概念是：

> a server no longer is a set of hardware components contained in sheet metal, but a logical composition of mutually-distrusting abstract components, called arenas.

这句话非常重要。

它重新定义了服务器：

> 服务器不是一堆装在金属壳里的硬件，而是由多个互不信任的抽象组件组成的逻辑组合。

这些抽象组件叫 **arena**。

---

## 5.1 什么是 arena？

可以把 arena 理解为：

> 一个具有硬件信任边界、运行独立固件/OS、拥有独立 Root-of-Trust 的执行与管理域。

典型 arena 包括：

- host CPU arena；
- BMC arena；
- SmartNIC arena；
- accelerator arena；
- storage controller arena；
- power controller arena；
- rack manager arena。

每个 arena 都有自己的：

- firmware；
- OS 或 runtime；
- Root-of-Trust；
- attestation 机制；
- 管理接口；
- 安全边界。

---

## 5.2 mutually-distrusting：互不信任

“mutually-distrusting” 是零信任思想在硬件层面的体现。

它意味着：

> 一个 arena 不默认信任另一个 arena。

例如：

- host OS 不天然信任 BMC；
- BMC 不天然信任 host OS；
- SmartNIC 不天然信任 host；
- scheduler 不天然信任机器，除非 attestation 通过；
- 控制平面不天然信任固件，除非 RoT 提供证明。

这种设计的好处是：

```text
某个 arena 被攻破，
不一定能自动控制其他 arena。
```

---

## 5.3 machine 是 arena 的组合

原文说：

> A machine is the composition of one or more arenas.

也就是说：

```text
machine = arena 1 + arena 2 + ... + arena N
```

一台现代服务器可能由多个 arena 组成。

每个 arena 有明确边界：

```text
+----------------+
| arena          |
|                |
| firmware       |
| OS             |
| RoT            |
| attestation    |
| control APIs   |
+----------------+
```

---

## 5.4 arena 和 VM / container 的区别

这个概念容易和 VM、container 混淆。

可以这样区分：

|抽象|隔离层级|典型目标|
| -----------| ---------------------------| ----------------------------|
|process|操作系统内进程隔离|应用隔离|
|container|OS 级资源隔离|轻量应用部署|
|VM|hypervisor 级虚拟硬件隔离|多租户操作系统隔离|
|arena|硬件信任域/固件域隔离|管理、安全、信任、固件隔离|

arena 更接近硬件信任边界，而不是单纯的软件隔离。

---

# 6. 如何处理硬件异构性：把管理功能移出去

原文说：

> The best way to handle this hardware heterogeneity is to hide it from most of the system stack by moving management functions elsewhere.

这是现代 WSC 系统设计的重要原则：

> **不要让主机 OS 和上层软件直接面对所有硬件差异。**

而是把硬件差异封装到独立管理域中。

---

## 6.1 虚拟化卸载到独立卡

原文举例：

> the offload arenas discussed above move virtualization into a separate card, reducing or eliminating server-specific code.

例如 SmartNIC / DPU 可以承担：

- 虚拟交换；
- VXLAN / Geneve；
- 防火墙；
- 加密；
- 存储虚拟化；
- NVMe-oF；
- virtio offload；
- SR-IOV；
- 流量计量；
- 安全隔离。

这样 host CPU 不需要运行大量云厂商基础设施代码。

好处：

- 降低 host CPU 开销；
- 减少 server-specific code；
- 提高 bare-metal 可行性；
- 提高安全边界；
- 统一网络/存储控制平面。

---

## 6.2 BMC 承担服务器管理和监控

原文说：

> server management and monitoring, e.g., fan speed control, has moved to a separate card, called Baseboard Management Controller, or BMC.

BMC 可以负责：

- 风扇控制；
- 温度监控；
- 电压监控；
- 电源状态；
- 远程开关机；
- 固件更新；
- 日志收集；
- 远程控制台；
- 故障诊断。

这样即使 host OS 崩溃，BMC 仍可工作。

---

## 6.3 每个 arena 有自己的 firmware stack 和 RoT

原文：

> Each of these arenas contains its own firmware stack, protected by a hardware root of trust.

这意味着每个 arena 都要有：

- 安全启动；
- 固件度量；
- 可信根；
- 签名验证；
- 防回滚；
- attestation 能力。

这是大规模安全运维的基础。

---

# 7. control plane：用集中控制平面管理大量 arena

原文 Figure 6.11 后面说：

> The control plane design is similar to prior approaches, e.g., software-defined networking: we aim for a clear distinction between a small set of boundary-enforcing functions local to each arena, and a broader control plane function that manages the fleet as a whole.

这句话非常关键。

它说明 WSC 管理采用类似 SDN 的思想：

```text
本地：
  小型、快速、边界执行功能

中央：
  全局、策略、调度、监控、证明控制平面
```

---

## 7.1 本地 boundary-enforcing functions

每个 arena 本地需要执行一些强制边界功能，例如：

- 只接受授权控制命令；
- 验证控制平面身份；
- 执行访问控制；
- 提供 attestation；
- 上报 telemetry；
- 隔离 workload 和管理功能；
- 拒绝非法固件；
- 执行安全启动。

这些功能必须靠近硬件，因为它们是最后防线。

---

## 7.2 中央 control plane

中央控制平面负责：

- 机器发现；
- 资源调度；
- 固件策略；
- attestation；
- telemetry 聚合；
- 故障检测；
- 维修流程；
- 网络配置；
- 电源和冷却策略；
- 机器模型管理。

它管理整个 fleet，而不是单台机器。

---

## 7.3 为什么类似 SDN？

SDN 的核心思想是：

```text
data plane：交换机执行转发规则
control plane：控制器集中决策
```

在这里变成：

```text
arena local functions：执行硬件边界策略
fleet control plane：集中管理整个数据中心硬件信任与资源
```

两者共同点：

- 本地组件简单、快速、可强制执行；
- 中央控制平面有全局视图；
- 策略集中定义；
- 执行分布在各节点；
- 通过模型和 API 管理大规模系统。

---

# 8. machine / rack / network models：把机器知识从代码移到模型

原文说：

> we rely heavily on machine, rack, and network models to support the centralized control plane.

这是超大规模运维的关键工程实践。

---

## 8.1 为什么需要模型？

如果每种服务器配置都写专门代码，会出现：

- 代码爆炸；
- 新硬件上线慢；
- 测试成本高；
- 容易出错；
- 难以推理安全边界；
- 难以扩展到新代际硬件。

所以需要用模型描述硬件结构。

原文说：

> we use a modeling language that allows us to represent each element of the figure at multiple levels of abstraction, through entity-relationship graphs...

也就是用实体关系图表示：

- machine；
- arena；
- controller；
- RoT；
- firmware storage；
- NIC；
- BMC；
- rack；
- switch；
- power domain；
- failure domain；
- attestation domain。

---

## 8.2 reachability：可达性

原文：

> define reachability, which controller services can connect to which control nodes.

也就是：

```text
哪些控制服务可以连接哪些控制节点？
```

例如：

- scheduler 是否可以连接 BMC？
- attestation service 是否可以连接 SmartNIC controller？
- telemetry collector 是否可以连接 accelerator manager？
- 某个服务是否只能访问特定网络域？

reachability 是安全和网络隔离的一部分。

---

## 8.3 failure domains：故障域

failure domain 描述：

```text
一个组件故障会影响哪些机器或服务？
```

例如：

- 一个 ToR 故障影响一个机架；
- 一个 power shelf 故障影响一组服务器；
- 一个 rack manager 故障影响一个机架的管理；
- 一个 SmartNIC 故障影响一台机器的网络；
- 一个 accelerator tray 故障影响一个计算节点。

控制平面需要知道这些关系，才能做：

- 调度；
- 副本放置；
- 维修优先级；
- 故障隔离；
- 容量规划。

---

## 8.4 attestation domains：证明域

attestation domain 描述：

```text
哪个 Root-of-Trust 可以证明哪些可变固件存储元件？
```

例如：

- BMC RoT 证明 BMC firmware；
- NIC RoT 证明 NIC firmware；
- host RoT 证明 BIOS/UEFI；
- accelerator RoT 证明 accelerator firmware；
- DC-SCM RoT 证明相关管理固件。

这使 attestation 可以模块化。

---

## 8.5 把 per-machine knowledge 从代码移到模型

原文最后强调：

> moving per-machine knowledge from code to models

这非常重要。

传统做法：

```text
if machine_type == "server_v1":
    do_this()
elif machine_type == "server_v2":
    do_that()
...
```

模型驱动做法：

```text
machine model 描述：
  有哪些 arena？
  有哪些 RoT？
  哪些固件需要 attest？
  哪些控制器可达？
  哪些故障域相关？

控制平面根据模型统一处理。
```

好处：

- 新硬件上线更快；
- 减少特殊代码；
- 降低工程成本；
- 更容易验证安全性；
- 更容易扩展到 WSC 规模。

---

# 9. attestation：机器加入集群前的安全证明

原文后半部分重点讲 attestation。

这是现代 WSC 安全体系的核心。

---

## 9.1 为什么需要 attestation？

因为控制平面不能盲目相信一台机器。

机器可能存在：

- 固件被篡改；
- 安全启动失败；
- 旧版本漏洞固件；
- 被撤销策略；
- 硬件配置不一致；
- 恶意供应链组件；
- 错误升级状态。

所以需要证明：

> 这台机器当前固件和可信状态是否符合预期。

这就是 attestation。

---

## 9.2 为什么由 job scheduler 做 central attestation authority？

原文说：

> Because workloads should only run on machines with an attested state, we chose to use our fleet-wide job scheduler as the central attestation authority.

原因很直接：

> scheduler 决定 workload 能不能放到某台机器上。

如果机器没有通过 attestation，scheduler 就不应该把任务调度到它上面。

让 scheduler 作为 central attestation authority 有几个好处：

1. 调度和安全策略统一；
2. 避免 workload 被放到不可信机器；
3. 减少额外服务依赖；
4. 提高可用性；
5. 简化机器加入集群的流程。

---

# 10. attestation 的具体流程

原文描述了一个完整流程。

可以整理成下面步骤。

---

## 步骤 1：请求加入资源池

当 scheduler 被要求把一台新机器加入资源池时：

```text
scheduler receives request:
  add new machine to resource pool
```

---

## 步骤 2：向机器索取 signed attestation policy

原文：

> it asks the machine for its signed attestation policy.

机器返回一个经过签名的 attestation policy。

这个 policy 包含：

- 机器中有哪些 roots of trust；
- 期望从这些 RoT 看到哪些 attestation；
- 策略版本；
- 撤销 ID；
- CA 签名。

可以理解为：

```text
attestation policy =
{
  machine_id,
  RoT_list,
  expected_firmware_measurements,
  policy_version,
  revocation_id,
  CA_signature
}
```

---

## 步骤 3：验证 policy 签名

scheduler 首先验证：

```text
policy signature valid?
```

如果签名无效，拒绝机器。

这保证 policy 不是伪造的。

---

## 步骤 4：检查 revocation list

原文：

> checks the policy’s revocation ID against a revocation list.

如果 policy 已被撤销，拒绝机器。

这可以防止：

- 使用旧 policy；
- 使用被撤销固件版本；
- 使用已知漏洞配置；
- 回滚到不安全状态。

---

## 步骤 5：向各 arena controller 收集 attestation

如果 policy 有效，scheduler 向机器中的各个 arena controller 发 RPC：

```text
scheduler → arena controllers:
  give me attestation statements from your RoTs
```

每个 arena 的 RoT 会提供 attestation statement。

例如：

```text
BMC RoT:
  BMC firmware measurement = ...
  signature = ...

SmartNIC RoT:
  NIC firmware measurement = ...
  signature = ...

Host RoT:
  BIOS/UEFI measurement = ...
  signature = ...
```

---

## 步骤 6：比较 attestation 是否符合 policy

scheduler 检查：

```text
actual attestation statements
        ?
expected policy intent
```

如果全部匹配：

```text
machine is trusted
```

如果任何一个不匹配：

```text
machine is rejected
```

---

## 步骤 7：加入集群或拒绝

原文：

> If every attestation matches its policy intent, the scheduler adds the machine to the cluster and allows jobs to be scheduled on it.

流程可以画成：

```text
request add machine
        ↓
ask machine for signed policy
        ↓
verify policy signature
        ↓
check revocation list
        ↓
RPC to arena controllers
        ↓
collect RoT attestation statements
        ↓
compare with expected policy
        ↓
all match?
   yes → add machine to cluster
   no  → reject machine
```

---

# 11. 为什么 policy 存在机器本身？

原文说：

> To avoid having the scheduler depend on another service, which can undermine availability, we store the policy for a machine on the machine itself, cryptographically signed by the certificate authority.

这是一个很实际的系统设计选择。

---

## 11.1 如果把 policy 存在中央服务中

可能的问题：

- 中央 policy service 故障时，scheduler 无法验证机器；
- 网络分区时无法加入新机器；
- 可用性下降；
- scheduler 依赖额外服务。

---

## 11.2 把 policy 存在机器本身

优点：

- 机器自己可以出示 policy；
- scheduler 不依赖外部 policy 服务；
- 只要签名有效，就可信；
- 提高系统可用性。

但还需要：

- CA 签名，防止伪造；
- revocation list，防止旧/被撤销 policy 被接受。

这体现了一个原则：

> 安全性不一定要以牺牲可用性为代价，可以通过密码学和系统设计兼顾二者。

---

# 12. firmware upgrade / downgrade 与 policy 生成

原文：

> We generate a new policy and revoke older ones each time our management processes upgrade or downgrade the firmware for a machine...

这很重要。

每次固件变化，机器的可信状态也变化。

例如：

- BMC 固件升级；
- NIC 固件升级；
- BIOS 更新；
- accelerator 固件更新；
- 固件降级修复 bug。

因此需要：

```text
new firmware state
        ↓
new attestation policy
        ↓
old policy revoked
```

---

## 12.1 为什么要撤销旧 policy？

因为旧 policy 可能对应：

- 漏洞固件；
- 错误配置；
- 被攻破版本；
- 不再允许的状态。

如果不撤销，攻击者可能试图让机器回滚到旧状态。

---

## 12.2 为什么 downgrade 也要生成新 policy？

有时候固件降级是合法运维操作，例如：

- 新版本有 bug；
- 性能回退；
- 兼容性问题；
- 安全补丁需要回滚。

但 downgrade 必须受控。

所以系统会：

- 根据机器模型判断是否允许；
- 生成新的合法 policy；
- 撤销旧 policy；
- 由 scheduler 重新验证。

---

# 13. 这一节体现的工程收益

原文最后总结：

> By constraining our hardware designs to meet the arena definition, and moving per-machine knowledge from code to models, we have been able to simplify reasoning about hardware trust, scale management at WSC scale to increasing server complexity, and greatly reduce the software engineering cost and delays of introducing new server configurations.

可以拆成三个收益。

---

## 13.1 简化硬件信任推理

如果每台机器都是特殊硬件组合，安全团队很难回答：

- 哪些固件可信？
- 哪个 RoT 证明哪个组件？
- 哪些边界必须强制执行？
- 哪些组件可以被 host 访问？
- 哪些故障会影响安全域？

arena 化之后，问题变成：

```text
机器由哪些 arena 组成？
每个 arena 的 RoT 是什么？
每个 arena 的 policy 是什么？
```

信任推理变得模块化。

---

## 13.2 在 WSC 规模管理复杂服务器

随着服务器越来越复杂：

- 更多加速器；
- 更多固件；
- 更多 SmartNIC；
- 更多 CXL 设备；
- 更多电源和冷却传感器；
- 更多管理控制器。

如果靠人工和专用代码，无法扩展。

通过：

- arena；
- RoT；
- attestation；
- model；
- control plane；

可以把复杂硬件纳入统一管理体系。

---

## 13.3 降低新服务器配置上线成本

新硬件上线通常需要：

- 驱动；
- 固件；
- 管理接口；
- 监控；
- 安全验证；
- 调度适配；
- 运维脚本；
- 故障处理。

如果每种新配置都要改大量代码，上线会很慢。

模型驱动后：

```text
新硬件 = 新 model + 符合 arena 规范
```

而不是：

```text
新硬件 = 大量新代码 + 大量特殊逻辑
```

这显著降低工程成本和延迟。

---

# 14. 与 6.2.1、6.2.2 的联系

这一节不是孤立的安全讨论，而是前两节的自然延伸。

---

## 14.1 与 6.2.1 的联系

6.2.1 提到：

- BMC；
- DC-SCM；
- Root-of-Trust；
- accelerator；
- NIC；
- PCIe；
- CXL；
- per-core DVFS；
- server tray。

这些在 6.2.3 中都变成了 arena 或资源池的一部分。

例如：

|6.2.1 概念|6.2.3 抽象|
| -------------| -------------------------------------|
|BMC|management arena|
|DC-SCM|RoT / management arena|
|SmartNIC|offload arena|
|GPU/TPU|accelerator arena / pooled resource|
|PCIe/CXL|disaggregation fabric|
|server tray|multi-arena machine|
|host CPU|workload arena|

---

## 14.2 与 6.2.2 的联系

6.2.2 提到：

- rack；
- ToR；
- rack management unit；
- power shelf；
- battery backup；
- data center fabric；
- accelerator rack；
- pod / clique。

这些在 6.2.3 中进入 control plane 和 model。

例如：

|6.2.2 概念|6.2.3 抽象|
| ----------------------| ------------------------------------|
|rack|failure domain / management domain|
|ToR|network reachability domain|
|rack management unit|control node / telemetry source|
|power shelf|power failure domain|
|data center fabric|control/data reachability|
|accelerator rack|high-bandwidth arena group / pod|
|OCP|标准化 arena/RoT/管理接口|

---

# 15. 读 Figure 6.9、6.10、6.11 的建议

---

## 15.1 Figure 6.9：服务器演化为 multi-node machines

这张图应该对比：

### Figure 6.9(a) monolith

```text
single CPU complex
single OS
all devices under host control
```

### Figure 6.9(b) multi-node

```text
host CPU
+ management controller
+ SmartNIC
+ accelerator
+ storage controller
+ other OS/firmware stacks
```

看这张图时要问：

- 哪些组件有独立 OS？
- 哪些组件有独立固件？
- 哪些组件与 host OS 隔离？
- 哪些组件通过总线或网络通信？

---

## 15.2 Figure 6.10：single-node vs multi-node multi-brained system

这张图强调：

```text
管理功能从 host 移出去
```

重点看：

- host OS 是否还管理风扇？
- 是否还管理网络虚拟化？
- 是否还管理存储虚拟化？
- BMC / SmartNIC / DPU 承担哪些功能？
- host 是否只运行 workload？

---

## 15.3 Figure 6.11：multi-arena architecture 和 control plane

这张图最复杂，重点看：

1. **粗虚线：arena / hardware trust boundary**

   - 每个 arena 是独立信任域；
   - 每个 arena 有自己的 RoT。
2. **control plane 与 node 的交互**

   - telemetry；
   - attestation；
   - scheduling；
   - firmware policy；
   - reachability。
3. **machine model**

   - 哪些 firmware 需要 attest；
   - 哪些 RoT 证明哪些 firmware；
   - 哪些 controller 可被哪些服务访问。
4. **attestation flow**

   - scheduler 请求 policy；
   - 验证签名；
   - 检查撤销；
   - 收集 RoT attestation；
   - 判断是否加入集群。

---

# 16. 关键术语表

|术语|含义|
| -----------------------------| ------------------------------------|
|monolith server|单体服务器，由单一 OS 管理|
|multi-node machine|内部包含多个计算节点的机器|
|multi-brained system|多个控制器/OS 共同管理的系统|
|management controller|管理控制器|
|SmartNIC|智能网卡，可承担网络/存储/安全卸载|
|DPU|Data Processing Unit，数据处理器|
|accelerator|加速器，如 GPU/TPU/VCU|
|bare-metal server|客户直接访问物理 CPU 的服务器|
|disaggregation|资源解耦/池化|
|resource pool|资源池|
|resource slice|资源切片|
|PCIe|高速总线|
|CXL|Compute Express Link|
|Ethernet|以太网，可用于存储/网络/管理|
|arena|硬件信任域/抽象管理域|
|trust domain|信任域|
|Root-of-Trust, RoT|可信根|
|attestation|远程证明/状态证明|
|attestation policy|证明策略|
|revocation list|撤销列表|
|control plane|控制平面|
|boundary-enforcing function|本地边界强制功能|
|machine model|机器模型|
|entity-relationship graph|实体关系图|
|reachability|可达性|
|failure domain|故障域|
|attestation domain|证明域|
|fleet|整个服务器集群|
|job scheduler|作业调度器|
|OCP|Open Compute Project|

---

# 17. 容易误解的几个点

---

## 误解 1：服务器变成分布式系统只是硬件变复杂了

不只是硬件复杂。

更重要的是：

- 安全边界变了；
- 管理平面变了；
- 信任模型变了；
- 控制平面变了；
- 软件栈变成多固件/多 OS 协同。

---

## 误解 2：bare-metal 就是云厂商完全不管机器

不是。

bare-metal 只是客户直接控制 host CPU。

云厂商仍然需要管理：

- BMC；
- SmartNIC；
- 网络；
- 存储接入；
- 电源；
- 冷却；
- 安全；
- attestation；
- 故障恢复。

---

## 误解 3：disaggregation 一定更好

不一定。

它能提高利用率和灵活性，但会增加：

- 延迟；
- 网络依赖；
- QoS 难度；
- 故障域复杂度；
- 安全复杂度。

是否 disaggregate 要看 workload。

---

## 误解 4：attestation 只是安全团队的事

不是。

在 WSC 中，attestation 直接影响调度：

```text
机器不可信 → scheduler 不调度 workload
```

所以它是系统可用性和安全性共同关注的问题。

---

## 误解 5：model 只是文档

不是。

这里的 model 是控制平面运行所依赖的形式化描述。

它影响：

- attestation；
- reachability；
- failure domain；
- scheduling；
- firmware policy；
- 新硬件上线流程。

---

# 18. 可以用来深入思考的问题

---

## 问题 1：为什么说现代服务器本身是分布式系统？

因为它内部包含多个独立计算域：

- host CPU；
- BMC；
- SmartNIC；
- accelerator；
- storage controller；
- power controller。

它们各自运行 OS/firmware，通过网络或总线通信，并有独立信任边界。

---

## 问题 2：arena 的核心作用是什么？

arena 把服务器拆成多个互不信任的硬件信任域。

每个 arena：

- 有自己的 OS/firmware；
- 有自己的 RoT；
- 可独立 attestation；
- 与其他 arena 隔离。

这提高了安全性和可管理性。

---

## 问题 3：为什么 bare-metal 云需要 SmartNIC / DPU？

因为客户要直接控制 host CPU，但云厂商仍需要管理网络、存储、安全和监控。

SmartNIC / DPU 可以承担这些功能，而不占用 host CPU，也不让客户完全控制云基础设施。

---

## 问题 4：disaggregated server 和传统 server 的区别是什么？

传统 server：

```text
资源物理绑定在一台机器中
```

disaggregated server：

```text
资源池化，按需切片，通过 PCIe/CXL/Ethernet 组合
```

---

## 问题 5：为什么 scheduler 要负责 attestation？

因为 scheduler 决定 workload 是否能运行在某台机器上。

如果机器未通过 attestation，scheduler 不应把任务调度到该机器。

---

## 问题 6：为什么 attestation policy 存在机器本身？

为了避免 scheduler 依赖额外服务，提高可用性。

机器可以直接出示经过 CA 签名的 policy，scheduler 只需验证签名和撤销状态。

---

## 问题 7：为什么要把 per-machine knowledge 从代码移到 model？

因为 WSC 中硬件配置太多。

如果每种配置都写特殊代码，会导致：

- 工程成本高；
- 上线慢；
- 容易出错；
- 难以扩展。

模型驱动可以统一描述机器结构、信任关系、故障域和证明域。

---

# 19. 这一节的深层设计哲学

这一节背后有几条非常重要的系统设计哲学。

---

## 19.1 零信任硬件化

不是默认相信 host OS，而是：

```text
每个 arena 都需要被证明；
每个固件都需要可信根；
每个机器加入集群都需要 attestation。
```

---

## 19.2 管理平面与数据平面分离

workload 运行在数据平面。

管理、监控、安全、证明运行在独立管理平面。

这样即使 workload OS 被攻破，管理平面仍可保持一定独立性。

---

## 19.3 用抽象对抗硬件复杂性

硬件越来越复杂：

- 多 CPU；
- 多加速器；
- 多 SmartNIC；
- 多 CXL 设备；
- 多固件；
- 多电源域。

解决办法不是让每个软件都理解所有硬件，而是：

```text
arena 抽象
+ machine model
+ control plane
+ attestation
```

---

## 19.4 用模型驱动规模化

WSC 规模下，靠人工和专用脚本不可行。

必须用：

- 机器模型；
- 机架模型；
- 网络模型；
- 故障域模型；
- 证明域模型；
- 策略模型。

这样才能把复杂硬件变成可管理系统。

---

# 20. 这一节可以整理成的精简笔记

```text
6.2.3 Individual servers as distributed systems

1. 核心问题：
   现代服务器不再是单一 OS 管理的 monolith，
   而是由多个计算域、固件栈和信任域组成的分布式系统。

2. 传统服务器：
   - 单节点；
   - 一个主 CPU complex；
   - 一个 OS 管理大部分硬件；
   - 安全边界和管理边界不清晰。

3. 现代服务器：
   - 包含 host CPU、BMC、SmartNIC、accelerator、
     storage controller、power controller 等多个计算元素；
   - 每个元素可能运行自己的 OS 或 firmware；
   - 服务器成为 multi-node / multi-brained system。

4. 多计算域的好处：
   - 提高安全性：workload OS 不能直接修改管理 OS；
   - 提高可管理性：BMC/SmartNIC 可独立监控和管理；
   - 支持 bare-metal：客户使用 host CPU，
     云厂商仍可通过独立控制域管理机器。

5. Disaggregation：
   - 服务器从物理盒子变成逻辑构造；
   - CPU、memory、SSD、GPU、NIC 等资源可池化；
   - 资源切片通过 PCIe、CXL 或 Ethernet 复用；
   - 优点是提高利用率、灵活性和独立升级能力；
   - 挑战是延迟、带宽、QoS、故障域和安全隔离。

6. arenas：
   - server 是多个 mutually-distrusting abstract components 的组合；
   - 这些组件叫 arena；
   - 每个 arena 是硬件信任边界；
   - 每个 arena 有自己的 OS/firmware 和 Root-of-Trust；
   - machine 是一个或多个 arenas 的组合。

7. 安全模型：
   - 运行 workload 的 OS 不能访问或修改管理系统 OS；
   - 每个 arena 不默认信任其他 arena；
   - 每个 arena 的 firmware stack 由 hardware RoT 保护；
   - 通过 attestation 验证固件和配置状态。

8. 处理硬件异构性的方法：
   - 不让上层软件直接面对所有硬件差异；
   - 把管理功能移到独立 arena；
   - 虚拟化可卸载到 SmartNIC/DPU；
   - 风扇、电源、温度等管理移到 BMC；
   - 减少 server-specific code。

9. control plane 设计：
   - 类似 SDN；
   - 每个 arena 本地有 boundary-enforcing functions；
   - 中央 control plane 管理整个 fleet；
   - 管理 telemetry、attestation、scheduling、firmware policy 等。

10. machine / rack / network models：
   - 使用建模语言和 entity-relationship graphs；
   - 表示 machine、arena、controller、RoT、firmware、
     rack、switch 等元素；
   - 定义 reachability、failure domains、attestation domains；
   - 把 per-machine knowledge 从代码移到模型。

11. attestation 流程：
   - scheduler 被要求加入新机器；
   - scheduler 向机器请求 signed attestation policy；
   - policy 包含 RoT 列表和期望的 attestation；
   - scheduler 验证 policy 签名；
   - 检查 revocation ID；
   - 向各 arena controller 收集 RoT attestation statements；
   - 如果所有 attestation 符合 policy，机器加入集群；
   - 否则拒绝。

12. policy 存储设计：
   - policy 存在机器本身；
   - 由 CA 签名；
   - 避免 scheduler 依赖额外服务；
   - 提高可用性；
   - 通过 revocation list 防止旧或被撤销 policy 被接受。

13. firmware upgrade/downgrade：
   - 每次固件升级或降级都生成新 policy；
   - 旧 policy 被撤销；
   - 保证机器可信状态与当前固件一致；
   - 防止非法回滚或漏洞固件重新进入集群。

14. 工程收益：
   - 简化硬件信任推理；
   - 在 WSC 规模管理复杂服务器；
   - 降低新服务器配置的软件开发成本；
   - 缩短新硬件上线延迟；
   - 提高安全性和可运维性。

15. 总结：
   现代服务器不是“铁皮里的硬件集合”，
   而是由多个互不信任的 arena 组成、
   由 control plane 和 machine model 统一管理、
   通过 RoT 和 attestation 建立信任的分布式系统。
```

---

# 21. 如果考试或讨论中要回答这一节，可以这样说

> 6.2.3 节讨论的是现代服务器如何从传统的单体机器演变成“作为分布式系统的服务器”。过去服务器通常是一个 monolith，由一个主 CPU 和单一操作系统管理大部分硬件。但今天的服务器内部包含多个独立计算元素，例如 host CPU、BMC、SmartNIC、DPU、加速器、存储控制器和电源管理控制器。它们各自运行自己的操作系统或固件栈，因此服务器本身已经是一个多节点、多信任域的分布式系统。
>
> 这种设计有三个主要好处。第一是提高安全性：运行用户 workload 的 OS 不能直接访问或修改管理系统的 OS，BMC、SmartNIC 和 Root-of-Trust 可以形成独立安全边界。第二是提高可管理性：即使 host OS 崩溃，BMC 或其他管理控制器仍然可以远程监控、重启、收集日志和更新固件。第三是支持 bare-metal 云服务：客户可以直接使用物理 CPU，而云厂商仍然可以通过独立管理域控制网络、存储、安全和监控。
>
> 原文进一步提出 disaggregated design。服务器不再必须是一个物理盒子，而可以是一个逻辑构造。CPU、内存、SSD、GPU 等资源可以被池化，服务器通过 PCIe、CXL 或 Ethernet 按需连接资源切片。这样能提高资源利用率和灵活性，但也引入延迟、QoS、故障域和安全隔离等新问题。
>
> 为了管理这种复杂性，原文引入 arena 概念。arena 是互不信任的抽象组件，每个 arena 都有自己的 OS/firmware 和 hardware Root-of-Trust。机器就是一个或多个 arena 的组合。这样可以把服务器拆成多个硬件信任域，使安全推理模块化。处理硬件异构性的最好方式不是让主机 OS 面对所有差异，而是把管理功能移到独立 arena，例如把虚拟化卸载到 SmartNIC/DPU，把风扇和电源管理交给 BMC。
>
> 在更大规模上，系统采用类似 SDN 的控制平面设计。每个 arena 本地只保留少量 boundary-enforcing functions，而中央 control plane 负责管理整个 fleet。为了支持这一点，系统使用 machine、rack 和 network models，通过实体关系图描述 reachability、failure domains 和 attestation domains。这样可以把 per-machine knowledge 从代码移到模型，减少新硬件上线时的工程成本。
>
> 原文最后用 attestation 作为例子。因为 workload 只能运行在可信机器上，fleet-wide job scheduler 被用作中央 attestation authority。当新机器要加入资源池时，scheduler 向机器请求签名过的 attestation policy。policy 包含机器中的 RoT 列表和期望的 attestation。scheduler 验证 policy 签名，并检查它是否被撤销。如果 policy 有效，scheduler 再向各个 arena controller 收集 RoT 提供的 attestation statements。只有所有 attestation 都符合 policy，机器才会被加入集群并允许调度任务。为了避免 scheduler 依赖额外服务，policy 存储在机器本身，并由 CA 签名。
>
> 总体来说，这一节的核心结论是：现代服务器不再是一个简单的硬件盒子，而是由多个互不信任的 arena 组成、通过 control plane、machine model、Root-of-Trust 和 attestation 统一管理的分布式系统。这种设计使 WSC 能够在服务器复杂度不断增加的情况下，仍然保持安全性、可管理性、可扩展性和较低的工程成本。


**专栏导航**

- ← 上一篇：[6.2.2 Hardware racks](/posts/6-2-2-hardware-racks/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[6.3 Accelerators and custom silicon →](/posts/6-3-accelerators-and-custom-silicon/)
