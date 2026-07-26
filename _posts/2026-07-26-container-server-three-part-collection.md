---
title: "容器与服务器：从「一个进程怎么被关进笼子」到「为什么你的服务器跑不了 Docker」"
author: Fu Qilin
date: 2026-07-26
categories: [Memo]
tags: [container, docker, kubernetes, namespace, cgroup, server, gpu, nccl]
description: "从一个开源新手任务连撞三台机器环境配置失败出发，系统讲清容器与服务器的底层原理：namespace、cgroups、capabilities、overlayfs、网络、K8s，以及 AI 训练/推理场景下的容器与分布式通信实践。"
excerpt: "为什么你的服务器跑不了 Docker？一篇把 namespace、cgroups、capabilities、overlayfs、网络、K8s 与 AI 训练/推理容器实践一次讲透的长文（上/中/下三篇 + 附录）。"
---

<!-- markdownlint-disable MD013 MD025 -->

## 容器与服务器：从「一个进程怎么被关进笼子」到「为什么你的服务器跑不了 Docker」

起因是我在做一个开源项目的新手任务时，连着在三台机器上配环境失败：

```
魔搭 Notebook（底层是阿里云 DSW）   Cannot connect to the Docker daemon
课题组 H100                          mount overlay: permission denied
换成 apptainer + sif                  fuse: device not found
```

折腾两小时之后我发现一个更糟的事实：我对这些报错背后的原理一无所知。我做的事情只是把报错交出去、拿回一条命令、试一下、再换一条——而从头到尾没问过一个问题：这台机器到底能不能做到我要它做的事。

后来我把这个问题弄清楚了，就有了这三篇。

**目标不是「教你用 Docker」，而是让你在下次撞墙时知道自己撞的是哪堵墙。**

全文约 7.6 万字。三篇可以独立阅读：

- **只想解决眼前的报错** → 直接跳到中篇第 0 章（三十秒诊断盒），或下篇附录 B（报错索引）
- **想搞清楚原理** → 从上篇开始顺着读
- **只想拿可用的东西** → 下篇附录 A（诊断脚本）和附录 H（分布式参数清单）可以直接抄走

### 总目录

**上篇 · 一个进程是怎么被关进笼子的**（原理）

0. 引子：你以为在装个软件，其实是在和内核谈判 · 全系列知识地图
1. 容器的本质：不是「轻量虚拟机」；以及谁在真正跑容器（CLI → dockerd → containerd → shim → runc）
2. 隔离之一：namespace（八种）
3. 隔离之二：cgroups（兼环境指纹）
4. 隔离之三：权力削减——容器里的 root 有两种
5. overlay 与写时复制（含 upperdir 对 xattr 的隐蔽要求）
6. 数据怎么活下来：持久化与挂载
7. 容器怎么上网
8. 镜像：你拉的那堆东西到底是什么
9. 从单机到集群：你为什么活在一个 Pod 里

**中篇 · 为什么你的服务器跑不了 Docker**（诊断与求生）

0. 三十秒诊断盒
1. 五类环境，五种命运
2. 跑起一个 Docker 到底要问内核要什么
3. 平台为什么宁可全禁
4. 报错鉴别诊断表（八类报错 × 多种病因）
5. 跑不了 Docker，到底怎么把环境跑起来
6. DinD：容器里跑容器，为什么那么难
7. 换个运行时，绕开了什么、绕不开什么

**下篇 · AI 训练与推理场景下的容器实践**

1. 容器怎么「看见」GPU
2. 容器里的分布式通信（shm / memlock / IB / host 网络 / NCCL 拓扑）
3. 容器安全与共享机礼仪
4. 工程方法论：怎么不再靠运气排错
5. 结语：三个报错，一份契约

附录 A–J：诊断脚本 · 报错索引 · 环境对照表 · 机制速查 · 无 root 工具箱 · 申请模板 · DinD 决策树 · 分布式参数清单 · 安全 checklist · 参考资料

---

## 上篇 ·《一个进程是怎么被关进笼子的》

> 系列共三篇。这是原理篇——中篇里所有的判断依据，都在这一篇里。
>
> 如果你是带着报错搜进来的，建议直接跳到中篇《为什么你的服务器跑不了 Docker》，拿到答案之后再回头读这篇。

> **适用范围与版本说明**（先看这一段，能省你很多时间）
>
> - 默认背景是 Linux 5.15+、Docker 24+、**cgroup v2**。文中涉及 cgroup v1 的部分只在较老的机器上才用得到。
> - 所有镜像 tag、驱动版本号都只是**写作当时的示例**，请换成你自己环境里的实际版本，不要直接照抄。
> - 命令里凡是带 `sudo` 的，都意味着“需要管理员”；你在只有普通用户权限的机器上直接跑是一定失败的。
> - 内核行为、安全策略、平台限制都在变。文中的**判定命令比结论更保值**——当结论和你机器上的输出矛盾时，以输出为准。

---

### 0. 引子：你以为在"装个软件"，其实是在"和内核谈判"

有一天我要跑一个开源项目的训练任务，官方给的是一个 Docker 镜像。我心想这不简单吗，`docker run` 一下的事。

然后我在三台机器上连撞三面墙：

- 魔搭的 Notebook（底下是阿里云 DSW）：`docker` 命令根本连不上 daemon。
- 课题组自己的 H100：`mount overlay: permission denied`，我明明是 root。
- 换 apptainer + sif：`fuse: device not found`，squashfs 挂不上。

那几个小时我干的事情是：把报错贴给大模型 → 它给我一串命令 → 我复制粘贴 → 报另一个错 → 再贴 → 再试。有时候能蒙对，更多时候是它一本正经地给了我一条在这台机器上根本不可能成功的命令。

后来我意识到问题不在大模型，在我：**我把容器当成了一个应用，而它其实是一份契约。**

`nginx` 是应用，你装上它，它就干活。容器不是。容器是**操作系统内核能力的消费者**——它能不能跑，不取决于你装没装 Docker，取决于**内核愿不愿意把某几项权力交给你**。你在一台机器上跑不了容器，几乎从来不是"软件坏了"，而是"这台机器的管理员（或者云平台）决定不给你这几项权力"。

这一篇讲的就是这份契约的条款：容器到底问内核要了什么，内核又是怎么给、怎么收回的。

读懂之后，你会发现 90% 的"环境玄学"其实是**必然结果**——不是运气不好，是条款里本来就没写这一条。

---

### 全系列知识地图

三篇一共讲十二个知识点，它们之间是有依赖关系的。先把图放在这里，你随时可以回来看自己读到了哪。

```
【地基】
 ① 共享内核              ── 容器不是虚拟机，这一条推出后面所有结论
     │
【四道墙：内核怎么关笼子】
     ├─ ② namespace        ── 你能看见什么
     ├─ ③ cgroups          ── 你能用多少（兼环境指纹）
     ├─ ④ capabilities     ── 你有哪几项权力（CAP_SYS_ADMIN 是关键）
     └─ ⑤ seccomp / LSM    ── 哪些系统调用真能叫得动
     │
【容器怎么跑起来】
     ├─ ⑥ overlayfs / CoW  ── 根文件系统（需要 mount 权 + xattr）
     ├─ ⑦ 挂载与持久化     ── 数据、/dev/shm、UID、宿主文件系统的物理现实
     ├─ ⑧ 网络            ── veth + iptables（多机训练时变成主要矛盾）
     └─ ⑨ 镜像            ── 一堆带元数据的 tar（所以能手工拆开用）
     │
【你到底在哪里】
     └─ ⑩ 编排与 Pod       ── 很多时候你已经在容器里了
     │
【AI 场景特有】
     ├─ ⑪ GPU 透传         ── prestart hook 把宿主驱动挂进来
     └─ ⑫ 分布式通信       ── 容器不影响计算，但处处影响通信
```

**三篇分工：**

||回答的问题|对应知识点|
| ----| ------------------------------| ---------------|
|上篇|容器到底是什么，内核怎么实现它|①–⑩|
|中篇|我为什么跑不了，跑不了怎么办|②–⑥ 的实战面|
|下篇|跑起来之后，AI 场景还有哪些坑|⑪⑫|

如果你只有五分钟，直接去看中篇的第 0 章（三十秒诊断盒）。

---

### 1. 容器的本质：它真的不是"轻量虚拟机"

#### 1.1 一句话定义

**容器 = 一组被内核隔离机制约束的普通进程。**

注意"普通进程"这四个字。你在容器里跑的 Python，和你在宿主机上直接跑的 Python，在内核眼里是同一种东西——都是 task_struct，都在同一个调度器里排队，都用同一套系统调用。

区别只在于：容器里的那个进程，**被套上了几层限制**。

#### 1.2 和虚拟机的根本区别：内核是谁的

```text
┌──────────────┐   ┌──────────────┐
│    App A     │   │    App B     │   ← 你的程序
├──────────────┤   ├──────────────┤
│   Guest OS   │   │   Guest OS   │   ← 每个 VM 一整个操作系统
│  （独立内核）  │   │  （独立内核）  │      有自己的内核
├──────────────┴───┴──────────────┤
│          Hypervisor             │   ← 虚拟化层：模拟硬件
├─────────────────────────────────┤
│        宿主硬件 / 宿主内核         │
└─────────────────────────────────┘
```

虚拟机是**硬件层面的隔离**：Hypervisor 虚拟出一整套假硬件，上面跑一个完整的、独立的内核。你在虚拟机里干任何事，都被挡在"假硬件"这一层里面。

```python
┌──────────────┐   ┌──────────────┐
│    App A     │   │    App B     │   ← 你的程序
├──────────────┴───┴──────────────┤
│         容器镜像里的库            │   ← 注意：这里没有操作系统！
├─────────────────────────────────┤      只有一层"约束"
│       宿主内核（只有一个）         │   ← 所有人共用这一个内核
├─────────────────────────────────┤
│            宿主硬件              │
└─────────────────────────────────┘
```

容器是**内核层面的隔离**：没有假硬件，没有第二个内核，所有容器和宿主机共用同一个内核。所谓的隔离，是这个内核**假装**给每个容器看到不同的世界。

#### 1.3 为什么容器"轻"

因为它省掉了两样最贵的东西：

- **没有 guest OS**：不用启动 systemd、不用初始化一堆内核子系统。镜像只装应用需要的库，几十 MB 到几 GB，而不是一个完整发行版。
- **没有硬件虚拟化开销**：系统调用直接进宿主内核，不经过 Hypervisor 转译。

结果就是：虚拟机启动几十秒，容器启动几十毫秒。

#### 1.4 「共享内核」推出的三个后果

这一条是全系列的地基，请务必记住：

**后果一：内核版本由宿主决定，镜像说了不算。**

你拉一个 `ubuntu:22.04` 的镜像，在 CentOS 7 的老机器上跑，容器里的 `uname -r` 显示的**还是宿主那个 3.10 的内核**。镜像只提供用户态的库和工具，内核永远是宿主的。

```bash
# 宿主机
$ uname -r
5.15.0-91-generic

# 容器里（镜像是 ubuntu:20.04）
$ docker run --rm ubuntu:20.04 uname -r
5.15.0-91-generic     # ← 一模一样
```

这就是为什么有些软件在容器里死活跑不起来：它需要某个内核特性（比如 io_uring、某个 eBPF 能力、某个新的 cgroup 控制器），而**宿主内核太老，镜像再新也没用**。

**后果二：隔离是"软"的。**

虚拟机的隔离是硬的——你要突破，得先攻破 Hypervisor。容器的隔离是内核里的一堆检查逻辑，**内核有漏洞，隔离就有洞**。这是后面"容器逃逸"和"平台为什么宁可全禁"的根源。

**后果三：特权能击穿隔离。**

既然隔离是内核做的检查，那只要你有足够的权力让内核跳过检查（`--privileged`、`CAP_SYS_ADMIN`），你就能捅穿它。这也是为什么共享环境里，这些权力被卡得死死的。

---

#### 1.5 谁在真正跑容器：`docker` 只是个前台

你敲 `docker run`，感觉像是 Docker 一个人干完了所有事。其实中间站着一串组件，每个只管一小段。这条链条不搞清楚，后面很多现象会显得莫名其妙——比如"K8s 里明明在跑容器，宿主上却没装 Docker"。

```
你敲的命令
    │  docker run ...
    ▼
docker CLI            只是个 HTTP 客户端。把命令翻译成 API 请求，
    │                  发给 /var/run/docker.sock 这个 Unix socket
    ▼
dockerd               常驻守护进程，root 身份运行。管镜像、网络、
    │                  存储卷这些"周边事务"。真正起容器它不亲自动手
    ▼
containerd            容器生命周期管理器。拉镜像、解层、准备 rootfs，
    │                  然后为每个容器叫一个 shim
    ▼
containerd-shim       每个容器一个。它的存在是为了让 containerd
    │                  能重启而不杀掉正在跑的容器（"守护进程解耦"）
    ▼
runc                  真正干活的那个。它是个用完就退出的命令行程序，
    │                  按 OCI 规范读一份 config.json，调 clone/unshare/
    │                  mount/setns/capset，然后 execve 进你的进程
    ▼
你的进程              此时 runc 已经退出了。容器里 PID 1 的父进程是 shim
```

有四个结论直接影响你排错：

**一、**​**​`Cannot connect to the Docker daemon`​**​ ** 是 CLI 找不到 dockerd，跟内核毫无关系。**  CLI 在你机器上装着（所以 `docker` 命令存在、`--help` 也能打），但 socket 那头没人应答。所以这个报错永远不能推出"我的内核不支持容器"——中篇第 4 章会把这个区分讲透。

**二、真正需要特权的其实只有 runc 那一小段。**  前面几层都是记账和调度，只有 runc 会去调 `mount`、`pivot_root`、`setns` 这些要 `CAP_SYS_ADMIN` 的系统调用。这就是为什么 rootless 方案的思路都是"想办法让 runc 那几步在无特权下也能成立"，而不是去改 Docker。

**三、这条链条是可以拆开卖的。**  runc 只是 OCI 运行时的一个实现，可以整个换掉——换成 `crun`（C 语言写的，更快）、`gVisor`（自己实现一层内核系统调用）、`Kata`（干脆给你起个轻量虚拟机）、`sysbox`（让容器内能嵌套跑容器）。上层的 containerd 完全不用改。中篇第 7 章那张运行时对照表，横向比的就是这一层。

**四、Docker 从来不是必需品。**  K8s 在 1.24 之后移除了 dockershim，现在直接调 containerd 或 CRI-O。所以你在一个 Pod 里 `which docker` 找不到东西，非常正常——底下确实在跑容器，只是那条链条从 containerd 起步，没有 dockerd 和 docker CLI 这两层。

> 顺手记一条：`docker` 命令属于 `docker` 组的人都能用，而 dockerd 是 root。所以**把用户加进 docker 组，等价于给了 root 权限**（`docker run -v /:/host` 就能改宿主任何文件）。这是中篇第 3 章里"管理员为什么不肯给你装 Docker"最硬的那条理由。

---

### 2. 隔离之一：namespace——「让你以为自己是唯一的」

#### 2.1 它到底干什么

namespace 解决的是 **&quot;你能看见什么&quot;** 。

内核维护着一堆全局资源：进程列表、挂载表、网络设备、主机名……namespace 的作用是把这些全局资源**切成互不相干的几份**，然后告诉进程：你只能看见你那一份。

注意关键词是"看见"。namespace 不管你能用多少资源（那是 cgroups 的事），也不管你能做什么操作（那是 capabilities 的事）。它只管**视野**。

#### 2.2 八种 namespace（不是七种）

很多老文章说七种，其实 Linux 5.6 之后是**八种**了：

|namespace|隔离什么|容器里的直观表现|
| ---------| ------------------------------------| ------------------------------------------|
|`pid`|进程 ID 与进程树|`ps` 只看得到自己那几个进程，主进程 PID 是 1|
|`mnt`|挂载点|有自己的一套文件系统视图，看不到宿主的目录|
|`net`|网卡、IP、端口、路由、iptables|有自己的 `eth0` 和独立的端口空间|
|`uts`|主机名和域名|`hostname` 是一串容器 ID|
|`ipc`|System V IPC、POSIX 消息队列、**共享内存**|和宿主的共享内存互不可见（这条后面会咬人）|
|`user`|UID/GID 映射|容器里的 root 可以映射成宿主的普通用户|
|`cgroup`|cgroup 根目录视图|看不到自己在宿主 cgroup 树里的真实位置|
|`time`|系统启动时间、单调时钟（Linux 5.6+）|容器可以有自己的 uptime|

**其中 **​**​`user`​**​ ** namespace 是最特殊的一个**——它是唯一一个"无特权用户也能创建"的 namespace，也正因为如此，它是 rootless 容器的整个技术基础。这一点在第 4 章会展开，也是很多人（包括之前的我）理解错的地方。

#### 2.3 从 chroot 到 namespace：一次视野的升级

`chroot` 是 1979 年就有的老东西，它只干一件事：把进程的"根目录"换成另一个目录。

问题是，它只换了文件系统这一个视角。进程还是能看到宿主所有的进程、所有的网卡、所有的端口。而且它有个著名的问题：**chroot 是可以逃出去的**（经典的 `chroot` 逃逸只要几行 C 代码），因为它从设计上就不是安全边界。

namespace 相当于把 chroot 的思路推广到了操作系统的每一个维度：不只是换根目录，而是**换一整套世界观**。而且它在内核数据结构层面就做了隔离，不是简单地改个路径前缀。

#### 2.4 动手：亲手造一个 namespace

这是最能建立直觉的一个实验，一条命令：

```bash
$ sudo unshare --pid --fork --mount-proc /bin/bash

# 进去之后：
# ps aux
USER  PID %CPU %MEM    VSZ   RSS TTY  STAT START   TIME COMMAND
root    1  0.0  0.0  12016  3352 pts/0 S   22:31   0:00 /bin/bash
root   12  0.0  0.0  44636  3396 pts/0 R+  22:31   0:00 ps aux
```

整台机器上明明跑着几百个进程，这里只看得到两个，而且 bash 的 PID 是 **1**。这就是 pid namespace。

几个参数的意思：`--pid` 建新的 pid namespace，`--fork` 是必须的（因为当前进程的 PID 不能改，得 fork 一个新的进来），`--mount-proc` 是把 `/proc` 重挂一遍（否则 `ps` 读的还是宿主的 `/proc`，会看到全部进程）。

