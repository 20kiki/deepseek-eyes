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

| Model | Use case | Precision | Speed |
| :--- | :--- | :--- | :--- |
| `qwen3-vl-plus` | **Precision work.** Photos, diagrams, small text, detailed scenes. Identifies artworks, authors, hidden text. | ★★★ | ★★ |
| `qwen3.6-plus` (default) | **General use.** Casual photos, simple screenshots. | ★★ | ★★ |
| `qwen3.6-flash` | **Quick preview only.** May misidentify colors and miss details. | ★ | ★★★ |

**Real test** (complex illustration, all with `--high-res`):

| | qwen3-vl-plus | qwen3.6-plus | qwen3.6-flash |
| :--- | :--- | :--- | :--- |
| Output detail | ~1200 words | ~500 words | ~400 words |
| Hidden text found | "LOVE" on balloon | none | none |
| Artwork identified | WLOP "The Sky Garden" 2018 | no | no |
| Color errors | none | none | rainbow → "yellow" |

> **Recommendation:** Use `--model qwen3-vl-plus --high-res` for anything where accuracy matters. Use `--model qwen3.6-plus --high-res` for casual photos. Avoid flash for precise work.

## 💰 Free Quota

Alibaba Cloud Bailian gives new users free API quota — no payment needed to start:

- **1 million tokens** per model series
- Valid for **90 days** from activation
- Mainland China region only
- Tip: enable "Stop when free quota exhausted" in the console to avoid unexpected charges

After the free quota runs out, vision models start at ~¥1 per million tokens.

## 🚀 Quick Start

> **What you need:** `python` installed. Run `python --version` in terminal to check.

### Step 1 — Install the skill

The skill is two files: `SKILL.md` + `eyes.py`. Download them into Claude Code's skills folder.

**macOS / Linux:**
```bash
mkdir -p ~/.claude/skills/deepseek-eyes
curl -o ~/.claude/skills/deepseek-eyes/SKILL.md https://raw.githubusercontent.com/20kiki/deepseek-eyes/master/SKILL.md
curl -o ~/.claude/skills/deepseek-eyes/eyes.py https://raw.githubusercontent.com/20kiki/deepseek-eyes/master/eyes.py
```

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills\deepseek-eyes"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/20kiki/deepseek-eyes/master/SKILL.md" -OutFile "$env:USERPROFILE\.claude\skills\deepseek-eyes\SKILL.md"
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/20kiki/deepseek-eyes/master/eyes.py" -OutFile "$env:USERPROFILE\.claude\skills\deepseek-eyes\eyes.py"
```

> To update later: re-run the same commands.

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
Drop `SKILL.md` and `eyes.py` into `~/.claude/skills/deepseek-eyes/`. See [Quick Start](#-quick-start) for the one-liner. Make sure `pip install dashscope` and `DASHSCOPE_API_KEY` are set first.

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
