---
name: deepseek-eyes
description: "Use when the user shares an image that Claude can't natively see, or when the user asks to analyze/describe/understand an image. Route every image through this skill — send the image path to eyes.py, which calls a vision model (default qwen3-vl-plus) via 百炼 DashScope and returns a Chinese text description. Then answer the user's question based on that description."
---

# Image Vision (阿里云百炼 Vision Models)

## Overview

This skill bundles a Python script (`eyes.py`) that sends an image to 阿里云百炼 (DashScope)'s vision models and returns a detailed Chinese text description. Use this whenever the user wants help with an image.

**Background:** The current model (DeepSeek V4 Pro) cannot natively see images. This skill bridges that gap by routing images through Qwen series vision models — the vision model does the seeing, and the text description is fed back into the conversation so the main model can reason about the image content.

## When to use

- User sends an image that the current model can't display (shows as [Unsupported Image])
- User asks "what's in this image?", "describe this picture", "analyze this screenshot"
- User provides an image path and wants help understanding it

## How to use

### Step 1: Run the script

**Always pass the user's exact question as `--prompt`.** The default prompt is a fallback — a targeted question produces much better results.

```bash
python ~/.claude/skills/deepseek-eyes/eyes.py "<image_path>" --prompt "<用户的具体问题>"
```

For screenshots / UI / error messages, also enable `--high-res`:
```bash
python ~/.claude/skills/deepseek-eyes/eyes.py "<image_path>" --prompt "<用户的具体问题>" --high-res
```

For photos / scenes where precision matters, use `qwen3-vl-plus`:
```bash
python ~/.claude/skills/deepseek-eyes/eyes.py "<image_path>" --prompt "<用户的具体问题>" --model "qwen3-vl-plus" --high-res
```

### Step 2: Read the output and answer

The script prints the description to stdout. Read it directly from the command output and answer the user's question about the image based on that description.

### Prerequisites

- `pip install dashscope` (already installed globally)
- `DASHSCOPE_API_KEY` environment variable must be set
- New 百炼 users get free quota — no payment needed to try

## Available Models

| Model | Use case | Precision | Speed |
|-------|----------|-----------|-------|
| `qwen3-vl-plus` (default) | **Always use unless you need speed.** Photos, diagrams, small text, detailed scenes. Identifies artworks, authors, hidden text. | ★★★ | ★★ |
| `qwen3.6-plus` | Legacy flagship. Use when vl-plus is unavailable. | ★★ | ★★ |
| `qwen3.6-flash` | **When you just need a quick look.** Simple photos, casual use. Not for precision work — can misidentify colors. | ★ | ★★★ |

**Real test comparison** (complex illustration, all with `--high-res`):

| | qwen3-vl-plus | qwen3.6-plus | qwen3.6-flash |
|---|---|---|---|
| Output detail | ~1200 words | ~500 words | ~400 words |
| Text found | "LOVE" on balloon | none | none |
| Artwork identified | WLOP "The Sky Garden" 2018 | no | no |
| Color errors | none | none | rainbow slide → "yellow" |

## Options

| Flag | Description |
|------|-------------|
| `--model` | Switch to `qwen3.6-flash` for speed, or `qwen3.6-plus` if vl-plus is unavailable |
| `--prompt` | **Always pass the user's exact question.** Targeted questions dramatically outperform the generic default. |
| `--file-url` | Use `file://` URL instead of base64 |
| `--high-res` | **Always on for best results.** Negligible speed cost, significant accuracy gain for text and detail. |

## Notes

- **Default: `qwen3-vl-plus --high-res`.** This is the right choice for 90% of use cases.
- **Need speed?** `--model qwen3.6-flash --high-res` — fast but may miss details.
- Description prints to stdout, read it directly from the command output.