再试试网络的：

```bash
$ sudo unshare --net /bin/bash
# ip a
1: lo: <LOOPBACK> mtu 65536 ...
    link/loopback 00:00:00:00:00:00
```

一张网卡都没有，只剩一个没启动的 lo。一个全新的 net namespace 就是这么干净——**容器的网络之所以要配一大堆东西，就是因为它出生时一无所有**。

#### 2.5 ⚠️ 这个实验本身就是一次诊断

这里有个特别妙的地方，也是我写这个系列的起点：

**上面这些实验，在受限环境里本身就会失败。**

```bash
# 在某些 K8s Pod / 共享集群上：
$ unshare -Ur echo ok
unshare: unshare failed: Operation not permitted
```

如果你连一个 user namespace 都建不出来，那你**必然**跑不了 rootless 容器——因为 rootless 的第一步就是建 user namespace。

所以 `unshare -Ur echo ok` 是我现在上任何一台新机器都会跑的命令之一：**一秒钟判断这台机器给不给我玩容器**。它出现在中篇开头的"30 秒诊断盒"里，原因就在这。

讲隔离的教程跑不了讲隔离的实验，这事儿听起来像个段子，但它比任何说教都更能让你理解：**这堵墙是真实存在的，而且很高**。

---

### 3. 隔离之二：cgroups——「给你多少你就只能用多少」

#### 3.1 它管的是「能用多少」

namespace 解决了"看得见什么"，但没解决一个很现实的问题：你看不到别人的进程，不代表你不能把机器的内存吃光。

cgroups（control groups）就是干这个的：把一组进程圈起来，给它们设资源上限。CPU、内存、IO、PID 数量、设备访问权限——都归它管。

#### 3.2 v1 和 v2 的区别（为什么新机器行为不一样）

这个区别不是细节控才关心的事，它真会影响你。

- **cgroup v1**：每种资源一棵独立的树。`/sys/fs/cgroup/memory/`、`/sys/fs/cgroup/cpu/`……各管各的。灵活，但混乱，而且中篇会讲到的 `release_agent` 逃逸就是 v1 的遗产。
- **cgroup v2**：统一一棵树，所有控制器挂在同一个层级上。更干净，而且支持**委派（delegation）** ——可以把一棵子树交给普通用户管。

**为什么你要关心：**  rootless 容器（podman、rootless docker）想限制资源，必须靠 cgroup v2 的委派机制。如果你的机器还是 v1，rootless 容器就设不了内存/CPU 限额（能跑，但 `--memory` 等参数静默失效）。

怎么看自己是哪个版本：

```bash
$ stat -fc %T /sys/fs/cgroup/
cgroup2fs      # ← v2
tmpfs          # ← v1
```

#### 3.3 OOM Killer：容器「莫名被杀」的真相

这是最常见、也最容易让人追错方向的一个现象。

你跑着跑着，程序没任何错误输出就没了。`docker ps -a` 一看：

```
STATUS: Exited (137) 2 minutes ago
```

**137 = 128 + 9**，9 就是 SIGKILL。你的进程是被强杀的。

然后你去 `docker inspect`：

```json
"OOMKilled": true
```

关键在于：**这个 OOM 很可能不是你以为的那个 OOM。**

机器总共 512G 内存，`free -h` 显示还剩 400G，你的程序才用了 20G——但它还是被杀了。因为杀它的不是全局 OOM Killer，而是 **cgroup 级别的 OOM**：平台给你这个容器设的限额就是 16G，你超了。

还有一个更坑的地方：**容器里的 **​**​`free -h`​**​ ** 和 **​**​`top`​**​ ** 看到的是宿主的内存，不是你的限额。**  因为这些工具读的是 `/proc/meminfo`，而 `/proc` 没有被 cgroup 隔离（除非装了 lxcfs 之类的东西）。这导致很多自动调参的程序（比如 JVM 的默认堆大小、一些数据处理库的并行度）在容器里会把参数设得离谱地大，然后当场自杀。

**正确的查法**：

```bash
# cgroup v2
cat /sys/fs/cgroup/memory.max        # 我的限额
cat /sys/fs/cgroup/memory.current    # 我现在用了多少
cat /sys/fs/cgroup/memory.events     # 看 oom_kill 计数

# cgroup v1
cat /sys/fs/cgroup/memory/memory.limit_in_bytes
cat /sys/fs/cgroup/memory/memory.usage_in_bytes
```

#### 3.4 CPU 限制：`--cpus` 和 `--cpu-shares` 不是一回事

很多人混用这两个，实际上它们的语义完全不同：

-  **​`--cpus=2`​**：**硬上限**。底层是 CFS 带宽控制（quota/period），意思是"每 100ms 周期里你最多用 200ms CPU 时间"。**就算机器完全空闲，你也只能用 2 核。**
-  **​`--cpu-shares=1024`​**：**相对权重**。只在**争抢时**生效。机器空闲时你能把所有核吃满；两个容器都想要 CPU 时，按 1024:512 = 2:1 分。

**一个真实的坑**：在多核机器上用 `--cpus=2` 跑 PyTorch，而 PyTorch 看到 `nproc` 是 128，于是开 128 个 OpenMP 线程去抢那 2 核的配额——上下文切换打架，比单线程还慢。

所以在容器里记得手动设：

```bash
export OMP_NUM_THREADS=2    # 和你的 --cpus 对齐
```

#### 3.5 关键线索：cgroup 路径会「自报家门」

这是我觉得整个系列里性价比最高的一个小知识：

```bash
cat /proc/1/cgroup
```

它告诉你 PID 1 在 cgroup 树里的位置。而这个位置基本等于"你到底活在什么环境里"：

|输出里包含|意味着|
| ----------| ----------------------|
|`/kubepods/...` 或 `/kubepods.slice/...`|**你是一个 K8s Pod**|
|`/docker/<64位哈希>`|你在一个 Docker 容器里|
|`/lxc/...`|你在 LXC 容器里|
|`/system.slice/...` 或 `0::/` 或 `/init.scope`|你在真机 / 完整 VM 上|

我当时在魔搭 Notebook 里跑这一行，看到了 `kubepods`。

那一瞬间所有事情都通了：我不是在一台"云服务器"上，我本身就是**一个被 K8s 调度出来的容器**。我想在里面再跑 Docker，就是在笼子里开笼子。这条路从根上就是堵死的，我先前花的那两个小时完全是无用功。

**一行命令，省两个小时。**  这就是为什么它排在中篇诊断盒的第一条。

#### 【所以然】

> cgroup 不只是个限额工具，它还是一枚**环境指纹**。它不会撒谎，而且看一眼就够了。

---

### 4. 隔离之三：权力削减（capabilities / seccomp / LSM）

前两道墙解决了"看不见"和"用不多"。但还有个最大的穿帮问题没解决：**容器里如果是 root，它能干什么？**

#### 4.1 capabilities：把 root 拆成四十个开关

传统 Unix 只有两种人：root（什么都能干）和非 root（什么都不能干）。这个模型太粗了——`ping` 需要发原始套接字，难道就要给它全部 root 权限？

于是 Linux 把 root 的权力拆成了四十来个细粒度开关（当前内核 `CAP_LAST_CAP` = 40，即 0–40 共 41 项）：

|capability|能干什么|
| ----------| ---------------------------|
|`CAP_NET_BIND_SERVICE`|绑定 1024 以下的端口|
|`CAP_NET_ADMIN`|配网卡、改路由、改 iptables|
|`CAP_NET_RAW`|发原始包（ping 靠它）|
|`CAP_CHOWN`|改文件所有者|
|`CAP_SYS_MODULE`|加载内核模块|
|`CAP_SYS_TIME`|改系统时间|
|**​`CAP_SYS_ADMIN`​**|**mount / umount / pivot_root / setns / 改 cgroup / 一堆 ioctl……**|

看出问题了吗？前面那些都很"细粒度"，而 `CAP_SYS_ADMIN` 是个垃圾桶——内核开发者历年来把不好归类的特权操作全塞进了它。内核社区自己都管它叫  **"the new root"** 。

**所以：给容器 **​**​`CAP_SYS_ADMIN`​**​ **，大致等于把宿主机送给它。**  这是后面所有限制的逻辑起点。

看自己手里有什么：

```bash
$ grep CapEff /proc/self/status
CapEff:	00000000a80425fb

$ capsh --decode=00000000a80425fb
0x00000000a80425fb=cap_chown,cap_dac_override,cap_fowner,cap_fsetid,
cap_kill,cap_setgid,cap_setuid,cap_setpcap,cap_net_bind_service,
cap_net_raw,cap_sys_chroot,cap_mknod,cap_audit_write,cap_setfcap
```

这就是 Docker 默认给容器的 14 个 capability。**注意里面没有 **​**​`cap_sys_admin`​**​ **。**  这一行输出，已经回答了一半的"为什么我的命令报 permission denied"。

#### 4.2 重点：「容器里的 root」有两种，别搞混

这一节是整篇文章最容易被讲错的地方。我自己一开始也搞错了，而且这个错会直接导致排错方向跑偏。

网上很多文章会告诉你："容器里的 root 其实是宿主上的普通用户，因为 user namespace 做了映射。"

**这句话对一半，而且不对的那一半会坑死你。**  实际上有两条完全不同的技术路线：

##### 路线 A：默认的 Docker——**真 root + 削权**

```bash
# 宿主上看一个普通容器的进程：
$ docker run -d --name test nginx
$ ps -ef | grep nginx
root     12345  ...  nginx: master process    # ← 宿主看到的就是 root
```

Docker **默认不开** user namespace remap。`userns-remap` 是个可选配置，而且开了会和 `--privileged`、部分卷挂载、`--pid=host` 等特性冲突，所以生产环境里很少用。

所以默认情况下，**容器里的 root 就是宿主上真实的 uid 0**。它越不了界，靠的是：

- capabilities 被 drop 到只剩 14 个
- seccomp 拦掉危险系统调用
- AppArmor/SELinux 做强制访问控制
- 挂载的 `/proc`、`/sys` 部分路径被设成只读或遮蔽

这叫**削权模型**：你是真皇帝，但大臣们把你的印收了。

##### 路线 B：rootless（podman / apptainer / rootless docker）——**假 root + 映射**

```bash
$ podman run -d --name test nginx      # 以普通用户身份跑
# 宿主上：
$ ps -ef | grep nginx
zhangsan 12345  ...  nginx: master process   # ← 宿主看到的是你自己
```

这里才真正用上了 user namespace：容器内的 uid 0 被**映射**到宿主的 uid 1000（你）。容器内的 uid 1–65535 则映射到 `/etc/subuid` 里分配给你的那一段子 UID 区间（比如 100000–165535）。

这叫**映射模型**：你在自家院子里当皇帝，出了门就是普通百姓。

##### 为什么必须分清楚

因为**排错方向完全相反**：

||路线 A（默认 Docker）|路线 B（rootless）|
| -----------------------------| -----------------------------| ------------------------------|
|报 permission denied 时查什么|查 capabilities、seccomp、LSM|查 `/etc/subuid`、`newuidmap` setuid 位、userns sysctl|
|能不能写宿主的 root 文件|能（如果挂进来了）|不能，UID 对不上|
|在 K8s Pod 里可行吗|不行（没 SYS_ADMIN）|也很难（userns 常被禁）|
|挂卷权限问题|UID 直接对应|UID 被偏移，写出的文件属主很怪|

如果你用的是默认 Docker 却去查 `/etc/subuid`，或者用 podman 却去求管理员给 `CAP_SYS_ADMIN`，都是在白费力气。

#### 4.3 seccomp：系统调用层面的门禁

capabilities 管的是"你有没有这个权力"，seccomp 管的是 **&quot;这个系统调用你能不能叫&quot;** 。

Docker 默认的 seccomp profile 允许大约 300 多个系统调用，拦掉大约 40 多个，包括：

- `mount` / `umount2`（所以容器里基本挂不了东西）
- `reboot`（不然你重启的是宿主）
- `init_module` / `delete_module`（不能改内核模块）
- `kexec_load`、`swapon`、`clock_settime`……

**一个关键细节**：seccomp 和 capabilities 是**叠加**的。就算你想办法拿到了 `CAP_SYS_ADMIN`，如果 seccomp 还在拦 `mount`，你依旧挂不了。两道锁，得同时开。

这也解释了一个常见困惑："我明明 `--cap-add=SYS_ADMIN` 了，怎么还不行？"——因为你还得 `--security-opt seccomp=unconfined`。（当然，两个都加上，你基本上就把容器安全关掉了。）

#### 4.4 AppArmor / SELinux：第四道墙

这两个属于 LSM（Linux Security Module），做的是**强制访问控制**：即使文件权限位允许、capability 也够，策略不允许就是不行。

Ubuntu 系的 Docker 默认带一个 `docker-default` AppArmor profile，RHEL/CentOS 系则是 SELinux。它们典型会拦：写 `/proc/sys/*`、写 `/sys/fs/*`、挂载操作、ptrace 容器外的进程。

**怎么发现是它在拦**：看宿主的 `dmesg`，会有 `apparmor="DENIED"` 或 `avc: denied` 字样。这是很多人想不到去看的地方——**容器里的报错很笼统，真正的原因写在宿主的内核日志里。**

#### 4.5 四道墙叠加起来

```
你的进程
   │
   ├─ namespace     → 你看不见别人的东西
   ├─ cgroups       → 你用不了太多资源
   ├─ capabilities  → 你没有关键的那几项权力
   ├─ seccomp       → 关键系统调用直接不让你叫
   └─ LSM           → 就算前面都过了，策略说不行就是不行
```

四道墙里，**只要有一道拦住，你就跑不了 Docker**。而共享平台通常四道都开着。

#### 【所以然】

> "root 不等于全能"是容器安全的地基。但请记住它有**两种实现方式**：默认 Docker 是"真 root 被削权"，rootless 是"假 root 被映射"。搞清楚你在哪条路上，排错才不会跑偏。

---

### 5. 容器怎么「存东西」：overlay 与写时复制

这一章直接对应我那个 `mount overlay: permission denied`。

#### 5.1 分层镜像与写时复制

先想一个问题：你本机拉了 10 个基于 `ubuntu:22.04` 的镜像，难道硬盘上存了 10 份 Ubuntu 根文件系统？

当然不是。镜像是**分层**的，10 个镜像共享同一份 Ubuntu 底层，各自只存自己的差异。

最好的类比是**透明塑料片**：

```
最上面：你运行时写的东西（可写层，容器专属）
         ↓ 看下去
  第4片：COPY 你的代码
  第3片：pip install torch
  第2片：apt install python3
  第1片：Ubuntu 22.04 基础系统
```

你从上往下看，看到的是一个**完整的、合并后的文件系统**。但硬盘上存的是分开的几片，而且下面四片是**只读共享**的——一百个容器用同一份。

**写时复制（copy-on-write）**​****就是这个机制的核心：你读一个文件，直接从只读层读；你要改它，系统先把它****​**复制**到最上面的可写层，你改的是那份副本。下面的共享层永远不变。

#### 5.2 overlayfs 的四层结构

Docker 默认的存储驱动 `overlay2`，底层就是内核的 overlayfs。它有四个角色：

|名字|作用|
| ----| ----------------------------------------------------------------------------|
|**lowerdir**|只读层，可以叠多个（就是镜像的各层）|
|**upperdir**|可写层，所有修改都落在这|
|**merged**|合并后的视图，也就是你在容器里看到的 `/`|
|**workdir**|overlayfs 内部用的临时工作目录（保证原子性），必须和 upperdir 同一个文件系统|

你可以手动玩一下（在有权限的机器上）：

```bash
mkdir -p /tmp/ov/{lower,upper,work,merged}
echo "我是底层" > /tmp/ov/lower/a.txt
sudo mount -t overlay overlay \
  -o lowerdir=/tmp/ov/lower,upperdir=/tmp/ov/upper,workdir=/tmp/ov/work \
  /tmp/ov/merged

cat /tmp/ov/merged/a.txt        # 我是底层
echo "被改了" > /tmp/ov/merged/a.txt
cat /tmp/ov/lower/a.txt         # 我是底层   ← 原件没动
cat /tmp/ov/upper/a.txt         # 被改了     ← 副本在这
```

一分钟，写时复制就看明白了。

#### 5.3 whiteout：怎么「删除」一个只读层里的文件

这个细节很有意思：底层是只读的，那我在容器里 `rm` 一个底层文件，发生了什么？

答案是：overlayfs 在 upperdir 里创建一个**字符设备文件（major=0, minor=0）** ，叫 whiteout。合并视图看到它就知道："这个文件被删了，尽管下面还有"。

```bash
rm /tmp/ov/merged/a.txt
ls -l /tmp/ov/upper/
# c--------- 1 root root 0, 0 ... a.txt    ← 看那个 c 和 0,0
```

**为什么要知道这个？**  因为它解释了一个坑：你在 Dockerfile 里写

```dockerfile
RUN wget 很大的文件.tar.gz && tar xf 很大的文件.tar.gz
RUN rm 很大的文件.tar.gz        # 想瘦身
```

结果镜像一点没变小。因为第二条 `RUN` 只是在新一层里写了个 whiteout 标记，**下面那层里的大文件原封不动地还在**，而且你又多了一层。想真瘦，必须写在**同一条** RUN 里。

#### 5.4 overlay 嵌套：真相没那么绝对，但结果一样

很多文章说"内核不支持 overlay 套 overlay"。准确的说法应该是：

overlayfs 长期不允许把另一个 overlayfs 用作 **upperdir**。原因是 upperdir 必须支持可信的扩展属性（xattr）来存 whiteout 和 opaque 标记，而 overlayfs 自己对 xattr 的语义支持不完全。较新的内核对部分嵌套场景做了放宽，但——

**Docker 的 overlay2 驱动会主动检测并拒绝。**  你会看到：

```
ERROR: could not use overlay2 driver on this system:
       backing file system is unsupported for this graph driver
```

所以实践上结论没变：在容器里再跑 Docker，**overlay2 基本用不了**，只能退而用 `fuse-overlayfs`（需要 `/dev/fuse`）或 `vfs`（不需特殊能力，但每层完整复制，慢得绝望且占盘翻倍）。这是 DinD 的第一个坑。

#### 5.5 【隐蔽大坑】upperdir 所在的文件系统要支持 xattr

这一条在共享集群上坐死了无数人，但很少被提到。

