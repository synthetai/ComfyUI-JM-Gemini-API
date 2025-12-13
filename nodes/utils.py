"""
ComfyUI-JM-Gemini-API Utils
Shared utility functions for all nodes
"""

import os
import numpy as np
import torch
from PIL import Image


def tensor2pil(image_tensor):
    """
    将ComfyUI的tensor格式图像转换为PIL Image
    ComfyUI图像格式: (batch, height, width, channels) 值范围0-1
    """
    # 确保是4D tensor
    if len(image_tensor.shape) == 3:
        image_tensor = image_tensor.unsqueeze(0)

    # 转换为numpy并调整值范围到0-255
    image_np = (image_tensor.squeeze(0).cpu().numpy() * 255).astype(np.uint8)

    # 转换为PIL Image
    return Image.fromarray(image_np)


def pil2tensor(image):
    """
    将PIL Image转换为ComfyUI的tensor格式
    返回格式: (batch, height, width, channels) 值范围0-1
    """
    # 确保是RGB模式
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # 转换为numpy数组
    image_np = np.array(image).astype(np.float32) / 255.0

    # 转换为tensor并添加batch维度
    image_tensor = torch.from_numpy(image_np).unsqueeze(0)

    return image_tensor


def get_output_dir():
    """
    获取ComfyUI的output目录
    """
    # ComfyUI的output目录通常在ComfyUI/output
    # 尝试多个可能的路径
    possible_paths = [
        os.path.join(os.getcwd(), "output"),
        os.path.join(os.path.dirname(os.getcwd()), "output"),
        os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "output"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # 如果都不存在，创建当前目录下的output
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
