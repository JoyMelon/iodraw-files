#!/bin/bash

echo "💎 奢侈品行业AI面试助手 - 启动脚本"
echo "===================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 请先安装Python 3.8+"
    exit 1
fi

# 检查是否在正确的目录
if [ ! -f "requirements.txt" ]; then
    echo "❌ 请在项目根目录下运行此脚本"
    exit 1
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📚 安装依赖..."
pip install -q -r requirements.txt

echo ""
echo "✅ 环境准备完成！"
echo ""
echo "请按以下步骤启动服务："
echo ""
echo "1. 启动后端服务（在终端1）："
echo "   source venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. 启动前端服务（在终端2）："
echo "   source venv/bin/activate && cd frontend && streamlit run streamlit_app.py"
echo ""
echo "或者，您可以使用 tmux 或 screen 同时运行两个服务。"
echo ""