overlayfs 的 upperdir 需要存两种元数据：`trusted.overlay.opaque`（目录不透明标记）和 whiteout。它们靠**扩展属性**存储。

而下面这些文件系统，要么不支持 xattr，要么不支持 `trusted.*` 命名空间：

- **NFS**（绝大多数学校/公司集群的 home 目录）
- **Lustre / GPFS / BeeGFS**（超算的并行文件系统）
- 某些配置下的 ZFS、tmpfs

**所以：如果你把 Docker 的 data-root 或者 apptainer 的 sandbox 放在 NFS 家目录里，就算你是真 root、权限全开，overlay 照样挂不上。**

这就是为什么中篇的诊断盒里有这一条：

```bash
findmnt -T $HOME -o TARGET,SOURCE,FSTYPE
# 如果 FSTYPE 是 nfs4 / lustre，立刻把工作目录换到本地盘（/tmp、/scratch、/local）
```

我后来回想，课题组那台机器的 `mount overlay: permission denied` 有相当大的概率就有这一层因素在里面。**同一个报错至少四种病因**，中篇会把它们完整拆开。

#### 5.6 容器删了 = 可写层没了

最后一个直接推论：可写层是绑在容器实例上的。容器一删，层就没了。

所以"我容器重启一下数据就没了"不是 bug，是**设计如此**。（准确地说：`docker restart` 不丢，因为容器还在；`docker rm` 后重建才丢。但很多平台的"重启实例"实际上是后者。）

这就直接引出下一章：**数据必须外挂。**

#### 【所以然】

> 理解了 CoW，你就同时理解了三件事：为什么镜像能省空间、为什么 `rm` 瘦不了镜像、为什么数据必须挂卷。
>
> 而理解了 upperdir 对文件系统的要求，你就提前避开了共享集群上最难查的那类报错。

---

### 6. 数据怎么活下来：持久化与挂载

上一章最后那句"可写层随容器一起消失"，直接导出了这一章的存在理由。

#### 6.1 三种挂载，分清楚

|类型|写法|数据存在哪|适合|
| ----------| ----| ------------| --------------------------------|
|bind mount|`-v /host/path:/container/path`|宿主任意路径|代码、数据集、checkpoint（**AI 场景 95% 用这个**）|
|volume|`-v myvol:/data`|Docker 管的 `/var/lib/docker/volumes/`|数据库、不关心具体位置的持久数据|
|tmpfs|`--tmpfs /tmp`|内存|临时文件、敏感数据|

有个很多人不知道的行为差异：

- **bind mount 目录在宿主不存在时，Docker 会自动建一个空目录**（这就是为什么你拼错路径时不报错，只是里面空空如也）
- **volume 第一次挂载时，会把镜像里该路径的内容拷贝进去；bind mount 不会，它直接遮盖**

第二条能解释一个经典翻车：你 `-v ./mycode:/workspace`，结果发现镜像作者预装在 `/workspace` 里的一堆东西全不见了——它们没被删，只是被你的目录盖住了。

#### 6.2 `/dev/shm`：默认 64MB 这个神坑

Docker 默认给容器的 `/dev/shm` 只有 **64MB**。

而 PyTorch 的 DataLoader 一旦 `num_workers > 0`，就靠共享内存在进程间传 tensor。于是你会看到：

```
RuntimeError: DataLoader worker (pid 1234) is killed by signal: Bus error.
# 或
ERROR: Unexpected bus error encountered in worker.
  This might be caused by insufficient shared memory (shm).
```

看到 **Bus error** 三个字，90% 是 `/dev/shm` 不够。

```bash
# 确认
df -h /dev/shm

# 解决
docker run --shm-size=32g ...
# 或直接用宿主的
docker run --ipc=host ...
```

这个坑在分布式训练里会变得更严重，下篇 §2 会展开讲。

#### 6.3 UID 不匹配：容器写的文件我删不掉

默认 Docker 容器里是 uid 0，而且（回忆一下 §4.2）**那就是宿主的真 root**。所以容器往 bind mount 里写的文件，在宿主上属主就是 root：

```bash
$ ls -l output/
-rw-r--r-- 1 root root 2.3G model.pt
$ rm output/model.pt
rm: cannot remove 'model.pt': Permission denied
```

共享机上这很讨厌——你得去求管理员帮你删自己的文件。

三种解法：

```bash
# 1. 启动时指定用户（最常用）
docker run -u $(id -u):$(id -g) ...

# 2. 镜像里就写好
# Dockerfile: RUN useradd -u 1000 -m appuser \n USER appuser

# 3. rootless docker / podman（UID 自动映射回你）
```

反过来，apptainer 天生没这个问题——它容器内外 UID 一致，这也是 HPC 集群喜欢它的原因之一。

#### 6.4 宿主文件系统的四个隐形地雷

这四个在实验室/集群环境里特别常见，而且报错都很误导人。

**雷一：home 在 NFS / Lustre 上**

```bash
findmnt -T $HOME -o TARGET,SOURCE,FSTYPE
# FSTYPE 显示 nfs4 / lustre / gpfs → 注意
```

上一章说过，overlay 的 `upperdir` 需要 xattr，而这些网络文件系统往往不支持。症状：`mount overlay: permission denied` 或 `invalid argument`——完全看不出和 NFS 有关。

解法：把容器存储目录指向本地盘。

```bash
export APPTAINER_CACHEDIR=/local/scratch/$USER/apptainer
export APPTAINER_TMPDIR=/local/scratch/$USER/tmp
# docker: /etc/docker/daemon.json 里改 "data-root"
```

**雷二：**​ **​`/tmp`​**​ ** 是个小 tmpfs**

```bash
df -h /tmp
# Size 2G，Filesystem tmpfs → 危险
```

apptainer 构建镜像、docker 解压层都在 `/tmp` 里展开。一个 20G 的 PyTorch 镜像直接把内存吃爆，报错是 `no space left on device`——你去 `df -h /` 发现根盘还剩一堆空间，一脸迷茫。

**雷三：磁盘配额（quota）**

```bash
quota -s        # 看自己的配额
lfs quota -h -u $USER /lustre   # Lustre 版
```

配额用完的报错也是 `no space left`，但 `df` 显示很充裕。这是集群上最容易浪费时间的误导。

**雷四：**​**​`noexec`​**​ ** / **​**​`nosuid`​**​ ** 挂载选项**

```bash
findmnt -T /path -o TARGET,OPTIONS
```

如果你的 home 或 scratch 带 `noexec`，那里面的二进制根本不能执行。症状是 `Permission denied` 或 `cannot execute binary file`，你会反复 `chmod +x` 而没任何用。

#### 【所以然】

> 容器把文件系统虚拟化了，但它**虚拟不掉宿主文件系统的物理现实**：xattr 支不支持、配额够不够、能不能执行。所以很多容器报错，真正的答案在 `findmnt` 里。

---

### 7. 容器怎么上网

网络这块日常开发里坑相对少（因为 `-p` 基本就够用了），但到了分布式训练就会变成主要矛盾。这里把原理讲清楚，下篇直接用。

#### 7.1 四种网络模式

|模式|含义|何时用|
| --------| -----------------------------------------| -----------------------------|
|`bridge`（默认）|容器在虚拟网桥上，有自己的 IP，出去要 NAT|单机服务、开发|
|`host`|直接用宿主网络栈，无隔离|**多机分布式训练、高性能网络**|
|`none`|只有 lo|完全不需要网络的任务|
|`container:xxx`|和另一个容器共享网络|sidecar、K8s Pod 内部就是这个|

#### 7.2 bridge 模式的真实面目

装完 Docker 后你会多一块网卡：

```bash
ip addr show docker0
# 172.17.0.1/16
```

每启一个容器，Docker 就创建一对 **veth pair**（虚拟网线），一头在容器的 network namespace 里叫 `eth0`，另一头插在 `docker0` 网桥上。

容器访问外网时，走的是 `MASQUERADE`（SNAT），把源 IP 改成宿主的。

#### 7.3 `-p 8080:80` 到底干了什么

它不是什么魔法，就是一条 **iptables DNAT 规则**：

```bash
sudo iptables -t nat -L DOCKER -n
# DNAT tcp -- 0.0.0.0/0  0.0.0.0/0  tcp dpt:8080 to:172.17.0.2:80
```

知道这个之后，两个常见现象就好理解了：

1. **为什么容器端口能绕过防火墙**：DNAT 发生在 `nat` 表，而很多人的防火墙规则写在 `filter` 表的 `INPUT` 链上——容器流量走的是 `FORWARD` 链。所以你以为封了端口，其实没封。**这是真实发生过很多次的安全事故。**
2.  **​`-p 127.0.0.1:8080:80`​**​ ** 和 **​ **​`-p 8080:80`​**​ ** 完全不同**：后者是向全世界开放的。在公网 IP 的机器上跑 Jupyter 时特别要命。

#### 7.4 容器之间怎么互相找到

默认 bridge 网络**不支持用容器名互访**。得自己建一个：

```bash
docker network create mynet
docker run -d --network mynet --name redis redis
docker run -it --network mynet alpine ping redis   # 能通
```

自建网络里 Docker 会跑一个内置 DNS（`127.0.0.11`），把容器名解析成 IP。

#### 7.5 为什么多机训练基本都用 `--network=host`

三个硬理由：

1. **性能**：bridge 模式每个包要过 veth + NAT，在 100Gbps 网络下这个开销很痛
2. **RDMA / InfiniBand 绕过内核网络栈**，NAT 对它没意义，而且会添乱
3. **地址一致性**：NCCL / torchrun 建连时互相交换 IP。bridge 模式下容器报的是 `172.17.0.x`，其他节点根本路由不到——现象就是**训练启动后永远卡在 **​**​`initializing process group`​**。

第三条是新手最常撞的墙，下篇 §2 会详细拆。

#### 【所以然】

> 容器网络不是新技术，就是 **network namespace + veth + iptables** 三个老零件拼出来的。你用 `ip`、`iptables` 这些老工具就能把它看透。

---

### 8. 镜像：你拉的那堆东西到底是什么

#### 8.1 OCI 标准：为什么镜像能跨工具用

你能 `apptainer pull docker://pytorch/pytorch`、`podman pull`、`skopeo copy`，是因为大家遵循同一套 **OCI Image Spec**。

一个镜像 = 三部分：

```
manifest.json    ← 清单：指向 config 和各层
 config.json     ← 元数据：环境变量、CMD、ENTRYPOINT、工作目录
layers/          ← 若干个 tar.gz，每个是一层文件系统差分
```

就这么简单。中篇 5.3 节那个"把镜像摊平成目录"的妙招，能成立就是因为这个结构是公开的、不依赖任何运行时。

#### 8.2 层缓存：为什么你改一行代码要重装全部依赖

Dockerfile 每一条指令生成一层。构建时从上往下比对，**一旦某层变了，后面所有层缓存全失效**。

错误写法：

```dockerfile
COPY . /app                    # 代码一改，这层就变
RUN pip install -r requirements.txt   # 于是依赖每次重装
```

正确写法：

```dockerfile
COPY requirements.txt /app/    # 依赖文件很少变
RUN pip install -r /app/requirements.txt   # 缓存命中
COPY . /app                    # 代码放最后
```

一个顺序调整，构建时间从 10 分钟变 10 秒。

#### 8.3 为什么 AI 镜像那么大

拆一下 `pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel` 的 20G：

|部分|大小量级|
| -----------------------| --------|
|Ubuntu base|~80MB|
|CUDA runtime|~2GB|
|**CUDA devel（nvcc、头文件、静态库）**| **~5GB**|
|cuDNN|~1.5GB|
|PyTorch + 预编译 kernel|~3GB|
|conda 环境及依赖|~2GB|

瘦身的三招：

1. **能用 **​**​`runtime`​**​ ** 就不用 **​**​`devel`​**。你只是推理的话根本不需要 nvcc，直接省 5G。（但如果要编译 flash-attn / 自定义算子，必须 `devel`）
2. **多阶段构建**：`devel` 里编译，把产物 `COPY --from` 到 `runtime`
3. **合并 RUN 并清缓存**：

```dockerfile
RUN apt-get update && apt-get install -y xxx \
    && rm -rf /var/lib/apt/lists/*
# 写成两条 RUN 的话，缓存已经存进上一层了，后面删也白删
```

第 3 条很多人不知道：**后面的层删掉前面层的文件，镜像不会变小**（上章讲的 whiteout 只是遮蔽）。

#### 8.4 【实用】磁盘预算公式

拉镜像前先算一算，避免拉到 90% 时 `no space left`：

> **需要的磁盘 ≈ 镜像压缩体积 × 2.5**

为什么是 2.5：下载的 tar.gz（1）+ 解压后的层（~2），中间还有瞬时共存。Docker Hub 页面上显示的是**压缩体积**，而 `docker images` 显示的是**解压后体积**，两者差 2-3 倍——很多人就是在这里估错的。

#### 8.5 拉不动镜像时的转运术

国内环境 + 集群无外网，这是日常。四种办法：

**方法 1：save / load（最无脑）**

```bash
# 能上网的机器上
docker pull pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime
docker save pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime | gzip > pt.tar.gz
# scp 过去
docker load < pt.tar.gz
```

**方法 2：skopeo（不需要 docker）**

```bash
skopeo copy docker://pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime \
            oci-archive:pt.tar
```

优点：两边都不需要 docker daemon，普通用户就能跑。

**方法 3：apptainer 直接转**

```bash
apptainer pull pt.sif docker://pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime
```

**方法 4：镜像加速器**

```bash
# 修改 /etc/docker/daemon.json
{ "registry-mirrors": ["https://xxx.mirror.aliyuncs.com"] }
# 没 root 的话，直接改镜像名
docker pull dockerproxy.com/pytorch/pytorch:xxx
```

#### 8.6 为什么 RL 训练栈喜欢把东西全塞镜像里

跟我这次撞的墙直接相关。像 Relax / veRL / OpenRLHF 这类 RL 训练框架，依赖链长得可怕：

```
PyTorch + CUDA + NCCL
  + vLLM（又带自己的 CUDA 算子）
  + flash-attn（需要编译，对 torch 版本敏感）
  + Ray（分布式调度）
  + DeepSpeed / FSDP
  + transformers / datasets / 各种 tokenizer
```

这些东西之间的版本约束非常硬（flash-attn 必须匹配 torch 的 ABI，vLLM 必须匹配 CUDA 小版本），手装一个下午都不一定能跑通。

所以官方一律给镜像——**镜像在这里的作用不是"隔离"，而是"依赖解算结果的快照"** 。作者花了一天解出来的版本组合，直接冻结给你。

这也意味着：当你用不了容器、只能裸装时，你真正丢掉的不是隔离性，而是**那份解算结果**。所以中篇 5.5 节才说：裸装时一定要把 Dockerfile 当安装手册读，版本号一个不能改。

#### 8.7 版本固定：`latest` 是个陷阱

```bash
# 差
docker pull pytorch/pytorch:latest

# 好
docker pull pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

# 最好（钉到 digest，完全不会变）
docker pull pytorch/pytorch@sha256:9c1f9a...
```

拿 digest：

{% raw %}
```bash
docker inspect --format='{{index .RepoDigests 0}}' <image>
```
{% endraw %}

论文复现、实验报告里写 tag 是不够的——tag 可以被重新推送。digest 不能。

#### 【所以然】

> 镜像不是魔法盒子，就是一堆带元数据的 tar。看懂这一点，你就能在没有 docker 的机器上把它拆开用。

---

### 9. 从单机到集群：你为什么活在一个 Pod 里

这一章不是教你用 K8s，而是回答一个很实际的问题：**为什么你买的"云 GPU 服务器"里没有 Docker。**

#### 9.1 三个概念，一句话一个

- **Pod**：一组共享网络和存储的容器（就是 §7.1 那个 `container:xxx` 模式）。K8s 调度的最小单位。
- **Deployment**：声明"我要 3 个这样的 Pod 一直跑着"，挂了自动拉起来。
- **Service**：给一组漂移不定的 Pod 一个固定入口。

#### 9.2 判定：我是不是在 Pod 里

三种方法，一秒出结果：

```bash
# 1. 看 cgroup 路径
cat /proc/1/cgroup
# 包含 kubepods → 你在 K8s Pod 里，基本别想 docker 了

# 2. 看服务账号
ls /var/run/secrets/kubernetes.io/serviceaccount/

# 3. 看环境变量
env | grep KUBERNETES
# KUBERNETES_SERVICE_HOST=10.96.0.1  → 实锤
```

我那天在魔搭 Notebook 上跑第一条，看到 `kubepods` 那一刻，其实问题就已经解决了——只不过当时我看不懂。

#### 9.3 为什么 Pod 里没有 Docker（也不应该有）

四个理由，每个都很硬：

1. **K8s 自己早就不用 Docker 了**。1.24 之后移除了 dockershim，现在直接用 containerd 或 CRI-O。宿主上可能根本就没装 Docker。
2. **资源会失控**。你在 Pod 里启的容器不在 K8s 的资源账本上，直接破坏调度器的判断。
3. **生命周期不匹配**。Pod 被驱逐时，你里面起的容器可能变成孤魂进程。
4. **安全**（根本原因）。中篇 §3 详述。

#### 9.4 那在 Pod 里该怎么干活

**接受一个事实：你已经在容器里了。**

你想要的"环境隔离"已经实现了，你真正缺的只是"那个镜像里的依赖"。于是选项只有三个：

1. **让平台用你的镜像启动**（魔搭、AutoDL、各家云都支持自定义镜像）——**这是正解**
2. 用户态方案把镜像内容弄出来（udocker / 摊平，中篇 §5）
3. 直接按 Dockerfile 裸装（中篇 5.5）

我那天花了两小时去试第四个不存在的选项：在 Pod 里装 Docker。

#### 【所以然】

> 很多时候你不是"用不了容器"，而是**已经在容器里了**。弄清楚自己的位置，比学会任何命令都重要。

---

### 上篇小结

把上面九章压成一张图：

```
一个普通进程
   ↓ namespace（八种）        → 看不到别人
   ↓ cgroups                   → 用不多资源
   ↓ capabilities/seccomp/LSM  → 干不了坏事
   ↓ overlayfs                 → 有自己的根目录
   ↓ veth + iptables           → 有自己的网络
= 一个容器
```

没有一行是 Docker 发明的。Docker 只是把这五步包成了一条命令。

