---
title: "个人主页从 0 到 1：Jekyll + GitHub Pages + AI Agent 完全指南"
author: Fu Qilin
categories: [Tutorial]
tags: [jekyll, github-pages, ai-agent, vibe-coding, chirpy]
date: 2026-04-27
excerpt: "从静态网页概念到 Jekyll 核心结构，从选主题到 AI Agent 辅助开发，再到 GitHub Pages 部署上线——一篇带你从零搭建个人主页的完整指南。"
mermaid: true
---

{% raw %}

> **本文同步发布于 [CSDN](https://blog.csdn.net/Qnesp/article/details/160060289)。**
>
> 文中的 [Demo](https://70asunflower.github.io/) 即为本站。

---

## 第一章：静态网页是什么？Jekyll 和它什么关系？

在动手做个人主页之前，你需要先理解一个基础概念：**静态网页**。因为 Jekyll 最终产出的就是静态网页，但它和"手写的静态网页"又有本质区别。

### 1.1 静态网页的定义

**静态网页**，就是服务器上直接存着一个完整的 `.html` 文件。

当你在浏览器里输入网址，服务器找到这个文件，原封不动地发给你，浏览器渲染出来给你看。

比如，你的服务器上有一个 `about.html` 文件：

```html
<!DOCTYPE html>
<html>
<head><title>关于我</title></head>
<body>
  <h1>关于我</h1>
  <p>我叫张三，是一名开发者。</p>
</body>
</html>
```

用户访问 `你的域名/about.html`，服务器就把这个文件的内容返回了。就这么简单。

**静态网页的特点**：
- 不需要数据库
- 不需要后端语言（PHP、Python、Node.js 等）
- 访问速度快（直接返回文件，不用计算）
- 极其安全（没有数据库注入、没有代码执行漏洞）

### 1.2 纯手写静态网页的痛点

假设你要做一个个人主页，有这几个页面：
- 首页
- 关于我
- 博客文章 1
- 博客文章 2
- ……
- 博客文章 10

如果你**纯手写 HTML**，会面临什么问题？

**痛点一：改导航栏要改 N 个文件**

每个页面都有相同的导航栏。有一天你想把"博客"改成"文章"，你要打开所有页面，一个一个改。

**痛点二：加一篇文章非常麻烦**

你要复制一个现有的文章 HTML，改标题、改日期、改正文内容、改侧边栏的"最新文章"链接……稍微漏改一处，整个网站就有问题。

**痛点三：没有模板复用**

每个页面的 HTML 结构都是独立的，你不能"继承"一个母版。

这就是为什么很多人觉得做个简单网站也很累。不是网站本身复杂，而是**维护成本高**。

### 1.3 Jekyll 是什么？

**Jekyll 是一个静态网站生成器（Static Site Generator, SSG）**。

官方定义是：*"一个把纯文本文件转换成静态网站的 Ruby 工具。"*

用人话说就是：

> 你写**内容**（Markdown 文章）和**模板**（HTML 布局），Jekyll 帮你把它们组装成一个完整的静态网站。

**Jekyll 的核心工作流程**：

```
输入                              输出
┌─────────────────┐              ┌─────────────────┐
│  Markdown 文章   │              │                 │
│  (你写的内容)     │              │  完整的 HTML     │
├─────────────────┤   Jekyll     │  网站            │
│  HTML 模板       │  ────────→   │  (_site/ 文件夹) │
│  (布局、样式)     │              │                 │
├─────────────────┤              │  可以直接部署     │
│  _config.yml    │              │  到任何服务器     │
│  (站点配置)      │              │                 │
└─────────────────┘              └─────────────────┘
```

**举个例子**：

你用 Markdown 写了一篇文章 `2026-01-15-hello.md`：

```markdown
---
title: 我的第一篇文章
date: 2026-01-15
---

这是我的第一篇博客。欢迎来到我的个人主页！
```

你有一个文章模板 `_layouts/post.html`，定义了文章的布局结构。

Jekyll 运行后，会自动把 Markdown 内容塞进模板，生成一个完整的 `hello.html`。

### 1.4 关键区别：Jekyll vs 纯手写静态网页

| 维度 | 纯手写 HTML 静态网页 | Jekyll 生成的静态网页 |
|------|---------------------|----------------------|
| **改导航栏** | 打开每个页面，一个一个改 | 改 `_includes/header.html` 一个文件，重新生成即可 |
| **加一篇文章** | 复制现有 HTML，手动改标题、日期、链接、正文…… | 新建一个 `.md` 文件，写正文，Front Matter 里写标题和日期 |
| **需要掌握的技术** | HTML + CSS | 同左 + 了解 Jekyll 的文件夹约定（约 30 分钟） |
| **最终结果** | 你手写的那些 HTML 文件 | `_site/` 文件夹里自动生成的完整 HTML 网站 |
| **用户访问时看到的是** | 静态 HTML | 同样是静态 HTML（没有数据库、没有后端） |

**核心结论**：

> Jekyll 不是运行时框架，用户访问你的网站时，看到的仍然是**纯静态 HTML**。Jekyll 的作用是**帮你生产这些 HTML 文件**，让你不用手写重复代码。

- **纯手写**：你既是"建筑师"又是"搬砖工人"，每一块砖都要自己砌。
- **Jekyll**：你是"建筑师"，负责设计结构；Jekyll 是"搬砖工人"，负责批量生产。

### 1.5 Jekyll 和其他方案的区别

| 类型 | 代表技术 | 工作方式 | 适合场景 | 需要数据库？ |
|------|---------|---------|---------|------------|
| **纯手写静态网页** | 直接写 HTML | 每次改内容要改 HTML 文件 | 1-3 个页面的超小型站 | 否 |
| **静态网站生成器** | Jekyll、Hugo、Hexo | 用模板生成完整 HTML | 博客、个人主页、文档站 | 否 |
| **动态网站** | WordPress、Django、Rails | 每次访问实时渲染 | 电商、论坛、需要登录的系统 | 是 |
| **单页应用（SPA）** | React、Vue | 浏览器下载空壳，JS 动态取数据 | 复杂的交互应用 | 通常需要 |

**Jekyll 的独特优势**：
- 比纯手写高效（不用重复劳动）
- 比动态网站简单（不用配数据库、不用操心安全）
- 访问速度极快（纯静态文件）
- 可以免费托管在 GitHub Pages

### 1.6 这一章的小结

1. **静态网页**就是服务器上存着的完整 HTML 文件，直接发给用户。
2. **纯手写静态网页**的痛点是：改一个公共组件要改 N 个文件，加内容很麻烦。
3. **Jekyll** 是一个自动化的"组装工厂"，你给内容和模板，它生成完整的静态网站。用户访问时看到的仍然是纯静态网页。

---

## 第二章：Jekyll 的核心结构（先看懂框架）

在让 AI Agent 帮你干活之前，你需要先知道 Jekyll 项目里每个文件夹是干什么的。不用背，但要知道"什么东西该放哪里"。

### 2.1 一张图看懂目录结构

```
你的项目文件夹/
├── _config.yml          # 站点的总配置文件
├── index.md             # 首页（也可以是 index.html）
├── about.md             # 关于页面（自定义页面）
├── _posts/              # 文章放这里
│   ├── 2026-01-15-第一篇文章.md
│   └── 2026-01-20-第二篇文章.md
├── _layouts/            # 页面布局模板
│   ├── default.html     # 默认布局（所有页面的基础骨架）
│   ├── post.html        # 文章布局（继承或使用 default）
│   └── page.html        # 普通页面布局
├── _includes/           # 可复用的零件
│   ├── header.html      # 网站头部
│   ├── footer.html      # 网站底部
│   └── sidebar.html     # 侧边栏
├── assets/              # 静态资源
│   ├── css/
│   │   └── main.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── avatar.jpg
├── _site/               # 🔴 生成的完整网站（不要手动改这个文件夹）
└── .gitignore           # Git 忽略文件（一般把 _site/ 加进去）
```

**你只需要记住**：写文章去 `_posts/`，改布局去 `_layouts/`，改零件去 `_includes/`，改配置去 `_config.yml`。

### 2.2 逐个解释：每个文件/文件夹是干什么的

#### `_config.yml` —— 整个站点的总开关

这是 Jekyll 最重要的配置文件，放在项目根目录。

一个最基础的 `_config.yml` 长这样：

```yaml
# 站点设置
title: 张三的个人主页
description: 开发者，写代码也写博客
url: https://zhangsan.github.io

# 主题设置
theme: minima

# 构建设置
permalink: /:year/:month/:day/:title/
timezone: Asia/Shanghai

# 导航菜单（很多主题会用到）
header_pages:
  - index.md
  - about.md
```

**你通常会让 AI Agent 帮你改这个文件**：改网站标题、改 URL、改导航菜单、改主题配色等。

#### `_posts/` —— 文章放这里

所有博客文章都放在这个文件夹里。有一个**严格的命名规则**：

```
YYYY-MM-DD-标题.md
```

例如：
- `2026-01-15-我的第一篇文章.md`
- `2026-01-20-关于Jekyll的学习笔记.md`

**为什么必须这样命名**？因为 Jekyll 会从文件名里解析出文章的日期和 URL。

一篇文章的内容长这样：

```markdown
---
title: 我的第一篇文章
layout: post
categories: 随笔
---

这里是文章正文。用 Markdown 写。

## 二级标题

- 列表项 1
- 列表项 2
```

顶部 `---` 包裹的部分叫 **Front Matter**，后面会讲。

#### `_layouts/` —— 页面布局模板

`_layouts` 里放的是 HTML 骨架。它定义了"页面长什么样"，但不写具体内容。

**`default.html`** —— 最基础的布局，通常包含：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{{ page.title }} | {{ site.title }}</title>
  <link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
  {% include header.html %}
  
  <main>
    {{ content }}
  </main>
  
  {% include footer.html %}
</body>
</html>
```

注意 `{{ content }}` 这个特殊标记 —— 具体页面的内容会被填到这里。

**`post.html`** —— 文章布局，可以继承 `default`：

```html
---
layout: default
---

<article>
  <h1>{{ page.title }}</h1>
  <p class="date">{{ page.date | date: "%Y-%m-%d" }}</p>
  
  <div class="content">
    {{ content }}
  </div>
</article>
```

#### `_includes/` —— 可复用的零件

`_includes` 里放的是页面的一部分，可以被任何布局或页面引用。

比如 `header.html`：

```html
<header>
  <nav>
    <a href="/">首页</a>
    <a href="/about">关于</a>
    <a href="/blog">博客</a>
  </nav>
</header>
```

在布局里用 `{% include header.html %}` 就能把它插进来。

**好处**：导航栏只需要维护这一个文件，所有引用它的页面自动同步。

#### `_site/` —— 🔴 生成的完整网站（不要手动改）

当你运行 `jekyll build` 后，Jekyll 会把所有东西组装好，输出到 `_site/` 文件夹。

这个文件夹里就是你最终要部署的完整网站：所有 `.md` 都变成了 `.html`，所有模板都被填充好了。

**重要**：
- 不要手动修改 `_site/` 里的任何文件 —— 下次重新生成会被覆盖。
- 通常把 `_site/` 加入 `.gitignore`，不提交到 Git 仓库（因为可以重新生成）。

#### `index.md` / `index.html` —— 首页

用户访问你网站根路径时看到的就是这个文件。

如果想在首页展示文章列表，可以用 Liquid 模板语言：

```liquid
---
layout: default
---

<h1>最新文章</h1>

<ul>
  {% for post in site.posts limit:5 %}
    <li>
      <a href="{{ post.url }}">{{ post.title }}</a>
      <span>{{ post.date | date: "%Y-%m-%d" }}</span>
    </li>
  {% endfor %}
</ul>
```

### 2.3 Front Matter：每个页面/文章开头的配置

Front Matter 是 Jekyll 最常用的功能之一。它是每个 `.md` 或 `.html` 文件开头的 YAML 配置块，用 `---` 包裹。

**示例**：

```markdown
---
title: 关于我
layout: page
permalink: /about/
---

这里是我的个人介绍。
```

**常用字段**：

| 字段 | 作用 | 示例 |
|------|------|------|
| `title` | 页面/文章的标题 | `title: 我的第一篇文章` |
| `layout` | 使用哪个布局模板 | `layout: post` |
| `permalink` | 自定义 URL | `permalink: /about/` |
| `date` | 文章日期（可覆盖文件名里的日期） | `date: 2026-01-15` |
| `categories` | 分类 | `categories: [随笔, 技术]` |
| `tags` | 标签 | `tags: [Jekyll, 教程]` |

### 2.4 Liquid：Jekyll 用的模板语言

Jekyll 使用 **Liquid** 作为模板语言。它让你可以在 HTML 里写逻辑，比如循环、条件判断、变量。

**你不需要学会写 Liquid** —— AI Agent 会帮你写。但你要能看懂大概意思：

```liquid
<!-- 循环：遍历文章列表 -->
{% for post in site.posts %}
  <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
{% endfor %}

<!-- 条件判断 -->
{% if page.author %}
  <p>作者：{{ page.author }}</p>
{% endif %}

<!-- 过滤器：格式化日期 -->
{{ page.date | date: "%Y年%m月%d日" }}
```

### 2.5 这一章的小结

| 如果你想… | 就去操作这个… |
|-----------|---------------|
| 改网站标题、URL、导航菜单 | `_config.yml` |
| 写一篇新文章 | 在 `_posts/` 新建 `YYYY-MM-DD-标题.md` |
| 改网站的整体布局（头部、底部结构） | `_layouts/default.html` |
| 改文章页面的布局 | `_layouts/post.html` |
| 改导航栏、页脚这种公共零件 | `_includes/header.html`、`footer.html` |
| 改 CSS 样式 | `assets/css/main.css` |
| 部署时传什么？ | `_site/` 里的内容（但通常让 GitHub 自动生成） |

**核心原则**：内容放 `_posts`，模板放 `_layouts`，零件放 `_includes`，配置放 `_config.yml`。

---

## 第三章：挑选一个现成的主题（不用从零开始）

有了前两章的基础，你现在知道 Jekyll 的文件夹是干什么的了。但如果要从头写一个完整的个人主页样式，还是很麻烦——要设计布局、写 CSS、做移动端适配……

**解决方案**：直接用别人做好的主题。

### 3.1 为什么选主题？

用一个现成的 Jekyll 主题，相当于你买了一栋**精装修的房子**：

| 你不需要做 | 主题已经帮你做好了 |
|-----------|-------------------|
| 设计整体布局 | 首页、文章页、关于页的 HTML 结构 |
| 写 CSS 样式 | 配色、字体、间距、响应式（手机/平板/电脑） |
| 做深色模式 | 很多现代主题自带深色/浅色切换 |
| 配置 SEO | 自动生成合适的 meta 标签 |
| 写分页逻辑 | 文章列表自动分页 |

**你要做的**：换掉里面的内容（改成你的名字、文章、社交链接），调整一些配置。

这就是 Vibe Coding 的核心思路：**站在别人的肩膀上，用 AI 帮你微调**。

### 3.2 去哪里找主题？

GitHub 上有一个专门的 Jekyll 主题集合页面：

**`github.com/topics/jekyll-theme`**

**如何筛选**：

1. **看演示链接**：大多数主题在 README 里会有一个 `Demo` 链接，点进去就能看到真实效果。
2. **看更新时间**：建议选近半年内有更新的主题，说明作者还在维护。
3. **看文档**：点进仓库，README 里安装步骤写得清晰的，对新手友好。
4. **看 Star 数**：Star 多的一般质量有保证，但新出的好主题 Star 可能不多。

### 3.3 推荐几个适合个人主页的主题

#### ① Chirpy

- **特点**：设计现代，有侧边栏头像和社交链接，自带深色/浅色切换
- **适合**：想要左侧个人简介 + 右侧文章列表这种布局的人

#### ② Minimal Mistakes

- **GitHub**：`mmistakes/minimal-mistakes`
- **特点**：功能最强大，配置选项极多，文档最完善
- **适合**：喜欢折腾、想要完全控制每个细节的人

#### ③ Beautiful Jekyll

- **GitHub**：`daattali/beautiful-jekyll`
- **特点**：极简设计，大白话文档，配置非常简单
- **适合**：想要最快上线、不想碰任何代码逻辑的人

#### ④ Jekyll TeXt

- **GitHub**：`kitian616/jekyll-TeXt-theme`
- **特点**：中文文档友好，支持多种皮肤，一键换色
- **适合**：习惯看中文文档、想要多种样式选择的用户

### 3.4 怎么选？一张决策表

| 如果你… | 推荐主题 |
|---------|---------|
| 喜欢侧边栏头像设计 | **Chirpy** |
| 想要功能最多、文档最全 | **Minimal Mistakes** |
| 想要最简单、最快上线 | **Beautiful Jekyll** |
| 习惯看中文文档 | **Jekyll TeXt** |

### 3.5 选好主题后，你要做什么？

1. **Fork 主题仓库**：复制到你自己的 GitHub 账号下
2. **克隆到本地**：让 AI Agent 帮你执行 `git clone`
3. **修改配置**：让 AI Agent 帮你改 `_config.yml`
4. **修改布局**：让 AI Agent 帮你调整首页结构
5. **预览**：运行 `jekyll s` 看效果
6. **推送**：让 AI Agent 帮你 `git push`

**你不需要做的事**：看懂所有 Liquid 代码、理解 CSS 类名关系、手动修改几十个文件。你只需要**描述你想改成什么样**，让 AI Agent 去定位文件、修改代码。

---

## 第四章：让 AI Agent 帮你克隆和修改（Vibe Coding 核心）

前几章你学会了 Jekyll 的结构，也选好了主题。现在进入真正的 Vibe Coding 环节：**让 AI Agent 帮你干所有脏活累活**。

你只需要做一件事：**用大白话描述你想改成什么样**。

### 4.1 核心理念：你是架构师，Agent 是施工队

传统开发方式：
> 你想改首页 → 找到 `index.html` → 看懂现有代码 → 手动修改 → 测试 → 提交

Vibe Coding 方式：
> 你想改首页 → 告诉 Agent "在文章列表上面加一个个人信息卡片" → Agent 找到文件、修改代码、甚至帮你提交

**你的角色**：描述"最终效果"
**Agent 的角色**：定位文件、写代码、运行命令

### 4.2 前置条件：安装 GitHub CLI（关键一步）

要让 Agent 能操作你的 GitHub 仓库，需要先安装 **GitHub CLI**（命令行工具，命令是 `gh`）。

**安装方法**：

- **macOS**：`brew install gh`
- **Windows**：`winget install --id GitHub.cli` 或去 `cli.github.com` 下载
- **Linux (Ubuntu/Debian)**：`sudo apt install gh`

**安装后登录**：

```bash
gh auth login
```

**验证是否成功**：

```bash
gh repo list
```

### 4.3 完整工作流（全程 Agent 操作）

#### 第 1 步：Fork 主题仓库

> "帮我把 `https://github.com/cotes2020/jekyll-theme-chirpy` 这个仓库 Fork 到我的 GitHub 账号下，然后用 `gh` 克隆到本地。"

```bash
gh repo fork cotes2020/jekyll-theme-chirpy --clone
```

#### 第 2 步：安装依赖

> "进入项目目录，安装 Jekyll 依赖。"

```bash
cd jekyll-theme-chirpy
bundle install
```

#### 第 3 步：修改配置文件

> "帮我修改 `_config.yml`：把 `title` 改成'张三的个人主页'，社交链接只保留 GitHub 和 Twitter。"

Agent 会读取文件 → 定位到对应行 → 修改内容 → 保存。

#### 第 4 步：修改首页布局

> "Chirpy 的首页默认是文章列表。我想在文章列表上面加一个个人信息卡片。"

Agent 会找到控制首页的文件 → 看懂现有 Liquid 代码 → 插入新的 HTML。

**你不需要知道**改哪个文件、怎么写 Liquid——Agent 会搞定。

#### 第 5 步：本地预览

> "启动本地服务器，让我预览效果。"

```bash
bundle exec jekyll s --livereload
```

打开 `http://localhost:4000` 就能看到效果。

#### 第 6 步：不满意继续改

> "头像太小了，改成 100px 的圆形。社交按钮不要文字，只要图标。"

Agent 会继续修改，直到你满意。

#### 第 7 步：提交并推送

> "帮我提交所有修改，推送到 GitHub。"

```bash
git add .
git commit -m "自定义首页布局，添加个人信息卡片"
git push origin main
```

### 4.4 Agent 能操作到什么程度？

| 操作类型 | 具体能力 | 示例提示词 |
|---------|---------|-----------|
| **读取文件** | 查看任何文件的内容 | "帮我看一下 `_config.yml` 里有哪些配置项" |
| **修改文件** | 定位到具体行并修改 | "把 `title` 改成'张三的博客'" |
| **新建文件** | 创建新页面、新样式 | "帮我新建一个 `projects.md`" |
| **运行命令** | 执行 Git、Jekyll、bundle 等 | "运行 `jekyll build`" |
| **Git 操作** | add、commit、push、PR | "提交并推送" |
| **GitHub 操作** | 创建仓库、开启 Pages | "帮我把这个仓库的 GitHub Pages 打开" |

### 4.5 常用提示词模板（直接复制用）

**修改配置类**：
> "帮我修改 `_config.yml`：把 `[配置项]` 改成 `[新值]`。"

**修改布局类**：
> "帮我找到首页的控制文件，在 `[某个位置]` 加上 `[某个内容]`。"

**添加页面类**：
> "帮我新建一个 `[页面名].md`，布局用 `[布局名]`，内容大概是 `[描述]`。"

**调试类**：
> "我运行 `jekyll s` 后报错 `[贴报错内容]`，帮我解决。"

### 4.6 没装 GitHub CLI 怎么办？

| 步骤 | 手动操作 | Agent 帮你做什么 |
|------|---------|-----------------|
| 1. Fork | 去 GitHub 网页点 Fork 按钮 | 给你仓库链接 |
| 2. 克隆 | `git clone 你的仓库链接` | 给你完整命令 |
| 3. 改配置 | 用编辑器打开 `_config.yml` | 给你完整的修改后文件内容 |
| 4. 改布局 | 打开 Agent 指定的文件，复制粘贴代码 | 告诉你改哪个文件、给你完整代码 |
| 5. 预览 | `bundle exec jekyll s` | 给你命令 |
| 6. 推送 | `git add . && git commit -m "xxx" && git push` | 给你命令 |

**核心公式**：

> 安装 `gh` + 选一个 AI Agent + 用大白话描述 = 自动完成从克隆到部署的一切

---

## 第五章：部署上线（让全世界能看到）

### 5.1 GitHub Pages 是什么？

**GitHub Pages** 是 GitHub 提供的免费静态网站托管服务。

- **免费**：不花一分钱，没有流量限制
- **自动 HTTPS**：自动给你配好 SSL 证书
- **与 Jekyll 天生一对**：原生支持 Jekyll，推送源码自动构建
- **全球 CDN**：访问速度快

**你的个人主页上线后的地址**：
- 如果仓库名是 `你的用户名.github.io` → 访问 `https://你的用户名.github.io`
- 如果仓库名是其他名字 → 访问 `https://你的用户名.github.io/仓库名`

### 5.2 部署的本质是什么？

部署就是把 Jekyll 生成的 `_site/` 文件夹里的内容放到一个 HTTP 服务器上。

传统方式：自己买服务器 → 装 Nginx → 上传文件 → 配置域名

GitHub Pages 方式：推送代码 → GitHub 自动运行 `jekyll build` → 自动托管 `_site/` → 完成

**你不需要自己运行 `jekyll build`**，GitHub 会帮你做。

### 5.3 让 AI Agent 帮你部署

#### 第 1 步：创建仓库

> "帮我在 GitHub 上创建一个新仓库，名字叫 `你的用户名.github.io`，公开的。"

```bash
gh repo create 你的用户名.github.io --public --clone
```

> ⚠️ 仓库名必须是 `你的用户名.github.io`。这是 GitHub Pages 的特殊规则。

#### 第 2 步：推送代码

```bash
git remote add origin https://github.com/你的用户名/你的用户名.github.io.git
git branch -M main
git push -u origin main
```

#### 第 3 步：开启 GitHub Pages

> "帮我打开这个仓库的 GitHub Pages，用 main 分支的根目录。"

```bash
gh repo edit --enable-pages -b main -p /
```

#### 第 4 步：等待部署完成

部署通常需要 1-2 分钟。你可以检查状态：

```bash
gh api repos/你的用户名/你的用户名.github.io/pages
```

当 `"status"` 是 `"built"` 时，就部署成功了。

#### 第 5 步：访问你的网站

打开浏览器，访问 `https://你的用户名.github.io`

🎉 你的个人主页上线了！

### 5.4 两种构建方式：Pages 默认 vs Actions

| 对比维度 | Pages 默认构建 | GitHub Actions 构建 |
|---------|---------------|---------------------|
| **配置难度** | 零配置，自动识别 | 需要写一个 `.yml` 文件 |
| **Jekyll 版本** | 固定版本（较旧） | 你可以指定任何版本 |
| **支持的插件** | 仅限白名单内插件 | 任何 Ruby gem 都可以 |
| **构建日志** | 看不到详细日志 | 完整的构建日志，方便调试 |
| **适合场景** | 大多数个人博客/主页 | 需要特定插件或新版 Jekyll |

- **新手、不需要特殊插件** → 用 Pages 默认构建（最简单）
- **需要用特定插件** → 用 Actions

### 5.5 如果需要用 Actions（备选方案）

创建 `.github/workflows/jekyll.yml`：

```yaml
name: Build and Deploy Jekyll Site

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v5
      - name: Build with Jekyll
        run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path }}"
        env:
          JEKYLL_ENV: production
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 5.6 （可选）绑定自定义域名

如果你有自己的域名，可以绑定到 GitHub Pages：

1. 在仓库中添加域名设置：
   ```bash
   gh api repos/你的用户名/你的用户名.github.io/pages -X POST -f domain=zhangsan.com
   ```

2. 在 DNS 里添加 CNAME 记录，指向 `你的用户名.github.io`

3. 在项目根目录创建 `CNAME` 文件：
   ```bash
   echo "zhangsan.com" > CNAME
   ```

### 5.7 部署后的日常更新

网站上线后，你只需要做一件事：**写新内容，然后推送**。

- **写一篇新文章**：告诉 Agent 在 `_posts/` 里生成新文章模板
- **修改已有内容**：告诉 Agent 改什么
- **推送更新**：`git push`，GitHub 自动重新构建

### 5.8 完整流程图

```
你写内容（Markdown）
       ↓
  git push 到 GitHub
       ↓
GitHub Pages 或 Actions 自动运行 jekyll build
       ↓
  生成 _site/ 静态文件
       ↓
  托管到 GitHub Pages CDN
       ↓
全世界通过 https://你的用户名.github.io 访问
```

---

## 结语：从今天开始，你有了自己的个人主页

到这里，你已经完成了从 0 到 1 的全部流程：

1. ✅ 理解了静态网页和 Jekyll 的关系
2. ✅ 学会了 Jekyll 的目录结构
3. ✅ 挑选了喜欢的主题
4. ✅ 用 AI Agent 克隆和修改了代码
5. ✅ 部署到了 GitHub Pages，网站上线

**你现在能做什么**：
- 把链接发给别人，当作你的数字名片
- 随时写新文章，推送即更新
- 告诉 Agent 你想怎么改布局，几分钟内完成

**下一步可以探索**：
- 给网站加上评论区（用 Giscus）
- 添加访问统计（用 Google Analytics 或 Umami）
- 优化 SEO，让搜索引擎能搜到你的网站

**记住这个 Vibe Coding 的工作流**：

> 描述你想要的效果 → Agent 写代码 → 你预览验证 → 满意就推送

不需要成为 Jekyll 专家，不需要记住 Liquid 语法，不需要手写 CSS。你只需要知道"框架长什么样"，剩下的交给 AI Agent。

---

🎉 恭喜你完成了全部教程。现在去把你的个人主页链接分享给朋友吧。

---

*全文完*

{% endraw %}
