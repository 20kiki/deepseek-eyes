"""Call a DashScope vision model to describe an image. Output to file and console."""

import sys
import os
import base64
import argparse
from pathlib import Path

OUTPUT_FILENAME = "image_desc.txt"

# Vision models available on DashScope (百炼)
# Reference: https://help.aliyun.com/zh/model-studio/models
AVAILABLE_MODELS = [
    # --- Qwen3.6 (latest flagship, native multimodal, 1M context) ---
    "qwen3.6-plus",       # 旗舰多模态，支持图像+视频（最长2h/2GB），万物识别/OCR/Agentic Coding
    "qwen3.6-flash",      # 轻量高效，MoE 35B-A3B，高并发/成本敏感场景

    # --- Qwen3-VL (dedicated vision-language models) ---
    "qwen3-vl-plus",      # 商业版旗舰 VL，支持思考/非思考模式
    "qwen3-vl-flash",     # 商业版快速 VL，速度优化

    # --- Qwen3-VL open-source ---
    "qwen3-vl-235b-a22b-instruct",   # 开源最大 VL (235B MoE)
    "qwen3-vl-235b-a22b-thinking",   # 开源最大 VL + 思维链
    "qwen3-vl-32b-instruct",         # 开源 32B VL
    "qwen3-vl-30b-a3b-instruct",     # 开源 30B MoE VL
    "qwen3-vl-30b-a3b-thinking",     # 开源 30B MoE VL + 思维链
    "qwen3-vl-8b-instruct",          # 开源 8B VL
    "qwen3-vl-8b-thinking",          # 开源 8B VL + 思维链

    # --- Qwen-VL commercial (previous generation, stable) ---
    "qwen-vl-max",        # 旗舰视觉模型
    "qwen-vl-plus",       # 均衡视觉模型，速度快成本低

    # --- Qwen2.5-VL open-source (previous generation) ---
    "qwen2.5-vl-72b-instruct",
    "qwen2.5-vl-32b-instruct",
    "qwen2.5-vl-7b-instruct",

    # --- Specialized ---
    "qvq-max",            # 视觉推理专用：数学题、几何证明、图表分析
    "qwen-vl-ocr",        # OCR 专用：文档/表格/手写/试卷提取
]
DEFAULT_MODEL = "qwen3.6-plus"


def encode_image(image_path: str) -> str:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")

    suffix = path.suffix.lower()
    mime_map = {
        ".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png",
        ".webp": "webp", ".bmp": "bmp",
    }
    mime = mime_map.get(suffix, "jpeg")
    return f"data:image/{mime};base64,{data}"


def main():
    parser = argparse.ArgumentParser(description="Describe an image with DashScope vision models")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--prompt", default="请详细描述这张图片的内容。",
                        help="Custom prompt for the vision model")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        choices=AVAILABLE_MODELS,
                        help=f"Vision model to use (default: {DEFAULT_MODEL})")
    args = parser.parse_args()

    try:
        import dashscope
    except ImportError:
        sys.stderr.write("dashscope not installed. Run: pip install dashscope\n")
        sys.exit(1)

    api_key = os.environ.get("DASHSCOPE_API_KEY", dashscope.api_key or "")
    if not api_key:
        sys.stderr.write(
            "DASHSCOPE_API_KEY not set.\n"
            "Get a free key at https://dashscope.console.aliyun.com/\n"
            "New users get free quota — no payment needed to try.\n"
        )
        sys.exit(1)

    image_url = encode_image(args.image)
    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_url},
                {"text": args.prompt},
            ],
        }
    ]

    sys.stderr.write(f"Calling {args.model}...\n")

    resp = dashscope.MultiModalConversation.call(
        model=args.model,
        messages=messages,
        max_tokens_per_image=1500,
    )

    if resp.status_code != 200:
        sys.stderr.write(f"API error ({resp.status_code}): {resp.message}\n")
        sys.exit(1)

    text = resp.output.choices[0].message.content[0]["text"]

    out_path = Path.cwd() / OUTPUT_FILENAME
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"[Saved to: {out_path}]")
    print(text)


if __name__ == "__main__":
    main()