**而这五步里的每一步，都需要内核把某个能力交给你。中篇就来看看，当内核不交的时候，会发生什么。**

---

## 中篇 ·《为什么你的服务器跑不了 Docker——以及跑不了到底该怎么办》

> 系列共三篇。这是最实用的一篇，可以独立阅读。
>
> 如果你现在正对着一个报错，从第 0 章的诊断盒开始，三十秒内应该能定位到你属于哪一类环境。想知道"为什么"，去读上篇。

> **适用范围与版本说明**（先看这一段，能省你很多时间）
>
> - 默认背景是 Linux 5.15+、Docker 24+、**cgroup v2**。文中涉及 cgroup v1 的部分只在较老的机器上才用得到。
> - 所有镜像 tag、驱动版本号都只是**写作当时的示例**，请换成你自己环境里的实际版本，不要直接照抄。
> - 命令里凡是带 `sudo` 的，都意味着“需要管理员”；你在只有普通用户权限的机器上直接跑是一定失败的。
> - 内核行为、安全策略、平台限制都在变。文中的**判定命令比结论更保值**——当结论和你机器上的输出矛盾时，以输出为准。

---

### 0. 三十秒诊断盒（先给答案，再讲道理）

把这几条命令一次贴进去，不用理解，先看输出：

```bash
echo "=== 1. 我在不在容器/Pod 里 ==="
cat /proc/1/cgroup
systemd-detect-virt -c 2>/dev/null || echo "(命令不存在)"

echo "=== 2. 我有哪些权力 ==="
grep CapEff /proc/self/status
# 把上面输出的十六进制值填进去：
# capsh --decode=00000000a80425fb

echo "=== 3. 能不能建 user namespace（rootless 的前提）==="
unshare -Ur echo ok
cat /proc/sys/user/max_user_namespaces 2>/dev/null

echo "=== 4. fuse 设备在不在（apptainer/podman 常需要）==="
ls -l /dev/fuse

echo "=== 5. 我的家目录是什么文件系统 ==="
findmnt -T $HOME -o TARGET,SOURCE,FSTYPE

echo "=== 6. docker 到底是什么状态 ==="
docker info 2>&1 | head -20
```

#### 怎么读这个输出

```
第 1 条输出里有 kubepods？
  └─ 是 → 你在 K8s Pod 里。基本不用想了，跑不了 Docker。跳到第 5 章。
  └─ 有 /lxc/ 或 /docker/ → 你在容器里。同样跳第 5 章。
  └─ 只有 0::/ 或 /init.scope → 你在真机或完整 VM 上，有戏，继续看。

第 3 条报 Operation not permitted？
  └─ 是 → rootless 路线（podman / rootless docker）也堵死了。
         只剩 udocker / proot / 找管理员。

第 4 条 /dev/fuse 不存在？
  └─ 是 → apptainer 挂 sif、fuse-overlayfs 全部不可用。
         但 udocker 的 proot 模式不需要它 —— 这是你的救命稻草。

第 5 条 FSTYPE 是 nfs / lustre / gpfs？
  └─ 是 → 别把镜像层、conda 环境放在家目录。
         overlay 的 upperdir 在这些文件系统上根本挂不起来（缺 xattr 支持）。
         这是共享集群里最隐蔽的一个坑。

第 6 条报 Cannot connect to the Docker daemon？
  └─ 结合第 1 条判断：在 Pod 里 = 平台不给；在真机上 = 可能只是没起服务或没进 docker 组。
```

#### 一句话预告

**跑不了 Docker，不等于跑不了容器。**

这句话是这整篇文章最重要的一句。Docker 只是容器的一种实现，而且是**要求最高**的那一种（它要 daemon、要 root、要挂 overlay）。你的镜像照样可以用别的方式跑起来，第 5 章给了整整一棵决策树。

---

### 1. 先把「服务器」这个词拆开：五类环境，五种命运

大部分"为什么我跑不了 docker"的困惑，都源于把很不一样的东西统称为"服务器"。我买的 ECS 是服务器，学校的 H100 是服务器，AutoDL 租的实例也叫服务器——但它们在容器这件事上，待遇完全不同。

|类型|典型例子|你是 root 吗|能跑 Docker 吗|该走哪条路|
| ----| ------------------------------------------| --------------------| ---------------| ----------------------------------------------|
|**① 裸金属 / 完整 VM**|自购服务器、阿里云 ECS、AWS EC2|真 root|✅ 能|直接 docker，没什么好说的|
|**② 云容器实例**|阿里云 DSW / 魔搭 Notebook、AutoDL、Colab|假 root（在 Pod 里）|❌ 基本不能|用平台的"自定义镜像启动"；退而求其次用 udocker|
|**③ HPC 共享集群**|课题组 H100、超算、公司训练集群|❌ 普通用户|❌ 不能|enroot+pyxis 或 apptainer；问管理员|
|**④ 受限 VM**|禁嵌套虚拟化、禁 modprobe、内核裁剪过的 VM|真 root|⚠️ 看缺哪一项|逐项诊断，通常可以修|
|**⑤ 容器内（DinD 场景）**|CI runner、已经在容器里了|看配置|⚠️ 很难|sysbox / 挂 socket / 换平台|

#### 我那三次撞墙，分别属于哪一类

这个表最有价值的地方是：**它告诉你不同的墙要用不同的方法翻。**

- **魔搭 Notebook（DSW）**  → 第 ② 类。`/proc/1/cgroup` 里明晃晃写着 `kubepods`，我本身就是 K8s 调度出来的一个 Pod。Pod 里想再跑 Docker，等于在笼子里开笼子，平台一定不会给我这个权限。**这条路从一开始就不通，不是我操作有问题。**
- **课题组 H100** → 第 ③ 类（也可能带一点 ④）。`mount overlay: permission denied`，而且我"是 root"。这里要注意：sudo 出来的 root 也可能因为机器本身在 LXC 里、或者 sysctl 禁了 userns、或者目标目录在 NFS 上而挂不了 overlay。**同一个报错至少四种病因**，第 4 章会拆。
- **apptainer + sif** → 还是第 ③ 类，但换了个死法。`/dev/fuse` 不存在 → squashfs 挂不上 → sif 打不开。这说明我用的是**非 setuid 模式**的 apptainer，它必须靠 FUSE 在用户态挂载。

三次撞墙，看起来是三个不同的错，其实背后是同一句话：**这些环境在设计上就不打算把挂载权交给我。**

---

### 2. 跑起一个 Docker，到底要问内核要什么

把 `docker run hello-world` 这一行拆开，内核要配合的事情是这样一串：

**① 创建 namespace** —— 需要 `CAP_SYS_ADMIN`（建 mnt/net/pid/uts/ipc namespace 都要它）

**② 挂载 rootfs** —— 需要 `CAP_SYS_ADMIN`（`mount` 系统调用），而且需要一个能用的存储驱动：

- `overlay2`：要求内核支持 overlayfs，且 upperdir 所在文件系统支持 xattr
- `fuse-overlayfs`：要求 `/dev/fuse` 存在且可用
- `vfs`：不要求特殊能力，但极慢极占盘（每层完整复制）

**③ pivot_root 切换根目录** —— 需要 `CAP_SYS_ADMIN`

**④ 建 cgroup 写限额** —— 需要对 cgroup 文件系统的写权限，或者 cgroup v2 的委派

**⑤ 配网络** —— 建 veth pair、改 iptables，需要 `CAP_NET_ADMIN`

**⑥ 整个过程不被 seccomp 拦** —— 默认 seccomp profile 会拦 `mount`、`pivot_root`、`unshare` 里的一部分

**⑦ 不被 AppArmor / SELinux 拦**

#### `CAP_SYS_ADMIN`：那个没被拆干净的 root

上面这串里，`CAP_SYS_ADMIN` 出现了三次。这不是巧合。

capabilities 的设计初衷，是把 root 那个"什么都能干"的超级权力拆成几十个细粒度开关，用哪个给哪个。这个想法很好，但实现的时候有个历史包袱：**很多不好归类的操作，全都塞进了 **​**​`CAP_SYS_ADMIN`​**。

结果就是这一个 capability 里装着：`mount` / `umount` / `pivot_root` / `setns` / `swapon` / `sethostname` / 改 cgroup / 很多 ioctl……内核社区自己都吐槽它是 "the new root"。

**所以你可以这么理解：给一个容器 **​**​`CAP_SYS_ADMIN`​**​ **，约等于把整台机器给它。**  这就是为什么所有共享平台都把它卡得死死的，也是为什么"求管理员给我 SYS_ADMIN"通常会被拒绝——你要的不是一项权限，你要的是半个 root。

#### 对照一下：受限环境剥夺了哪几项

|需要的能力|K8s Pod（DSW）|HPC 集群普通用户|完整 VM|
| -----------------| -------------------------| -------------------------| -------|
|`CAP_SYS_ADMIN`|❌ 默认不给|❌ 不给|✅|
|挂 overlay|❌|❌|✅|
|`/dev/fuse`|❌ 需 Pod 显式声明 device|⚠️ 看管理员有没有建节点|✅|
|建 user namespace|⚠️ 常被 sysctl 关掉|⚠️ 看配置|✅|
|写 cgroup|❌ 由 kubelet 接管|❌ 由 Slurm 接管|✅|
|改 iptables|❌|❌|✅|

看这张表就明白了：不是某一项没给，是**整排都没给**。指望通过某个 flag 绕过去，方向就错了。

---

### 3. 平台为什么宁可全禁：三个不可协商的理由

很多人（包括之前的我）的第一反应是："这不是故意为难人吗？给个权限能死啊？"

真去了解一下就会发现，平台方在这件事上几乎没有选择余地。

#### 理由一：容器逃逸——特权容器等于物理机钥匙

上篇讲过，容器的隔离是"软"的：它是内核里的一堆检查逻辑。一旦你手里有了挂载权，这些检查就可以被绕开。

最经典的一类思路是这样的：容器里如果有 `CAP_SYS_ADMIN`，我就能挂载宿主的设备或者 cgroup 文件系统。cgroup v1 有个 `release_agent` 机制——当一个 cgroup 里最后一个进程退出时，内核会**以宿主 root 身份**执行你指定的那个脚本。于是攻击者只需要：挂上 cgroup、写一个指向容器 rootfs 里某个脚本的 `release_agent`、让 cgroup 清空。几行 shell，宿主机 root 到手。

类似的路子还有很多（`/proc/sys/kernel/core_pattern`、劫持宿主 runc 二进制的 CVE-2019-5736、通过 `/proc/self/exe` 的各种花样）。共同点是：**它们都以"容器有挂载或写宿主敏感路径的能力"为前提**。

所以平台的逻辑很简单：把这个前提掐掉，上面所有攻击一次性全废。

#### 理由二：多租户——一台机器上有几百个陌生人

一台 8 卡 A100 的物理机，平台可能同时跑着几十个用户的 Pod。你的邻居是谁，你不知道，平台也不敢假设他是好人。

在这个前提下，"给张三开个口子"这件事根本不成立：内核漏洞不认人，张三能逃逸，李四就能逃逸。平台唯一理性的策略是**对所有人一视同仁地全禁**。

这也解释了一个现象：为什么你自己买的云主机（ECS）能随便玩 Docker，而看起来更"高级"的 GPU Notebook 反而不行——因为 ECS 是给你一台独占的虚拟机（隔离在 Hypervisor 那一层，你在里面折腾不影响别人），而 Notebook 是共享物理机上的一个容器。**不是贵不贵的问题，是隔离层次不同。**

#### 理由三：责任与计费边界

这条最少被提到，但在商业上很关键。

平台按 Pod 来计量资源、来做调度、来做故障恢复。如果你在 Pod 里又自己起了一个 Docker daemon，那这个 daemon 起的容器，平台是看不见的：

- 它吃的内存算谁的？cgroup 层级会乱掉
- 节点要驱逐、要迁移，你那些容器怎么办？平台不知道它们存在
- 出了安全事故，责任怎么划？

所以哪怕技术上能给，运营上也不愿意给。

#### 【所以然】

> 不是"云不让你用 Docker"，而是"**容器化的、多租户的环境，从架构上就没法把挂载特权交出来**"。
>
> 你撞的不是一堵为难你的墙，是一堵承重墙。

---

### 4. 报错鉴别诊断表（本篇核心资产）

这一章是我写整个系列的初衷。

我以前的做法是：报错 → 贴给大模型 → 拿到一条命令 → 试。问题在于，**同一个报错往往有好几种病因，而大模型只会给你最常见的那一种的解法**。如果你恰好不是那种，就会陷入"试了没用→再问→又一条命令"的死循环。

所以下面每一条都是四列：**报错 → 可能病因（多个）→ 判定命令 → 解法**。先判定，再动手。

---

#### 4.1 `Cannot connect to the Docker daemon at unix:///var/run/docker.sock`

|可能病因|判定命令|解法|
| ---------------------------------------| ---------| ----------------------------------------|
|① 你根本在 Pod/容器里，平台没给 daemon|`cat /proc/1/cgroup` 看有无 `kubepods`/`docker`|**没救**，跳到第 5 章换路|
|② daemon 没启动|`systemctl status docker`|`sudo systemctl start docker`|
|③ daemon 启动失败了|`journalctl -u docker -n 50`|看日志里的真实原因（常是存储驱动或磁盘）|
|④ 你不在 docker 组里|`id \| grep docker`|`sudo usermod -aG docker $USER` 然后**重新登录**|
|⑤ socket 路径不对|`echo $DOCKER_HOST`；`ls -l /var/run/docker.sock`|修正环境变量|

> ⚠️ 第 ④ 条提醒：加入 docker 组**等于给了 root 权限**（能挂宿主根目录跑特权容器）。这也是共享集群管理员永远不会把你加进去的原因。

---

#### 4.2 `mount overlay: permission denied` / `operation not permitted`

这个是我在课题组 H100 上撞的那个，也是最值得拆的一个。

|可能病因|判定命令|解法|
| --------------------------------| ------------| -----------------------------|
|① 你本身就在容器/LXC 里，没有 `CAP_SYS_ADMIN`|`grep CapEff /proc/self/status` + `capsh --decode=<值>`，看有无 `cap_sys_admin`|无解，换路（第 5 章）|
|② user namespace 被 sysctl 禁了|`unshare -Ur echo ok`；`cat /proc/sys/user/max_user_namespaces`|管理员改 sysctl；否则无解|
|③ **目标目录在 NFS/Lustre 上，不支持 xattr**|`findmnt -T <目录> -o FSTYPE`|**把工作目录换到本地盘**（`/tmp`、`/scratch`、`/local`）|
|④ AppArmor/SELinux 拦截|宿主上 `dmesg \| grep -Ei 'apparmor.*DENIED\|avc: *denied'`|调整策略（需管理员）|
|⑤ 内核没编 overlayfs|`grep overlay /proc/filesystems`|`modprobe overlay`（需 root），不行就换存储驱动|

**病因 ③ 是最容易被忽略的。**  它的鬼地方在于：你明明是 root，权限全开，报的却是 permission denied——因为不是你没权限，是**那个文件系统存不了 overlay 需要的元数据**。而学校集群的 home 目录十个有九个是 NFS。

---

#### 4.3 `fuse: device not found, try 'modprobe fuse' first` / `/dev/fuse: No such file`

这是我 apptainer 那一次的报错。

|可能病因|判定命令|解法|
| -------------------------------| ---------------| ------------------------------------|
|① 宿主没加载 fuse 模块|`lsmod \| grep fuse`|`sudo modprobe fuse`（需 root）|
|② 你在容器里，设备节点没挂进来|`ls -l /dev/fuse`|跟管理员要：Pod 加 device 声明，或 `docker run --device /dev/fuse`|
|③ 节点存在但权限不够|`ls -l /dev/fuse` 看权限位|`chmod 666 /dev/fuse`（需 root）|
|④ apptainer 是**非 setuid 安装**，必须靠 FUSE|`apptainer --version` + `ls -l $(which apptainer)` 看有无 s 位|装 setuid 版（需管理员），或绕开 sif|

**关于 ④，多说两句。**  很多人以为"apptainer 不需要 root"。准确地说：

- **setuid 模式**：apptainer 的核心二进制带 setuid 位，它自己瞬间提权去挂 squashfs。你不需要 root，但**安装的时候需要 root 把 setuid 位设上**。
- **非 setuid 模式**（pip/conda 装的、或者管理员出于安全关掉的）：只能在用户态靠 `squashfuse` 挂，而那**必须有 **​ **​`/dev/fuse`​**。

我当时就是后者，而且机器上根本没有 `/dev/fuse` 这个节点。两条路同时断了。

**临时绕过去的办法**（不需要 fuse）：

```bash
# 不挂载，直接把 sif 里的 squashfs 解出来
unsquashfs -d rootfs xxx.sif       # 有时需要先用 apptainer sif dump 取出数据分区
# 然后用 proot 进去
proot -R rootfs -w / /bin/bash
```

---

#### 4.4 `newuidmap: Permission denied` / `cannot setup user namespace`

这是 **rootless 路线专属**的报错（podman / rootless docker / buildah）。

|可能病因|判定命令|解法|
| ------------------------| -------------| -----------------|
|① `/etc/subuid` `/etc/subgid` 里没你|`grep $USER /etc/subuid /etc/subgid`|管理员执行 `usermod --add-subuids 100000-165535 $USER`|
|② `newuidmap` 丢了 setuid 位|`ls -l $(which newuidmap)`，看有无 `s`|重装 `shadow-utils` / `uidmap` 包|
|③ userns 被内核参数禁用|`cat /proc/sys/user/max_user_namespaces`（为 0 则禁）|`sysctl -w user.max_user_namespaces=15000`（需 root）|
|④ Debian 系的额外开关|`sysctl kernel.unprivileged_userns_clone`|设为 1（需 root）|

---

#### 4.5 `no space left on device`（但 df 看着还有空间）

|可能病因|判定命令|解法|
| -----------------------------| --------| ---------------------------------|
|① 真的满了（镜像层吃盘）|`docker system df -v`|`docker system prune -a`|
|② **inode 耗尽**（小文件太多）|`df -i`|清理悬空镜像，或换大 inode 的分区|
|③ `/tmp` 是小 tmpfs，解压时爆了|`df -h /tmp`|`export TMPDIR=/data/tmp`|
|④ quota 限额（共享集群常见）|`quota -s` 或 `lfs quota -u $USER /lustre`|换目录或申请扩容|
|⑤ docker data-root 在小分区|`docker info \| grep "Docker Root Dir"`|改 `/etc/docker/daemon.json` 的 `data-root`|

