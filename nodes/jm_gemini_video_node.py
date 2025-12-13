"""
ComfyUI-JM-Gemini-API Video Node
A custom node for ComfyUI that generates videos using Google's Gemini Veo API
"""

import os
import time
import logging
import io
import tempfile
from google import genai
from google.genai import types

from .utils import tensor2pil, get_output_dir

# 设置日志
logger = logging.getLogger(__name__)

# 视频模型常量
VEO_3_1_GENERATE = "veo-3.1-generate-preview"
VEO_3_1_FAST_GENERATE = "veo-3.1-fast-generate-preview"
VEO_3_0_GENERATE = "veo-3.0-generate-001"
VEO_3_0_FAST_GENERATE = "veo-3.0-fast-generate-001"


def pil_to_image(pil_image):
    """
    将PIL Image转换为API可接受的Image格式
    使用types.Image直接构造（适用于图生视频）
    """
    # 确保图片是RGB模式（API可能不支持RGBA等格式）
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')

    # 将PIL Image转换为bytes
    image_bytes_io = io.BytesIO()
    pil_image.save(image_bytes_io, format='PNG')
    image_bytes = image_bytes_io.getvalue()

    # 使用types.Image创建Image对象
    return types.Image(
        image_bytes=image_bytes,
        mime_type="image/png"  # 修复：MIME type 应该是 "image/png" 而不是 "PNG"
    )


def pil_to_image_via_file(pil_image):
    """
    将PIL Image转换为API可接受的Image格式
    通过临时文件方式（与工作脚本保持一致）
    """
    # 确保图片是RGB模式
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        tmp_path = tmp_file.name
        pil_image.save(tmp_path, format='PNG')

    try:
        # 使用 types.Image.from_file() 加载（与工作脚本一致）
        image = types.Image.from_file(location=tmp_path)
        return image
    finally:
        # 清理临时文件
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


