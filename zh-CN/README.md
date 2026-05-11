# deepseek-eyes

**Language:** [English](../README.md) | [简体中文](README.md)

[![GitHub stars](https://img.shields.io/github/stars/20kiki/deepseek-eyes?style=social)](https://github.com/20kiki/deepseek-eyes/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../LICENSE)
[![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-orange)](https://claude.ai/code)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://python.org)

给 DeepSeek 装上眼睛 — 接入阿里云百炼视觉模型，让没有原生识图能力的模型也能理解图片内容。

> 有消息说 DeepSeek 之后会推出多模态模型，狠狠期待！但在此之前，这个工具可以帮你先顶上。

---

## 它解决什么问题

当前 DeepSeek 不支持原生的图片输入。当你向 DeepSeek 发送截图、照片、示意图时，它无法直接「看到」图片内容。

这个 skill 通过接入阿里云百炼（DashScope）的视觉模型来实现图片理解：

```
你的图片 → eyes.py → 百炼视觉模型 → 中文文字描述 → 当前对话模型
```

这样，即使模型本身不支持图片输入，也能基于文字描述来回答你关于图片的问题。

## 可用模型

参考 [百炼官方文档](https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2845871)，通过 `--model` 参数切换：

| 模型 | 说明 |
|------|------|
| `qwen3.6-plus`（默认）| 最新一代旗舰，性能最强，万物识别/OCR/物体定位 |
| `qwen3.6-flash` | 速度更快，成本更低 |
| `qwen3-vl-plus` | 专用视觉语言模型，高精度物体识别与定位 |

## 白嫖额度

阿里云百炼对新用户有免费额度，无需付费即可使用以上所有模型：

- 每模型系列赠送 **100 万 Token**（qwen3.6-plus 输入+输出各 100 万）
- 有效期 **90 天**（自开通之日起）
- 仅限中国大陆版

> 注册后在 [百炼控制台](https://bailian.console.aliyun.com/) 获取 API Key 即可。建议开启「免费额度用完即停」避免超额扣费。额度用完后按量计费，视觉模型约 ¥1/百万 Token 起。

---

## 快速开始

### 1. 安装依赖

```bash
pip install dashscope
```

### 2. 配置 API Key

在 [百炼控制台](https://bailian.console.aliyun.com/) 获取 API Key，然后设置环境变量：

**macOS / Linux：**
```bash
export DASHSCOPE_API_KEY="your-api-key"
```

**Windows（永久生效）：**
```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", "User")
```
设置后需重启终端。临时使用可在当前窗口 `$env:DASHSCOPE_API_KEY="your-api-key"`（仅本次有效）。

### 3. 使用

```bash
# 基本用法 (默认 qwen3.6-plus)
python eyes.py path/to/image.png

# 指定提示词
python eyes.py screenshot.png --prompt "这张图片里有什么错误信息？"

# 切换模型
python eyes.py photo.jpg --model qwen3-vl-plus

# 追求速度 / 降低成本
python eyes.py photo.jpg --model qwen3.6-flash

# 高分辨率模式（表格/文档/小字场景推荐）
python eyes.py table.png --high-res
```

描述文本直接打印到终端。

---

## 安装

### Claude Code
```bash
cp -r . ~/.claude/skills/deepseek-eyes/
```

### 手动 / 其他平台
直接运行 `eyes.py`，将输出文本粘贴到任何 LLM 对话中即可。

---

## 项目结构

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

`deepseek` `vision` `multimodal` `claude-code` `skill` `bailian` `qwen` `image-understanding`

---

## 许可证

MIT
