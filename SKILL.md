---
name: deepseek-eyes
description: Use when the user shares an image (screenshot, photo, diagram) that Claude can't natively see, or when the user asks to analyze/describe/understand an image. Route every image the user wants analyzed through this skill — send the image path to the bundled eyes.py script, which calls a vision model (default: qwen3.6-plus) via DashScope and returns a Chinese text description. Then answer the user's question based on that description.
---

# Image Vision (DashScope Vision Models)

## Overview

This skill bundles a Python script (`eyes.py`) that sends an image to Alibaba Cloud DashScope's vision models and returns a detailed Chinese text description. Use this whenever the user wants help with an image.

**Background:** The current model (DeepSeek V4 Pro) cannot natively see images. This skill bridges that gap by routing images through Qwen series vision models — the vision model does the seeing, and the text description is fed back into the conversation so the main model can reason about the image content.

## When to use

- User sends an image that the current model can't display (shows as [Unsupported Image])
- User asks "what's in this image?", "describe this picture", "analyze this screenshot"
- User provides an image path and wants help understanding it

## How to use

### Step 1: Run the script

```bash
python ~/.claude/skills/deepseek-eyes/eyes.py "<image_path>"
```

With a custom prompt:
```bash
python ~/.claude/skills/deepseek-eyes/eyes.py "<image_path>" --prompt "这张图片里有什么错误信息？"
```

Switch models or enable high-res:
```bash
python ~/.claude/skills/deepseek-eyes/eyes.py "<image_path>" --model "qwen3-vl-plus" --high-res
```

### Step 2: Read the output and answer

The script prints the description to stdout. Read it directly from the command output and answer the user's question about the image based on that description.

### Prerequisites

- `pip install dashscope` (already installed globally)
- `DASHSCOPE_API_KEY` environment variable must be set
- New DashScope users get free quota — no payment needed to try

## Available Models

| Model | Notes |
|-------|-------|
| `qwen3.6-plus` (default) | Latest flagship, best all-around |
| `qwen3.6-flash` | Faster & cheaper |
| `qwen3-vl-plus` | Dedicated VL, high-precision object recognition |

## Options

| Flag | Description |
|------|-------------|
| `--model` | Switch vision model (see table above) |
| `--prompt` | Custom question/prompt for the image |
| `--file-url` | Use `file://` URL instead of base64 |
| `--high-res` | High resolution mode (documents/tables/small text) |

## Notes

- The script always works — the current model never needs to "see" the image directly
- Description prints to stdout, read it directly from the command output
- Default prompt asks for a detailed description in Chinese; override with `--prompt` for targeted questions
- Switch models with `--model` to balance speed, cost, and accuracy
