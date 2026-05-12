<div align="center">
  <h1>deepseek-eyes</h1>
  <p>给 DeepSeek 装上眼睛 — 接入阿里云百炼视觉模型，让没有原生识图能力的模型也能理解图片内容。</p>

  [![GitHub stars](https://img.shields.io/github/stars/20kiki/deepseek-eyes?style=social)](https://github.com/20kiki/deepseek-eyes/stargazers)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
  [![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-orange)](https://claude.ai/code)
  [![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://python.org)
</div>

**Language:** [English](../README.md) | [简体中文](README.md)

---

## 📋 目录
- [它能解决什么](#-它能解决什么)
- [工作原理](#-工作原理)
- [可用模型](#-可用模型)
- [免费额度](#-免费额度)
- [快速开始](#-快速开始)
- [安装](#-安装)
- [标签](#标签)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## 🔍 它能解决什么

当前 DeepSeek 不支持原生的图片输入。当你向 DeepSeek 发送截图、照片、示意图时，它无法直接「看到」图片内容。

> 有消息说 DeepSeek 之后会推出多模态模型，狠狠期待！但在此之前，这个工具可以帮你先顶上。

## 🔍 工作原理

```
你的图片 → eyes.py → 百炼视觉模型 → 中文文字描述 → 当前对话模型
```

脚本把你的图片发送到阿里云百炼的视觉 API，获取详细的文字描述后打印到终端。当前模型读取这段文字来回答你的问题——它不需要直接"看"图片。

## 🎯 可用模型

参考 [百炼官方文档](https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2845871)，通过 `--model` 参数切换：

| 模型 | 说明 |
| :--- | :--- |
| `qwen3.6-plus`（默认）| 最新一代旗舰，性能最强，万物识别/OCR/物体定位 |
| `qwen3.6-flash` | 速度更快，成本更低 |
| `qwen3-vl-plus` | 专用视觉语言模型，高精度物体识别与定位 |

## 💰 免费额度

阿里云百炼对新用户有免费额度，无需付费即可使用以上所有模型：

- 每模型系列赠送 **100 万 Token**
- 有效期 **90 天**（自开通之日起）
- 仅限中国大陆版

> 注册后在 [百炼控制台](https://bailian.console.aliyun.com/) 获取 API Key 即可。建议开启「免费额度用完即停」避免超额扣费。额度用完后按量计费，视觉模型约 ¥1/百万 Token 起。

## 🚀 快速开始

> **前置条件：** 电脑上已安装 `git` 和 `python`。在终端输入 `git --version` 和 `python --version` 检查。

### 第一步 — 安装 skill

打开终端：
- **macOS / Linux：** 打开终端（Terminal）
- **Windows：** `Win + R`，输入 `powershell`，回车

运行：

```bash
git clone https://github.com/20kiki/deepseek-eyes.git ~/.claude/skills/deepseek-eyes
```

这条命令把项目下载到 Claude Code 的 skills 文件夹。以后想更新，进入该文件夹执行 `git pull`。

### 第二步 — 安装 Python 依赖

```bash
pip install dashscope
```

### 第三步 — 获取 API Key

在 [百炼控制台](https://bailian.console.aliyun.com/) 注册并创建 API Key，然后设置到系统中：

**macOS / Linux — 在终端中执行：**
```bash
echo 'export DASHSCOPE_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc
```
若使用 zsh，将 `.bashrc` 替换为 `.zshrc`。

**Windows — 在 PowerShell 中执行：**
```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", "User")
```
设置后需重启终端。临时使用：`$env:DASHSCOPE_API_KEY="your-api-key"`（仅当前窗口有效）。

### 第四步 — 完成

在 Claude Code 中分享任意图片并提出问题，skill 会自动处理。

## 📦 安装

### Claude Code
```bash
git clone https://github.com/20kiki/deepseek-eyes.git ~/.claude/skills/deepseek-eyes
```

Claude Code 会自动发现。请先确保已 `pip install dashscope` 并配置好 `DASHSCOPE_API_KEY`（见[快速开始](#快速开始)）。

### 手动 / 其他平台
直接运行 `eyes.py`，将输出文本粘贴到任何 LLM 对话中即可。

## 📁 项目结构

```
├── README.md          # 英文说明
├── SKILL.md           # Skill 定义
├── eyes.py            # 核心脚本
├── requirements.txt   # Python 依赖 (dashscope)
├── LICENSE            # MIT
└── zh-CN/
    └── README.md      # 当前文件（中文说明）
```

## 标签

[`deepseek`](https://github.com/topics/deepseek) [`vision`](https://github.com/topics/vision) [`multimodal`](https://github.com/topics/multimodal) [`claude-code`](https://github.com/topics/claude-code) [`skill`](https://github.com/topics/skill) [`bailian`](https://github.com/topics/bailian) [`qwen`](https://github.com/topics/qwen) [`image-understanding`](https://github.com/topics/image-understanding)

## 🤝 贡献指南

欢迎贡献。详见 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 📄 许可证

MIT