> 镜像盘算式：**磁盘需求 ≈ 压缩体积 × 2.5**（拉下来的压缩层 + 解压后的层 + 可写层）。一个标称 20G 的 PyTorch 镜像，给 50G 盘真的不宽裕。

---

#### 4.6 `OOMKilled` / 退出码 137

|可能病因|判定命令|解法|
| -------------------------------| ----------------| --------------------------|
|① 容器内存限额太小|`cat /sys/fs/cgroup/memory.max`|调大 `--memory`，或改小 batch|
|② `/dev/shm` 爆了（伪装成 OOM）|`df -h /dev/shm`|`--shm-size=32g`|
|③ 程序读到宿主内存数字自动调参|容器内 `free -h` vs `cat /sys/fs/cgroup/memory.max` 对比|手动设参数，不依赖自动探测|
|④ 真的泄漏|监控 `memory.current` 曲线|改代码|

> 重要：容器里的 `free -h` 和 `top` 看到的是**宿主**的内存，不是你的限额。要看限额必须读 cgroup 文件。

---

#### 4.7 `port is already allocated` / 服务起了但外面访问不了

|可能病因|判定命令|解法|
| ------------------------------| ---------------| --------------|
|① 端口被占|`ss -tlnp \| grep <端口>`|换端口|
|② 忘了 `-p` 映射|`docker ps` 看 PORTS 列|加 `-p 8080:8080`|
|③ **服务只监听 127.0.0.1**|容器内 `ss -tln`|改成监听 `0.0.0.0`|
|④ 云安全组/防火墙没放行|云控制台|放行|
|⑤ host 网络模式下端口直接撞了|`docker inspect` 看 NetworkMode|换端口或换模式|

第 ③ 条是新手头号坑：很多框架（Flask、Jupyter、vLLM）默认只监听 localhost。在宿主上这没问题，在容器里 localhost 是**容器自己的** localhost，外面永远进不来。

---

#### 4.8 `nvidia-container-cli: initialization error` / 容器里看不到 GPU

|可能病因|判定命令|解法|
| -----------------------------| ---------| ---------------------------|
|① 忘了加 `--gpus all`|看命令行|加上|
|② toolkit 没装|`docker info \| grep -i runtime`|装 nvidia-container-toolkit|
|③ 宿主驱动就有问题|宿主上 `nvidia-smi`|先修宿主|
|④ 驱动升级了没重启|`cat /proc/driver/nvidia/version` vs `nvidia-smi`|重启，或 `nvidia-smi -r`|
|⑤ apptainer 的 `--nv` 漏挂库|换 `--nvccli` 试|用 `--nvccli`|
|⑥ cgroup device 白名单不允许|`ls /dev/nvidia*` 在容器内|受限环境，找管理员|

（这一块在下篇有完整的排查树。）

---

### 5. 【最重要的一章】跑不了 Docker，到底怎么把环境跑起来

前面四章都在诊断，这一章治病。

因为说到底，你要的不是 Docker，你要的是**把那个镜像里的环境跑起来**。这两件事不是一回事。

下面按侵入性从低到高排序，**从上往下试**。

#### 5.1 第一优先：问平台能不能「用自定义镜像启动实例」

这是我踩完坑才想明白的一件事，也是最大的思维盲区：

**你在 Pod 里跑不了 Docker，但平台本身就是用你的镜像启动 Pod 的。**

你一直想在笼子里开笼子，而平台早就允许你"指定这个笼子长什么样"。

- **阿里云 DSW / 魔搭**：创建实例时选"自定义镜像"，先把镜像推到 ACR（阿里云容器镜像服务），启动时选它
- **AutoDL**：支持上传自定义镜像，也支持从已有实例制作镜像
- **公司/学校的 K8s 平台**：提交任务时写 `image:` 字段

如果你手里没有一台能 `docker build` 的机器，可以：用云厂商的镜像构建服务（ACR 有构建流水线）、用 GitHub Actions 构建后推到 ghcr.io、或者就用官方镜像直接启动。

**这条路能走通的话，后面那些都不用看了。**

#### 5.2 udocker：受限环境里的救命稻草

如果平台不给你换镜像，那 **udocker** 是我推荐的第一选择。

它出自欧盟 INDIGO-DataCloud 项目（主要开发方是葡萄牙 LIP 实验室），本来是为了让高能物理的计算作业能在没有任何特权的 HPC 集群上跑容器。设计目标就一个：**什么特权都不要，也能把 docker 镜像跑起来**。

**它为什么能行**：它根本不真的“建容器”。它把镜像层解开成普通目录，然后用几种用户态技术让你的程序"以为"自己在容器里：

|执行模式|原理|需要什么|
| --------| --------------------------| -----------------|
|**P 模式（PRoot）**|用 `ptrace` 拦截系统调用，改写路径|**什么都不需要**，连 `/dev/fuse` 都不要|
|**F 模式（Fakechroot）**|`LD_PRELOAD` 拦截 libc 调用|不需特权，比 P 快|
|**R 模式（runc）**|真用 runc + user namespace|需要 userns 可用|
|**S 模式（singularity）**|调用已装的 apptainer|需要 apptainer|

**重点是 P 模式**。它靠 ptrace 在用户态模拟一切，不需要 root、不需要 mount、不需要 `/dev/fuse`、不需要 user namespace。只要你能在那台机器上跑普通程序，你就能跑 udocker。

**怎么用**：

```bash
# 装（纯 Python，不需管理员）
pip install udocker
udocker install

# 拉镜像（支持镜像加速地址）
udocker pull pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime

# 建容器并设为 P 模式
udocker create --name=mytorch pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime
udocker setup --execmode=P1 mytorch

# GPU！udocker 支持
udocker setup --nvidia mytorch

# 跑
udocker run -v $HOME/work:/work mytorch python train.py
```

**代价要说清楚**：

- P 模式靠 ptrace，**系统调用密集的工作负载会明显变慢**（大量小文件 IO、频繁 fork）。但纯 GPU 计算的部分几乎不受影响——CUDA kernel 跑在卡上，ptrace 管不着。
- 没有真正的隔离（它不是安全工具，是兼容工具）
- 网络就是宿主网络，没有端口映射这一说

对于"我只是想把这个训练任务跑完"这个需求来说，**这些代价完全可以接受**。

#### 5.3 把镜像「摊平」成目录，然后 proot 进去

如果连 udocker 都装不了（比如完全断网的环境），还可以手工拆。

思路很简单：**镜像就是一堆 tar 包，解开叠起来就是一个根文件系统。**

```bash
# 方法一：从 registry 直接搞下来（不需要 docker）
skopeo copy docker://pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime \
            oci-archive:torch.tar
umoci unpack --image torch.tar rootfs-bundle
# 得到 rootfs-bundle/rootfs/，就是完整的根文件系统

# 方法二：在别的机器上导出，拷过来
#（在能用 docker 的机器上）
docker create --name tmp pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime
docker export tmp | gzip > rootfs.tar.gz
#（拷到目标机器）
mkdir rootfs && tar xzf rootfs.tar.gz -C rootfs

# 然后进去
proot -R rootfs -w /workspace -b /dev -b /proc -b /sys \
      -b $HOME/data:/data /bin/bash
```

`proot` 的 `-R` 相当于 chroot，`-b` 相当于 bind mount。全部在用户态完成，不需任何特权。

如果你手里是 sif（像我那次）：

```bash
# sif 本质是个容器格式，里面装着 squashfs 分区
unsquashfs -d rootfs xxx.sif
# 若直接不行，先把数据分区 dump 出来：
apptainer sif list xxx.sif        # 看有哪些分区
apptainer sif dump 4 xxx.sif > fs.squash
unsquashfs -d rootfs fs.squash
```

#### 5.4 enroot + pyxis：去问你的集群管理员这一句

如果你在一个 **Slurm 集群**上（学校集群、超算、公司训练集群大多是），这一节可能直接解决你的问题。

**enroot** 是 NVIDIA 开发的无特权容器运行时，**pyxis** 是它的 Slurm 插件。装了之后，跑容器就是一行：

```bash
srun --container-image=pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime \
     --container-mounts=$HOME/work:/work \
     --gpus=8 \
     python /work/train.py
```

没有 daemon、不需要 root、GPU 自动透传、和 Slurm 的资源调度无缝对接。

**关键在于：很多集群已经装了，但没人告诉你。**  先自己查一下：

```bash
which enroot
srun --help | grep -i container
scontrol show config | grep -i plugin
```

有的话，你先前所有的折腾都白费了（我就是）。没有的话，这也是你向管理员提的最值得提的一个请求——它安全、官方维护、专为这种场景设计。

#### 5.5 彻底不用容器：从 Dockerfile 反推裸机安装脚本

有时候最快的路就是不用容器。尤其是当你发现镜像里其实就是一个 conda 环境加几个 pip 包的时候。

**反推 SOP**：

1. **拿到 Dockerfile**（项目仓库里通常有）。没有的话用 `skopeo inspect --config docker://<image>` 看历史，或者 `docker history --no-trunc`。
2. **分类里面的指令**：

   - `FROM nvidia/cuda:12.1.1-devel-ubuntu22.04` → 对应：你需要哪个 CUDA toolkit 版本（用 conda 装 `cudatoolkit` 或 module load）
   - `apt install xxx` → 系统库。没 root 的话用 conda 装对应的包（大多数都有）
   - `pip install xxx` → 直接照搬
   - `ENV` → 写进你的 activate 脚本
3. **用 micromamba 建环境**（比 conda 快很多，单个二进制文件，不需安装）：

```bash
curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xvj bin/micromamba
./bin/micromamba create -n relax python=3.10 -c conda-forge
eval "$(./bin/micromamba shell hook -s bash)"
micromamba activate relax
```

4. **装 PyTorch 时对齐驱动版本**（最容易错的一步）：

```bash
nvidia-smi | head -3     # 看 Driver Version（不是右上角的 CUDA Version）
# 驱动 >= 525.60 → 整个 CUDA 12.x 系列都能跑（cu121 / cu124 都行）
# 驱动 < 525    → 只能用 CUDA 11.x 的轮子，如 cu118
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

这里有个极容易踩的坑，值得单独说清楚。

很多人以为"想用 cu124 就必须把驱动升到 550"，其实不是。NVIDIA 从 CUDA 11 开始提供一个叫 **minor version compatibility**（小版本兼容）的东西：**只要驱动满足该大版本的最低要求，那个大版本下所有小版本的 CUDA 程序都能跑。**  具体到 CUDA 12，Linux 上的门槛是驱动 **525.60.13**——过了这条线，12.0 到 12.6 的轮子你都能装。

所以共享集群上那台驱动停在 535 、三个月没人敢升的机器，你完全不需要去求管理员升驱动。两个例外要记住：

- **新卡不在这个豆子里。**  新架构的 GPU 需要能认得它的驱动，这是硬要求，和 CUDA 版本兼容无关。
- **要自己编译就不一样了。**  装预编译轮子只要满足驱动门槛；但要编 flash-attn、apex 这类带自定义 kernel 的东西，你还需要一份**完整的 CUDA toolkit（nvcc）** ，而且它的版本最好和 torch 编译时用的对上。这个用 conda 装就行，不需 root：
  ```bash
  micromamba install -c nvidia cuda-toolkit=12.1
  nvcc --version    # 确认拿到的是刚装的那个
  ```

5. **验证**：

```bash
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.device_count())"
```

这条路的真实代价是：如果那个项目依赖很脏（自定义 CUDA 算子、需要编译 flash-attn / apex / 某个魔改版 vLLM），可能要花一整天。但好处是：**一旦装好就是你自己的，不依赖任何平台、任何特权、任何管理员的心情。**

一个实用技巧：装好之后用 `conda-pack` 把环境打包成 tar，下次换机器直接解压就能用，算是穷人版的镜像：

```bash
pip install conda-pack
conda-pack -n relax -o relax-env.tar.gz
# 新机器上
mkdir -p ~/envs/relax && tar -xzf relax-env.tar.gz -C ~/envs/relax
source ~/envs/relax/bin/activate
conda-unpack     # 修复硬编码路径
```

注意它不能跨 glibc 差异太大的系统（比如 CentOS 7 打包拿到 Ubuntu 24.04），但同一个集群内基本都行。

#### 5.6 向管理员申请的正确姿势

很多人发的邮件是这样的：

> 老师好，服务器上能不能装个 Docker？

基本必被拒。因为在管理员耳朵里，这句话等于"能不能给我 root"（参见本篇 §3）。

**正确姿势是：不要要权限，要一个具体能力。**  而且把风险说清楚。

四个请求，按对方答应概率从高到低排：

**请求 A：创建 **​ **​`/dev/fuse`​**​ **（风险最小）**

```bash
sudo mknod -m 666 /dev/fuse c 10 229
# 或在容器启动时加：--device /dev/fuse
```

话术："只需要一个设备节点，不需要 root。这是 apptainer 官方推荐的非特权模式依赖。"

**请求 B：装 setuid 模式的 apptainer（HPC 集群标配）**

```bash
# 管理员执行，一次性
apt install apptainer-suid   # 或 rpm 包
```

话术："apptainer 是专为 HPC 多租户设计的，不带 daemon，容器内外 UID 一致，没有 Docker 的提权问题。国内外超算中心普遍部署。"

**请求 C：放开非特权 user namespace**

```bash
sudo sysctl -w kernel.unprivileged_userns_clone=1
sudo sysctl -w user.max_user_namespaces=15000
# 并给用户分配 subuid/subgid
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
```

话术："这是 rootless podman / apptainer 的前提。RHEL8+ 和 Ubuntu 默认就是开的。"
—— 坦白说这一条被拒的概率不低，因为历史上 userns 确实是提权漏洞重灾区，很多安全基线明文要求关。被拒了不要纠缠。

**请求 D：装 enroot + pyxis（如果是 Slurm 集群）** 
话术："NVIDIA 官方的 Slurm 容器方案，计费和资源限制完全走 Slurm，比我们现在手动配环境好管。"
这一条对管理员有 sell point——它不是给你开口子，是帮他把口子堆回去。

**邮件模板**

```
主题：关于 xx 服务器容器环境的一个小请求

老师好，

我在 xx 机器上跑 xx 项目，需要一个包含 CUDA 12.1 + 自定义编译依赖的环境。
直接裸装会污染公共环境，所以想用容器。

我已经确认过：
- 机器上没有 docker，我理解多租户环境不适合装（docker 组等于 root），所以不申请这个
- 我想用 apptainer（无 daemon、UID 不变，是 HPC 集群的标准方案）
- 它在本机报 "fuse: device not found"，原因是 /dev/fuse 不存在

所以想麻烦您一件事（二选一即可）：
1. sudo mknod -m 666 /dev/fuse c 10 229   # 只创建设备节点，不涉及提权
2. 或者安装 apptainer-suid 包

如果都不方便，我会改用 udocker（纯用户态）或直接在 conda 里裸装，不需要您做任何操作，先告知一声。

谢谢！
```

最后那句"如果都不方便我自己有 Plan B"非常关键——它把邮件从"求你办事"变成"知会一声"，回复率会高很多。

#### 5.7 及时止损：什么时候该放弃容器

一个很朴素的判据：

**当你只需要在一台机器上跑一次实验时，容器带来的价值接近于零。**

容器的核心价值是**可移植**和**可重现**。如果你就在这一台机器上跑一个实验、跑完就完事了，那么花四小时搞容器 vs 花一小时 conda 裸装，后者完胜。

什么时候必须坚持容器：

- 需要在多台机器/集群上反复部署
- 依赖脏到裸装会要你命（比如需要特定 glibc、特定系统库版本）
- 需要交付给别人复现
- CI / 生产部署

我这次的 Relax 新手任务属于第一种。现在回头看，正确做法就是直接 micromamba 裸装，半小时搞定。

#### 【所以然】

> 没有 root 不等于没有容器。你失去的只是"把文件系统挂载成一层"这一个具体能力，而绕过它的办法至少有五种。
>
> 但也别忘了最后一条：**有时候最快的路就是不用容器。**

---

### 6. DinD：容器里跑容器，为什么那么难

很多人的真实处境是：我已经在一个容器里了（AutoDL、魔搭 DSW、公司的 K8s 开发机），想在里面再跑一个 Docker。

这就是 DinD（Docker in Docker）。它难在三个地方。

#### 6.1 难点一：overlay 套 overlay

上篇 5.6 节讲过：overlayfs 长期不允许把另一个 overlayfs 当作 `upperdir`。而你外层容器的根文件系统就是 overlay。

新内核（5.11+）放宽了部分场景，但 Docker 的 overlay2 驱动自己会主动拒绝，报：

```
failed to mount overlay: invalid argument
# 或
ERROR: could not use overlay2 driver on this system:
       backing file system is unsupported for this graph driver
```

#### 6.2 难点二：内层 dockerd 需要的能力，外层没给

内层 dockerd 要干的事和裸机上一模一样（本篇 §2 的七步）：建 namespace、mount、写 cgroup、改 iptables。而外层容器默认只有 14 个 capabilities、有 seccomp、cgroup 只读挂载。

所以官方 `docker:dind` 镜像的用法里那个 `--privileged` 不是懒，是真的需要。

#### 6.3 难点三：cgroup 层级委派

cgroup v2 需要外层把一个子树的写权限"委派"给内层。K8s 环境下 `/sys/fs/cgroup` 通常是只读挂载的，内层 dockerd 启动时就会报：

```
failed to create cgroup: read-only file system
```

#### 6.4 解法梯度（从容易到难）

**方案 0：挂 docker.sock（其实不是 DinD）**

```bash
docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli
```

叫 DooD（Docker outside of Docker）。容器里的 docker 客户端直接指挥**宿主的** daemon。

优点：没性能损失，没嵌套问题。
**致命缺点：这等于把宿主 root 送给了容器**（`docker run -v /:/host --privileged` 就接管全机）。而且路径语义很坑：你写 `-v ./data:/data`，那个 `./data` 是**宿主上的路径**，不是你当前容器里的。

**方案 1：privileged + vfs 存储驱动**

```bash
docker run --privileged docker:dind --storage-driver=vfs
```

`vfs` 不用 overlay，每层完整拷贝。能跑，但**磁盘占用爆炸**——一个 20G 的 PyTorch 镜像可能展开成 60G+。

**方案 2：fuse-overlayfs**

```bash
docker run --privileged --device /dev/fuse \
  docker:dind --storage-driver=fuse-overlayfs
