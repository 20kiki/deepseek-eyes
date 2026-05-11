"""Call a 百炼 (DashScope) vision model to describe an image. Print result to stdout."""

import sys
import os
import base64
import argparse
from pathlib import Path

# Fix garbled Chinese on Windows terminal
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

AVAILABLE_MODELS = [
    "qwen3.6-plus",         # 最新一代，性能最强，推荐优先使用
    "qwen3.6-flash",        # 速度更快，成本更低
    "qwen3-vl-plus",        # 专用视觉语言模型
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
    parser = argparse.ArgumentParser(description="Describe an image with 百炼 (DashScope) vision models")
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
            "Get a free key at https://bailian.console.aliyun.com/\n"
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
    print(text)


if __name__ == "__main__":
    main()
