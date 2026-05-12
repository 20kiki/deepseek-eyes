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
- [How It Works](#-how-it-works)
- [Available Models](#-available-models)
- [Free Quota](#-free-quota)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Topics](#topics)
- [Contributing](#-contributing)
- [License](#-license)

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

> **What you need:** `git` and `python` installed. Run `git --version` and `python --version` in terminal to check.

### Step 1 — Install the skill

Open terminal:
- **macOS / Linux:** Open Terminal
- **Windows:** `Win + R`, type `powershell`, Enter

Run:

```bash
git clone https://github.com/20kiki/deepseek-eyes.git ~/.claude/skills/deepseek-eyes
```

This downloads the project into Claude Code's skills folder. Run `git pull` in that folder anytime to update.

### Step 2 — Install Python dependency

```bash
pip install dashscope
```

### Step 3 — Get API Key

Register at [Bailian Console](https://bailian.console.aliyun.com/), create an API key, then save it to your system:

**macOS / Linux — run in terminal:**
```bash
echo 'export DASHSCOPE_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc
```
Use `~/.zshrc` if you're on zsh.

**Windows — run in PowerShell:**
```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", "User")
```
Restart terminal after setting. For temporary use: `$env:DASHSCOPE_API_KEY="your-api-key"` (current session only).

### Step 4 — Done

Share any image in Claude Code and ask a question about it — the skill handles the rest.

## 📦 Installation

### Claude Code
```bash
git clone https://github.com/20kiki/deepseek-eyes.git ~/.claude/skills/deepseek-eyes
```

Claude Code auto-discovers it. Make sure `pip install dashscope` and set `DASHSCOPE_API_KEY` first (see [Quick Start](#quick-start)).

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

[`deepseek`](https://github.com/topics/deepseek) [`vision`](https://github.com/topics/vision) [`multimodal`](https://github.com/topics/multimodal) [`claude-code`](https://github.com/topics/claude-code) [`skill`](https://github.com/topics/skill) [`bailian`](https://github.com/topics/bailian) [`qwen`](https://github.com/topics/qwen) [`image-understanding`](https://github.com/topics/image-understanding)

## 🤝 Contributing

Contributions welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT
