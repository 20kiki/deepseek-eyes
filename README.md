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

DashScope 上有多个视觉模型可以调用，通过 `--model` 参数切换：

| 模型 | 特点 |
|------|------|
| `qwen3-vl-plus`（默认）| 最新一代，综合能力强，推荐 |
| `qwen-vl-max` | 上一代旗舰，效果优秀 |
| `qwen-vl-plus` | 上一代标准版，速度更快、成本更低 |

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
