# deepseek-eyes

解决当前 DeepSeek 无法理解图片的问题。

> 有消息说 DeepSeek 之后会推出多模态模型，狠狠期待！但在此之前，这个工具可以帮你先顶上。

## 背景

当前 DeepSeek 不支持原生的图片输入。当你向 DeepSeek 发送截图、照片、示意图时，它无法直接「看到」图片内容。

这个 skill 通过接入阿里云百炼（DashScope）的视觉模型来实现图片理解：

```
你的图片 → image_vision.py → 视觉模型 (DashScope) → 中文文字描述 → 当前对话模型
```

所有模型统一使用 `MultiModalConversation` API 调用。

## 白嫖额度

阿里云百炼对新用户有免费 API 额度：

- 访问 [百炼控制台](https://dashscope.console.aliyun.com/) 注册/登录
- 新用户通常赠送数十万 Token 的免费额度
- 额度用完后按量计费，视觉模型单价也很低

## 可用模型

参考 [百炼官方文档](https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2845871)，通过 `--model` 参数切换：

| 模型 | 说明 |
|------|------|
| `qwen3.6-plus`（默认）| 最新一代旗舰，性能最强，万物识别/OCR/物体定位 |
| `qwen3.6-flash` | 速度更快，成本更低 |
| `qwen3-vl-plus` | 专用视觉语言模型，适合高精度物体识别与定位 |

## 快速开始

### 1. 安装依赖

```bash
pip install dashscope
```

### 2. 配置 API Key

在 [百炼控制台](https://dashscope.console.aliyun.com/) 获取 API Key，然后设置环境变量：

**macOS / Linux：**
```bash
export DASHSCOPE_API_KEY="your-api-key"
```

**Windows PowerShell：**
```powershell
$env:DASHSCOPE_API_KEY="your-api-key"
```

### 3. 使用

```bash
# 基本用法 (默认 qwen3.6-plus)
python image_vision.py "path/to/image.png"

# 指定提示词
python image_vision.py "screenshot.png" --prompt "这张图片里有什么错误信息？"

# 切换模型
python image_vision.py "photo.jpg" --model "qwen3-vl-plus"

# 追求速度 / 降低成本
python image_vision.py "photo.jpg" --model "qwen3.6-flash"

# 高分辨率模式（表格/文档/小字场景推荐）
python image_vision.py "table.png" --high-res

# 使用 file:// URL 而非 base64
python image_vision.py "photo.jpg" --file-url
```

描述文本直接打印到终端。

### 4. 作为 Claude Code Skill 使用

将整个目录复制到 `~/.claude/skills/image-vision/`，Claude Code 会自动加载 `SKILL.md` 中定义的 skill。之后当你在对话中分享图片时，Claude 会自动调用脚本来获取图片描述。

## 支持的图片格式

- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)
- BMP (.bmp)

## License

MIT