class JMGeminiVideoGenerator:
    """
    ComfyUI custom node for generating videos using Google Gemini Veo API
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "gemini_api_key": ("STRING", {
                    "multiline": False,
                    "default": "",
                    "placeholder": "Enter your Gemini API key",
                    "password": True
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Enter your video prompt here"
                }),
            },
            "optional": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff
                }),
                "negative_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "Enter negative prompt (optional)"
                }),
                "model": ([
                    VEO_3_1_GENERATE,
                    VEO_3_1_FAST_GENERATE,
                    VEO_3_0_GENERATE,
                    VEO_3_0_FAST_GENERATE
                ], {
                    "default": VEO_3_1_GENERATE
                }),
                "aspect_ratio": (["16:9", "9:16"], {
                    "default": "16:9"
                }),
                "resolution": (["720p", "1080p"], {
                    "default": "720p"
                }),
                "duration": (["4", "6", "8"], {
                    "default": "8"
                }),
                "first_image": ("IMAGE",),
                "last_image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("video_path",)
    FUNCTION = "generate_video"
    CATEGORY = "JM-Gemini"

    def generate_video(self, gemini_api_key, prompt, seed=0, negative_prompt="",
                      model=VEO_3_1_GENERATE, aspect_ratio="16:9",
                      resolution="720p", duration="8",
                      first_image=None, last_image=None):
        """
        主函数：调用Gemini Veo API生成视频
        """
        # seed参数仅用于ComfyUI重新执行，不传递给API

        # 验证API key
        if not gemini_api_key or not gemini_api_key.strip():
            raise ValueError("Gemini API key is required")

        # 验证prompt
        if not prompt or not prompt.strip():
            raise ValueError("Prompt is required")

        # 设置输出目录
        output_dir = get_output_dir()

        try:
            # 创建客户端
            client = genai.Client(api_key=gemini_api_key)

            # 根据输入图像判断生成模式
            if first_image is None and last_image is None:
                # 文生视频模式
                logger.info("[JM-Gemini] Text-to-Video mode")
                video_path = self._generate_text_to_video(
                    client=client,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    model=model,
                    aspect_ratio=aspect_ratio,
                    resolution=resolution,
                    duration=duration,
                    output_dir=output_dir
                )
            elif first_image is not None and last_image is None:
                # 图生视频模式
                logger.info("[JM-Gemini] Image-to-Video mode")
                video_path = self._generate_image_to_video(
                    client=client,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    model=model,
                    aspect_ratio=aspect_ratio,
                    resolution=resolution,
                    duration=duration,
                    first_image=first_image,
                    output_dir=output_dir
                )
            elif first_image is not None and last_image is not None:
                # 首尾帧生成视频模式
                # 仅支持Veo 3.1模型
                if model not in [VEO_3_1_GENERATE, VEO_3_1_FAST_GENERATE]:
                    raise ValueError("First and last frame interpolation is only supported by Veo 3.1 models")
                logger.info("[JM-Gemini] First-Last Frame Interpolation mode")
                video_path = self._generate_interpolation_video(
                    client=client,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    model=model,
                    aspect_ratio=aspect_ratio,
                    resolution=resolution,
                    duration=duration,
                    first_image=first_image,
                    last_image=last_image,
                    output_dir=output_dir
                )
            else:
                raise ValueError("Invalid image configuration: last_image provided without first_image")

            return (video_path,)

        except Exception as e:
            logger.exception(f"[JM-Gemini] Error generating video: {e}")
            raise RuntimeError(f"Failed to generate video: {str(e)}")

    def _generate_text_to_video(self, client, prompt, negative_prompt, model,
                                aspect_ratio, resolution, duration, output_dir):
        """
        文生视频模式
        """
        logger.info(f"[JM-Gemini] Generating text-to-video with model={model}, duration={duration}s")

        # 构建配置
        config_params = {
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration_seconds": int(duration),
            "person_generation": "allow_all"
        }
        if negative_prompt:
            config_params["negative_prompt"] = negative_prompt

        config = types.GenerateVideosConfig(**config_params)

        # 调用API生成视频
        operation = client.models.generate_videos(
            model=model,
            prompt=prompt,
            config=config
        )

        # 等待视频生成完成
        video_path = self._wait_and_download_video(
            client=client,
            operation=operation,
            output_dir=output_dir,
            prefix=f"{model.replace('.', '_')}_text2video"
        )

        return video_path

    def _generate_image_to_video(self, client, prompt, negative_prompt, model,
                                 aspect_ratio, resolution, duration,
                                 first_image, output_dir):
        """
        图生视频模式
        """
        logger.info(f"[JM-Gemini] Generating image-to-video with model={model}, duration={duration}s")

        # 转换图像为PIL格式，再转为Image格式
        pil_image = tensor2pil(first_image)
        image = pil_to_image(pil_image)

        # 构建配置
        config_params = {
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration_seconds": int(duration),
            "person_generation": "allow_adult"
        }
        if negative_prompt:
            config_params["negative_prompt"] = negative_prompt

        config = types.GenerateVideosConfig(**config_params)

        # 调用API生成视频
        operation = client.models.generate_videos(
            model=model,
            prompt=prompt,
            image=image,
            config=config
        )

        # 等待视频生成完成
        video_path = self._wait_and_download_video(
            client=client,
            operation=operation,
            output_dir=output_dir,
            prefix=f"{model.replace('.', '_')}_image2video"
        )

        return video_path

    def _generate_interpolation_video(self, client, prompt, negative_prompt, model,
                                      aspect_ratio, resolution, duration,
                                      first_image, last_image, output_dir):
        """
        首尾帧生成视频模式（仅支持Veo 3.1）
        注意：在 last_frame 插值模式下，aspect_ratio 和 resolution 参数会导致 INVALID_ARGUMENT 错误
        因此仅使用 duration_seconds 和 last_frame 参数
        """
        logger.info(f"[JM-Gemini] Generating interpolation video with model={model}, duration={duration}s")

        # 转换图像为PIL格式，再转为Image格式
        # 使用临时文件方式以确保与工作脚本完全一致
        first_pil = tensor2pil(first_image)
        last_pil = tensor2pil(last_image)

        first_img = pil_to_image_via_file(first_pil)
        last_img = pil_to_image_via_file(last_pil)

        # 构建配置 - 首尾帧插值模式
        # 测试是否支持 aspect_ratio 和 resolution 参数
        config_params = {
            "aspect_ratio": aspect_ratio,
            "resolution": resolution,
            "duration_seconds": int(duration),
            "last_frame": last_img
        }
        if negative_prompt:
            config_params["negative_prompt"] = negative_prompt

        config = types.GenerateVideosConfig(**config_params)

        # 调用API生成视频
        operation = client.models.generate_videos(
            model=model,
            prompt=prompt,
            image=first_img,
            config=config
        )

        # 等待视频生成完成
        video_path = self._wait_and_download_video(
            client=client,
            operation=operation,
            output_dir=output_dir,
            prefix=f"{model.replace('.', '_')}_interpolation"
        )

        return video_path

    def _wait_and_download_video(self, client, operation, output_dir, prefix):
        """
        等待视频生成完成并下载
        """
        # 轮询操作状态直到视频生成完成
        logger.info("[JM-Gemini] Waiting for video generation to complete...")
        poll_count = 0
        max_polls = 120  # 最多等待20分钟 (120 * 10秒)

        while not operation.done:
            if poll_count >= max_polls:
                raise TimeoutError("Video generation timeout after 20 minutes")

            logger.info(f"[JM-Gemini] Polling operation status... ({poll_count + 1}/{max_polls})")
            time.sleep(10)
            operation = client.operations.get(operation)
            poll_count += 1

        logger.info("[JM-Gemini] Video generation completed")

        # 检查是否有错误
        if hasattr(operation, 'error') and operation.error:
            logger.error(f"[JM-Gemini] Operation error: {operation.error}")
            raise RuntimeError(f"Video generation failed with error: {operation.error}")

        # 检查安全过滤
        if hasattr(operation, 'response'):
            if hasattr(operation.response, 'rai_media_filtered_count') and operation.response.rai_media_filtered_count:
                logger.warning(f"[JM-Gemini] {operation.response.rai_media_filtered_count} videos were filtered by safety")
            if hasattr(operation.response, 'rai_media_filtered_reasons') and operation.response.rai_media_filtered_reasons:
                logger.warning(f"[JM-Gemini] Filtered reasons: {operation.response.rai_media_filtered_reasons}")

        # 获取生成的视频
        if not hasattr(operation, 'response') or not hasattr(operation.response, 'generated_videos'):
            raise RuntimeError("No video was generated in the response")

        generated_videos = operation.response.generated_videos
        if not generated_videos or len(generated_videos) == 0:
            raise RuntimeError("No video was generated. This may be due to content safety filters.")

        generated_video = generated_videos[0]

        # 下载视频
        logger.info("[JM-Gemini] Downloading generated video...")
        client.files.download(file=generated_video.video)

        # 保存视频文件
        timestamp = int(time.time())
        file_name = f"{prefix}_{timestamp}.mp4"
        file_path = os.path.join(output_dir, file_name)

        generated_video.video.save(file_path)
        logger.info(f"[JM-Gemini] Video saved to {file_path}")

        return file_path


# 节点类映射
NODE_CLASS_MAPPINGS = {
    "JMGeminiVideoGenerator": JMGeminiVideoGenerator
}

# 节点显示名称映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "JMGeminiVideoGenerator": "JM Gemini Video Generator"
}
