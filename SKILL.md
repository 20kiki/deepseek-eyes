---
name: image-vision
description: Use when the user shares an image (screenshot, photo, diagram) that Claude can't natively see, or when the user asks to analyze/describe/understand an image. Route every image the user wants analyzed through this skill — send the image path to the bundled image_vision.py script, which calls a vision model (default: Qwen3-VL) via DashScope and returns a Chinese text description. Then answer the user's question based on that description.
---

# Image Vision (DashScope Vision Models)

## Overview

This skill bundles a Python script (`image_vision.py`) that sends an image to Alibaba Cloud DashScope's vision models and returns a detailed Chinese text description. Use this whenever the user wants help with an image.

**Background:** The current model (DeepSeek V4 Pro) cannot natively see images. This skill bridges that gap by routing images through Qwen-VL series models — the vision model does the seeing, and the text description is fed back into the conversation so the main model can reason about the image content.

## When to use

- User sends an image that the current model can't display (shows as [Unsupported Image])
- User asks "what's in this image?", "describe this picture", "analyze this screenshot"
- User provides an image path and wants help understanding it

## How to use

### Step 1: Run the script

```bash
python ~/.claude/skills/image-vision/image_vision.py "<image_path>"
```

If the user has a specific question about the image, pass it via `--prompt`:
```bash
python ~/.claude/skills/image-vision/image_vision.py "<image_path>" --prompt "这张图片里有什么错误信息？"
```

To use a different vision model, pass `--model`:
```bash
python ~/.claude/skills/image-vision/image_vision.py "<image_path>" --model "qwen-vl-max"
```

### Step 2: Read the output and answer

The script saves the description to `image_desc.txt` in the current working directory. After the script runs:

1. Read `image_desc.txt`
2. Based on the description, answer the user's question about the image
3. Delete `image_desc.txt` (optional, to keep things tidy)

### Prerequisites

- `pip install dashscope` (already installed globally)
- `DASHSCOPE_API_KEY` environment variable must be set (Alibaba Cloud DashScope)
- Free API quota available for new DashScope users

## Available Models

| Model | Notes |
|-------|-------|
| `qwen3.6-plus` (default) | Latest flagship multimodal, 1M context, image+video (2h/2GB) |
| `qwen3.6-flash` | Lightweight MoE 35B-A3B, cost-optimized |
| `qwen3-vl-plus` | Dedicated VL model with thinking mode |
| `qwen3-vl-flash` | Fast VL model |
| `qwen3-vl-235b-a22b-instruct` | Open-source 235B MoE VL |
| `qwen3-vl-32b-instruct` | Open-source 32B VL |
| `qwen3-vl-8b-instruct` | Open-source 8B VL (lightweight) |
| `qwen-vl-max` | Previous-gen flagship (stable) |
| `qwen-vl-plus` | Previous-gen standard (fast & cheap) |
| `qwen2.5-vl-72b-instruct` | Open-source 72B VL |
| `qvq-max` | Visual reasoning: math, geometry, charts |
| `qwen-vl-ocr` | OCR specialist: docs, tables, handwriting |

## Notes

- The script always works — the current model never needs to "see" the image directly
- Always delete `image_desc.txt` after reading, it's a temporary artifact
- Default prompt asks for a detailed description in Chinese; override with `--prompt` for targeted questions
- Switch models with `--model` to balance speed, cost, and accuracy
