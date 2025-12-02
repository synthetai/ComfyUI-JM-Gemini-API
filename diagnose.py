"""
诊断脚本：检查 google-genai 安装情况
在 Windows 和 Mac 上分别运行此脚本，对比输出结果
"""
import sys
import platform

print("=" * 60)
print("系统信息")
print("=" * 60)
print(f"操作系统: {platform.system()} {platform.release()}")
print(f"Python 版本: {sys.version}")
print(f"Python 路径: {sys.executable}")
print()

print("=" * 60)
print("检查 google-genai 安装")
print("=" * 60)

try:
    import google.genai
    print(f"✓ google.genai 已安装")
    print(f"  版本: {google.genai.__version__ if hasattr(google.genai, '__version__') else '未知'}")
    print(f"  路径: {google.genai.__file__}")
except ImportError as e:
    print(f"✗ google.genai 导入失败: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("检查 google.genai.types 模块")
print("=" * 60)

try:
    from google.genai import types
    print(f"✓ google.genai.types 已导入")
    print(f"  路径: {types.__file__ if hasattr(types, '__file__') else '内置模块'}")
except ImportError as e:
    print(f"✗ google.genai.types 导入失败: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("检查 types 模块中的类/属性")
print("=" * 60)

all_types = dir(types)
image_related = [x for x in all_types if 'image' in x.lower()]
config_related = [x for x in all_types if 'config' in x.lower()]

print(f"所有与 'image' 相关的类型 ({len(image_related)} 个):")
for item in image_related:
    print(f"  - {item}")

print()
print(f"所有与 'config' 相关的类型 ({len(config_related)} 个):")
for item in config_related:
    print(f"  - {item}")

print()
print("=" * 60)
print("检查 ImageConfig 是否存在")
print("=" * 60)

if hasattr(types, 'ImageConfig'):
    print("✓ types.ImageConfig 存在")
    print(f"  类型: {type(types.ImageConfig)}")

    # 尝试查看 ImageConfig 的签名
    try:
        import inspect
        sig = inspect.signature(types.ImageConfig)
        print(f"  签名: {sig}")
    except Exception as e:
        print(f"  无法获取签名: {e}")
else:
    print("✗ types.ImageConfig 不存在")
    print()
    print("可能的替代类型:")
    possible_alternatives = [
        'GenerateImageConfig',
        'ImageGenerationConfig',
        'ContentConfig',
        'GenerateContentConfig'
    ]
    for alt in possible_alternatives:
        if hasattr(types, alt):
            print(f"  ✓ types.{alt} 存在")

print()
print("=" * 60)
print("检查依赖库版本")
print("=" * 60)

dependencies = [
    'pydantic',
    'httpx',
    'google.auth',
    'PIL',
    'numpy',
    'torch'
]

for dep in dependencies:
    try:
        if dep == 'PIL':
            import PIL
            module = PIL
            name = 'Pillow'
        elif dep == 'google.auth':
            import google.auth
            module = google.auth
            name = 'google-auth'
        else:
            module = __import__(dep)
            name = dep

        version = getattr(module, '__version__', '未知')
        print(f"✓ {name}: {version}")
    except ImportError:
        print(f"✗ {name}: 未安装")

print()
print("=" * 60)
print("完成诊断")
print("=" * 60)
