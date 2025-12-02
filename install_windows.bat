@echo off
REM Windows 安装脚本 - 安装所有必要的依赖包
REM 请在 ComfyUI 的 Python 环境中运行此脚本

echo ========================================
echo 安装 ComfyUI-JM-Gemini-API 依赖
echo ========================================
echo.

echo [1/3] 卸载旧版本...
pip uninstall google-genai -y

echo.
echo [2/3] 清除 pip 缓存...
pip cache purge

echo.
echo [3/3] 安装所有依赖（包含 Google AI SDK）...
pip install google-genai==1.52.0 google-auth>=2.40.0 google-api-core>=2.25.0 googleapis-common-protos>=1.70.0 google-auth-httplib2>=0.2.0 --no-cache-dir

echo.
echo [4/3] 安装其他依赖...
pip install -r requirements.txt

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 验证安装...
python test_import.py

echo.
pause