```

磁盘友好得多，代价是用户态文件系统的性能损耗（大量小文件 IO 时明显变慢）。当然前提是你得有 `/dev/fuse`——而这恰恰是我那天没有的东西。

**方案 3：sysbox（最优雅，但需要管理员）**

sysbox 是一个替代 runc 的 OCI 运行时，它用 user namespace + 文件系统虚拟化让容器**不需要 privileged 也能跑 DinD**：

```bash
docker run --runtime=sysbox-runc -it nestybox/ubuntu-focal-systemd-docker
```

问题是它得在**宿主**上安装。你已经在容器里了的话，这条路不存在。

#### 6.5 为什么 AutoDL 这类平台 DinD 体验那么差

把上面三个难点套到这类平台上：

1. 你的实例本身就是一个非特权容器 → 拿不到 `--privileged`
2. 它不会给你 `/dev/fuse` → fuse-overlayfs 走不通
3. 磁盘配额就几十 G → vfs 驱动直接撑爆
4. cgroup 只读 → 内层 dockerd 启动失败

四条路全堵死。所以**在这类平台上尝试 DinD 基本是浪费时间**，直接走本篇 5.1（平台自定义镜像）或 5.2（udocker）。

#### 【所以然】

> DinD 难，本质上是因为**容器的隔离机制本来就不是为了"嵌套"设计的**。你在试图让一个被剥夺了内核能力的进程，去行使那些恰恰被剥夺的能力。

---

### 7. 换个运行时，到底绕开了什么（以及绕不开什么）

> 这一章比的是「docker CLI → dockerd → containerd → shim → runc」这条链条里最后一环的替代品。如果你对这条链条没概念，先回去看一眼上篇 1.5 节，下面的表会好读很多。

我那天的思路是："Docker 不行，那我换 apptainer。" 然后撞了第二堵墙。

错在哪里？错在我以为"换个工具"等于"换个原理"。

#### 7.1 一张表看清楚

|运行时|需要 daemon|需要 root|需要 userns|需要 /dev/fuse|需要 setuid|
| ----------------------| ------------| --------------------| -----------| ------------------------------| -------------------|
|Docker（默认）|✅|✅（daemon 是 root）|❌|❌|❌|
|Docker rootless|✅（用户级）|❌|✅**必须**|⏺️（用 fuse-overlayfs 时要）|❌|
|Podman rootful|❌|✅|❌|❌|❌|
|Podman rootless|❌|❌|✅**必须**|⏺️|❌|
|Apptainer（setuid）|❌|❌|❌|❌|✅（安装时要 root）|
|Apptainer（非 setuid）|❌|❌|✅|✅**必须**|❌|
|udocker（P 模式）|❌|❌|❌|❌|❌|
|enroot|❌|❌|✅|❌|❌|

看这张表就明白我那天的遭遇了：

我用的 apptainer 是 **非 setuid 安装**（pip / conda 装的都是），它挂载 squashfs 只能走 FUSE（`squashfuse`），而机器没有 `/dev/fuse`。

而 setuid 版本的 apptainer 不需要 FUSE——它靠一个 setuid root 的小程序直接调内核的 loop mount。**但这个 setuid 位必须由 root 安装时打上。**

所以 "apptainer 不需要 root" 这句流传很广的话，准确说法是：

> **apptainer 让普通用户不需要 root 就能跑容器，但前提是管理员先用 root 把它装对了。**

#### 7.2 rootless 到底 rootless 在哪

rootless 容器的魔法就一个：**user namespace 里的假 root**。

```bash
unshare -Ur id
# uid=0(root) gid=0(root)  ← 在这个 namespace 里你是 root
# 但宿主看你依然是 uid=1000
```

有了这个假 root，你就在**这个 namespace 内部**拥有全套 capabilities，于是可以建 mount namespace、可以 chroot。

但注意两个坑：

**坑一：假 root 不能挂任意文件系统。**  内核只允许在 userns 里挂少数几种文件系统（tmpfs、proc、sysfs、bind mount、以及新内核下的 overlay）。ext4、squashfs 这种需要读块设备的，**不行**。这就是为什么 rootless 方案总是和 FUSE 绑定出现。

**坑二：userns 本身可能被关。**  前面说过，很多安全基线会关掉它。一行验证：

```bash
unshare -Ur echo ok    # 输出 ok 就有，报 Operation not permitted 就没有
```

#### 7.3 一句话总纲

把本篇所有内容压成一句：

> **换运行时绕得开 daemon 和 root 权限，绕不开内核的挂载能力。**

- Docker 要 daemon + root → podman/apptainer 绕开了
- 但所有"真容器"都要 mount → 要么有 `CAP_SYS_ADMIN`，要么有 userns 假 root + FUSE，要么有 setuid 帮手
- 三样都没有？那就只剩**不靠挂载的方案**：udocker 的 P 模式（ptrace 拦 syscall 改路径）、proot、或者干脆不用容器

我那天在三个环境上撞的三堵墙，其实是同一堵墙的三个角度：

|现场|表面报错|真实原因|
| ---------------| --------| ---------------------------------------|
|魔搭 DSW|`Cannot connect to the Docker daemon`|我在 Pod 里，平台不可能在笼子内再给钥匙|
|课题组 H100|`mount overlay: permission denied`|没有 `CAP_SYS_ADMIN`（或 home 在 NFS 上存不了 xattr）|
|apptainer + sif|`fuse: device not found`|非 setuid 安装 + 无 `/dev/fuse`，squashfs 无法挂载|

三次都是同一句话：**内核不把挂载能力交给你。**

---

下一篇：假设你终于把容器跑起来了，接下来就是 AI 场景特有的那一堆坑：GPU 怎么透传、多卡通信为什么卡死、NCCL 报错怎么读。

---

## 下篇 ·《AI 训练与推理场景下的容器实践》

> 系列共三篇。前两篇讲的是通用的容器原理和受限环境求生，网上多少有些近似的替代品。
>
> 这一篇没有。因为它讲的是一件很少被系统写过的事：**容器对分布式通信的影响**。

> **适用范围与版本说明**（先看这一段，能省你很多时间）
>
> - 默认背景是 Linux 5.15+、Docker 24+、**cgroup v2**。文中涉及 cgroup v1 的部分只在较老的机器上才用得到。
> - 所有镜像 tag、驱动版本号都只是**写作当时的示例**，请换成你自己环境里的实际版本，不要直接照抄。
> - 命令里凡是带 `sudo` 的，都意味着“需要管理员”；你在只有普通用户权限的机器上直接跑是一定失败的。
> - 内核行为、安全策略、平台限制都在变。文中的**判定命令比结论更保值**——当结论和你机器上的输出矛盾时，以输出为准。

---

### 1. 容器怎么「看见」GPU

#### 1.1 一个先有鸡还是先有蛋的问题

上篇反复强调：容器和宿主共享内核。那么问题来了——

NVIDIA 的驱动是**内核模块**（`nvidia.ko`），它装在宿主上。容器里显然不可能再装一遍内核模块（它没那个权限，也没那个必要）。可是容器里的 CUDA 程序又必须调用驱动才能用卡。

**容器里怎么才能"看见"那张卡？**

答案分两半：

- **内核态部分**（`nvidia.ko`）：本来就是共享的，容器和宿主用同一个内核，也就用同一个驱动模块。这部分不用管。
- **用户态部分**：容器需要两样东西——① 设备节点 `/dev/nvidia0`、`/dev/nvidiactl`、`/dev/nvidia-uvm` 等；② 和宿主驱动**版本严格匹配**的用户态驱动库 `libcuda.so.<版本号>`、`libnvidia-ml.so.<版本号>`。

这两样东西，镜像里是**没有**的（也不能有——镜像不知道你宿主装的是 535 还是 550）。

#### 1.2 NVIDIA Container Toolkit 干了什么

它的做法非常巧妙：**在容器启动的那一瞬间，把宿主的驱动库和设备节点"塞"进去。**

具体机制是 OCI 规范里的 **prestart hook**。你 `docker run --gpus all` 的时候：

```
docker → containerd → runc
                       │
                       ├─ 创建 namespace、准备 rootfs
                       ├─ 【prestart hook】调用 nvidia-container-runtime-hook
                       │     ├─ 查询宿主驱动版本
                       │     ├─ 把 /dev/nvidia* 设备节点挂进容器
                       │     ├─ 把 libcuda.so.550.xx 等库 bind mount 进容器
                       │     ├─ 把 nvidia-smi 等工具挂进去
                       │     └─ 配置 cgroup device 白名单（允许访问这些设备）
                       └─ 启动你的进程
```

所以 `nvidia-smi` 能在容器里跑，不是因为镜像里装了它，而是因为**宿主那个被挂进来了**。你在容器里 `ls -l $(which nvidia-smi)` 会发现它是从外面 bind mount 进来的。

**一个直接推论**：`--gpus all` 不是"打开一个开关"，而是"执行一段挂载脚本"。所以它失败的方式，和挂载失败的方式一模一样。

#### 1.3 apptainer 的 `--nv` 和 `--nvccli`：同一个思路，两种实现

我在课题组机器上踩过这个：`apptainer exec --nv ...` 进去之后 `nvidia-smi` 报 "couldn't communicate with the NVIDIA driver"，换成 `--nvccli` 就好了。当时完全不懂为什么，现在清楚了：

- **​`--nv`​**​ **（传统模式）** ：apptainer 自己实现的一套简化逻辑。它读一个叫 `nvliblist.conf` 的配置文件，里面列着一串库名（`libcuda.so`、`libnvidia-ml.so`……），然后在宿主上 `ldconfig -p` 找到这些库，挨个 bind mount 进容器。

  - **优点**：不依赖外部组件，简单。
  - **缺点**：那个列表是**写死的**。新驱动加了新库、或者你需要的某个库不在列表里，它就漏掉了。表现出来就是"进去了但看不到卡"或者"某些功能报 symbol not found"。
- **​`--nvccli`​**​ ** 模式**：直接调用 NVIDIA 官方的 `nvidia-container-cli`（也就是 Container Toolkit 的核心），走和 Docker 完全一样的那套逻辑。

  - **优点**：官方维护，该挂什么它最清楚，不会漏。
  - **缺点**：宿主上必须装了 `nvidia-container-cli`；而且某些模式下它需要额外权限。

**结论**：宿主装了 Container Toolkit 就优先用 `--nvccli`；`--nv` 当作兜底。这不是玄学，是"一个用硬编码列表，一个用官方逻辑"的区别。

#### 1.4 GPU 透传失败排查树

```
nvidia-smi 在容器里失败
│
├─ 报 "command not found"
│   └─ hook 根本没跑。检查：docker info | grep -i runtime 有没有 nvidia
│      检查 /etc/docker/daemon.json 是否配了 nvidia runtime
│      检查有没有加 --gpus 参数（忘了加是最常见的原因）
│
├─ 报 "couldn't communicate with the NVIDIA driver"
│   └─ 设备节点没进来。检查容器内 ls /dev/nvidia*
│      检查宿主 nvidia-smi 是否正常（宿主自己坏了的情况比你想的多）
│      apptainer 用户：换 --nvccli 试试
│
├─ 报 "Driver/library version mismatch"
│   └─ 经典问题：宿主驱动升级了但内核模块还是旧的（没重启），
│      或者镜像里自带了一个和宿主版本不匹配的 libcuda.so 把挂进来的覆盖了。
│      解法：宿主 reboot；镜像里别装驱动，只装 CUDA runtime。
│
├─ 报 "nvidia-container-cli: initialization error"
│   └─ toolkit 装了但跑不起来。多半是 cgroup v2 兼容问题，
│      或者你在一个没有 device cgroup 写权限的环境里（又是受限环境）。
│
└─ 能看到卡，但少了几张
    └─ 检查 CUDA_VISIBLE_DEVICES、检查 --gpus '"device=0,1"' 的写法、
       检查平台是不是给你做了 MIG 切分或时间片共享。
```

#### 【所以然】

> 容器用 GPU 不是"自动的"，是**一个 hook 在启动瞬间把宿主的驱动挂进来**。
>
> 理解这一点，你就知道为什么镜像里不该装驱动、为什么驱动版本要和宿主对齐、为什么 GPU 透传的失败方式全都长得像挂载失败。

---

### 2. 【本系列独家】容器里的分布式通信

单卡跑通了，多卡多机就一定跑得通吗？不一定。而且失败的方式往往特别难查——不报错，就是 hang 住；或者能跑，但慢得离谱。

原因是：**容器几乎不影响计算，但处处影响通信。**

计算是进程内的事，容器管不着。通信要走共享内存、走网卡、要做设备发现、要拿到对端地址——**每一样都被 namespace 隔了一刀**。

下面这几个参数，是我现在跑任何多卡任务都会先写上的。重点讲"不写会怎么死"。

#### 2.1 `--shm-size` 与 `--ipc=host`：NCCL 的命根子

**Docker 默认给容器的 **​ **​`/dev/shm`​**​ ** 只有 64MB。**

这个数字在 2013 年可能够用，在今天是个笑话。谁在用它：

- PyTorch DataLoader 的多 worker：worker 之间传 tensor 走的就是共享内存
- **NCCL 的单机多卡通信**：同一台机器上的 GPU 之间做 all-reduce，NCCL 会优先走 P2P/NVLink，但控制面和部分 fallback 路径要用共享内存
- 各种多进程推理框架的 KV cache 共享

**不写会怎么死**：

- DataLoader：`RuntimeError: DataLoader worker (pid xxx) is killed by signal: Bus error` —— Bus error 就是共享内存写爆了
- NCCL：直接 hang 住，或者 `NCCL WARN Error while creating shared memory segment`

**怎么写**：

```bash
docker run --shm-size=32g ...          # 明确给够
# 或者
docker run --ipc=host ...              # 直接用宿主的 IPC namespace
```

两者的区别值得说清楚：

- `--shm-size=32g`：还是**独立的** ipc namespace，只是把容器自己的 `/dev/shm` 调大。安全，推荐。
- `--ipc=host`：**取消 IPC 隔离**，容器和宿主共用一套共享内存。NVIDIA 官方镜像文档推荐这个，因为某些 NCCL/CUDA IPC 场景需要跨容器共享。但它削弱了隔离——同宿主上别的容器理论上能看到你的共享内存段。

**我的建议**：单容器多卡，用 `--shm-size`；需要多个容器之间做 CUDA IPC（比如推理服务拆成多个容器），才上 `--ipc=host`。

#### 2.2 `--ulimit memlock=-1`：RDMA 的入场券

RDMA（InfiniBand 或 RoCE）的核心思路是**网卡直接读写内存，绕开 CPU 和内核**。要做到这一点，那块内存必须被**锁在物理内存里**（pinned），不能被 swap 出去——否则网卡 DMA 到一半发现页没了，整个机器就炸了。

锁内存这件事受 `RLIMIT_MEMLOCK` 限制，而这个限制在容器里默认非常小（通常 64KB）。

**不写会怎么死**：

```
NCCL WARN Call to ibv_reg_mr failed with error Cannot allocate memory
# 或者
ibv_reg_mr failed: Cannot allocate memory
```

注意那个 "Cannot allocate memory" 极具误导性——你会以为是内存不够，去查 free 发现内存明明还剩几百 G。其实是**能锁的内存不够**。

**怎么写**：

```bash
docker run --ulimit memlock=-1 --ulimit stack=67108864 ...
```

`-1` 表示 unlimited。`stack` 那条是 NVIDIA 官方镜像的推荐值，某些 CUDA 内核需要大栈。

#### 2.3 `--device=/dev/infiniband`：让容器看得见 IB 卡

和 GPU 一样，IB 卡在容器里也需要设备节点。`--gpus` 那套 hook 只管 GPU，**不管 IB**。

```bash
docker run --device=/dev/infiniband ...
# 或者更精确地
docker run --device=/dev/infiniband/uverbs0 --device=/dev/infiniband/rdma_cm ...
```

还有一个特别容易翻车的点：**容器里的用户态 RDMA 驱动（**​**​`libibverbs`​**​ ** + **​**​`libmlx5`​**​ ** 等 provider 库）版本，要和宿主内核驱动兼容**。这和 GPU 驱动是一模一样的道理，但没有一个 hook 帮你自动挂，得靠镜像里自己装对版本（NVIDIA 的 PyTorch NGC 镜像里已经装好了 MLNX OFED 用户态部分，这是它们那么大的原因之一）。

**症状**：`ibv_devinfo` 在容器里看不到设备，或者 NCCL 日志里显示 `NET/IB : No device found`，然后悄悄退化成 socket 传输——**能跑，但慢十倍**。

#### 2.4 为什么多机训练几乎必须 `--network=host`

这是最反直觉的一条。默认的 bridge 网络在多机场景下有两个致命问题：

**问题一：NAT 会毁掉地址发现。**

多机 NCCL 启动时要互相交换连接信息，交换的是"我在哪个 IP、哪个端口"。容器在 bridge 网络里的 IP 是 `172.17.x.x` 这种**只在本机有效的私有地址**。节点 A 的容器告诉节点 B："来连我，我在 172.17.0.3"——节点 B 上恰好也有个 172.17.0.3（它自己的容器），于是要么连错，要么连不上，最后表现为**启动时 hang 死，没有任何报错**。

**问题二：RDMA 根本不走内核网络栈。**

这条更根本。bridge 模式的隔离是靠 net namespace + veth + iptables NAT 实现的，而这些**全都在内核网络栈里**。RDMA 的整个卖点就是绕开内核网络栈直接 DMA——它根本不经过 veth，也不经过 iptables。

所以在 bridge 模式下用 RDMA，会出现一种精神分裂的状态：控制面（TCP 握手）走 NAT 后的假地址，数据面（RDMA）走真实的物理网卡地址，两边对不上，连接建不起来。

**结论**：

```bash
docker run --network=host ...     # 多机分布式，基本是必选项
```

代价是端口隔离没了，同一台机器上跑多个容器要自己管好端口不冲突。这是分布式训练圈子里公开的秘密：**多机场景下，容器的网络隔离基本上是被放弃的。**

#### 2.5 NCCL 的拓扑发现，在容器里为什么会算错

这是最隐蔽、也最贵的一个坑：**它不报错，只是让你慢。**

NCCL 启动时会做一件很重要的事：探测这台机器的硬件拓扑，然后决定用什么算法、走什么路径。它要知道：

- 哪两张卡之间有 NVLink（带宽 300+ GB/s）
- 哪两张卡只能走 PCIe（带宽几十 GB/s，还可能跨 NUMA）
- 网卡挂在哪个 PCIe switch 下，离哪张卡近

这些信息 NCCL 是从 `/sys/class/pci_bus/`、`/sys/devices/`、`/sys/class/infiniband/` 这些 sysfs 路径里读的。

**问题来了**：容器里的 `/sys` 常常是**不完整的**。设备节点被 hook 挂进来了，但 sysfs 里描述"这张卡插在哪个 PCIe 槽、和别的卡什么关系"的那些拓扑信息，往往没有完整挂进来。

于是 NCCL 探测失败 → 保守地假设一个最差的拓扑 → **明明有 NVLink 却走 PCIe，明明有 IB 却走 TCP socket**。

你的任务照样能跑完，只是慢了 5 倍，而你完全不知道。

**怎么发现**：

```bash
export NCCL_DEBUG=INFO
# 然后在日志里找这几行：
# NCCL INFO NET/IB : Using [0]mlx5_0:1/RoCE     ← 好，用上 IB 了
# NCCL INFO NET/Socket : Using [0]eth0          ← 坏，退化成 socket 了
# NCCL INFO Channel 00 : 0[..] -> 1[..] via P2P/IPC       ← 好，走 NVLink/P2P
# NCCL INFO Channel 00 : 0[..] -> 1[..] via SHM/direct    ← 一般
# NCCL INFO Channel 00 : 0[..] -> 1[..] via NET/Socket    ← 灾难
```

**怎么修**：

```bash
nvidia-smi topo -m                 # 先在宿主和容器里各跑一次，对比输出是否一致
                                   # 如果容器里全是 PHB/SYS 而宿主是 NV8，就是拓扑没进来

