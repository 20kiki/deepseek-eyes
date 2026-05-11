"""Call a DashScope vision model to describe an image. Output to file and console."""

import sys
import os
import base64
import argparse
from pathlib import Path

OUTPUT_FILENAME = "image_desc.txt"

# Available vision models on DashScope
AVAILABLE_MODELS = [
    "qwen3-vl-plus",
    "qwen-vl-max",
    "qwen-vl-plus",
]
DEFAULT_MODEL = "qwen3-vl-plus"


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
