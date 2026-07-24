---
title: "全网免费 GPU 资源收集（2026-07-15 整理）"
author: Fu Qilin
categories: [Memo]
tags: [gpu, free-compute, cloud-computing, ai-infra, students, startup]
date: 2026-07-15
excerpt: "把普通人/学生/研究者/初创团队能拿到的零成本 GPU 算力一次列清：开箱即用的免费 Notebook、开发者免费档、国内可访问平台、AMD 系免费 GPU、科研/创业大额额度，附避坑提示与选择决策指南。"
---

> 目标：把**普通人 / 学生 / 研究者 / 初创团队**能拿到的"零成本 GPU 算力"一次性列清。
> 每个平台名称均为**直达链接**，点开即用。
> 按"开箱即用 → 开发者免费档 → 国内可访问 → **AMD 系免费 GPU** → 科研/创业大额额度 → 国内科研基础设施"**六类**组织，末尾附**避坑提示**与**选择决策指南**。
> 说明：额度/价格随平台活动变动，以下为 2026-07-15 检索到的公开口径，使用前以官网为准。

---

## 一、开箱即用的免费 Notebook GPU（无需信用卡）

这类最适合新手：浏览器里直接跑 Notebook，注册即用，不绑卡。

| 平台 | 免费 GPU | 时长/配额 | 存储 | 信用卡 | 备注 |
|---|---|---|---|---|---|
| **[Google Colab](https://colab.research.google.com)** | NVIDIA T4 (16GB) / 偶尔 L4 | 会话≤12h，闲置~90min 断；周配额动态 ~15–30 GPU-h | 临时盘（挂 Drive 持久化） | ❌ 不需要 | K80 已退役；L4/A100 是 Pro 付费档 |
| **[Kaggle Notebooks](https://www.kaggle.com/code)** | P100 (16GB) 或 2×T4 (32GB)，含 TPU v5e-8 | 周配额 ~30 GPU-h；GPU 会话≤9–12h | 20GB 持久 | ❌ 不需要（绑手机号） | 竞赛生态 + 5万+ 数据集 |
| **[Hugging Face ZeroGPU](https://huggingface.co/spaces)** | RTX Pro 6000 Blackwell (48/96GB) | 日配额 ~5 min（登出 2min / PRO 40min），单次调用~60s | Space 仓库 | ❌ 不需要 | **只做推理/Demo**（Gradio @spaces），非训练 |
| **[Saturn Cloud](https://saturncloud.io)** | T4-class (≤16GB) | **Hosted Free：官方 10 GPU Jupyter 小时 + 3 Dask 小时 / 月**（第三方称 30h 或"无限"，以注册后控制台为准） | 持久 | ❌ 不需要 | 最接近 Colab/Kaggle 的日常 Notebook；已转型为 GPU 云"控制平面"/BMaaS |
| **[Lightning AI](https://lightning.ai/notebooks)** | T4 / L4 / L40S / A100 / H200 | **15 月额度 ≈ 75 免费 T4 GPU 小时/月**（官方页口径），支持 T4/L4/L40S/A100/H200 | 10GB Drive + 100GB Studio | 赠额度阶段不需要 | PyTorch 团队出品；已与 Voltage Park 合并（3.6万卡）；超出后 T4 ~$0.19/h、A100 ~$2.71、H100 ~$1.99 |
| **[Paperspace Gradient](https://www.digitalocean.com/products/gradient)**（现 DigitalOcean） | 共享 M4000 (8GB) | 会话≤6h 自动关，1 并发 | 5GB | ❌ 不需要 | Notebook UX 精致；付费 RTX4000 $0.51/h、A100 $2.23、H100 $3.18 |
| **[Intel Tiber AI Cloud](https://ai.cloud.intel.com/products)** | Intel Gaudi / Intel Max GPU | Standard 免费档（限时使用，按项目） | 会话级 | ❌ 不需要 | 英特尔硬件，适合尝鲜；原 Intel Developer Cloud 改名而来 |
| **[Amazon SageMaker Studio Lab](https://studiolab.sagemaker.aws)** | T4 (16GB) | 会话≤4h，每 24h 限 4h | 15GB | ❌ 不需要 | ⚠️ **即将关闭新用户注册：2026-07-30 起停止新注册**（现有用户可继续用）。想薅的务必在 7/30 前注册 |
| **[NVIDIA LaunchPad](https://www.supermicro.com/en/featured/startup-accelerator-program)**（企业级 GPU 评估） | H100 / B200 / GH200 等企业级 GPU | 免费远程访问企业级硬件 + NVIDIA AI Enterprise 软件栈；引导式实验（guided labs）/ Sandbox | 会话级 | ❌ 不需要 | ⚠️ 原 nvidia.com/launchpad 自助免费实验已转为**限时窗口**（如 Supermicro Startup Accelerator 单周窗口）；属"企业评估/原型验证"而非稳定免费 Notebook，需申请/排期 |

**这一类怎么选**：纯新手/小模型实验 → Colab 或 Kaggle；做模型 Demo/推理页 → HF ZeroGPU；持久云 IDE + PyTorch 生态 → Lightnight AI。

---

## 二、开发者免费档（Serverless / API，适合推理、批量、小微调）

适合会写代码、要"按需起 GPU、用完缩到 0"的人。

| 平台 | 免费内容 | 覆盖硬件 | 信用卡 | 适合 |
|---|---|---|---|---|
| **[Modal](https://modal.com/pricing)** | **Starter 每月 $30 计算额度**，无月费 | T4 → B200 全系 | ❌ 不需要（超 $30 才计费） | 突发推理、批量任务、小微调；Python SDK，按秒计费、缩到 0 |
| **[Replicate](https://replicate.com)** | 新账户赠免费额度，按秒计费 | 5万+ 开源模型 | 部分需要 | 一行 API 跑开源模型（图像/音频/视频强），被 Cloudflare 收购 |
| **[Together AI](https://www.together.ai)** | 免费档（有限速率）+ OpenAI 兼容 API | Llama/Mixtral/Qwen/DeepSeek 等 | 部分需要 | 低成本 LLM 推理 + 微调，token ~$0.06/百万 |
| **[RunPod](https://www.runpod.io)** | Community 免费额度 + 社区模板/Serverless 端点 | Secure Cloud A100 $1.89/h；Community H100 spot 更便宜 | 社区档不需要 | 便宜的社区 GPU 云；**无长期免费独享 GPU**，靠社区额度/spot |
| **[Vast.ai](https://vast.ai)** | 无真正免费档，但**极便宜** | 竞价市场 RTX 3090 $0.17/h 起 | 需要 | 实验间隙的廉价比价市场 |
| **[Thunder Compute](https://www.thundercompute.com)** | **新用户 $20 免费额度（即时、无需卡）** + 首充 100% 匹配最高 $50（学生邮箱自动 $20）；A100 $0.78/h、H100 $1.38/h、RTX A6000 $0.27/h | A100/H100/RTX 全系 | 免费用不到；匹配需绑卡 | 学生/indie 首选，便宜且免费额度即时到账；北美机房 |
| **[SaladCloud](https://www.salad.com)** | **新用户试用额度**；分布式闲置 GPU 用量计费低至 $0.02/h（托管容器） | 191+ 国家节点，SOC2 | 试用需注册 | 极便宜推理/渲染/批处理；个人也可装客户端共享闲置算力赚币 |

> Modal 的 $30/月实测约 = 50h T4 / ~12h A100 / ~5h B200。对"尖峰"工作非常划算。
> 💡 **欧盟便宜云（非稳定免费档，合格新账户可能获有限试用额度）**：[DataCrunch](https://datacrunch.io)（芬兰/冰岛，H100 $2.39/h、A100 $1.59/h，ISO27001/GDPR）、[Genesis Cloud](https://genesishpc.com)（欧盟主权云、100% 可再生，H100/H200 集群）。价格低但需先付费或申请试用，不作为"白嫖"入口。

---

## 三、国内可访问平台（中文生态、网络友好）

对国内用户最实用的一类——访问稳、中文文档全、多数实名即用。

| 平台 | 免费资源 | 限制 | 适合 |
|---|---|---|---|
| **[魔搭 ModelScope](https://modelscope.cn)**（阿里达摩院） | **每天 2000 次免费 API 调用 + 100 小时免费 GPU 算力**，CPU 长期免费；xGPU 永久免费（推理，等效 T4） | 需绑阿里云账号 | 开源模型下载/微调/推理/部署，国内最活跃社区 |
| **[飞桨 AI Studio](https://aistudio.baidu.com)**（百度） | **每日 12h V100 (16GB)**，CPU 免费；预装 PaddlePaddle + PyTorch/TensorFlow | 仅限 PaddlePaddle 框架为主、需实名 | 入门教学、课程、Paddle 模型开发、竞赛 |
| **[九天·毕昇](https://jiutian.10086.cn)**（中国移动） | 注册赠 **1000 算力豆（≈50h V100）**，邀友 +500；Jupyter/VSCode 双环境、可 root | 算力豆有效期短（~7天），需任务续期 | 自定义环境、需 root 的实验、千亿模型 Playground |
| **[阿里天池实验室](https://tianchi.aliyun.com)** | 每周 30h GPU（P100/T4，24GB），CPU 免费；5万+ 数据集 | 实名 + 绑手机；会话≤9h | 数据挖掘竞赛、多框架实验 |
| **[腾讯云 Cloud Studio](https://cloudstudio.net)** | 每月 10000 分钟 GPU（16GB 显存 + 32GB 内存 + 8 核），集成 ollama / DeepSeek-R1 | 需实名；超额度付费 | 轻量 AI 开发、模型部署测试、多框架验证 |
| **[华为 ModelArts](https://www.huaweicloud.com/product/modelarts.html)** | 每次 8h GPU（MindSpore/TensorFlow），常送代金券 | 需实名 | MindSpore 生态、企业级落地 |
| **[AutoDL](https://www.autodl.com)** | **非完全免费但极便宜**（几毛~几元/小时）；新用户赠 ¥10 额度 | 按量付费 | 不想折腾免费额度、要稳定长训的人；国内最大 GPU 云 |
| **[趋动云 VirtAI / OrionX](https://www.virtaicloud.com)** | 注册送 **50GB 存储 + 新人算力（约 50h 24G 显存）**；最低 ¥0.49/h；**永久免费 OrionX 社区版** | 按量、分钟计费 | GPU 池化技术，适合实验/轻量训推、显存超分 |
| **[矩池云 Matgo](https://www.matgo.cn)** | 新用户绑定微信领 **5 元体验金 / 5 小时 GPU**；摩尔线程 MUSA 卡限时免费活动 | 按时计费 | 国产 GPU 体验、AI 教学实训 |

> 国内大厂（阿里云 FC、华为云等）常做"新用户首购免费 / 体验赠送"活动，但羊毛往往只能薅一次，需规划使用时间。

> 💡 **附：国内免费模型 API（注意：是 token 额度，不是让你跑自定义代码的 GPU 算力）**
> 这些适合"只调 API 做应用"，不满足"我要租卡训练"的需求（详见第七节避坑 #2）：
> - **[火山方舟（字节）](https://console.volcengine.com/ark)** — 每模型 50 万 tokens 免费（安心体验模式），企业协作计划每日 500 万
> - **[硅基流动 SiliconFlow](https://cloud.siliconflow.cn)** — 新用户 2000 万 tokens 免费（DeepSeek/Llama 等开源）
> - **[智谱 AI](https://open.bigmodel.cn)** — 新用户 2000 万 tokens（GLM 系列，永久）
> - **[阿里百炼](https://bailian.aliyun.com)** — 每模型 100 万 tokens 免费（千问/DeepSeek 全系，永久）
> - **[Hyperbolic](https://www.hyperbolic.ai)**（国际）— 免费推理 API（60 req/min、无需卡，含 Qwen3-235B / DeepSeek-V3 等）；⚠️ **GPU 算力本身无免费档**（按小时付费 $0.16 起），别把它当免费 GPU 云

---

## 四、AMD 系免费 GPU（注册送积分 / 信用值，国内可直接访问）

> 用户特别指出的一类——**注册即送积分/信用值、可兑换 GPU 服务时长**，主要由 AMD 提供。AMD 同时有**中文站（国内可访问、微信登录）**和**海外站（美元信用值、Instinct 大卡）**两套，免费额度机制清晰，是经常被漏掉的高性价比来源。

### 4.1 AMD AI 开发者计划（中文站 / 中国区官方）[developer.amd.com.cn](https://developer.amd.com.cn)
| 项目 | 内容 |
|---|---|
| **注册即送** | 活动期 **100 小时中国区专属算力**（另有"200 小时免费送"活动，以官网当期为准） |
| **积分体系** ⭐ | 完善信息 +100 积分、活跃贡献累积积分，**等额兑换算力券**（即"积分兑换 GPU 服务时长"） |
| **进阶通道** | 通过**魔搭社区联动"开发者激励计划"**，最高累计 **1000+ 小时** GPU 算力 |
| **底层硬件** | AMD Radeon PRO W7900 等专业级 GPU |
| **登录方式** | 微信 / 魔搭社区账号 / 手机号邮箱（推荐微信，一键直达） |
| **开箱即用** | 内置技术模板与预配置工作区，浏览器登录即上手 ROCm 实战 |
| **官方支持** | 中国成员专属微信群，AMD 官方团队解答 ROCm 与硬件适配 |

> 领取流程：扫码/链接注册 → 完善信息（领 100 积分）→ 进 Radeon Cloud → 选模板/创建工作区 → 在 Profile 点 "Redeem Credits" 输入兑换链接完成兑换。

### 4.2 AMD AI Developer Program（海外站）[developer.amd.com/ai-dev-program](https://developer.amd.com/ai-dev-program.html)
| 项目 | 内容 |
|---|---|
| **注册赠信用值** | 加入计划即获 **$100 美元 AMD Developer Cloud 信用值**（自存入账户起 **30 天过期**） |
| **信用值去向（二选一）** | ① **AMD Developer Cloud**——直连 Instinct MI300X（单卡 192GB / 八卡 1536GB），跑推理/训练/微调/自定义负载；② **Fireworks AI**——托管 LLM 端点（90 天过期） |
| **额外福利** | 1 个月 DeepLearning.AI Pro 会员；每月硬件抽奖；AI Academy 课程；专属 Discord |
| **积分/任务** | 完善 Profile +100pts、完成课程 +200pts、参加活动 +500pts，可解锁更多权益 |
| **认证加成** | 通过 **ROCm Star Developer Certificate** 等可额外获免费云时长（基础 25h + 最多 50h） |

### 4.3 AMD Developer Cloud（ADC，底层算力）
- 面向独立开发者与开源贡献者，符合条件可申请免费信用值（即 4.2 的 $100）。
- 零配置：即时启动云 Jupyter Notebook，预装 vLLM / SGLang / PyTorch / Triton。
- 即用即付（绑卡）或免费时段二选一；免费额度用尽且未绑卡则 VM 被销毁、数据不可访问。

### 4.4 AUP Learning Cloud（AMD 大学计划学习云）[amd.com/learning-cloud](https://www.amd.com/en/corporate/university-program/learning-cloud.html)
| 项目 | 内容 |
|---|---|
| **面向对象** | 学生、教师、高校研究者 |
| **硬件** | AMD Ryzen AI 系统 + Radeon GPU，预配置 AI/ML 框架与实验 |
| **远程节点** | San Jose / Dublin / **Shanghai（上海）** / Taipei（Bangalore 即将上线） |
| **获取方式** | 创建 AMD 账号 → 填 AUP Learning Cloud Access Form 申请 → 审核通过后开通 |
| **适合** | 课程实训、教学、快速原型；开源栈也可本地化部署成教育 hub |

> ⚠️ **AMD 额度的三个"过期坑"**：① 中文站 100h 多为**活动期**额度，留意 Promo Expire 提示；② 海外 $100 信用值 **30 天**过期；③ Fireworks 信用值 **90 天**过期。务必激活后尽快用，别囤。

**AMD 怎么选**：国内网络 + 微信登录 + 想攒积分 → 中文站；需要 Instinct 大卡跑真训练/微调 → 海外站 $100；高校师生做课程/科研 → AUP Learning Cloud。

---

## 五、科研 / 学生 / 创业大额额度（需申请，额度大）

适合：高校师生、科研人员、AI 初创（尤其无 VC 背景也能拿）。**关键路径：先入 NVIDIA Inception，再叠加其他。**

| 项目 | 额度 | 硬性要求 | 周期 |
|---|---|---|---|
| **[NVIDIA Inception](https://www.nvidia.com/inception)**（虚拟加速器） | 免费加入；间接带来 AWS Activate $25K–$100K、优先 GPU 定价、DLI 培训、VC 网络 | AI 初创、已注册公司、<10 年、有活跃开发者、有官网；**加密币类排除** | 全年滚动，审核 1–4 周 |
| **[Nebius AI Lift](https://nebius.com/startup-program)**（需 Inception 会员） | 最高 **$150K 云额度 + $10K 推理额度**；优先 H100/H200/Blackwell | AI 初创，bootstrapped 到 pre-B 轮 | 未公开，按档 |
| **[Nebius 科研资助](https://nebius.com/research-credits)**（Research Grants） | GPU 云额度 + Token（按提案定） | 研究生/博士后/高校教师/非营利研究机构 | 2026–2027 学年申请中 |
| **[Google Cloud for Startups](https://cloud.google.com/startup)** | 最高 **$350K** | 有产品 traction 的初创 | 申请制 |
| **[Microsoft Founders Hub](https://foundershub.microsoft.com)** | 最高 **$150K** Azure 额度（含 H100） | 有上线产品、无需 VC 背书 | 申请制 |
| **[AWS Activate](https://aws.amazon.com/activate)**（经 Inception） | 最高 **$100K** | 经 Inception 通道 | 申请制 |
| **[Modal for Startups](https://modal.com/startups)** | $500 – $50K | 成立 <5 年，无 VC 也可 | 快速 |
| **[Lambda Research Grants](https://lambdalabs.com/research)** | 研究 GPU 额度 | 学术/科研 | 申请制 |
| **[Thunder Compute 学生档](https://www.thundercompute.com/students)** | 学生邮箱注册自动 $20 免费额度 | 美国高校 .edu 邮箱 | 即时到账 |
| **[Prime Intellect Fast Compute Grants](https://www.primeintellect.ai)** | **$500–$100K** 计算额度（按提案定） | 开源 AI 研究者 / 博士生 / 博士后 / 小团队；邮件投提案至 contact@primeintellect.ai；无国籍/院校限制，但须 Open-AI 方向、非闭源产品 | 申请制，审核 5–10 天 |

**堆叠策略（无 VC 背景的 AI 初创 realistic 路径）**：
1. 先申请 **NVIDIA Inception**（免费、~2–4 周）→ 解锁下游档位；
2. 再申 **Nebius AI Lift**（$150K + $10K 推理，需 Inception）；
3. 叠加 **Modal for Startups**（$500–$50K，快）；
4. 配合 **Google for Startups**（$350K）；
→ 一年可堆 **$200K+** 真实 H100/H200 额度，不稀释股权。

---

## 六、国内科研算力基础设施（公益 / 国家战略）

面向**公益科研、高校、国家级课题**，额度大但需申请/排队，不适合随手玩。

| 平台 | 资源 | 获取方式 |
|---|---|---|
| **[鹏城云脑 / 鹏城实验室](https://cloudbrain.pcl.ac.cn)** | E 级自主可控智算（A100/V100/NPU），~70% 机时对外开放 | 资源申请：cloudbrain.pcl.ac.cn；博士生/访问学者可获顶尖算力 + 津贴 |
| **[启智 AI 协作平台](https://openi.pcl.ac.cn)**（OpenI / 夸智） | 免费 A100 / V100 / 昇腾 910 NPU（鹏城云脑 + 中国算力网普惠算力） | 在线申请；A100 排队久，建议优先 V100 / 智算集群 |
| **[星云算力服务](https://data-starcloud.pcl.ac.cn)**（StarCloud，鹏城·中国算力网） | 面向全球公益科研，十年计划 3500 万卡时（支持 GEO） | data-starcloud.pcl.ac.cn；面向地球观测/遥感/气象等科学计算 |

---

## 七、⚠️ 避坑提示（必读）

1. **Oracle "always-free" 只有 CPU**——网上流传的"免费 A10 GPU"不存在。
2. **免费推理 API（Groq / Cerebras / Google AI Studio / Cloudflare Workers AI / 火山方舟 / 硅基流动 等）≠ 免费 GPU**：它们返回的是托管模型的 token，**不是让你跑自定义代码的 GPU**。别被"免费算力"字眼误导（第三节已单列标注）。
3. **大厂试用额度要信用卡，且试用期内禁 GPU**：GCP $300、Azure $200、AWS/Oracle 等价额度，需绑卡、30–90 天过期，且**试用账户直接跑 GPU 会被拦**，必须先转付费账户——对"站着不花钱的 GPU"不成立。
4. **SageMaker Studio Lab 即将关门**：2026-07-30 起停止新用户注册，现有用户可继续用；要薅趁早。
5. **会话/配额限制是常态**：Colab/Kaggle 等会闲置断开、高峰掉 CPU、配额随需求浮动。务必**频繁保存 / 挂载持久存储**（Google Drive、Kaggle 20GB、腾讯 Cloud Studio 等）。
6. **免费档多为中端 GPU + 共享硬件 + 时间限制**，不是"白嫖 H100 训练大模型"的入口；真要训练大模型，走第五节的申请档或低价租赁（AutoDL/Vast.ai/Thunder Compute）。
7. **过拟合风险**：免费算力让实验变容易，但回测/训练结果漂亮 ≠ 实盘/落地有效，注意样本外验证。

---

## 八、选择决策指南（按场景对号入座）

| 你的场景 | 首选 | 备选 |
|---|---|---|
| 深度学习入门 / 课程 / 小模型实验 | [Colab](https://colab.research.google.com)、[Kaggle](https://www.kaggle.com/code)、[飞桨 AI Studio](https://aistudio.baidu.com) | [阿里天池](https://tianchi.aliyun.com) |
| 国内网络 + 中文生态 | [魔搭 ModelScope](https://modelscope.cn)、[腾讯 Cloud Studio](https://cloudstudio.net)、[九天·毕昇](https://jiutian.10086.cn) | [华为 ModelArts](https://www.huaweicloud.com/product/modelarts.html) |
| 做模型 Demo / 推理页（Gradio） | [HF ZeroGPU](https://huggingface.co/spaces)、[魔搭](https://modelscope.cn)、[Modal](https://modal.com/pricing) | [Replicate](https://replicate.com)、[Together AI](https://www.together.ai) |
| 写代码、突发推理/批量、要缩到 0 | **[Modal](https://modal.com/pricing)**（$30/月免费） | [Replicate](https://replicate.com)、[RunPod](https://www.runpod.io) 社区 |
| 想认真训练、接实盘同代码（如 NautilusTrader） | 低价租赁 [AutoDL](https://www.autodl.com) / [Vast.ai](https://vast.ai) / [RunPod](https://www.runpod.io) / [Thunder Compute](https://www.thundercompute.com) | 或申请科研/创业额度 |
| AI 初创要大额算力且不稀释股权 | [NVIDIA Inception](https://www.nvidia.com/inception) → [Nebius](https://nebius.com/startup-program) / GCP / MS / AWS 叠加 | [Modal for Startups](https://modal.com/startups) |
| 高校师生 / 公益科研 | [鹏城云脑](https://cloudbrain.pcl.ac.cn)、[启智](https://openi.pcl.ac.cn)、[星云算力](https://data-starcloud.pcl.ac.cn)、[Nebius 科研资助](https://nebius.com/research-credits) | 各平台教育档、[AUP Learning Cloud](https://www.amd.com/en/corporate/university-program/learning-cloud.html) |
| 注册送积分/信用值、想用 AMD 硬件练 ROCm | [AMD 中文站](https://developer.amd.com.cn)（积分兑算力）/ [海外站 $100](https://developer.amd.com/ai-dev-program.html) | [AUP Learning Cloud](https://www.amd.com/en/corporate/university-program/learning-cloud.html)（师生） |
| 学生零成本试水（无卡） | [Thunder Compute $20](https://www.thundercompute.com/students) / [GPUHub $3](https://gpuhub.com)（与 AutoDL 同属视拓云 Seetacloud） | [Colab](https://colab.research.google.com) |

---

## 九、参考来源（检索于 2026-07-15，含复核更新）

**通用 / 海外**
- [aimultiple.com/gpu-cluster](https://aimultiple.com/gpu-cluster) — Top 6 Free Cloud GPU Services
- [gputracker.dev/blog/google-colab-alternatives](https://gputracker.dev/blog/google-colab-alternatives) — 2026 Colab 替代品实测
- [gputracker.dev/cloud-gpu-pricing](https://gputracker.dev/cloud-gpu-pricing) — 2026 云 GPU 价格（54 家）
- [dev.to Top 10 Cloud GPU Providers 2026](https://dev.to/iyanadriyansyah/top-10-cloud-gpu-providers-for-ai-in-2026-tested-compared-4hkm) — 实测对比
- [yangmao.ai GPU Cloud Free Tier Guide](https://yangmao.ai/en/compute) — 13 家免费档汇总
- [thundercompute.com/blog/free-cloud-gpu-credits](https://www.thundercompute.com/blog/free-cloud-gpu-credits) — 2026 十大免费 GPU 额度（$250K+）
- [aicreditmart.com Modal Free Tier $30](https://aicreditmart.com/ai-credits-providers/modal-free-tier-how-to-get-30-month-in-compute-credits-2026/) / [Lightning AI Free](https://aicreditmart.com/ai-credits-providers/lightning-ai-free-plan-22-gpu-hours-month-guide-2026/) / [Colab Free](https://aicreditmart.com/ai-credits-providers/google-colab-free-tier-t4-gpu-access-guide-2026/) / [SageMaker Studio Lab](https://aicreditmart.com/ai-credits-providers/amazon-sagemaker-studio-lab-free-ml-environment-guide-2026/)
- [aws.amazon.com SageMaker Studio Lab 可用性变更](https://docs.aws.amazon.com/en_en/sagemaker/latest/dg/studio-lab.html) — **2026-07-30 关闭新用户注册**
- [saturncloud.io](https://saturncloud.io/) / [saturncloud.io/try/dask-on-saturncloud](https://saturncloud.io/try/dask-on-saturncloud) — 免费档 10 GPU-h/月
- [lightning.ai/notebooks](https://lightning.ai/notebooks) / [usagepricing.com/lightning-ai](https://usagepricing.com/blueprint/lightning-ai) — 免费档 15 额度≈75 T4 GPU-h/月（官方页口径）
- [intel.com Tiber AI Cloud](https://ai.cloud.intel.com/products) — Intel Tiber AI Cloud
- [thundercompute.com](https://www.thundercompute.com/) / [thundercompute.com/students](https://www.thundercompute.com/students) — $20 学生免费额度
- [salad.com](https://www.salad.com/) — SaladCloud 分布式 GPU
- [datacrunch.io](https://datacrunch.io/) / [genesishpc.com](https://genesishpc.com/) — 欧盟便宜云
- [modal.com/pricing](https://modal.com/pricing) / [replicate.com](https://replicate.com/) / [together.ai](https://www.together.ai/) / [runpod.io](https://www.runpod.io/) / [vast.ai](https://vast.ai/)
- [gpuhub.com](https://gpuhub.com/) — GPUHub（新加坡视拓云，与 AutoDL 同公司；社区 $3 免费额度）
- [supermicro.com Startup Accelerator (LaunchPad)](https://www.supermicro.com/en/featured/startup-accelerator-program) — NVIDIA LaunchPad 企业级免费 GPU（限时窗口）；[developer.nvidia.cn LaunchPad 试用](https://developer.nvidia.cn/blog/managing-edge-ai-with-fleet-command-and-launchpad)
- [aicredits.dev Prime Intellect Grants](https://aicredits.dev/submissions/176-prime-intellect-fast-compute-grants-500-100k) — $500–$100K 计算额度（邮件申请制，Open-AI 方向）
- [hyperbolic.ai](https://www.hyperbolic.ai/) / [apivault Hyperbolic](https://www.apivault.directory/providers/hyperbolic) — 免费推理 API（60 req/min、无需卡）；GPU 算力本身无免费档

**国内 / AMD**
- [modelscope.cn](https://modelscope.cn) — 魔搭社区
- [aistudio.baidu.com](https://aistudio.baidu.com) — 飞桨 AI Studio
- [jiutian.10086.cn](https://jiutian.10086.cn) — 九天·毕昇
- [tianchi.aliyun.com](https://tianchi.aliyun.com) — 阿里天池
- [cloudstudio.net](https://cloudstudio.net) — 腾讯云 Cloud Studio
- [huaweicloud.com/modelarts](https://www.huaweicloud.com/product/modelarts.html) — 华为 ModelArts
- [autodl.com](https://www.autodl.com) — AutoDL
- [virtaicloud.com](https://www.virtaicloud.com) — 趋动云 VirtAI / OrionX
- [matgo.cn](https://www.matgo.cn) — 矩池云 Matgo
- [console.volcengine.com/ark](https://console.volcengine.com/ark) — 火山方舟（字节）
- [cloud.siliconflow.cn](https://cloud.siliconflow.cn) — 硅基流动 SiliconFlow
- [open.bigmodel.cn](https://open.bigmodel.cn) — 智谱 AI
- [bailian.aliyun.com](https://bailian.aliyun.com) — 阿里百炼
- [developer.amd.com.cn](https://developer.amd.com.cn) / [developer.amd.com/ai-dev-program](https://developer.amd.com/ai-dev-program.html) — AMD AI 开发者计划（中文站 + 海外站）
- [amd.com Developer Cloud 免费信用值](https://www.amd.com/developer/resources/cloud-access.html)
- [amd.com AUP Learning Cloud](https://www.amd.com/en/corporate/university-program/learning-cloud.html)
- [github.com/datawhalechina/hello-rocm](https://github.com/datawhalechina/hello-rocm) — AMD Radeon Cloud 中文站使用教程
- [devpress.csdn.net AMD 200 小时算力领取](https://devpress.csdn.net/v1/article/detail/161649354) — AMD 200 小时算力领取指南

**科研 / 创业额度**
- [nvidia.com/inception](https://www.nvidia.com/inception) — NVIDIA Inception
- [nebius.com/startup-program](https://nebius.com/startup-program) / [nebius.com/research-credits](https://nebius.com/research-credits) — Nebius 额度
- [cloud.google.com/startup](https://cloud.google.com/startup) / [foundershub.microsoft.com](https://foundershub.microsoft.com) / [aws.amazon.com/activate](https://aws.amazon.com/activate) — 三大云初创计划
- [modal.com/startups](https://modal.com/startups) / [lambdalabs.com/research](https://lambdalabs.com/research) — Modal/Lambda 科研档
- [cloudbrain.pcl.ac.cn](https://cloudbrain.pcl.ac.cn) / [openi.pcl.ac.cn](https://openi.pcl.ac.cn) / [data-starcloud.pcl.ac.cn](https://data-starcloud.pcl.ac.cn) — 鹏城云脑 / 启智 / 星云算力

---

*本清单为公开信息汇编，不构成任何平台的官方承诺；额度、价格、申请条件以各平台官网实时公布为准。复核更新于 2026-07-15（修正 Saturn/Lightning 免费档口径、标注 SageMaker Studio Lab 即将关新注册、增补 Thunder Compute/SaladCloud/趋动云/矩池云 及国内免费模型 API）；同日对 4 个存疑 URL 做 WebFetch 验证：gpuhub.io（无内容，已更正为 **gpuhub.com**）、jiutian.10086.cn / matgo.cn / virtaicloud.com 均确认有效；并补注 GPUHub 与 AutoDL 同属视拓云。*
*二次真实性复核（2026-07-15 第二轮）：① SageMaker Studio Lab 关新注册（2026-07-30）经 AWS 官方文档确认 ✅；② Lightning AI 免费档据官网更正为 **75 T4 GPU-h/月**（原 22/80h 不实）；③ Saturn Cloud 官方口径 10 GPU-h/月（第三方"30h/无限"为不一致说法）；④ 新增 **NVIDIA LaunchPad**（企业级限时窗口，非稳定免费 Notebook）、**Prime Intellect Fast Compute Grants**（$500–$100K 申请制）、**Hyperbolic 免费推理 API**（GPU 算力无免费档）；⑤ AMD 中文站 100h/200h 为促销口径，登录页 JS 渲染无法实时抓取，标注"以注册后控制台为准"。*
