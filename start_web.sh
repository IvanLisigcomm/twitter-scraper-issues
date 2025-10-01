#!/bin/bash
# Twitter爬虫 Web应用启动脚本

echo "================================"
echo "  Twitter爬虫 Web应用启动脚本  "
echo "================================"
echo ""

# 检查Python版本
echo "📌 检查Python版本..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ 错误: 未找到Python"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $PYTHON_VERSION"
echo ""

# 检查是否安装了依赖
echo "📌 检查依赖..."
if ! $PYTHON_CMD -c "import flask" &> /dev/null; then
    echo "⚠️  未安装Flask，正在安装依赖..."
    $PYTHON_CMD -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "✅ 依赖安装完成"
    else
        echo "❌ 依赖安装失败"
        exit 1
    fi
else
    echo "✅ 依赖已安装"
fi
echo ""

# 创建必要的目录
echo "📌 检查目录结构..."
mkdir -p data
mkdir -p templates
mkdir -p static/css
mkdir -p static/js
echo "✅ 目录结构正常"
echo ""

# 启动Flask应用
echo "================================"
echo "🚀 启动Web服务器..."
echo "================================"
echo ""
echo "📍 访问地址: http://localhost:8887"
echo "📍 按 Ctrl+C 停止服务器"
echo "📍 提示: 如果端口被占用，可以修改 app.py 中的端口号"
echo ""

$PYTHON_CMD app.py

