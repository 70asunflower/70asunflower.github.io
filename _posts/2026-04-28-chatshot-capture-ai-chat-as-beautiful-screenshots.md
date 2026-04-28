---
title: "ChatShot：把 AI 对话变成精美截图"
author: Fu Qilin
categories: [Tools]
tags: [chrome-extension, ai, open-source, chatshot]
date: 2026-04-28
excerpt: "一个浏览器插件，解决 AI 对话截图分享的所有痛点——块级选择、智能拼图、主题适配，9 大平台全覆盖。"
---

你有没有过这种经历？

想分享一段 AI 的回答，截图——满屏 UI 元素，裁剪半天还是丑；复制粘贴——代码高亮没了，数学公式乱了，表格全散架。

于是我做了一个工具来解决这件事。

## ChatShot 是什么

**ChatShot** 是一个 Chrome / Edge 浏览器扩展，把 AI 对话中你选中的内容，拼成一张干净、美观、可直接分享的图片。

核心工作流四步走：

> **Select** → **Merge** → **Stitch** → **Share**

选中你要的块 → 合并相邻块 → 拼成一张图 → 粘贴到任何地方。

![ChatShot](https://raw.githubusercontent.com/70asunflower/ChatShot/main/screenshots/promo.png){: .shadow }

## 能干什么

### 块级选择

不是整页截图。ChatShot 自动识别段落、代码块、表格、数学公式、Mermaid 图这些独立的内容块，你只需要点击选中想要的，跳过不关心的。

### 合并与拆分

选中多个相邻块后，**Shift + Click** 可以将它们合并为一个整体——比如一段文字配一段代码，合并后截出来更自然。也可以随时拆分回去。

### 两种拼图布局

| 布局 | 效果 |
|------|------|
| **↔️ Horizontal Masonry** | 瀑布流，自动填最短列，紧凑不浪费空间 |
| **↕️ Vertical Stack** | 单列纵向排列，干净整洁 |

![Vertical Stack vs Horizontal Masonry](https://raw.githubusercontent.com/70asunflower/ChatShot/main/screenshots/vertical-stitch.png){: .shadow } ![Horizontal Masonry](https://raw.githubusercontent.com/70asunflower/ChatShot/main/screenshots/horizontal-stitch.png){: .shadow }

瀑布流 vs 逐行排列的区别：

```
逐行排列:                      瀑布流:
+------+ +------+            +------+ +------+
|  1   | |      |            |  1   | |      |
|      | |  2   |            |      | |  2   |
+------+ |      |            +------+ |      |
         +------+            +------+ +------+
-- gap -- -- gap --          |  3   | +------+
+------+                     +------+ |  4   |
|  3   |                            +------+
+------+
```

### 其他特性

- **主题自动适配** — 匹配当前页面的亮色/暗色模式
- **一键复制 + 下载** — 点击 Capture，图片自动进剪贴板并下载到本地
- **完整渲染保留** — 语法高亮、KaTeX 数学公式、Mermaid 图表、表格格式，原样保留
- **响应选择器** — 可以选择对话中任意一条回复，不局限于最新的一条

## 支持哪些平台

| 平台 | 状态 |
|------|------|
| DeepSeek | ✅ |
| ChatGPT | ✅ |
| Gemini | ✅ |
| NotebookLM | ✅ |
| 豆包 (Doubao) | ✅ |
| Kimi | ✅ |
| 通义千问 (Qianwen) | ✅ |
| 智谱 (ChatGLM) | ✅ |
| Copilot | ✅ |
| Claude | 🔜 即将支持 |

国内外主流 AI 助手基本全覆盖了。

## 怎么装

1. 克隆仓库：

   ```bash
   git clone https://github.com/70asunflower/ChatShot.git
   ```

2. 打开 Chrome，访问 `chrome://extensions/`
3. 右上角打开 **开发者模式**
4. 点击 **加载已解压的扩展程序** → 选择 `ChatShot` 文件夹
5. 打开任意支持的 AI 平台 → 开始截图

Edge 同理，进入 `edge://extensions/` 操作即可。

## 怎么用

1. 在支持的 AI 平台打开对话
2. 点击工具栏的 **H**（瀑布流）或 **V**（垂直堆叠）
3. 点击选中 / 取消选中要截取的内容块
4. （可选）**Shift + Click** 合并相邻块
5. 点击 **Capture** — 图片自动复制到剪贴板并下载

## 技术实现

简单说几句，感兴趣的可以直接看源码。

- **扩展架构**：Chrome Extension Manifest V3，content script 注入
- **渲染引擎**：[html-to-image](https://github.com/bubkoo/html-to-image)（基于 SVG foreignObject）
- **数学公式**：KaTeX CSS 内联获取，确保截图时公式正常渲染
- **语法高亮**：计算样式烘焙（computed style baking），保留宿主页面原始高亮配色
- **语言**：纯 JavaScript + CSS，无框架依赖，轻量

---

项目完全开源，MIT 协议。

👉 **GitHub**: [https://github.com/70asunflower/ChatShot](https://github.com/70asunflower/ChatShot)

欢迎体验、Star、提 Issue 或 PR。
