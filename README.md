# image-vision

解决当前 DeepSeek 无法理解图片的问题。

> 有消息说 DeepSeek 之后会推出多模态模型，狠狠期待！但在此之前，这个工具可以帮你先顶上。

## 背景

当前 DeepSeek 不支持原生的图片输入。当你向 DeepSeek 发送截图、照片、示意图时，它无法直接「看到」图片内容。

这个 skill 通过接入阿里云百炼（DashScope）的视觉模型来实现图片理解：

```
你的图片 → image_vision.py → 视觉模型 (DashScope) → 中文文字描述 → 当前对话模型
```

所有模型统一使用 `MultiModalConversation` API 调用，脚本会根据模型类型自动处理差异（如 qvq 系列的流式输出、OCR 模型的专用参数）。

## 白嫖额度

阿里云百炼对新用户有免费 API 额度：

- 访问 [百炼控制台](https://dashscope.console.aliyun.com/) 注册/登录
- 新用户通常赠送数十万 Token 的免费额度
- 额度用完后按量计费，视觉模型单价也很低

## 可用模型

以下模型均已确认可通过 `MultiModalConversation.call()` 调用，通过 `--model` 参数切换：

### 新一代旗舰（推荐）

| 模型 | 说明 |
|------|------|
| `qwen3.6-plus`（默认）| 最新旗舰多模态，图像+视频（最长 2h/2GB），1M 上下文，万物识别/OCR/智能体编程 |
| `qwen3.6-flash` | 轻量高效版，MoE 35B-A3B 架构，效果接近 Plus 成本更低 |

### 专用视觉语言模型（Qwen3-VL）

| 模型 | 说明 |
|------|------|
| `qwen3-vl-plus` | 商业版旗舰 VL，支持思考/非思考模式 |
| `qwen3-vl-flash` | 商业版快速 VL，速度优化 |

### 经典商用版（Qwen-VL）

| 模型 | 说明 |
|------|------|
| `qwen-vl-max` | 上一代旗舰，效果稳定 |
| `qwen-vl-plus` | 上一代均衡版，速度快成本低 |

### 专项模型

| 模型 | 场景 | 注意事项 |
|------|------|----------|
| `qvq-max` | 视觉推理：数学、几何、图表分析 | 仅支持流式输出，脚本自动处理 |
| `qvq-plus` | 同上，更快更轻量 | 同上 |
| `qwen-vl-ocr` | OCR 专用：文档、表格、手写提取 | 自动启用 OCR 专用参数 |
| `qwen-vl-ocr-latest` | OCR 专用最新版 | 同上 |

> 更多模型（Qwen2.5-VL 开源系列、Qwen3.5 全模态系列等）也在百炼平台上可用，但调用方式可能略有不同。以上罗列的是经脚本验证可直接通过 `--model` 切换的模型。

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
python image_vision.py "photo.jpg" --model "qwen-vl-max"

# OCR 场景：文档/表格文字提取
python image_vision.py "document.jpg" --model "qwen-vl-ocr-latest" --prompt "提取所有文字，保留表格结构"

# 视觉推理：数学题/几何证明
python image_vision.py "math_problem.png" --model "qvq-max" --prompt "解这道题"

# 使用 file:// URL 而非 base64（更简洁，但部分账号可能不支持）
python image_vision.py "photo.jpg" --file-url

# 高分辨率模式（表格/文档/小字场景推荐）
python image_vision.py "table.png" --high-res
```

输出会保存到 `image_desc.txt` 并同时打印到终端。

### 4. 作为 Claude Code Skill 使用

将整个目录复制到 `~/.claude/skills/image-vision/`，Claude Code 会自动加载 `SKILL.md` 中定义的 skill。之后当你在对话中分享图片时，Claude 会自动调用脚本来获取图片描述。

## 支持的图片格式

- PNG (.png)
- JPEG (.jpg, .jpeg)
- WebP (.webp)
- BMP (.bmp)

## License

MIT