export NCCL_TOPO_FILE=/topo.xml    # 手动喂一份拓扑文件（可以用宿主导出的）
export NCCL_SOCKET_IFNAME=eth0     # 明确指定用哪张网卡做控制面，别让它瞎猜
export NCCL_IB_HCA=mlx5_0,mlx5_1   # 明确指定用哪几张 IB 卡
export NCCL_IB_DISABLE=0           # 确认没被谁设成 1
export NCCL_P2P_DISABLE=0          # 同上
```

**一个实操建议**：把 `nvidia-smi topo -m` 在宿主和容器里各跑一遍做对比，写进你的启动检查清单。这一步只要十秒，能救你几十个小时。

#### 2.6 MIG、时间片共享、以及 `CUDA_VISIBLE_DEVICES` 的语义陷阱

在共享平台上还有一层：**你看到的"一张卡"可能不是一张完整的卡。**

- **MIG（Multi-Instance GPU）** ：A100/H100 可以在硬件层面切成最多 7 个实例，每个有独立的 SM、L2、显存通道。容器里看到的是 `MIG 1g.10gb` 这样的设备。**关键限制：MIG 实例之间不能做 P2P，NCCL 跨 MIG 通信会退化。**  所以在 MIG 环境里做多卡训练基本没有意义。
- **时间片共享（time-slicing）** ：多个容器共用一张物理卡，靠调度器轮转。显存不隔离，一个 OOM 全体遭殃，而且性能抖动极大。
- **​`CUDA_VISIBLE_DEVICES`​**​ ** 在容器里的语义变了**：hook 挂进来的设备已经被重新编号了。你在宿主上看到的 GPU 3，进容器可能变成 GPU 0。所以在容器里再设 `CUDA_VISIBLE_DEVICES=3` 很可能直接报"no CUDA device"。
  - **正确做法**：在 `docker run` 层面用 `--gpus '"device=3"'` 选卡，容器里就用默认的 0。**不要在两个层面同时选卡**，这是新手最容易搞晕自己的地方。

#### 【所以然】

> 容器不影响你的矩阵乘法，但它**在通信路径上处处设卡**：共享内存被隔离、锁页内存被限额、设备节点要显式挂载、网络地址被 NAT、硬件拓扑被遮蔽。
>
> 这就是为什么分布式任务的 `docker run` 命令，参数比单卡任务长一倍——那些参数不是玄学配方，**每一个都在拆掉一堵挡在通信路上的墙**。

---

### 3. 容器安全与共享机礼仪

前面两篇大部分在讲"平台为什么限制我"。这一章反过来：当你自己有权限的时候，该怎么用。

两者其实是同一套逻辑的两面。

#### 3.1 最小权限：别无脑 `--privileged`

`--privileged` 是个核弹级的开关，它同时做了：给全部 capabilities、关掉 seccomp、关掉 AppArmor、把 `/dev` 全部挂进去、允许写 `/sys`。

也就是说，**上篇讲的四道墙一次性全拆了**。

正确的做法是先全部 drop 再按需加回来：

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE ...
```

常见需求对应的最小 capability：

|你想干什么|只需要|
| --------------------| -----------------------|
|绑 80/443 端口|`NET_BIND_SERVICE`|
|在容器里 ping|`NET_RAW`|
|改挂载目录的文件属主|`CHOWN`、`FOWNER`|
|用 gdb / py-spy 调试|`SYS_PTRACE`（不需要 privileged！）|
|调实时优先级|`SYS_NICE`|

很多人上来就 `--privileged`，其实只是因为想用 `py-spy` 看个堆栈——那只需要 `--cap-add=SYS_PTRACE`。

#### 3.2 非 root 运行

```dockerfile
RUN useradd -u 1000 -m appuser
USER appuser
```

好处不只是安全：上篇 6.3 节那个"容器写的文件我删不掉"的问题也一并解决了。

快速版（不改镜像）：

```bash
docker run -u $(id -u):$(id -g) ...
```

注意这样容器里可能找不到对应的用户名，某些程序会抱怨。可以加 `-v /etc/passwd:/etc/passwd:ro`。

#### 3.3 只读 rootfs

```bash
docker run --read-only \
  --tmpfs /tmp \
  -v /data/output:/output \
  ...
```

根文件系统只读，只有你明确指定的地方能写。除了安全，它还能逼你把输出路径想清楚，避免一堆临时文件悄悄写到可写层里、容器一删全没。

#### 3.4 永远设资源上限

```bash
docker run --memory=64g --memory-swap=64g --cpus=16 ...
```

为什么重要：不设限额的容器 OOM 时，内核的全局 OOM Killer 会按分数杀进程，**很可能杀的不是你，而是旁边无辜同事跑了三天的任务**。

设了限额，死的就只是你自己。这是共享机上最基本的善意。

#### 3.5 镜像卫生

- 固定版本，最好钉 digest（上篇 8.7）
- 定期清理：

```bash
docker system df -v          # 先看谁在吃盘
docker system prune          # 清停止的容器、悬空镜像、构建缓存
docker system prune -a       # 连未使用的镜像一起清（慎用）
docker builder prune         # 只清 BuildKit 缓存
```

悬空镜像（`<none>:<none>`）是磁盘被吃满的头号元凶。构建一次 20G 的镜像，改一行重构建一次，五次之后你的盘就没了。

#### 3.6 日志轮转

这个坑很隐蔽：Docker 默认的 `json-file` 日志驱动**没有上限**。一个疯狂打 log 的训练任务跑一周，可以轻松写出几百 G 的 `*-json.log`。

```json
// /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "100m", "max-file": "5" }
}
```

#### 3.7 共享机礼仪（没人写在文档里，但很重要）

- **跑完即停**。占着卡去吃饭是共享集群上最招人恨的行为。用 `nvidia-smi` 看一眼自己的显存占用。
- **别占满**。神奇的是很多人习惯性 `--gpus all`，即使只用一张卡。
- **不污染系统目录**。共享机上不要往 `/usr/local` 里装东西，用 `$HOME/.local` 或 conda 环境。
- **磁盘自律**。数据集用完就清，镜像缓存定期 prune。
- **改了全局配置要告知**。你改了 `/etc/docker/daemon.json` 或者 `sysctl`，其他人可能莫名其妙地撞墙。

#### 【所以然】

> "平台限制你"和"你自己写容器也要讲安全"是同一件事的两个方向。理解了为什么你被限制，你就知道自己该怎么限制自己。

---

### 4. 工程方法论：怎么不再靠运气排错

前面三章都是知识。这一章是我觉得更值钱的部分：**下次遇到没见过的报错，该怎么办。**

因为技术细节会过时，方法不会。

#### 4.1 动手之前先验环境前提

我那次失败的根本原因，是**顺序错了**：我先花两小时试各种命令，最后才发现这台机器从设计上就不可能跑 Docker。

正确的顺序是反过来的：**先花三十秒确认前提，再决定用哪条路。**

把中篇第 0 章那个诊断盒存成一个脚本，扔进 `~/bin`：

```bash
mkdir -p ~/bin && vim ~/bin/envcheck   # 内容见本篇附录 A
chmod +x ~/bin/envcheck
```

以后每上一台新机器，第一件事就是跑 `envcheck`。这个习惯的收益率高得离谱——三十秒换回来的，是「我到底该走哪条路」这个决定。

**一个具体判据**：如果 `cat /proc/1/cgroup` 里有 `kubepods`，就**不要再花时间尝试装 Docker**。直接去问平台的自定义镜像功能怎么用。

#### 4.2 最小复现 + 二分定位

多机训练卡住了，可能的原因有二十个：镜像、驱动、NCCL、网络、共享内存、防火墙、代码本身……一个个猜是没有尽头的。

**方法是分层验证，每层只验证一件事，从最简单的开始。**  一旦某层挂了，问题就锁定在那一层，不用再往上看。

```bash
# 第 1 层：容器本身能不能跑？
docker run --rm hello-world

# 第 2 层：容器能不能看见 GPU？
docker run --rm --gpus all nvidia/cuda:12.1.1-base-ubuntu22.04 nvidia-smi

# 第 3 层：PyTorch 能不能用 GPU？
docker run --rm --gpus all <你的镜像> \
  python -c "import torch;print(torch.cuda.device_count(), torch.cuda.get_device_name(0))"

# 第 4 层：单机多卡通信通不通？（关键的一层，很多人跳过）
docker run --rm --gpus all --shm-size=8g --ipc=host <你的镜像> python - <<'EOF'
import torch, torch.distributed as dist, os
dist.init_process_group("nccl", init_method="tcp://127.0.0.1:29500",
                        world_size=1, rank=0)
t = torch.ones(1024, device="cuda")
dist.all_reduce(t)
print("nccl ok:", t.sum().item())
EOF

# 第 5 层：才轮到你自己的训练脚本
```

第 4 层是分水岭。**如果第 4 层过了而你的训练脚本挂了，问题在代码或超参，不在容器**——这时候就该停止折腾环境，去看代码。反过来，如果第 4 层就挂了，看你自己的训练日志是浪费时间。

我见过太多人（也包括我）在第 5 层的日志里翻来翻去找线索，而问题其实在第 2 层。

#### 4.3 读报错，而不是刷报错

这是我这次最大的行为改变。

以前我的循环是：报错 → 复制 → 粘贴给大模型 → 拿到命令 → 试 → 新报错 → 再粘贴。这个循环的问题是：**它每一轮都在丢信息。**  容器里的报错常常只是症状，真正的原因写在别的地方。

四个「别的地方」，按被忽略的程度排序：

```bash
# ① daemon 自己的日志（Docker 启动失败时，真实原因只在这里）
journalctl -u docker -n 100 --no-pager

# ② 让 daemon 说话（前台带 debug 跑，能看到存储驱动探测的全过程）
sudo systemctl stop docker
sudo dockerd --debug

# ③ 宿主的内核日志 —— 最容易被漏掉的一个
dmesg -T | grep -Ei 'apparmor.*DENIED|avc: *denied|overlayfs|oom'

# ④ 让 NCCL 说话（不加这个，多机问题基本没法查）
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,NET
```

第 ③ 条值得单独强调：**容器里报 **​**​`permission denied`​**​ **，真正的原因往往是宿主 dmesg 里的一行 **​**​`apparmor="DENIED"`​**​ **。**  容器里的报错信息是被截断过的，因为拦你的那个组件不在容器里。

第 ④ 条同理：NCCL 默认几乎不说话，hang 住时你只看到光标在闪。加上 `NCCL_DEBUG=INFO` 之后，它会把拓扑探测、传输选择、每条 channel 的建立过程全打出来——本篇 2.5 节那几行关键日志就是这么读出来的。

#### 4.4 认出「坏环境」的信号，早点换路

有些信号一出现，就说明**这条路不该继续走了**。早认出来，比会修更值钱：

|信号|含义|该做什么|
| --------------------------------| --------------------| --------------------------------------------|
|`/proc/1/cgroup` 里有 `kubepods`|你在 Pod 里|立刻放弃装 Docker，改走平台自定义镜像|
|`unshare -Ur echo ok` 失败|userns 被禁|rootless 全家桶都别试了，走 udocker / proot|
|`/dev/fuse` 不存在且你不是 root|FUSE 路线断|apptainer 非 setuid、fuse-overlayfs 全部作废|
|`findmnt -T $HOME` 显示 nfs / lustre|overlay 存不了 xattr|工作目录立刻换到本地盘|
|同一个报错换了三种命令都没变|你在症状层打转|停下来，去读 dmesg 和 daemon 日志|
|你开始复制粘贴自己也看不懂的命令|已经进入盲试状态|停手，回到 4.2 的分层验证|

最后一条是行为信号，不是技术信号，但它最准。**当你开始运行自己解释不了的命令时，你已经不是在排错了，是在赌博。**

#### 4.5 沉没成本管理：给自己设一个硬上限

配环境这件事有个特别恶劣的性质：**它总让你觉得「就差最后一步了」。**  而这个感觉可以持续八个小时。

我现在的规矩是：**两小时硬上限。**  到点了不管进展如何，停下来写三行字：

```
1. 已确认的事实：（只写命令输出证实过的，不写推测）
2. 当前假设：（我认为问题是什么，用什么命令能证实/证伪）
3. Plan B：（如果这个假设也错了，下一条路是什么，预估多久）
```

写完这三行，通常会发生两件事之一：要么你发现第 1 行几乎是空的——说明你两小时全在盲试；要么你发现 Plan B 其实只要半小时，而你为了 Plan A 已经烧了两小时。

我那天如果在第一个小时末写下这三行，第 1 行会是「`/proc/1/cgroup` 显示 kubepods」，然后我立刻就会明白 Plan A 是死路。

#### 4.6 把大模型的回答当假设，不当答案

大模型在这类问题上非常有用——它知道的命令比我多得多。但它有一个结构性的局限：**它看不见你的机器。**

它只能基于「最常见的情况」给你一条命令。而环境问题恰恰是**长尾**的：同一条 `mount overlay: permission denied`，可能是 capabilities，也可能是 NFS 不支持 xattr，也可能是 AppArmor（中篇 4.2 节列了至少五种）。它默认按最常见那种回答，而你恰好不是那种，于是你们就一起在错误的方向上越走越远。

更麻烦的是**听起来很深刻但其实不对**的回答。举一个我自己栽过的例子：

> 「容器里的 root 其实是宿主上的普通用户，因为 user namespace 做了映射。」

这句话在网上流传极广，我一开始也照抄进了自己的笔记。但它只对 rootless 容器成立——**默认的 Docker 并不开启 userns-remap，容器里的 root 就是宿主上真实的 uid 0**（上篇 4.2 节详细拆过）。

后果很实际：如果你信了这句话，遇到权限问题就会去查 `/etc/subuid` 和 `newuidmap`，而真正该查的是 capabilities 和 seccomp。**方向反了，查一天也查不出来。**

所以我现在的用法是：

1. 让它给**判定命令**，而不是修复命令。「我怎么确认是不是 X」比「怎么修 X」安全得多。
2. 任何「应该可以」「一般来说」的断言，都要求配一条能在我机器上跑的验证命令。跑不出来的断言就当没说。
3. 它给的命令，先看懂再执行。看不懂就先问「这条命令改变了什么，失败会有什么后果」——尤其是带 `sudo`、`rm -rf`、`--privileged` 的。

本篇所有小节都尽量遵守一条自我要求：**每个论断后面都跟一条可以自己跑的命令。**  你不必相信我，你可以去验。

#### 4.7 给自己建一张机器指纹表

最后一个小习惯，收益远超成本。每台你用过的机器，跑完 `envcheck` 之后记一行：

|机器|环境类型|有 root|userns|/dev/fuse|home 文件系统|结论：怎么跑环境|
| -------------| ----------| ---------| ---------| ---------| -------------| ----------------------------------------------|
|魔搭 Notebook|K8s Pod|假 root|❌|❌|overlay|只能用平台自定义镜像|
|课题组 H100|HPC 共享机|sudo 可用|⚠️ 部分|❌|NFS|apptainer(setuid) 或裸装，工作目录必须放本地盘|
|自购 ECS|完整 VM|真 root|✅|✅|ext4|随便，直接 docker|

这张表的作用不是备忘，是**避免重复撞同一堵墙**。环境问题最气人的地方就是三个月后你会把结论忘干净，然后从头再试一遍那些注定失败的命令。

#### 【所以然】

> 排错能力不是记住更多命令，而是**建立「先验证前提、再分层定位、最后才动手改」的顺序**。
>
> 顺序对了，你用的命令再少也能收敛；顺序错了，命令再多也只是在症状层面打转。

---

### 5. 结语：三个报错，一份契约

回到开头那三个报错。

```
魔搭 Notebook    Cannot connect to the Docker daemon
课题组 H100      mount overlay: permission denied
apptainer + sif   fuse: device not found
```

当时在我看来这是三个不相干的毛病，所以我就三次重新开始、三次重新搜、三次重新试。

把三篇读完之后，它们其实只是同一句话的三个叙述角度：

|现场|表面报错|真实含义|
| ---------------| --------------| ----------------------------------------------|
|魔搭 Notebook|连不上 daemon|我自己就是个容器，平台不可能在笼子里再给钥匙|
|课题组 H100|overlay 挂不上|没有 `CAP_SYS_ADMIN`，或者目录在 NFS 上存不了 xattr|
|apptainer + sif|没有 `/dev/fuse`|非 setuid 安装，而用户态挂载的唯一通道也被堵了|

