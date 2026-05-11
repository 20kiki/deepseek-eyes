# image-vision

解决当前DeepSeek无法理解图片的问题

## 解决的问题

当前DeepSeek不支持原生的图片输入。当你DeepSeek向发送截图、照片、示意图时，它们无法直接「看到」图片内容。

这个 skill 通过接入阿里云 DashScope 的 Qwen3-VL 多模态模型来实现图片理解：

```
你的图片 → image_vision.py → Qwen3-VL (视觉模型) → 中文文字描述 → 当前对话模型
```

这样，即使模型本身不支持图片输入，也能基于文字描述来回答你关于图片的问题。

## 快速开始

### 1. 安装依赖

```bash
pip install dashscope
```

### 2. 配置 API Key

在 [DashScope 控制台](https://dashscope.console.aliyun.com/) 获取 API Key，然后设置环境变量：

```bash
export DASHSCOPE_API_KEY="your-api-key"
```

或在 Windows 上：

```powershell
$env:DASHSCOPE_API_KEY="your-api-key"
```

### 3. 使用

```bash
python image_vision.py "path/to/image.png"
```

输出会保存到 `image_desc.txt` 并同时打印到终端。

**指定自定义提示词：**

```bash
python image_vision.py "screenshot.png" --prompt "这张图片里有什么错误信息？"
```

### 4. 作为 Claude Code Skill 使用

将整个目录复制到 `~/.claude/skills/image-vision/`，Claude Code 会自动加载 `SKILL.md` 中定义的 skill。之后当你在对话中分享图片时，Claude 会自动调用脚本来获取图片描述。

## 支持的图片格式

- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)
- BMP (.bmp)

## License

MIT
