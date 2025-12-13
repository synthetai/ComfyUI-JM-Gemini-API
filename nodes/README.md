# Nodes Directory

This directory contains all Gemini-related custom nodes for ComfyUI.

## File Structure

```
nodes/
├── __init__.py                  # Node registration and export
├── utils.py                     # Shared utility functions
├── jm_gemini_image_node.py     # Image generation node
├── jm_gemini_video_node.py     # Video generation node
└── README.md                    # This file
```

## Current Nodes

### JM Gemini Image Generator (`jm_gemini_image_node.py`)
- Text-to-image generation
- Image-to-image generation
- Image editing
- Support for Gemini image models (gemini-3-pro-image-preview, gemini-2.5-flash-image)

### JM Gemini Video Generator (`jm_gemini_video_node.py`)
- Text-to-video generation
- Image-to-video generation
- First-last frame interpolation (Veo 3.1 only)
- Support for Veo models (veo-3.1-generate-preview, veo-3.1-fast-generate-preview, veo-3.0-generate-001, veo-3.0-fast-generate-001)

## Shared Utilities (`utils.py`)

Common functions used across all nodes:
- `tensor2pil()`: Convert ComfyUI tensor to PIL Image
- `pil2tensor()`: Convert PIL Image to ComfyUI tensor
- `get_output_dir()`: Get ComfyUI output directory

## Adding New Nodes

To add a new Gemini-related node:

1. Create a new Python file in this directory (e.g., `jm_gemini_video_node.py`)

2. Implement your node class with the standard ComfyUI node structure:

```python
class YourNewNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # your inputs
            }
        }

    RETURN_TYPES = ("TYPE",)
    RETURN_NAMES = ("output",)
    FUNCTION = "your_function"
    CATEGORY = "JM-Gemini"

    def your_function(self, ...):
        # your implementation
        pass

# Export mappings
NODE_CLASS_MAPPINGS = {
    "YourNewNode": YourNewNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YourNewNode": "Your Display Name"
}
```

3. Import shared utilities from `utils.py`:

```python
from .utils import tensor2pil, pil2tensor, get_output_dir
```

4. Update `nodes/__init__.py` to import your new node:

```python
from .jm_gemini_image_node import NODE_CLASS_MAPPINGS as IMAGE_NODE_CLASS_MAPPINGS
from .jm_gemini_image_node import NODE_DISPLAY_NAME_MAPPINGS as IMAGE_NODE_DISPLAY_NAME_MAPPINGS

from .jm_gemini_video_node import NODE_CLASS_MAPPINGS as VIDEO_NODE_CLASS_MAPPINGS
from .jm_gemini_video_node import NODE_DISPLAY_NAME_MAPPINGS as VIDEO_NODE_DISPLAY_NAME_MAPPINGS

from .your_new_node import NODE_CLASS_MAPPINGS as YOUR_NODE_CLASS_MAPPINGS
from .your_new_node import NODE_DISPLAY_NAME_MAPPINGS as YOUR_NODE_DISPLAY_NAME_MAPPINGS

# Merge all mappings
NODE_CLASS_MAPPINGS = {
    **IMAGE_NODE_CLASS_MAPPINGS,
    **VIDEO_NODE_CLASS_MAPPINGS,
    **YOUR_NODE_CLASS_MAPPINGS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **IMAGE_NODE_DISPLAY_NAME_MAPPINGS,
    **VIDEO_NODE_DISPLAY_NAME_MAPPINGS,
    **YOUR_NODE_DISPLAY_NAME_MAPPINGS
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

4. Restart ComfyUI to load the new node

## Node Naming Convention

- File name: `jm_gemini_<feature>_node.py`
- Class name: `JMGemini<Feature><Type>`
- Category: `JM-Gemini` (consistent across all nodes)
- Display name: `JM Gemini <Feature> <Type>`

Examples:
- `jm_gemini_image_node.py` → `JMGeminiImageGenerator` → "JM Gemini Image Generator"
- `jm_gemini_video_node.py` → `JMGeminiVideoGenerator` → "JM Gemini Video Generator"
- `jm_gemini_chat_node.py` → `JMGeminiChatProcessor` → "JM Gemini Chat Processor"
