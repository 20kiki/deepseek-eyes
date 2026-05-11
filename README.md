<div align="center">
  <h1>deepseek-eyes</h1>
  <p>Give DeepSeek eyes — route images through Alibaba Cloud Bailian vision models so models that can't natively see images can still understand them.</p>

  [![GitHub stars](https://img.shields.io/github/stars/20kiki/deepseek-eyes?style=social)](https://github.com/20kiki/deepseek-eyes/stargazers)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
  [![Platform: Claude Code](https://img.shields.io/badge/Platform-Claude%20Code-orange)](https://claude.ai/code)
  [![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-green)](https://python.org)
</div>

**Language:** [English](README.md) | [简体中文](zh-CN/README.md)

---

## 📋 Table of Contents
- [The Problem](#the-problem)
- [How It Works](#how-it-works)
- [Available Models](#available-models)
- [Free Quota](#free-quota)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Contributing](#contributing)
- [License](#license)

---

DeepSeek (and many other LLMs) cannot natively see images. When you share a screenshot, photo, or diagram, the model literally can't process it.

> DeepSeek has hinted at a multimodal model coming soon — but until then, this tool fills the gap.

## 🔍 How It Works

```
Your Image → eyes.py → Bailian Vision Model (Qwen series) → Chinese Text Description → Your Chat Model
```

The script sends your image to Alibaba Cloud Bailian's vision API, gets back a detailed description, and prints it to stdout. The LLM reads this text and answers your question — it never needs to "see" the image directly.

## 🎯 Available Models

All models use the Bailian `MultiModalConversation` API. Switch with `--model`:

| Model | Description |
| :--- | :--- |
| `qwen3.6-plus` (default) | Latest flagship — best all-around, object recognition / OCR / spatial localization |
| `qwen3.6-flash` | Faster & cheaper — MoE 35B-A3B, near-Plus quality at lower cost |
| `qwen3-vl-plus` | Dedicated vision-language — high-precision recognition, 3D localization, long video |

## 💰 Free Quota

Alibaba Cloud Bailian gives new users free API quota — no payment needed to start:

- **1 million tokens** per model series
- Valid for **90 days** from activation
- Mainland China region only
- Tip: enable "Stop when free quota exhausted" in the console to avoid unexpected charges

After the free quota runs out, vision models start at ~¥1 per million tokens.

## 🚀 Quick Start

### 1. Install

```bash
pip install dashscope
```

### 2. Get API Key

Register at [Bailian Console](https://bailian.console.aliyun.com/), create an API key, then set it in your terminal:

**macOS / Linux (permanent) — run in terminal:**
```bash
echo 'export DASHSCOPE_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc
```
Use `~/.zshrc` if you're on zsh.

**Windows (permanent) — run in PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", "User")
```
Restart terminal after setting. For temporary use: `$env:DASHSCOPE_API_KEY="your-api-key"` (current session only).

### 3. Use

```bash
# Basic usage
python eyes.py path/to/image.png

# With a specific question
python eyes.py screenshot.png --prompt "What error message is shown?"

# Switch models
python eyes.py photo.jpg --model qwen3.6-flash

# High-res mode for documents / tables / small text
python eyes.py table.png --high-res
```

The description prints directly to stdout.

## 📦 Installation

### Claude Code
```bash
cp -r . ~/.claude/skills/deepseek-eyes/
```

### Manual / Other platforms
Run `eyes.py` directly — it's a standalone script. Feed the output into any LLM conversation.

## 📁 Structure

```
├── README.md          # You are here (English)
├── SKILL.md           # Skill definition
├── eyes.py            # Core script — image → vision model → text
├── requirements.txt   # Python dependency (dashscope)
├── LICENSE            # MIT
└── zh-CN/
    └── README.md      # 简体中文
```

## Topics

`deepseek` `vision` `multimodal` `claude-code` `skill` `bailian` `qwen` `image-understanding`

## 🤝 Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT
