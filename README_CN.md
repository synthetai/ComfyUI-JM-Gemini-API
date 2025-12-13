# ComfyUI-JM-Gemini-API

用于ComfyUI的自定义节点，使用Google Gemini API生成图像和视频，支持文生图、图生图、文生视频和图生视频功能。

[English](README.md) | 简体中文

## 功能特性

### 图像生成
- 支持多个Gemini图像模型：
  - `gemini-3-pro-image-preview`（默认，支持1K/2K/4K分辨率）
  - `gemini-2.5-flash-image`
- 文生图（Text-to-Image）
- 图生图（Image-to-Image）支持单张或多张图片输入
- 图片编辑模式（单图输入）
- 可配置的宽高比（1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9）
- 分辨率控制（1K, 2K, 4K）- 仅适用于gemini-3-pro-image-preview
- 最多支持10张图片输入
- 自动保存图像到ComfyUI的output目录

### 视频生成
- 支持Gemini Veo视频模型：
  - `veo-3.1-generate-preview`（默认）
  - `veo-3.1-fast-generate-preview`
  - `veo-3.0-generate-001`
  - `veo-3.0-fast-generate-001`
- 文生视频（Text-to-Video）
- 图生视频（Image-to-Video）单图动画
- 首尾帧插值（仅限Veo 3.1）
- 支持负向提示词
- 可配置的宽高比（16:9, 9:16）
- 分辨率控制（720p, 1080p）
- 时长控制（4、6、8秒）
- 自动保存视频到ComfyUI的output目录

**重要限制说明：**
- **1080p分辨率**：Veo 3.1 模型的1080p分辨率仅支持8秒时长
- **首尾帧插值**：仅支持Veo 3.1模型，且时长只能为8秒

## 安装说明

### 1. 克隆或下载仓库

将本仓库克隆或下载到ComfyUI的custom_nodes目录：

```bash
cd custom_nodes
git clone https://github.com/synthetai/ComfyUI-JM-Gemini-API.git
```

### 2. 安装依赖

```bash
cd ComfyUI-JM-Gemini-API
pip install -r requirements.txt
```

### 3. 重启ComfyUI

关闭并重新启动ComfyUI，节点将自动加载。

## 系统要求

- Python 3.8+
- ComfyUI
- google-genai >= 0.2.0
- Pillow >= 10.0.0
- torch
- torchvision
- numpy
- httpx[socks]（支持代理）

## 代理配置（可选，中国用户推荐）

由于网络原因，中国大陆用户访问Gemini API可能需要配置代理。本节点已支持HTTP/HTTPS/SOCKS5代理。

### 方法一：设置环境变量（推荐）

#### HTTP/HTTPS 代理

```bash
export HTTP_PROXY="http://代理地址:端口"
export HTTPS_PROXY="http://代理地址:端口"
```

#### SOCKS5 代理（推荐）

```bash
export HTTP_PROXY="socks5://代理地址:端口"
export HTTPS_PROXY="socks5://代理地址:端口"
```

例如，使用本地SOCKS5代理：

```bash
export HTTP_PROXY="socks5://127.0.0.1:1080"
export HTTPS_PROXY="socks5://127.0.0.1:1080"
```

### 方法二：启动ComfyUI时设置

**Linux/Mac:**

```bash
HTTP_PROXY="socks5://127.0.0.1:1080" HTTPS_PROXY="socks5://127.0.0.1:1080" python main.py
```

**Windows (PowerShell):**

```powershell
$env:HTTP_PROXY="socks5://127.0.0.1:1080"
$env:HTTPS_PROXY="socks5://127.0.0.1:1080"
python main.py
```

**Windows (CMD):**

```cmd
set HTTP_PROXY=socks5://127.0.0.1:1080
set HTTPS_PROXY=socks5://127.0.0.1:1080
python main.py
```

### 常用代理工具

- **Clash**: 支持SOCKS5和HTTP代理
- **V2Ray**: 支持SOCKS5代理
- **Shadowsocks**: 支持SOCKS5代理

配置好代理后，节点将自动通过代理访问Gemini API。

## 使用说明

### 获取Gemini API密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用您的Google账号登录
3. 创建新的API密钥
4. 复制API密钥，在节点中使用

### 节点参数说明

#### 必需输入参数：

- **gemini_api_key**：您的Gemini API密钥（字符串）
- **prompt**：描述要生成图像的文本提示词（多行文本）
- **model**：选择模型：
  - `gemini-3-pro-image-preview`（默认，支持1K/2K/4K分辨率）
  - `gemini-2.5-flash-image`（速度更快，仅使用宽高比）
- **aspect_ratio**：图像宽高比（1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9）
- **resolution**：图像分辨率（1K, 2K, 4K）
  - 注意：仅对`gemini-3-pro-image-preview`模型有效
  - 默认值：2K

#### 可选输入参数：

- **image1 ~ image10**：最多10个可选的图像输入，用于图生图
  - 连接Load Image节点的输出
  - 文生图时可以留空

#### 输出：

- **image**：生成的图像（ComfyUI IMAGE tensor格式）
  - 可连接到Preview Image或Save Image节点
  - 自动保存到ComfyUI output目录

### 使用示例

#### 1. 文生图（Text-to-Image）

1. 在工作流中添加"JM Gemini Image Generator"节点
2. 输入您的Gemini API密钥
3. 编写提示词
4. 选择模型和宽高比
5. 保持所有图像输入为空
6. 将输出连接到Preview Image节点
7. 运行工作流

#### 2. 图片编辑（单图输入）

1. 添加Load Image节点并加载图片
2. 添加"JM Gemini Image Generator"节点
3. 将Load Image的输出连接到image1输入
4. 在提示词中输入编辑指令（例如："添加日落背景"）
5. 配置模型和参数
6. 运行工作流

#### 3. 图生图（多图输入）

1. 添加多个Load Image节点
2. 分别连接到image1、image2等输入
3. 输入描述如何组合/转换这些图像的提示词
4. 运行工作流

## 模型区别

### gemini-3-pro-image-preview
- 支持分辨率参数（1K、2K、4K）
- 默认分辨率：2K
- 支持单图编辑
- 输出质量更高

### gemini-2.5-flash-image
- 生成速度更快
- 仅使用宽高比（无分辨率参数）
- 适合快速迭代

## 常见问题

### 常见错误

1. **"Gemini API key is required"（需要Gemini API密钥）**
   - 确保您已输入有效的API密钥

2. **"No images were generated"（未生成图像）**
   - 检查您的提示词是否清晰且描述详细
   - 尝试不同的宽高比或分辨率
   - 验证API密钥是否有效且有足够的配额

3. **"Failed to generate image"（生成图像失败）**
   - 检查网络连接
   - 验证API密钥权限
   - 检查Gemini API服务状态

4. **图像质量问题**
   - 对于gemini-3-pro-image-preview，尝试使用1K/2K/4K分辨率
   - 让提示词更加详细和具体

## 输出目录

生成的图像自动保存到：
- `ComfyUI/output/`目录
- 文件名格式：`{model}_{mode}_{timestamp}.png`
  - 示例：`gemini3pro_text2img_1234567890.png`

## 添加新节点

如需添加更多Gemini功能节点：

1. 在`nodes/`目录下创建新的节点文件（如`jm_gemini_video_node.py`）
2. 实现节点类并导出映射
3. 在`nodes/__init__.py`中导入并合并映射
4. 重启ComfyUI

详细说明请参考`nodes/README.md`

## 许可证

MIT License

## 鸣谢

作者：JM

基于Google Gemini API开发

## 技术支持

如遇问题或有功能建议，请访问[GitHub仓库](https://github.com/yourusername/ComfyUI-JM-Gemini-API/issues)提交Issue。

## 视频节点使用说明

### 节点：JM Gemini Video Generator（JM Gemini视频生成器）

#### 必需输入参数：
- **gemini_api_key**：您的Gemini API密钥（字符串，加密输入）
- **prompt**：描述要生成视频的文本提示词（多行文本）

#### 可选输入参数：
- **negative_prompt**：描述视频中不应包含的内容（多行文本）
- **model**：选择视频模型：
  - `veo-3.1-generate-preview`（默认，最高质量）
  - `veo-3.1-fast-generate-preview`（快速生成）
  - `veo-3.0-generate-001`（稳定版本）
  - `veo-3.0-fast-generate-001`（稳定+快速）
- **aspect_ratio**：视频宽高比（16:9或9:16，默认：16:9）
- **resolution**：视频分辨率（720p或1080p，默认：720p）
- **duration**：视频时长（4、6或8秒，默认：8秒）
- **first_image**：首帧图像（可选，用于图生视频或插值）
- **last_image**：尾帧图像（可选，仅用于Veo 3.1插值）

#### 输出：
- **video_path**：生成的视频文件路径（STRING字符串）

### 视频生成模式

#### 1. 文生视频（Text-to-Video）
1. 添加"JM Gemini Video Generator"节点
2. 输入API密钥和提示词
3. 保持两个图像输入为空
4. 配置模型和参数
5. 运行工作流 - 视频将保存到output目录

#### 2. 图生视频（Image-to-Video）
1. 添加Load Image节点并加载图片
2. 将其连接到**first_image**输入
3. 输入描述运动/动画的提示词
4. 运行工作流

#### 3. 首尾帧插值（仅限Veo 3.1）
1. 添加两个Load Image节点
2. 将第一张图片连接到**first_image**输入
3. 将最后一张图片连接到**last_image**输入
4. 选择Veo 3.1模型（veo-3.1-generate-preview或veo-3.1-fast-generate-preview）
5. **设置时长为8秒**（首尾帧插值模式必需）
6. 输入描述过渡的提示词
7. 运行工作流 - 模型将生成两帧之间的平滑插值

**重要说明**：
- 视频生成可能需要几分钟时间。节点会每10秒轮询一次API状态，最多等待20分钟。
- **1080p分辨率**仅支持**8秒时长**（Veo 3.1模型）
- **首尾帧插值**功能仅支持**Veo 3.1模型**，且**时长只能为8秒**

## 更新日志

### 版本 1.1.0
- 新增视频生成功能，添加JM Gemini Video Generator节点
- 支持Veo 3.1和Veo 3.0模型
- 文生视频功能
- 图生视频动画功能
- 首尾帧插值功能（仅限Veo 3.1）
- 重构代码结构，分离节点文件和共享工具函数

### 版本 1.0.0
- 初始版本发布
- 支持gemini-3-pro-image-preview和gemini-2.5-flash-image模型
- 文生图功能
- 图生图功能（最多10张图片）
- 可配置的宽高比和分辨率
