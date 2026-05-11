"""Call a DashScope vision model to describe an image. Output to file and console.

Supported models (all via MultiModalConversation API):
  qwen3.6-plus / qwen3.6-flash   — latest flagship multimodal (2026-04)
  qwen3-vl-plus / qwen3-vl-flash — dedicated vision-language models
  qwen-vl-max / qwen-vl-plus     — previous-gen commercial (stable)
  qvq-max / qvq-plus             — visual reasoning (stream-only)
  qwen-vl-ocr / qwen-vl-ocr-latest — OCR specialist
"""

import sys
import os
import base64
import argparse
from pathlib import Path

OUTPUT_FILENAME = "image_desc.txt"

# Models confirmed to work with MultiModalConversation.call()
# Reference: https://www.alibabacloud.com/help/zh/model-studio/vision-model
AVAILABLE_MODELS = [
    # --- Qwen3.6: latest flagship, native multimodal ---
    "qwen3.6-plus",
    "qwen3.6-flash",

    # --- Qwen3-VL: dedicated vision-language ---
    "qwen3-vl-plus",
    "qwen3-vl-flash",

    # --- Qwen-VL commercial (stable) ---
    "qwen-vl-max",
    "qwen-vl-plus",

    # --- QVQ: visual reasoning (stream-only, handled specially) ---
    "qvq-max",
    "qvq-plus",

    # --- Qwen-OCR: OCR specialist ---
    "qwen-vl-ocr",
    "qwen-vl-ocr-latest",
]

# Models that require stream=True
STREAM_ONLY_MODELS = {"qvq-max", "qvq-plus"}

# Models that support ocr_options
OCR_MODELS = {"qwen-vl-ocr", "qwen-vl-ocr-latest"}

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


def collect_stream_output(responses) -> str:
    """Collect text from a streaming MultiModalConversation response."""
    parts = []
    for chunk in responses:
        msg = chunk.output.choices[0].message
        content = msg.content
        if content and len(content) > 0:
            text = content[0].get("text", "")
            if text:
                parts.append(text)
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Describe an image with DashScope vision models")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("--prompt", default="请详细描述这张图片的内容。",
                        help="Custom prompt for the vision model")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        choices=AVAILABLE_MODELS,
                        help=f"Vision model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--file-url", action="store_true",
                        help="Use file:// URL instead of base64 (simpler, but may not work for all accounts)")
    parser.add_argument("--high-res", action="store_true",
                        help="Enable high resolution mode (recommended for documents/tables/OCR)")
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

    # Prepare image reference
    if args.file_url:
        image_ref = f"file://{os.path.abspath(args.image)}"
    else:
        image_ref = encode_image(args.image)

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

    # Build common kwargs
    kwargs = dict(
        model=args.model,
        messages=messages,
    )

    # Stream-only models (qvq-max, qvq-plus)
    use_stream = args.model in STREAM_ONLY_MODELS
    if use_stream:
        kwargs["stream"] = True
        sys.stderr.write("(stream mode — required for this model)\n")

    # High resolution for documents/tables
    if args.high_res:
        kwargs["vl_high_resolution_images"] = True

    # OCR-specific options
    if args.model in OCR_MODELS:
        kwargs["ocr_options"] = {"task": "text_recognition"}

    resp = dashscope.MultiModalConversation.call(**kwargs)

    if use_stream:
        text = collect_stream_output(resp)
    else:
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
