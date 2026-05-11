"""Call a DashScope vision model to describe an image. Output to file and console.

Supported models (all via MultiModalConversation API):
  Qwen3.6: qwen3.6-plus / qwen3.6-flash / qwen3.6-35b-a3b
  Qwen3.5: qwen3.5-plus / qwen3.5-flash
  Qwen3-VL: qwen3-vl-plus / qwen3-vl-flash

Reference: https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2845871
"""

import sys
import os
import base64
import argparse
from pathlib import Path

OUTPUT_FILENAME = "image_desc.txt"

AVAILABLE_MODELS = [
    # Qwen3.6 — latest generation (2026-04)
    "qwen3.6-plus",         # 性能最强，推荐优先使用
    "qwen3.6-flash",        # 速度更快，成本更低
    "qwen3.6-35b-a3b",      # 开源系列

    # Qwen3.5
    "qwen3.5-plus",         # 千问性能最强的视觉理解模型
    "qwen3.5-flash",        # 速度更快，成本更低

    # Qwen3-VL
    "qwen3-vl-plus",        # Qwen3-VL 系列性能最强
    "qwen3-vl-flash",       # 速度更快，成本更低
]

DEFAULT_MODEL = "qwen3.6-plus"


def encode_image(image_path: str) -> str:
    """Encode a local image as a base64 data URL."""
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
    parser.add_argument("--file-url", action="store_true",
                        help="Use file:// URL instead of base64")
    parser.add_argument("--high-res", action="store_true",
                        help="Enable high resolution mode (documents/tables/small text)")
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

    image_ref = f"file://{os.path.abspath(args.image)}" if args.file_url else encode_image(args.image)

    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_ref},
                {"text": args.prompt},
            ],
        }
    ]

    sys.stderr.write(f"Calling {args.model}...\n")

    kwargs = dict(model=args.model, messages=messages)
    if args.high_res:
        kwargs["vl_high_resolution_images"] = True

    resp = dashscope.MultiModalConversation.call(**kwargs)

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
