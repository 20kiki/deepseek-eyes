# image-vision

解决当前 DeepSeek 无法理解图片的问题。

> 有消息说 DeepSeek 之后会推出多模态模型，狠狠期待！但在此之前，这个工具可以帮你先顶上。

## 背景

当前 DeepSeek 不支持原生的图片输入。当你向 DeepSeek 发送截图、照片、示意图时，它无法直接「看到」图片内容。

这个 skill 通过接入阿里云 DashScope 的视觉模型来实现图片理解：

```
你的图片 → image_vision.py → 视觉模型 (Qwen-VL 系列) → 中文文字描述 → 当前对话模型
```

这样，即使模型本身不支持图片输入，也能基于文字描述来回答你关于图片的问题。

## 白嫖额度

阿里云 DashScope 目前对新用户有免费 API 额度，可以白嫖一把：

- 访问 [DashScope 控制台](https://dashscope.console.aliyun.com/) 注册/登录
- 新用户通常赠送数十万 Token 的免费额度
- 额度用完后按量计费，视觉模型单价也很低

## 可用模型

阿里云百炼（DashScope）平台提供丰富的视觉模型，通过 `--model` 参数切换：

### 新一代旗舰（推荐）

| 模型 | 特点 |
|------|------|
| `qwen3.6-plus`（默认）| 最新旗舰多模态，支持图像+视频（最长 2h/2GB），1M 上下文，万物识别/OCR/Agentic Coding |
| `qwen3.6-flash` | 轻量高效版，MoE 35B-A3B 架构，效果接近 Plus 但成本更低 |

### 专用视觉语言模型（Qwen3-VL）

| 模型 | 特点 |
|------|------|
| `qwen3-vl-plus` | 商业版旗舰 VL，支持思考/非思考模式 |
| `qwen3-vl-flash` | 商业版快速 VL，速度优化 |
| `qwen3-vl-235b-a22b-instruct` | 开源最大 VL（235B MoE） |
| `qwen3-vl-32b-instruct` | 开源 32B 密集模型 |
| `qwen3-vl-30b-a3b-instruct` | 开源 30B MoE 模型 |
| `qwen3-vl-8b-instruct` | 开源 8B 轻量模型 |
| `qwen3-vl-235b-a22b-thinking` / `30b-a3b-thinking` / `8b-thinking` | 以上模型 + 思维链推理版本 |

### 经典商用版

| 模型 | 特点 |
|------|------|
| `qwen-vl-max` | 上一代旗舰，效果稳定 |
| `qwen-vl-plus` | 上一代均衡版，速度快、成本低 |

### 开源系列（Qwen2.5-VL）

| 模型 | 特点 |
|------|------|
| `qwen2.5-vl-72b-instruct` | 72B 视觉语言模型 |
| `qwen2.5-vl-32b-instruct` | 32B 视觉语言模型 |
| `qwen2.5-vl-7b-instruct` | 7B 视觉语言模型 |

### 专项模型

| 模型 | 场景 |
|------|------|
| `qvq-max` | 视觉推理：数学题、几何证明、图表分析 |
| `qwen-vl-ocr` | OCR 专用：文档、表格、手写、试卷提取 |

## 快速开始

### 1. 安装依赖

```bash
pip install dashscope
```

### 2. 配置 API Key

在 [DashScope 控制台](https://dashscope.console.aliyun.com/) 获取 API Key，然后设置环境变量：

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
# 基本用法
python image_vision.py "path/to/image.png"

# 指定提示词
python image_vision.py "screenshot.png" --prompt "这张图片里有什么错误信息？"

# 指定其他模型
python image_vision.py "photo.jpg" --model "qwen-vl-max"

# 组合使用
python image_vision.py "diagram.png" --model "qwen-vl-plus" --prompt "图中一共有几个节点？"
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
