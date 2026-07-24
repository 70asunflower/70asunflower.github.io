---
title: "5.1 Data center infrastructure basics"
author: Fu Qilin
categories: [分布式计算]
tags: [distributed-computing, datacenter, wsc, ai-infra]
date: 2026-07-23
description: "《The Data Center as a Computer》AI 导读专栏正文：5.1 Data center infrastructure basics。"
excerpt: "《The Data Center as a Computer》AI 导读专栏正文：5.1 Data center infrastructure basics。"
---
<!-- markdownlint-disable MD013 MD025 MD033 -->
> 📌 本篇是 **《The Data Center as a Computer》AI 导读** 栏目的正文。
> ← [返回栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
>
> 说明：本栏目正文内容由 AI 根据原书原文生成，请自行甄别内容真实性。

## 5.1 Data center infrastructure basics

下面我结合你提供的原文，把 **5.1 Data center infrastructure basics** 这一节读厚。

这一节是第 5 章“数据中心基础设施”的开头，它的作用是把视角从“服务器、软件、调度系统”进一步拉回到：

> 数据中心首先是一个物理设施。  
> 它最核心的任务不是“运行代码”，而是：  
> **把电送进来，把热带出去，并保证设备安全、稳定、持续运行。**

---

### 一、这一节的核心观点：数据中心本质上是一台“供电和散热机器”

原文一开始说：

> Internet and cloud services run on a planet-scale computer with workloads distributed across multiple data center buildings around the world.

这句话把互联网和云服务描述成一台：

```text
planet-scale computer
行星级计算机
```

但这台行星级计算机并不是一台抽象的机器，它由很多具体建筑组成：

```text
data center buildings
数据中心建筑
```

这些建筑里面放着：

```text
计算设备
存储设备
网络设备
供电系统
冷却系统
安防系统
运维设施
```

原文随后点出了数据中心的本质：

> The main function of the buildings is to deliver the utilities needed by equipment and personnel there: power, cooling, shelter, and security.

也就是说，数据中心建筑的主要功能不是“计算”，而是提供基础设施服务：

```text
power     供电
cooling   冷却
shelter   遮蔽和物理环境
security  安全
```

服务器、存储、交换机当然重要，但它们是“被承载”的设备。

建筑本身的任务是：

```text
让 IT 设备能够持续、稳定、安全地运行。
```

---

### 二、为什么原文说数据中心“几乎没有做功”？

原文有一句很有意思：

> By classic physics definitions, there is little work produced at the data center. Other than some departing photons, all of the energy consumed is converted into heat.

这句话初看有点反直觉。

我们通常认为数据中心“做了很多工作”：

```text
处理搜索请求；
训练大模型；
存储照片；
播放视频；
运行数据库；
执行金融交易。
```

但原文说的是经典物理意义上的 “work”。

在物理学里，机械功通常意味着：

```text
力使物体发生位移
```

例如：

```text
起重机吊起货物
汽车推动车身前进
电机转动轮子
```

而数据中心里，大部分电能最终并没有转化为机械功，而是转化为：

```text
热
```

服务器计算时消耗电能：

```text
CPU/GPU/内存/磁盘/网卡 消耗电力
```

这些电力最终几乎都变成热量：

```text
芯片发热
电源发热
风扇发热
磁盘发热
光模块发热
交换机发热
```

唯一离开数据中心的能量形式之一是：

```text
光子
```

也就是光纤中传输的光信号。

但这些光子最终也会在远端设备里被吸收，转化为电信号和热量。

所以从能量角度看：

```text
输入：电能
输出：热量 + 极少量离开的光信号
```

这就是原文想强调的：

> 数据中心从物理上看，主要是一台把电能转换成热能的机器。

---

### 三、这句话的深层含义：数据中心设计围绕“电”和“热”

原文紧接着说：

> Delivering input energy and subsequently removing waste heat are at the heart of the data center’s design and drive the vast majority of non-computing costs.

这句话是整节的纲领。

可以拆成两件事：

```text
1. Delivering input energy
   把足够多、足够稳定、足够安全的电力送进来。

2. Removing waste heat
   把设备产生的热量持续带走。
```

这两件事决定了数据中心的：

```text
建筑设计
成本结构
选址
电力系统
冷却系统
运维复杂度
能效指标
可靠性
扩展能力
```

也就是说，数据中心不是“盖一栋楼，放进去服务器”这么简单。

真正困难的是：

```text
如何长期稳定地提供几十 MW 甚至上百 MW 电力？
如何把这些电力产生的热量高效排走？
如何在故障时不中断？
如何降低 PUE？
如何控制建设和运营成本？
```

---

### 四、数据中心成本为什么用 “$/W” 衡量？

原文说：

> Data center construction costs are roughly proportional to the amount of power delivered and typically run in the range of $5–20 per watt.

这是一个非常重要的工程经济指标。

---

#### 1. 为什么成本与功率成正比？

因为数据中心里大量基础设施都围绕功率规模配置。

如果你要提供：

```text
1 MW IT power
```

你需要的不只是服务器，还包括：

```text
变压器
配电柜
UPS
电池
发电机
燃油储备
电缆
母线
PDU
冷却水系统
冷水机组
冷却塔
水泵
风管
机柜
消防系统
安防系统
监控系统
```

这些设施的规模都取决于：

```text
要供多少电？
要排多少热？
```

所以数据中心建设成本常按每瓦特美元计算：

```text
$/W
```

---

#### 2. $5–20/W 是什么概念？

假设建设成本是：

```text
$10/W
```

如果数据中心 critical power 是：

```text
100 MW
```

那么建设成本大约是：

```text
100,000,000 W × $10/W = $1,000,000,000
```

也就是 10 亿美元。

如果成本是：

```text
$5/W
```

则是：

```text
5 亿美元
```

如果是：

```text
$20/W
```

则是：

```text
20 亿美元
```

所以原文说：

> varying considerably depending on size, location, and design.

影响成本的因素包括：

```text
土地价格
电力接入成本
当地气候
冷却方式
冗余等级
建筑规模
网络接入
施工成本
法规要求
灾害风险
水资源条件
税收政策
```

---

#### 3. 为什么这个指标重要？

因为它把数据中心从“IT 设备问题”变成了“基础设施经济问题”。

例如：

```text
同样 100 MW，
如果建设成本从 $12/W 降到 $8/W，
就节省 4 亿美元。
```

这也是为什么超大规模云厂商极其重视：

```text
标准化设计
模块化建设
自研供电
自研冷却
自研服务器
自研芯片
能效优化
选址优化
```

---

### 五、Planet to campuses to buildings：行星级计算机的层级结构

原文标题是：

> Planet to campuses to buildings

这其实给出了云基础设施的空间层级。

可以理解为：

```text
Planet
  └── Regions
        └── Campuses
              └── Buildings
                    └── Server halls
                          └── Rows / Racks
                                └── Servers
```

---

#### 1. Planet：全球分布

大型互联网和云服务不是运行在单个数据中心里，而是分布在全球：

```text
北美
南美
欧洲
亚洲
中东
澳洲
```

这样做的目的包括：

```text
靠近用户，降低延迟；
容灾，避免单点故障；
合规，满足数据本地化要求；
利用不同地区电力和网络资源；
平衡负载；
提高可用性。
```

---

#### 2. Campus：数据中心园区

一个 campus 可能包含多栋数据中心建筑。

例如：

```text
Building A
Building B
Building C
变电站
冷却中心
网络楼
办公区
安保设施
```

多个建筑可以共享：

```text
电力入口
冷却设施
网络骨干
安防系统
运维人员
备件仓库
```

---

#### 3. Building：单栋数据中心建筑

每栋建筑里有：

```text
服务器大厅
电力分配系统
冷却系统
网络区域
运维区域
安防区域
```

原文后面详细展开了这些组件。

---

### 六、如何理解数据中心规模：critical power 是关键指标

原文说：

> Data center sizes vary widely and are commonly described in terms of critical power, the total power that can be continuously supplied to IT equipment.

这里有一个非常重要的概念：

```text
critical power
关键功率
```

---

#### 1. 什么是 critical power？

critical power 指的是：

> 可以持续供给 IT 设备的总功率。

注意，它不是：

```text
建筑总面积
机柜数量
服务器数量
网络带宽
```

而是：

```text
能长期稳定给 IT 设备用多少电。
```

例如：

```text
1 MW critical power
10 MW critical power
100 MW critical power
```

---

#### 2. 为什么用功率而不是面积衡量规模？

因为数据中心的核心限制通常是电力和冷却，而不是地板面积。

同样 10,000 平方米的数据中心，如果功率密度不同，规模差异很大。

例如：

```text
低密度机房：
  每机柜 5 kW

高密度机房：
  每机柜 30 kW

AI GPU 机房：
  每机柜 50 kW 甚至更高
```

同样面积下，高功率密度机房需要更强的：

```text
供电
冷却
配电
气流管理
```

所以用 critical power 比用面积更能反映真实规模。

---

#### 3. 不同类型数据中心的功率规模

原文给了一个很好的对比。

---

##### 传统企业数据中心

原文说：

> Traditional enterprise servers were housed in data centers smaller than 5,000 sq ft and with less than 1 MW of critical power.

也就是：

```text
面积 < 5,000 sq ft
约 < 450 平方米
critical power < 1 MW
```

这类数据中心通常服务于单个企业：

```text
公司内部邮件系统
内部数据库
ERP
文件服务
小型虚拟化集群
```

---

##### Colocation 数据中心

原文说：

> Commercial data centers built to host servers from multiple companies are larger, and can support a critical load of tens of megawatts.

Colocation，也叫托管数据中心。

它的特点是：

```text
多家公司租用机柜或机房空间；
数据中心提供电力、冷却、网络、物理安全；
客户自己带服务器或租用设备。
```

规模通常是：

```text
几十 MW
```

例如：

```text
10 MW
30 MW
50 MW
```

---

##### 大型云提供商数据中心

原文说：

> Data centers of large cloud providers are similar, though often larger than colos.

大型云厂商，例如：

```text
Google
AWS
Microsoft
Meta
```

它们的数据中心通常更大，而且很多会组成 campus。

---

##### WSC 数据中心园区

原文说：

> The critical power of WSC data center campuses are often above 100 MW.

也就是说，warehouse-scale computing 的园区级 critical power 常常超过：

```text
100 MW
```

100 MW 是什么概念？

粗略估算，如果一台服务器平均功耗是 500 W：

```text
100 MW / 500 W = 200,000 台服务器
```

如果平均功耗是 1 kW：

```text
100 MW / 1 kW = 100,000 台服务器
```

如果包括存储、网络、冗余、冷却等，实际数量会更复杂。

但可以看出：

```text
100 MW 级别意味着数十万台设备级别的规模。
```

---

### 七、数据中心建筑的基本组成

原文第二段开始讲数据中心的物理组成。

可以把它拆成三大区域：

```text
1. 电力区域
2. 冷却区域
3. IT 区域
```

再加上：

```text
网络区域
运维区域
安防区域
管理网络区域
```

---

### 八、机械区：冷却系统所在地

原文说：

> A mechanical yard hosts the cooling systems, such as cooling towers and chillers.

mechanical yard，机械区，或者叫 central utility building，中央公用设施楼。

它主要放冷却相关设备。

---

#### 1. Cooling towers，冷却塔

冷却塔用于把热量排到大气中。

基本原理是：

```text
热水 -> 冷却塔 -> 蒸发散热 -> 冷却水回用
```

热量最终从 IT 设备传到空气或水中。

---

#### 2. Chillers，冷水机组

冷水机组用于制造冷却水。

它通过制冷循环把热量从冷冻水中移走。

常见流程：

```text
服务器产生热
  -> 热空气或热水
  -> 冷却系统
  -> 冷冻水吸收热量
  -> 冷水机组把热量转移出去
  -> 冷却塔或外部散热
```

---

#### 3. 为什么冷却如此重要？

因为服务器功率密度越来越高。

一个现代机柜可能消耗：

```text
10 kW
20 kW
30 kW
50 kW 或更高
```

如果热量不能及时带走：

```text
服务器温度升高；
CPU/GPU 降频；
硬件寿命下降；
故障率上升；
系统自动关机；
服务不可用。
```

所以冷却系统不是辅助设备，而是核心基础设施。

---

### 九、电力区：发电机和配电设备

原文说：

> An electrical yard houses electrical equipment, such as generators and power distribution centers.

electrical yard，电力区，放置电力相关设备。

---

#### 1. 数据中心电力链路的简化视图

一个典型数据中心电力路径可能是：

```text
外部电网
  -> 变电站
  -> 中压配电
  -> 变压器
  -> UPS
  -> 低压配电
  -> PDU
  -> 机柜
  -> 服务器
```

如果外部电网故障：

```text
发电机启动
  -> 接管供电
```

---

#### 2. 为什么需要发电机？

数据中心必须高可用。

即使外部电网中断，也不能立刻停机。

因此通常有：

```text
UPS 电池先支撑短时间；
柴油发电机或天然气发电机启动；
发电机持续供电直到电网恢复。
```

---

#### 3. 为什么需要冗余？

数据中心通常要求：

```text
任何单一故障不导致服务中断。
```

因此电力系统常有冗余设计，例如：

```text
N+1
2N
2N+1
```

这些冗余会增加成本，但提高可用性。

---

### 十、服务器大厅：IT 设备所在地

原文说：

> Within the data center, the main server hall hosts the compute, storage, and networking equipment organized into hot aisles and cold aisles.

server hall，服务器大厅，是真正放 IT 设备的地方。

---

#### 1. Hot aisle / cold aisle：冷热通道

这是数据中心气流组织的经典设计。

服务器通常：

```text
从前面吸入冷空气
从后面排出热空气
```

因此机柜排列成：

```text
冷通道 -> 机柜前面
热通道 -> 机柜后面
```

示意：

```text
Cold Aisle
  | 机柜前 | 机柜后 |
Hot Aisle
  | 机柜前 | 机柜后 |
Cold Aisle
```

这样做的目的是：

```text
让冷空气和热空气分开；
避免冷热空气混合；
提高冷却效率；
降低能耗；
让服务器进风温度更稳定。
```

---

#### 2. Hot air containment：热气封闭

原文提到：

> in some data centers, hot air containment structures

热气封闭是把热通道完全封闭起来。

例如：

```text
热通道顶部和两端封闭
热空气直接回收到冷却系统
```

这样可以进一步提高效率。

---

#### 3. 为什么气流管理很重要？

如果冷热空气混合：

```text
冷空气被浪费；
服务器进风温度升高；
冷却系统必须更努力工作；
能耗上升；
局部热点可能出现。
```

所以现代数据中心非常重视：

```text
机柜盲板
地板送风
风管设计
封闭通道
温度传感器
气流模拟
```

---

### 十一、服务器楼层上的维修区

原文说：

> The server floor can also host repair areas for operations engineers.

在超大规模数据中心里，硬件故障是常态，而不是例外。

因此服务器大厅里可能有：

```text
维修台
备件柜
诊断设备
替换硬盘
替换内存
替换电源
替换网卡
```

运维工程师可以在现场快速更换故障部件。

这体现了 WSC 的一个重要思想：

> 不追求单台机器永不故障，而是假设故障会发生，并通过快速检测、隔离和替换来维持系统整体可用。

---

### 十二、网络区域：数据中心的关键神经中枢

原文说：

> Most data centers also have separate areas designated for networking, including inter-cluster, campus-level, and long-haul connectivity and a separate facility management network.

网络区域非常关键。

---

#### 1. 网络区域包含哪些连接？

原文提到几类：

```text
inter-cluster connectivity
集群之间连接

campus-level connectivity
园区级连接

long-haul connectivity
长距离连接

facility management network
设施管理网络
```

---

##### inter-cluster connectivity

集群之间连接，例如：

```text
计算集群 A <-> 存储集群 B
计算集群 C <-> 数据库集群 D
```

用于数据中心内部不同集群之间的高速通信。

---

##### campus-level connectivity

园区级连接，例如：

```text
Building A <-> Building B
Building B <-> 网络核心楼
```

一个 campus 内多栋建筑之间需要高速网络。

---

##### long-haul connectivity

长距离连接，例如：

```text
Iowa <-> Oregon
Oregon <-> 欧洲
美国 <-> 亚洲
```

这通常依赖：

```text
光纤
DWDM
光传输设备
路由器
骨干网
```

---

##### facility management network

设施管理网络是独立网络，用于管理：

```text
电力设备
冷却设备
传感器
摄像头
门禁
BMC
服务器管理口
环境监控
```

它通常和生产数据网络隔离，以提高安全性和可靠性。

---

#### 2. 为什么网络区域需要额外物理安全？

原文说：

> Given the criticality of networking for data center availability, networking areas often have additional physical security and high-availability features.

因为网络是数据中心的神经系统。

如果网络中断：

```text
服务器还在运行，但无法通信；
存储还在，但无法访问；
服务还在，但用户无法使用；
集群可能失去协调；
控制平面可能失效。
```

所以网络区域通常有：

```text
更严格门禁
独立供电
冗余链路
冗余设备
物理隔离
防火分区
监控摄像
访问审计
```

---

### 十三、数据中心建筑的安全与规范

原文说：

> Data center building construction follows established codes around fire-resistive and noncombustible construction, safety, and so on.

数据中心建筑必须符合严格规范。

---

#### 1. 防火和不燃材料

数据中心里有大量：

```text
电力设备
电池
电缆
光纤
服务器
塑料部件
冷却管道
```

一旦发生火灾，损失巨大。

因此建筑通常要求：

```text
防火墙体
不燃材料
防火分区
烟雾探测
早期空气采样
气体灭火或预作用喷淋
电池间防爆
电缆阻燃
```

---

#### 2. 物理安全

原文提到：

> elaborate security for access, including circle locks, metal detectors, guard personnel, and an extensive network of cameras.

大型数据中心通常有多层物理安全：

```text
外围围栏
车辆屏障
门卫
徽章门禁
生物识别
金属探测
人员陪同
摄像监控
机柜锁
机房分区
访问日志
```

目的是防止：

```text
未授权进入
设备盗窃
人为破坏
供应链攻击
硬件篡改
社会工程攻击
```

---

### 十四、典型数据中心架构的两大系统：供电和冷却

原文最后说：

> Beyond the IT equipment, the two major systems in the data center provide power delivery and cooling.

这句话可以视为第 5 章后续内容的总纲。

数据中心除了 IT 设备，最关键的两个系统是：

```text
Power delivery
供电系统

Cooling
冷却系统
```

---

### 十五、供电系统：从电网到服务器

可以把供电系统理解为一条能量输送链：

```text
外部电网
  -> 变电站
  -> 发电机备份
  -> 中压配电
  -> 变压器
  -> UPS
  -> 低压配电
  -> PDU
  -> 机柜
  -> 服务器电源
  -> CPU/GPU/内存/磁盘/网卡
```

每一层都要考虑：

```text
效率
冗余
安全
监控
故障切换
容量扩展
```

---

### 十六、冷却系统：从芯片到室外

冷却系统可以理解为一条热量搬运链：

```text
CPU/GPU 产生热
  -> 散热器或液冷板
  -> 服务器风扇或液体回路
  -> 机柜热通道
  -> 机房空调或冷却水
  -> 冷水机组
  -> 冷却塔
  -> 室外空气或水
```

热量的路径是：

```text
芯片 -> 服务器 -> 机房 -> 冷却系统 -> 外部环境
```

所以冷却系统本质上是在做：

```text
热量搬运
```

---

### 十七、为什么数据中心效率如此重要？

原文虽然没有直接提 PUE，但这里非常适合补充。

---

#### 1. PUE 是什么？

PUE，Power Usage Effectiveness，是衡量数据中心能效的常用指标。

定义：

```text
PUE = 数据中心总耗电 / IT 设备耗电
```

例如：

```text
IT 设备耗电：100 MW
冷却、供电损耗、照明等：20 MW
总耗电：120 MW
```

则：

```text
PUE = 120 / 100 = 1.2
```

PUE 越接近 1，说明非 IT 能耗越少。

---

#### 2. 为什么 PUE 很重要？

假设一个数据中心 IT 负载是：

```text
100 MW
```

如果 PUE 是：

```text
1.5
```

总功耗是：

```text
150 MW
```

如果 PUE 降到：

```text
1.1
```

总功耗是：

```text
110 MW
```

节省：

```text
40 MW
```

这相当于少建一座中型电厂，或者少消耗大量电力。

所以原文说：

> drive the vast majority of non-computing costs

供电和冷却效率直接决定数据中心的运营成本。

---

### 十八、如何把这一节和 WSC 的核心思想联系起来？

这本书反复强调：

> The data center as a computer.

但这一节提醒我们：

> 这台“大计算机”不是抽象的，它首先是一个巨大的物理能量系统。

可以这样理解：

```text
软件视角：
  数据中心是运行分布式服务的平台。

硬件视角：
  数据中心是大量服务器、存储和网络设备的集合。

基础设施视角：
  数据中心是把电力转换为计算和热量的工厂。

经济视角：
  数据中心的规模和成本主要由 critical power 决定。

安全视角：
  数据中心必须保证物理、电力、网络和固件层面的可信。
```

---

### 十九、一个具体例子：100 MW 数据中心园区意味着什么？

假设一个 WSC campus 的 critical power 是：

```text
100 MW
```

这意味着什么？

---

#### 1. 建设成本

如果建设成本是：

```text
$10/W
```

那么：

```text
100 MW = 100,000,000 W
100,000,000 × $10 = $1,000,000,000
```

也就是约 10 亿美元。

这还只是建设成本，不包括：

```text
土地
服务器
网络设备
存储设备
软件
运维人员
电力费用
网络带宽费用
```

---

#### 2. 电力消耗

如果持续运行：

```text
100 MW
```

一年耗电量约为：

```text
100 MW × 24 h × 365 d = 876,000 MWh
```

也就是：

```text
876 GWh/年
```

如果 PUE 是 1.2，则总设施耗电：

```text
876 × 1.2 = 1,051.2 GWh/年
```

---

#### 3. 热量排放

如果 IT 设备消耗：

```text
100 MW
```

几乎这些功率最终都变成热：

```text
约 100 MW 热量
```

冷却系统必须持续带走这些热。

这相当于一个小型城市级别的热负荷。

---

### 二十、这一节的关键概念总结

---

#### 1. 数据中心是行星级计算机的一部分

```text
Planet-scale services
  -> multiple regions
  -> multiple campuses
  -> multiple buildings
```

---

#### 2. 数据中心建筑的核心功能

```text
供电
冷却
遮蔽
安全
```

---

#### 3. 数据中心本质上是能量转换设施

```text
电能输入
  -> 计算/存储/网络
  -> 热能输出
```

---

#### 4. 非计算成本主要来自供电和冷却

```text
power delivery
cooling
```

---

#### 5. 数据中心规模用 critical power 衡量

```text
enterprise: < 1 MW
colo: tens of MW
WSC campus: often > 100 MW
```

---

#### 6. 数据中心建设成本常用 $/W 表示

```text
$5–20/W
```

---

#### 7. 数据中心主要物理区域

```text
mechanical yard     冷却设备
electrical yard     电力设备
server hall         IT 设备
networking areas    网络设备
facility management network 设施管理网络
repair areas        维修区域
security layers     安防体系
```

---

#### 8. 冷热通道是常见气流组织方式

```text
cold aisle：机柜前进冷风
hot aisle：机柜后排热风
containment：封闭通道，提高效率
```

---

### 二十一、这一节可以整理成的精简笔记

```text
5.1 Data center infrastructure basics

5.1.1 Planet to campuses to buildings
1. 互联网和云服务运行在行星级计算机上。
2. 工作负载分布在全球多个数据中心建筑中。
3. 数据中心建筑的主要功能是提供：
   - power 供电
   - cooling 冷却
   - shelter 物理遮蔽
   - security 安全
4. 从物理角度看，数据中心几乎不做机械功。
   - 输入电能
   - 除少量光子外，几乎全部转化为热
5. 数据中心设计核心：
   - 输入能量
   - 移走废热
6. 非计算成本主要由供电和冷却驱动。
7. 建设成本大致与 critical power 成正比：
   - 约 $5–20/W
   - 受规模、地点、设计影响

5.1.2 Basic structure of a data center
1. 数据中心规模常用 critical power 描述。
   - critical power：可持续供给 IT 设备的总功率
2. 规模分类：
   - 传统企业数据中心：< 1 MW，< 5,000 sq ft
   - colocation：数十 MW
   - 大型云数据中心：类似或更大
   - WSC campus：常 > 100 MW
3. 数据中心可由多栋建筑组成 campus。
4. 多数数据中心为单层，少数多层。
5. 主要组成部分：
   - mechanical yard：冷却塔、冷水机等冷却系统
   - electrical yard：发电机、配电中心等电力系统
   - server hall：计算、存储、网络设备
   - hot aisle / cold aisle：冷热通道气流组织
   - repair areas：现场维修区域
   - networking areas：集群、园区、长距离网络
   - facility management network：独立设施管理网络
6. 网络区域通常有额外物理安全和高可用设计。
7. 建筑需满足防火、不燃、安全等规范。
8. 典型数据中心两大非 IT 系统：
   - power delivery 供电
   - cooling 冷却
```

---

### 二十二、如果考试或讨论中要回答这一节，可以这样说

你可以这样概括：

> 5.1 节从基础设施角度说明数据中心不是简单的“服务器房间”，而是一个以供电和冷却为核心的物理系统。互联网和云服务运行在行星级计算机上，由分布在全球的数据中心建筑承载。这些建筑的主要功能是为 IT 设备和人员提供电力、冷却、遮蔽和安全。由于数据中心消耗的电能几乎最终都转化为热量，因此如何输入能量并移走废热成为设计核心，也决定了大部分非计算成本。数据中心规模通常用 critical power 衡量，即能够持续供给 IT 设备的总功率。传统企业数据中心通常小于 1 MW，colocation 可达数十 MW，而 WSC 园区常超过 100 MW。建设成本大致与供电能力成正比，约为每瓦 5 到 20 美元。数据中心建筑通常包括机械区、电力区、服务器大厅、网络区域和设施管理网络。服务器大厅采用冷热通道等气流组织方式，以提高冷却效率。由于网络对可用性至关重要，网络区域通常具有额外物理安全和冗余设计。总体而言，这一节强调数据中心本质上是一台把电能转化为计算和热量的大规模基础设施机器。

---

### 二十三、最后给你一个形象类比

可以把数据中心想象成一座“数字工厂”。

```text
服务器：
  工厂里的机器。

网络：
  工厂里的传送带和通信系统。

软件：
  生产流程和管理系统。

电力系统：
  工厂的能源供应。

冷却系统：
  工厂的排热和空调系统。

建筑和安全：
  工厂厂房、围墙、门禁和消防。

critical power：
  这座工厂最多能同时运行多少机器。

$/W：
  每增加一瓦产能需要多少建设成本。

PUE：
  工厂用于生产以外的能源浪费有多少。
```

而这一节最重要的提醒是：

> 数据中心不是“放服务器的房子”，而是“为计算服务的电力和冷却基础设施”。


**专栏导航**

- ← 上一篇：[4.4 Server-level software](/posts/4-4-server-level-software/)
- 返回：[栏目总览](/posts/the-data-center-as-a-computer-ai-guide/)
- 下一篇：[5.1.3 Data center taxonomy: Tiers →](/posts/5-1-3-data-center-taxonomy-tiers/)