三句话合成一句：**这台机器不打算把挂载能力交给我。**

而挂载能力是容器的命门——上篇那五步流水线里，`mount` 出现了三次。所以不管报错长什么样，最后都只有三条出路：

**一、改契约。**  找管理员要一个**具体能力**（一个设备节点、一个 setuid 安装、一个 sysctl），而不是要「Docker 权限」。中篇 5.6 节那份邮件模板的全部设计思路就是这一句。

**二、换一条不需要那项能力的路。**  udocker 的 P 模式用 ptrace 改写路径，根本不挂载；proot 同理；平台自定义镜像则是让**平台替你挂**。

**三、换机器，或者干脆不用容器。**  如果你只是要在这一台机器上跑一次实验，micromamba 半小时裸装完事，容器带给你的价值接近于零。

我那天花两小时试的，是第四个不存在的选项：在不给我挂载权的机器上，让挂载成功。

所以这三篇的真正结论不是某个命令，而是一个提问方式的转变：

> 以前我问的是「这个报错怎么修」。
>
> 现在我问的是「**这台机器肯给我哪几项能力，而我要干的事需要哪几项**」。

后一个问题只需要三十秒就能回答（附录 A 那个脚本），而它能直接告诉你后面两小时该怎么过。

这大概就是对一个报错背后的原理花时间弄清楚的回报率：不是下次能快一点，而是下次知道哪些路根本不需要走。

---

## 附录

附录是设计成可以直接抄走用的。建议只收藏这一部分。

### 附录 A：环境诊断脚本（envcheck.sh）

存成 `~/bin/envcheck` 并 `chmod +x`。上任何一台新机器先跑它。它全程只读，不会改你机器上的任何东西。

```bash
#!/usr/bin/env bash
# envcheck - 容器可行性三十秒体检（只读，无副作用）

hr(){ printf '\n\033[1;36m===== %s =====\033[0m\n' "$1"; }

hr "1. 我在哪里（环境类型）"
cat /proc/1/cgroup 2>/dev/null | head -5
systemd-detect-virt -c 2>/dev/null || echo "(不在容器里，或命令不存在)"
[ -d /var/run/secrets/kubernetes.io/serviceaccount ] && echo ">>> 命中：K8s Pod"
env | grep -q KUBERNETES_SERVICE_HOST && echo ">>> 命中：K8s 环境变量"

hr "2. 我有哪些权力（capabilities）"
CAP=$(grep CapEff /proc/self/status | awk '{print $2}')
echo "CapEff = $CAP"
command -v capsh >/dev/null && capsh --decode="$CAP" | tr ',' '\n' | grep -i sys_admin \
  && echo ">>> 有 CAP_SYS_ADMIN" || echo ">>> 没有 CAP_SYS_ADMIN（挂不了 overlay）"

hr "3. user namespace 能不能建（rootless 的前提）"
unshare -Ur echo "ok - userns 可用" 2>&1
echo -n "max_user_namespaces = "; cat /proc/sys/user/max_user_namespaces 2>/dev/null || echo "?"
sysctl -n kernel.unprivileged_userns_clone 2>/dev/null | sed 's/^/unprivileged_userns_clone = /'

hr "4. /dev/fuse 在不在"
ls -l /dev/fuse 2>&1

hr "5. 文件系统现实（overlay 能不能落地）"
findmnt -T "$HOME" -o TARGET,SOURCE,FSTYPE,OPTIONS 2>/dev/null
findmnt -T /tmp   -o TARGET,FSTYPE,OPTIONS 2>/dev/null
grep -q overlay /proc/filesystems && echo "内核支持 overlayfs" || echo ">>> 内核没有 overlayfs"

hr "6. cgroup 版本"
stat -fc %T /sys/fs/cgroup/ 2>/dev/null   # cgroup2fs=v2, tmpfs=v1

hr "7. 磁盘与配额"
df -h "$HOME" /tmp /dev/shm 2>/dev/null
quota -s 2>/dev/null | tail -3 || echo "(无 quota 信息)"

hr "8. 容器工具链现状"
for c in docker podman apptainer singularity udocker enroot proot skopeo; do
  printf '%-12s %s\n' "$c" "$(command -v $c || echo '-')"
done
docker info 2>&1 | grep -Ei 'storage driver|cgroup|docker root dir|^ *ERROR|cannot connect' | head -6

hr "9. subuid/subgid（rootless 用）"
grep "^$USER:" /etc/subuid /etc/subgid 2>/dev/null || echo ">>> 没分配 subuid，rootless 跑不起来"

hr "10. GPU"
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv 2>/dev/null || echo "(无 nvidia-smi)"
ls /dev/nvidia* 2>/dev/null | head
nvidia-smi topo -m 2>/dev/null | head -12

echo
echo "===== 怎么读 ====="
echo "第1项有 kubepods      → 你在 Pod 里，别装 Docker，走平台自定义镜像"
echo "第2项无 SYS_ADMIN     → 挂不了 overlay，真容器路线全断"
echo "第3项失败          → rootless（podman/非setuid apptainer）也走不通"
echo "第4项不存在        → FUSE 路线断，只剩 udocker P 模式 / proot"
echo "第5项 home 是 nfs    → 工作目录换本地盘，否则 overlay 必挂"
```

### 附录 B：报错快速索引

完整的四列鉴别诊断表（报错 → 多种病因 → 判定命令 → 解法）在**中篇第 4 章**。这里只做跳转：

|你看到的报错|去哪看|最常被漏掉的那种病因|
| -------------------| -------------------| ---------------------------------------|
|`Cannot connect to the Docker daemon`|中篇 4.1|你本身在 Pod 里，根本没 daemon|
|`mount overlay: permission denied`|中篇 4.2|目标目录在 NFS/Lustre 上，存不了 xattr|
|`fuse: device not found`|中篇 4.3|apptainer 是非 setuid 安装，必须靠 FUSE|
|`newuidmap: Permission denied`|中篇 4.4|`/etc/subuid` 里没你|
|`no space left on device`（df 看着还有）|中篇 4.5|inode 耗尽，或 `/tmp` 是小 tmpfs，或 quota|
|退出码 137 / `OOMKilled`|中篇 4.6|cgroup 限额（不是全机内存），或 `/dev/shm` 爆了|
|`port is already allocated` / 访问不了|中篇 4.7|服务只监听 127.0.0.1|
|`nvidia-container-cli: initialization error`|中篇 4.8 + 本篇 1.4|宿主驱动自己就坏了|
|`Bus error` in DataLoader|上篇 6.2 / 本篇 2.1|`/dev/shm` 默认只有 64MB|
|`ibv_reg_mr failed: Cannot allocate memory`|本篇 2.2|不是内存不够，是 `memlock` 限额|
|多机卡在 `initializing process group`|本篇 2.4|bridge 网络下报的是 172.17.x.x 私有地址|
|能跑但比宿主慢 5 倍|本篇 2.5|NCCL 拓扑探测失败，退化成 socket/PCIe|
|`Driver/library version mismatch`|本篇 1.4|宿主驱动升级了但没重启|

### 附录 C：五类环境对照表

|类型|典型例子|你是 root 吗|能跑 Docker 吗|推荐走法|
| -------------------| -----------------------| --------------------| --------------| ---------------------------|
|① 裸金属 / 完整 VM|自购服务器、ECS、EC2|真 root|✅|直接 docker|
|② 云容器实例|魔搭/DSW、AutoDL、Colab|假 root（在 Pod 里）|❌|平台自定义镜像 ≫ udocker|
|③ HPC 共享集群|课题组集群、超算|❌ 普通用户|❌|enroot+pyxis 或 apptainer|
|④ 受限 VM|内核裁剪过、禁 modprobe|真 root|⚠️ 看缺哪项|逐项诊断，通常可修|
|⑤ 容器内（DinD）|CI runner、开发容器|看配置|⚠️ 很难|sysbox / 挂 socket / 换平台|

### 附录 D：机制速查

**八种 namespace**

|名称|隔离什么|
| ----| -----------------------------------------------|
|`pid`|进程 ID 与进程树|
|`mnt`|挂载点|
|`net`|网卡、IP、端口、路由、iptables|
|`uts`|主机名、域名|
|`ipc`|System V IPC、消息队列、**共享内存**|
|`user`|UID/GID 映射（唯一无特权可建，rootless 的基础）|
|`cgroup`|cgroup 根目录视图|
|`time`|启动时间、单调时钟（Linux 5.6+）|

**常用 capabilities**

|capability|用来干什么|
| ----------| ------------------------------------------------------------|
|`CAP_SYS_ADMIN`|mount / pivot_root / setns / 改 cgroup……（"the new root"）|
|`CAP_NET_ADMIN`|配网卡、改路由、改 iptables|
|`CAP_NET_RAW`|发原始包（ping）|
|`CAP_NET_BIND_SERVICE`|绑 1024 以下端口|
|`CAP_SYS_PTRACE`|gdb / py-spy 调试|
|`CAP_SYS_NICE`|调实时优先级|
|`CAP_CHOWN` / `CAP_FOWNER`|改文件属主 / 绕过属主检查|

**四种网络模式**

|模式|何时用|
| --------| -----------------------------|
|`bridge`（默认）|单机服务、开发|
|`host`|**多机分布式训练、RDMA**|
|`none`|完全不需网络|
|`container:xxx`|sidecar；K8s Pod 内部就是这个|

**三种挂载**

|类型|写法|特点|
| ----------| ----| ------------------------------------|
|bind mount|`-v /host:/ctr`|AI 场景 95% 用这个；直接遮盖目标路径|
|volume|`-v myvol:/data`|首次挂载会把镜像里的内容拷进去|
|tmpfs|`--tmpfs /tmp`|在内存里，容器死就没|

### 附录 E：无 root 求生工具箱

|工具|适用场景|需要的权限|
| ----| ----------------------------| -------------------|
|**平台自定义镜像**|云 Notebook / K8s 平台|无（平台替你做）|
|**udocker（P 模式）**|什么特权都没时的兵家必争之地|无|
|**proot + 手工摄平镜像**|udocker 也装不了|无|
|**enroot + pyxis**|Slurm 集群|管理员预先安装|
|**apptainer（setuid）**|HPC 集群标配|管理员安装时需 root|
|**podman rootless**|有 userns 的机器|userns + subuid|
|**micromamba 裸装**|依赖不脏、只跑一次|无|
|**conda-pack**|环境搭家（穷人版镜像）|无|

优先级就按这个顺序从上往下试。

### 附录 F：给管理员的申请模板

完整说明在中篇 5.6 节。核心原则两句：**不要要「权限」，要一个具体能力；并且告诉对方你有 Plan B。**

```
主题：关于 xx 服务器容器环境的一个小请求

老师好，

我在 xx 机器上跑 xx 项目，需要一个包含 CUDA 12.x + 自定义编译依赖的环境。
直接裸装会污染公共环境，所以想用容器。

我已经确认过：
- 机器上没有 docker，我理解多租户环境不适合装（docker 组等于 root），所以不申请这个
- 我想用 apptainer（无 daemon、容器内外 UID 一致，是 HPC 集群的标准方案）
- 它在本机报 "fuse: device not found"，原因是 /dev/fuse 不存在

所以想麻烦您一件事（二选一即可）：
1. sudo mknod -m 666 /dev/fuse c 10 229   # 只创建设备节点，不涉及提权
2. 或者安装 apptainer-suid 包

如果都不方便，我会改用 udocker（纯用户态）或直接在 conda 里裸装，
不需要您做任何操作，先告知一声。

谢谢！
```

四个请求按答应概率从高到低：**A** 创建 `/dev/fuse` → **B** 装 setuid 版 apptainer → **D** 装 enroot+pyxis（Slurm 集群，对管理员有好处）→ **C** 放开非特权 userns（被拒概率最高，安全基线常明文要求关）。

### 附录 G：DinD 决策树

```
我已经在容器里了，想再跑 Docker
│
├─ 我能控制宿主（自己的机器 / CI 配置归我）？
│   ├─ 能 → 宿主装 sysbox，--runtime=sysbox-runc。最优雅，不需 privileged
│   └─ 不能 → 继续往下
│
├─ 我能拿到 --privileged 吗？
│   ├─ 能 + 有 /dev/fuse → dind --storage-driver=fuse-overlayfs（磁盘友好）
│   ├─ 能 + 没 /dev/fuse + 磁盘宽裕 → dind --storage-driver=vfs（慢、占盘翻倍）
│   └─ 不能 → 继续往下
│
├─ 我只是想 build 镜像，不是真要跑 daemon？
│   └─ 是 → 用 kaniko / buildah（无需 privileged），或直接交给
│          云厂商镜像构建服务 / GitHub Actions
│
└─ 都不行（AutoDL / 魔搭这类平台基本都到这里）
    └─ 停手。走中篇 5.1（平台自定义镜像）或 5.2（udocker）
```

☠️ **不推荐的一条路**：挂 `/var/run/docker.sock`（DooD）。它能跑，但等于把宿主 root 送给容器，而且路径语义很坑（`-v ./data:/data` 里的 `./data` 是**宿主上的路径**）。

### 附录 H：分布式训练容器参数清单

直接拿去改。每一行为什么需要，看本篇第 2 章。

```bash
docker run --rm -it \
  --gpus all \
  --network=host \                 # 多机必选：bridge 的私有 IP 会让 NCCL 建不上连
  --ipc=host \                     # 或 --shm-size=32g；不加会报 Bus error
  --ulimit memlock=-1 \            # RDMA 锁页内存；不加报 ibv_reg_mr failed
  --ulimit stack=67108864 \         # 某些 CUDA kernel 需要大栈
  --device=/dev/infiniband \        # IB 卡设备节点（--gpus 不管这个）
  -v /data:/data \
  -v $HOME/ckpt:/ckpt \
  -e NCCL_DEBUG=INFO \             # 出问题时的唯一线索来源
  -e NCCL_SOCKET_IFNAME=eth0 \     # 明确控制面网卡，别让它瞎猜
  -e NCCL_IB_HCA=mlx5_0,mlx5_1 \   # 明确 IB 卡
  -e OMP_NUM_THREADS=8 \           # 和你的 --cpus 对齐，否则线程打架
  <你的镜像> bash
```

**启动后的三秒体检**（强烈建议写进启动脚本）：

```bash
nvidia-smi topo -m          # 和宿主对比；全是 PHB/SYS 就是拓扑没进来
df -h /dev/shm              # 不应该是 64M
ulimit -l                   # 应该是 unlimited
ibv_devinfo 2>/dev/null | head    # IB 场景：看得见设备吗
```

### 附录 I：安全与共享机 checklist

自己有权限时的自查项（详见本篇第 3 章）：

- [ ] 没有无脑 `--privileged`，而是 `--cap-drop=ALL` 再按需 `--cap-add`
- [ ] 只想用 py-spy/gdb 的话，用的是 `--cap-add=SYS_PTRACE`，不是 privileged
- [ ] 容器里不以 root 跑（`-u $(id -u):$(id -g)` 或镜像里 `USER`）
- [ ] **设了资源上限**（`--memory` / `--cpus`）——不设限时全局 OOM Killer 可能杀的是同事跑了三天的任务
- [ ] 镜像版本固定（最好钉 digest），不用 `latest`
- [ ] 配了日志轮转（`log-opts` 里的 `max-size` / `max-file`）
- [ ] 定期 `docker system df -v` + `prune`，悬空镜像是吃盘元凶
- [ ] 跑完就释放卡，不习惯性 `--gpus all`
- [ ] 不往 `/usr/local` 装东西，用 `$HOME/.local` 或 conda
- [ ] 改了 `daemon.json` / `sysctl` 这类全局配置，告知其他人

### 附录 J：参考与延伸阅读

下面都是一手资料。认真读一遍比看二十篇二手博客有用。

**内核机制（最权威）**

- `man 7 namespaces`、`man 7 capabilities`、`man 7 cgroups`——本系列上篇的事实基础基本都能在这三个 man page 里核对
- Linux 内核文档：[overlayfs](https://docs.kernel.org/filesystems/overlayfs.html)（upperdir 对 xattr 的要求写在这里）
- Linux 内核文档：[cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)

**运行时**

- [OCI Runtime Spec](https://github.com/opencontainers/runtime-spec) / [Image Spec](https://github.com/opencontainers/image-spec)
- [Rootless Containers](https://rootlesscontaine.rs/)——rootless 的权限前提讲得最清楚
- [Apptainer 官方文档](https://apptainer.org/docs/)（特别看 setuid / 非 setuid 的差异那一节）
- [udocker](https://github.com/indigo-dc/udocker) —— 四种执行模式的说明在 README
- [sysbox](https://github.com/nestybox/sysbox) —— 无特权 DinD
- [enroot](https://github.com/NVIDIA/enroot) + [pyxis](https://github.com/NVIDIA/pyxis)

**GPU 与分布式**

- [NVIDIA Container Toolkit 文档](https://docs.nvidia.com/datacenter/cloud-native/)
- [NCCL 环境变量完整列表](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html)——本篇 2.5 那些变量的权威来源
- [NCCL 故障排查指南](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html)

**安全**

- [Docker 默认 seccomp profile](https://github.com/moby/moby/blob/master/profiles/seccomp/default.json)——想知道到底拦了哪些 syscall，直接看这个文件
- CVE-2019-5736（runc 逃逸）、cgroup v1 `release_agent` 逃逸——中篇第 3 章那些限制的现实依据

---

### 写在最后

这三篇的起点很不体面：我花了两小时，在一台从设计上就不可能成功的机器上，反复试一些注定失败的命令。

真正让我不舒服的不是浪费了时间，而是那两小时里我一直在做一件事：把报错交给别人（或者别的什么），拿回一条命令，然后试。我从头到尾没有问过一个问题：**这台机器到底能不能做到我要它做的事？**

那个问题的答案，`cat /proc/1/cgroup` 一行就能给。

所以如果这三篇只能留下一句话，我希望是这句：

> **容器不是一个软件，是一份你和内核之间的契约。** 
> **跑不起来的时候，不要问「怎么修」，先问「契约里到底写了什么」。**

如果你也在某台机器上撞过这三堵墙，欢迎把你的 `envcheck` 输出和最后的解法讲一讲——环境问题的长尾特别长，多一个现场就多一份线索。

---
