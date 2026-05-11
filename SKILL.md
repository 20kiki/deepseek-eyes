---
name: image-vision
description: Use when the user shares an image (screenshot, photo, diagram) that Claude can't natively see, or when the user asks to analyze/describe/understand an image. Route every image the user wants analyzed through this skill — send the image path to the bundled image_vision.py script, which calls Qwen3-VL via DashScope and returns a Chinese text description. Then answer the user's question based on that description.
---

# Image Vision (Qwen3-VL)

## Overview

This skill bundles a Python script (`image_vision.py`) that sends an image to Alibaba Cloud DashScope's Qwen3-VL model and returns a detailed Chinese text description. Use this whenever the user wants help with an image.

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

### Step 2: Read the output and answer

The script saves the description to `image_desc.txt` in the current working directory. After the script runs:

1. Read `image_desc.txt`
2. Based on the description, answer the user's question about the image
3. Delete `image_desc.txt` (optional, to keep things tidy)

### Prerequisites

- `pip install dashscope` (already installed globally)
- `DASHSCOPE_API_KEY` environment variable must be set

## Notes

- The script always works — the current model never needs to "see" the image directly
- Always delete `image_desc.txt` after reading, it's a temporary artifact
- Default prompt asks for a detailed description in Chinese; override with `--prompt` for targeted questions
